# Repository instructions

Read `core/ENGINEERING_CONSTITUTION.md` and `core/EVIDENCE_POLICY.md` before
substantive work. Use `skills/sdlc-orchestrator/SKILL.md` to select the workflow
and only the specialist skills needed for the request. Paths in these
instructions are relative to the repository root.

This repository maintains the framework itself. Preserve established contracts,
license text, user changes, and history. Work on a feature branch and propose a
PR; merging, releasing, and deployment require the appropriate authorization.
Keep canonical rules in `core/` and skills in `skills/`. Adapter skill files are
generated routing wrappers; regenerate with `python scripts/sync_adapters.py`.

Run `python scripts/validate_framework.py`,
`python -m unittest discover -s tests -v`, and
`python scripts/sync_adapters.py --check` for framework changes. Update
`plans/enhancements/MASTER_TRACKER.md` with evidence and limitations.
Do not claim live Codex/Claude compatibility from static checks.
