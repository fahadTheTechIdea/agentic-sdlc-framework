"""Preview or install a local framework snapshot without overwriting project files."""
import argparse
from pathlib import Path

from sync_adapters import wrappers
from validate_framework import validate


BUNDLE_PATHS = ("core", "skills", "templates", "workflows", "adapters", "docs", "scripts")
BUNDLE_FILES = ("VERSION", "framework.json", "README.md", "LICENSE.txt")


def integration_text():
    return (
        "## Agentic SDLC framework v1.2\n\n"
        "Read `.agentic-framework/core/ENGINEERING_CONSTITUTION.md` and "
        "`.agentic-framework/core/EVIDENCE_POLICY.md`, then "
        "`.agentic-framework/skills/sdlc-orchestrator/SKILL.md`. "
        "Use the framework within the host's instructions and existing project "
        "conventions. Keep project plans in their current locations. "
        "Do not replace project test commands with framework structural checks.\n"
    )


def plan(root, target, adapter):
    if not target.is_dir():
        raise ValueError("target must be an existing project directory")
    if target.resolve() == root.resolve() or target.resolve().is_relative_to(root.resolve()):
        raise ValueError("target must be outside the framework source")
    if (target / ".agentic-framework").exists() or (target / ".agentic-framework").is_symlink():
        raise ValueError("existing framework installation refused; review upgrades manually")
    content = {}
    # Include plans/tests and both wrapper trees so the vendored snapshot validates itself.
    for directory in (*BUNDLE_PATHS, "plans", "tests", ".agents", ".claude", ".github"):
        for source in (root / directory).rglob("*"):
            if source.is_file() and "__pycache__" not in source.parts and source.suffix != ".pyc":
                if source.is_symlink():
                    raise ValueError(f"source symlink refused: {source}")
                content[f".agentic-framework/{source.relative_to(root).as_posix()}"] = source.read_bytes()
    for name in (*BUNDLE_FILES, "AGENTS.md", "CLAUDE.md"):
        content[f".agentic-framework/{name}"] = (root / name).read_bytes()
    instruction = {"codex": "AGENTS.md", "claude": "CLAUDE.md"}.get(adapter)
    snippet = integration_text()
    content[".agentic-framework/INTEGRATE.md"] = snippet.encode("utf-8")
    if instruction and not (target / instruction).exists() and not (target / instruction).is_symlink():
        content[instruction] = snippet.encode("utf-8")
    host = {"codex": ".agents/", "claude": ".claude/"}.get(adapter)
    if host:
        for path, body in wrappers(root, prefix=".agentic-framework/").items():
            if path.startswith(host):
                content[path] = body.encode("utf-8")
    target = target.resolve()
    for relative in content:
        destination = target / relative
        if not destination.resolve().is_relative_to(target):
            raise ValueError(f"destination escapes target: {relative}")
        if destination.exists() or destination.is_symlink():
            raise ValueError(f"destination collision: {relative}")
        for parent in destination.parents:
            if parent == target:
                break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise ValueError(f"unsafe destination parent: {parent}")
    return content


def install(target, content):
    for relative, data in sorted(content.items()):
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also refuses a collision introduced after preflight.
        with path.open("xb") as stream:
            stream.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--adapter", choices=("codex", "claude", "generic"), required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        errors = validate(root)
        if errors:
            raise ValueError("invalid source framework: " + "; ".join(errors))
        content = plan(root, args.target, args.adapter)
        for name in sorted(content):
            print(name)
        if args.write:
            install(args.target, content)
            print("Installed. Review INTEGRATE.md and merge the snippet into existing instructions if needed.")
        else:
            print("Preview only. Add --write to install after reviewing this list.")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
