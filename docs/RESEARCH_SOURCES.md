# Source register

Reviewed 2026-10-19. These sources establish host file conventions; lifecycle,
SOLID review, RACI and evidence rules in this baseline are framework design
choices. They do not imply product certification or standards conformance.

| Source | Supported fact | Use here |
| --- | --- | --- |
| [OpenAI AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Codex discovers project instructions along the directory path; overrides can affect what loads | Root instruction adapter; verify effective instructions |
| [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) | Project skill discovery includes `.agents/skills`; skills use `SKILL.md` | Generated Codex wrappers |
| [Claude Code memory](https://code.claude.com/docs/en/memory) | Claude project guidance uses `CLAUDE.md` | Explicit shared-file routing |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | Project skills use `.claude/skills/<name>/SKILL.md` | Generated Claude wrappers |

Refresh host conventions before changing adapters. Installed versions, workspace
trust and organization settings can affect availability. Check live discovery
in each intended host rather than treating documentation as runtime evidence.
No external skills are vendored; canonical procedures here were authored for
this framework. Additional standards or compliance requirements need a separate
source-backed assessment for the target project.

CI uses GitHub-hosted runners and the official `actions/checkout` v4 and
`actions/setup-python` v5 actions. Their tag targets were read directly from
the official Git repositories on 2026-10-19 and pinned to immutable commits
in the workflow. Updating those pins is a reviewed dependency change; the
local Python tools themselves have no third-party package dependencies.

## Application operational services

Reviewed 2026-10-19. The requirement to provide Log, Audit and Notification Services
in every application, with a UI Notification Service for UI applications, comes
from the owner's direct instruction. The sources below support implementation
details; they do not mandate these service names or certify any application.

| Source | Supported guidance | Application here |
| --- | --- | --- |
| [OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | Deliberate event coverage, protected logging data and verification of logging failures | Coverage matrix, redaction and storage/failure checks |
| [Microsoft exception practices](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions) | Intentional exception handling and preservation of original exception information | No silent swallowing; explicit failure/recovery and owning reporting boundary |
| [OpenTelemetry log model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) | Structured records with event time, severity and optional trace correlation | Shared event envelope and propagated correlation |
| [Microsoft transactional outbox](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos) | Persist business state and outgoing event intent atomically, then relay events | Durable intent for operations requiring that guarantee; actual provider validation remains necessary |

The portable framework does not require Azure, a particular logging vendor or a
separate service deployment. Channel policy, UI integration, durable audit storage
and emergency diagnostic behavior must be designed and tested in each application.

## Quality, security, reliability and agent evaluation

Reviewed 2026-10-19. The owner accepted the nine recommendations researched from
these primary sources. Their application in this framework is a design choice;
no source mandates identical service names, every gate for every task, or automatic
approval stops. Apply controls proportionally through existing project mechanisms.

| Source | Supported guidance | Application here |
| --- | --- | --- |
| [OWASP secure coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html) | Test integrity, verified dependencies, untrusted development content, scoped tools and review of unexpected changes | Test/lockfile review, dependency/secret checks, host-enforced access and adversarial fixtures |
| [Anthropic agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Stable tasks, independent outcome tests, transcript review and regression evaluations | Six starter cases, outcome grader and separate human rubric; no live result implied |
| [Anthropic long-running agent harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Incremental work, persistent progress and real end-to-end verification | Existing coherent slices/handoff plus actual acceptance-boundary checks |
| [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Least privilege, deny by default, permission checks on every request and authorization tests | Shared trusted-boundary policy and denied/resource/tenant checks |
| [Microsoft options validation](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options) | Typed options and startup validation with ValidateOnStart | Platform-native config validation; .NET example rather than a portable dependency |
| [Microsoft retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry) | Transient faults, bounded retries and duplicate effects for non-idempotent operations | Retry deadlines, cancellation and explicit replay/idempotency contracts |
| [Microsoft continuity and recovery](https://learn.microsoft.com/en-us/azure/reliability/concept-business-continuity-high-availability-disaster-recovery) | Test backups/restoration, integrity and recovery duration; validate recovery plans | Isolated restoration evidence and risk-based migration recovery |
| [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) | Latency, traffic, errors and saturation; user-impacting actionable alerts | Runtime signals, meaningful thresholds and shared notification routing |

Dependency and secret scanners, authorization/recovery tests and runtime health
implementations belong to target projects. The portable framework does not silently
add vendors, network scans, production drills or new application infrastructure.

## Wizard tree design examples

Reviewed 2026-10-19 for P8 design vocabulary only. Blazor and Django are examples
within a broader technology-tree architecture. These sources support distinct
framework concepts; they do not establish a version recommendation or verify all
cataloged profiles. Selected versions/compatibility and a refresh policy remain
separate work. Starter blueprints not covered in this register are proposed question
structures and require official, version-specific references before runtime promotion.

| Source | Supported branch concepts | Design use |
| --- | --- | --- |
| [Blazor render modes](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/render-modes?view=aspnetcore-10.0) | Blazor Web App rendering/interactivity choices differ from standalone WebAssembly | Distinct L02/L03/L07 branches rather than a universal website menu |
| [Blazor security](https://learn.microsoft.com/en-us/aspnet/core/blazor/security/?view=aspnetcore-10.0) | Security depends on server/client boundaries and enforcement | L05 questions linked to chosen execution model |
| [Django overview](https://docs.djangoproject.com/en/6.1/intro/overview/) | Models, URLs, views and templates form framework-specific development concepts | Django-specific application/interface tree vocabulary |
| [Django authentication](https://docs.djangoproject.com/en/6.1/topics/auth/) | Framework account/authentication/permission facilities | Dedicated identity/access questions, not another framework's menu |
| [Django models](https://docs.djangoproject.com/en/6.1/topics/db/models/) | Framework model/data concepts | Dedicated data/model choices and references |
| [Django deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/) | Deployment/security/configuration/static/media checks | Django-specific operations and acceptance questions |

The Django stable documentation URLs resolved to 6.1 during this inspection; this
is source provenance only. No Django or .NET version was selected for a project.

### MAUI mobile/desktop expansion

Reviewed 2026-10-19 for the dedicated MAUI design tree. MAUI now has a detailed
blueprint, rather than only an inventory entry. These references establish platform
and UI-variant concepts; no SDK/workload versions, minimum OS values, release-support
status or device/store acceptance were selected or qualified by this design update.

| Source | Supported concept | Design use |
| --- | --- | --- |
| [MAUI overview](https://learn.microsoft.com/en-us/dotnet/maui/what-is-maui?view=net-maui-10.0) | Native mobile/desktop development, shared/platform-specific code and Apple build prerequisites | Separate mobile/desktop branches, native UI choices and explicit toolchain/hardware gates |
| [MAUI platforms](https://learn.microsoft.com/en-us/dotnet/maui/supported-platforms?view=net-maui-10.0) | Platform, release and Hybrid prerequisites differ; additional Tizen support is provider-supplied | Target/variant compatibility references and independent qualification |
| [Blazor Hybrid](https://learn.microsoft.com/en-us/aspnet/core/blazor/hybrid/?view=aspnetcore-10.0) | Native execution of Razor components in an embedded WebView differs from browser WebAssembly | Dedicated Hybrid UI/service-lifetime/WebView branches, separate from website profiles |

### Native iOS/Android and React Native mobile trees

Reviewed 2026-10-19 for design vocabulary and platform-specific decision areas.
The trees prescribe questions and evidence needs; exact SDK/runtime/library versions,
device capabilities, signing and distribution requirements still need project-level
verification. No app or simulator/device/store checks were executed.

| Source | Supported concept | Design use |
| --- | --- | --- |
| [Apple SwiftUI](https://developer.apple.com/swiftui/) | SwiftUI and incremental interoperability with UIKit | Native iOS UI variants, state/navigation/interoperability questions |
| [Apple iOS](https://developer.apple.com/ios/) | Native iOS development and platform resources | Separate native Apple mobile profile and reference boundary |
| [Xcode requirements](https://developer.apple.com/xcode/system-requirements) | Xcode/SDK/host/deployment compatibility is version-dependent | Record actual native toolchain constraints rather than a guessed latest version |
| [Android Compose](https://developer.android.com/develop/ui/compose/documentation) | Compose has its own UI/state/lifecycle/adaptive layout/test concepts | Dedicated Kotlin/Compose tree |
| [Android Views](https://developer.android.com/develop/ui/views/layout/declaring-layout) | View/layout-based UI has separate framework concepts | Existing View-based and deliberate interoperability branches |
| [Android architecture](https://developer.android.com/topic/architecture/recommendations) | Context-sensitive UI/data separation, lifecycle and testing recommendations | Native Android boundary/lifecycle/verification questions, preserving active contracts |
| [React Native introduction](https://reactnative.dev/docs/getting-started) | React concepts applied to native application development | Separate shared-mobile tree, with explicit native platform gates |

Apple's JavaScript-only tutorial/documentation endpoints did not provide substantive
readable content during this check; the accessible SwiftUI overview, iOS overview
and Xcode compatibility page were used instead. Kotlin Multiplatform and native
web-container profiles remain inventory-only; no compatibility claim follows from
listing them in the mobile selector.

## Game-domain layers and engine trees

Reviewed 2026-10-19 for P9 design. The game group structure and optional shared-core
boundary are framework design choices. Engine documentation supports distinct
terminology, runtime/target constraints and ownership questions, not blanket
cross-engine compatibility, platform support, deterministic physics or a runnable
game wizard. No engine/project version was selected by this research.

| Source | Supported concept | Design use |
| --- | --- | --- |
| [Godot C#/.NET](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/index.html) | .NET-enabled editor and language/target-specific export constraints; inspected guidance excludes C# web export | Godot/C# profile, exact-version/toolchain gates and explicit browser-target conflict |
| [Godot scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html) | Reusable, loosely coupled scene/node relationships | Engine-native world/lifetime/dependency branches, preserving active contracts |
| [Godot processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html) | Frame processing and physics processing have different timing responsibilities | Explicit simulation tick ownership and frame/physics integration checks |
| [Unity gameplay programming](https://docs.unity3d.com/Manual/scripting.html) | Unity-specific gameplay programming concepts and C# guidance | Separate engine/object/toolchain questions rather than a Godot tree copy |
| [Unity prefabs](https://docs.unity3d.com/Manual/Prefabs.html) | Reusable engine object/asset composition | Scene/object/prefab and content reference decisions |
| [Unity scripting restrictions](https://docs.unity3d.com/Manual/scripting-restrictions.html) | Backend/platform/AOT restrictions differ from general .NET expectations | Actual runtime/API/export checks for shared libraries and packaged players |
| [Unreal C++](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine) | Native gameplay classes, reflection and editor integration | Distinct C++ module/object and tooling branches |
| [Unreal Blueprints](https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprints-visual-scripting-in-unreal-engine) | Visual gameplay scripting can complement C++ | Blueprint/C++ responsibility choices; no built-in C# compatibility claim |
| [Unreal gameplay framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine) | Game, player, controller, pawn and state responsibilities | Engine-specific ownership, level/session and multiplayer questions |

The attempted separate Godot c_sharp_platforms URL was unavailable; the accessible
C# index above supplied the inspected platform constraints. Engine documentation
must be refreshed against the selected release/target before real project setup.
Unity/Epic documentation version labels observed during research are not project
pins or recommendations. Plugin, asset, SDK, vendor license/distribution and actual
build/playtest/device/online-service evidence remain separate acceptance work.
