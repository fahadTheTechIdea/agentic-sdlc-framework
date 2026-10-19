# P8: Develop the project wizard as eight layers

Date: 2026-10-19. Owner: repository owner; author/reviewer: assistant, self-review.
Status: layer design prepared; wizard runtime and host behavior not implemented.
Authorization: develop the previously proposed steps as layers first. Preserve the
eight top-level steps; do not build a UI, new runtime, profile updater or scaffolder
in this phase. Framework maintenance continues directly on master.
The owner clarified that Blazor and Django are examples only. Technology-specific
trees must support an extensible range of project types and frameworks.

## Problem and intended outcome

A flat project questionnaire leaves consequential decisions unspecified. Develop
each original step into a decision layer with nested questions, explicit inputs,
conditional branches, dependencies, outputs and checks. The same layer contracts
will support conversational, terminal or graphical presentation later.

A wizard layer is a configuration/decision area. It is not automatically an
application tier, a separate service, an agent or a new skill. A selected project
can still be a simple single deployment. Integration reuses the existing SDLC
orchestrator, constitution, specialist procedures and artifact templates.

## The eight layers

| Order | Layer and detailed design | Nested decision areas | Main output |
| --- | --- | --- | --- |
| L01 | [Project definition and type](wizard/L01_PROJECT.md) | Purpose, users, outcomes, project family, targets, scope, constraints | Project brief and applicability map |
| L02 | [Technology and architecture](wizard/L02_TECHNOLOGY.md) | Existing assets, language/runtime, application frameworks, boundaries, conventions, quality constraints | Stack and architecture decision profile |
| L03 | [Interface and experience](wizard/L03_INTERFACE.md) | Channels, navigation, workflows, components, accessibility, localization, UI feedback | Interface and interaction profile |
| L04 | [Data and persistence](wizard/L04_DATA.md) | Domain model, storage, access, consistency, synchronization, migration, recovery | Data and lifecycle profile |
| L05 | [Users, identity and security](wizard/L05_SECURITY.md) | Identity, accounts, authorization, tenancy, secrets, privacy, threat boundaries | Access and security profile |
| L06 | [Integrations and shared services](wizard/L06_INTEGRATIONS.md) | External contracts, shared Log/Audit/Notification capabilities, UI notification adapter, jobs, delivery reliability | Capability and integration map |
| L07 | [Hosting and operations](wizard/L07_HOSTING.md) | Environments, topology, deployment, infrastructure, telemetry, continuity, cost | Deployment and operations profile |
| L08 | [Delivery and verification](wizard/L08_DELIVERY.md) | Requested deliverable, artifacts, ownership, slices, checks, Git workflow, handoff | Specification/design/plan and verification mapping |

Every layer follows [the shared layer contract](wizard/LAYER_CONTRACT.md). Read the
contract first, then the relevant detailed layer; do not repeat every question
for every project. Layer files define questions and decisions, not preset answers.

## A separate technology tree inside each layer

The [tree model](wizard/TREE_MODEL.md) defines framework/variant-specific roots for
each L01-L08 layer. The [catalog and eight starter blueprints](wizard/TREE_CATALOG.md)
cover multiple website stacks, an API, mobile, worker, CLI and library examples,
with a broader extensible inventory for additional technologies. These are design
blueprints, not implemented or version-verified runtime support.

Each deliverable selects its own profile. For example, a browser UI with a separate
API has two technology trees connected by explicit contracts. A generic language
choice cannot substitute for the selected framework's interface, data, security,
integration, deployment and testing trees. Common framework policies are inherited;
profile-specific choices, conditional questions and outputs remain distinct.

## Dependency and navigation model

The initial walkthrough is L01 → L02 → L03 → L04 → L05 → L06 → L07 → L08.
This is a navigation order, not a claim that all choices are independent or final.
L01 determines applicability; L02 proposes a stack subject to later data, security,
integration and hosting constraints. A later answer may invalidate earlier decisions.

Use field-level dependencies: mark only affected answers `needs_review`, explain
why, and preserve the original answers and unrelated progress. A conflict is shown
at the decision that owns it, with affected layers linked. Never silently replace
a user's selection or let the last-written answer win.

Examples: choosing offline mobile operation revisits L03/L04/L05/L06; changing from
one tenant to multiple tenants revisits L04/L05/L06/L07/L08; selecting a headless
worker makes visual interface questions N/A but retains operational notifications.
A hosting runtime incompatibility returns to L02 rather than guessing a version.

## Framework integration boundaries

| Existing area | How the proposed wizard uses it |
| --- | --- |
| sdlc-orch / canonical orchestrator | One entry; classify new versus existing project, load relevant layer questions, route procedures |
| Specification and architecture skills | Convert selected outcomes and decisions into existing specification/SDD and ADRs |
| Planning skill and master tracker | Sequence the selected capabilities and record ownership/risks |
| Implementation skill | Run only when the current user scope authorizes implementation |
| Verification and handoff skills | Check selected criteria, preserve evidence and resumable state |
| Constitution and engineering standards | Remain canonical; layer menus cannot disable governing rules |
| Operational service standard | L06 owns service mapping; L03/L05/L07 constrain presentation, isolation and operations |
| Quality/security/reliability standard | Each applicable layer names its assurance checks |
| Host adapters | Present the same decisions in Codex and Claude; no copied host-specific policy |

