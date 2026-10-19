# Steam publishing requirements snapshot

Checked: **2026-10-19**. Scope: Steam games/software and selected operating systems;
Early Access, demos, DLC and special products have additional branches.
Apply [the publishing policy](../../core/PUBLISHING_REQUIREMENTS.md).

## Onboarding and timing: preserve the observed conflict

Steam's official pages disagree about the fee-to-release waiting period for early
titles: [onboarding](https://partner.steamgames.com/doc/gettingstarted/onboarding)
currently says **21 days**, while [Steam Direct](https://partner.steamgames.com/steamdirect)
says **30 days**. Both describe a public Coming Soon page of at least **two weeks**.
Neither page establishes an exception for this particular account.

Record fee/payment eligibility, actual Steamworks earliest-release date and any
authoritative clarification. Do not silently choose 21 days. Use at least 30 days
as a conservative framework planning buffer while the conflict is unresolved,
but never treat that buffer as proof that the account/build can release.

Onboarding also requires entity/identity, payment/bank and tax information. These
are private account/owner gates; store only redacted completion evidence, not raw
personal/bank/tax data. [Official onboarding](https://partner.steamgames.com/doc/gettingstarted/onboarding),
[fee workflow](https://partner.steamgames.com/doc/gettingstarted/appfee)

## Review and release gates

| ID | Required product evidence | Official source |
| --- | --- | --- |
| STEAM-REVIEW | Finish separate Store Presence and Game Build checklists; submit store presence before build review and obtain both approvals | [Release process](https://partner.steamgames.com/doc/store/releasing) |
| STEAM-BUILD | Product launches on every advertised OS; advertised features exist in the current build; verify applicable Steam Wallet requirements for in-game transactions | [Review process](https://partner.steamgames.com/doc/store/review_process) |
| STEAM-TIME | Review guidance typically estimates 3-5 business days; allow at least 7 business days per review and additional correction time, without promising a completion date | [Review process](https://partner.steamgames.com/doc/store/review_process) |
| STEAM-CONTENT | Complete truthful content/maturity declarations and applicable generative-AI disclosures; assess player-consumed pre-generated content and live-generation guardrails | [Content survey](https://partner.steamgames.com/doc/gettingstarted/contentsurvey) |
| STEAM-ASSETS | Actual store/library graphical assets, screenshots, descriptions, localization and feature claims must match current product/rules; verify live dimensions/specifications | [Graphical asset rules](https://partner.steamgames.com/doc/store/assets/rules) |
| STEAM-RELEASE | Correct app/package/depot/build/branch/launch configuration, pricing and qualified release permissions; review the proposed public action and actual release state | [Release process](https://partner.steamgames.com/doc/store/releasing) |

AI-assisted coding tools alone are not the content survey's stated focus; its
current AI section concerns content shipped to/consumed by players and generation
inside the running product. Record applicable assets/narrative/audio/localization
and any live generation honestly. Survey answers do not waive content/IP rules.

## Platform and game consequences

An editor run is not a packaged-player test. Verify every advertised OS, clean
installation, first launch, required runtime/native dependencies, configuration,
save/recovery and requested online/platform features. macOS/Windows/Linux platform
requirements and any Steam Deck claims need their own evidence. Steam SDK/platform
features, controller support, cloud saves and achievements must not be claimed
merely because an engine can export a desktop executable.

Keep content rights, plugin/native dependency inventory and privacy/online-service
behavior consistent with the store page and actual build. The game profile and
app/server components retain their existing security/reporting obligations.

## Remaining gates

No Steamworks account, fee payment, eligibility date, legal/financial details,
listing, content survey, build/depot upload, review approval or public release was
inspected/executed. Resolve the 21/30-day source conflict through real account/
authoritative evidence before scheduling a release. Recheck all selected product
requirements immediately before submission/publication.
