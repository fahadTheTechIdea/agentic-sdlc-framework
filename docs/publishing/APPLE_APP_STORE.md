# Apple App Store requirements snapshot

Checked: **2026-10-19**. Scope: Apple App Store submissions, primarily iOS/iPadOS;
other Apple platforms and alternative distribution require their applicable branches.
This is researched policy context, not a completed application readiness record.
Apply [the publishing policy](../../core/PUBLISHING_REQUIREMENTS.md).

## Dated gates observed in official guidance

| ID | Applicability and observed rule | Effective date | Primary source |
| --- | --- | --- | --- |
| APPLE-01 | Uploads must use Xcode 26 or later with the applicable SDK 26 family listed by Apple (iOS/iPadOS/tvOS/visionOS/watchOS) | 2026-04-28 | [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) |
| APPLE-02 | iOS/iPadOS uploads must have a deployment target of iOS 13 or later | 2026-09-09 | [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) |
| APPLE-03 | Answer the updated age-rating questions to avoid interruption of update submissions | 2026-01-31 | [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) |
| APPLE-04 | Required-reason API use, including SDK use, needs approved reasons | 2024-05-01 | [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) |

SDK 26 does **not** mean a minimum supported device OS of 26. Record SDK, deployment
target and engine/toolchain compatibility separately. Do not extrapolate the
listed SDK rule to macOS; inspect the actual macOS submission requirements.

## Release checklist and project evidence

| Gate | Required project work and evidence | Official reference |
| --- | --- | --- |
| Identity/build | Confirm App Store Connect access, app/bundle IDs, versions, signing/provisioning and current upload validation. Capture archive/build identity and compatible engine/SDK evidence | [Submitting](https://developer.apple.com/app-store/submitting/) |
| Privacy | Reconcile App Privacy responses and policy with actual first/third-party collection, tracking, analytics, crash/audit and online behavior | [App Privacy](https://developer.apple.com/app-store/app-privacy-details/) |
| SDK supply chain | Check the current listed SDKs/repackaged dependencies for required privacy manifests and, for applicable binary SDKs, signatures; inspect the release dependency inventory | [SDK requirements](https://developer.apple.com/support/third-party-SDK-requirements/) |
| Accounts | Apps supporting account creation must offer initiation of deletion in-app, with applicable retention/process exceptions accurately communicated. Test the real flow and associated data handling | [Account deletion](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion) |
| Review access | Stable functioning release, truthful metadata/screenshots, accessible backend and usable demo access/resources where needed; explain non-obvious features | [Review guidelines: Before You Submit](https://developer.apple.com/app-store/review/guidelines/) |
| Conditional features | Evaluate applicable current rules for digital purchases/subscriptions, third-party login, permissions, tracking, children, user-generated/AI content, content rights and safety; document real exceptions | [Review guidelines](https://developer.apple.com/app-store/review/guidelines/) |
| Territories/account | Verify current agreements and regional/trader obligations through the actual account. Do not assume a framework knows the owner's legal classification | [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) |

The SDK requirements page applies listed-SDK rules to the described new-app or
SDK-adding update cases, including repackaged SDKs. Do not claim every dependency
requires the same signature treatment. Recheck the list for the actual submission.

## Platform and engine consequences

Godot, Unity, MAUI, Flutter, React Native and native apps must prove that their
selected export/native-library chain produces an acceptable archive and supports
the requested device/toolchain. C# versus GDScript is not an exemption from store
policy. macOS adds its own signing/sandbox/distribution checks; alternative
distribution/notarization is not identical to App Store approval.

## Remaining gates

No Apple account, agreements, legal classification, signing identities, archive,
devices, privacy submission, review or store release was inspected/executed for an
application. Recheck current official pages and App Store Connect immediately
before a real submission; record new effective dates instead of assuming this
snapshot remains newest. Use the publishing-readiness matrix and actual owner.
