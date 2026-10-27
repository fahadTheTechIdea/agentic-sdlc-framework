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
[the orchestrator](skills/sdlc-orch/SKILL.md). Describe the outcome once;
the orchestrator selects relevant skills. You do not need to invoke every skill.

With a user-level installation, use the orchestrator in new or existing project
folders without copying the framework into each application. Use the optional
project installer below when the team needs a committed, pinned snapshot.
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

The [quality, security and reliability standard](core/QUALITY_SECURITY_RELIABILITY.md)
adds test integrity and executable gates, agent behavior evaluations, authorization
and isolation, validated configuration/secrets, safe retries/cancellation, recovery
drills, runtime health, dependency verification and host-enforced tool permissions.
Use [the assurance matrix](templates/ASSURANCE.md) for applicable checks and evidence;
reuse existing project controls and keep small changes small. The six-case
[agent evaluation starter](evals/README.md) includes an executable outcome grader.
Grader tests do not establish live Codex/Claude behavior or application compliance.

- **Codex:** open this repository; `AGENTS.md` routes work. Invoke
  `$sdlc-orch` if you want an explicit entry point.
- **Claude Code:** open this repository; `CLAUDE.md` routes work. Invoke
  `/sdlc-orch` if you want an explicit entry point.
- **ChatGPT or another assistant:** provide the files in
  [the session guide](adapters/generic/SESSION_BOOTSTRAP.md). A repository URL
  alone does not prove the assistant can read its contents.
- **A new or existing application:** follow [adoption instructions](docs/ADOPTION.md), including
  the preview-first installer. Existing project instructions are preserved.

The longer `sdlc-orchestrator` name remains supported. Both names use the same
orchestrator procedure; `sdlc-orch` is the preferred name for everyday use.

For guided project choices, ask the orchestrator to use
[the setup conversation](docs/PROJECT_SETUP.md). It selects relevant technology
and layer blueprints, records decisions in your existing project documents, and
continues within your requested plan or implementation scope.

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
`sdlc-orch` skill are available. Commit the reviewed integration using
that application's authorized Git workflow. This repository's master-only rule
applies to framework maintenance; it does not change another project's rules.

## Use it for each task

