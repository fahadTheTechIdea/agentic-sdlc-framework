# Codex adapter

`AGENTS.md` supplies repository instructions. Generated `.agents/skills/` wrappers
expose the canonical skills using Codex's project discovery convention. Invoke
`$sdlc-orchestrator` or describe the task and let the instructions route it.
The wrapper tells the assistant to read the canonical file; it does not copy
policy or alter sandbox/approval settings. Check loaded instructions and skill
availability in a fresh session after adoption.

For another project see `docs/ADOPTION.md`; do not copy this repository's
maintenance-specific `AGENTS.md` over that project's instructions.
Official sources and review date are in `docs/RESEARCH_SOURCES.md`.
