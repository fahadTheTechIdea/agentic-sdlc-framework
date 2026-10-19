# L04: Data and persistence

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Define domain data, lifecycle and storage contracts from L01 workflows and L02
stack choices. A stateless component or library may have no owned persistence,
but still needs clear input/output contracts and data handling boundaries.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L04.01 | Owned data, caller-owned data, external read-only data, or no retained data | External/caller-owned → contract/provenance questions; no store invented |
| L04.02 | Entities, identifiers, relationships, units, time zones, null and retention meaning | Link sensitive fields and ownership to L05 |
| L04.03 | Store: relational, document, local embedded, files, object storage, existing service or custom | Choose engine/provider only through the matching stack/hosting compatibility branch |
| L04.04 | Framework-native access, existing repository/adapter, direct queries or external API | Reuse existing contracts; do not mandate another ORM or repository layer |
| L04.05 | Transactions, concurrency, consistency and duplicate/replay handling | Identify state + audit/event atomicity requirements and lost-response behavior |
| L04.06 | Offline use, cache, synchronization and conflicts | Offline/sync → define authority, reconciliation, invalidation and cancellation |
| L04.07 | Schema/data evolution, import/export and recovery | Define dry run, compatibility, backups, restore checks and irreversible changes |
| L04.08 | Data acceptance | Include integrity, unauthorized access, concurrency and provider-specific checks |

The data tree depends on the stack: Django models/migrations are a distinct branch;
a .NET backend may use its approved EF Core or existing data-access contracts;
a TypeScript service opens its selected library/provider tree; native mobile may
need local storage and synchronization. Browser clients consume authorized APIs
and must not inherit backend connection-string/secret choices.

## Dependencies and change effects

L04 owns domain and persistence decisions. L05 owns tenant/access policy, L06 owns
delivery contracts, L07 owns operational deployment. A provider, tenant or offline
change invalidates affected migrations, transactions, isolation and recovery checks.

## Outputs and completion checks

Produce the data model, provenance, storage/access choices, consistency/sync contract,
migration/recovery plan and check mapping in existing artifacts. Verify unknown
provider constraints are visible. An engine selection does not prove its migrations,
transaction boundaries or restore procedures have run.

## Reference and standards needs

Record official engine/provider, data-access/migration and recovery guidance plus
applicable retention/privacy obligations. Supported version combinations and
restore evidence must be verified in the target project later.
