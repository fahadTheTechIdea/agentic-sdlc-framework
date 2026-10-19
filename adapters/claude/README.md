# Claude Code adapter

`CLAUDE.md` explicitly routes to the shared instructions. Generated
`.claude/skills/` wrappers expose the same canonical skills through Claude's
project skill convention; use `/sdlc-orchestrator` as an explicit entry point.
This uses ordinary file reading rather than assuming Codex's instruction
discovery works in Claude. No hooks, permissions, model choices or tool servers
are installed. Verify loaded instructions and skill discovery in a fresh
Claude Code session; structural validation alone is insufficient.

For another project see `docs/ADOPTION.md`. Official sources and review date
are in `docs/RESEARCH_SOURCES.md`.
