"""Validate framework structure and optional evidence/RACI records without dependencies."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from sync_adapters import metadata, sync
from agent_eval import load_cases
from review_cycle import starter_files
from wizard_core import load_catalog


def inside_file(root, relative):
    """Resolve a portable relative file path without escaping root, including symlinks."""
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError(f"invalid relative path: {relative!r}")
    path = Path(relative)
    if path.is_absolute() or ":" in relative:
        raise ValueError(f"absolute path refused: {relative}")
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f"missing file or path outside root: {relative}")
    return target


def required_string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected a nonempty string")


def load_json(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def validate_evidence(path, version):
    data = load_json(path)
    if data.get("framework_version") != version:
        raise ValueError("evidence framework_version mismatch")
    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError("evidence checks must be a nonempty array")
    seen = set()
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("check must be an object")
        required_string(check.get("id"), "check id")
        if check["id"] in seen:
            raise ValueError("duplicate check id")
        seen.add(check["id"])
        required_string(check.get("claim"), "claim")
        limits = check.get("limitations")
        if not isinstance(limits, list) or any(not isinstance(x, str) or not x.strip() for x in limits):
            raise ValueError("limitations must be an array of nonempty strings")
        status = check.get("status")
        if status not in ("verified", "failed", "not_run"):
            raise ValueError("invalid evidence status")
        if status == "not_run":
            if not limits or check.get("exit_code") is not None:
                raise ValueError("not_run needs limitations and no exit code")
            continue
        if not isinstance(check.get("revision"), str) or not re.fullmatch(r"[0-9a-f]{40}", check["revision"]):
            raise ValueError("executed check needs a full revision SHA")
        for field in ("timestamp", "environment", "scope", "command"):
            required_string(check.get(field), field)
        stamp = datetime.fromisoformat(check["timestamp"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("timestamp needs a time zone")
        code = check.get("exit_code")
        if type(code) is not int or (status == "verified") != (code == 0):
            raise ValueError("evidence status and exit code disagree")
        inside_file(path.parent, check.get("output"))


def validate_raci(path):
    data = load_json(path)
    roles = data.get("roles")
    if not isinstance(roles, dict) or not roles:
        raise ValueError("roles must be a nonempty object")
    for role_id, role in roles.items():
        required_string(role_id, "role id")
        if not isinstance(role, dict) or role.get("kind") not in ("human", "role", "agent"):
            raise ValueError("invalid role kind")
        required_string(role.get("name"), "role name")
    rows = data.get("assignments")
    if not isinstance(rows, list) or not rows:
        raise ValueError("assignments must be a nonempty array")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("assignment must be an object")
        required_string(row.get("id"), "assignment id")
        required_string(row.get("deliverable"), "deliverable")
        if row["id"] in seen:
            raise ValueError("duplicate assignment id")
        seen.add(row["id"])
        for kind in ("R", "A", "C", "I"):
            values = row.get(kind)
            if not isinstance(values, list) or any(not isinstance(x, str) or x not in roles for x in values):
                raise ValueError(f"{kind}: unregistered role or invalid array")
            if len(values) != len(set(values)):
                raise ValueError(f"{kind}: duplicate role")
        if not row["R"] or len(row["A"]) != 1:
            raise ValueError("each assignment needs responsible executors and exactly one accountable role")
        if roles[row["A"][0]]["kind"] == "agent":
            raise ValueError("an agent cannot be the accountable decision owner")


def validate_links(root, path):
    errors = []
    body = path.read_text(encoding="utf-8")
    # The repository uses inline links; deliberately do not claim a full Markdown parser.
    body = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "", body)
    body = re.sub(r"`+[^`\n]*`+", "", body)
    for match in re.finditer(r"\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)\)", body):
        link = match[1].strip("<>")
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        decoded = unquote(parsed.path)
        try:
            relative = (path.parent / decoded).resolve().relative_to(root.resolve()).as_posix()
            inside_file(root, relative)
        except (ValueError, OSError) as exc:
            errors.append(f"{path.relative_to(root)}: broken or escaping link {link}: {exc}")
    return errors


def validate(root):
    errors = []
    try:
        manifest = load_json(root / "framework.json")
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        if manifest.get("version") != version or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("VERSION and manifest must agree on a semantic version")
        files = manifest.get("required_files")
        skills = manifest.get("skills")
        if not isinstance(files, list) or not files or any(not isinstance(x, str) for x in files):
            raise ValueError("required_files must be a nonempty string array")
        if not isinstance(skills, list) or not skills or any(not isinstance(x, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", x) for x in skills):
            raise ValueError("skills must be a nonempty valid-name array")
        if len(set(files)) != len(files) or len(set(skills)) != len(skills):
            raise ValueError("duplicate manifest entries")
        for relative in files:
            try:
                if not inside_file(root, relative).read_bytes().strip():
                    errors.append(f"empty required file: {relative}")
            except (OSError, ValueError) as exc:
                errors.append(str(exc))
        registered = {f"skills/{name}/SKILL.md" for name in skills}
        actual = {p.relative_to(root).as_posix() for p in (root / "skills").glob("*/SKILL.md")}
        if registered != actual:
            errors.append("canonical skill inventory differs from manifest")
        for name in skills:
            if metadata(inside_file(root, f"skills/{name}/SKILL.md"))[0] != name:
                errors.append(f"skill name mismatch: {name}")
        errors.extend(sync(root, check=True))
        for path in root.rglob("*.md"):
            if ".git" not in path.relative_to(root).parts:
                errors.extend(validate_links(root, path))
        validate_evidence(root / "templates/EVIDENCE.json", version)
        validate_raci(root / "templates/RACI.json")
        load_cases(root / "evals/cases.json")
        load_catalog(root / "wizard/catalog.json")
        starter_files(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--raci", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root)
    for kind, path in (("evidence", args.evidence), ("raci", args.raci)):
        if path is not None:
            try:
                if kind == "evidence":
                    validate_evidence(path.resolve(), (root / "VERSION").read_text().strip())
                else:
                    validate_raci(path.resolve())
            except (OSError, ValueError, KeyError, TypeError) as exc:
                errors.append(f"{kind}: {exc}")
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("Framework structure, templates and adapters validated.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
