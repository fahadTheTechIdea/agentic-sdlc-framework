# Game development layers and selection map

Status: design extension to [the existing layered wizard](../P8_LAYERED_WIZARD.md).
Plan: [P9](../P9_GAME_DEVELOPMENT.md). Uses [the tree model](TREE_MODEL.md) and
[layer contract](LAYER_CONTRACT.md). No runnable game wizard is registered.

## Choose the game, engine and targets independently

```text
Game or simulation
  Experience: genre / core loop / audience / first playable outcome
  Presentation: 2D / 3D / mixed, with perspective and interaction requirements
  Execution: real-time / turn-based / hybrid
  Players: local single player / local multiplayer / online
  Engine
    Godot → C#/.NET preferred for this owner / other language profile
    Unity → C# and the actual project execution/tooling choices
    Unreal → C++ / Blueprints / mixed
    Custom .NET host → selected rendering/input/platform adapters
    Other engine → profile detail and compatibility evidence required
  Targets: desktop / mobile / browser / console / XR / headless server
    Resolve engine + language + version + renderer/export + target compatibility
  Existing L01-L08 roots + applicable G01-G09 game-domain trees
```

Genre and engine are not the same choice: an engine can serve multiple game types,
and the same concept can have different engine implementations. Requested targets
and known project pins constrain the choice. Do not silently switch language or
engine to make an export option appear available.

## G01: Concept and playable scope

Questions: player fantasy/problem, audience, genre or genre mix, core repeatable
loop, win/loss/progression conditions, interaction/perspective, target session
length, content scope and non-goals. Open genre-specific children: puzzle rules,
platformer movement/challenge, strategy/economy turns, action/combat feedback,
RPG quests/progression, simulation goals or a custom description.

Output: a game brief or existing GDD section linked to the specification, plus a
small first-playable acceptance scenario. Human playtesting checks whether the
loop is understandable/enjoyable; passing unit tests cannot establish fun.
Owner: L01/L08. No monetization, online account or large feature list is implied.

## G02: Rules, time, simulation and physics

Questions: real-time/turn-based/hybrid, authoritative state, tick versus render
timing, pause/time scaling, physics use, units/coordinates, random seeds and replay/
determinism needs. If cross-engine reuse is requested, separate portable rules
from engine-native objects and lifecycle through explicit adapters.

Output: update ownership/order, command/state/event contracts, physics boundary and
testable invariants. Single-writer state and deterministic behavior are choices to
justify, not labels inferred from C# or a fixed step. Check repeated updates,
ordering, cancellation/pause and seeded scenarios as applicable. Owner: L02/L04.

## G03: World, scenes, entities and levels

Questions: level/world scope, engine scene/object composition, entity/component
ownership, spawning/despawning, loading/streaming, persistent versus scene-local
state, navigation and procedural generation. Branch into authored levels,
generated worlds or mixed content only as needed.

Output: world/entity/scene boundaries, loading/unloading policy, identity/reference
rules and content validation. Check stale references, duplicate spawning, missing
content and disposal/lifetime behavior. Reuse existing entities/contracts rather
than create an unrelated universal engine model. Owner: L02/L04/L06.

## G04: Input, player control, cameras and accessibility

Questions: keyboard/mouse/controller/touch/XR devices, remapping, focus/UI capture,
camera perspective/control, player movement, pause/menu interactions, accessibility,
localization and per-target adaptation. Multiple local players add input/player
ownership and split-screen/camera requirements.

Output: input/action and player/camera contracts plus observable interaction cases.
Check UI versus gameplay input, reconnect/focus changes and target-specific controls.
Owner: L03/L05. Input mapping does not authorize a remote gameplay action.

## G05: Gameplay systems and AI

Questions: only selected mechanics, such as combat, inventory, building, crafting,
quests, dialogue, economy, progression, turns, AI state/decision/navigation and
difficulty/balance configuration. Each mechanic opens its own rules, lifecycle,
data, edge cases and acceptance branches.

Output: feature slices, state/rule contracts, data definitions and balancing
assumptions. Test invariants and failure paths; use playtests to evaluate experience.
Prefer existing engine/project systems. Do not build every possible mechanic or
a universal ECS/AI framework by default. Owner: L01/L02/L04.

## G06: Presentation and content pipeline

Questions: renderer/pipeline and target constraints, sprites/models/materials,
animation, audio, VFX, game HUD/menus/UI notifications, localization and content
creation/import workflow. Record source assets, authorship/licenses, import settings,
stable references, package/plugin versions and generated/derived content policy.

Output: presentation/asset map and frame/memory/loading budgets linked to target
checks. Separate logical gameplay state from engine resources where reuse needs it.
Check missing assets, import/reference integrity, lifecycle and player-visible
failure states; engine/editor success does not prove exported content integrity.
Owner: L03/L04/L06. Asset acquisition or redistribution needs applicable authority.

## G07: Saves, settings, content and replay

