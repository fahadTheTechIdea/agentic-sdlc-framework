# L02: Technology and architecture

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Select technology-specific trees and architectural boundaries from L01 outcomes,
approved stack constraints and inspected assets. Applies per deliverable; one
project may contain several ecosystems. Preserve explicit project pins.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L02.01 | Reuse existing stack, choose a stack, or compare alternatives | Reuse → inspect version/config/contracts; comparison → keep proposed candidates distinct |
| L02.02 | Ecosystem/language: .NET, Python, JavaScript/TypeScript, Java/Kotlin, Go, Rust, native platforms, other | Ecosystem opens its framework tree; it does not decide UI, data or hosting implicitly |
| L02.03 | Framework/product shape from the relevant family | Web/UI, API, desktop, mobile, worker, package and data trees expose different options |
| L02.04 | Framework variant and execution model | Resolve the matching variant branches in L03-L08 and their constraints |
| L02.05 | Module boundaries, dependency direction and distribution | Reuse active contracts; select modular separation or independent deployments only when justified |
| L02.06 | Toolchain/build/package/test conventions | Inspect existing tooling first; new choices need compatibility and provenance checks |
| L02.07 | Constraints/alternatives and material decisions | Record tradeoffs, unresolved incompatibilities and ADR-worthy changes |

Examples of distinct branches: a Blazor web profile distinguishes application and
rendering models; a Django profile asks about its project/apps and template/API
boundaries; a React web profile distinguishes the selected application framework
and client/server boundaries; a Spring API profile opens Java/JVM build and service
contract questions. These examples do not exhaust the catalog or prescribe versions.

## Technology-specific branch ownership

Use [the profile catalog](TREE_CATALOG.md). Each framework/variant has layer roots,
conditions and constraints. Do not alias all .NET projects to Blazor or all Python
projects to Django. Unresolved or unsupported profiles can support requirements
discovery, but cannot produce verified scaffold instructions by guessing.

## Dependencies and change effects

L02 reads L01 and consumes constraints from L03-L07. Changing a framework invalidates
only affected profile-specific answers and checks. If a hosting target cannot run
the chosen stack, present the conflict to the owner; do not auto-upgrade or swap it.

## Outputs and completion checks

Output selected/candidate stack profiles per deliverable, observed/pinned versions,
module map, shared contracts, tooling choices and ADR links in the existing SDD.
Check target fit, known constraints and branch coverage. A selected profile is
not proof that its version/provider combination works.

## Reference and standards needs

Reserve official lifecycle, release/support, framework, package and compatibility
references. Version-specific tree resolution and freshness policy remain a later
design slice; no option is labeled latest/supported/verified without evidence.
