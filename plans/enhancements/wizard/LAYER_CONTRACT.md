# Shared contract for wizard layers

Status: proposed design, not an implemented schema or engine.
Parent: [P8 layer development](../P8_LAYERED_WIZARD.md).
Technology specialization: [tree model](TREE_MODEL.md) and
[multi-technology catalog](TREE_CATALOG.md).

## A layer contains

1. Purpose and applicability: the decision area and when a branch is relevant.
2. Inputs: upstream selections, inspected project facts and explicit constraints.
3. Substeps: stable question IDs, choices, conditional follow-ups and decision rules.
4. Dependencies: fields read, downstream fields affected and conflicts to surface.
5. Outputs: named decisions and mapping to existing specification/SDD/plan artifacts.
6. Completion checks: what is resolved, unknown, not applicable or still needs evidence.
7. Reference needs: technology/standard facts to verify later, without invented versions.

Top-level layer IDs L01-L08 remain stable. Each substep may contain several
questions, such as L04.03.storage-location. Menu wording may evolve without
changing persisted decision identity. These identifiers are a design convention;
a machine-readable catalog and migrations remain to be implemented.

Each selected technology profile supplies layer-specific tree roots and nested
questions. Include profile ID/revision, variant and node ID in answer identity;
common semantic outputs do not erase framework-specific decisions. Every layer
has its own technology branch or an explicit N/A root. The catalog is extensible;
example profiles do not limit the supported design to those frameworks.

## Proposed answer envelope

For each decision, preserve: decision ID; project/deliverable scope; value or explicit
unknown; applicability and reason; origin; source locator when observed; confidence
or uncertainty; user constraint; owning layer; dependencies; last edit; history;
and the effect on pending checks. Never store passwords/tokens in wizard state.

Origin distinguishes a direct user answer, inspected repository evidence, an
assistant recommendation and an inferred assumption. Recommendations/assumptions
remain labeled and can be revised; prefilled answers cannot masquerade as user
choices. An explicitly pinned project stack is a constraint, not an upgrade request.

An applicable technology/standard reference reserves: subject, selected or observed
version, official source URL/locator, verified-at timestamp, support status,
compatibility result, evidence locator and remaining unknowns. Unknown references
stay unverified. The later freshness design owns how these are researched/refreshed.

## Layer state and completion

| State | Meaning |
| --- | --- |
| not_started | Applicability and questions have not been evaluated |
| in_progress | Relevant decisions are being collected |
| resolved | Decisions needed for the requested output are captured; this does not mean runtime checks passed |
| needs_review | A dependency changed or a contradiction invalidated a decision |
| blocked | A required user decision or external fact prevents the next dependent action |
| not_applicable | Branch excluded with a recorded reason; parent context is preserved |

Evidence status is separate: verified, failed or not_run under the existing
[evidence policy](../../../core/EVIDENCE_POLICY.md). A resolved decision can still
have an unrun compatibility/acceptance check. Planning may proceed with explicit
unknowns; implementation cannot claim a required unverified gate as satisfied.

## Interaction and navigation

Begin with the user's existing description and project evidence. Ask a small batch
of related questions at a time; expose deeper questions only when their parent
choice requires them. Choices support free text, multiple targets and an explicit
unsure/recommend option. Explain recommendations through relevant constraints.

Support back/edit, defer, review summary and resume. A changed decision marks
dependent answers needs_review, retains history and preserves unrelated answers.
Do not require a confirmation click after every question/layer. Ask only for
missing consequential decisions; preserve authorization already present.

Existing-project mode performs read-only inventory first. Suggested prefills link
to real files/configuration and distinguish observation from interpretation.
Do not overwrite existing instructions/plans or automatically run migrations,
scaffolding, account creation, provisioning, external messages or package installs.

## Proposed ownership and artifact mapping

Each decision has one owning layer even when several layers consume it. Other
layers add requirements or raise conflicts; they do not maintain independent copies.
L08 assembles links/outputs into the project's existing artifact locations.

| Shared concern | Decision owner | Consumers |
| --- | --- | --- |
| Project targets and scope | L01 | All layers |
| Stack and module boundaries | L02 | L03-L08 |
| UI behavior and UI notifications | L03 | L05-L08 |
| Data model, consistency and restore contract | L04 | L05-L08 |
| Identity, access and tenant boundaries | L05 | L03/L04/L06/L07/L08 |
| Log/Audit/Notification and external delivery contracts | L06 | L03/L04/L05/L07/L08 |
| Environments, runtime health and operational ownership | L07 | L02/L04/L05/L06/L08 |
| Requested actions, plan, verification and handoff | L08 | All layers |

The framework's [constitution](../../../core/ENGINEERING_CONSTITUTION.md),
[engineering standards](../../../core/ENGINEERING_STANDARDS.md),
[operational standard](../../../core/LOGGING_AUDIT_NOTIFICATIONS.md) and
[assurance standard](../../../core/QUALITY_SECURITY_RELIABILITY.md) remain canonical.
A menu can select an implementation/provider or record an existing gap; it cannot
disable mandatory reporting, swallow exceptions or weaken security/test gates.

## Conflict examples and recovery

- UI choice conflicts with target devices: L03 raises a target issue to L01 and a
  framework compatibility issue to L02; keep both proposed choices visible.
- Database not available in selected hosting: L07 flags L04/L02 needs_review;
  present alternatives without silently changing providers.
- Tenant model changes: revisit authorization, data ownership, notification
  recipient scope and isolation tests, not unrelated typography choices.
- User stops or host closes: preserve the last valid saved answers and unresolved
  questions; never claim a partially written state was safely persisted.
  Atomic saves, schema validation, file collision handling and schema migration
  must be designed/tested in P8.1 before state-writing behavior is delivered.
