# P9: Game development layers and engine-specific trees

Date: 2026-10-19. Owner: repository owner; author/reviewer: assistant, self-review.
Scope: develop game-domain layers and engine tree designs for the existing wizard.
Status: proposed design; no game, engine plugin, wizard runtime or adapter implemented.
Authorization: extend layer design for games, prioritizing the owner's Godot/C#/.NET
workflow while allowing Unity, Unreal and additional engines. Work directly on master.

## Outcome and scope

A game cannot be configured adequately through website-oriented choices alone.
Add a [game domain extension](wizard/GAMES.md) over the existing L01-L08 framework.
Its G01-G09 trees ask game-specific questions while preserving existing decisions,
security/reporting requirements, traceability and delivery authorization.

Engine profiles implement different decision branches:
[Godot/C#](wizard/games/GODOT.md), [Unity/C#](wizard/games/UNITY.md),
[Unreal C++/Blueprints](wizard/games/UNREAL.md) and
[custom .NET game/simulation hosts](wizard/games/CUSTOM_DOTNET.md).
Other engines are explicit inventory entries until their trees and evidence exist.

The owner's preferred starting choice is Godot/C#; preference is a suggested answer,
not a global mandate. New or existing project scope and selected targets remain
authoritative. No Godot project or external application repository is modified here.

## Domain groups and ownership

| Group | Game questions | Existing owning layers |
| --- | --- | --- |
| G01 | Concept, genre, core loop, player experience and first playable slice | L01/L08 |
| G02 | Time, simulation, physics, rules and determinism requirements | L02/L04 |
| G03 | World, entities, scenes/levels, loading and procedural content | L02/L04/L06 |
| G04 | Input, player control, cameras and interaction accessibility | L03/L05 |
| G05 | Gameplay features, AI, progression, economy and balancing | L01/L02/L04 |
| G06 | Rendering, art/assets, animation, audio, HUD and content pipeline | L03/L04/L06 |
| G07 | Saves, settings, content definitions, replay and recovery | L04/L05/L06 |
| G08 | Multiplayer/session topology, authority and online services | L02/L05/L06/L07 |
| G09 | Runtime budgets, playtesting, automated checks and distribution | L07/L08 |

Groups are conditional branches, not nine compulsory service modules. A puzzle
prototype need not acquire multiplayer, a complex AI framework or a database.
Game-specific questions refine the owner's L-layer decisions; they do not create
conflicting copies or another governance workflow.

## Acceptance criteria and design verification

| ID | Criterion | Design evidence | Runtime acceptance |
| --- | --- | --- | --- |
| GAME-001 | Explicit game-domain questions beyond ordinary app setup | G01-G09 with branches, outputs and checks | Not run |
| GAME-002 | Different engines receive their own trees | Godot, Unity, Unreal and custom .NET blueprints | No resolver implemented |
| GAME-003 | Godot/C# preference is supported without forcing every game into C# | Suggested profile and engine/language choices | No host behavior tested |
| GAME-004 | Reuse/portability preserves active contracts and engine boundaries | Optional shared-core/adapter design and interoperability limits | No cross-engine compatibility proven |
| GAME-005 | Export/platform restrictions affect selection rather than being hidden | Godot target conflict rule; all profiles retain version/target checks | No engine builds/exports |
| GAME-006 | Logging/audit/notification rules fit frame-sensitive applications | Event classification, no per-frame durable I/O requirement, safe engine-thread UI adapters | No game telemetry benchmark |
| GAME-007 | Quality includes playability and measured runtime acceptance | First playable/vertical slice, playtests, frame/memory/load/network budgets | Not run |
| GAME-008 | Engine/asset/package provenance and source/version checks are visible | Engine-specific reference needs and source register | No blanket support/licensing claim |

## Delivery sequence

| Slice | Deliverable | Status |
| --- | --- | --- |
| P9.D | Domain groups, engine profiles, framework integration and target constraints | Design prepared |
| P9.1 | Machine-readable game group/profile definitions and dependency validation | Not implemented; depends on P8 tree/schema work |
| P9.2 | Godot/C# conversational configuration and scoped artifact preview | Not implemented |
| P9.3 | First runnable game slice selected by the owner, with actual engine evidence | Not implemented; a real game scope is required |
| P9.4 | Unity/Unreal/custom profile execution and compatibility checks | Not implemented |
| P9.5 | Profile maintenance, engine/platform version evidence and adversarial/behavior scenarios | Not run |

Future implementation should start with one playable outcome: boot, chosen player
interaction, a small test world, one meaningful mechanic and safe failure/reporting.
Add save/recovery, assets and online features only as the selected design requires.
No engine, SDK, asset pack, service subscription or plugin is installed by this phase.

## Risks, compatibility and verification limits

Engine-native object lifetime, threading, serialization, physics and platform
exports differ. Do not promise that a C# library or saved world transfers unchanged.
A fixed tick alone does not prove deterministic cross-platform simulation.
The .NET runtime/API surface supported by an engine is not necessarily the newest
desktop .NET SDK. Unreal's native C++/Blueprints path does not imply C# support.

Run the repository's existing structure/link, adapter parity, regression and diff
checks. They validate design integration and existing tools only. Record actual
engine builds, exports, playtests, devices, networking and stores as unrun until
they occur; reference documents and headless tests cannot substitute for them.

Local verification on 2026-10-19: structure/link validation, adapter parity, all
47 existing regression tests and diff checks passed. This is documentation and
manifest integration evidence only. Review was self-review; no new engine-level
tests were fabricated to count prose or imply that game functionality ran.
