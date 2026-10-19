# Technology-specific decision tree model

Status: shared design, with an initial [terminal runtime/catalog](../../../docs/WIZARD.md)
implemented for 19 profiles. Version-range resolution and automatic migration
remain unimplemented.
Parent: [P8](../P8_LAYERED_WIZARD.md); shared rules: [layer contract](LAYER_CONTRACT.md).

## Structure: a layer selects a technology tree

The eight layers define decision ownership. Every selected framework profile
supplies a root for each layer, either a real subtree or an explicit N/A branch
with a reason. The common questions capture shared intent; technology-specific
trees decide which concrete questions and choices to expose.

For a project with multiple deliverables, resolve each deliverable separately:

```text
Project
  Deliverable: browser website
    Profile: selected ecosystem / framework / variant / version constraints
      L01 product tree
      L02 technology and architecture tree
      L03 interface tree
      L04 data tree
      L05 identity and security tree
      L06 integrations and shared-services tree
      L07 hosting and operations tree
      L08 delivery and verification tree
  Deliverable: separate API, worker, mobile app or package
    Profile: its own ecosystem / framework / variant / version constraints
      Its own L01-L08 roots, connected by explicit shared contracts
```

A .NET, Python or JavaScript label is not sufficiently specific to resolve a
framework tree. A single language can produce websites, native/desktop software,
APIs, workers, CLIs and libraries with different branches. A selected framework
may have execution variants that change several layers.

## Tree composition

1. Shared layer intent and mandatory framework rules remain canonical.
2. Product-family trees contribute domain questions, such as device targets or API callers.
3. Ecosystem/framework trees supply native choices and remove irrelevant questions.
4. Framework variant/version conditions refine applicable nodes and compatibility.
5. Existing-project constraints/pins and observed implementations constrain the choices.

This is compositional specialization, not copying all rules into each tree.
A profile declares which question slots it specializes and which shared controls
it inherits. A specialized tree cannot disable authorization, reporting, evidence,
test integrity or other governing requirements. Conflicting declarations must be
reported; selection order is not a license for the last profile to override policy.

## Proposed profile and node contracts

| Entity | Required design fields |
| --- | --- |
| Profile | Stable profile ID/revision; product families; ecosystem/framework; variant and version constraints; maintainers/source; inherited profile references |
| Layer root | Profile + layer ID; root node ID or explicit N/A reason; consumed/produced decisions; applicability conditions |
| Node | Stable ID; question/purpose; answer type; choices/free-text path; visibility prerequisites; allowed transitions; decision/output binding |
| Choice | Stable value; label; child branch; constraints/conflicts; affected decisions; reference needs |
| Constraint | Referenced decision IDs; compatibility condition; reason; owning layer; blocked/review behavior |
| Check | Expected outcome, owning layer, verification kind and evidence requirement; trusted procedure reference rather than executable remote text |
| Evidence reference | Official source, subject/version/context, checked date, support/compatibility result and known gaps |

The initial runtime publishes [catalog](../../../wizard/catalog.schema.json) and
[session](../../../wizard/session.schema.json) JSON shapes with semantic validation.
The wider tree design remains extensible. Use namespaced
question IDs such as `L03.dotnet.blazor.web.rendering` and
`L03.python.django.web.presentation`. Both may map to the shared semantic output
`interface.presentation`, but preserve their profile-specific answer/history.

## Resolution, version and coverage rules

- Honor applicable project instructions and explicit project-local pins. Detected
  versions are observations, not consent to upgrade.
- Choose the family and framework from actual user/project evidence; if ambiguous,
  ask the missing decision or retain candidates. Do not infer a framework from
  language alone or from a familiar example.
- Select only matching variants/version ranges. Unsupported/unknown combinations
  remain unverified; do not silently choose a nearby tree or hide a missing branch.
- Require L01-L08 root coverage. Headless UI and absent owned storage use reasoned
  N/A roots; shared operational/security obligations remain applicable.
- Inheritance cycles, missing targets, duplicate IDs, invalid transition targets
  and conflicting output bindings must fail profile validation.