Questions: whether saves are needed, state authority/schema, checkpoints/autosave,
settings and input preferences, version evolution, content IDs, atomic writes,
corruption/recovery, cloud sync and optional replay. A replay requires a designed
command/timing/randomness model, not just serialized positions.

Output: save/content contract, migration/recovery policy and compatibility checks.
Check round-trip, interrupted writes, old/corrupt saves, duplicate sync and recovery
on the actual target. Never invent progress or silently replace a failed save with
success. Owner: L04/L05/L06. Do not create a server database for a local save file.

## G08: Multiplayer and online capabilities

Questions: none/local-only/online; player/session counts and topology; authority
and command validation; replication, prediction/interpolation/rollback/lockstep
only when justified; join/leave/reconnect; latency/loss; identity, lobby/matchmaking,
leaderboards, economy and other requested services.

Output: network/authority/session contracts, trust boundaries and online-service
requirements. Treat client commands as untrusted, protect player/account data and
validate reward/inventory changes at their authority. Test packet loss/replay,
duplicate/out-of-order inputs, disconnect/reconnect, exploits and load as applicable.
Owner: L02/L05/L06/L07. Single-player selection skips online questions with reasons.

## G09: Performance, playtesting and distribution

Questions: target devices/hardware, frame-time and memory/loading budgets,
allocation/GC sensitivity, physics/tick/network budgets, profiling, accessibility/
playtests, builds/exports, packaging, signing, storefront or console/vendor gates.
Choose numeric budgets with the actual product/hardware; no universal FPS target.

Output: first-playable and vertical-slice gates, measured runtime evidence,
regressions and target-specific release checklist. Separate headless rule checks,
editor tests, exported builds, real gameplay, devices, network and store evidence.
Owner: L07/L08. Profiles do not provision accounts, purchase licenses or publish.

## Engine-specific implementations of the game trees

| Engine/profile | Detailed tree | Coverage status |
| --- | --- | --- |
| Godot with C#/.NET | [Godot](games/GODOT.md) | Design blueprint; owner's preferred starting profile |
| Unity with C# | [Unity](games/UNITY.md) | Design blueprint; actual runtime/target compatibility unresolved |
| Unreal C++/Blueprints | [Unreal](games/UNREAL.md) | Design blueprint; C# is not implied |
| Custom .NET game/simulation host | [Custom .NET](games/CUSTOM_DOTNET.md) | Design blueprint; rendering/input/library selection explicit |
| Godot/GDScript, MonoGame/FNA, Stride, Bevy, Phaser, Defold, GameMaker or another engine | Future explicit profiles | Inventory only; do not claim complete trees or target support |

These are examples, not a closed engine list or a claim of runtime support.
A separate backend, launcher, editor/content tool or website is a linked deliverable
with its own appropriate profile.

## Portable C# logic and engine adapters

When portability is a real requirement, keep reusable rules/simulation/save DTOs
independent of Godot nodes, Unity objects, Unreal types, renderer/input and platform
SDKs. Host adapters translate input into commands, own lifecycle/timing integration
and present state/events through each engine's scene/rendering/UI systems.

Use this boundary only where justified. For a small engine-native prototype, a
second framework or abstraction layer may be unnecessary. Existing shared cores
and contracts take priority over inventing replacements.

Godot and Unity both using C# does not establish matching .NET/API/AOT behavior.
For Unreal, reusing .NET binaries would require a separately qualified interop
strategy; shared schemas/behavioral contracts or reimplementation may be more
appropriate. Source reuse, data compatibility and runtime embedding are separate
claims requiring separate checks.

## Game reporting, audit and notifications

Reuse the framework Log/Audit/Notification and UI Notification capabilities. Define
durable events for relevant actions such as save/recovery, account/permission,
purchases/rewards and administrative operations. Use bounded/sampled diagnostic
telemetry for high-frequency state where appropriate; auditing coverage does not
mean serializing the entire world or writing durable logs for every frame/entity.

Keep blocking storage/network/email work out of frame-sensitive paths; design queues,
backpressure and required audit consistency explicitly. Adapt UI notifications to
the engine thread/lifecycle and player/session scope. Never swallow exceptions,
fake save/network success or emit secret/player-sensitive payloads.

## Branch identity, conflict and evidence rules

Game nodes use IDs such as G02.godot.csharp.timing and bind to the owning L-layer
decision. Engine, networking or target changes mark affected answers needs_review
without losing the game concept/history. Game group roots participate in the same
registry, dependency, provenance and future migration validation as other profiles.

Current Godot C# documentation states that web export is unavailable. A browser
target plus that profile must raise a compatibility conflict until applicable
official release evidence establishes otherwise; do not offer a fabricated export
or silently change the user's language.
[Godot C# platform guidance](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/index.html)

This phase supplies design only. Engine builds, exported games, playtests,
networking, devices and store/vendor acceptance remain unrun.
