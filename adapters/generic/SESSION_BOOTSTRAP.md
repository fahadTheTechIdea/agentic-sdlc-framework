# Bootstrap a ChatGPT or other assistant session

Provide the framework version and these files as readable attachments or
available repository files: `core/ENGINEERING_CONSTITUTION.md`,
`core/EVIDENCE_POLICY.md`, `skills/sdlc-orchestrator/SKILL.md`, and
`workflows/DELIVERY.md`. Add the target project's instructions, current tracker,
relevant specification and the handoff if one exists. Supply specialist skills
only when the orchestrator selects them. Include the target revision and changes.

The preferred user entry name is `sdlc-orch`. Its optional routing file is
`skills/sdlc-orch/SKILL.md`; include the canonical orchestrator procedure named
above as well when providing attachments to a session without repository access.

Suggested prompt:

> Use these Agentic SDLC Framework v1.2 files as project guidance within your
> host instructions. First confirm which project files you can actually read.
> My outcome is <outcome>, with constraints <constraints>. Inspect the existing
> implementation, choose the smallest sufficient workflow, and complete the
> authorized work with scoped evidence. If you cannot execute or edit, provide
> a proposal and exact checks to run; do not imply execution.

Repository instructions are not automatically imported into every chat. Do not
assume cross-session memory, local filesystem access, installed skills, tool
connections, user approvals or agent delegation carry over. Use
`templates/HANDOFF.md` to transfer current state and pending decisions.
