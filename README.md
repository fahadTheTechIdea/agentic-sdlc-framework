# Agentic Software Development Framework

Version **1.2.0** — a reviewable baseline for evidence-led software delivery
with Codex, Claude Code, and other assistants. This repository is the intended
home of the framework. It contains instructions, templates, and local tooling;
it is not an autonomous agent runtime or a guarantee against hallucinations.

The framework is available on **`master`**. The original baseline branch has
been merged. Maintenance in this repository uses `master` directly, as requested
by the owner; additional branches and PRs require an explicit owner request.

## Start here

Read [the constitution](core/ENGINEERING_CONSTITUTION.md), then use
[the orchestrator](skills/sdlc-orchestrator/SKILL.md). Describe the outcome once;
the orchestrator selects relevant skills. You do not need to invoke every skill.

Install once per application project, then describe each task to the orchestrator.
It selects a proportionate workflow: a small fix stays small; a substantial
feature can use specification, design, planning, implementation and verification.
Skills are reusable procedures; selecting several does not require multiple agents.

Applications must create or reuse shared **Log, Audit and Notification Services**,
plus a **UI Notification Service** when a UI exists. Exceptions must not be silently
swallowed. Logging/audit coverage, safe channel routing (email, file, UI and other
configured adapters) and failure behavior are part of design and verification.
See [the operational standard](core/LOGGING_AUDIT_NOTIFICATIONS.md) and
[service coverage template](templates/OPERATIONAL_SERVICES.md). Existing projects
extend their active services; this framework update does not modify application code.

- **Codex:** open this repository; `AGENTS.md` routes work. Invoke
  `$sdlc-orchestrator` if you want an explicit entry point.
- **Claude Code:** open this repository; `CLAUDE.md` routes work. Invoke
  `/sdlc-orchestrator` if you want an explicit entry point.
- **ChatGPT or another assistant:** provide the files in
  [the session guide](adapters/generic/SESSION_BOOTSTRAP.md). A repository URL
  alone does not prove the assistant can read its contents.
- **A new or existing application:** follow [adoption instructions](docs/ADOPTION.md), including
  the preview-first installer. Existing project instructions are preserved.

## Install in a new or existing application

Clone the framework source from `master` into its own folder. These commands
run in a terminal; Git and Python 3.11+ must be available:

```text
git clone --branch master https://github.com/fahadTheTechIdea/agentic-sdlc-framework.git
cd agentic-sdlc-framework
```

Choose the application folder separately. For a **new project**, create an empty
application folder first. For an **existing project**, use its current repository
root. Run these commands from the framework source folder, replacing the example
Windows path with the actual application path:

```text
python scripts/adopt.py "C:\Projects\MyApp" --adapter codex
python scripts/adopt.py "C:\Projects\MyApp" --adapter codex --write
```

The first command previews the files; the second installs them. For Claude Code,
replace `codex` with `claude` in both commands. The installer copies the framework
into the application's `.agentic-framework/` folder and adds the selected host's
skill wrappers. It does not create application code or initialize Git.

If the application already has `AGENTS.md` or `CLAUDE.md`, the installer preserves
it. Integrate the snippet from `.agentic-framework/INTEGRATE.md` into that existing
file, preserving the project's current rules. Then open a fresh Codex or Claude
Code session **in the application folder** and check that its instructions and
`sdlc-orchestrator` skill are available. Commit the reviewed integration using
that application's authorized Git workflow. This repository's master-only rule
applies to framework maintenance; it does not change another project's rules.

## Use it for each task

| Host | Explicit entry point |
| --- | --- |
| Codex | `$sdlc-orchestrator` followed by your request |
| Claude Code | `/sdlc-orchestrator` followed by your request |

New project example — put your outcome, technology and constraints after the
host's entry point:

```text
Create an application for [purpose and users] using [technology]. My constraints
are [constraints]. Define measurable requirements, a proportionate architecture,
and a phased plan with a master tracker. Implement the first runnable slice and
verify it. Record assumptions, significant decisions, evidence and remaining gaps.
```

Existing project example:

```text
Implement [feature or fix]. First inspect the existing code, instructions, tests
and active tracker. Reuse existing components and contracts. Extend the current
plans without creating duplicate systems. Implement the change using this
project's authorized Git workflow, run relevant checks, and report evidence and gaps.
```

Add **"plan only"** when you want a proposal before implementation. In later
sessions, use the project's current tracker and [handoff](templates/HANDOFF.md)
to resume; you do not need to reinstall for each task. Installation into another
project creates a snapshot, so future framework updates need a reviewed update.
For both hosts in the same application, follow the second-host instructions in
[the adoption guide](docs/ADOPTION.md) instead of running the installer twice.

## What is included

| Area | Canonical source |
| --- | --- |
| Authority, scope, safety and engineering rules | [Constitution](core/ENGINEERING_CONSTITUTION.md) |
| Evidence and uncertainty | [Evidence policy](core/EVIDENCE_POLICY.md) |
| SOLID and design tradeoffs | [Engineering standards](core/ENGINEERING_STANDARDS.md) |
| Shared logging/audit, exception and notification requirements | [Operational service standard](core/LOGGING_AUDIT_NOTIFICATIONS.md) |
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
