# Adopt the framework in another project

The framework source is on `master`; the baseline branch has already been merged.
Python 3.11+ and Git are needed for the commands below. No global skills or
account settings change.

## Get the framework source once

Clone into a folder separate from the application you want to build or maintain:

```text
git clone --branch master https://github.com/fahadTheTechIdea/agentic-sdlc-framework.git
cd agentic-sdlc-framework
```

If you already have a clean framework checkout, switch to `master` and update
it with `git pull --ff-only origin master`. Preserve any local changes first.
For a reproducible adoption, record `git rev-parse HEAD` before installation.
Releases are optional; a reviewed commit from master can be used before a release
tag exists. Framework maintenance itself follows `AGENTS.md`: master only.

## Select the application and host

For a new application, create its folder first; the installer requires an existing
directory and does not scaffold application code or initialize Git. For an
existing application, use its repository root and inspect its instructions,
working tree and active plans before integration. Keep the framework source
folder and application folder separate.

Run these commands from the framework source folder. Replace the example path
with the actual application folder:

```text
python scripts/adopt.py "C:\Projects\MyApp" --adapter codex
python scripts/adopt.py "C:\Projects\MyApp" --adapter codex --write
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

## Start the application session

Open a fresh Codex or Claude Code session in the application folder. Confirm
which project instructions were loaded and that `sdlc-orch` is available.
Use `$sdlc-orch` in Codex or `/sdlc-orch` in Claude Code, followed
by the outcome you want. You do not need to call every specialist skill. For
new applications, describe users, outcomes, technology and constraints. For
existing applications, name the feature/fix and ask the orchestrator to extend
the current code and plans. Add "plan only" when implementation is not wanted.

The installer has been tested for file behavior; live host discovery and behavior
remain separate checks. If the skill is missing, verify the selected host's
wrapper directory, existing instruction integration and relevant host settings.
For another task in the same project, use the installed snapshot and current
tracker/handoff. Reinstallation is unnecessary.

Commit and publish the reviewed adoption using the application's own authorized
Git workflow. The framework repository's master-only maintenance rule is not
automatically imposed on adopted applications.

## A second host and framework updates

For a second host, use the manual integration approach: create routing wrappers
following `scripts/sync_adapters.py`, with paths prefixed by `.agentic-framework/`,
and merge the snippet into the host instruction file. Do not rerun the installer
over an existing installation. Updates are deliberate reviewed diffs against a
new pinned version; no silent remote updates are implemented in v1.2.

When adding the second host manually, preserve the installed snapshot. Add only
that host's wrappers using the same canonical skill metadata and paths prefixed
by `.agentic-framework/`; integrate the existing snippet into its root instruction
file. Refuse colliding files instead of overwriting them, and confirm discovery
in the second host. The initial installer does not automate this second-host step.

Map your current plans, architecture records, ownership and verification to the
templates. Keep equivalent existing artifacts. Start with one runnable slice,
record evidence, and inspect loaded instructions/skill discovery in a fresh
host session. For generic chats use
`adapters/generic/SESSION_BOOTSTRAP.md`; there is no automatic skill discovery.

## Undo an adoption

To undo adoption, inspect the installation file list and remove only the added
files and any snippet you manually merged. Preserve subsequent project changes.
The installer is not transactional across disk failures; if interrupted, inspect
partial files before retrying. Preflight detects normal collisions before writes.
