"""Review-cycle gate: lane reports, bounded builder rounds, approver and human decision.

The gate reads a record directory and reports the next state. It never launches an
agent, merges, or authenticates who wrote a file; see core/REVIEW_CYCLE.md.
"""
import argparse
import json
from pathlib import Path
import re
import sys

from wizard_core import ID, nonempty, read_json, redirected, require, stamp, zoned_timestamp

SCHEMA = 1
LANE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FINDING_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")
RESERVED_LANES = ("approval",)
REVISION = re.compile(r"(?:[0-9a-f]{40}|sha256:[0-9a-f]{64})\Z")
ROUND_DIR = re.compile(r"round-([1-9][0-9]*)\Z")
DECISION_FILE = re.compile(r"([0-9]{3})\.json\Z")
VERDICTS = ("PASS", "CHANGES", "BLOCKED")
SEVERITIES = ("blocker", "major", "minor")
REVIEWER_KINDS = ("agent", "human", "self")
APPROVER_KINDS = ("agent", "human")
APPROVAL_DECISIONS = ("APPROVE", "ESCALATE")
HUMAN_DECISIONS = ("approve", "reject", "request_changes")
ORIGINS = ("terminal", "conversation")

CYCLE_KEYS = {"schema_version", "change", "criteria", "created_at", "lanes", "builder", "accountable",
              "max_fix_rounds", "approver_required", "independent_review_required", "human_approval_required"}
REPORT_KEYS = {"schema_version", "lane", "round", "revision", "verdict", "reviewer", "reviewed_at",
               "checked", "findings", "limitations"}
APPROVAL_KEYS = {"schema_version", "round", "revision", "decision", "approver", "decided_at",
                 "rationale", "checked", "concerns"}
DECISION_KEYS = {"schema_version", "seq", "round", "decision", "by", "decided_at", "origin",
                 "statement", "rationale", "grant_rounds"}

NEXT = {
    "awaiting_reports": "Collect a report from every missing lane, each reviewing the same revision.",
    "resume_builder": "Builder addresses the listed findings and produces a new revision; then start the next round.",
    "awaiting_approver": "Approver reviews the passing round and records APPROVE or ESCALATE.",
    "ready_to_deliver": "Deliver through the project's authorized Git workflow. This is a gate result, not a merge.",
    "needs_human": "The accountable human decides: approve, reject or request_changes.",
    "human_approved": "Deliver through the project's authorized Git workflow.",
    "human_rejected": "Stop. Do not deliver this revision.",
}


def exact(data, required, optional, label):
    require(isinstance(data, dict), f"{label}: expected an object")
    missing, extra = required - set(data), set(data) - required - optional
    require(not missing, f"{label}: missing {', '.join(sorted(missing))}")
    require(not extra, f"{label}: unknown {', '.join(sorted(extra))}")
    require(data["schema_version"] == SCHEMA and type(data["schema_version"]) is int,
            f"{label}: unsupported schema_version")


def text_list(value, label, minimum=0):
    require(isinstance(value, list) and all(nonempty(x) for x in value), f"{label}: expected nonempty strings")
    require(len(value) >= minimum, f"{label}: needs at least {minimum} entr{'y' if minimum == 1 else 'ies'}")


def whole(value, label, minimum):
    require(type(value) is int and value >= minimum, f"{label}: expected an integer >= {minimum}")


def check_cycle(data):
    exact(data, CYCLE_KEYS, set(), "cycle")
    for key in ("change", "criteria"):
        require(nonempty(data[key]), f"cycle: {key} needs text")
    zoned_timestamp(data["created_at"])
    lanes = data["lanes"]
    require(isinstance(lanes, list) and lanes and len(set(lanes)) == len(lanes), "cycle: lanes need unique entries")
    for lane in lanes:
        require(isinstance(lane, str) and LANE.fullmatch(lane) and lane not in RESERVED_LANES,
                f"cycle: invalid lane {lane!r}")
    exact_ident(data["builder"], {"id"}, "cycle builder")
    exact_ident(data["accountable"], {"id", "name"}, "cycle accountable")
    require(nonempty(data["accountable"]["name"]), "cycle accountable: name needs text")
    whole(data["max_fix_rounds"], "cycle: max_fix_rounds", 0)
    for key in ("approver_required", "independent_review_required", "human_approval_required"):
        require(type(data[key]) is bool, f"cycle: {key} must be true or false")
    return data


