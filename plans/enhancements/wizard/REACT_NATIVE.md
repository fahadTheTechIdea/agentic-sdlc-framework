# React Native mobile tree blueprint

Status: design only. Profile: `typescript.react-native.mobile`, with the actual
language, application framework/workflow and native integration ownership recorded.
Uses [the mobile selector](MOBILE.md) and [tree contract](TREE_MODEL.md).

## Entry tree

```text
Shared React Native app
  Targets: iOS / Android / both
  Existing app and actual package/native configuration, or new project
  Application framework/workflow and native project ownership
  Shared React Native UI
    Required native integrations and platform-specific adaptations
  For each selected target
    Resolve L01-L08 and that platform's build/distribution checks
```

React Native uses React concepts for native application development. Its profile
is separate from a React browser website; browser packages and deployment assumptions
must be checked before reuse. [Official introduction](https://reactnative.dev/docs/getting-started)

## Eight layer roots and follow-up branches

| Layer | React Native decisions | Output and acceptance needs |
| --- | --- | --- |
| L01 Project | iOS/Android target matrix → workflows/connectivity → new/existing app → distribution | Distinct platform acceptance even when the client source is shared |
| L02 Technology | Actual React Native/language/package pins → application framework/workflow → native code/module ownership → shared versus platform modules | Package/native-toolchain compatibility and explicit ownership; no automatic workflow migration |
| L03 Interface | Native component/navigation/state/form choices → target adaptations/lifecycle → accessibility/localization → safe UI notifications | Per-platform interaction and lifecycle scenarios; no website render-mode questions |
| L04 Data | API/local state/storage → approved native adapters → offline cache/sync/conflict → migration/recovery | Data authority and meaningful replay/offline/upgrade checks |
| L05 Security | Identity/callback/session choices → server authorization → native credential adapters → permissions and tenant cleanup | Minimum privileges and resource/recipient/session isolation checks |
| L06 Integrations | Shared Log/Audit/Notification contracts → JS/native reporting boundaries and UI adapter → requested device/push/background capabilities | Native package/provider compatibility and truthful failure/cancellation/delivery outcomes |
| L07 Operations | Actual native build/distribution workflow → independent iOS and Android prerequisites → environment/config/signing/update/diagnostics | Platform-specific package, signing/account and device gates; optional external build services need explicit scope |
| L08 Delivery | Selected output → package/type/test and native checks → target UI/device/provider acceptance → handoff | Exact evidence and unrun gates; shared tests never certify both native targets |

## Conditional questions and invalidation

Changing native module dependencies or the application workflow revisits L02
compatibility, L05 privileges, L06 integrations and L07/L08 build/acceptance. New
platform targets preserve shared answers but open their own native toolchain,
permissions, signing and device checks. Offline/multi-account changes propagate
through data, credentials, recipient routing and tests.

Reuse existing project state, packages, native modules and reporting contracts.
Unknown package/runtime combinations remain unverified; no new native library,
build subscription or push provider is installed merely by selecting this profile.

## Reference and verification status

Reviewed 2026-10-19: [React Native introduction](https://reactnative.dev/docs/getting-started).
This is a design vocabulary/reference check, not compatibility qualification.
A real project must verify the chosen release, application workflow, native module
versions and platform toolchains against official version-specific references.
No iOS/Android build, native UI test, signing, account or store check was executed.
