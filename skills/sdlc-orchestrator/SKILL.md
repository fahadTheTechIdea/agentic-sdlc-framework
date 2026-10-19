---
name: sdlc-orchestrator
description: Route software delivery requests through the Agentic SDLC framework, selecting a proportional workflow and relevant specialist skills.
---

# SDLC orchestrator

Preferred user entry: `$sdlc-orch` in Codex or `/sdlc-orch` in Claude Code.
This file remains the single orchestrator procedure; the longer
`sdlc-orchestrator` entry also continues to work.

Use paths relative to the framework root (the directory containing `framework.json`).
When adopted in another project this root is `.agentic-framework/`; keep project
artifacts in the project's existing locations.

1. Read `core/ENGINEERING_CONSTITUTION.md` and `core/EVIDENCE_POLICY.md`.
2. Inspect the target repository, applicable instructions, existing plans,
   contracts, tests, branch and uncommitted work. Do not assume a new project.
3. Classify the request using `workflows/DELIVERY.md`: research/plan only, small
   edit, feature, bug, adoption, new project, or incident. Capture acceptance
   criteria, constraints, authorization and unknowns. Scale documentation to risk.
   For application design, implementation or review, read
   `core/LOGGING_AUDIT_NOTIFICATIONS.md`. Inventory shared Log, Audit and Notification
   Services plus a UI Notification Service when a UI exists. Reuse existing
   capabilities, plan missing foundations, and check affected event/error paths.
   Never swallow exceptions or substitute silent success. Record out-of-scope
   application gaps without turning a limited fix into an unrequested rewrite.
   For substantive software changes or reviews, read the relevant sections of
   `core/QUALITY_SECURITY_RELIABILITY.md`. Select affected assurance checks using
   `templates/ASSURANCE.md` or existing project records. For changes to skills,
   prompts, models or tools, select behavioral cases from `evals/README.md`;
   distinguish actual host runs from structural/grader tests.
4. Read only the matching specialist procedures below. These are skill routing
   choices, not instructions to spawn agents or invoke every skill.
5. Maintain one active tracker and requirement-to-evidence mapping. Implement
   authorized slices, run the relevant checks, review, and deliver through the
   project's authorized Git workflow or a precise handoff. Respect instructions
   to work directly on a designated branch; do not create an additional branch
   or PR unless authorized. Ask only for decisions that materially block progress.

| Need | Read |
| --- | --- |
| Unclear requirements, a feature specification or SDD | `skills/sdlc-specification/SKILL.md` |
| Boundaries, SOLID tradeoffs, architecture decision | `skills/sdlc-architecture/SKILL.md` |
| Ownership, phase sequencing and risk | `skills/sdlc-planning/SKILL.md` |
| Implementation or regression fix | `skills/sdlc-implementation/SKILL.md` |
| Claims, tests, review and completion gates | `skills/sdlc-verification/SKILL.md` |
| Session resume or transfer | `skills/sdlc-handoff/SKILL.md` |

For a typo: inspect, make the edit, check it and report. For a major feature:
specify, design, plan, implement, verify and review. A plan-only request stops
after the proposal. Missing runtime/tool access means describe the missing gate;
it never justifies invented output or a fabricated approval.