def exact_ident(data, keys, label, optional=()):
    require(isinstance(data, dict) and set(keys) <= set(data) <= set(keys) | set(optional), f"{label}: invalid fields")
    require(isinstance(data["id"], str) and ID.fullmatch(data["id"]), f"{label}: invalid id")


def check_person(person, kinds, builder, label):
    exact_ident(person, {"kind", "id"}, label, optional={"model"})
    require(person["kind"] in kinds, f"{label}: kind must be one of {', '.join(kinds)}")
    require("model" not in person or nonempty(person["model"]), f"{label}: model needs text")
    require(person["kind"] == "self" or person["id"] != builder["id"], f"{label}: the builder cannot review or approve its own work")


def check_report(cycle, doc, round_no, lane):
    label = f"round {round_no} {lane}"
    exact(doc, REPORT_KEYS, set(), label)
    require(doc["lane"] == lane and lane in cycle["lanes"], f"{label}: lane does not match its place in the cycle")
    require(doc["round"] == round_no and type(doc["round"]) is int, f"{label}: round does not match its directory")
    require(isinstance(doc["revision"], str) and REVISION.fullmatch(doc["revision"]),
            f"{label}: revision must be a 40-hex commit or sha256:<64-hex> patch digest")
    require(doc["verdict"] in VERDICTS, f"{label}: verdict must be one of {', '.join(VERDICTS)}")
    check_person(doc["reviewer"], REVIEWER_KINDS, cycle["builder"], f"{label} reviewer")
    zoned_timestamp(doc["reviewed_at"])
    text_list(doc["checked"], f"{label} checked")
    text_list(doc["limitations"], f"{label} limitations")
    require(isinstance(doc["findings"], list), f"{label}: findings must be an array")
    ids = set()
    for finding in doc["findings"]:
        exact_finding(finding, label)
        require(finding["id"] not in ids, f"{label}: duplicate finding {finding['id']}")
        ids.add(finding["id"])
    serious = [f for f in doc["findings"] if f["severity"] in ("blocker", "major")]
    if doc["verdict"] == "PASS":
        require(not serious, f"{label}: PASS cannot carry blocker or major findings")
        require(doc["checked"], f"{label}: PASS must say what was checked")
    elif doc["verdict"] == "CHANGES":
        require(serious, f"{label}: CHANGES needs at least one blocker or major finding")
        require(doc["checked"], f"{label}: CHANGES must say what was checked")
    else:
        require(doc["limitations"], f"{label}: BLOCKED must state what prevented the review")


def exact_finding(finding, label):
    require(isinstance(finding, dict) and {"id", "severity", "summary"} <= set(finding)
            <= {"id", "severity", "summary", "location", "evidence"}, f"{label}: invalid finding fields")
    require(isinstance(finding["id"], str) and FINDING_ID.fullmatch(finding["id"]), f"{label}: invalid finding id")
    require(finding["severity"] in SEVERITIES, f"{label}: finding severity must be one of {', '.join(SEVERITIES)}")
    for key in ("summary", "location", "evidence"):
        require(key not in finding or nonempty(finding[key]), f"{label}: finding {key} needs text")


def check_approval(cycle, doc, round_no):
    label = f"round {round_no} approval"
    exact(doc, APPROVAL_KEYS, set(), label)
    require(doc["round"] == round_no and type(doc["round"]) is int, f"{label}: round does not match its directory")
    require(isinstance(doc["revision"], str) and REVISION.fullmatch(doc["revision"]), f"{label}: invalid revision")
    require(doc["decision"] in APPROVAL_DECISIONS, f"{label}: decision must be APPROVE or ESCALATE")
    check_person(doc["approver"], APPROVER_KINDS, cycle["builder"], f"{label} approver")
    zoned_timestamp(doc["decided_at"])
    require(nonempty(doc["rationale"]), f"{label}: rationale needs text")
    text_list(doc["checked"], f"{label} checked")
    text_list(doc["concerns"], f"{label} concerns")
    if doc["decision"] == "APPROVE":
        require(doc["checked"], f"{label}: APPROVE must say what was checked")
    else:
        require(doc["concerns"], f"{label}: ESCALATE must state its concerns")


