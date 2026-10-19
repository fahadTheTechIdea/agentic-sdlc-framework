# Custom .NET game or simulation host tree

Status: design blueprint. Profile: `custom.dotnet.game`.
Uses [game-domain groups](../GAMES.md) and [the shared tree model](../TREE_MODEL.md).
This profile does not mean writing a new engine for every game.

## Entry branches

```text
Custom/reused .NET game or simulation
  Existing core/engine/framework / explicitly requested new host
  Headless simulation / interactive client / both
  Chosen host/rendering/input/audio libraries and target requirements
  Portable rules/state boundary and platform adapters, where useful
  Selected G01-G09 and L01-L08 decisions
```

MonoGame/FNA, Stride and other named frameworks need dedicated future profiles and
official compatibility references. Listing them as possibilities does not claim
that this custom profile provides their complete trees or a working adapter.

## Existing framework layer roots

| Layer | Custom .NET branches and required output |
| --- | --- |
| L01 | Game/simulation purpose, core loop, targets and existing assets → first useful playable or headless scenario |
| L02 | Inspect current runtime/projects/contracts → selected host/library/toolchain → simulation versus platform boundaries and update ownership |
| L03 | Interactive input/render/camera/UI branch, or reasoned headless N/A → safe UI adapter only when UI exists |
| L04 | Domain/content/state/units/IDs → local save/settings/replay → schema, consistency and recovery; no database by default |
| L05 | Local/server command authority → untrusted inputs/content/save data → credential/privacy boundaries if applicable |
| L06 | Existing Log/Audit/Notification services → host/input/render/audio/device/network adapters → bounded dispatch and explicit failure handling |
| L07 | Actual .NET/runtime/native dependency and target requirements → executable/server/package distribution → measured operational ownership |
| L08 | Domain/headless invariants plus real host/render/input/build checks → playtest/export/device/network evidence appropriate to actual targets |

## Game-domain specialization

G01 defines the playable/simulation outcome and excludes unrequested engine work.
G02 defines a single tick owner, commands/state/events, units/randomness/pause
and required determinism; fixed update or pure .NET does not prove determinism.
G03 defines entity/component/world ownership and loading without importing engine
objects into portable contracts. G04/G06 select actual interaction/presentation/
asset adapters or record headless N/A branches with reasons.

G05 adds only chosen rules/mechanics/AI and data definitions. G07 defines stable
save/content identity, versions and recovery, with replay only when designed.
G08 defines authority/networking only if selected. G09 maps tests and measured
budgets to the real host/device; a headless suite cannot establish rendering,
input latency, exported packages or platform support.

## Reuse boundary and acceptance

Read the complete affected project subtree, active plans and shared contracts
before designing replacement models. Keep rendering/platform SDKs outside a
reusable simulation core when that is the intended architecture. Extend existing
state, entity, lifecycle, codec and host contracts rather than invent parallel APIs.

Each selected host adapter must prove build/runtime compatibility, lifecycle/tick
ownership, state/view conversion, resource lifetime and error/cancellation behavior.
Data and behavioral compatibility across hosts require explicit contract tests.
Cross-engine physics/rendering equivalence is never assumed.

## Reference and verification status

This is an architectural question tree, not a chosen framework/API/version.
Future selected libraries/runtimes need official version-specific references and
real target builds. No application repository, simulation core, renderer, native
dependency, determinism test or game host was inspected or changed by this phase.
