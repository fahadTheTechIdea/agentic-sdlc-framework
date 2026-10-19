---
name: sdlc-architecture
description: Assess software boundaries and SOLID tradeoffs, and record consequential architecture choices in ADRs.
---

# Architecture and SOLID

Read `core/ENGINEERING_STANDARDS.md`; inspect existing shared abstractions and
callers. Prefer reuse over parallel models. Identify the reason each boundary
exists and how failures, concurrency, authorization and transactions cross it.

Compare realistic alternatives and their consequences. Use `templates/ADR.md`
for costly, hard-to-reverse or cross-module decisions; include status, owner,
evidence, supersession and verification. An agent recommendation is proposed
until an authorized decision-maker accepts it. Check substitutability with
behavioral contracts where implementations are interchangeable. Do not add
interfaces, services or patterns solely to tick a SOLID checkbox.