The future invocation `sdlc-orch new project wizard` remains a proposal.
This documentation does not add a registered command or make the wizard runnable.
Existing-project entry must inventory and prefill verified observations while
preserving active contracts, plans and project pins. It cannot authorize migration.

## Common technology/standards field

Each detailed layer identifies where a technology or standard affects its choices.
The shared contract reserves reference/version, official source, verification date,
support/compatibility result and unknown status. No current version, compliance or
freshness claim is supplied in this phase. A later technology/standards verification
design must populate those fields before presenting an option as verified-current.
A user may express a preference before verification; preferences are not evidence.

## Requirements and acceptance criteria

| ID | Design criterion | Design verification | Runtime acceptance |
| --- | --- | --- | --- |
| WIZ-001 | Preserve eight original steps as named layers | Eight linked layer documents and this index | Not run |
| WIZ-002 | Each layer has nested questions, branches, dependencies, outputs and checks | Layer-by-layer self-review | Not run |
| WIZ-003 | Shared answer state records origin, applicability, uncertainty and invalidation | Shared contract review | Not run |
| WIZ-004 | New/existing projects, mixed targets and N/A paths are defined | Walkthroughs below | Not run |
| WIZ-005 | Reuse existing skills, rules, services, plans and templates | Integration mapping and local links | Not run |
| WIZ-006 | User scope and authorized Git workflow control actions | L08 and shared contract | Not run |
| WIZ-007 | Technology/standard evidence has a home in every applicable layer | Layer reference sections; no hard-coded latest claims | Verification mechanism deferred |
| WIZ-008 | Design status cannot imply runnable wizard/model behavior | Explicit status and README wording | Not run |
| WIZ-009 | Each selected framework/variant supplies distinct roots for every applicable layer | Tree model and eight multi-family blueprints | Resolver/coverage validation not implemented |
| WIZ-010 | Many technologies and mixed deliverables are supported by the design contract | Extensible catalog, unknown-profile behavior and composition rules | Runtime support not implemented |

## Design walkthroughs (not executed wizard tests)

| Scenario | Expected layer path and review points |
| --- | --- |
| Local command-line utility | L01 CLI; L03 visual UI N/A; L04 persistence may be N/A with reason; L05 OS/user boundaries; L06 shared reporting appropriate to size; L07 local distribution; L08 focused checks |
| Web application with multiple tenants | L03 browser flows; L04 ownership/consistency; L05 resource/tenant policies; L06 recipient isolation; L07 hosted runtime; L08 negative isolation and browser checks |
| Offline mobile application | L01 platform/device scope; L03 disconnected interaction; L04 local store/conflicts; L05 local identity/secret handling; L06 deferred delivery; L07 package/distribution; L08 device/network checks |
| Existing service with approved stack | Prefill L01/L02 from inspected evidence, preserve user edits; L03 N/A if headless; inspect active L04-L07 capabilities; L08 plan permitted changes and gaps |
| Library plus sample UI | L01 separate deliverables; core library L03 N/A, sample UI L03 applicable; package compatibility and sample deployment tracked separately |
| User changes delivery to plan only | Preserve choices; L08 outputs documents and unresolved checks; no scaffold, dependency installation, Git initialization or deployment |
| User changes a website framework | Replace only affected technology-specific subtrees, preserve history and common intent; no previous framework's rendering/auth/ORM/deployment choices leak into the new tree |
| User selects an uncataloged framework | Capture intent and explicit profile gaps; do not claim support or silently use a familiar website profile |

## Development sequence

These are future implementation slices, not authority to implement during this
design-only phase. Each slice needs its own runnable acceptance evidence.

| Slice | Scope | Status |
| --- | --- | --- |
| P8.D | Develop eight layers, technology-specific tree contracts/catalog, dependencies and framework mapping | Documentation prepared |
| P8.1 | Define machine-readable answer/profile/node schemas, registry and tree coverage checks | Not implemented |
| P8.2 | Add L01/L02 tree selection, conversational flow, provenance, save/resume and no-write preview | Not implemented |
| P8.3 | Add technology-specific L03-L07 branches and invalidation/conflict handling | Not implemented |
| P8.4 | Map L08 decisions to existing artifacts and authorized delivery actions | Not implemented |
| P8.5 | Design verified technology/standards profiles and refresh rules | Deferred until layer design is settled |
| P8.6 | Add behavioral cases, independent outcome checks and actual Codex/Claude runs | Not run |
| P8.7 | Consider terminal/browser presentation over the same contracts | Deferred; no UI technology selected |

RACI for this design: repository owner is accountable for consequential product
choices; the assistant is responsible for drafting and self-review. Additional
reviewers, technology owners and operational owners must be assigned by the real
project, not invented by the wizard.

## Local verification

The existing structure/link, adapter parity and regression commands must run for
this repository change. They verify documentation integration and existing tooling,
not conversational behavior. Actual command outcomes are recorded in the delivery
report; hosted CI is checked on the published revision. Official documentation
was checked for the named Blazor/Django example branch concepts. No supported-stack
recommendation, release/version qualification, application scaffolding, model
evaluation or personal installation change is part of this layer-definition phase.

Local results on 2026-10-19: structure/link validation, generated-adapter parity,
all 47 existing regression tests and diff whitespace checks passed. This was a
documentation/manifest change; no new behavioral tests were invented to validate
prose. Review was self-review. The selected wizard scenarios and profile trees
remain unexecuted designs, regardless of the existing regression result.
