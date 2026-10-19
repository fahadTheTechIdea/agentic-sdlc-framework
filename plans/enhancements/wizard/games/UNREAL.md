# Unreal game tree: C++, Blueprints and mixed projects

Status: design blueprint. Profile: `unreal.cpp-blueprint.game`.
Uses [game-domain groups](../GAMES.md) and [the shared tree model](../TREE_MODEL.md).
C#/.NET is not assumed to be a built-in gameplay path.

## Entry branches

```text
Unreal game
  Existing project / new
  Native C++ / Blueprints / mixed
  Actual engine version, modules/plugins and toolchain constraints
  Game concept/perspective/world and target requirements
  Single-player / local multiplayer / online authority model
  L01-L08 roots and applicable G01-G09 trees
```

Epic documents native [C++ gameplay programming](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)
and [Blueprint visual scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprints-visual-scripting-in-unreal-engine).
The tree asks which responsibilities belong in each. A C# bridge, embedded runtime
or external simulation service is an additional integration decision requiring
its own maintenance, target, licensing, lifetime and packaging evidence.

## Existing framework layer roots

| Layer | Unreal-specific branches and required output |
| --- | --- |
| L01 | Genre/core loop/perspective/world/targets → intended player experience and first playable |
| L02 | Actual engine/toolchain/modules/plugins → C++/Blueprint ownership → gameplay framework and optional shared-core/interop boundaries |
| L03 | Player input/controllers/cameras and chosen UI/HUD/menu approach → lifecycle/localization/accessibility → safe UI notifications |
| L04 | Engine content versus authoritative gameplay/save state → stable identity, configuration, migration/recovery and persistence needs |
| L05 | Client/server/session authority → validation of commands and untrusted saves/mods → credentials/platform identities/privacy |
| L06 | Engine logging/reporting and shared Audit/Notification contracts → UI-thread/lifetime adapters → requested networking/platform/external services |
| L07 | Selected engine/target prerequisites → content cooking/build/package/distribution → optional dedicated server/backend → runtime budgets and recovery ownership |
| L08 | Actual code/Blueprint/engine automation and build checks → packaged-game/playtest/performance/device/network gates → scoped evidence and handoff |

## Unreal-specific game branches

| Game groups | Decision tree and checks |
| --- | --- |
| G01/G05 | Selected mechanics → existing gameplay systems and C++/Blueprint responsibilities → small playable feature and balance/playtest criteria |
| G02 | Engine tick/physics and simulation authority → scheduling/pause/state ownership → optional external-core synchronization → no implied deterministic physics |
| G03 | Actors/components, world/levels and gameplay framework ownership → spawning/loading/lifetime → preserve references and state across transitions |
| G04 | Player/controller/pawn/input/camera responsibilities → UI versus gameplay capture → actual device/perspective control cases |
| G06 | Selected renderer/target budget → art/material/animation/audio/VFX/UI and asset-import pipeline → content dependency and packaged-game checks |
| G07 | Content references versus save/replay schema → ownership/identity/version changes → round-trip, interruption, corruption and migration recovery |
| G08 | None/local/online → authority/replication/session topology → server/client validation and requested online services → loss/replay/reconnect/load checks |
| G09 | Actual engine/target build and content packaging workflow → measured CPU/GPU/memory/load/network budgets → packaged runtime/playtest and distribution gates |

Epic's [gameplay framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine)
provides distinct game/player/controller/pawn/state concepts. Preserve their
intended responsibilities rather than translate a Godot or Unity hierarchy
mechanically. Modules/plugins and optional features need version-specific sources.

## Cross-engine and .NET interoperability

Sharing game requirements, API schemas, data formats and behavioral tests is
different from sharing executable code. A reusable C# simulation core does not
automatically run inside an Unreal packaged game. Choose and independently qualify
native reimplementation, interop/plugin embedding, a process/service boundary or
no runtime sharing according to actual constraints.

If an existing project already has an interop solution, inspect its contracts and
evidence first. Do not install a third-party C# plugin merely to make the wizard's
language selection succeed or claim unsupported console/mobile compatibility.

## Invalidation and evidence

C++/Blueprint boundary changes reopen state/lifetime/save/network ownership and
test coverage. Engine/plugin/target changes revisit compilation, content packaging
and runtime/interop constraints. UI notifications and reporting remain bounded,
safe and explicit through failures.

Reviewed 2026-10-19 using the official references above. No version, SDK, plugin,
renderer, native/.NET interoperability or platform/store certification was selected
or verified. No Unreal game/build/playtest/server was executed in this phase.
