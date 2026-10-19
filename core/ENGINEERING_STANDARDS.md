# Engineering standards

## SOLID in review

| Principle | Apply it by | Evidence to look for | Avoid |
| --- | --- | --- | --- |
| Single responsibility | Give modules cohesive reasons to change; separate domain rules from transport and storage | A change stays within its intended boundary | Splitting every function into a class |
| Open/closed | Extend stable variation points when variation is demonstrated | A new provider reuses the existing contract | Treating all edits to existing code as violations |
| Liskov substitution | Preserve preconditions, postconditions, errors, ordering and side effects of a contract | Run the same behavioral contract checks against interchangeable implementations | Assuming matching signatures prove substitutability |
| Interface segregation | Expose the capabilities a consumer needs | Consumers do not need unrelated operations or fake implementations | Many one-method interfaces without a need |
| Dependency inversion | Keep domain policy independent of replaceable infrastructure | Storage or transport can change without rewriting domain rules | Adding a parallel abstraction beside an active shared contract |

Document material tradeoffs in an ADR. Simple procedural code can satisfy the
same goals. Do not prescribe a language, framework, microservice topology, DI
container, test count or coverage target without project evidence.

## Design and implementation

Applications must follow [the logging, audit, exception and notification standard](LOGGING_AUDIT_NOTIFICATIONS.md).
Create or reuse shared Log, Audit and Notification Services; add a UI Notification
Service for applications with a UI. Document their contracts and event coverage
using [the operational service matrix](../templates/OPERATIONAL_SERVICES.md).
Never swallow exceptions; use explicit outcomes and the shared reporting pipeline.

Use explicit input validation, error/empty/unauthorized states and cancellation
where relevant. Make units, time zones, concurrency assumptions and transaction
boundaries visible. Design migrations with backups, dry runs and recovery
appropriate to impact. Keep API compatibility intentional and version breaking
changes. Avoid silent fallback data and success-shaped failure responses.

Read dependency APIs from the installed version or authoritative documentation
before use. Pin or lock dependencies as the project requires. Record new
packages, provenance, licenses and operational costs. Do not create new shared
frameworks when existing components can own the behavior.

Test observable behavior at the appropriate boundary: unit tests for rules,
contract tests for interchangeable adapters, integration tests for persistence
and authorization, and browser/device checks for user interactions. Include
failure paths and regression cases for substantive fixes. Select accessibility,
security, performance, recovery and observability checks based on actual risk.
Use project-specific quality gates and disclose any gate that was unavailable.

Apply [quality, security and reliability](QUALITY_SECURITY_RELIABILITY.md) to the
affected boundary: test integrity and executable gates, agent evaluations when
changing agent behavior, authorization/isolation, validated configuration, bounded
retries and cancellation, proven recovery, runtime health, dependency checks and
host-enforced tool permissions. Reuse [the assurance matrix](../templates/ASSURANCE.md)
or existing project verification to record applicability and actual evidence.

## SDD terminology

This framework uses **SDD** for *Software Design Description*, the durable design
artifact in `templates/SDD.md`. **Specification-driven development** is the
workflow: accepted intent and criteria guide plans, implementation and checks.
Neither term implies that a generated specification is automatically approved.
