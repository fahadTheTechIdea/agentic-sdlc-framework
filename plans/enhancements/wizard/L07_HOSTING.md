# L07: Hosting and operations

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Choose delivery/runtime environments from L01 constraints, L02 execution model and
L03-L06 service needs. Hosted servers, packaged apps, libraries and local tools
take different distribution branches.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L07.01 | Environments: local, test/staging, production, isolated/on-premises or custom | Identify which environments actually exist and their owners |
| L07.02 | Distribution: hosted service/site, static assets, app package, package registry, local executable | Match the selected profile; do not assume every deliverable is containerized |
| L07.03 | Runtime/topology: existing host, platform runtime, container, serverless, device/local process | Check selected framework/variant and provider capability before proposing deployment |
| L07.04 | Network, domain, TLS, reverse proxy, storage and managed dependencies | Record credential/account/hardware requirements without provisioning them |
| L07.05 | Configuration, secrets, environment separation and release mechanism | Use approved stores and CI; no embedded production secrets |
| L07.06 | Runtime signals, readiness, objectives and notification ownership | Hosted health/load/error signals versus desktop/device/local diagnostics |
| L07.07 | Capacity, continuity, backup/restore, migration/rollback and cost | Link L04 integrity/recovery needs; record realistic operational responsibility |
| L07.08 | Acceptance/distribution gates | Provider smoke, restart/recovery, package signing/device/store checks as applicable |

Each stack has a deployment tree. Blazor server-interactive and standalone browser
applications cannot be treated as the same hosting choice; Django opens its
WSGI/ASGI/static/media/runtime branches; a React-based project follows the chosen
framework's build/server requirements; Java, Go, desktop, mobile and packages follow
their own execution/distribution branches. Compatibility is checked, not assumed.

## Dependencies and change effects

L07 owns environments and operational objectives. Constraints flow back to L02
framework/runtime, L04 store/recovery, L05 security and L06 jobs/notification channels.
Changing deployment does not silently change the application architecture.

## Outputs and completion checks

Produce environment/distribution map, owners, resources, secret references, runtime
objectives, deployment/recovery plan and missing external gates. Resource estimates
remain assumptions until measured/quoted. Selecting a host grants no permission
to create resources, spend money or deploy.

## Reference and standards needs

Record vendor runtime/support/distribution guidance and operational requirements
for selected versions/targets. Exact current hosting support, pricing and signing/
store rules require separate current verification; none is asserted by this design.
