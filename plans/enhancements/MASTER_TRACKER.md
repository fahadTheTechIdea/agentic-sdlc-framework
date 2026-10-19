# Framework v1.2 — master tracker

Specification: [v1.2 scope](specs/V1_2.md).
Authorization: the baseline PR is merged. The owner explicitly requires master-only
maintenance and authorized updating the README and related documents directly on master.
Policy acceptance and release remain repository-owner decisions.

| Phase | Task | Status | Design/evidence |
| --- | --- | --- | --- |
| P1 | Inventory repository and recover available conversation context | Complete | [Assessment](../../docs/BASELINE_ASSESSMENT.md) |
| P1 | Constitution, evidence, SOLID, workflows and artifact templates | Implemented, review pending | [P1 design](P1_BASELINE_DESIGN.md) |
| P1 | Orchestrator, specialist skills and Codex/Claude wrappers | Locally verified; live acceptance pending | [P1 design](P1_BASELINE_DESIGN.md) |
| P2 | Validation, safe adoption and failure-oriented tests | Locally verified; live acceptance pending | [P2 design](P2_VALIDATION_DESIGN.md) |
| P2 | Windows/Linux CI workflow | Both hosted jobs passed for implementation revision 131c41e | [Hosted CI evidence](../../evidence/v1.2/HOSTED_CI.md) |
| P3 | Local checks and self-review | Passed: 32 tests, structure, wrapper parity and CLI adoption; self-review only | [Evidence](../../evidence/v1.2/VERIFICATION.md) |
| P3 | Branch/PR delivery | PR merged into master on 2026-10-19 at the owner's explicit request | [PR #1](https://github.com/fahadTheTechIdea/agentic-sdlc-framework/pull/1) |
| P4 | Master-only instructions and new/existing project usage guides | Updated; 32 local tests, structure, wrapper and skill checks passed | [P4 documentation plan and results](P4_MASTER_USAGE.md) |
| P5 | Logging, audit, exception and notification engineering practices | Framework rules implemented; 32 local tests passed; host installation state tracked per machine | [P5 plan and results](P5_OPERATIONAL_SERVICES.md) |
| P6 | Shared sdlc-orch entry name for Codex and Claude | Implemented; 32 local tests and eight entry/skill validations passed | [P6 alias update](P6_SHORT_ENTRY.md) |
| P7 | Nine researched assurance recommendations, skill routing and behavioral evaluation tooling | Implemented; 47 local tests and eight canonical skill checks passed; live model cases remain not run | [P7 plan and results](P7_ASSURANCE.md) |
| P8 | Layered project wizard with technology-specific decision trees | Design documents prepared; structure/parity and 47 existing tests passed; eight layers, mobile selector and native iOS/Android, React Native, MAUI and other blueprints; runtime not implemented | [P8 layer design](P8_LAYERED_WIZARD.md) |
| P9 | Game-domain layers and engine-specific trees | Design prepared: G01-G09 and five engine/language blueprints including separate Godot C#/GDScript; engine/runtime acceptance not run | [P9 game design](P9_GAME_DEVELOPMENT.md) |
| P10 | Current Apple/Google/Steam publishing requirements and GDScript routing | Implemented; structure/parity, 47 existing tests and eight skill checks passed; official profiles dated 2026-10-19; app/account/store acceptance not run | [P10 publishing update](P10_PUBLISHING.md) |
| P11 | Guided setup, per-layer technology freshness and remaining publishing integration | Procedures/templates integrated; structure/parity, 47 regression tests and eight canonical skill validations passed; live task/runtime acceptance not run | [P11 integration](P11_INTEGRATION.md) |
| P12 | Interactive terminal wizard, catalog, persistence and dependency review | Implemented; 67 local tests, structure/parity and eight skill validations passed; actual Windows terminal start/resume verified with a synthetic fixture; 19 initial decision profiles | [P12 runtime](P12_WIZARD_RUNTIME.md) |
| P12 | Short wizard entry for both hosts | Added `sdlc-orch w` (`wizard` also accepted) as request routing in the same skill; no separate command or runtime change; author self-review, live shortcut behavior not evaluated | Canonical orchestrator and wizard guide; required checks recorded in local delivery report |
| Acceptance | Personal Codex and Claude skill discovery | Inventory verified for the owner's local installation on 2026-10-19; refresh checked per revision | Per-machine installation receipt/report; not a claim about all hosts |
| Acceptance | Actual Codex and Claude task behavior | Not run | Needs recorded live scenario runs, separate from host inventories |
| Acceptance | Real application pilot and independent review | Not run | Owner selects pilot/reviewer |
| Acceptance | License copyright, policy acceptance, release/tag | Pending owner decisions | Existing license preserved |

Status records describe the stage reached; implementation is distinct from
local verification, hosted CI, human acceptance and release.
