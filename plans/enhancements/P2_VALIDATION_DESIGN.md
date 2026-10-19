# Phase 2: executable validation and adoption — design

## Problem and goals
Instructions without checks can drift. Implement REQ-005 and REQ-006 with
standard-library Python tools and failure-oriented tests.

## API surface and files
- `scripts/validate_framework.py [--root PATH] [--evidence FILE] [--raci FILE]`:
  nonzero on structural/contract errors; never executes supplied evidence commands.
- `scripts/sync_adapters.py [--check]`: deterministic wrappers; check mode is read-only.
- `scripts/adopt.py TARGET --adapter codex|claude|generic [--write]`:
  preview by default; preflight all destinations and preserve existing instructions.
- `tests/`: temporary-repository tests for invalid artifacts, path boundaries,
  drift and installer collision behavior.
- `.github/workflows/validate.yml`: Windows/Linux validation and regression gates.

## Errors, compatibility and recovery
Readable diagnostics and nonzero exits for invalid input. Refuse path escape,
symlink destinations and overwrite collisions. No third-party dependencies or
shell command execution from records. Python 3.11+. Installation is preflighted
but is not a filesystem transaction; interrupted writes require inspection.

## Risks and checks
Shape validation cannot authenticate evidence or assess design quality. Document
supported Markdown link syntax and JSON contracts, and test meaningful failures.
Run full tooling regression and a disposable adoption smoke check. CI and live
host evidence must remain distinct from local test results.

## Execution order
1. Implement deterministic wrapper generation.
2. Implement structural/evidence/RACI validation.
3. Implement preview-first adoption with conflict checks.
4. Add negative tests and Windows/Linux CI; record scoped results.
