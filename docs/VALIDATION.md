# Validation contract

Run the three commands in README. Python 3.11+ and its standard library suffice.
The manifest `framework.json` pins the baseline version, required files and
canonical skill list. Validator failures exit 1 with readable diagnostics;
successful structural checks exit 0.

Checks include required nonempty files, version agreement, registered skills,
simple `name`/`description` frontmatter, generated adapter parity and local
Markdown inline links. Supported local links are `[label](relative/path)` and
`[label](<relative path>)`, including URL-encoded paths; anchors are ignored.
Reference-style links, HTML links, remote availability and heading anchor
correctness are outside this lightweight checker. Links in fenced code are
ignored, as are inline-code examples. Local links must stay inside the framework root.

Optional records:

```text
python scripts/validate_framework.py --evidence templates/EVIDENCE.json --raci templates/RACI.json
```

Evidence JSON: object with `framework_version` and nonempty `checks` array.
Each check needs unique `id`, nonempty `claim`, `status`, and string-list
`limitations`. Executed checks require full 40-character revision SHA, zoned
ISO timestamp, nonempty environment/scope/command, integer exit code and an
existing output file relative to the record's directory. `verified` requires
zero; `failed` requires nonzero. `not_run` requires a limitation. Commands are
data and are never executed by this validator. Output paths cannot escape the
record directory. Store the JSON at the intended project evidence root.

RACI JSON: `roles` is a nonempty map from role ID to `{kind, name}`; kind is
`human`, `role`, or `agent`. `assignments` is a nonempty list with unique `id`,
nonempty `deliverable`, and `R`, `A`, `C`, `I` arrays of registered role IDs.
Each row requires at least one R and exactly one A; the A cannot be an agent.
One person/role can have multiple responsibility types. No real identity,
organizational authority, consent or approval is authenticated by this check.

The regression suite mutates disposable copies to exercise rejection behavior.
It also checks installer preview, preservation, collision handling and generated
adapter drift. Static and local checks do not prove live host discovery, model
behavior, application quality, production safety or elimination of hallucinations.

The validator also checks [the agent case inventory](../evals/cases.json): unique
case IDs, safe relative fixture paths, protected tests, editable-file scope, expected
outcomes and human rubric presence. [The evaluation guide](../evals/README.md)
explains prepare/grade commands. The regression suite tests both accepted and
rejected synthetic submissions, including deleted/weakened tests, changed user
work, untrusted-payload artifacts, false completion and cancellation behavior.
This validates evaluation tooling, not live agent compliance. No models are
launched by the grader or CI. Application scans, access tests, recovery drills,
browser/device/provider checks and operational objectives must be verified in
their actual projects through [assurance records](../templates/ASSURANCE.md).

Publishing profiles are dated research documents, not executable compliance tests.
The framework validates their presence/links and skill/template integration only;
it does not query live store policy, accounts, signing, testers, native-library
compatibility, review approvals or release state. Apply
[publishing policy](../core/PUBLISHING_REQUIREMENTS.md) and record actual evidence
in [publishing readiness](../templates/PUBLISHING_READINESS.md). Static checks or
author wording scenarios cannot establish live agent/store behavior.

The [setup conversation](PROJECT_SETUP.md) and
[technology verification policy](../core/TECHNOLOGY_FRESHNESS.md) are maintained
procedures. Presence and link checks do not execute a setup conversation, resolve
technology trees, inspect live version support, or invalidate/persist answers.
The technology review template records scoped evidence; it is not an automated
all-stack compatibility check. Per-machine host discovery must be recorded
separately from actual agent behavior and project acceptance.
