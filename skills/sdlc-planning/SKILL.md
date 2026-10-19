---
name: sdlc-planning
description: Build phased software delivery plans, RACI ownership and traceability for multi-step implementation work.
---

# Plan delivery and ownership

Extend the active project tracker. For new substantial work use
`templates/PHASE_PLAN.md` and `templates/RACI.md`. Sequence small reversible
tasks with explicit dependencies, acceptance criteria, checks and recovery.
Each RACI decision/deliverable has exactly one accountable named human/role
and at least one responsible executor. Identify which approvals are actually
required and which authorization already exists.

Record risk and open decisions. Keep implementation, local validation,
independent review, CI and release status separate. Do not mark documentation
as implementation progress. Use `templates/RACI.json` if machine validation
is useful; explain any roles combined by one person and any self-review.

For application work, include the service coverage matrix and failure-path checks
from `core/LOGGING_AUDIT_NOTIFICATIONS.md`. Put missing Log, Audit and Notification
foundations, plus UI Notification Service for UI applications, in the first
appropriate runnable slice. Existing-project tasks extend the active services
within authorized scope and track wider gaps explicitly.
