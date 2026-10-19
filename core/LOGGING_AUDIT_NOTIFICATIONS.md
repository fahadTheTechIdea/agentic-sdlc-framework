# Logging, audit, exception handling and notifications

These are mandatory application engineering practices requested by the owner.
They apply to new applications and to the affected boundaries of existing ones.
Reuse compliant services already present; create missing capabilities within the
authorized implementation scope. Record broader gaps in the active tracker.
Never claim system-wide coverage from a review of one feature.

## Required shared services

| Capability | Responsibility | Required scope |
| --- | --- | --- |
| Log Service | Structured operational diagnostics, exception reporting, correlation and configured sinks | Every application |
| Audit Service | Attributable, durable records of system actions and their outcomes | Every application |
| Notification Service | Policy-based routing of log, audit, business, progress and other notification events to configured channels | Every application |
| UI Notification Service | Safe, accessible, correctly scoped presentation of notifications to the application's users | Every application with a UI |

These names describe capabilities, not mandatory class names, separate deployments,
or a replacement for existing framework APIs. A shared Log and Audit Service may
expose distinct logging and audit contracts. Keep their purposes, retention and
access policies explicit. Reuse platform logging such as an existing .NET logger;
do not add a parallel logger or scatter direct provider calls throughout the code.
Use dependency injection or the project's existing composition mechanism.
Services must have working implementations: a no-op stub is not production support.

## System-wide coverage

Account for every application module, entry point, background job, integration
and UI boundary in an event coverage matrix. Record business commands, state
changes, lifecycle events, integration outcomes, validation failures, permission
decisions and exceptions through the shared services. Audit important reads,
exports, sensitive access, configuration/permission changes and destructive actions
with actor, target, operation and result. Include successful, failed and denied
actions; a failed or rolled-back command must never appear as a completed change.

"Audit everything" means accountable coverage of system activity, not dumping
every variable or confidential payload. Define each event category's destination,
detail level and rationale for exclusions. Do not silently omit a subsystem.
Verbosity controls may reduce routine diagnostics; mandatory audit events must
not disappear because debug logging or trace sampling is disabled.

## Structured event contracts

Every record needs a stable event name/ID, UTC occurrence time, severity/category
and originating component/operation. Use a common envelope for application/version,
environment, correlation/request ID and safe context. Audit records additionally
need trustworthy actor/service identity, target, action and outcome. Record an
explicit anonymous/system/unknown state when applicable instead of inventing identity.
Carry trace/span IDs when available; preserve correlation across jobs and channel
dispatch. Notification delivery records need their own ID, originating event ID,
channel, recipient scope and delivery/retry state. Treat client-supplied identity
as untrusted; authoritative audit attribution comes from the trusted boundary.

Redact secrets and sensitive data before persistence or dispatch. Restrict event
access and configure retention, storage limits/rotation and safe rendering.
Keep internal exception detail in appropriately protected diagnostic storage;
email and UI messages must not expose credentials, raw payloads or stack traces.
See the [source register](../docs/RESEARCH_SOURCES.md) for supporting guidance.

## Never swallow exceptions

- Do not use empty catch/except blocks, ignored task failures, blanket catch-and-
  continue, or an error converted into a success/null/default value without a
  documented result and observability path. Logging an error alone does not make
  a false success response acceptable.
- Catch when a boundary can recover, translate or terminate deliberately. Send
  the exception and safe operation/correlation context to the Log Service, record
  the associated business/security outcome through the Audit Service, and publish
  an appropriate notification through the Notification Service.
- Choose the boundary responsible for the primary diagnostic record. Intermediate
  layers can enrich and rethrow; do not emit the same exception at every layer.
  Preserve the original cause and stack when propagating or wrapping exceptions.
- Return an explicit failure, rethrow, compensate or use a documented recovery
  strategy. A fallback must report degraded/recovered state and never fabricate
  valid domain data. Retries need bounds, cancellation and eventual failure reporting.
