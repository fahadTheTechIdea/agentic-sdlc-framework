# ADR-0001: canonical portable core with generated host wrappers

Status: proposed; date: 2026-10-19.
Accountable decision role: repository owner; acceptance pending PR review.

## Context

The current request names Codex, Claude and cross-session use. Initial source
revision `02c5944` has no existing framework to extend. Duplicating policy per
host would create separate rules that can drift.

## Options

1. Write independent complete skill suites for each assistant: easy to load,
   but every policy change needs multiple edits and reviews.
2. Keep canonical skills and generate small discovery wrappers: adds a generation
   step, but keeps policy ownership in one place and permits parity checks.
3. Use one hosted orchestration service: adds credentials, runtime dependencies
   and operations beyond the requested baseline.

## Proposed decision

Use option 2. Canonical policy belongs in `core/`, procedures in `skills/`.
Root adapters and generated host wrappers route to those sources. Use Python's
standard library for validation and adoption to avoid runtime package setup.

## Consequences and verification

Discovery still depends on the host and its effective settings. A wrapper requires
the assistant to read a canonical file. Sync checks and mutation tests establish
file consistency; fresh Codex/Claude sessions and a real project pilot remain
separate acceptance gates. Adoption vendors a pinned snapshot and preserves
existing instructions. Updating installed snapshots is a deliberate reviewed diff.