- Changes to a profile/variant/version keep answer history, invalidate dependent
  nodes and show the proposed migration. Never silently drop old selections.

## Examples of genuinely different subtrees

| Layer | Blazor website example | Django website example | Other independent branches |
| --- | --- | --- | --- |
| L01 | Website workflows and browser audience | Website workflows and browser/admin audience | Package consumers, API callers, native devices, worker schedules |
| L02 | Web App versus standalone WebAssembly and selected execution variant | Python/Django project and apps; template/API boundaries | React application framework, Spring service, Go service, Flutter app |
| L03 | Web App rendering/interactivity branch versus standalone browser model | URL/view/template/form branch; optional client enhancement | Native view/navigation, desktop windows, CLI commands, no visual UI |
| L04 | Server data access versus authorized client API; selected provider | Model/query/migration decisions and provider | Other ORM/driver, caller-owned data, local offline store |
| L05 | Server policy/identity and browser trust boundaries | Django account/session/permission decisions | Service identity, OS/device identity, package input trust |
| L06 | Native reporting/hosting adapters and UI component lifetime | Logging/request/task/reporting adapters and delivery | Queue consumers, device dispatch, offline channels, event providers |
| L07 | Hosting that matches server/browser execution needs | WSGI/ASGI, static/media and environment settings | Framework server/static output, device packaging, package registry |
| L08 | Selected .NET build/test and browser/provider checks | Django checks/tests and browser/provider checks | JVM/Go/JS tools, device/store acceptance, consumer compatibility |

These are examples, not an exhaustive list or a fixed two-framework scope.
[The catalog](TREE_CATALOG.md) separates broad profile inventory from concrete
tree blueprints and implementation/verification status.

## Cross-stack composition

A browser frontend plus Python API is two profiles connected by a versioned API
contract, not a merged framework with every question from both. Share only actual
decisions: contract/auth flow, environment URLs, error semantics, correlation,
units/time, ownership and compatibility tests. Backend storage credentials are
never browser configuration. Multiple clients may reuse the same API contract.

A monolithic deployment can still contain clear module contracts. Profile count
does not dictate process count, microservices or independent Git repositories.

## Domain-specific layer extensions

Profiles may compose a domain extension such as [games](GAMES.md). The existing
L01-L08 roots remain required; a game profile also declares G01-G09 roots or reasoned
N/A branches. Each domain node binds to the owning L-layer semantic decision and
adds its own engine-specific conditions, outputs, dependency edges and checks.
Do not collect or maintain another copy of a decision already owned by a layer.

P12 validates domain root sets, stable namespaced IDs, condition/dependency
references, cycles and conflicting bindings for its initial catalog. Generalized
inheritance/transition graphs and automatic migration remain future extensions.
A domain group does not automatically authorize a new skill, agent, service or
package. The shared framework rules remain canonical; the executable implementation
is separate from these design documents and described in the runtime guide.

## Technology and standards freshness boundary

The tree design reserves versioned references and applicability conditions now.
Use the on-demand [technology verification policy](../../../core/TECHNOLOGY_FRESHNESS.md)
to check actual supported versions and relevant standards before making current
claims. An automated version/compatibility resolver remains unimplemented.
Official documentation inspected
for examples is listed in [the source register](../../../docs/RESEARCH_SOURCES.md).
It does not establish that every catalog entry is current, supported or tested.

## Future acceptance cases

Before delivering a runtime, test at least: selecting different frameworks changes
the real questions; no Blazor render modes appear in a Django tree; native mobile
does not receive web-only hosting questions; a mixed project preserves separate
profiles; unknown profiles stay explicit; version conflicts are reported; changing
framework invalidates dependent answers; N/A has reasons; plan-only writes no
application files; resumed answers retain profile/node identity and provenance.

P12 tests exercise the implemented subset: profile-specific/conditional questions,
mixed deliverables, unknown profiles, dependency review, N/A, preview, provenance
and resume. Automatic version-range resolution and real host model tasks remain
unrun/unimplemented as recorded in the runtime plan.
