# L01: Project definition and type

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Identify the intended product before choosing implementation details. Always enter
this layer, including existing-project mode. Inputs are the user's description,
authorized scope, existing repository facts and constraints; none implies permission
to initialize, rewrite or deploy a project.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L01.01 | New project, existing project, add a component, or explore only | Existing/add-component → inventory current deliverables and contracts first |
| L01.02 | Who uses it, what problem it solves, and measurable outcomes | Separate business users, operators, consumers and external systems |
| L01.03 | Product family: web, API, desktop, mobile, worker, CLI, library, data/AI, game/simulation, mixed or custom | Mixed → create linked deliverables; custom → capture needs without claiming a supported profile |
| L01.04 | Target users/platforms: browsers, OS/device families, headless execution, package consumers | Each independently delivered target keeps its own constraints and checks |
| L01.05 | Scope: initial workflows, MVP boundary, exclusions and existing work to preserve | Distinguish required capability from possible later expansion |
| L01.06 | Constraints: team skills, approved technologies, cost, connectivity, data sensitivity, geography, deadlines | Unknown values stay unknown; they influence stack and hosting suggestions |
| L01.07 | Choose a technology now, reuse detected choices, or compare candidates | Resolve a profile through L02; revisit only technology-specific L01 questions |

A family choice activates different product trees: mobile asks about supported
device/OS targets and disconnected use; a library asks about package consumers
and compatibility; an API asks about callers and public/private exposure; a game
asks about execution target, interaction and determinism requirements. These are
independent branches, not a single website questionnaire with hidden fields.

## Technology-specific branch ownership

The selected framework profile contributes L01 questions relevant to its product
shape; examples appear in [the catalog](TREE_CATALOG.md). A backend and separate
frontend have separate profile instances connected by a contract. Selecting a
language alone does not select every framework built on that language.

## Dependencies and change effects

L01 owns deliverable IDs, target platforms and scope. Changes re-evaluate the
applicability of L02-L08; preserve unaffected answers. A later technology preference
cannot silently change the required targets or user outcomes.

## Outputs and completion checks

Output a project brief, named deliverables, requirements, constraints, non-goals
and initial applicability map into the existing specification location. Check that
every deliverable has a purpose/target, explicit unknowns and an action scope.
Do not mark product feasibility or cross-platform compatibility verified yet.

## Reference and standards needs

Record relevant platform/distribution restrictions and domain obligations as facts
to verify, with an owner and source if known. This layer does not choose a current
framework version or claim legal/regulatory conformance.
