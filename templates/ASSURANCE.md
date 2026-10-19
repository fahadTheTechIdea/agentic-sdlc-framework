# Assurance matrix: <scope>

Revision/patch: <value>; environment: <value>; accountable owner: <person/role>
Apply [the quality, security and reliability rules](../core/QUALITY_SECURITY_RELIABILITY.md).
Extend existing project verification rather than creating a parallel checklist.
For each row record applicable or N/A with a reason; verified, failed or not_run;
actual command/scenario, output locator, limitations and the next action/owner.

| Area | Existing control / affected boundary | Required check and expected outcome | Status / evidence / gap / owner |
| --- | --- | --- | --- |
| Gates and test integrity | <CI/build/tests; baseline failures> | <regression before/after; test diff review; real UI/provider check> | <pending> |
| Agent evaluations | <changed skill/tool/model or N/A> | <selected cases; host/model/settings; actual transcript and diff; human rubric> | <pending> |
| Authorization | <shared policy; actor/action/resource/tenant> | <allowed, denied, guessed ID, cross-tenant; no UI-only control> | <pending> |
| Configuration / secrets | <schema/options/provider; safe diagnostics> | <missing/invalid values; startup/degraded mode; reload; redaction> | <pending> |
| Reliability | <timeouts/cancellation/retry/idempotency/transaction> | <duplicate/concurrent requests; lost response; timeout/cancel; actual provider> | <pending> |
| Recovery / migration | <backup; recovery objectives; migration compatibility> | <isolated restore, integrity, elapsed time; dry run; recovery path> | <pending> |
| Runtime health | <signals/objectives/readiness; alert owner> | <failure detection; tail latency/load; safe notification and recovery> | <pending> |
| Dependencies | <lockfile/inventory; verified registry/publisher/API/license> | <vulnerability/secret scans; scanner/database date; findings disposition> | <pending> |
| Agent trust / tools | <host-enforced scopes; tool-server provenance> | <untrusted instruction fixture; action trace; instruction/CI/test diffs> | <pending> |
| Publishing / distribution | <selected store/target/account scope or reasoned N/A> | <live policy/effective dates; actual artifact and console gates; PUBLISHING_READINESS.md> | <pending> |

## Gate disposition

<Separate pre-existing failures, introduced regressions, unavailable environments
and accepted exceptions. Link existing decisions with their actual authority.
No completion or release claim beyond the gates actually satisfied.>
