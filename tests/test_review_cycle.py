"""Gate behavior of the review cycle: waiting, round cap, approver limits, human decisions."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_cycle as rc

REV1, REV2, REV3, REV4 = "1" * 40, "2" * 40, "3" * 40, "4" * 40
WHEN = "2026-10-26T10:00:00+03:00"


def report(lane, number=1, verdict="PASS", revision=REV1, kind="agent", findings=None, **extra):
    doc = {"schema_version": 1, "lane": lane, "round": number, "revision": revision, "verdict": verdict,
           "reviewer": {"kind": kind, "id": f"{lane}-reviewer"}, "reviewed_at": WHEN,
           "checked": ["src/app.py", "criteria AC-1"], "findings": findings or [], "limitations": []}
    doc.update(extra)
    return doc


def major(identifier="CODE-1"):
    return [{"id": identifier, "severity": "major", "summary": "Defect", "location": "src/app.py:3"}]


def approval(number=1, decision="APPROVE", revision=REV1, **extra):
    doc = {"schema_version": 1, "round": number, "revision": revision, "decision": decision,
           "approver": {"kind": "agent", "id": "approver"}, "decided_at": WHEN, "rationale": "Reviewed",
           "checked": ["all lane reports"], "concerns": ["Needs a product decision"] if decision == "ESCALATE" else []}
    doc.update(extra)
    return doc


class CycleCase(unittest.TestCase):
    lanes = "code,security,ux"
    options = {}

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name) / "CHG-1"
        settings = {"change": "CHG-1 Example", "criteria": "spec.md", "lanes": self.lanes, "builder": "builder",
                    "accountable": "owner", "accountable_name": "Project owner", "max_fix_rounds": 2,
                    "no_approver": False, "independent": False, "human_approval": False}
        settings.update(self.options)
        rc.init_cycle(self.dir, **settings)

    def state(self):
        return rc.current_status(self.dir)

    def post(self, *docs):
        status = None
        for doc in docs:
            status = rc.add_report(self.dir, doc)
        return status

    def passing_round(self, number=1, revision=REV1):
        return [report(lane, number, revision=revision) for lane in self.lanes.split(",")]

    def human(self, decision="approve", **extra):
        fields = {"decision": decision, "by": "owner", "origin": "terminal", "statement": "",
                  "rationale": "Accepted", "grant_rounds": 0}
        fields.update(extra)
        return rc.add_decision(self.dir, **fields)


class GateFlowTests(CycleCase):
    def test_new_cycle_waits_for_every_lane(self):
        status = self.state()
        self.assertEqual((status["state"], status["round"], status["missing_lanes"]),
                         ("awaiting_reports", 1, ["code", "security", "ux"]))

    def test_partial_reports_never_advance(self):
        status = self.post(report("code"), report("security"))
        self.assertEqual((status["state"], status["missing_lanes"]), ("awaiting_reports", ["ux"]))

    def test_one_failing_lane_cannot_be_outvoted(self):
        status = self.post(report("code"), report("security", verdict="CHANGES", findings=major("SEC-1")), report("ux"))
        self.assertEqual(status["state"], "resume_builder")
        self.assertEqual(status["next_round"], 2)
        self.assertEqual([f["id"] for f in status["findings"]], ["SEC-1"])

    def test_all_pass_goes_to_approver_then_ready(self):
        self.assertEqual(self.post(*self.passing_round())["state"], "awaiting_approver")
        self.assertEqual(rc.add_approval(self.dir, approval())["state"], "ready_to_deliver")

    def test_approver_escalation_needs_human(self):
        self.post(*self.passing_round())
        status = rc.add_approval(self.dir, approval(decision="ESCALATE"))
        self.assertEqual(status["state"], "needs_human")
        self.assertIn("Needs a product decision", status["reasons"][0])

    def test_changes_then_clean_second_round_reaches_approver(self):
        self.post(report("code", verdict="CHANGES", findings=major()), report("security"), report("ux"))
        status = self.post(*self.passing_round(2, REV2))
        self.assertEqual((status["state"], status["round"]), ("awaiting_approver", 2))

    def test_round_two_requires_a_new_revision(self):
        self.post(report("code", verdict="CHANGES", findings=major()), report("security"), report("ux"))
        with self.assertRaisesRegex(ValueError, "revision did not change"):
            rc.add_report(self.dir, report("code", 2, revision=REV1))
        self.assertFalse((self.dir / "round-2").exists())

    def test_fix_budget_exhaustion_escalates(self):
        for number, revision in ((1, REV1), (2, REV2)):
            status = self.post(report("code", number, "CHANGES", revision, findings=major()),
                               report("security", number, revision=revision), report("ux", number, revision=revision))
            self.assertEqual(status["state"], "resume_builder")
        status = self.post(report("code", 3, "CHANGES", REV3, findings=major()),
                           report("security", 3, revision=REV3), report("ux", 3, revision=REV3))
        self.assertEqual(status["state"], "needs_human")
        self.assertIn("fix budget exhausted: 2 of 2", status["reasons"][0])

    def test_blocked_lane_escalates_even_with_budget_left(self):
        status = self.post(report("code"), report("security", verdict="BLOCKED", limitations=["No access to the threat model"]),
                           report("ux"))
        self.assertEqual(status["state"], "needs_human")
        self.assertIn("No access to the threat model", status["reasons"][0])

    def test_approval_cannot_override_requested_changes(self):
        self.post(report("code", verdict="CHANGES", findings=major()), report("security"), report("ux"))
        with self.assertRaisesRegex(ValueError, "before every lane passed"):
            rc.add_approval(self.dir, approval())

    def test_reports_cannot_continue_past_an_escalation(self):
        self.post(report("code"), report("security", verdict="BLOCKED", limitations=["No access"]), report("ux"))
        with self.assertRaisesRegex(ValueError, "did not end in a builder resume"):
            rc.add_report(self.dir, report("code", 2, revision=REV2))


class ZeroBudgetTests(CycleCase):
    options = {"max_fix_rounds": 0}

    def test_changes_escalate_without_a_builder_round(self):
        status = self.post(report("code", verdict="CHANGES", findings=major()), report("security"), report("ux"))
        self.assertEqual(status["state"], "needs_human")


class ConfigurationTests(CycleCase):
    def test_no_approver_cycle_finishes_after_lanes(self):
        folder = Path(self.temp.name) / "CHG-2"
        rc.init_cycle(folder, change="CHG-2", criteria="spec.md", lanes="code", builder="builder", accountable="owner",
                      accountable_name="Owner", max_fix_rounds=2, no_approver=True, independent=False, human_approval=False)
        self.assertEqual(rc.add_report(folder, report("code"))["state"], "ready_to_deliver")
        with self.assertRaisesRegex(ValueError, "no approver"):
            rc.add_approval(folder, approval())

    def test_init_refuses_to_overwrite_and_rejects_bad_lanes(self):
        base = dict(change="C", criteria="s", lanes="code", builder="b", accountable="o", accountable_name="O",
                    max_fix_rounds=2, no_approver=False, independent=False, human_approval=False)
        with self.assertRaisesRegex(ValueError, "already exists"):
            rc.init_cycle(self.dir, **base)
        for lanes in ("approval", "../escape", "Code", "code,code", ""):
            with self.assertRaises(ValueError, msg=lanes):
                rc.init_cycle(Path(self.temp.name) / "other", **{**base, "lanes": lanes})


class IndependenceTests(CycleCase):
    def test_builder_cannot_review_or_approve_as_another_actor(self):
        with self.assertRaisesRegex(ValueError, "builder cannot review"):
            rc.add_report(self.dir, report("code", reviewer={"kind": "agent", "id": "builder"}))
        self.post(*self.passing_round())
        with self.assertRaisesRegex(ValueError, "builder cannot review or approve"):
            rc.add_approval(self.dir, approval(approver={"kind": "agent", "id": "builder"}))

    def test_self_review_is_accepted_but_labelled_unless_independence_required(self):
        self.assertEqual(self.post(report("code", kind="self"), report("security"), report("ux"))["state"], "awaiting_approver")


class RequiredIndependenceTests(CycleCase):
    options = {"independent": True}

    def test_self_review_does_not_count(self):
        status = self.post(report("code", kind="self"), report("security"), report("ux"))
        self.assertEqual(status["state"], "needs_human")
        self.assertIn("lane code is a self-review", status["reasons"][0])


class ApproverIndependenceTests(CycleCase):
    options = {"independent": True}

    def test_approver_who_reviewed_a_lane_is_refused(self):
        self.post(*self.passing_round())
        with self.assertRaisesRegex(ValueError, "approver cannot also be a lane reviewer"):
            rc.add_approval(self.dir, approval(approver={"kind": "agent", "id": "code-reviewer"}))

    def test_separate_approver_is_accepted(self):
        self.post(*self.passing_round())
        self.assertEqual(rc.add_approval(self.dir, approval())["state"], "ready_to_deliver")


class HumanApprovalRequiredTests(CycleCase):
    options = {"human_approval": True}

    def test_approver_approval_still_waits_for_the_human(self):
        self.post(*self.passing_round())
        self.assertEqual(rc.add_approval(self.dir, approval())["state"], "needs_human")
        self.assertEqual(self.human("approve")["state"], "human_approved")


class RecordIntegrityTests(CycleCase):
    def expect(self, doc, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            rc.add_report(self.dir, doc)

    def test_pass_cannot_carry_serious_findings_or_empty_checks(self):
        self.expect(report("code", findings=major()), "PASS cannot carry")
        self.expect(report("code", checked=[]), "must say what was checked")

    def test_changes_needs_a_serious_finding(self):
        self.expect(report("code", verdict="CHANGES"), "at least one blocker or major")
        minor = [{"id": "C-1", "severity": "minor", "summary": "Style"}]
        self.expect(report("code", verdict="CHANGES", findings=minor), "at least one blocker or major")

    def test_blocked_must_explain(self):
        self.expect(report("code", verdict="BLOCKED"), "must state what prevented")

    def test_unknown_fields_and_values_are_rejected(self):
        self.expect(report("code", surprise=True), "unknown surprise")
        self.expect(report("code", verdict="MAYBE"), "verdict must be")
        self.expect(report("code", revision="abc"), "revision must be")
        self.expect(report("code", reviewed_at="2026-10-26T10:00:00"), "zone")
        self.expect({**report("code"), "lane": "docs"}, "not part of this cycle")

    def test_mixed_revisions_in_one_round_are_rejected(self):
        self.post(report("code"))
        self.expect(report("security", revision=REV2), "different revisions")

    def test_digest_revision_is_accepted(self):
        digest = "sha256:" + "a" * 64
        self.assertEqual(self.post(report("code", revision=digest))["state"], "awaiting_reports")

    def test_a_report_is_never_overwritten(self):
        self.post(report("code"))
        self.expect(report("code", verdict="CHANGES", findings=major()), "already has a code report")
        self.assertEqual(json.loads((self.dir / "round-1/code.json").read_text())["verdict"], "PASS")

    def test_rounds_cannot_be_skipped(self):
        self.expect(report("code", 3, revision=REV3), "cannot start before")

    def test_stray_and_tampered_files_fail_the_status(self):
        (self.dir / "notes.txt").write_text("x", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unexpected entry"):
            self.state()
        (self.dir / "notes.txt").unlink()
        folder = self.dir / "round-1"
        folder.mkdir()
        (folder / "docs.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unexpected entry in round-1"):
            self.state()

    def test_duplicate_json_keys_are_refused(self):
        folder = self.dir / "round-1"
        folder.mkdir()
        (folder / "code.json").write_text('{"verdict": "PASS", "verdict": "CHANGES"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            self.state()

    def test_hand_added_round_after_a_pass_is_detected(self):
        self.post(*self.passing_round())
        rc.write_new(self.dir / "round-2" / "code.json", report("code", 2, revision=REV2))
        with self.assertRaisesRegex(ValueError, "did not end in a builder resume"):
            self.state()

    def test_symlinked_record_is_refused(self):
        target = Path(self.temp.name) / "elsewhere.json"
        target.write_text(json.dumps(report("code")), encoding="utf-8")
        folder = self.dir / "round-1"
        folder.mkdir()
        try:
            (folder / "code.json").symlink_to(target)
        except OSError:
            self.skipTest("OS account cannot create symlinks")
        with self.assertRaisesRegex(ValueError, "link refused"):
            self.state()


class ApprovalIntegrityTests(CycleCase):
    def test_approval_must_match_reviewed_revision(self):
        self.post(*self.passing_round())
        with self.assertRaisesRegex(ValueError, "different revisions"):
            rc.add_approval(self.dir, approval(revision=REV2))

    def test_approve_requires_checks_and_escalate_requires_concerns(self):
        self.post(*self.passing_round())
        with self.assertRaisesRegex(ValueError, "must say what was checked"):
            rc.add_approval(self.dir, approval(checked=[]))
        with self.assertRaisesRegex(ValueError, "must state its concerns"):
            rc.add_approval(self.dir, approval(decision="ESCALATE", concerns=[]))

    def test_only_the_latest_round_takes_an_approval_once(self):
        self.post(*self.passing_round())
        rc.add_approval(self.dir, approval())
        with self.assertRaisesRegex(ValueError, "already has an approval"):
            rc.add_approval(self.dir, approval())
        with self.assertRaisesRegex(ValueError, "name a round that has reports"):
            rc.add_approval(self.dir, approval(number=2))


class HumanDecisionTests(CycleCase):
    def escalate(self):
        self.post(report("code"), report("security", verdict="BLOCKED", limitations=["No access"]), report("ux"))

    def test_decision_needs_an_escalation(self):
        self.post(*self.passing_round())
        with self.assertRaisesRegex(ValueError, "has no escalation"):
            self.human("approve")
        self.assertFalse((self.dir / "decisions").exists())

    def test_approve_and_reject_are_terminal(self):
        self.escalate()
        self.assertEqual(self.human("approve")["state"], "human_approved")
        with self.assertRaisesRegex(ValueError, "more than one"):
            self.human("reject")

    def test_reject(self):
        self.escalate()
        self.assertEqual(self.human("reject")["state"], "human_rejected")

    def test_only_the_accountable_human_can_decide(self):
        self.escalate()
        with self.assertRaisesRegex(ValueError, "only the accountable human owner"):
            self.human("approve", by="builder")

    def test_conversation_origin_must_quote_the_human(self):
        self.escalate()
        with self.assertRaisesRegex(ValueError, "quote the human's words"):
            self.human("approve", origin="conversation")
        self.assertEqual(self.human("approve", origin="conversation", statement="Ship it, I accept the risk.")["state"],
                         "human_approved")

    def test_request_changes_resumes_and_grants_more_rounds(self):
        for number, revision in ((1, REV1), (2, REV2), (3, REV3)):
            self.post(report("code", number, "CHANGES", revision, findings=major(f"C-{number}")),
                      report("security", number, revision=revision), report("ux", number, revision=revision))
        self.assertEqual(self.state()["state"], "needs_human")
        self.assertEqual(self.human("request_changes", grant_rounds=1)["state"], "resume_builder")
        self.post(report("code", 4, "CHANGES", REV4, findings=major("C-4")),
                  report("security", 4, revision=REV4), report("ux", 4, revision=REV4))
        self.assertEqual(self.state()["state"], "resume_builder")

    def test_request_changes_without_a_grant_escalates_again_on_the_next_failure(self):
        for number, revision in ((1, REV1), (2, REV2), (3, REV3)):
            self.post(report("code", number, "CHANGES", revision, findings=major(f"C-{number}")),
                      report("security", number, revision=revision), report("ux", number, revision=revision))
        self.human("request_changes")
        self.post(report("code", 4, "CHANGES", REV4, findings=major("C-4")),
                  report("security", 4, revision=REV4), report("ux", 4, revision=REV4))
        self.assertEqual(self.state()["state"], "needs_human")

    def test_only_request_changes_may_grant_rounds(self):
        self.escalate()
        with self.assertRaisesRegex(ValueError, "only request_changes"):
            self.human("approve", grant_rounds=1)


class HostTemplateTests(unittest.TestCase):
    """The optional Claude/Codex agent templates must stay consistent with the policy."""
    names = {"review-approver", "review-code", "review-security", "review-ui-design", "review-ux"}

    def claude(self):
        for path in sorted((ROOT / "adapters/claude/review-cycle").glob("*.md")):
            head, _, body = path.read_text(encoding="utf-8").partition("\n---\n")
            fields = dict(line.split(": ", 1) for line in head.splitlines()[1:])
            yield path, fields, body

    def test_both_hosts_have_the_same_agents(self):
        self.assertEqual({p.stem for p, _, _ in self.claude()}, self.names)
        self.assertEqual({p.stem for p in (ROOT / "adapters/codex/review-cycle").glob("*.toml")}, self.names)

    def test_claude_templates_are_read_only_and_point_at_the_contract(self):
        for path, fields, body in self.claude():
            with self.subTest(path.name):
                self.assertEqual(fields["name"], path.stem)
                tools = {t.strip() for t in fields["tools"].split(",")}
                self.assertLessEqual(tools, {"Read", "Grep", "Glob", "Bash"})
                self.assertIn("templates/review-cycle/", body)
                self.assertIn("Do not edit", body)

    def test_codex_templates_have_the_documented_fields(self):
        import tomllib
        for path in sorted((ROOT / "adapters/codex/review-cycle").glob("*.toml")):
            with self.subTest(path.name):
                data = tomllib.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(set(data), {"name", "description", "developer_instructions"})
                self.assertEqual(data["name"], path.stem)
                self.assertIn("templates/review-cycle/", data["developer_instructions"])

    def test_every_template_lane_is_defined_in_the_policy(self):
        policy = (ROOT / "core/REVIEW_CYCLE.md").read_text(encoding="utf-8")
        for name in self.names - {"review-approver"}:
            self.assertIn(f"| `{name[len('review-'):]}` |", policy)


class DeliveryCheckTests(CycleCase):
    lanes = "code,security"

    def clear_round(self, revision=REV1):
        self.post(*self.passing_round(revision=revision))
        rc.add_approval(self.dir, approval(revision=revision))

    def test_status_reports_the_reviewed_revision(self):
        self.post(report("code"))
        self.assertEqual(self.state()["revision"], REV1)

    def test_the_reviewed_revision_is_deliverable(self):
        self.clear_round()
        self.assertEqual(rc.check_delivery(self.dir, REV1)["state"], "ready_to_deliver")

    def test_a_different_revision_is_refused(self):
        self.clear_round()
        with self.assertRaisesRegex(ValueError, "not " + REV2):
            rc.check_delivery(self.dir, REV2)

    def test_a_state_that_is_not_deliverable_is_refused(self):
        self.post(*self.passing_round())
        with self.assertRaisesRegex(ValueError, "awaiting_approver"):
            rc.check_delivery(self.dir, REV1)

    def test_a_rejected_revision_is_refused(self):
        self.post(report("code"), report("security", verdict="BLOCKED", limitations=["No access"]))
        self.human("reject")
        with self.assertRaisesRegex(ValueError, "human_rejected"):
            rc.check_delivery(self.dir, REV1)

    def test_a_human_approved_revision_is_deliverable(self):
        self.post(report("code"), report("security", verdict="BLOCKED", limitations=["No access"]))
        self.human("approve")
        self.assertEqual(rc.check_delivery(self.dir, REV1)["state"], "human_approved")

    def test_a_malformed_revision_is_refused(self):
        self.clear_round()
        with self.assertRaisesRegex(ValueError, "revision must be"):
            rc.check_delivery(self.dir, "HEAD")

    def test_a_revision_built_after_changes_is_the_one_delivered(self):
        self.post(report("code", verdict="CHANGES", findings=major()), report("security"))
        self.clear_round_two()
        with self.assertRaisesRegex(ValueError, "not " + REV1):
            rc.check_delivery(self.dir, REV1)
        self.assertEqual(rc.check_delivery(self.dir, REV2)["revision"], REV2)

    def clear_round_two(self):
        self.post(*self.passing_round(2, REV2))
        rc.add_approval(self.dir, approval(2, revision=REV2))


class TemplateAndCliTests(unittest.TestCase):
    def test_starter_templates_match_the_contract(self):
        self.assertEqual(rc.starter_files(ROOT), ["approval.json", "cycle.json", "human-decision.json", "lane-report.json"])

    def test_framework_validator_rejects_a_drifted_starter_record(self):
        from validate_framework import validate
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "framework"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            self.assertEqual(validate(copy), [])
            path = copy / "templates/review-cycle/lane-report.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            del data["checked"]
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("lane-report.json" in error for error in validate(copy)))

    def test_cli_runs_the_whole_flow(self):
        with tempfile.TemporaryDirectory() as temp:
            folder, script = Path(temp) / "CHG-9", str(ROOT / "scripts/review_cycle.py")

            def run(*args):
                return subprocess.run([sys.executable, script, *args], capture_output=True, text=True)

            result = run("init", str(folder), "--change", "CHG-9", "--criteria", "spec.md", "--lanes", "code,security",
                         "--builder", "builder", "--accountable", "owner", "--accountable-name", "Owner")
            self.assertEqual(result.returncode, 0, result.stderr)
            for lane in ("code", "security"):
                path = Path(temp) / f"{lane}.json"
                path.write_text(json.dumps(report(lane)), encoding="utf-8")
                result = run("report", str(folder), "--file", str(path))
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("awaiting_approver", result.stdout)
            result = run("status", str(folder), "--json")
            self.assertEqual(json.loads(result.stdout)["state"], "awaiting_approver")
            blocked = run("deliver-check", str(folder), "--revision", REV1)
            self.assertEqual(blocked.returncode, 1)
            self.assertIn("awaiting_approver", blocked.stderr)
            approved = Path(temp) / "approval.json"
            approved.write_text(json.dumps(approval()), encoding="utf-8")
            self.assertEqual(run("recommend", str(folder), "--file", str(approved)).returncode, 0)
            self.assertEqual(run("deliver-check", str(folder), "--revision", REV1).returncode, 0)
            self.assertEqual(run("deliver-check", str(folder), "--revision", REV2).returncode, 1)
            repeat = run("report", str(folder), "--file", str(Path(temp) / "code.json"))
            self.assertEqual(repeat.returncode, 1)
            self.assertIn("ERROR:", repeat.stderr)
            self.assertNotIn("Traceback", repeat.stderr)


if __name__ == "__main__":
    unittest.main()
