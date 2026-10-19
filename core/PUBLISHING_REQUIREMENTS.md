# Store publishing and release-readiness policy

Applies when designing distribution, preparing a store submission/release, updating
a published product, or reviewing store eligibility. A source-only edit need not
complete every publishing checklist. Reuse existing project release records.

## Select the actual distribution scope

Record store, app/game ID, platform/form factor, territory, account type, new app
versus update, intended release date, engine/framework/language versions, native
dependencies and requested features. An iOS, Android or desktop build does not
identify its store or prove eligibility. Treat browser, alternative marketplaces,
enterprise distribution and other channels separately.

Official-source research snapshots, checked **2026-10-19**:
[Apple App Store](../docs/publishing/APPLE_APP_STORE.md),
[Google Play](../docs/publishing/GOOGLE_PLAY.md),
[Steam](../docs/publishing/STEAM.md). These cover major gates, not every possible
product/territory requirement or a guaranteed approval.

## Freshness and authority

1. Reopen the relevant official policy, submission, SDK/target and account-specific
   console requirements during release preparation and immediately before submission
   or publication. Also revisit them after a release-date, target, SDK, engine,
   monetization, privacy, content or account change. Do not treat a pinned framework
   snapshot, search excerpt, prior chat or successful old upload as current policy.
2. Record checked-at date/time, source URL/section, effective/deadline date (or
   explicitly unspecified), scope and exceptions. Distinguish current requirements,
   announced future enforcement, historical/superseded guidance and uncertainty.
3. Where official pages disagree, record both and the affected gate. Do not choose
   the shorter waiting period or easier threshold silently. Verify the actual
   console rule or obtain authoritative clarification; preserve evidence. Conservative
   planning buffers do not prove eligibility.
4. Account-specific exemptions/extensions need actual approval evidence. Merely
   seeing an extension described online does not mean this account has it.
5. If live sources or console access are unavailable, finish independent local
   work and report policy/console gates unverified. Never invent compliant dates,
   certificates, tests, account status, approval or store acceptance.

This is an on-demand verification obligation. No recurring monitor, automatic
refresh service, network policy scraper or paid account action is installed.

## Required readiness records

Use [publishing readiness](../templates/PUBLISHING_READINESS.md) or existing
equivalent records. Map each applicable requirement to its source, applicability,
actual build/configuration or console evidence, owner, status and next action.
Evidence status follows verified/failed/not_run; N/A is an applicability decision
with a reason, not a passing execution.

Inspect the release artifact, not only source: identifiers/versions, signing,
SDK/target, native libraries, engine export settings, packaged assets and dependency
inventory. Verify functional, permission, privacy, purchase/deletion and platform
behavior as applicable. Record artifact hash/build ID and tested revision. A build
that launches locally has not completed account, listing, testing-track, review,
storefront or publishing gates.

Keep privacy disclosures synchronized with actual logs/audits, crash/analytics,
ads, online services and third-party SDKs. Do not mark data collection absent
without inspecting behavior. Include safe review access and an operational backend
when required, without committing review credentials or personal/legal/bank data.

## Integrate into the existing framework

- L02 and game engine trees: test engine/runtime/export/native-plugin compatibility
  with the store's current SDK and target rules.
- L03-L06 and G04-G08: selected permissions, accounts/deletion, privacy, ratings,
  payments, user/AI content and device/online services influence requirements.
- L07: distribution/account/toolchain, signing, artifact and operational gates.
- L08 and G09: actual test-track/review/readiness evidence, release timing and
  explicit delivery authorization.
- Reuse Log/Audit/Notification and UI Notification services for relevant release,
  purchase, account/deletion and delivery failures, with redaction and truthful outcomes.

Publishing, uploading private artifacts, accepting agreements, purchasing fees,
creating accounts, sending review/support messages or releasing to users requires
the authorization applicable to that action. Existing explicit authorization is
honored; this policy does not add a new confirmation at every development step.
Framework maintenance authorization does not itself publish an application.

## Completion labels

Keep implemented, locally verified, release-artifact verified, console-ready,
submitted, store-approved and publicly released distinct. The last states require
actual corresponding evidence. User-selected deferrals for accounts/hardware
remain visible; they do not prevent completing independently verifiable work.
