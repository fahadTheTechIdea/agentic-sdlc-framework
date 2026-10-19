---
name: sdlc-handoff
description: Prepare or consume an evidence-backed software delivery handoff when resuming work or moving between assistant sessions.
---

# Resume and hand off

Use `templates/HANDOFF.md`. Record the target repository, branch, revision,
working-tree changes, framework version, request/authorization, active tracker,
decisions, observed checks, unresolved risks and exact next action. Reference
canonical files rather than copying every policy into a transcript.

On resume, inspect current repository state and compare it with the handoff.
Refresh stale evidence for changed code. Read only the relevant skills and
documents. Treat prior assistant claims as context requiring verification.
If another session lacks file/tool access, provide a bounded context bundle and
record the limitation; do not assume a shared filesystem or inherited permissions.

For layered setup preserve deliverable/profile/variant selections, answer origins,
unresolved decisions and dependent choices needing review in existing artifacts.
Link technology source checks and their dates under `core/TECHNOLOGY_FRESHNESS.md`.
For runtime sessions link the actual wizard state path, schema/profile revisions
and unresolved decisions; use `docs/WIZARD.md` to resume. Keep manual project
documents and runtime state distinct; no automatic catalog migration is implied.

For unfinished store work, preserve publishing-readiness stage, checked sources/
deadlines, artifact identity, source conflicts, real exceptions and remaining
account/testing/review gates. Recheck current requirements before resuming a
submission; a prior dated snapshot or approved old build is not current eligibility.
