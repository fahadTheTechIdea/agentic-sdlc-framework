# Engineering standards

For stack selection, version-sensitive changes and standards research, use
[technology verification](TECHNOLOGY_FRESHNESS.md). Preserve approved pins;
documented support and actual runtime compatibility require separate evidence.

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

## Publishing and distribution

For store-bound design, packaging, release-readiness or published-app updates,
apply [publishing requirements](PUBLISHING_REQUIREMENTS.md). Select actual store,
platform/form factor, account/product scope and release date; recheck primary
policy and console requirements. Use [publishing readiness](../templates/PUBLISHING_READINESS.md)
or existing project records for artifact, privacy/content, account/testing/review,
timing and authorization evidence. A dated framework snapshot is not proof of
current policy, accepted SDKs or store eligibility.

## Documentation maintenance: replace or remove

Planning, feature changes, replacements and debugging include maintaining the
affected documentation. Prefer updating the existing authoritative document in
place. Do not create a new fix/update/feature Markdown file merely to repeat or
contradict an existing specification, design, plan or usage guide.

1. Before writing, search for the affected feature, old/new names and relevant
   paths across specifications, plans, README files, usage guides, decisions,
   indexes and handoffs. Identify which document owns the current concern.
2. Update that document in place when the concern is unchanged. Create a separate
   document only for a distinct scope or required record, and explain its purpose
   in the existing tracker rather than creating another tracking system.
3. When documentation is obsolete, **replace or remove it**. Merge still-valid
   unique requirements, decisions and unresolved tasks into the current owner
   before removing a redundant file. For partial feature replacements, update
   only affected sections and preserve still-supported behavior.
4. Do not keep an obsolete active guide by adding an archive copy, a dated
   duplicate, a superseded banner or a redirect stub as the default solution.
   Update incoming links, indexes, tracker references, examples and handoffs to
   the replacement, and remove obsolete instructions in the same scoped change.
   Normal Git history preserves earlier content; never rewrite that history.
5. Preserve records with a real retention purpose: accepted ADRs, immutable test/
   release evidence, required incident/compliance history and explicitly retained
   project records. These document past decisions/results, not current usage.
   Keep their historical scope clear and point current navigation to the active
   design. This exception is not a reason to retain ordinary stale fix/plan files.
6. Keep planned and implemented behavior distinct. A new proposal can replace an
   old proposal; it must not overwrite operational instructions for functionality
   that remains live until the authorized replacement actually ships. Intentionally
   supported versions may have distinct, clearly scoped current documentation.
7. Verify the affected document set before reporting completion: search again for
   obsolete feature names/paths/instructions, check incoming links after removals,
   reconcile statuses with actual code/evidence, and confirm no competing document
   is presented as the current authority. Text matches may be valid history; inspect
   their context rather than claiming a search proves semantic consistency.

Record updated/replaced/removed paths and any unresolved conflict in the existing
tracker or verification report. Scope cleanup to the task, preserve unrelated user
work, and do not delete unique or required records based only on filename or age.
If a retention/ownership conflict cannot be resolved from project instructions,
record the specific gap without inventing a cleanup approval. This procedure
requires review; the structural validator cannot detect contradictory prose.

## SDD terminology

This framework uses **SDD** for *Software Design Description*, the durable design
artifact in `templates/SDD.md`. **Specification-driven development** is the
workflow: accepted intent and criteria guide plans, implementation and checks.
Neither term implies that a generated specification is automatically approved.
