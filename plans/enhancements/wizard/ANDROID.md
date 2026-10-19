# Native Android tree blueprint

Status: design only. Profiles: `kotlin.android.mobile` and `java.android.mobile`.
Both share this blueprint and [the mobile selector](MOBILE.md); choose language/UI
branches deliberately and preserve existing code. Uses [the tree contract](TREE_MODEL.md).

## Native entry tree

```text
Native Android app
  Targets: phone / tablet / foldable
  Existing application or new
    Kotlin
      Jetpack Compose / Android Views / mixed
    Existing Java
      Android Views / deliberate Kotlin interoperability for Compose
  SDK/toolchain and selected target constraints
    Resolve L01-L08 below
```

Google documents Compose as an Android UI toolkit, with its own state, layout,
navigation, lifecycle and testing concepts. Existing view-based applications also
need explicit view/interoperability branches.
[Compose documentation](https://developer.android.com/develop/ui/compose/documentation),
[Android Views](https://developer.android.com/develop/ui/views/layout/declaring-layout)

## Eight layer roots and follow-up branches

| Layer | Native Android decisions | Output and acceptance needs |
| --- | --- | --- |
| L01 Project | Phone/tablet/foldable targets → workflows/connectivity → new/existing app → distribution intent | Target/workflow matrix; TV, Wear and automotive extensions remain separate |
| L02 Technology | Existing Kotlin/Java pins → Compose, Views or mixed → actual Gradle/Android toolchain and dependencies → app/module boundaries | Selected stack/UI and compatibility constraints; no automatic Java-to-Kotlin rewrite |
| L03 Interface | Compose branch → composables/state/navigation; Views branch → layouts/view lifetimes/navigation; mixed → interoperability; all → adaptive layout, accessibility/localization, back behavior, lifecycle and UI notifications | Observable flows and state/lifecycle handling per form factor/UI variant |
| L04 Data | Existing data layer/contracts → selected persistence/network adapters → local/offline authority → sync, duplicate requests, migrations and recovery | Data lifecycle and provider checks; preserve active stores rather than introduce a second repository system |
| L05 Security | User/service identity → backend access policies → credential/session handling → device/runtime permissions and tenant cleanup | Minimum permissions, truthful denials and protected resource/session checks |
| L06 Integrations | Existing Log/Audit/Notification services → lifecycle-safe UI adapter → requested device APIs → local/push notifications and platform-permitted background jobs | Correlated coverage, safe recipients, delivery/cancellation/retry and process-lifetime behavior |
| L07 Operations | Selected SDK/build requirements → package/application identity/config → signing/distribution → crash/health/update/recovery ownership | Actual build/install and signing/distribution evidence per target and environment |
| L08 Delivery | Plan/starter/slice → existing CI/artifacts → selected local/instrumented/UI/provider checks → emulator/device/release acceptance | Actual results and remaining hardware/account gates, without claiming all devices from one build |

Google's [architecture recommendations](https://developer.android.com/topic/architecture/recommendations)
inform UI/data boundaries and lifecycle-aware state. Apply them with project
context; this tree does not force a new architectural layer or dependency for
every small application.

## Conditional questions and invalidation

- Adding a tablet/foldable revisits layout, state/navigation and device acceptance,
  not unrelated API/business choices.
- Switching Views/Compose reopens UI/interoperability/lifetime checks and component
  compatibility while preserving user requirements and active domain contracts.
- Process recreation, rotation/configuration change, permission denial/revocation,
  offline operation and repeated jobs become explicit scenarios when relevant.
- Background work and push are capability-specific branches, not permission for
  permanent execution, a vendor subscription or unrestricted device access.
- API level, dependency or build-tool changes flag compatibility for review; do
  not silently select the newest version or claim store eligibility.

## Reference and verification status

Reviewed 2026-10-19: Google Compose, Views and architecture references above.
No Kotlin/Java/SDK/Gradle version, minimum/target API level or release support was
selected. Actual compatibility, hardware behavior, distribution requirements,
signing and store acceptance remain unverified. No Android app was generated.
