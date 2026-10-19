# Native iOS/iPadOS tree blueprint

Status: design only. Profile: `swift.ios.mobile`; UIKit/SwiftUI are UI variants.
Existing Objective-C integration is an explicit interoperability constraint, not
authority to rewrite existing code. Uses [the mobile selector](MOBILE.md) and
[tree contract](TREE_MODEL.md).

## Native entry tree

```text
Native Apple mobile app
  Targets: iPhone / iPad / both
  Existing application or new
    Swift codebase, with any existing Objective-C interoperability recorded
  UI variant
    SwiftUI
    UIKit
    Mixed / incremental integration
  For each target + supported OS/toolchain combination
    Resolve L01-L08 below
```

Apple documents SwiftUI alongside UIKit and supports incremental integration.
The wizard must preserve an existing UI approach rather than force migration.
[Apple SwiftUI guidance](https://developer.apple.com/swiftui/)

## Eight layer roots and follow-up branches

| Layer | Native iOS decisions | Output and acceptance needs |
| --- | --- | --- |
| L01 Project | iPhone/iPad targets → workflows and connectivity → new/existing app → distribution intent | Device/workflow scope; other Apple platforms require separate profiles |
| L02 Technology | Existing Swift/toolchain/dependency pins → SwiftUI, UIKit or mixed → module/shared-contract boundaries → optional backend profile | Native stack and UI variant; verify actual Xcode/SDK/dependency compatibility |
| L03 Interface | SwiftUI branch → view/state/navigation choices; UIKit branch → view-controller/navigation and existing resources; mixed → interoperability ownership; all → lifecycle, layout, accessibility, localization, UI feedback | Target-specific flows, state restoration and safe UI Notification Service behavior |
| L04 Data | Caller/API/local data → selected native/existing persistence adapter → offline authority/cache → synchronization, cancellation, conflict, migration and recovery | Data contract and meaningful offline/upgrade/recovery checks; no store chosen merely from language |
| L05 Security | Identity source → session/callback boundaries → server authorization → local sensitive data/credential handling → requested permissions/entitlements and tenant cleanup | Protected operations, minimum device privileges and denied/expired/session-isolation cases |
| L06 Integrations | Reused Log/Audit/Notification services → native UI adapter → requested device capabilities → local/push/deferred delivery and allowed background behavior | Event/recipient coverage and safe dispatch; test delivery failures, duplicates and cancelled work |
| L07 Operations | Selected Apple build environment → app identity/environments → signing/provisioning/distribution → diagnostics/update/recovery → account/hardware owners | Independent build, install, signing and distribution evidence; missing prerequisites are visible gates |
| L08 Delivery | Requested plan/starter/slice → existing CI/artifacts → actual selected unit/UI/integration tools → simulator/device/distribution gates | Evidence per target/UI variant; no simulator result implies all hardware or App Store acceptance |

The layers define questions and checks, not availability guarantees for every
device feature or distribution route. Investigate selected capabilities and OS
versions before proposing exact implementation APIs.

## Conditional questions and invalidation

- Selecting iPad adds its layout/window/input acceptance needs without assuming
  that a passing iPhone flow proves them.
- Switching SwiftUI/UIKit revisits navigation, view state/lifetime, interoperability,
  UI notifications and UI tests; retain shared business/API contracts.
- Requested camera/location/push/background work opens only the needed permission,
  entitlement, service and failure branches. Never request all device permissions.
- Offline data or multiple accounts/tenants reopens local data protection,
  synchronization, sign-out cleanup and recipient isolation.
- A separate backend remains independently profiled; server credentials never
  become bundled client configuration.

## Reference and verification status

Reviewed 2026-10-19: [SwiftUI](https://developer.apple.com/swiftui/),
[iOS development](https://developer.apple.com/ios/) and
[Xcode system requirements](https://developer.apple.com/xcode/system-requirements).
Apple documentation references guide UI/toolchain branches; no Xcode/Swift/SDK
version or minimum OS was selected. Compatible build environment, actual devices,
signing/accounts and store acceptance remain unverified. No app was generated.
