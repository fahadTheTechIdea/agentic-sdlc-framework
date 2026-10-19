---
name: sdlc-implementation
description: Implement authorized software changes in coherent slices, preserving active contracts and adding relevant regression checks.
---

# Implement an authorized slice

Read the active specification/plan and affected code. Respect plan-only scope.
Inspect the branch and working tree; preserve unrelated user work. Extend the
existing implementation and public contracts unless an accepted decision changes
them. Verify unfamiliar APIs from installed source or authoritative versioned docs.

Implement the smallest coherent slice, including failure behavior and meaningful
checks at the boundary affected. Follow `core/ENGINEERING_STANDARDS.md`.
Run focused checks, then the project's required regression gate at the appropriate
phase. Update the tracker and `templates/VERIFICATION.md` from actual output.
If a gate fails, fix within scope or record the failure and missing decision.
Use the owner's authorized Git workflow: direct commits on the designated branch
when requested, or a feature branch/PR when appropriate and authorized. Do not
create branches or PRs contrary to project instructions. Do not merge or release
merely because implementation checks pass.
