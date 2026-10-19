# Technology and standards verification

Apply when selecting or changing a stack, researching current recommendations,
or preparing a version-sensitive build/release. A focused change uses only the
affected decisions; it does not require auditing the entire application.

## Preserve the actual project context

Inspect project pins, manifests, lockfiles, installed toolchains and active plans.
Record the observed version separately from a proposed version and the latest
supported candidate. An existing pin is a constraint; finding a newer release
does not authorize upgrading it. Distinguish stable, preview, LTS/support lifecycle,
minimum supported OS, build SDK, target API and distribution requirements.

For new projects, prefer a supported stable combination that fits the requested
targets and maintenance needs. The newest individual components may be incompatible.
For existing projects, identify necessary changes and alternatives before changing
the approved stack. Preserve explicit unknowns when evidence is unavailable.

## Verify each affected layer

Use [the technology review template](../templates/TECHNOLOGY_REVIEW.md) or the
project's existing SDD/ADR/verification records. One decision has one owner; link
shared evidence instead of copying independently maintained version lists.

| Layer | Relevant facts to verify, when applicable |
| --- | --- |
| L01 project | Target devices, operating systems, product constraints and distribution scope |
| L02 technology | Runtime/framework/toolchain lifecycle, selected variants and package compatibility |
| L03 interface | Framework-native UI/rendering, browser/device capabilities and applicable accessibility standards |
| L04 data | Provider/driver versions, ORM/storage compatibility, migration and backup/restore behavior |
| L05 security | Identity/provider protocols, supported security mechanisms, permission and privacy requirements |
| L06 integrations | API/SDK contract versions, deprecations, reporting/notification adapters and delivery constraints |
| L07 hosting | Available runtime/OS/architecture, deployment/signing/export tooling and infrastructure constraints |
| L08 delivery | Build/test/CI tools, dependency checks, store requirements and actual acceptance evidence |

For games, verify the engine, language/runtime, renderer, export templates, native
plugins, assets and actual target together. C#, GDScript, Unity scripting and
Unreal C++/Blueprints have different constraints. The owner's Godot/C# preference
is a starting preference, not export evidence. Keep each target independently qualified.

## Source and evidence rules

Prefer official versioned documentation, release notes, lifecycle/support pages,
compatibility matrices and vendor security advisories. Check installed source for
the exact API when available. Record the subject/version, source URL/section,
checked-at timestamp with zone, effective/deprecation date when stated, target
scope, support result, compatibility result and remaining unknowns.

Use separate evidence statuses: source inspection can verify a documented claim;
it cannot verify a working build, provider, device or production deployment.
Record actual commands, revision/artifact identity and results for executed checks
under [the evidence policy](EVIDENCE_POLICY.md). Reading a page today does not
establish that every statement on it applies to this project's version or region.

If authoritative sources disagree, retain both claims, their dates and scopes.
Mark the affected decision needs_review or blocked and identify what would resolve
it. Do not silently pick the easier requirement or invent a compatibility result.

## Refresh and invalidation

Refresh affected references when selecting/changing a version, target, provider,
engine/plugin, hosting environment or standard; when a relevant deprecation or
security advisory is found; and before a version-sensitive delivery. For stores,
also follow [publishing policy](PUBLISHING_REQUIREMENTS.md), including the live
checks immediately before submission/publication. A framework pin preserves
instructions, not the future validity of external requirements.

Preserve previous decisions and evidence. Mark only affected dependent choices
and checks for review, explain why, and keep unrelated progress. Time alone never
converts an unknown result into verified. When live access is unavailable, report
the last checked date and finish independent work within authorization.

This policy defines an on-demand procedure. No version resolver, scheduled updater,
all-stack compatibility database or automatic dependency upgrade is implemented.
