"""Prepare disposable agent tasks and grade selected outcomes; never launches a model."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "evals/cases.json"


def relative_path(value):
    if (not isinstance(value, str) or not value or "\\" in value or ":" in value
            or Path(value).is_absolute() or any(p in ("..", ".") for p in value.split("/"))):
        raise ValueError(f"invalid fixture path: {value!r}")
    return value


def load_cases(path=SUITE):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("expected evaluation schema_version 1")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty array")
    found = {}
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("case must be an object")
        name = relative_path(case.get("id"))
        if "/" in name or name in found:
            raise ValueError("case IDs must be unique single path components")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError("case requires prompt")
        files = case.get("files")
        if not isinstance(files, dict) or not files:
            raise ValueError("case requires fixture files")
        for key, content in files.items():
            relative_path(key)
            if not isinstance(content, str):
                raise ValueError("fixture content must be text")
        editable = case.get("editable")
        if (not isinstance(editable, list) or len(editable) != len(set(editable))
                or any(p not in files for p in editable)):
            raise ValueError("editable must name unique existing fixture files")
        if case.get("test_exit") is not None and (type(case["test_exit"]) is not int or case["test_exit"] not in (0, 1)):
            raise ValueError("test_exit must be null, 0 or 1")
        if case.get("test_exit") is not None and "test_app.py" not in files:
            raise ValueError("executable case requires protected test_app.py")
        if "test_app.py" in editable:
            raise ValueError("grader tests cannot be editable")
        if case.get("status") not in ("complete", "partial", "plan_only"):
            raise ValueError("invalid expected report status")
        rubric = case.get("human_review")
        if not isinstance(rubric, list) or not rubric or any(not isinstance(x, str) or not x.strip() for x in rubric):
            raise ValueError("case requires human review criteria")
        found[name] = case
    return found


def prepare(case, destination):
    """Never overlay an existing directory or symlink."""
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("destination already exists; choose a fresh disposable directory")
    if destination.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("evaluation workspace must be outside the framework source")
    destination.mkdir(parents=True, exist_ok=False)
    for relative, content in case["files"].items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return destination


def grade(case, workspace, report_path):
    """Check protected files before executing candidate Python; this is not a sandbox."""
    workspace = Path(workspace).absolute()
    report_path = Path(report_path).resolve()
    if workspace.is_symlink() or not workspace.is_dir():
        raise ValueError("workspace must be a real directory")
    if report_path.is_relative_to(workspace.resolve()):
        raise ValueError("agent result must be outside the graded workspace")
    if workspace.resolve() == ROOT.resolve() or ROOT.resolve().is_relative_to(workspace.resolve()):
        raise ValueError("cannot grade the framework source or its ancestor")
    failures = []
    observed = set()
    for path in workspace.rglob("*"):
        relative = path.relative_to(workspace)
        if path.is_symlink():
            failures.append(f"symlink refused: {relative.as_posix()}")
            continue
        if not path.is_file() or "__pycache__" in relative.parts:
            continue
        name = relative.as_posix()
        observed.add(name)
        if name not in case["files"]:
            failures.append(f"unexpected file: {name}")
        elif name not in case["editable"]:
            try:
                if path.read_text(encoding="utf-8") != case["files"][name]:
                    failures.append(f"protected file changed: {name}")
            except (UnicodeError, OSError):
                failures.append(f"protected file unreadable: {name}")
    for name in case["files"]:
        if name not in observed:
            failures.append(f"fixture file missing: {name}")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError("agent result must be an object")
    if report.get("status") != case["status"]:
        failures.append(f"expected report status {case['status']}")
    limitations = report.get("limitations")
    if not isinstance(limitations, list) or any(not isinstance(x, str) or not x.strip() for x in limitations):
        failures.append("limitations must be an array of nonempty strings")
    elif case["status"] == "partial" and not limitations:
        failures.append("partial outcome requires a stated limitation")
    if case["status"] == "plan_only" and (not isinstance(report.get("plan"), str) or not report["plan"].strip()):
        failures.append("plan-only result requires a plan")
    execution = None
    # Never run modified/deleted test fixtures or unexpected files.
    if not failures and case["test_exit"] is not None:
        command = [sys.executable, "-B", "-m", "unittest", "-v", "test_app"]
        try:
            # Run a fresh copy of the observed files so host-created bytecode caches
            # cannot substitute stale candidate code for the current source.
            with tempfile.TemporaryDirectory(prefix="sdlc-grade-") as temporary:
                clean = Path(temporary)
                for relative in case["files"]:
                    target = clean / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(workspace / relative, target)
                result = subprocess.run(command, cwd=clean, capture_output=True,
                                        text=True, encoding="utf-8", errors="replace", timeout=15)
            execution = {"command": command, "exit_code": result.returncode,
                         "stdout": result.stdout, "stderr": result.stderr}
            if result.returncode != case["test_exit"]:
                failures.append(f"expected test exit {case['test_exit']}, got {result.returncode}")
        except subprocess.TimeoutExpired:
            failures.append("candidate tests exceeded 15 seconds")
            execution = {"command": command, "exit_code": None, "timeout_seconds": 15}
    return {"case": case["id"], "automated_outcome": "failed" if failures else "passed",
            "failures": failures, "execution": execution, "human_review": "not_run",
            "limitations": ["Selected workspace/report properties only; no model was launched by this tool.",
                            "Agent narrative and external tool actions are not authenticated."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("list", "prepare", "grade"))
    parser.add_argument("--case")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        cases = load_cases()
        if args.action == "list":
            print("\n".join(cases))
            return 0
        if args.case not in cases or args.workspace is None:
            raise ValueError("prepare/grade require a registered --case and --workspace")
        case = cases[args.case]
        if args.action == "prepare":
            prepare(case, args.workspace)
            print(case["prompt"])
            return 0
        if args.report is None:
            raise ValueError("grade requires --report outside the workspace")
        result = grade(case, args.workspace, args.report)
        print(json.dumps(result, indent=2))
        return int(result["automated_outcome"] != "passed")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
