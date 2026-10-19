# Interactive project wizard

Python 3.11+; no package installation or browser server required. The same engine
works from Codex, Claude, a terminal, or noninteractive commands. The initial
catalog contains 19 decision profiles derived from the existing blueprints.
It collects decisions, not proof of current versions, working applications or
store eligibility. Broader inventory-only technologies still need their own trees.

## Start and resume

Run from the framework root (source checkout, installed snapshot, or the project's
`.agentic-framework` root). Replace the path with an existing application folder:

```text
python scripts/project_wizard.py profiles
python scripts/project_wizard.py start "C:\Projects\MyGame" --profile godot.csharp.game
python scripts/project_wizard.py start "C:\Projects\MyGame" --write --interactive
```

The first start previews without writing. The interactive command asks for a
project family/profile and saves `.sdlc/wizard.json` in the application folder.
Add `--mode existing` to perform bounded path-only inventory of existing project
manifests; it does not read their contents, infer versions or replace a stack.
Use `--name` for the project name and `--state` for a different state path.

```text
python scripts/project_wizard.py run "C:\Projects\MyGame\.sdlc\wizard.json"
python scripts/project_wizard.py show "C:\Projects\MyGame\.sdlc\wizard.json"
```

Each accepted answer is saved before the next prompt. Use `:back` to revisit an
answered question, `:skip` to defer it, `:review` for a summary, `:na REASON` for
allowed N/A decisions, and `:quit` to stop. EOF/Ctrl+C preserves accepted saves.
Choice questions accept a number, listed value or explicit custom text. Multiple
selections use commas. Custom selections are unqualified; describe constraints
in the remaining questions and verify them separately. Never enter secrets.

## Codex and Claude

Use `$sdlc-orch w` in Codex or `/sdlc-orch w` in Claude. The longer `wizard`
request also works; no exact sentence is required. The shortcut starts selection
or resumes the active project's existing state through the same procedure.
The host should inspect project instructions/pins first.
Use the chosen framework root to locate this script. If the host cannot expose
terminal input, it can ask the same relevant questions conversationally and save
answers through the commands below; do not claim a terminal ran when it did not.
Use the same state file for either host. Existing state is resumed, never overwritten.

For noninteractive operation, show JSON state and use exact node IDs from the
catalog/summary. `questions STATE --next` returns the next active unresolved prompt
and choices as JSON without writing; omit `--next` to collect unresolved questions
or use `--all` for every active question. Hosts can load the relevant prompts
without reading the whole catalog. `--value` accepts JSON; pass arguments as a
structured process argument list or a safe shell-quoted JSON string.

```text
python scripts/project_wizard.py show STATE --json
python scripts/project_wizard.py questions STATE --next
python scripts/project_wizard.py answer STATE L02.godot.csharp.game.variant --value '"compatibility"'
python scripts/project_wizard.py answer STATE L02.godot.csharp.game.versions --value null --reason "Toolchain not inspected"
python scripts/project_wizard.py add STATE backend --profile java.spring.api
python scripts/project_wizard.py profile STATE main --profile godot.gdscript.game
python scripts/project_wizard.py export STATE
python scripts/project_wizard.py export STATE --output NEW_DECISIONS.md --write
```

The quoted JSON example uses PowerShell/POSIX single-quote syntax; Windows cmd
users should use the interactive interface or their shell's JSON quoting rules.
Observed answers require `--origin observed --source FILE:LINE`; recommendations
and inferences retain their own origins. `--na --reason` records allowed N/A.
An answer command explicitly saves a decision. Start/export require `--write`;
export without it is a no-write preview. Export only creates a new file in an
existing folder; use its decisions to extend the project's active documents.

## State and compatibility boundaries

The versioned [catalog](../wizard/catalog.json) gives each profile independent
L01-L08 roots, conditional variant questions, dependencies and output bindings.
Game profiles also cover G01-G09. The [catalog schema](../wizard/catalog.schema.json)
and [session schema](../wizard/session.schema.json) describe JSON shape; runtime
validation in `scripts/wizard_core.py` additionally checks identities, root coverage,
references/cycles, conditions, values, provenance and profile revisions. The
standard-library runtime does not execute an external JSON Schema engine.

Answer changes invalidate transitive dependent answers, preserve their previous
values/history and leave unrelated decisions intact. Hidden answers remain
preserved for review and are excluded from resolved output. Profile switches
archive the previous deliverable and retain other deliverables. Profile-revision
mismatches fail explicitly; automatic catalog/state migration is not implemented.

Layer status is derived from decision state; source/build/store evidence stays
separate. The Godot C# starter follows the inspected Godot 4 path: its web-export
conflict is surfaced without silently changing language or target. Older engine
generations/custom profiles require separate qualification. Other combinations
require actual verification under
[technology policy](../core/TECHNOLOGY_FRESHNESS.md) and
[publishing policy](../core/PUBLISHING_REQUIREMENTS.md). The catalog is a starting
decision tree, not an exhaustive compatibility rules engine or an auto-updater.

## Persistence and reporting

State writes use a same-directory temporary file, flush/fsync, exclusive creation
for new files, and atomic replacement for updates. An exclusive cooperative lock
and loaded-content digest detect concurrent wizard writers/stale saves. This is
not a lock against arbitrary external editors or a multi-file transaction. A
crashed process may leave `.lock`/temporary files: inspect them and the last valid
JSON before removing abandoned files manually. Symlink/junction write paths are
refused. Invalid states, I/O failures and collisions report failure without a
success claim. Files are limited to 4 MiB, with history preserved until explicit
archival/migration outside this first runtime.

Scoped services use Python logging for boundary errors, session history for
attributable local decision changes (origin/source and timestamps, no authenticated
identity), and terminal messages for notifications. No email service, separate
server or graphical UI adapter is needed here. History is user-editable local
evidence, not a tamper-proof security audit log. The tool never logs answer payloads
as diagnostics. Session/export contents can contain project information; review
them before sharing or committing. No secrets scanner or encryption is implied.

No application scaffolding, installs, migrations, Git initialization, deployment,
browser UI, automated source research, store action or live model evaluation runs
from this wizard. Delivery intent is recorded and then passed to the normal SDLC
procedures within the user's existing authorization.
