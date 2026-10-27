# Templates

Adapt these to the project's existing conventions; do not create duplicate
artifact systems. Text in angle brackets is a template prompt, not an observed
fact. Remove unresolved placeholders from completed project artifacts.

- [Specification](SPECIFICATION.md): outcomes and acceptance criteria.
- [SDD](SDD.md): Software Design Description for substantial design work.
- [RACI](RACI.md) and [machine-readable starter](RACI.json): ownership.
- [ADR](ADR.md): consequential decision with lifecycle and evidence.
- [Phase plan](PHASE_PLAN.md): scoped implementation tasks and gates.
- [Verification](VERIFICATION.md), [evidence record](EVIDENCE.json): claims and results.
- [Operational services](OPERATIONAL_SERVICES.md): logging, audit, exception handling,
  notification pipeline and conditional UI notification coverage and checks.
- [Review cycle records](review-cycle/cycle.json): cycle, lane report, approval and
  human decision contracts for the [review cycle](../core/REVIEW_CYCLE.md).
- [Handoff](HANDOFF.md): resume across sessions and tools.
- [Technology review](TECHNOLOGY_REVIEW.md): pins, source dates, support and
  compatibility evidence across affected layers without an automatic upgrade.
- [Publishing readiness](PUBLISHING_READINESS.md): current store policy, artifact,
  account/testing/review evidence and scoped release authorization.
- [Assurance](ASSURANCE.md): applicable quality/security/reliability controls,
  gate commands, agent evaluations and evidence without duplicating project records.

The JSON starters validate structurally but contain no real approvals or executed
checks. Assign real roles and capture actual evidence before using them to
support a completion claim.
