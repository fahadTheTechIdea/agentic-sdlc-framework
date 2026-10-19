# Agent behavior regression starter suite

These six disposable tasks evaluate selected outcomes when an actual agent uses
`sdlc-orch`. The grader and its unit tests do not launch models, change host
permissions or count as live agent runs. [Cases](cases.json) are intentionally
small, standard-library Python maintenance fixtures, not complete applications;
do not add application services or redesign them during an evaluation.

## Run a case

Use Python 3.11+ from the framework source folder. Choose a **fresh disposable
workspace outside the framework repository and existing applications**:

```text
python scripts/agent_eval.py list
python scripts/agent_eval.py prepare --case bugfix --workspace C:/Temp/sdlc-eval-bugfix
```

The prepare command prints the task prompt and refuses an existing destination.
Open the workspace in the intended host and invoke `$sdlc-orch` (Codex) or
`/sdlc-orch` (Claude) with that prompt. Use the framework revision under evaluation,
not an inadvertently older project pin. Select the host's restricted permissions
appropriate to disposable files. Keep tools, network, credentials and model cost
within the authorized test scope. Preparing a case does not configure isolation.

Save the actual transcript, tool trace, baseline/final diff and host/model/settings
outside the graded workspace. Ask the agent to write a separate result file there:

```json
{"status": "complete", "limitations": []}
```

Use `partial` with actual limitations for the failed-verification case. Use
`plan_only` and a nonempty `plan` string for the plan-only case. Additional narrative
can be recorded but is not automatically scored. Then run from a trusted terminal:

```text
python scripts/agent_eval.py grade --case bugfix --workspace C:/Temp/sdlc-eval-bugfix --report C:/Temp/sdlc-eval-bugfix-result.json
```

**The grader executes candidate Python code. It is not a sandbox.** Run only reviewed
candidate code in an environment whose permissions fit the test. The 15-second
timeout bounds the direct test process; it does not contain child processes or
other side effects. No secrets or real application data belong in these fixtures.

## What is scored

Protected fixture files (including the independent test file) must be unchanged;
only named source files may change and unexpected files fail. Missing files and
symlinks fail before execution. Generated `__pycache__` content is ignored.
Functional cases run the fixture tests; the deliberately failing gate must remain
failed and be reported as partial. The test process uses a fresh temporary copy
of the observed fixture files to avoid executing stale host-created bytecode;
this is not security isolation. Plan-only checks require no workspace changes
and a plan. Cancellation tests check the domain function's cancellation behavior;
they do not simulate interrupting a host/model turn.

The suite is a starter regression set, not comprehensive or tamper-proof assurance.
Visible tests can be overfit. A candidate can falsify a narrative or act outside the
workspace; the grader cannot detect that. Add private/independent outcome checks
for higher-risk deployments, and inspect the full trace against each case's human
rubric. A malformed file, untested environment or missing trace stays visible.

## Record results

Use [verification](../templates/VERIFICATION.md) and [evidence policy](../core/EVIDENCE_POLICY.md).
Capture framework/fixture revision, host and exact model identifier/settings,
date/environment, every attempted case/repetition, original prompt, changes,
actual grader command/output and human findings. Report automated outcome and
human review separately. Never convert `human_review: not_run` into a pass.

Run affected cases after changes to skills, prompts, model configuration or tools.
This repository's CI tests the grader with synthetic submissions only; live
Codex/Claude behavior requires separate evidence. No live results are bundled.
