# Phase 4: master-only maintenance and practical usage

Date: 2026-10-19. Scope: owner requested the branch merged into master and the
README and related documents updated. Work directly on master only.

## Observed state and outcome

PR #1 was already merged into master at `3cff76c`. A fresh fetch and merge check
reported the baseline branch fully included. The old branch needs no additional
merge and is retained as history; creating another branch or PR is outside scope.

The README and adoption guide now explain getting source from master, choosing
new/existing application folders, installing the appropriate host adapter once,
preserving existing instructions, invoking only the orchestrator and resuming
without reinstalling. Second-host installation remains a documented manual step.

Repository instructions enforce the owner's master-only choice. Portable core,
workflow and skill guidance respect each adopted project's authorized Git workflow
instead of requiring branches/PRs. Original verification reports remain dated
evidence; this documentation update does not establish live host behavior.

## Files and checks

Update README, AGENTS.md, adoption/adapter guides, portable Git workflow wording,
baseline status, specification, tracker and delivery design. No runtime or
installer behavior changes. Preserve license text, existing history and unrelated work.

Run framework validation, wrapper parity, relevant skill validation and the
existing tooling regression suite required by AGENTS.md. Record actual outcomes
in this document/tracker, commit directly to master and push normally.

## Validation results

Local environment: Windows, Python 3.14.3; 2026-10-19. Source state: master at
`52e757c6f97334f913ae4e54303c7dd6b24a05f2` plus the P4 documentation/skill-body
changes, followed by this status update. No runtime or installer code changed.
Review type: author self-review.

| Check actually run | Result |
| --- | --- |
| `python scripts/validate_framework.py --evidence evidence/v1.2/checks.json --raci templates/RACI.json` | Passed |
| `python scripts/sync_adapters.py --check` | Passed; wrappers match canonical metadata |
| `python -m unittest discover -s tests -v` | 32 passed |
| Local Skill Creator validator for the orchestrator and implementation skills | Both passed |
| `git diff --check` | Passed |
| Fresh fetch and merge check against the baseline branch | Already up to date; baseline fully merged |

Hosted CI for this follow-up is available in the master workflow run after push;
earlier hosted baseline results do not certify this later update. Live Codex/Claude
pilots, application pilot, independent review and policy/release acceptance remain
separate open gates.
