# Claude Code adapter

`CLAUDE.md` explicitly routes to the shared instructions. Generated
`.claude/skills/` wrappers expose the same canonical skills through Claude's
project skill convention; use `/sdlc-orch` as an explicit entry point.
This uses ordinary file reading rather than assuming Codex's instruction
discovery works in Claude. No hooks, permissions, model choices or tool servers
are installed. Verify loaded instructions and skill discovery in a fresh
Claude Code session; structural validation alone is insufficient.

Use this framework repository on `master`. For another project, install once
with `--adapter claude`, integrate any existing `CLAUDE.md`, then open a fresh
Claude Code session in the application folder. Start each task with
`/sdlc-orch` and your outcome; it selects the relevant procedures.
Installation is not needed for every task. Follow the target project's
authorized Git workflow.

For detailed setup see `docs/ADOPTION.md`. Official sources and review date
are in `docs/RESEARCH_SOURCES.md`.

With a personal installation, the same entry works in new/existing application
folders without a project copy. Explicit local pins take precedence. For guided
choices follow [project setup](../../docs/PROJECT_SETUP.md); technology/source
checks and store-readiness records use the shared canonical procedures.

For an independent multi-lane review, use `/sdlc-orch review`. Optional subagent
templates are in `adapters/claude/review-cycle/`; they are not installed. Copy the
ones you want into `.claude/agents/` after reading them and see
[the review cycle guide](../../docs/REVIEW_CYCLE.md) for tool and permission notes.

For persisted interactive setup, ask `/sdlc-orch` to start the project wizard.
Use [the runtime guide](../../docs/WIZARD.md) and the selected framework root's
`scripts/project_wizard.py`; the same state works in Codex. No new skill required.
