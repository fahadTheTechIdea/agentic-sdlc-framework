# P12: Interactive project wizard runtime

Date: 2026-10-19. Authorization: proceed with the interactive wizard runtime.
Owner/accountable: repository owner. Implementation and review: assistant,
self-review. Work directly on master; preserve existing plans and installations.

## Design and scope

Use Python 3.11+ standard library and a portable terminal interface over one
versioned JSON catalog and session contract. Separate catalog/state logic from
CLI presentation. Reuse existing L01-L08 and G01-G09 blueprints and core policies;
do not introduce another skill, web server, package dependency or application
scaffolder. Runtime support means decision collection, not qualified engine builds.

| Requirement | Acceptance |
| --- | --- |
| RUN-001 | Distinct selectable application/mobile/game profiles cover eight layers; games also cover nine domain groups; invalid catalogs fail |
| RUN-002 | New/existing project entry, multiple deliverables, conditional questions and explicit unknown/custom choices |
| RUN-003 | Save/resume typed answers with origin, observed source, applicability, timestamp and change history |
| RUN-004 | Changed dependencies and profile switches preserve history and unrelated deliverables; conflicts remain visible |
| RUN-005 | Preview defaults to no writes; explicit saves use atomic replacement, collision/symlink/concurrent-change checks; interruptions preserve prior saves |
| RUN-006 | Interactive back/defer/review/quit and noninteractive commands use the same core; decision export is explicit and never overwrites project artifacts |
| RUN-007 | Existing-project inventory is read-only, bounded, path-only and never an implicit stack upgrade; source/compatibility/store checks stay unverified |
| RUN-008 | CLI diagnostics, persisted mutation history and terminal notifications provide scoped reporting without secret payload logging or no-op services |
| RUN-009 | Integration in manifest/adoption/host guidance; regression, actual scripted terminal sessions and CI; installation refresh |

## Verification and remaining gates

Test malformed catalogs/state, profile-specific branches, transitive invalidation,
hidden answers, profile history, mixed deliverables, invalid values/origins,
N/A reasons, preserved unknowns, interrupted/failed saves, concurrency, collisions,
preview/export and real CLI interactions. Existing framework checks remain required.
Recorded CLI transcripts establish terminal behavior only. Live model evaluations,
every possible technology tree, automated version research, browser UI, scaffolding,
engine/device/store acceptance and production audit services remain separate work.

## Status

Implemented: catalog and published JSON shapes, semantic validation, conditional
questions, 19 profiles, multiple deliverables, typed/provenanced answers, history,
dependency review, atomic state/summary writes, preview, resume, back/defer/N/A,
explicit conflict and CLI/host routing. The adoption bundle includes the runtime
and catalog so project-local snapshots remain self-contained.

Local verification on 2026-10-19: structure/link validation, generated-adapter
parity, all 67 regression tests (20 new wizard tests), eight canonical Skill Creator
validations and diff checks passed. Full test command:
`python -m unittest discover -s tests -v` on local Windows/Python 3.14.3.
The tests caught a redirected Windows Unicode-encoding issue during family
selection; explicit UTF-8 input/output was added and the full suite passed after
the correction. CI targets Python 3.11 on Windows and Linux and is inspected after push.

A real Windows PTY session used a synthetic Godot GDScript fixture: entered mixed
English/Arabic intent, chose web and Compatibility, deferred toolchain evidence,
quit and resumed at the deferred answer. JSON preserved Unicode and null/unknown
state. This is actual terminal engine behavior with synthetic decisions, not a
real game or live agent evaluation. Session/output logs are retained in the local
workspace's `work/wizard-runtime-acceptance/` folder; per-machine installation and
hosted CI results belong in the delivery report/receipt after publication.

Author self-review covered persistence failures, stale writers, hidden decisions,
unknown/custom choices and scope preservation. The initial Godot 4 C# web conflict
was rechecked against [official C# platform guidance](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/index.html)
on 2026-10-19. Older engine generations/custom profiles require separate
qualification; do not treat the starter rule as a universal cross-version resolver.
