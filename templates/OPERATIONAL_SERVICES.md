# Operational services: <application or feature>

Use with [the logging, audit and notification standard](../core/LOGGING_AUDIT_NOTIFICATIONS.md).
Extend equivalent existing design/verification records instead of creating a
second service catalog. Values below are prompts, not implemented capabilities.

## Capabilities and reuse

| Capability | Existing contract and actual implementation path | Required addition/reuse | Owner | Verification evidence |
| --- | --- | --- | --- | --- |
| Log Service | <verified path> | <reuse/addition> | <role> | <pending/check> |
| Audit Service | <verified path> | <reuse/addition> | <role> | <pending/check> |
| Notification Service | <verified path> | <reuse/addition> | <role> | <pending/check> |
| UI Notification Service | <verified path or headless N/A reason> | <reuse/addition> | <role> | <pending/check> |

## Event coverage and destinations

Account for every module, entry point, worker and integration in the declared scope.

| Boundary/event | Actor/target/outcome | Log level | Durable audit requirement | Notification rule/channels | Coverage evidence or justified exclusion |
| --- | --- | --- | --- | --- | --- |
| <operation or event category> | <trusted attribution and results> | <level> | <store/guarantee> | <recipient/suppression policy> | <check/limitation> |

## Failure, data and delivery contracts

<Event IDs, UTC timestamps, correlation/trace context, exception owner and preserved
cause; explicit failure/cancellation/recovery outcomes; redaction, access, retention
and rotation; business/audit/outbox transaction boundaries; attempted versus committed
actions; emergency diagnostics; channel configuration and recipient authorization;
retry/deduplication/dead-letter policy; shutdown/restart and delivery status.>

## UI scope when applicable

<User/tenant/session lifetime, UI dispatcher, safe messages/reference IDs, severity
and progress, toast/banner/dialog/notification center, accessibility and persistence.
For headless applications, state N/A and explain why.>

## Acceptance scenarios

| Scenario | Required observable outcome | Actual check and evidence/status |
| --- | --- | --- |
| An application operation throws | Primary diagnostic record preserves cause/context; truthful result; related audit/notification policy applied | <pending> |
| An async worker fails or is cancelled | Failure is observed; cancellation is classified correctly; no false success | <pending> |
| A command succeeds, fails, is denied or rolls back | Audit outcome is attributable and matches what actually committed | <pending> |
| Audit persistence is unavailable | Protected action is blocked or declared durable evidence guarantee is met; no silent audit loss | <pending> |
| A notification provider is unavailable | Visible delivery state; bounded retries/final failure; other channels follow policy | <pending> |
| Delivery is retried or replayed | Deduplication/idempotency and audit integrity hold under the declared guarantee | <pending> |
| An event contains sensitive fields | Redaction applies before stores/channels; UI/email reveal only authorized safe details | <pending> |
| Logger/notification error reporting also fails | No recursive storm; emergency diagnostic/degraded health path is observable | <pending> |
| Two users or tenants receive UI events | Each sees only authorized notifications on the correct UI context | <pending or headless N/A reason> |
| Process restarts with pending durable work | Required audit/delivery intent survives and recovery behavior is verified | <pending or documented non-durable scope> |

## Completion and remaining gaps

<Implemented boundaries, reuse decisions, executed evidence, unverified providers/UI,
system-wide coverage limitations and concrete follow-up tasks. Do not mark a service
implemented because its interface, design, framework checklist or stub exists.>
