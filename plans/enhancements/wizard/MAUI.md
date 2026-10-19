# .NET MAUI technology tree blueprint

Status: design blueprint; no runnable wizard profile or platform qualification.
Profiles: retain `dotnet.maui.mobile`; add `dotnet.maui.desktop`. A project targeting
both composes their platform branches and shares appropriate decisions. Both use
this blueprint and [the common tree contract](TREE_MODEL.md), rather than copies
of the framework rules. Catalog: [technology trees](TREE_CATALOG.md).

## Entry tree and UI variants

```text
Application
  .NET MAUI
    Targets (select individually)
      Mobile: Android / iOS
      Desktop: Windows / macOS via Mac Catalyst
      Additional target: explicit provider-specific verification required
    UI variant
      Native MAUI controls: XAML and/or C#
      MAUI Blazor Hybrid: Razor components in BlazorWebView
    For each selected target + UI variant
      Resolve the eight layer roots below
```

Microsoft documents MAUI for native mobile and desktop applications. Its platform
requirements vary with release and UI variant; inspect the selected release's
SDK/workload/toolchain requirements before declaring a target supported. Additional
Tizen support is supplied by Samsung and needs its own qualification. A requested
Linux, TV or other target must remain explicit and unverified until the appropriate
provider/target evidence exists. [Microsoft platform guidance](https://learn.microsoft.com/en-us/dotnet/maui/supported-platforms?view=net-maui-10.0)

In the Hybrid branch, Razor components execute natively and render in an embedded
WebView. It is distinct from browser WebAssembly and a server-rendered Blazor
website. A separate browser deliverable selects its own website profile and may
reuse suitable components/contracts. [Microsoft Hybrid guidance](https://learn.microsoft.com/en-us/aspnet/core/blazor/hybrid/?view=aspnetcore-10.0)

## Eight layer trees

Each row inherits shared intent, reporting/security obligations and answer
provenance from [the layer contract](LAYER_CONTRACT.md). Proposed root identity is
`Lxx.<profile>.<decision>` scoped by deliverable, platform and UI variant.

| Layer | Nested MAUI-specific decisions | Required output and review/check |
| --- | --- | --- |
| L01 Project | New/existing app → mobile, desktop or combined → individual OS/device targets → business flows, connectivity and distribution | Target matrix and MVP scope; no single-platform result certifies other targets |
| L02 Technology | Existing pins/workloads → selected .NET/MAUI/toolchain → native controls or Blazor Hybrid → shared modules/platform adapters → backend API if required | Version/toolchain constraints, UI variant and module map; unknown compatibility remains unverified |
| L03 Interface | Native branch → pages/windows, navigation, binding/state and existing view-model conventions; Hybrid branch → Razor components, WebView/native boundary and shared UI; both → input, localization/RTL, accessibility, lifecycle and UI notifications | Actual target/variant interaction flows; device/window/navigation and truthful failure/cancellation acceptance |
| L04 Data | No retained data, local data, remote API or mixed → approved store/adapter → offline authority/cache → sync/conflict/idempotency → migrations/recovery | Data ownership and offline/sync contract; test interrupted writes, duplicate sync, upgrade and recovery as applicable |
| L05 Security | OS/device boundary → identity/callback/session needs → server-side API permission authority → local credentials/sensitive data → platform permissions and tenant/session cleanup | Secret references and per-target permission/access checks; local UI visibility never authorizes backend access |
| L06 Integrations | Existing Log/Audit/Notification Services → shared UI Notification Service with native/Hybrid adapters → requested device capabilities → local versus push notifications → permitted lifecycle/background behavior | Event and recipient coverage, safe UI dispatch and delivery policy; notification failures and offline queues cannot imply success |
| L07 Operations | Per-target SDK/build host/workload → package/signing/distribution → environment/config/API endpoints → diagnostics/update/recovery ownership | Independent target build/distribution matrix with owners, hardware/account gaps and actual runtime evidence |
| L08 Delivery | Plan/starter/slice → existing artifacts/CI → shared-unit and target-specific UI/integration checks → packaging/signing/device/store gates → evidence/handoff | Phased plan and actual results by platform/variant; preserve user Git workflow and label unrun gates |

## Platform and variant follow-up trees

| Branch | Questions to collect | Evidence needed before acceptance |
| --- | --- | --- |
| Android | Device/form factor and OS requirements; SDK/workload compatibility; requested permissions/device features; package/distribution; suspend/resume/offline behavior | Selected release/toolchain requirements; emulator and physical-device scope; signing/distribution only when applicable |
| iOS | Device/OS requirements; compatible Apple build environment; entitlements/callbacks; signing/provisioning; device/store route | Available Mac/build toolchain, relevant hardware/account/signing evidence and scoped device checks |
| Windows | OS/runtime requirements; window/navigation/input behavior; packaged/unpackaged decision if supported by the selected toolchain; install/update route | Actual target build/runtime and installer/update evidence; avoid inferring desktop acceptance from Android |
| macOS / Mac Catalyst | Supported OS/toolchain; Mac build availability; window/input adaptation; entitlements/signing/distribution | Actual selected Mac Catalyst build/runtime and required signing/distribution checks |
| Blazor Hybrid | WebView requirements; shared Razor component assumptions; native service/resource access; navigation/dispatch lifetime; authentication boundary | Selected target WebView compatibility and native/Hybrid interaction checks; browser-only tests are insufficient |
| Additional/provider targets | Provider, tooling, device, supported variant and distribution route | Official provider evidence plus target-specific acceptance; no automatic support claim |

The questions above are design requirements, not a claim that every capability or
distribution route is available on every target. Platform-dependent background
execution, push notifications and device APIs need explicit compatibility checks.
Do not request every permission or introduce a backend/push vendor by default.

## Dependencies and invalidation

- Changing native controls to Hybrid revisits L02/L03 UI structure, L05 trust and
  callback handling, L06 UI adapter lifetime, L07 WebView prerequisites and L08 tests.
- Adding a target reopens its SDK, permissions, package, UI and device gates without
  discarding previously verified targets or silently claiming cross-platform parity.
- Enabling offline operation revisits L04 synchronization/authority, L05 local data,
  L06 deferred delivery and L08 disconnection/replay/recovery tests.
- Adding a separate API creates an explicit backend profile/contract. Backend
  database credentials do not become mobile/desktop application configuration.

## Shared framework integration

Reuse existing app services, view models, component libraries, stores and active
plans. Log/Audit/Notification and UI Notification implementation follows
the [operational standard](../../../core/LOGGING_AUDIT_NOTIFICATIONS.md); this
profile selects suitable adapters, not a second policy. Apply the
[assurance standard](../../../core/QUALITY_SECURITY_RELIABILITY.md) to configuration,
access, retry/cancellation, restore, dependencies and operational checks.

## Reference and verification status

Reviewed 2026-10-19: [MAUI overview](https://learn.microsoft.com/en-us/dotnet/maui/what-is-maui?view=net-maui-10.0),
[supported platforms](https://learn.microsoft.com/en-us/dotnet/maui/supported-platforms?view=net-maui-10.0)
and [Blazor Hybrid](https://learn.microsoft.com/en-us/aspnet/core/blazor/hybrid/?view=aspnetcore-10.0).
These establish framework concepts and separate platform/variant requirements;
no current project version, minimum OS or compatible SDK set is selected here.
SDK/workload pins, target support, device behavior, signing/store acceptance and
actual native/Hybrid wizard execution remain unverified. A Mac is required for
Apple-target builds as described in the MAUI overview; unavailable prerequisites
are recorded as missing gates rather than simulated passes.
