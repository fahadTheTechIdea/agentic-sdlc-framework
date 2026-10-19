# Phase 5: logging, audit, exceptions and notifications

Date: 2026-10-19. Authorization: owner's request to add these practices to the
framework. Work on master directly. Refresh both previously installed user copies
so subsequent Codex/Claude work receives the updated rules.

## Problem and outcomes

At master revision `e567f84738e3cd3342ae45891823ad8e1287a6ef`, engineering standards
mention observability but do not require shared Log/Audit/Notification Services,
UI Notification Service or a complete exception/event coverage contract.

Implement REQ-008 with one canonical operational standard, a reusable service/event
coverage matrix, routing in the orchestrator and specialist procedures, and checks
in application design/planning/verification templates. Reuse active services and
contracts; UI notification is conditional on UI presence. Application projects
themselves are outside this framework-update task.

## Design and boundaries

`core/LOGGING_AUDIT_NOTIFICATIONS.md` owns the rules. The existing seven skills
reference it; no parallel observability skill or runtime library is added.
`templates/OPERATIONAL_SERVICES.md` captures real implementations, event coverage,
exception ownership, durable audit intent, channel routing/failure policy and UI
scope. The constitution, engineering standards, README and delivery workflow route
to this source. Manifest required-file/link checks include the new resources.

The source register distinguishes owner requirements from external implementation
guidance. Never hide an exception or failed audit/channel operation; define
observable failure, recovery and emergency diagnostic behavior without recursive
notification loops. Do not send every raw event to email/UI or expose sensitive data.

## Execution and gates

1. Inspect existing rules and source guidance; add canonical requirements.
2. Extend active skills and templates; register files and update docs/tracker.
3. Run structure, wrapper parity, all canonical skill checks and the existing
   regression suite. Static checks do not prove application compliance.
4. Commit/push master; inspect hosted Windows/Linux CI.
5. Preserve the prior installed snapshot, back up owned user integration files,
   install the new committed snapshot and refresh both host references. Verify
   file integrity, skill validation and host discovery without changing application code.

## Verification and limits

Local checks on Windows/Python 3.14.3, 2026-10-19: framework file/link/template and
existing evidence/RACI validation passed; generated adapter parity passed; all
32 existing regression tests passed; all seven canonical skill validations passed;
`git diff --check` passed. Source state: master at `e567f84738e3cd3342ae45891823ad8e1287a6ef`
with the P5 documentation/skill changes before commit. Self-review only.

Hosted results belong to the CI run for the published commit. User-level snapshot
updates and host discovery are per-machine installation operations; their exact
source revision, backups, integrity and results belong in that machine's
installation receipt rather than this portable repository's application evidence.

The operational rules are implemented in the framework. Actual logging/audit/channel
providers, UI isolation and application durability require tests in each adopting
application and are not established by these framework checks. No existing
application repository was changed by this policy update.
