# P7 assurance verification

Scope: nine researched framework recommendations, routing/templates, safe adoption
of the added evaluation files and an executable six-case outcome grader.
Review: self-review only. No independent reviewer, live model evaluation or
application security/recovery/operational acceptance is claimed.

The [check records](checks.json) capture revision, timestamp, environment, commands,
exit status and raw output. They describe a dirty implementation tree based on the
recorded parent revision. [Source file hashes](source-files.json) and the captured
source-diff.patch identify the tested source; the evidence directory itself is
excluded from that digest to avoid circular evidence. Use the source file hashes
alongside the parent revision; a tracked diff alone omits newly created files.

| Requirement | Implementation | Verification |
| --- | --- | --- |
| All nine recommendations | Canonical assurance standard, existing constitution/standards, source register | Structure/link checks; self-review of rule-to-source mapping |
| Relevant procedure routing | Orchestrator, specification, architecture, implementation and verification; workflow/templates | Eight canonical skill validations; adapter parity |
| Outcome evaluation tools | Six disposable cases; prepare/grade CLI; protected fixtures and human rubric | 15 new grader tests, including negative submissions; 47 total tests |
| Preserve adoption behavior | Installer includes evals alongside existing snapshot paths | Existing Codex, Claude and generic adoption tests pass |
| Live agent behavior | Representative cases and evidence instructions supplied | Not run; tooling tests do not substitute |
| Application controls | Assurance matrix maps active controls to real checks | Not run in applications; no application code was modified |

The initial full regression exposed missing evaluation files in adopted snapshots.
The installer bundle was corrected and the full suite passed afterward. Final
checks and sanitized raw outputs accompany this file. Hosted CI is additional
evidence on the published commit; personal host discovery is stored in the local
installation receipt rather than presented as a repository-wide behavior result.

The first evidence-collection attempt also encountered a temporary broken link:
this document referenced checks.json before the collector had written it. The
[initial failed records](initial-failures.json) preserve those outputs. After the
record existed, structure/adoption/regression checks were rerun successfully;
the passing records are in checks.json. This was evidence-generation ordering,
not a suppressed test or weakened assertion.
