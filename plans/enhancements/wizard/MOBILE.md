# Mobile application selection trees

Status: design map. Detailed blueprints are not runnable wizard profiles or proof
of SDK, device or store acceptance. Parent: [catalog](TREE_CATALOG.md).

## Start with targets, then choose the implementation approach

```text
Mobile application
  Target devices
    iOS / iPadOS
    Android: phone / tablet / foldable
    Both platform families
    Other form factor: dedicated extension and qualification required
  Implementation approach
    Native per platform
      iOS: Swift → SwiftUI / UIKit / mixed
      Android: Kotlin → Compose / Views / mixed
               Existing Java → Views / deliberate Kotlin interop
    Shared cross-platform application
      .NET MAUI → native controls / Blazor Hybrid
      Flutter → its own widget/platform trees
      React Native → its own framework/native integration trees
    Other sharing or hybrid approach
      Kotlin Multiplatform → profile detail pending
      Web-based native container (such as Capacitor) → profile detail pending
    Browser/PWA
      Separate web profile and browser capability/distribution checks
```

Targets and frameworks are separate decisions. iOS and Android can each be served
by native or cross-platform implementations. Selecting both does not automatically
select MAUI, Flutter or React Native; selecting a shared stack does not certify
both platforms. Each selected target keeps its own build/runtime/distribution gates.

## Coverage map

| Choice | Detailed design | Current status |
| --- | --- | --- |
| Native iOS/iPadOS with SwiftUI, UIKit or mixed UI | [iOS tree](IOS.md) | Eight-layer blueprint |
| Native Android with Kotlin/Java and Compose/Views branches | [Android tree](ANDROID.md) | Eight-layer blueprint |
| .NET MAUI mobile, optionally shared with desktop | [MAUI tree](MAUI.md) | Eight-layer native-controls/Hybrid blueprint |
| Flutter mobile | [Flutter blueprint](TREE_CATALOG.md#blueprint-dartfluttermobile) | Eight-layer starter blueprint |
| React Native mobile | [React Native tree](REACT_NATIVE.md) | Eight-layer blueprint |
| Kotlin Multiplatform or web-based native container | Inventory in the catalog | Detailed layer trees pending |
| Browser/PWA | Web family plus a future PWA capability profile | PWA-specific tree pending |
| TV, watches, automotive or other specialized targets | Separate form-factor/profile extension | Detailed trees and provider qualification pending |

This is explicit coverage, not an exhaustive list of mobile technologies. New
profiles follow [the tree contract](TREE_MODEL.md); unknown combinations remain
unverified rather than inheriting unrelated website or phone-only questions.

## Common controls and per-platform ownership

The existing layer contract and Log/Audit/Notification/UI Notification obligations
remain canonical. Individual trees select implementation adapters, device/session
lifetimes, safe permissions, offline/sync behavior and platform acceptance checks.
Native iOS plus native Android may share API contracts and requirements while
retaining separate client profiles and native implementations.

Changing implementation approach reopens affected UI, data adapter, credential/
callback, device integration, build and test decisions. Preserve user intent and
history; no profile change authorizes rewriting an existing app or provisioning
accounts, certificates, signing keys, store releases or paid services.
