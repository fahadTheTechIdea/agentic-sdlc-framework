# Codex adapter

`AGENTS.md` supplies repository instructions. Generated `.agents/skills/` wrappers
expose the canonical skills using Codex's project discovery convention. Invoke
`$sdlc-orch` or describe the task and let the instructions route it.
The wrapper tells the assistant to read the canonical file; it does not copy
policy or alter sandbox/approval settings. Check loaded instructions and skill
availability in a fresh session after adoption.

Use this framework repository on `master`. For another project, install once
with `--adapter codex`, integrate any existing `AGENTS.md`, then open a fresh
session in the application folder. Start each task with `$sdlc-orch` and
your outcome; it selects the relevant procedures. Installation is not needed
for every task. Follow the target project's authorized Git workflow.

For detailed setup see `docs/ADOPTION.md`; do not copy this repository's
maintenance-specific `AGENTS.md` over that project's instructions.
Official sources and review date are in `docs/RESEARCH_SOURCES.md`.

With a user-level installation, the same entry works in new/existing application
folders without a project copy. Explicit local pins take precedence. For guided
choices follow [project setup](../../docs/PROJECT_SETUP.md); technology/source
checks and store-readiness records use the shared canonical procedures.

For persisted interactive setup, ask `$sdlc-orch` to start the project wizard.
Use [the runtime guide](../../docs/WIZARD.md) and the selected framework root's
`scripts/project_wizard.py`; the same state works in Claude. No new skill required.