def check_decision(cycle, doc, seq):
    label = f"decision {seq:03}"
    exact(doc, DECISION_KEYS, set(), label)
    require(doc["seq"] == seq and type(doc["seq"]) is int, f"{label}: seq does not match its file")
    whole(doc["round"], f"{label}: round", 1)
    require(doc["decision"] in HUMAN_DECISIONS, f"{label}: decision must be one of {', '.join(HUMAN_DECISIONS)}")
    require(doc["by"] == cycle["accountable"]["id"], f"{label}: only the accountable human {cycle['accountable']['id']} can decide")
    zoned_timestamp(doc["decided_at"])
    require(doc["origin"] in ORIGINS, f"{label}: origin must be terminal or conversation")
    require(isinstance(doc["statement"], str), f"{label}: statement must be text")
    require(doc["origin"] == "terminal" or nonempty(doc["statement"]),
            f"{label}: a decision recorded from conversation must quote the human's words in statement")
    require(nonempty(doc["rationale"]), f"{label}: rationale needs text")
    whole(doc["grant_rounds"], f"{label}: grant_rounds", 0)
    require(doc["grant_rounds"] == 0 or doc["decision"] == "request_changes", f"{label}: only request_changes can grant rounds")


def read_record(path):
    require(path.is_file() and not redirected(path), f"missing record file or link refused: {path.name}")
    return read_json(path)


def load(root):
    """Parse every file and check it on its own; cross-file rules belong to evaluate()."""
    root = Path(root)
    require(root.is_dir() and not redirected(root), "review record folder not found")
    cycle = check_cycle(read_record(root / "cycle.json"))
    rounds, decisions = {}, []
    for entry in sorted(root.iterdir(), key=lambda p: p.name):
        require(not redirected(entry), f"link refused: {entry.name}")
        match = ROUND_DIR.fullmatch(entry.name)
        if entry.name == "cycle.json":
            continue
        if match and entry.is_dir():
            number = int(match[1])
            rounds[number] = {"reports": {}, "approval": None}
            for item in sorted(entry.iterdir(), key=lambda p: p.name):
                lane = item.name[:-5] if item.name.endswith(".json") else ""
                require(lane and (lane == "approval" or lane in cycle["lanes"]),
                        f"unexpected entry in {entry.name}: {item.name}")
                doc = read_record(item)
                if lane == "approval":
                    check_approval(cycle, doc, number)
                    rounds[number]["approval"] = doc
                else:
                    check_report(cycle, doc, number, lane)
                    rounds[number]["reports"][lane] = doc
        elif entry.name == "decisions" and entry.is_dir():
            files = sorted(entry.iterdir(), key=lambda p: p.name)
            for position, item in enumerate(files, 1):
                found = DECISION_FILE.fullmatch(item.name)
                require(found and int(found[1]) == position, f"decisions must be numbered 001.json upward: {item.name}")
                doc = read_record(item)
                check_decision(cycle, doc, position)
                decisions.append(doc)
        else:
            raise ValueError(f"unexpected entry: {entry.name}")
    require(sorted(rounds) == list(range(1, len(rounds) + 1)), "round folders must be numbered 1..N without gaps")
    return cycle, rounds, decisions


def round_revision(rd):
    docs = [*rd["reports"].values(), *([rd["approval"]] if rd["approval"] else [])]
    revisions = {d["revision"] for d in docs}
    return docs, revisions


def lanes_clear(cycle, rd):
    """True when every lane reported PASS and none is an unacceptable self-review."""
    return all(l in rd["reports"] and rd["reports"][l]["verdict"] == "PASS"
               and not (cycle["independent_review_required"] and rd["reports"][l]["reviewer"]["kind"] == "self")
               for l in cycle["lanes"])


