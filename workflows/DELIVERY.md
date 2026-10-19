# Delivery workflows

## Select the smallest sufficient workflow

| Request | Required approach | Artifacts when justified |
| --- | --- | --- |
| Small reversible edit | Inspect → edit → focused check → report | Existing task or PR note |
| Feature or significant refactor | Discover → specify → design → plan → implement slices → verify → review | Specification, SDD, tracker, verification |
| Bug | Reproduce → identify cause → smallest fix → regression check → review | Bug evidence; ADR only for a design decision |
| New project | Clarify outcomes → inventory constraints → architecture → first runnable slice → gates | Specification, SDD, RACI, plan, decisions |
| Existing project adoption | Inventory → map existing conventions → fill gaps → pilot one slice | Adoption mapping; preserve existing artifacts |
| Research or plan only | Inspect sources → alternatives → recommendation | Evidence-backed proposal; no implementation |
| Incident or risky migration | Establish impact → authorized containment → recovery/rollback → verify | Incident log, recovery evidence, accountable owner |

## Phase gates

1. **Discover:** read applicable instructions, current state, source, tests and
   active trackers. Record proven facts separately from assumptions.
2. **Specify:** problem, non-goals, requirement IDs, measurable criteria, constraints
   and owner. Resolve only decisions that block safe progress.
3. **Design:** boundaries, contracts, dependencies, failure modes, data/security
   considerations and alternatives. Use SDD and ADR proportional to impact.
   For applications, apply `core/LOGGING_AUDIT_NOTIFICATIONS.md` and complete the
   shared-service/event coverage matrix: Log, Audit, Notification and UI Notification
   Service when a UI exists. Reuse current implementations and track missing foundations.
4. **Plan:** atomic tasks, ownership, dependencies, checks, recovery and scope.
   RACI assigns exactly one accountable role for each decision/deliverable.
   Record user authorization already present; do not invent a new approval gate.
5. **Implement:** one coherent slice at a time; reuse active code and contracts.
   Verify each slice. Keep trackers and decisions consistent with actual changes.
6. **Verify/review:** run affected checks and the project's required regression
   gates. Check failure paths, SOLID tradeoffs, security and operational risks.
   Verify exception reporting, truthful audit outcomes, channel failure handling,
   redaction and UI notification isolation against the operational service matrix.
   Record self-review versus independent review accurately.
7. **Deliver:** publish reviewable commits to the owner's designated branch, or
   use a branch/PR when that is the authorized project workflow. The framework
   source repository `fahadTheTechIdea/agentic-sdlc-framework` uses master directly
   unless its owner explicitly requests otherwise.
   Include outcomes, evidence and gaps. Release/deployment is a separate authorized
   action. Preserve a useful handoff for unfinished work.

## Working limits

Load the constitution and evidence policy once, then read only relevant skill
references. Set an effort/tool budget appropriate to the request. If repeated
attempts produce no new evidence, diagnose the cause and change approach;
escalate only when a user decision or external change is necessary. Record the
last useful result and next action rather than looping or declaring success.
Do not run parallel writers on shared files without explicit coordination.
