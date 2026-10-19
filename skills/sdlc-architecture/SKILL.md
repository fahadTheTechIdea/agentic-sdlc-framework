---
name: sdlc-architecture
description: Assess software boundaries and SOLID tradeoffs, and record consequential architecture choices in ADRs.
---

# Architecture and SOLID

Read `core/ENGINEERING_STANDARDS.md`; inspect existing shared abstractions and
callers. Prefer reuse over parallel models. Identify the reason each boundary
exists and how failures, concurrency, authorization and transactions cross it.

Compare realistic alternatives and their consequences. Use `templates/ADR.md`
for costly, hard-to-reverse or cross-module decisions; include status, owner,
evidence, supersession and verification. An agent recommendation is proposed
until an authorized decision-maker accepts it. Check substitutability with
behavioral contracts where implementations are interchangeable. Do not add
interfaces, services or patterns solely to tick a SOLID checkbox.

For technology choices apply `core/TECHNOLOGY_FRESHNESS.md`. Verify the selected
runtime/framework/provider/target combination, preserve project pins and record
documented support separately from executed compatibility checks. Reuse the SDD/ADR
or `templates/TECHNOLOGY_REVIEW.md`; do not create a competing version inventory.

Apply `core/LOGGING_AUDIT_NOTIFICATIONS.md` and identify the existing shared Log,
Audit and Notification Service contracts. Include UI Notification Service design
when a UI exists. Separate durable records from notification channel delivery;
define exception ownership, audit consistency, channel outage behavior, emergency
diagnostics and user/tenant isolation. Use `templates/OPERATIONAL_SERVICES.md`
within the current SDD. Do not create parallel services or bind domain policy
directly to email, file or UI providers.

Use relevant sections of `core/QUALITY_SECURITY_RELIABILITY.md` for authorization
and trust boundaries, config validation, retry/idempotency/concurrency contracts,
recovery objectives, runtime signals and dependency provenance. Reuse existing
native controls; record measurable checks in `templates/ASSURANCE.md` or the SDD.

If distribution includes a store, use `core/PUBLISHING_REQUIREMENTS.md` to check
engine/runtime/export/native dependencies against current submission constraints.
Keep SDK, deployment target and store eligibility separate; privacy/deletion,
content/payment and signing requirements can affect the design. Preserve source
conflicts and actual account exceptions instead of inventing compatible defaults.
