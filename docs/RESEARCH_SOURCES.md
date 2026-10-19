# Source register

Reviewed 2026-10-19. These sources establish host file conventions; lifecycle,
SOLID review, RACI and evidence rules in this baseline are framework design
choices. They do not imply product certification or standards conformance.

| Source | Supported fact | Use here |
| --- | --- | --- |
| [OpenAI AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Codex discovers project instructions along the directory path; overrides can affect what loads | Root instruction adapter; verify effective instructions |
| [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) | Project skill discovery includes `.agents/skills`; skills use `SKILL.md` | Generated Codex wrappers |
| [Claude Code memory](https://code.claude.com/docs/en/memory) | Claude project guidance uses `CLAUDE.md` | Explicit shared-file routing |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | Project skills use `.claude/skills/<name>/SKILL.md` | Generated Claude wrappers |

Refresh host conventions before changing adapters. Installed versions, workspace
trust and organization settings can affect availability. Check live discovery
in each intended host rather than treating documentation as runtime evidence.
No external skills are vendored; canonical procedures here were authored for
this framework. Additional standards or compliance requirements need a separate
source-backed assessment for the target project.

CI uses GitHub-hosted runners and the official `actions/checkout` v4 and
`actions/setup-python` v5 actions. Their tag targets were read directly from
the official Git repositories on 2026-10-19 and pinned to immutable commits
in the workflow. Updating those pins is a reviewed dependency change; the
local Python tools themselves have no third-party package dependencies.

## Application operational services

Reviewed 2026-10-19. The requirement to provide Log, Audit and Notification Services
in every application, with a UI Notification Service for UI applications, comes
from the owner's direct instruction. The sources below support implementation
details; they do not mandate these service names or certify any application.

| Source | Supported guidance | Application here |
| --- | --- | --- |
| [OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | Deliberate event coverage, protected logging data and verification of logging failures | Coverage matrix, redaction and storage/failure checks |
| [Microsoft exception practices](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions) | Intentional exception handling and preservation of original exception information | No silent swallowing; explicit failure/recovery and owning reporting boundary |
| [OpenTelemetry log model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) | Structured records with event time, severity and optional trace correlation | Shared event envelope and propagated correlation |
| [Microsoft transactional outbox](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos) | Persist business state and outgoing event intent atomically, then relay events | Durable intent for operations requiring that guarantee; actual provider validation remains necessary |

The portable framework does not require Azure, a particular logging vendor or a
separate service deployment. Channel policy, UI integration, durable audit storage
and emergency diagnostic behavior must be designed and tested in each application.
