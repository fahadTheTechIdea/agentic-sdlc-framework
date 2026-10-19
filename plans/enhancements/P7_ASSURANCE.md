# P7: Research-backed assurance rules and agent evaluations

Authorized 2026-10-19: owner accepted all nine researched recommendations.
Work directly on master, preserving current contracts, skills and installations.

## Acceptance and implementation

1. One canonical standard covers test integrity, agent evaluations, authorization,
   configuration/secrets, safe retries, recovery, runtime health, dependencies and
   agent/tool trust. Apply proportionally and reuse existing implementations.
2. Route the relevant skills and workflow to the standard; extend SDD/verification
   with a reusable assurance matrix. Keep `sdlc-orch` as the shared entry point.
3. Provide isolated starter tasks and an executable outcome grader, including
   failure-oriented tooling tests. Keep live agent results distinct from grader tests.
4. Register sources and new artifacts; run framework validation, adapter parity,
   regression tests and required skill validation. Record limitations honestly.
5. Commit/push master, inspect hosted checks, and refresh only receipt-owned personal
   Codex/Claude integrations with backups. Do not alter pinned application versions.

## Verification and remaining acceptance

Implemented: [canonical standard](../../core/QUALITY_SECURITY_RELIABILITY.md),
[assurance matrix](../../templates/ASSURANCE.md), workflow/skill/template routing,
source register and [six-case evaluation tooling](../../evals/README.md).

Local verification on 2026-10-19: 47 tests passed, framework structure and adapter
parity passed, and all eight canonical skill files passed the Skill Creator check.
Tests cover rejection of broken source, weakened/deleted tests, changed user work,
plan-only violations, false completion, injection artifacts, cancellation, stale
bytecode, invalid fixture inventories and unsafe destinations. The full regression
also validates all three adoption modes; the installer now bundles `evals/`.

See [captured evidence](../../evidence/p7/VERIFICATION.md) for exact scope and logs.
Hosted CI and per-machine installation state are recorded externally after publishing;
inspect the commit's Actions checks and the local installation receipt for current state.
Live model scenarios and application/provider/recovery drills are separate gates;
framework rules and grader unit tests cannot establish those outcomes.
