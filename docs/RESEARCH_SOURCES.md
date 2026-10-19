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
