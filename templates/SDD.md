# Software Design Description: <title>

Status: proposed | accepted | superseded
Specification: <path>; owner: <person/role>; version/date: <value>

## Context, scope and quality attributes
<System context, constraints, measurable availability/performance/accessibility needs.>

## Existing implementation and reuse
<Verified paths, active contracts and extension points; no invented components.>

## Architecture and boundaries
<Components, responsibilities, dependency direction, deployment and diagrams if useful.>

## Data and contracts
<API schemas, persistence, units, time zones, authorization, compatibility and ownership.>

## Behavior and failure modes
<Key sequences, validation, errors, cancellation, retries, idempotency, concurrency,
transaction boundaries and explicit empty/unauthorized behavior.>

## Security, privacy and dependencies
<Trust boundaries, threats, mitigations, secrets, retention, package provenance/licenses.>

## Migration, operation and recovery
<Rollout, observability, backups, rollback or compensation and recovery validation.>

## Log, audit, exception and notification services
<Complete or link OPERATIONAL_SERVICES.md: actual shared Log/Audit/Notification
contracts and implementations; UI Notification Service when a UI exists; event
coverage and trustworthy outcomes; exception ownership and preserved causes;
durable storage/transaction guarantees; channel routing, redaction, failure and
retry policy; UI user/tenant/session isolation. Reuse existing services and
document any legacy gaps or headless UI N/A reason.>

## Quality, security and reliability assurance
<Complete or link ASSURANCE.md for applicable boundaries: authorization and tenant
isolation, configuration validation/secrets, retry/idempotency/cancellation,
restoration/migration evidence, runtime health/objectives, verified dependencies,
test integrity and required CI/acceptance gates. For changed agent behavior include
selected evaluation scenarios and host-enforced tool scopes. Record N/A reasons.>

## Publishing and distribution constraints
<For selected stores, link PUBLISHING_READINESS.md or existing equivalent: actual
distribution scope, refreshed official policy/effective dates, SDK/native-library
compatibility, privacy/content obligations and external account/review gates.>

## Alternatives and decisions
<ADR links, SOLID tradeoffs, assumptions, costs and unresolved consequential choices.>

## Traceability and validation
| Requirement | Component/task | Check | Evidence/status |
| --- | --- | --- | --- |
| REQ-001 | <path/task> | <check> | <pending> |
