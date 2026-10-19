---
name: sdlc-verification
description: Verify software acceptance criteria and evidence, review changes, and report scoped completion with remaining gates.
---

# Verify and review

Read `core/EVIDENCE_POLICY.md`. Map each criterion to source changes and checks
using `templates/VERIFICATION.md`. Run checks on the actual changed revision;
record exact commands, environment, exit codes and sanitized output locators.
Use `templates/EVIDENCE.json` for machine-checkable records when appropriate.

Review failure paths, existing contract reuse, SOLID tradeoffs and risks relevant
to the change. Label self-review. Run independent review when project governance
requires it and the environment supports it; never imply another reviewer ran.

Do not infer CI, browser, provider or production behavior from local tests.
An unavailable mandatory gate prevents a full completion claim. Report verified
scope, failures, skipped checks and the next action to close any remaining gate.
Framework structure can be checked with `scripts/validate_framework.py`; this
does not replace the target application's own checks.
