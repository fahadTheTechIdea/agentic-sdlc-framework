# Review cycle guide

How to run the [review cycle policy](../core/REVIEW_CYCLE.md): parallel specialist
reviewers, a bounded builder loop, an approver and a recorded human decision.
Python 3.11+ and the standard library suffice. Use it for significant or
high-risk changes; a small edit keeps the normal verification.

Start it in either host with `$sdlc-orch review` (Codex) or `/sdlc-orch review`
(Claude). `rc` also works. These are request shortcuts in the existing skill, like
`w`, not separately registered commands. The assistant follows
[the review-cycle skill](../skills/sdlc-review-cycle/SKILL.md).

## How the pipeline maps to this framework

The cycle follows the "factory" pattern of a spec-writer, a builder, four parallel
reviewers (security, UX, UI design, code), a wait-for-all gate, a capped builder
loop, an approver and a human escalation. This table shows where each step lives
and where this framework deliberately differs.

| Pattern step | Here | Difference |
| --- | --- | --- |
| Spec-writer | [Specification skill](../skills/sdlc-specification/SKILL.md); the criteria locator is recorded in `cycle.json` | Reviewers judge against written criteria |
| Builder | [Implementation skill](../skills/sdlc-implementation/SKILL.md) | The builder id can never appear as a reviewer or approver |
| Four parallel reviewers | Lanes `security`, `ux`, `ui-design`, `code`, plus `operations` and `publishing` | Lanes are chosen per change; a library has no `ux` lane |
| Wait for all reviews | State `awaiting_reports` | Enforced by the gate: a missing lane is not a pass |
| Any CHANGES resumes the builder, at most 2 rounds | State `resume_builder`, `max_fix_rounds` | Needs a new revision, and every lane reviews it again |
| All PASS goes to the approver | State `awaiting_approver` | The approver cannot override a lane |
| APPROVE merges to main | State `ready_to_deliver` | **Does not merge.** Delivery uses the project's authorized Git workflow |
| ESCALATE goes to needs-human | State `needs_human` | Also entered for a blocked lane, a spent budget or a missing independent review |
| `/factory approve` | `review_cycle.py decide` | Only the named accountable human; origin and their words are recorded |
| Models per role | Not pinned | The host and project choose; see [policy](../core/REVIEW_CYCLE.md) |

## Run it

From the framework root (the project's `.agentic-framework` when adopted):

```text
python scripts/review_cycle.py init .sdlc/review/CHG-7 --change "CHG-7 Password reset" \
    --criteria specs/reset.md --lanes code,security --builder builder \
    --accountable owner --accountable-name "Project owner"
python scripts/review_cycle.py report .sdlc/review/CHG-7 --file security-round-1.json
python scripts/review_cycle.py recommend .sdlc/review/CHG-7 --file approval-round-2.json
python scripts/review_cycle.py decide .sdlc/review/CHG-7 --by owner --decision approve \
    --origin terminal --rationale "Accepted the remaining risk"
python scripts/review_cycle.py status .sdlc/review/CHG-7 --json
python scripts/review_cycle.py deliver-check .sdlc/review/CHG-7 --revision <commit-or-digest>
```

`deliver-check` exits 0 only when the state is `ready_to_deliver` or `human_approved`
and the revision is the one the lanes reviewed, so a later commit cannot ride on an
earlier approval. `status` prints the reviewed revision.

Options on `init`: `--max-fix-rounds N` (default 2), `--independent` (a `self`
review does not count), `--human-approval` (always end with a human decision) and
`--no-approver`. Contracts are the starters in
[templates/review-cycle](../templates/review-cycle/cycle.json). The tool rejects
unknown fields, an overwrite, a mixed-revision round, an unchanged revision after a
`CHANGES` round, an approval before every lane passed and a decision that answers
no escalation. A rejected record is not written and the command exits 1.

Excerpts of real tool output from a scripted two-lane run in a scratch folder (the
revisions were placeholder hashes, and the three outputs come from separate commands):

```text
State: resume_builder (round 1)
Next: Builder addresses the listed findings and produces a new revision; then start the next round.
Next round: 2
Finding security/SEC-1 (major) [src/auth.py:88]: Reset token is logged in clear text

ERROR: round 2: the builder was resumed but the revision did not change

State: awaiting_approver (round 2)
Next: Approver reviews the passing round and records APPROVE or ESCALATE.
```

The record is the audit trail: keep it with the change, and keep secrets and
personal data out of reports.

## Host setup

The reviewers return JSON; the orchestrator records it, so lanes never write the
same file. These templates are optional and not activated by the framework. Copy
only what you want, after reading them. Their behavior in a live host has not been
evaluated here.

**Claude Code.** Copy [adapters/claude/review-cycle](../adapters/claude/review-cycle/review-code.md)
to the project's `.claude/agents/` folder. Subagents are Markdown files with `name`
and `description`; the `tools` allowlist is enforced by the harness, and an omitted
`model` uses the main conversation's model. Set `model` per lane if you want a tier
split. Subagents inherit the parent's permission rules and `Bash` is not read-only,
so deny writes and pushes in `permissions.deny` rather than relying on the prompt.
A new `agents` folder needs a restart.

**Codex.** Copy [adapters/codex/review-cycle](../adapters/codex/review-cycle/review-code.toml)
to `.codex/agents/`. Codex starts subagents when you ask or when project or skill
instructions request it, so ask for the reviewers explicitly when you start the
cycle. Subagents inherit the session's sandbox and approvals and a custom agent
cannot make itself read-only, so start the session in a read-only mode when you can.

**No subagents.** Run each lane in turn yourself; each report's `reviewer.kind` is
`self`. With `--independent` such a lane escalates to the accountable human. A human
can write a lane report by hand from the template with `kind` `human`.

## What this does not establish

The tool checks structure and sequence. It cannot prove who wrote a file, that a
reviewer was a different model or context, or that a `checked` entry is true. It
does not launch agents or call a model. Unit tests exercise the gate with synthetic
records; no live Codex or Claude review cycle has been run. See
[the policy limits](../core/REVIEW_CYCLE.md) and the [validation notes](VALIDATION.md).
