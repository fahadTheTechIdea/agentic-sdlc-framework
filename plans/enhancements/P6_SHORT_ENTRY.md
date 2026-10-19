# Phase 6: shared sdlc-orch entry name

Date: 2026-10-19. Authorization: owner requested `sdlc-orch` in both hosts.
Work directly on master and refresh the existing user installations.

Add a small `skills/sdlc-orch/SKILL.md` entry that routes to the existing
orchestrator procedure, preserving the longer name and one canonical workflow.
Register it in the manifest, generate both host wrappers, and update the root
instructions, adoption snippet, catalog and usage guides to prefer the short name.
Retain historical evidence and prior installed snapshots.

Verify both names are included in new host-specific project adoptions and that
the snapshot remains valid. Run the existing 32 regression tests, structure,
wrapper parity and skill validation. Publish master and inspect hosted CI.
Back up receipt-owned user integrations, install the short entry in both user
skill directories, refresh snapshot references/global instructions and verify
both hosts discover the short command without running model tasks.

Local verification: 32 regression tests passed on Windows/Python 3.14.3 with
base master `8a1f825eab1ae53d8f2a432c2f90f975ffac6788` plus this update. File/link
validation, wrapper parity, all eight entry/skill checks and diff whitespace checks
passed. Tests cover short/long wrapper installation for both project adapters.
Host refresh and discovery results are recorded in the local installation receipt;
hosted CI results belong to the published commit. No model behavior evaluation
is implied by discovery checks.

Application repositories are not changed; explicitly pinned project snapshots
retain their existing version until deliberately updated.
