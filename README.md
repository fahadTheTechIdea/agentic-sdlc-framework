# Agentic Software Development Framework

Version **1.2.0** — a reviewable baseline for evidence-led software delivery
with Codex, Claude Code, and other assistants. This repository is the intended
home of the framework. It contains instructions, templates, and local tooling;
it is not an autonomous agent runtime or a guarantee against hallucinations.

## Start here

Read [the constitution](core/ENGINEERING_CONSTITUTION.md), then use
[the orchestrator](skills/sdlc-orchestrator/SKILL.md). Describe the outcome once;
the orchestrator selects relevant skills. You do not need to invoke every skill.

- **Codex:** open this repository; `AGENTS.md` routes work. Invoke
  `$sdlc-orchestrator` if you want an explicit entry point.
- **Claude Code:** open this repository; `CLAUDE.md` routes work. Invoke
  `/sdlc-orchestrator` if you want an explicit entry point.
- **ChatGPT or another assistant:** provide the files in
  [the session guide](adapters/generic/SESSION_BOOTSTRAP.md). A repository URL
  alone does not prove the assistant can read its contents.
- **Another project:** follow [adoption instructions](docs/ADOPTION.md), including
  the preview-first installer. Existing project instructions are preserved.

Example request:

> Use the Agentic Software Development Framework v1.2. Inspect this project,
> build a customer import feature with measurable acceptance criteria, and
> carry the authorized work through implementation and verification. Reuse
> existing components. Record decisions, evidence, and remaining gaps.

## What is included

| Area | Canonical source |
| --- | --- |
| Authority, scope, safety and engineering rules | [Constitution](core/ENGINEERING_CONSTITUTION.md) |
| Evidence and uncertainty | [Evidence policy](core/EVIDENCE_POLICY.md) |
| SOLID and design tradeoffs | [Engineering standards](core/ENGINEERING_STANDARDS.md) |
| Routing and lifecycle | [Orchestrator](skills/sdlc-orchestrator/SKILL.md), [workflows](workflows/DELIVERY.md) |
| SDD, RACI, ADR, handoff and verification | [Templates](templates/README.md) |
| Focused reusable procedures | [Skill catalog](skills/CATALOG.md) |
| Validation contract and limits | [Validation guide](docs/VALIDATION.md) |
| Initial assessment, provenance and outstanding decisions | [Assessment](docs/BASELINE_ASSESSMENT.md) |
| Implementation and acceptance status | [Master tracker](plans/enhancements/MASTER_TRACKER.md) |

## Validate locally

Python 3.11 or later; no third-party dependencies:

```text
python scripts/validate_framework.py
python -m unittest discover -s tests -v
python scripts/sync_adapters.py --check
```

CI runs these checks on Windows and Linux. Checks establish structure,
consistency, and selected failure behavior; they do not establish the quality
of every design or the behavior of a live assistant.

The v1.2 designation is reconstructed from the current request. Detailed prior
assistant proposals could not be recovered from the referenced conversation.
See the assessment before treating this as a verbatim historical agreement.
The existing [MIT license](LICENSE.txt) is preserved; its copyright placeholders
still need an owner-supplied value.
