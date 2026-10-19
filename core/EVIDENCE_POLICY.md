# Evidence policy

## Claim classes

- **Observed:** directly inspected source or tool output, with a locator and scope.
- **Inferred:** reasoned from named observations; state the reasoning and uncertainty.
- **Proposed:** a recommendation or intended future behavior.
- **Unknown:** unavailable or not yet checked; state what would resolve it.

Use the narrowest supported claim. Source code can establish what is written;
execution establishes what occurred in that environment. Passing checks on an
earlier revision cannot certify later changes. Record the tested revision,
dirty-tree state or patch digest when applicable, timestamp with time zone,
environment, exact command, exit status, output locator and covered criteria.
Never relabel a skipped, unavailable or failing check as passed.

For third-party claims use authoritative sources, retrieval dates, version and
relevant sections. Distinguish source content from framework recommendations.
Repository observations should include revision and path (line if useful).
Prior chat claims and generated summaries require current verification where
material. Say when the original content could not be recovered.

## Verification records

`templates/EVIDENCE.json` defines the supported record shape. The executable
validator accepts `verified`, `failed`, and `not_run` check statuses. A verified
record requires exit code 0 and an existing local output file; a failed record
requires a nonzero exit code and output. Executed records need a full commit
SHA, command, timestamp with time zone, environment and scope. Dirty changes
belong in the scope, along with a patch digest or other reproducible locator.
`not_run` requires a reason in limitations and may use null execution fields.

This structural validation does not authenticate logs, execute commands, inspect
the truth of claims, or enforce a release decision. Never make up a passing
record to satisfy it. Store sanitized logs under `evidence/` or an approved CI
artifact location. Only local output paths inside the evidence record's project
root are supported by the validator; download CI evidence deliberately if needed.

## Completion and resumption

Map each acceptance criterion to evidence and unresolved limitations in
`templates/VERIFICATION.md`. If a required check fails, fix within scope or
report the failed gate; do not hide it behind unrelated passing tests.
Handoffs must identify revision, working-tree changes, observed progress,
decisions, pending questions, exact next action and remaining checks.
Reinspect repository state on resume. A previous session's memory is context,
not proof of current completion.
