# Verification: <scope>

Revision: <full SHA>; working tree/patch digest: <value>; environment: <value>
Date/time with zone: <ISO timestamp>; reviewer: <name/role>; review type: <self/independent>

| Requirement | Implementation | Check/command | Exit/status | Output evidence | Limitations |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | <path> | <exact command/scenario> | <actual value/not run> | <locator> | <scope/gaps> |

## Review findings and disposition
<Actionable defects, severity, resolution or accepted risk and decision owner.>

## Operational service checks for application changes
<Link the completed OPERATIONAL_SERVICES.md matrix or equivalent. Verify shared
Log/Audit/Notification implementations and UI Notification Service if applicable;
no swallowed exceptions or false success; correlated/preserved causes and audit
outcomes; redaction, delivery failures/retries and UI isolation. Record actual
evidence and every unverified provider/coverage gate; headless UI needs an N/A reason.>

## Quality, security and reliability checks
<Link the completed ASSURANCE.md matrix or existing equivalent. Record required
gate commands/baselines, test modifications and reasons, applicable authorization,
config, retry/cancellation, restore, health and dependency checks. For agent behavior
record actual case runs separately from grader tests. Mark N/A and not_run honestly.>

## Completion assessment
<Met criteria, failed/missing gates, local/CI/runtime distinction, next action.>
