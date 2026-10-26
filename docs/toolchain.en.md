---
title: "Development toolchain"
capabilities: [ecosystem, cli, open_author, open_revisions, open_grants]
language_versions: ["3.0", "2.4"]
---

# Development toolchain

The Nexa 3.0 CLI, Nexa Code, and VS Code extension share native contracts, revisions, and acceptance rules. Tools display and orchestrate; the runtime decides authorization, CAS, and evidence. This page describes local source/install artifacts for Nexa Code `3.0.0.dev0` / Ink `3.0.0-dev.0` and extension `0.3.0`. Follow each repository's current build instructions for installation.

## CLI

Install Nexa 3.0.0 using [Quickstart](quickstart.md). Automatic checking of 3.0 files uses `check --json`; explicit build/run enters OCI and model resolution. Unversioned 2.4 files retain `validate`, `inspect`, and `agent`. See the [CLI reference](cli_reference.md).

## Nexa Code

[Nexa-Code](https://github.com/Nexa-Language/Nexa-Code) supplies a Python host and Ink/React terminal. Follow its installation guide for Python 3.10+, uv, Node.js 20+, and pnpm 10.18.3, then build Ink. Start from the Nexa-Code repository:

```sh
./nexa-cc.sh --cwd /absolute/project --program sum.nx --environment sum.environment.json --state .nexa/open-programs.sqlite3 --program-id sum-demo --max-model-calls 4 --max-tokens 20000 --timeout 120
```

`--program` explicitly opens the native Open Program interface; omitting it retains legacy Agent sessions. `--environment` selects reviewed configuration, with paths resolved from `--cwd`. `--docker-context` is optional. `uv run nexa-code-engine` exposes a JSON Lines host with the same flags. The terminal shows environment, budgets, goals/obligations, draft and active revisions, activities, evidence, and proposal diffs.

Code budgets apply to each explicit operation; `/build` and `/run` have separate accounting. `/build` builds and activates a revision. Create a new author draft with `/draft` before `/resolve`. `/sync` and `/approve` show the exact diff/proposal and require `y/n` confirmation.

Before build, execution, Author resolve, proposal inspection, grant, apply, and runtime resume, Code reloads configuration through the native environment loader and compares its semantic digest with the session binding. Changes to checkers, the image, capabilities, or provider bindings return `environment_changed`; missing or invalid files return `environment_unavailable`. JSON formatting or key order changes are allowed when semantics remain the same. After drift, restart Code with the reviewed environment, then rebuild and regenerate/review the relevant evidence. `/check`, `/status`, exact cancellation, and patch recovery remain available. These checks run before a new operation enters the runtime; inspect or cancel an existing activity using its exact ID.

Implemented native command forms follow. Obtain IDs from the actual current output:

```text
/check
/draft
/build
/locked
/status
/resolve total {}
/cancel author ACTIVITY_ID
/answer CLARIFICATION_ID Answer text
/sync SYNC_ID
/reject-sync SYNC_ID
/proposal PROPOSAL_ID
/approve PROPOSAL_ID local-operator
/apply PROPOSAL_ID GRANT_ID
/recover PROPOSAL_ID
/import repair.capsule.json
```

`/run <goal> [JSON]` executes a selected runtime goal. `/maintain {"paths":["calc.py"],"request":"Fix add"}` proposes repository maintenance; its JSON also accepts `event` and an imported `capsule_id`. `/revise` builds and activates a revision; `/resume` recovers the controller. `/cancel runtime ACTIVITY_ID` targets the exact runtime activity; author activities use `author`. Capsule `/export` accepts JSON with path, activity_id, source, creator, and license. Retained 2.4 `/permissions` and tool approvals govern legacy sessions; 3.0 Apply requires an exact grant.

Code source synchronization replaces only the intent string inside the target goal and checks the complete replacement ProgramIR. Other bytes remain intact, including LF/CRLF, comments, and valid parameters named `intent`. Existing `SourceSync` record formats and IDs remain compatible; a separate durable write-intent records the recovery directory before moving source. After process interruption, startup, `/check`, `/status`, and `/sync` recover filesystem stages. Completing the native revision still requires explicit `/sync` confirmation.

`/status` and the native panel expose `source_recovery` entries with `original_path`, `temporary_path`, `state`, and `sync_id`. Beside the source, `.nexa-intent-<id>/original` retains the original inode and subsequent writes from an editor that already had that inode open; it remains after successful synchronization. Keep these directories with the state database during recovery, review the original and current source, then continue synchronization. Recovery preserves existing user files. Manually archive recovery directories after the relevant editors are closed and retained edits have been saved or reconciled. An older interrupted write without a write-intent reports `source_recovery_required` and requires manual identification and restoration of the retained file.

## VS Code 0.3.0

The local [Nexa-extension](https://github.com/Nexa-Language/Nexa-extension) VSIX contains a minimal read-only Python SDK bridge. Development/packaging requires Node.js 22+ and pnpm; the VS Code API baseline is 1.96. Configure an explicit CLI and a Python interpreter containing Nexa 3.0.0 in the resource's workspace:

```json
{
  "nexa.executablePath": "/absolute/path/to/Nexa/.venv/bin/nexa",
  "nexa.executableArgs": [],
  "nexa.open.pythonPath": "/absolute/path/to/Nexa/.venv/bin/python",
  "nexa.open.pythonArgs": [],
  "nexa.open.environment": "sum.environment.json",
  "nexa.open.state": ".nexa/open-programs.sqlite3",
  "nexa.open.programId": "sum-demo",
  "nexa.open.maxModelCalls": 4,
  "nexa.open.maxTokens": 20000,
  "nexa.open.timeoutSeconds": 120
}
```

`nexa.open.pythonPath` must be explicit. Startup checks runtime version and capabilities. `pythonArgs` defaults to `[]`; the extension performs no shell expansion or automatic Python installation. Relative environment/state paths resolve from the resource's owning root in a multi-root workspace. Name environments `*.environment.json`; JSON schemas also match `*.nx.lock`, `*.capsule.json`, `*.program.json`, and `*.patch.json`.

| Setting | Default / purpose |
| --- | --- |
| `nexa.open.environment` | Empty; required for explicit build/resolve/run/apply |
| `nexa.open.state` | `.nexa/open-programs.sqlite3` |
| `nexa.open.programId` | Empty; falls back to the source file stem |
| `nexa.open.pythonPath` / `pythonArgs` | Empty / `[]`; explicit bridge interpreter and arguments |
| `nexa.open.capsule` | Empty; explicitly selects an imported capsule digest for run/maintenance |
| `nexa.open.dockerContext` | Empty; uses the Docker context |
| `nexa.open.maxModelCalls` / `maxTokens` / `timeoutSeconds` | `4` / `20000` / `120` seconds |

Existing `Nexa: Build` / `Nexa: Run` (`nexa.build` / `nexa.run`) route by language version. Find new commands in the Command Palette:

| Command ID | Title |
| --- | --- |
| `nexa.open.check` | Nexa: Check Open Program |
| `nexa.open.buildLocked` | Nexa: Build Locked Open Program |
| `nexa.open.resolve` | Nexa: Resolve Goal |
| `nexa.open.revise` | Nexa: Revise and Activate Program |
| `nexa.open.maintain` | Nexa: Maintain Repository |
| `nexa.open.status` | Nexa: Refresh Open Program Status |
| `nexa.open.cancel` | Nexa: Cancel Activity |
| `nexa.open.answer` | Nexa: Answer Clarification |
| `nexa.open.syncSource` | Nexa: Synchronize Clarification Source |
| `nexa.open.proposal` | Nexa: Review Exact Patch |
| `nexa.open.apply` | Nexa: Authorize and Apply Exact Patch |
| `nexa.open.recover` | Nexa: Recover Open Program or Patch |
| `nexa.open.resumeApply` | Nexa: Resume Exact Patch Application |
| `nexa.open.capsuleImport` | Nexa: Import Capsule |
| `nexa.open.capsuleExport` | Nexa: Export Activity Capsule |

3.0 diagnostics come from CheckReport and Outline uses actual ProgramIR spans. Automatic checks use a check client without a provider, make zero model requests, and execute no candidates. Restricted Mode provides static grammar and snippets only; trusting the workspace enables CLI/Author/bridge processes. Each process uses that resource's configuration, and late results are discarded after document changes or closure.

Explicit Author operations bind a private environment file snapshot. Before each actual RPC send, including when a queued request is dispatched, the extension checks the original configuration file's contents. Changed contents, replacement with different contents, or deletion invalidate the old client and reject that request. Review the current configuration, then explicitly start another Author operation to create a new client. This comparison uses file contents, so reformatting also requires rebinding. The check happens at the boundary for sending a new request; inspect activity state for the progress and outcome of requests already sent.

## State rules shared by both clients

Answering clarification creates a database child draft. The client reads the new IR and presents the target intent's source diff. After confirmation, it checks the source digest/document version, writes, checks again, and synchronizes with exact CAS. Conflicts, rejection, or exit preserve pending synchronization. Build/run from the old source waits for synchronization, including clarification initiated by another client.

Author and runtime activities are listed separately and cancellation uses the exact selected ID. Candidate acceptance, evidence validity, exact grants, and application outcomes are displayed separately. Review the actual diff before Apply. Handle expired state, file changes, or invalid evidence using the runtime's response. See [revision and recovery](open_revisions.md) for unknown effects.
