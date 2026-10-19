# L05: Users, identity and security

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Define trusted identities, permissions and data boundaries from L01 users/exposure,
L02 stack and L03/L04 interaction/data needs. No login UI does not mean no security:
local apps, workers, packages and APIs still have relevant trust boundaries.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L05.01 | Actors: anonymous, local OS user, registered users, external identity, service identities | Separate authentication source from permission authority |
| L05.02 | Accounts/session model and identity integration | Open framework-specific session/cookie/token/federation branches as applicable |
| L05.03 | Authorization: action/resource ownership, roles, attributes/relationships, existing policies | Deny protected operations by default; validate trusted entry paths |
| L05.04 | Single organization, multiple organizations/tenants, shared/public resources | Multi-tenant → scope resolution, data/UI/cache/export/notification isolation |
| L05.05 | Secrets, configuration, transport, keys and credential lifecycle | Store references only; no secret values in wizard/project evidence |
| L05.06 | Sensitive data, consent/retention obligations and threat boundaries | Record applicable jurisdiction/domain requirements as unknown until established |
| L05.07 | Negative/abuse cases and recovery | Expired identity, denied role, guessed ID, cross-tenant access and safe errors |

Trees follow the chosen ecosystem: ASP.NET Core authorization/identity integration,
Django's authentication/permission model, Java service security, native-mobile
credential/device boundaries and browser-to-API boundaries require different
questions. Optional third-party identity providers need their own integration
branch and compatibility evidence; no provider is silently installed.

## Dependencies and change effects

L05 owns access and tenant policy. L03 displays permitted experiences, L04 enforces
data ownership, L06 constrains event recipients and external credentials, and L07
defines deployment trust boundaries. Tenant/identity changes trigger those reviews.

## Outputs and completion checks

Produce actor/action/resource/tenant policy, identity/session choices, trust map,
secret references, privacy assumptions and negative tests in the current SDD and
assurance matrix. Check access is enforced beyond UI visibility and required
denied/allowed paths are named. Do not assert a security certification.

## Reference and standards needs

Record official framework security/session guidance, identity protocol/provider
references and applicable security requirements with version/context. Requirements
selection, implementation and runtime security verification remain distinct.
