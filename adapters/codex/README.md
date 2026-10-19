# Codex adapter

`AGENTS.md` supplies repository instructions. Generated `.agents/skills/` wrappers
expose the canonical skills using Codex's project discovery convention. Invoke
`$sdlc-orchestrator` or describe the task and let the instructions route it.
The wrapper tells the assistant to read the canonical file; it does not copy
policy or alter sandbox/approval settings. Check loaded instructions and skill
availability in a fresh session after adoption.

Use this framework repository on `master`. For another project, install once
with `--adapter codex`, integrate any existing `AGENTS.md`, then open a fresh
session in the application folder. Start each task with `$sdlc-orchestrator` and
your outcome; it selects the relevant procedures. Installation is not needed
for every task. Follow the target project's authorized Git workflow.

For detailed setup see `docs/ADOPTION.md`; do not copy this repository's
maintenance-specific `AGENTS.md` over that project's instructions.
Official sources and review date are in `docs/RESEARCH_SOURCES.md`.
