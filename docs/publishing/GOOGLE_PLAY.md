# Google Play requirements snapshot

Checked: **2026-10-19**. Select form factor and new-submission/update versus existing
availability separately. Apply [the publishing policy](../../core/PUBLISHING_REQUIREMENTS.md).
No application's production eligibility is established by this research.

## Target API requirements

The [official target API page](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en)
states the following for submissions from **2026-08-31** (TV retains its listed rule):

| Form factor | New app/update target API floor |
| --- | --- |
| Ordinary mobile / Android Auto | Android 16 / API 36 |
| Wear OS | Android 15 / API 35 |
| Android Automotive OS | Android 15 / API 35 |
| Android TV | Android 14 / API 34 |
| Android XR | Android 14 / API 34 |

Existing ordinary mobile apps' discoverability uses a separate API 35 threshold.
The page's detailed availability section lists separate form-factor thresholds.
It describes possible extensions to **2026-11-01**; require actual granted account/
app evidence, not an assumed exemption. Android Auto and Automotive OS are distinct.

The inspected page's introductory existing-app wording and detailed form-factor
availability section are not fully aligned. Preserve that ambiguity for affected
non-mobile existing apps and verify Play Console/current authoritative clarification;
do not reuse the ordinary-mobile threshold or a translated search snippet blindly.

## Native library compatibility and enforcement dates

Google's [16 KB guidance](https://developer.android.com/guide/practices/page-sizes)
requires support for 16 KB memory pages on 64-bit devices for Play apps targeting
API 35+. The inspected page announces that unsupported **updates will be blocked
from 2027-02-01**. This differs from older commonly circulated deadlines; refresh
the live page and app's console notices before release. The capability requirement
and announced enforcement date are separate facts.

Inspect native libraries included directly or through engines/plugins/SDKs; verify
alignment and actual execution on a 16 KB environment. Managed language or
GDScript does not prove that the packaged engine's native libraries are compatible.

## Account, testing and submission gates

| ID | Applicability and required evidence | Official source |
| --- | --- | --- |
| PLAY-TEST | Personal accounts created after 2023-11-13: closed test with at least 12 continuously opted-in testers for 14 preceding days, then apply for production access; record real console outcome | [Personal-account testing](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en) |
| PLAY-PACKAGE | Actual app ID/versionCode, signed release artifact, applicable app-bundle/Play App Signing configuration and SDK/target validation | [App setup](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en) |
| PLAY-DATA | Accurate Data safety information and privacy policy reconciled with real first/third-party collection and sharing; evaluate track-specific exceptions | [Data safety](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en) |
| PLAY-DELETE | For in-scope account-creating mobile apps, in-app initiation plus a functional outside-app web deletion resource. Document the separate non-mobile/exempt cases | [Deletion policy](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en) |
| PLAY-CONTENT | Complete actual app-content declarations, ratings/target audience, ads, sensitive permissions, review access and policy-specific feature branches | [Prepare for review](https://support.google.com/googleplay/android-developer/answer/9859455?hl=en) |

Production-access testing is not a universal requirement for every account type,
nor an automatic approval after the minimum period. Account verification, owner
permissions, agreements, current policy notices and release-track state remain
console gates. New digital payments, children, user/AI content and sensitive-device
features need their applicable current policies, not generic checkbox approval.

## Remaining gates

No Play account/extension, testers, signing/app bundle, native ELF/alignment, 16 KB
runtime, physical device, policy declaration, production-access approval or store
release was tested. Complete these on the actual artifact/account and record
verified/failed/not_run with sources and a responsible owner. No APK/source build
alone proves store eligibility.
