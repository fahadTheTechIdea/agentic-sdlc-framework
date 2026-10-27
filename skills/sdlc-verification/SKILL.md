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

For a significant or high-risk change that needs independent multi-lane review,
use `skills/sdlc-review-cycle/SKILL.md`. Its recorded verdicts are review evidence;
they do not replace the acceptance checks above or imply delivery approval.

Do not infer CI, browser, provider or production behavior from local tests.
An unavailable mandatory gate prevents a full completion claim. Report verified
scope, failures, skipped checks and the next action to close any remaining gate.
Framework structure can be checked with `scripts/validate_framework.py`; this
does not replace the target application's own checks.

Verify documentation maintenance under `core/ENGINEERING_STANDARDS.md`: inspect
the affected old/new document set, replace/remove obsolete guidance, check incoming
links and match current claims to implementation. Report changed/removed paths and
remaining conflicts in existing verification records. Structural link checks alone
do not prove that contradictory or stale Markdown has been eliminated.

For application changes, verify `core/LOGGING_AUDIT_NOTIFICATIONS.md` using
`templates/OPERATIONAL_SERVICES.md`: actual Log/Audit/Notification implementations,
UI Notification Service when applicable, covered boundaries, preserved exception
causes, no silent failure/success substitution, correct audit outcomes, redaction,
channel outage/retry behavior and UI user/tenant isolation. Review catch/except and
async paths; source scanning alone is not runtime evidence. Record wider legacy
gaps and untested provider/UI behavior explicitly.

Apply `core/QUALITY_SECURITY_RELIABILITY.md` using `templates/ASSURANCE.md` or
existing project verification. Check test integrity, real acceptance boundaries,
denied access/isolation, invalid config, duplicate/retried/cancelled operations,
restore/migration evidence, runtime signals and dependency findings as relevant.
Record N/A reasons and unavailable gates. For changed skills/prompts/tools/models,
use `evals/README.md`: inspect actual outcomes and transcripts, and keep grader
tooling tests separate from live agent results. Never weaken tests to claim success.

For store readiness, use `core/PUBLISHING_REQUIREMENTS.md` and
`templates/PUBLISHING_READINESS.md`: reopen current official sources/console scope,
capture effective/deadline dates, verify the actual artifact and preserve conflicting
source or exception evidence. Separate local/artifact checks, account/testing,
submitted, approved and released states. Missing external gates stay not_run;
structural checks and old policy snapshots cannot certify store eligibility.
