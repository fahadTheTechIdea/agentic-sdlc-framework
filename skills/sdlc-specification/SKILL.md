---
name: sdlc-specification
description: Create measurable software specifications and Software Design Descriptions for features or new projects with material design scope.
---

# Specify outcomes and design

Inspect the existing product, contracts and plans before proposing requirements.
Use `templates/SPECIFICATION.md` for intent and acceptance criteria, with stable
requirement IDs. Separate observed requirements, assumptions and recommendations.
Ask for unresolved consequential product choices; infer reversible details within
the authorized scope. Do not claim that a proposed requirement was approved.

For material design scope, fill `templates/SDD.md` with actual boundaries, data,
contracts, failure modes, security, migration, operations and verification links.
Use `core/ENGINEERING_STANDARDS.md` for SDD terminology. Reuse an equivalent
existing document instead of creating a parallel specification system.

Include the mandatory application foundations in
`core/LOGGING_AUDIT_NOTIFICATIONS.md`: shared Log, Audit and Notification Services,
and a UI Notification Service if a UI exists. Capture measurable event coverage,
exception/failure behavior and notification delivery outcomes. Reuse existing
contracts and `templates/OPERATIONAL_SERVICES.md`; distinguish implemented scope
from broader legacy gaps and headless UI non-applicability.
