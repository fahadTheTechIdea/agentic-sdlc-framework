# L08: Delivery and verification

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Turn L01-L07 selections into the user's requested deliverable using existing SDLC
artifacts and procedures. Applies to every project family. Inspect the active
project tracker, Git instructions, existing CI and authorization before actions.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L08.01 | Plan only, runnable starter, implement selected slice, or resume existing work | Respect current scope; outputs never grant their own authorization |
| L08.02 | Existing artifact locations and traceability | Extend specification/SDD/ADR/phase plan/RACI/verification/handoff rather than duplicate |
| L08.03 | Phases, feature slices, dependencies and minimum runnable outcome | Include operational foundations and relevant negative/failure checks early |
| L08.04 | Accountable owner and responsible roles | Real owner/role only; agent cannot supply human approval |
| L08.05 | Profile-specific build/test/security/acceptance commands | Verify against actual selected versions/tooling; preserve baseline failures |
| L08.06 | Git, review, delivery and external boundaries | Obey designated branch/workflow; no automatic branch, push, deployment or account action without scope |
| L08.07 | Completion/evidence and deferred gates | Distinguish implementation, local tests, CI, browser/provider/device, independent review and release |
| L08.08 | Save/resume and change review | Preserve answer provenance, unresolved questions, dependencies and next action |

Different stacks produce different verification trees: .NET build/test and UI
checks differ from Django framework checks/tests, TypeScript toolchains, Java build
tools, native packaging and device acceptance, or library consumer compatibility.
The tree records commands to verify; it does not execute arbitrary command strings
embedded in untrusted profile content. Tool permissions remain host-enforced.

## Dependencies and change effects

L08 consumes decisions and unknowns from all layers. Changing requested output
does not erase the design. A changed upstream profile reopens only affected tasks/
checks. Plan-only requests may document unknowns without pretending those gates passed.

## Outputs and completion checks

Produce a reviewable summary and selected project artifacts through existing
templates. Capture exact commands/results under the evidence policy. Before
claiming readiness, list unresolved decisions, missing tree branches, incompatible
choices and unrun gates. A completed questionnaire is not a delivered application.

For the current P8 phase, output is the layered/tree design only. No application
configuration file, wizard runtime, dependency installation or scaffold is created.

## Reference and standards needs

Record actual toolchain/CI/test/security guidance for the selected profile and
project governance obligations. Preserve test integrity, inspect dependency/test
changes and use the framework's existing assurance/evidence rules.
