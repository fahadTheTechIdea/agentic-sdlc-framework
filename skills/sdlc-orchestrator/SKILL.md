---
name: sdlc-orchestrator
description: Route software delivery requests through the Agentic SDLC framework, selecting a proportional workflow and relevant specialist skills.
---

# SDLC orchestrator

Preferred user entry: `$sdlc-orch` in Codex or `/sdlc-orch` in Claude Code.
This file remains the single orchestrator procedure; the longer
`sdlc-orchestrator` entry also continues to work.

Short wizard request: `$sdlc-orch w` in Codex or `/sdlc-orch w` in Claude.
When the invocation request is `w` or `wizard` (case-insensitive), route directly
to the interactive/persisted setup procedure in `docs/WIZARD.md` for the active
project. Resume its existing wizard state when present; otherwise begin project/
profile selection. No full sentence is required. These are request shortcuts
inside the existing skill, not separately registered host commands. Preserve the
same scope, state guards and project pins as the normal wizard request.

Short review request: `$sdlc-orch review` or `rc` in Codex, `/sdlc-orch review` or
`rc` in Claude. When the invocation request is exactly `review` or `rc`
(case-insensitive), route to `skills/sdlc-review-cycle/SKILL.md` for the active
change: resume its record under `.sdlc/review/` when one exists, otherwise open a
cycle only if the change meets the use conditions in `core/REVIEW_CYCLE.md`. It is
a request shortcut like `w`; it authorizes no agents, merge or release.

Use paths relative to the framework root (the directory containing `framework.json`).
When adopted in another project this root is `.agentic-framework/`; keep project
artifacts in the project's existing locations.

1. Read `core/ENGINEERING_CONSTITUTION.md` and `core/EVIDENCE_POLICY.md`.
2. Inspect the target repository, applicable instructions, existing plans,
   contracts, tests, branch and uncommitted work. Do not assume a new project.
   Before creating feature/fix/plan documents, apply the documentation maintenance
   section of `core/ENGINEERING_STANDARDS.md`: find the active owner, update it,
   replace/remove obsolete guidance and reconcile references within scope.
3. Classify the request using `workflows/DELIVERY.md`: research/plan only, small
   edit, feature, bug, adoption, new project, or incident. Capture acceptance
   criteria, constraints, authorization and unknowns. Scale documentation to risk.
   For guided new-project setup or an existing-project setup assessment, read
   `docs/PROJECT_SETUP.md`. Use only relevant layer/profile blueprints; record
   decisions in existing project artifacts. For an interactive/persisted wizard,
   read `docs/WIZARD.md` and use `scripts/project_wizard.py` from the selected
   framework root. Resume existing state; a new session previews until explicitly
   saved. If terminal input is unavailable, ask the catalog questions and use the
   same noninteractive engine: `questions STATE --next` reads a relevant prompt,
   and `answer` saves the response with accurate origin. Do not run an
   unattended prompt loop, overwrite state or imply application scaffolding.
   When choosing/changing technology or checking current standards, apply
   `core/TECHNOLOGY_FRESHNESS.md`; preserve pins and separate documented support
   from actual compatibility checks. Do not load the entire catalog for a small fix.
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
   For distribution design, packaging, store readiness or published-app updates,
   read `core/PUBLISHING_REQUIREMENTS.md` and the selected Apple/Google/Steam
   profile. Recheck official sources and console scope before eligibility claims;
   record deadlines, granted exceptions, conflicts and unverified external gates.
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
| Independent multi-lane review of a significant or high-risk change, with capped fix rounds and an approver | `skills/sdlc-review-cycle/SKILL.md` |
| Session resume or transfer | `skills/sdlc-handoff/SKILL.md` |

For a typo: inspect, make the edit, check it and report. For a major feature:
specify, design, plan, implement, verify and review. A plan-only request stops
after the proposal. Missing runtime/tool access means describe the missing gate;
it never justifies invented output or a fabricated approval.
