"""Generate small host wrappers; policy and skill bodies remain canonical."""
import argparse
import json
from pathlib import Path
import re


def metadata(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n", text)
    if not match or len(match[1]) > 64:
        raise ValueError(f"{path}: expected plain name/description frontmatter")
    return match[1], match[2]


def wrappers(root, prefix=""):
    manifest = json.loads((root / "framework.json").read_text(encoding="utf-8"))
    result = {}
    for skill in manifest["skills"]:
        name, description = metadata(root / "skills" / skill / "SKILL.md")
        if name != skill:
            raise ValueError(f"{skill}: folder and skill name differ")
        for host in (".agents", ".claude"):
            result[f"{host}/skills/{skill}/SKILL.md"] = (
                f"---\nname: {name}\ndescription: {description}\n---\n\n"
                "Generated routing wrapper; edit the canonical skill instead.\n\n"
                f"Read `{prefix}skills/{skill}/SKILL.md` from the project root "
                "and follow that procedure within the host's instructions. "
                f"The framework root is `{prefix or '.'}`. "
                "Only load the references relevant to the current request.\n"
            )
    return result


def sync(root, check=False):
    expected = wrappers(root)
    errors = []
    for relative, content in expected.items():
        path = root / relative
        if any(parent.is_symlink() for parent in (path, *path.parents) if parent != root and parent.is_relative_to(root)):
            errors.append(f"symlink wrapper refused: {relative}")
        elif not path.is_file() or path.read_text(encoding="utf-8") != content:
            if check:
                errors.append(f"adapter drift: {relative}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
    for host in (".agents", ".claude"):
        for path in (root / host / "skills").glob("*/SKILL.md"):
            if path.relative_to(root).as_posix() not in expected:
                errors.append(f"unregistered adapter: {path.relative_to(root)}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        errors = sync(root, args.check)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(error)
    if not errors:
        print("Adapter wrappers are synchronized.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