- Treat expected cancellation, validation and absence as explicit outcomes at the
  appropriate severity; cancellation is not automatically an error alert. Observe
  asynchronous work through an owning task/worker; do not lose failures in
  untracked fire-and-forget work. Include startup and top-level UI/API/job handlers.

For language-specific behavior follow the installed framework's exception contract;
for .NET, consult [Microsoft's exception guidance](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions).

## Durable audit and honest failure handling

Protect audit records from ordinary application edits/deletions. Record corrections
as new attributable events. Choose access control, integrity protection, retention
and storage appropriate to the project; append-only does not by itself prove
tamper resistance or legal compliance.

For operations that require an atomic business change plus audit/notification
intent, use the existing transaction and durable outbox or an equivalent supported
mechanism. Publish committed events after commit. Record denied attempts and
rolled-back failures separately so rollback does not erase evidence of the attempt.
Specify the consistency guarantee and verify it on the actual storage provider.

Document what happens when logging, audit storage or delivery fails. Mandatory
audit failure must block the protected action or retain its evidence through a
durable mechanism that meets the declared guarantee. Ordinary diagnostic failure
may use a bounded fallback/degraded result, but must be visible. Do not recursively
call a broken logger or generate notification-failure alerts through the same
failing route without a circuit/attempt limit. Use a minimal independent emergency
diagnostic path and operator-visible health status where needed.

## Notification pipeline and channels

Route producers through the shared Notification Service rather than calling email,
file or UI providers directly. Support configurable channel adapters for email,
file output and UI presentation as needed by the application, plus other channels
through the same contract. Enable only channels with valid configuration and
authorized recipients; missing configuration is a visible delivery/configuration
state, not a successful send. This standard does not authorize sending messages
from a development agent or require all channels to be enabled at once.

Persist logs/audits in their required stores before treating notification delivery
as evidence of those records. The notification pipeline is an additional route,
not the sole copy of mandatory audit evidence. Apply category/severity rules,
recipient/tenant authorization, redaction and rate limits. Every event can be
accounted for without emailing or displaying a toast for every diagnostic entry.

For delivery that must survive process restart, use a durable queue/outbox with
bounded retries/backoff, idempotency/deduplication, dead-letter/replay handling,
ordering rules where required and visible failure state. Do not promise exactly-
once delivery without evidence. Avoid making a business request wait for SMTP
or a slow notification provider. Isolate channels so one failing channel cannot
silently discard the others; distinguish queued, delivered, failed and suppressed.
Use a simpler local pipeline when it satisfies the documented durability needs.

## UI notification service when a UI exists

Expose a UI-facing service for success, information, warning, error and progress
notifications. UI components consume this service instead of independently
building toasts/dialogs or accessing email/logging providers. Reuse existing
notification components and the host's UI dispatcher/thread model.

Map authorized events to user-safe messages and support appropriate toast/banner,
notification-center or dialog presentation. Preserve the full record in diagnostic
or audit storage and expose a safe reference ID when useful. Scope delivery and
service lifetime to the correct user, tenant and UI session; never broadcast
private errors or use shared mutable state that leaks one user's notifications.
Specify dismissal, persistence and accessibility behavior. Keep routine progress
nonblocking; use blocking dialogs only when the user must make a decision.
For headless applications mark UI notification as not applicable with a reason;
logging, audit and the Notification Service still apply.

## Design and verification gate

Complete [the operational service matrix](../templates/OPERATIONAL_SERVICES.md)
in the SDD or equivalent existing design. Identify actual implementation paths,
event coverage, storage, routing, failure policies, owners and checks. Add the
foundations to the first runnable application slice; extend them for later features.
For a limited existing-project fix, implement the affected integration and record
broader missing foundations rather than silently expanding the task.

Verify exception visibility and original cause, truthful failure results, durable
audit outcomes, channel routing/redaction, delivery failures and retry deduplication,
and correct UI user/tenant isolation when applicable. Test storage/provider failure
and shutdown/restart where the design promises durability. Source checks can flag
suspicious catch blocks; they do not prove system-wide coverage. Framework file
validation proves that this guidance is installed, not that an application
implements it. Record application-specific evidence and any unverified gate.
