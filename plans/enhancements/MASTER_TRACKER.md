# Framework v1.2 — master tracker

Specification: [v1.2 scope](specs/V1_2.md).
Authorization: current request permits assessment and implementation on a branch/PR.
Policy acceptance and release remain repository-owner decisions.

| Phase | Task | Status | Design/evidence |
| --- | --- | --- | --- |
| P1 | Inventory repository and recover available conversation context | Complete | [Assessment](../../docs/BASELINE_ASSESSMENT.md) |
| P1 | Constitution, evidence, SOLID, workflows and artifact templates | Implemented, review pending | [P1 design](P1_BASELINE_DESIGN.md) |
| P1 | Orchestrator, specialist skills and Codex/Claude wrappers | Locally verified; live acceptance pending | [P1 design](P1_BASELINE_DESIGN.md) |
| P2 | Validation, safe adoption and failure-oriented tests | Locally verified; live acceptance pending | [P2 design](P2_VALIDATION_DESIGN.md) |
| P2 | Windows/Linux CI workflow | Configured, hosted run pending | [P2 design](P2_VALIDATION_DESIGN.md) |
| P3 | Local checks and self-review | Passed: 32 tests, structure, wrapper parity and CLI adoption; self-review only | [Evidence](../../evidence/v1.2/VERIFICATION.md) |
| P3 | Branch/PR delivery | In progress | [P3 design](P3_REVIEW_DESIGN.md) |
| Acceptance | Fresh Codex and Claude discovery/behavior checks | Not run | Needs separate host sessions |
| Acceptance | Real application pilot and independent review | Not run | Owner selects pilot/reviewer |
| Acceptance | License copyright, policy acceptance, release/tag | Pending owner decisions | Existing license preserved |

Status records describe the stage reached; implementation is distinct from
local verification, hosted CI, human acceptance and release.
