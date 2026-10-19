# Godot GDScript game tree

Status: design blueprint. Profile: `godot.gdscript.game`.
Uses [game groups](../GAMES.md), [the shared tree model](../TREE_MODEL.md) and
[the Godot engine concepts](GODOT.md). It is a separate language/export tree,
not an alias that silently inherits C# runtime restrictions or .NET assumptions.

## Entry branches

```text
Godot game
  Existing project / new
  Language: GDScript
    Existing typing/warnings conventions or explicit proposed conventions
  Engine version and actual project/addon constraints
  2D / 3D / mixed; renderer
  Real-time / turn-based / hybrid; local / online
  Targets and export templates
    Desktop / mobile / browser / other explicitly qualified targets
  Existing L01-L08 + selected G01-G09 branches
```

The [GDScript reference](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)
is the language source. Inspect the project's actual release and code conventions;
do not introduce a .NET project or replace active scripts merely to match the
owner's usual C# preference. Mixed-language projects require explicit interop and
target checks rather than an assumed portable .NET core.

## Eight layer roots

| Layer | GDScript-specific branches and output |
| --- | --- |
| L01 | Genre/core loop, 2D/3D, selected targets and first playable; preserve existing game scope |
| L02 | Godot version/renderer/export templates → GDScript scripts/typing/warnings/addons → node/scene and optional reusable-rule boundaries |
| L03 | Input/actions/player/camera → engine UI/HUD/menu/state → localization/accessibility and safe UI Notification Service adapter |
| L04 | Game/content/resource IDs and authoritative state → native/portable save schema, settings, migrations and recovery; online persistence only when needed |
| L05 | Local/online authority → untrusted saves/mods/network input → target permissions, secrets and player/account privacy |
| L06 | Scene/script lifetimes, signals and requested platform/network services → shared Log/Audit/Notification adapters and nonblocking safe UI feedback |
| L07 | Actual renderer/template/target prerequisites → native packages or browser hosting → selected Apple/Google/Steam publishing profile and release artifact evidence |
| L08 | Actual engine/script checks and selected test tools → editor plus exported-game/playtest/device/browser checks → publishing readiness and scoped evidence |

## Game-domain specialization and browser branch

G01/G05 select only the intended loop and mechanics. G02 separates frame versus
physics/tick ownership, pause and seed/order requirements. G03/G04 define reusable
scene/node/signal, lifecycle, input/camera and UI-capture boundaries. G06 owns the
selected renderer, art/audio/animation/HUD and asset import/reference workflow.
G07 defines saves/content/replay with real recovery checks. G08 selects local or
online authority/networking. G09 requires measured runtime and exported-target
playability, not merely an error-free editor.

For browser export, use [Godot's web export guidance](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html):
verify the actual renderer/browser requirements, export files and serving setup.
The inspected guidance uses WebGL 2.0 with Compatibility rendering; multi-threaded
export adds browser isolation/header constraints. Choose single/multi-thread
behavior deliberately, and test browser input, audio, storage, loading and failure
paths. GDScript selection is not itself proof that the requested renderer/addons
or browser features are compatible. Browser hosting is not an App Store listing.

Native mobile/desktop exports retain their engine/SDK/native-library, signing,
device and selected-store requirements. Apply the canonical
[publishing policy](../../../../core/PUBLISHING_REQUIREMENTS.md); using GDScript
does not exempt an Android engine binary from native-library checks or an Apple
archive from submission requirements.

## Invalidation and evidence

Changing C# to GDScript reopens code/package/interop, export, serialization and
testing decisions; it does not authorize an automatic rewrite. Changing target,
renderer/addons or thread mode reopens affected runtime/hosting/publishing checks.
Keep the owner's selected language and any incompatibilities visible.

Reviewed 2026-10-19 using the official references above. No engine version, addon,
typing rule, browser/SDK combination, build/export, playtest, interop or store
acceptance was selected or executed. The tree is design-only until a wizard
runtime and actual project/target acceptance evidence are delivered.
