# Guided setup through sdlc-orch

Use the installed orchestrator in the application folder. It can guide a
conversation using the existing layer and technology blueprints; the framework
does not yet provide an interactive application, registered wizard subcommand,
machine-readable tree resolver or automatic save/resume engine.

## Start a new project

Invoke `$sdlc-orch` in Codex or `/sdlc-orch` in Claude Code, then describe:

```text
Guide me through setting up a new project for [purpose/users]. Use the framework's
layer designs. Help me select the project type, technology and targets. Ask only
the unresolved questions needed for my scope, a small related batch at a time.
Record choices, assumptions, current-source checks and open decisions in the
project's specification, design and tracker. Plan only for now.
```

Replace the final sentence with the implementation scope you want when ready,
such as “Implement and verify the first runnable slice.” Prior authorization
continues to apply; the procedure does not add approval stops at each layer.

## Extend an existing project

```text
Use the layered setup guidance to assess this existing project for [feature].
Inspect its instructions, framework pin, manifests, active plans and shared services
first. Preserve its stack and contracts. Prefill only observed facts with file
references, label recommendations separately, and ask about material unknowns.
Implement and verify the authorized change using this project's Git workflow.
```

This request is scoped to the feature. Wider gaps belong in the existing tracker;
they do not automatically authorize a rewrite, dependency upgrade or migration.

## How the conversation selects layers

1. Capture purpose, users, new/existing mode, deliverables, target platforms,
   constraints and requested output. Reuse answers already provided.
2. Read the [layer contract](../plans/enhancements/wizard/LAYER_CONTRACT.md) and
   [catalog](../plans/enhancements/wizard/TREE_CATALOG.md). Select each deliverable's
   framework/variant. Read only relevant detailed layers and profile blueprints.
3. Work through L01 project, L02 technology, L03 interface, L04 data, L05 security,
   L06 integrations/services, L07 hosting and L08 delivery as needed. Headless UI
   can be N/A with a reason; reporting and security obligations remain applicable.
4. For mobile, use the [mobile map](../plans/enhancements/wizard/MOBILE.md): native
   iOS/Android, MAUI, Flutter and React Native remain distinct. For games, use
   [game groups](../plans/enhancements/wizard/GAMES.md) and the selected Godot C#,
   Godot GDScript, Unity, Unreal or custom host blueprint. Separate targets and
   languages; do not infer export compatibility from an engine name.
5. Apply [technology verification](../core/TECHNOLOGY_FRESHNESS.md) to affected
   choices. Store delivery additionally uses [publishing policy](../core/PUBLISHING_REQUIREMENTS.md)
   and the selected dated store profile, refreshed against live sources.
6. Capture answers with origin (user, observed, recommendation or inferred),
   evidence/uncertainty, dependencies and unresolved decisions in existing project
   artifacts. When a choice changes, retain history and mark affected decisions
   needs_review. Do not imply that an automatic state engine performed this work.
7. Use the existing specification/SDD/ADR, plan and verification templates only
   where needed. Implement within current authorization, then record actual checks.
   Preserve the selected profile, decision state and next action in the handoff.

For an uncataloged technology, capture its intended profile and explicit coverage
gaps; research and develop the missing tree within scope. An inventory entry or
an illustrative blueprint is not tested runtime support. Multiple deliverables
keep distinct profiles connected by actual shared contracts.

Only the orchestrator needs invoking. Specialist procedures are selected as needed;
layers are decision areas, not extra skills, agents or mandatory services.