def findings_of(rd):
    return [{"lane": lane, **f} for lane, doc in rd["reports"].items() for f in doc["findings"]]


def pre_human_state(cycle, rd, used, allowed):
    missing = [lane for lane in cycle["lanes"] if lane not in rd["reports"]]
    if missing:
        return {"state": "awaiting_reports", "missing_lanes": missing}
    reasons = []
    for lane in cycle["lanes"]:
        doc = rd["reports"][lane]
        if doc["verdict"] == "BLOCKED":
            reasons.append(f"lane {lane} could not complete: {doc['limitations'][0]}")
        if cycle["independent_review_required"] and doc["reviewer"]["kind"] == "self":
            reasons.append(f"independent review is required but lane {lane} is a self-review")
    changes = [lane for lane in cycle["lanes"] if rd["reports"][lane]["verdict"] == "CHANGES"]
    if reasons:
        return {"state": "needs_human", "reasons": reasons, "findings": findings_of(rd)}
    if changes:
        if used < allowed:
            return {"state": "resume_builder", "changes_from": changes, "findings": findings_of(rd)}
        return {"state": "needs_human", "findings": findings_of(rd),
                "reasons": [f"fix budget exhausted: {used} of {allowed} automatic builder resumptions used and lanes still request changes: {', '.join(changes)}"]}
    if cycle["approver_required"]:
        approval = rd["approval"]
        if approval is None:
            return {"state": "awaiting_approver"}
        if approval["decision"] == "ESCALATE":
            return {"state": "needs_human", "reasons": ["approver escalated: " + c for c in approval["concerns"]]}
    if cycle["human_approval_required"]:
        return {"state": "needs_human", "reasons": ["the cycle requires the accountable human's approval"]}
    return {"state": "ready_to_deliver"}


def evaluate(cycle, rounds, decisions):
    """Cross-file rules and the resulting state; raises ValueError for an inconsistent record."""
    count = len(rounds)
    require(all(d["round"] <= count for d in decisions), "a decision refers to a round that has no reports")
    if count == 0:
        return {"state": "awaiting_reports", "round": 1, "missing_lanes": list(cycle["lanes"])}
    # A human-requested resumption is the human's decision, so it never spends the automatic budget.
    grants, used, previous, outcome = 0, 0, None, None
    for number in range(1, count + 1):
        rd = rounds[number]
        docs, revisions = round_revision(rd)
        require(len(revisions) <= 1, f"round {number}: reports review different revisions")
        revision = next(iter(revisions), None)
        if previous is not None and revision is not None:
            require(revision != previous, f"round {number}: the builder was resumed but the revision did not change")
        if rd["approval"] is not None:
            require(cycle["approver_required"], f"round {number}: an approval exists but the cycle has no approver")
            require(lanes_clear(cycle, rd), f"round {number}: approval recorded before every lane passed independently")
        outcome = pre_human_state(cycle, rd, used, cycle["max_fix_rounds"] + grants)
        answers = [d for d in decisions if d["round"] == number]
        require(len(answers) <= 1, f"round {number}: more than one human decision")
        if answers:
            doc = answers[0]
            require(outcome["state"] == "needs_human", f"decision {doc['seq']:03} answers round {number}, which has no escalation")
            grants += doc["grant_rounds"]
            state = {"approve": "human_approved", "reject": "human_rejected", "request_changes": "resume_builder"}[doc["decision"]]
            outcome = {**outcome, "state": state, "decision": doc["decision"], "rationale": doc["rationale"]}
        elif outcome["state"] == "resume_builder":
            used += 1
        if outcome["state"] == "resume_builder":
            outcome["next_round"] = number + 1
        if number < count:
            require(outcome["state"] == "resume_builder", f"round {number + 1} exists but round {number} did not end in a builder resume")
        if revision is not None:
            previous = revision
    last = rounds[count]
    limits = sorted({lim for doc in last["reports"].values() for lim in doc["limitations"]})
    reviewed = {"revision": previous} if previous is not None else {}
    return {"round": count, "limitations": limits, **reviewed, **outcome}


