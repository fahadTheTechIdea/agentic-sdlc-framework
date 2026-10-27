# P13: Review cycle

Date: 2026-10-26. Authorization: the owner's request to revise and enhance the
framework and implement a pipeline like the one in `docs/DevelopmentCycle.jpeg`
(spec-writer, builder, four parallel reviewers, wait-for-all, capped builder rounds,
approver, human escalation). Owner/accountable: repository owner. Implementation and
review: assistant, self-review. Nothing was committed, pushed, merged or released.

## Gap and design

The framework had implementation, verification and a line allowing independent
review, but no structure for several reviewers, a stopping rule, an approver's limits
or a recorded human decision. The picture is a pattern for exactly that. A
deterministic gate was chosen over prose alone because the parts that a model most
easily gets wrong (waiting for every reviewer, stopping, not overriding a reviewer,
inventing an approval) are checkable from a small record.

The framework keeps its own rules where the picture conflicts with them: an agent
approver gives a recommendation and cannot merge; a human decision is recorded by the
named accountable human; no model names are pinned; separate agents need host support
and authorization. [Policy](../../core/REVIEW_CYCLE.md) and
[guide](../../docs/REVIEW_CYCLE.md) own the rules and the mapping table. Research is
recorded in [the source register](../../docs/RESEARCH_SOURCES.md).

| Requirement | Acceptance |
| --- | --- |
| REV-001 | Policy defines roles, lanes, states and rules; constitution item 14 points to it |
| REV-002 | A round advances only when every required lane reported on one revision; a missing lane is not a pass |
| REV-003 | `CHANGES` resumes the builder up to `max_fix_rounds` automatic times; a new revision is required and every lane reviews it; the spent budget escalates |
| REV-004 | The approver cannot override a lane, cannot be the builder, and only recommends; the builder cannot appear as a reviewer |
| REV-005 | Only the named accountable human decides escalations; `conversation` origin must quote their words; `grant_rounds` adds automatic rounds |
| REV-006 | Reports and decisions are never overwritten; unknown fields, stray files, links, duplicate keys and hand-added rounds are refused |
| REV-007 | `ready_to_deliver` is a gate result; the cycle merges and releases nothing |
| REV-008 | Optional Claude and Codex agent templates exist for four lanes and the approver, are read-only by tool list, and are not installed by the framework |
| REV-009 | Orchestrator routing and `review`/`rc` shortcut, skill, catalog, manifest, adoption bundle, validator and documentation are consistent |
| REV-011 | `deliver-check` succeeds only for a deliverable state and the exact reviewed revision; `status` shows that revision |
| REV-010 | Gate behavior has focused tests whose catching power is shown by mutation; live host behavior is reported `not_run` |

## Revised existing material

Constitution (item 14), delivery workflow (table row and review phase), orchestrator
and short-entry skills (routing and shortcut), verification and implementation skills
(how a resumed builder behaves), handoff template (review state), templates index,
skill catalog, README, both adapter READMEs, evaluation guide (manual rubric),
validation guide, research register, manifest and validator (starter-record contract).

## Status

Implemented and locally verified on 2026-10-26 (Windows 11, Python 3.14.4). Base
revision `fdc9dceb0bae90a05c1575cb033849daee0e6744`; the changes are uncommitted in
the working tree. Scope digest `sha256:393e3eb40cbe1550dbc1b0ca4750a20a24c1ebd2084e4e87de9bf79e744dde9d`
covers the 40 changed or new files (including the pre-existing untracked reference
image) except this plan and the tracker, which hold the results. It is the SHA-256 of
the sorted `sha256  path` lines from `git status --porcelain -uall`.

| Command | Result | Covers |
| --- | --- | --- |
| `python scripts/validate_framework.py` | exit 0 | REV-009: manifest, links, wrappers, starter records |
| `python scripts/sync_adapters.py --check` | exit 0 | REV-009: generated wrapper parity for nine skills |
| `python -m unittest discover -s tests -p "test_review_cycle.py"` | 58 tests, OK | REV-002 to REV-008, REV-010, REV-011 |
| `python -m unittest discover -s tests -p "test_framework.py"` | 32 tests, OK | REV-009: installer, validator and adapter behavior with the new files |
| `python scripts/adopt.py <scratch> --adapter claude` (preview only) | new files listed in the bundle | REV-009: adoption snapshot |

Catching power: ten mutations of a scratch copy of the gate were each caught by the
tests, and none survived: wait-for-all, round cap, approval overriding `CHANGES`, an
unchanged-revision round, builder self-review as another id, ignored required
independence, report overwrite, a human decision without an escalation, any actor
deciding, and mixed revisions. The first test run also exposed a real flaw, which
was fixed and given its own tests: a human-requested resumption spent the automatic
round budget it was meant to extend. A scripted run of the real CLI produced the
excerpts in the guide.

**Not run, deliberately.** Only the two test files touched by this work ran, as the
owner's standing rule asks for focused tests. `test_wizard.py` and `test_agent_eval.py`
were not run: this change did not edit the wizard or evaluation code. The repository
instructions list the full `discover` command, which CI runs; it was not run locally
and no push was made. Author self-review only; no independent reviewer ran.

## Remaining gates

No live Codex or Claude review cycle has been run, so the templates, the shortcut and
the skill's procedure are not evaluated in a host. The templates were written against
vendor documentation read on 2026-10-26 and need a fresh recheck before use. The gate
cannot authenticate authorship, reviewer independence or the truth of `checked`
entries. Lane coverage beyond the six standard lanes is project-defined. The owner
decides whether to commit and push; the repository's workflow runs on every push.