| Host | Explicit entry point |
| --- | --- |
| Codex | `$sdlc-orch` followed by your request |
| Claude Code | `/sdlc-orch` followed by your request |

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
| Layer-specific technology and standards checks | [Technology verification](core/TECHNOLOGY_FRESHNESS.md), [review template](templates/TECHNOLOGY_REVIEW.md) |
| SOLID and design tradeoffs | [Engineering standards](core/ENGINEERING_STANDARDS.md) |
| Keep feature/fix documentation current; replace or remove obsolete files | [Documentation maintenance](core/ENGINEERING_STANDARDS.md#documentation-maintenance-replace-or-remove) |
| Shared logging/audit, exception and notification requirements | [Operational service standard](core/LOGGING_AUDIT_NOTIFICATIONS.md) |
| Current store publishing and release evidence | [Publishing policy](core/PUBLISHING_REQUIREMENTS.md), [readiness template](templates/PUBLISHING_READINESS.md) |
| Quality gates, security, reliability and tool trust | [Assurance standard](core/QUALITY_SECURITY_RELIABILITY.md), [matrix](templates/ASSURANCE.md) |
| Agent behavior regression tasks and outcome grading | [Evaluation guide](evals/README.md) |
| Routing and lifecycle | [Orchestrator](skills/sdlc-orch/SKILL.md), [workflows](workflows/DELIVERY.md) |
| Independent multi-lane review with capped fix rounds, approver and human escalation | [Review cycle policy](core/REVIEW_CYCLE.md), [guide](docs/REVIEW_CYCLE.md), [skill](skills/sdlc-review-cycle/SKILL.md) |
| SDD, RACI, ADR, handoff and verification | [Templates](templates/README.md) |
| Focused reusable procedures | [Skill catalog](skills/CATALOG.md) |
| Validation contract and limits | [Validation guide](docs/VALIDATION.md) |
| Initial assessment, provenance and outstanding decisions | [Assessment](docs/BASELINE_ASSESSMENT.md) |
| Implementation and acceptance status | [Master tracker](plans/enhancements/MASTER_TRACKER.md) |

## Review cycle

For a significant or high-risk change, `$sdlc-orch review` (Codex) or
`/sdlc-orch review` (Claude) runs the [review cycle](docs/REVIEW_CYCLE.md): specialist
reviewer lanes (code, security, UX, UI design and others) each review the same
revision, every lane must report, requested changes return to the builder for a
capped number of rounds, a fully passing round reaches an approver, and anything
unresolved goes to the named accountable human. `scripts/review_cycle.py` is the
deterministic gate that enforces the sequence over a record in the project. An agent
approver gives a recommendation, never human approval or authority to merge; delivery
stays under the project's authorized Git workflow. Optional Claude Code subagent and
Codex custom-agent templates are in `adapters/`. Unit tests exercise the gate with
synthetic records; no live Codex or Claude review run has been evaluated.
See [the plan and results](plans/enhancements/P13_REVIEW_CYCLE.md).

## Interactive project wizard and layer designs

The [terminal wizard](docs/WIZARD.md) now supports 19 application/mobile/game
decision profiles, conditional questions, multiple deliverables, saved answers,
resume/back/defer, dependency review and a decision summary. From the framework root:

```text
python scripts/project_wizard.py start "C:\Projects\MyApp" --write --interactive
python scripts/project_wizard.py run "C:\Projects\MyApp\.sdlc\wizard.json"
```

The application folder must exist. Without `--write`, `start --profile PROFILE`
previews without writing. Add `--mode existing` for path-only project inventory.
Use **`$sdlc-orch w`** in Codex or **`/sdlc-orch w`** in Claude; it can use
the same engine conversationally if terminal input is unavailable. No extra skill
or dependency installation is required. See [the runtime plan](plans/enhancements/P12_WIZARD_RUNTIME.md).

The [wizard design](plans/enhancements/P8_LAYERED_WIZARD.md) develops the eight
project setup steps as layers, each with nested questions and technology-specific
decision trees. An extensible catalog covers multiple project families; Blazor
and Django are examples, not the scope boundary. Starter blueprints show
different website, API, mobile/desktop, worker, CLI and library paths. The
[mobile selection map](plans/enhancements/wizard/MOBILE.md) includes native iOS
(SwiftUI/UIKit), native Android (Kotlin/Java, Compose/Views), React Native, Flutter
and [.NET MAUI native-controls/Blazor Hybrid](plans/enhancements/wizard/MAUI.md).
The runtime catalog implements initial decision trees derived from these designs;
the broader inventory and deeper specialized branches are not all implemented.
Version-qualified technology support and automatic source research remain separate.

The [guided setup procedure](docs/PROJECT_SETUP.md) makes these documents usable
in a conversation or through the terminal runtime. [Technology verification](core/TECHNOLOGY_FRESHNESS.md)
defines official-source checks, compatibility evidence and refresh triggers across
affected layers. It preserves project pins and makes missing evidence explicit;
it does not automatically update dependencies or certify every catalog entry.

The [game development extension](plans/enhancements/wizard/GAMES.md) adds game-specific
concept, simulation, world, input, gameplay/AI, asset, save/replay, multiplayer and
performance/playtest trees. Engine blueprints distinguish Godot C#/.NET and
[Godot GDScript](plans/enhancements/wizard/games/GODOT_GDSCRIPT.md), Unity C#,
Unreal C++/Blueprints and custom .NET game/simulation hosts. Godot/C# is the owner's
preferred starting profile, with target/export compatibility checked independently.
See [the game development plan](plans/enhancements/P9_GAME_DEVELOPMENT.md).

## Store publishing requirements

[Publishing policy](core/PUBLISHING_REQUIREMENTS.md) routes store-readiness work to
dated official-source profiles for [Apple App Store](docs/publishing/APPLE_APP_STORE.md),
[Google Play](docs/publishing/GOOGLE_PLAY.md) and [Steam](docs/publishing/STEAM.md),
checked 2026-10-19. They cover applicable SDK/target, privacy/content, native-library,
account/testing/review, signing and release timing gates. Record actual evidence
with [publishing readiness](templates/PUBLISHING_READINESS.md).

Recheck official pages and actual console scope before submission/release; this
snapshot cannot guarantee future policy or account eligibility. Source conflicts
are explicit, including Steam's differing waiting-period pages. Framework updates
do not submit an app, pay fees or publish to a store.

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
