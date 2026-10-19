# L06: Integrations and shared services

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Map existing and required capabilities from L01 workflows, L02 framework and
L03-L05 UI/data/access decisions. Shared Log, Audit and Notification capabilities
follow the existing operational standard even without external integrations.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L06.01 | Existing shared services and contracts versus missing foundations | Inventory/reuse before proposing classes, libraries or deployments |
| L06.02 | Shared Log Service: events, severity, correlation, redaction, ownership | Choose ecosystem-native adapters and independent emergency diagnostics |
| L06.03 | Shared Audit Service: business/security coverage, durability and retention | Link transactional guarantees to L04 and access to L05 |
| L06.04 | Shared Notification Service: email, file, UI or other requested channels | Define routing, recipient authorization, delivery status and noise policy |
| L06.05 | UI Notification Service adapter when a visual UI exists | Resolve framework-specific lifetime/dispatch/state; headless → reasoned N/A |
| L06.06 | External APIs, events, files, identity, payments or custom integrations | Each provider opens contract, credential, sandbox and failure branches |
| L06.07 | Background/scheduled work, queues and durable delivery | Distinguish in-process scheduling from durability/independent-worker needs |
| L06.08 | Reliability and acceptance | Timeouts, cancellation, bounded retries, deduplication, outbox/dead letters when justified |

Technology-specific branches select implementation mechanisms, not duplicate policy:
a .NET server profile maps existing hosted services/reporting adapters; a Django
profile maps existing logging/audit, request/task and notification contracts; a
browser client needs safe server APIs and UI feedback; desktop/mobile profiles
need their own dispatch, offline queue and user/session lifetime handling.
A queue, vendor or separate service is not automatically required.

## Dependencies and change effects

L06 owns capability/provider contracts; L03 owns UI behavior, L04 transaction state,
L05 recipient/tenant policy, L07 operational hosting. Changing channels or job
durability revisits those constraints and L08 failure-path tests.

## Outputs and completion checks

Fill the existing operational-services matrix with real reused/proposed contracts,
event coverage, exception owners, channel choices and failure behavior. Every error
path preserves the cause and a truthful outcome; no catch/except branch silently
claims success. List untested providers and legacy gaps rather than hiding them.

## Reference and standards needs

Record ecosystem reporting APIs, queue/provider contracts and delivery guarantees
from official sources for selected versions. Existing framework logging/audit/
notification and assurance standards remain the canonical requirements.
