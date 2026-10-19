# Unity C# game tree

Status: design blueprint. Profile: `unity.csharp.game`.
Uses [game-domain groups](../GAMES.md) and [the shared tree model](../TREE_MODEL.md).
No Unity installation, project conversion or engine package is performed here.

## Entry branches

```text
Unity game
  Existing project / new
  Selected editor/runtime and actual project package constraints
  2D / 3D / mixed; actual rendering/content approach
  Engine object/component model and justified optional extensions
  Single-player / local multiplayer / online
  Per-target scripting/build backend, export and distribution requirements
  L01-L08 roots and applicable G01-G09 trees
```

Unity's [gameplay programming guidance](https://docs.unity3d.com/Manual/scripting.html)
and [prefab model](https://docs.unity3d.com/Manual/Prefabs.html) supply engine-specific
concepts. Do not substitute Godot node/scene questions or assume the editor uses
the same runtime/API surface as a standalone modern .NET application.

## Existing framework layer roots

| Layer | Unity-specific branches and required output |
| --- | --- |
| L01 | Genre/core loop/2D/3D/targets → selected player experience and first playable |
| L02 | Existing editor/package/runtime pins → C# object/component and module boundaries → optional shared-core or data-oriented choices only when justified |
| L03 | Input/player/camera and selected UI/HUD/menu approach → state/lifecycle/localization/accessibility → UI notification adapter |
| L04 | Asset/content and scene references versus game/save data → state authority/IDs → settings/save/migration/recovery → online state only if required |
| L05 | Local/online identities and authority → untrusted content/network commands → credentials/platform services and privacy |
| L06 | Existing shared Log/Audit/Notification capabilities → engine-thread UI adapter → requested device, multiplayer and external-service integrations |
| L07 | Actual renderer/packages/build backend and target SDK requirements → export/signing/store route → runtime/crash/update/operational ownership |
| L08 | Existing C#/engine tests and build automation → editor and exported-player checks → target performance/playtest/device/network gates and evidence |

## Unity-specific game branches

| Game groups | Decision tree and checks |
| --- | --- |
| G01/G05 | Required mechanics → existing project systems/components → playable slice → balancing assumptions and actual player feedback |
| G02 | Frame/fixed update ownership and scheduling → pause/time scaling → physics integration and portable-core stepping → no duplicate or rate-dependent simulation |
| G03 | Scenes, object/component ownership and prefabs → spawn/pool/load/unload policy → check reference/lifetime/persisted-state behavior |
| G04 | Selected input/device mapping → player/camera/UI capture → target-specific controls and reconnect/focus behavior |
| G06 | Actual rendering pipeline/target fit → assets/animation/audio/VFX/UI and import/reference settings → missing-asset/export integrity and measured budgets |
| G07 | Engine content references versus versioned game save schema → stable IDs/migration/recovery → replay only with declared timing/randomness contracts |
| G08 | None/local/online → selected networking package/service and authority model → session/replication/replay/reconnect checks; no vendor automatically chosen |
| G09 | Actual engine/player build tools → scripting backend/AOT/platform restrictions → profiled runtime and independent exported-player/distribution acceptance |

Unity documents target/backend-specific scripting restrictions, including AOT
limitations. A successful desktop/editor build does not establish an exported
player's behavior.
[Official scripting restrictions](https://docs.unity3d.com/Manual/scripting-restrictions.html)

## Shared C# core and engine boundaries

When reuse is needed, keep portable rules/state separate from engine object,
renderer/input/physics and serialization lifetimes. Match the core's actual
target/API/dependency surface to the selected Unity version/backend. Reflection,
dynamic code, threads and serialization may need target-specific checks; neither
a common language nor an engine-neutral design proves compatibility.

Use existing components/contracts and test strategies. Do not impose a new ECS,
dependency container, asset delivery package or network service on every game.

## Invalidation and evidence

Changes to editor/packages/rendering/backend/target reopen affected assets, APIs,
builds and runtime checks. Network/save changes propagate to authority, schema and
failure-path acceptance. Preserve user work and active project plans.

Reviewed 2026-10-19 using the official references above. Exact editor/runtime,
target support, package/provider compatibility, licensing/distribution terms,
engine builds and all gameplay/device/network acceptance remain unverified.
