# Publishing readiness: <product / release>

Store/channel: <Apple App Store / Google Play / Steam / other>
Platform/form factor/territories: <actual scope>; new app/update: <value>
Account/app identity references: <redacted IDs>; accountable owner: <person/role>
Planned submission/release date: <date>; current phase/authorization: <scope>
Source revision/artifact hash or build ID: <value>; framework snapshot: <value>

Apply [publishing policy](../core/PUBLISHING_REQUIREMENTS.md). This record is not
a submission, agreement, approval or public release.

## Current policy evidence

| Requirement ID | Official URL/section | Checked-at with zone | Effective/deadline date or unspecified | Applicability/exception and evidence | Current/future/uncertain |
| --- | --- | --- | --- | --- | --- |
| <store gate> | <direct official source> | <actual timestamp> | <actual date> | <target/account/product scope; real approval if exception> | <state> |

Capture conflicts explicitly, including Steam's currently differing waiting-period
pages and any form-factor/translation differences. Do not resolve them by guessing.

## Artifact and acceptance matrix

| Gate | Actual implementation/artifact/console locator | Exact check / expected outcome | Status verified/failed/not_run | Sanitized evidence | Owner / next action |
| --- | --- | --- | --- | --- | --- |
| SDK/target/export and native dependencies | <value> | <actual check> | not_run | <locator> | <owner> |
| Signing/IDs/versions/distribution | <value> | <actual check> | not_run | <locator> | <owner> |
| Functional/device/OS/runtime compatibility | <value> | <actual check> | not_run | <locator> | <owner> |
| Privacy/permissions/accounts/deletion | <value> | <actual check> | not_run | <locator> | <owner> |
| Content/ratings/AI/assets/rights/monetization | <value> | <actual check> | not_run | <locator> | <owner> |
| Account/test-track/timing and review access | <value> | <actual check> | not_run | <locator> | <owner> |
| Listing/build reviews and public release | <value> | <actual check> | not_run | <locator> | <owner> |

Mark N/A through applicability with a reason. Missing accounts/hardware/access are
not_run gates, not passed or automatically N/A. Keep credentials, signing keys and
raw personal/bank/tax data outside the repository and evidence.

## Disposition and handoff

Current stage: <implemented / local / artifact verified / console-ready / submitted /
store-approved / released; evidence required for each claimed stage>
Failures, unresolved source conflicts, upcoming deadlines and granted exceptions:
<actual findings and evidence>.
Deferred external gates: <scope, owner, next action>.
Public/external actions already authorized and still required: <actual scope>.
