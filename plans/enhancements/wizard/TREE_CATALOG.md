# Technology tree catalog and starter blueprints

Status: design inventory, not installed/verified runtime support.
Uses [tree model](TREE_MODEL.md), [layer contract](LAYER_CONTRACT.md) and
[eight layer definitions](../P8_LAYERED_WIZARD.md).

## Extensible inventory

The profile IDs below are proposed identifiers. The scope is open-ended: new
technologies add profiles and L01-L08 trees through the shared contract, without
editing a giant host-specific questionnaire. No entry here is a support claim.

| Product family | Example ecosystem/framework profiles to define | Design state |
| --- | --- | --- |
| Websites/web apps | dotnet.blazor.web; python.django.web; typescript.react.web; typescript.vue.web; ruby.rails.web; php.laravel.web | Three illustrative website blueprints below; others inventory only |
| APIs/backends | dotnet.aspnet.api; python.fastapi.api; python.django.api; java.spring.api; node.service.api; go.service.api; rust.service.api | One illustrative backend blueprint below; others inventory only |
| Desktop | dotnet.wpf.desktop; dotnet.winforms.desktop; dotnet.avalonia.desktop; python.qt.desktop; typescript.electron.desktop; rust.tauri.desktop | Inventory; each needs its own view, data, packaging and lifetime trees |
| Mobile | dotnet.maui.mobile; dart.flutter.mobile; kotlin.android.mobile; swift.ios.mobile | One illustrative mobile blueprint below; others inventory only |
| Workers/jobs | dotnet.worker; python.worker; node.worker; java.worker; go.worker | One illustrative worker blueprint below; others inventory only |
| CLI/tools | dotnet.cli; python.cli; go.cli; rust.cli; node.cli | One illustrative CLI blueprint below; others inventory only |
| Libraries/SDKs | dotnet.library; python.package; typescript.package; java.library; go.module; rust.library | One illustrative library blueprint below; others inventory only |
| Data/AI | python.data-pipeline; python.model-service; dotnet.data-pipeline; custom.data-system | Inventory; data/AI-specific privacy, evaluation and operation trees required |
| Games/simulation | dotnet.game-simulation; native.game-simulation; custom.engine-plugin | Inventory; engine, device, deterministic/realtime and packaging trees required |
| Mixed/custom | Explicit combination of named deliverables or custom profile | Compose existing contracts; unknown profiles stay unverified |

A profile also needs framework variants and version constraints. React alone,
for example, does not establish a complete application framework, rendering model,
router, build system or backend. Exact products/versions require later evidence.
Python worker/CLI and .NET library are deliberately not treated as Django/Blazor.

## Reading the starter blueprints

Each table develops one possible tree shape across all eight layers. Questions
with alternatives open follow-up branches; entries describe decisions rather
than automatic selections. Common rules are inherited from the layer definitions,
not weakened or copied. Blueprints are not code, scaffold recipes or complete
version-verified catalogs. Additional products in the inventory require their own
equally explicit trees before a runtime can claim them as supported.

## Blueprint: dotnet.blazor.web

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | Website purpose → public content, authenticated workflow or mixed → browser/SEO/connectivity needs |
| L02 | Blazor Web App or standalone WebAssembly → runtime/tooling and server/client boundaries |
| L03 | Web App → static server rendering or supported interactive variants; standalone → browser interaction → forms/components/state/UI feedback |
| L04 | Server-owned access or browser-to-server API → approved provider/access contracts → concurrency/migration/recovery |
| L05 | Authentication source and permission authority → server enforcement → client-safe state and tenant isolation |
| L06 | Existing Log/Audit/Notification mapping → server delivery and UI adapter → lifetime/reconnect/failure paths |
| L07 | Match chosen execution variant → server capability or browser assets plus required APIs → config/health/deployment |
| L08 | Existing .NET toolchain → domain/provider/component/browser checks → selected output and evidence |

Specialization example: changing the L02 execution variant revisits L03 interaction,
L04 API boundary, L05 trust, L06 UI adapter lifetime and L07 hosting. It never
silently copies direct database credentials into browser settings.

## Blueprint: python.django.web

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | Website workflows → public pages, authenticated product, admin workflows or mixed → audience/targets |
| L02 | Django project/apps → templates, API responsibilities or mixed → Python/framework/toolchain constraints |
| L03 | URL/view/template/form flows → optional client enhancement → validation/localization/UI feedback |
| L04 | Existing or new models → queries/provider → schema/data migrations → consistency/recovery |
| L05 | Accounts/session/permission model → object/tenant policies → sensitive actions and denied paths |
| L06 | Existing logging/audit/notification adapters → synchronous request or background delivery requirements → failure handling |
| L07 | WSGI/ASGI deployment needs → static/media/config/security settings → processes/health/recovery |
| L08 | Django checks/tests and selected quality tooling → browser/provider/access acceptance → output/evidence |

A Django API plus separate frontend is a composition with a separate frontend
profile. The wizard must not assume that Django means an admin-only product or
that every project needs a separate task-queue vendor.

## Blueprint: typescript.react.web

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | Browser product → content, interactive app or mixed → audience/connectivity |
| L02 | React plus an explicitly chosen application framework/build approach → execution/rendering boundaries → versions/tooling |
| L03 | Selected framework's routing/rendering/component/state/form tree → accessibility/localization/UI notifications |
| L04 | Backend-owned data via API, framework server facilities or explicit local storage → cache/offline/sync if needed |
| L05 | Authentication/session boundary and server authorization → browser-safe configuration and tenant-aware state |
| L06 | Backend reporting/delivery contracts and client diagnostics → UI adapter → third-party SDK boundaries |
| L07 | Actual framework output/runtime needs → static/server/other supported deployment → API/runtime health |
| L08 | Selected package manager/build/type/lint/test tools → browser/API/negative access checks → output/evidence |

