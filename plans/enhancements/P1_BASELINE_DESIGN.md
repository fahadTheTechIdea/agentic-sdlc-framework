# Phase 1: policy, skills and adapters — design

## Problem, goals and scope
At revision `02c5944`, `README.md:1` is the only framework description. Implement
REQ-001 through REQ-004 in `specs/V1_2.md` as a portable policy/instruction baseline.

## Design and API surface
Keep shared rules in `core/`, procedures in `skills/`, reusable artifacts in
`templates/`, delivery routing in `workflows/`. `AGENTS.md` and `CLAUDE.md` are
thin host entry points. Generate host skill wrappers from canonical metadata;
avoid independent copies of policy. No application or network API is added.

## Files, errors and compatibility
Add the directories above and `adapters/`, `docs/`, `framework.json`, `VERSION`.
Expand README. Preserve license, Git configuration and existing history.
Missing historical detail is disclosed in the assessment, never invented.
Missing host/tool access remains an explicit acceptance gap.

## Risks and verification
Main risk: static instructions look like guaranteed runtime enforcement. State
limits in README, adapter docs and evidence policy. Verify file/link integrity,
canonical metadata and wrapper synchronization; require separate live host pilots.

## Execution order
1. Record initial assessment and source register.
2. Add shared rules and artifact templates.
3. Add orchestrator and focused skills, then generated wrappers.
4. Review proportional scope, authority and evidence wording.
