# Godot C#/.NET game tree

Status: design blueprint. Profile: `godot.csharp.game`; GDScript and native-extension
profiles are separate choices. Preferred starting profile for this owner, subject
to actual project scope, targets and existing pins.
Uses [game-domain groups](../GAMES.md) and [the shared tree model](../TREE_MODEL.md).

## Entry branches

```text
Godot game
  Existing project / new
  Language: C#/.NET (this profile)
  Engine editor/build and .NET/toolchain constraints
  2D / 3D / mixed
  Real-time / turn-based / hybrid; local / online
  Selected target + renderer + export requirements
  L01-L08 roots and applicable G01-G09 game trees
```

Godot's C# path requires its .NET-enabled editor. The current C# documentation
excludes web export and identifies target-specific mobile limitations. The wizard
must check the exact selected engine release, runtime and export templates rather
than assume every Godot language/target combination works.
[Official C# guidance](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/index.html)

## Existing framework layer roots

| Layer | Godot-specific branches and required output |
| --- | --- |
| L01 | Genre/core loop, 2D/3D and target audience → first playable → selected target/device scope |
| L02 | Existing Godot/.NET pins → scene/node and C# module boundaries → engine-native rules or optional portable simulation core → actual target compatibility |
| L03 | Input/action and player/camera choices → engine UI/HUD/menu structure → localization/accessibility → safe UI notification adapter |
| L04 | Content definitions/resources, authoritative game state and identifiers → local saves/settings/replay → migration/recovery → remote persistence only when required |
| L05 | Offline/online identities and authority → untrusted saves/mods/network inputs → device/credential boundaries and applicable permissions |
| L06 | Scene/node lifecycle and requested device/network services → shared reporting/audit/notification adapters → nonblocking delivery and truthful outcomes |
| L07 | Renderer/export choices per target → selected editor/.NET/export-template prerequisites → packaging/signing/distribution → runtime diagnostics/recovery |
| L08 | Existing project artifacts and actual .NET/engine commands → headless/domain checks plus editor/exported-game/playtest/device gates → scoped delivery evidence |

## Godot-specific game branches

| Game groups | Decision tree and checks |
| --- | --- |
| G01/G05 | Choose only required mechanics → reusable scenes/modules and data-driven rules → first meaningful player loop and bounded feature slices |
| G02 | Frame processing versus fixed physics processing → one authoritative simulation/tick owner → pause/time scaling and adapter update contract → test no duplicate steps or frame-rate-dependent rules |
| G03 | Scene/node composition, reusable child scenes, signal/dependency boundaries → world/level loading and entity lifetime → check missing references, unload/dispose and repeated spawning |
| G04 | Actual input action map/devices → player/control/camera and UI capture → remapping/focus/controller/touch checks where selected |
| G06 | Chosen renderer and target budgets → art/audio/animation/import/reference workflow → UI notifications dispatched within engine lifetime/thread constraints |
| G07 | Native content versus portable save schema → stable IDs/versioned state → safe write/migration/recovery → optional replay with explicit tick/seed assumptions |
| G08 | None/local/online → engine/project network contract and authority → separate backend/headless-host profile if needed → loss/replay/reconnect/exploit cases |
| G09 | Actual Godot/C# build/export prerequisites → profiled frame/tick/memory/loading budgets → playtests and independently verified target exports |

Godot documents distinct frame and physics callbacks; the tree must not treat
render cadence as authoritative simulation time by accident.
[Processing guidance](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
Reusable scene boundaries should preserve existing nodes/contracts and avoid
unnecessary environmental coupling.
[Scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html)

## Optional shared .NET core

If cross-engine reuse is requested, keep simulation/rules and portable state free
of Godot node/vector/resource dependencies where appropriate. The Godot adapter owns
engine object mapping, input, rendering, timing and UI; it must not run a second
simulation step when another owner already advanced it. Validate the actual
runtime/API surface and serialization rules before claiming reuse.

This is optional architecture, not an instruction to replace a working Godot
game with a universal engine framework. Existing shared code and plans take priority.

## Invalidation and evidence

Changing engine version/language, renderer, target or multiplayer topology flags
affected module, asset, update, networking and export decisions needs_review.
C# plus browser export is a conflict under the inspected guidance; preserve both
user requirements and ask the consequential choice rather than fake an export.

Reviewed 2026-10-19 using the official references above. No engine/runtime version
was selected; no game, adapter, build/export, determinism, physics, playtest,
network/device or storefront result was executed or qualified by this design.