The React profile is incomplete until its application framework/variant is chosen.
A browser UI tree must not pretend it supplies a backend data/audit service.

## Blueprint: java.spring.api

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | API consumers → internal/partner/public → business operations and compatibility |
| L02 | JVM/language/framework choices → existing build system → module/deployment boundaries |
| L03 | No visual UI with reason, or separate admin/client deliverable → API caller experience and errors |
| L04 | Existing storage contracts or selected access/provider → consistency/concurrency/migrations |
| L05 | Caller/service identities → framework-native access policies → resource/tenant rules |
| L06 | Existing reporting/delivery capabilities → outbound clients/events/jobs → replay/cancellation/failure policy |
| L07 | Approved JVM runtime/distribution → process/container/platform constraints → config/health/recovery |
| L08 | Actual chosen build/test commands → API contract/provider/security/load checks → output/evidence |

This blueprint asks about the project's actual framework/build choices. It does
not prescribe a current JDK, security library, API style or cloud provider.

## Blueprint: dart.flutter.mobile

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | Supported mobile/device targets → user journeys/distribution → connectivity and device needs |
| L02 | Framework/toolchain and platform constraints → shared versus native integration boundaries |
| L03 | Widget/navigation/state/form tree → touch/accessibility/localization → device lifecycle and UI notifications |
| L04 | Server data and/or local store → offline authority/synchronization/conflict/recovery |
| L05 | Identity and API authorization → local credential/device trust → tenant/session cleanup |
| L06 | Shared reporting and safe UI adapter → requested native integrations/push/deferred delivery → failures |
| L07 | Per-platform builds/distribution/signing → backend dependencies → crash/health/update/recovery ownership |
| L08 | Unit/widget/integration and actual device/platform gates → selected output and account/hardware deferrals |

A mobile profile does not inherit website server-rendering choices or assume
device/store acceptance from a local build. Each target keeps its own qualification.

## Blueprint: dotnet.worker

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | Trigger: continuous, scheduled, event/message or manual → work unit and required durability |
| L02 | Existing .NET hosting/toolchain → module boundaries → in-process versus independent-worker responsibility |
| L03 | Visual UI N/A with reason; any dashboard is a separate selected interface/deliverable |
| L04 | State/checkpoints/provider ownership → transaction/idempotency/concurrency and replay |
| L05 | Service identity → resource/tenant permissions → protected credentials and administrative operations |
| L06 | Log/Audit/Notification coverage → job/queue/provider contracts → timeout/cancellation/retry/dead-letter needs |
| L07 | Actual host/runtime → scheduling/restart/shutdown/capacity/health → recovery and operational ownership |
| L08 | Worker and provider checks → replay/cancellation/outage/restart evidence → output/rollout/handoff |

No queue or new process is chosen merely because background work exists. Durability
and execution constraints decide whether the active host is sufficient.

## Blueprint: python.cli

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | Local users/automation → commands, platforms, input sources and intended outputs |
| L02 | Existing Python/runtime/package tooling → command structure and distribution constraints |
| L03 | Commands/options/help/text or structured output → error/exit/cancellation experience; visual UI N/A |
| L04 | Streams/files/API/caller-owned data → persistence only if needed → integrity and recovery |
| L05 | OS/user privileges, filesystem/network scope and supplied credentials → safe sensitive inputs |
| L06 | Shared reporting/audit/notification capabilities sized to tool → file/email/other requested adapters |
| L07 | Local executable/environment/package delivery → config/update/support ownership |
| L08 | Command contract/exit-code/filesystem/failure tests → platform/distribution checks → output/evidence |

A CLI still needs deliberate user interaction and safe error reporting; N/A visual
UI does not mean N/A behavior design.

## Blueprint: dotnet.library

| Layer | Branch and nested decisions |
| --- | --- |
| L01 | Package consumers → public contract, target environments and compatibility requirements |
| L02 | Target framework/toolchain/package constraints → dependency/public API boundaries |
| L03 | Visual UI N/A; samples or design-time UI use separate profiles if requested |
| L04 | Caller-owned data or explicit persistence adapter → schema/serialization/transaction ownership |
| L05 | Caller trust/input validation → unsafe operations/secret handling → authorization ownership documented |
| L06 | Caller-supplied reporting/audit/notification contracts as appropriate → no unrequested hosted services |
| L07 | Package version/distribution/signing requirements → consumer runtime compatibility |
| L08 | Public-contract/API/serialization/consumer checks → packaging/docs/handoff evidence |

A reusable package must not create a second application permission/reporting system
or force consumers to start an unrelated service.

## Coverage and future expansion

For every profile, future registration must provide all eight roots, conditional
nodes, stable IDs, declared outputs/dependencies, reference needs and test cases.
A profile with a missing layer is incomplete. Inventory-only entries are a backlog,
not hidden fallbacks to a website tree. A user may select a custom technology and
complete a proposed design while its profile/compatibility remain unverified.

The next design pass should expand profile blueprints by prioritized user demand
and actual project evidence. Profile code, machine validation, maintained version
ranges, technology freshness and live host acceptance remain future slices.
