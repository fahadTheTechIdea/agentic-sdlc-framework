---
name: sdlc-review-cycle
description: Run a bounded multi-lane review cycle with parallel reviewers, capped builder fix rounds, an approver and a recorded human decision.
---

# Run a review cycle

Read `core/REVIEW_CYCLE.md` (rules, lanes, limits) and `docs/REVIEW_CYCLE.md`
(commands). Use this for significant or high-risk changes only; a small edit
uses ordinary verification. Paths are relative to the framework root; run
`scripts/review_cycle.py` from it. You are the orchestrator and the only writer
of the record.

1. **Confirm the cycle fits.** The change needs written acceptance criteria
   (`skills/sdlc-specification/SKILL.md`). Name the builder, the lanes the change
   needs, and the accountable *human* or role; an agent cannot be accountable.
   Set `--independent` or `--human-approval` when governance requires them.
2. **Check what you may delegate.** Separate reviewer agents need host support and
   the authority the host and project require. Otherwise review each lane yourself
   in turn, label it `self`, or ask a human reviewer. Never present self-review as
   independent.
3. **Open the record** with `init` in `.sdlc/review/<change-id>/` (or the project's
   existing location). Do not overwrite an existing record; resume it with `status`.
4. **Fix the revision.** Use the full commit SHA of a clean tree, or a
   `sha256:<hex>` digest of the exact patch for uncommitted work. Do not commit or
   push only to obtain one; Git authorization is unchanged.
5. **Run every lane on that revision, in parallel when the host allows.** Give each
   reviewer the lane name, revision, criteria locator and the report contract
   (`templates/review-cycle/lane-report.json`). Reviewers do not edit; they reply
   with one JSON object. Do not act on partial results: wait for all lanes.
6. **Record each report** with `report`. A contract error is returned and nothing
   is written; ask that reviewer to correct the format only. A reviewer that returned
   nothing has not reported, so run that lane again. Never ask for a different verdict.
7. **Follow `status`:**
   - `resume_builder`: give the builder the findings by id. It follows
     `skills/sdlc-implementation/SKILL.md`, does not weaken tests to pass, produces a
     new revision and answers each finding. Then repeat from step 5 with **all** lanes.
   - `awaiting_approver`: run the approver on the passing round; record its output
     with `recommend`.
   - `ready_to_deliver` or `human_approved`: run `deliver-check --revision <the
     revision to ship>`; only on exit 0, deliver through the project's authorized Git
     workflow. A different revision needs a new round.
   - `needs_human`: show the reasons and findings, ask the accountable human to
     `approve`, `reject` or `request_changes`, and record the answer with `decide`
     exactly as the rules in `core/REVIEW_CYCLE.md` allow. Never choose for them.
   - `human_rejected`: stop.
8. **Report** the final state, rounds used, unresolved findings and `limitations`,
   and say what the gate does not prove. Link the record in the tracker and handoff.
   Any live agent behavior you did not observe stays `not_run`.
