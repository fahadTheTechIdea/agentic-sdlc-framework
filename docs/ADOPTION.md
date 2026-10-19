# Adopt the framework in another project

Start from a reviewed commit or release of this repository. Python 3.11+ is
needed for the supplied tooling. No global skills or account settings change.

```text
python scripts/adopt.py /path/to/project --adapter codex
python scripts/adopt.py /path/to/project --adapter codex --write
```

Use `--adapter claude` or `--adapter generic` for the other hosts. The first
command previews the exact file list; only `--write` writes. The installer
vendors the framework under `.agentic-framework/`, adds selected host skill
wrappers, and creates `AGENTS.md` or `CLAUDE.md` only when missing. If the project
already has that instruction file, it is preserved and an integration snippet
is written inside `.agentic-framework/INTEGRATE.md`. Merge that snippet manually
into the existing instructions and inspect directory overrides. The installer
never overwrites a file, never creates a Git repository, and refuses an existing
framework installation or colliding skill path. Review before committing.

For a second host, use the manual integration approach: create routing wrappers
following `scripts/sync_adapters.py`, with paths prefixed by `.agentic-framework/`,
and merge the snippet into the host instruction file. Do not rerun the installer
over an existing installation. Updates are deliberate reviewed diffs against a
new pinned version; no silent remote updates are implemented in v1.2.

Map your current plans, architecture records, ownership and verification to the
templates. Keep equivalent existing artifacts. Start with one runnable slice,
record evidence, and inspect loaded instructions/skill discovery in a fresh
host session. For generic chats use
`adapters/generic/SESSION_BOOTSTRAP.md`; there is no automatic skill discovery.

To undo adoption, inspect the installation file list and remove only the added
files and any snippet you manually merged. Preserve subsequent project changes.
The installer is not transactional across disk failures; if interrupted, inspect
partial files before retrying. Preflight detects normal collisions before writes.
