# Claude Code adapter

`CLAUDE.md` explicitly routes to the shared instructions. Generated
`.claude/skills/` wrappers expose the same canonical skills through Claude's
project skill convention; use `/sdlc-orchestrator` as an explicit entry point.
This uses ordinary file reading rather than assuming Codex's instruction
discovery works in Claude. No hooks, permissions, model choices or tool servers
are installed. Verify loaded instructions and skill discovery in a fresh
Claude Code session; structural validation alone is insufficient.

Use this framework repository on `master`. For another project, install once
with `--adapter claude`, integrate any existing `CLAUDE.md`, then open a fresh
Claude Code session in the application folder. Start each task with
`/sdlc-orchestrator` and your outcome; it selects the relevant procedures.
Installation is not needed for every task. Follow the target project's
authorized Git workflow.

For detailed setup see `docs/ADOPTION.md`. Official sources and review date
are in `docs/RESEARCH_SOURCES.md`.