DELIVERABLE = ("ready_to_deliver", "human_approved")


def check_delivery(root, revision):
    """Return the status when the gate allows delivering exactly this revision; otherwise raise."""
    require(isinstance(revision, str) and REVISION.fullmatch(revision),
            "revision must be a 40-hex commit or sha256:<64-hex> patch digest")
    status = current_status(root)
    require(status["state"] in DELIVERABLE, f"not deliverable: the gate state is {status['state']}")
    require(status.get("revision") == revision,
            f"the gate reviewed {status.get('revision')}, not {revision}; run a new round on the revision to deliver")
    return status


def write_new(path, data):
    """Create exclusively so an earlier verdict or decision can never be replaced."""
    path = Path(path)
    require(not redirected(path.parent), f"link refused: {path.parent.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    except FileExistsError as exc:
        raise ValueError(f"{path.name} already exists and is never overwritten") from exc


def current_status(root):
    cycle, rounds, decisions = load(root)
    return evaluate(cycle, rounds, decisions)


def init_cycle(root, **fields):
    root = Path(root)
    lanes = [x.strip() for x in fields["lanes"].split(",")]
    cycle = {"schema_version": SCHEMA, "change": fields["change"], "criteria": fields["criteria"],
             "created_at": stamp(), "lanes": lanes, "builder": {"id": fields["builder"]},
             "accountable": {"id": fields["accountable"], "name": fields["accountable_name"]},
             "max_fix_rounds": fields["max_fix_rounds"], "approver_required": not fields["no_approver"],
             "independent_review_required": fields["independent"], "human_approval_required": fields["human_approval"]}
    check_cycle(cycle)
    write_new(root / "cycle.json", cycle)
    return cycle


def add_report(root, doc):
    cycle, rounds, decisions = load(root)
    number, lane = doc.get("round"), doc.get("lane")
    require(type(number) is int and number >= 1 and isinstance(lane, str), "report needs integer round and lane")
    require(number <= len(rounds) + 1, f"round {number} cannot start before round {len(rounds)} ends")
    rd = rounds.setdefault(number, {"reports": {}, "approval": None})
    require(lane in cycle["lanes"], f"lane {lane!r} is not part of this cycle")
    require(lane not in rd["reports"], f"round {number} already has a {lane} report; start a new round instead of re-running it")
    check_report(cycle, doc, number, lane)
    rd["reports"][lane] = doc
    status = evaluate(cycle, rounds, decisions)
    write_new(Path(root) / f"round-{number}" / f"{lane}.json", doc)
    return status


def add_approval(root, doc):
    cycle, rounds, decisions = load(root)
    number = doc.get("round")
    require(type(number) is int and number in rounds, "approval must name a round that has reports")
    require(number == len(rounds), "only the latest round can be approved")
    require(rounds[number]["approval"] is None, f"round {number} already has an approval")
    check_approval(cycle, doc, number)
    rounds[number]["approval"] = doc
    status = evaluate(cycle, rounds, decisions)
    write_new(Path(root) / f"round-{number}" / "approval.json", doc)
    return status


def add_decision(root, **fields):
    cycle, rounds, decisions = load(root)
    require(rounds, "there is no round to decide")
    doc = {"schema_version": SCHEMA, "seq": len(decisions) + 1, "round": len(rounds), "decision": fields["decision"],
           "by": fields["by"], "decided_at": stamp(), "origin": fields["origin"], "statement": fields["statement"],
           "rationale": fields["rationale"], "grant_rounds": fields["grant_rounds"]}
    check_decision(cycle, doc, doc["seq"])
    decisions.append(doc)
    status = evaluate(cycle, rounds, decisions)
    write_new(Path(root) / "decisions" / f"{doc['seq']:03}.json", doc)
    return status


def render(status):
    lines = [f"State: {status['state']} (round {status['round']})", f"Next: {NEXT[status['state']]}"]
    if "revision" in status:
        lines.append(f"Reviewed revision: {status['revision']}")
    if status.get("missing_lanes"):
        lines.append("Missing lanes: " + ", ".join(status["missing_lanes"]))
    if "next_round" in status:
        lines.append(f"Next round: {status['next_round']}")
    for reason in status.get("reasons", []):
        lines.append(f"Reason: {reason}")
    for item in status.get("findings", []):
        place = f" [{item['location']}]" if "location" in item else ""
        lines.append(f"Finding {item['lane']}/{item['id']} ({item['severity']}){place}: {item['summary']}")
    for limit in status.get("limitations", []):
        lines.append(f"Limitation: {limit}")
    return "\n".join(lines)


def starter_files(root):
    folder = Path(root) / "templates/review-cycle"
    shapes = {"cycle.json": CYCLE_KEYS, "lane-report.json": REPORT_KEYS,
              "approval.json": APPROVAL_KEYS, "human-decision.json": DECISION_KEYS}
    for name, keys in shapes.items():
        data = read_record(folder / name)
        require(isinstance(data, dict) and set(data) == keys and data["schema_version"] == SCHEMA,
                f"templates/review-cycle/{name}: fields differ from the record contract")
    return sorted(shapes)


def parser():
    top = argparse.ArgumentParser(description=__doc__)
    sub = top.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create cycle.json in a new record folder")
    init.add_argument("folder", type=Path)
    init.add_argument("--change", required=True, help="change identifier and short title")
    init.add_argument("--criteria", required=True, help="path or tracker locator of the acceptance criteria")
    init.add_argument("--lanes", required=True, help="comma-separated lane ids, for example code,security,ux,ui-design")
    init.add_argument("--builder", required=True, help="id of the builder; it cannot review or approve")
    init.add_argument("--accountable", required=True, help="id of the accountable human or role")
    init.add_argument("--accountable-name", required=True)
    init.add_argument("--max-fix-rounds", type=int, default=2)
    init.add_argument("--no-approver", action="store_true", help="skip the approver step")
    init.add_argument("--independent", action="store_true", help="refuse builder self-review as a pass")
    init.add_argument("--human-approval", action="store_true", help="always end in a human decision")
    for name, text in (("report", "record one lane report"), ("recommend", "record the approver's decision")):
        item = sub.add_parser(name, help=text)
        item.add_argument("folder", type=Path)
        item.add_argument("--file", type=Path, required=True, help="JSON written by the reviewer or approver")
    decide = sub.add_parser("decide", help="record the accountable human's decision")
    decide.add_argument("folder", type=Path)
    decide.add_argument("--by", required=True)
    decide.add_argument("--decision", choices=HUMAN_DECISIONS, required=True)
    decide.add_argument("--rationale", required=True)
    decide.add_argument("--origin", choices=ORIGINS, required=True,
                        help="terminal: the human ran this; conversation: an assistant records words the human just wrote")
    decide.add_argument("--statement", default="", help="the human's own words; required for --origin conversation")
    decide.add_argument("--grant-rounds", type=int, default=0)
    check = sub.add_parser("deliver-check", help="exit 0 only when this exact revision may be delivered")
    check.add_argument("folder", type=Path)
    check.add_argument("--revision", required=True, help="the commit or patch digest about to be delivered")
    status = sub.add_parser("status", help="validate the record and show the state and next action")
    status.add_argument("folder", type=Path)
    status.add_argument("--json", action="store_true")
    return top


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            init_cycle(args.folder, **{k: v for k, v in vars(args).items() if k not in ("command", "folder")})
            print(f"Created {args.folder / 'cycle.json'}")
            return 0
        if args.command == "report":
            status = add_report(args.folder, read_record(args.file))
        elif args.command == "recommend":
            status = add_approval(args.folder, read_record(args.file))
        elif args.command == "decide":
            status = add_decision(args.folder, decision=args.decision, by=args.by, origin=args.origin,
                                  statement=args.statement, rationale=args.rationale, grant_rounds=args.grant_rounds)
        elif args.command == "deliver-check":
            status = check_delivery(args.folder, args.revision)
        else:
            status = current_status(args.folder)
        print(json.dumps(status, indent=2) if getattr(args, "json", False) else render(status))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
