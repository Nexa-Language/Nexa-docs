---
title: "CLI reference"
capabilities: [cli, compilation, checkpoint]
language_versions: ["3.0", "2.4"]
---

# CLI reference

The installed Nexa 3.0 CLI dispatches `build` and `run` using the source language declaration. The tables below separate Open Programs and the 2.4 compatibility path.

## Open Programs 3.0

| Command | Behavior |
| --- | --- |
| `nexa check FILE --json` | Offline native contract diagnostics and obligations |
| `nexa build FILE --environment ENV --state DB --json` | Build and accept an artifact using real OCI |
| `nexa build FILE --environment ENV --state DB --locked --json` | Revalidate the locked artifact, zero model generation requests |
| `nexa run FILE --environment ENV --state DB --program-id ID --goal GOAL --input INPUT.json --json` | Explicitly select a runtime goal and JSON inputs |
| `nexa run FILE --environment ENV --state DB --program-id ID --repository PATH --include FILE --request TEXT --json` | Repository maintenance proposal with evidence |
| `nexa author --environment ENV --state DB` | Author JSON-RPC 3.0 on stdio |
| `nexa open revise FILE --environment ENV --state DB --program-id ID --expected-revision REV` | Source CAS, build, and activation |
| `nexa open status ID --state DB` | Active RuntimeHead |
| `nexa open cancel ACTIVITY_ID --environment ENV --state DB` | Durable cancellation of the selected runtime activity |
| `nexa open resume ID --environment ENV --state DB` | Controller recovery with unknown-effect checks |
| `nexa open schema NAME` | Packaged 3.0 schema |

Build/run accept `--max-model-calls` (4), `--max-tokens` (20000), `--timeout` (120 seconds), `--docker-context`, and `--lock`. Run also accepts `--capsule`, `--event`, `--expected-revision`, and `--locked`. `--include` is repeatable. Default state is `.nexa/open-programs.sqlite3`; a build lock defaults to `FILE.nx.lock`. Environments are required for execution.

Use [patch authorization](open_grants.md) for evidence/approve/apply/recover, [capsules](open_capsules.md) for export/import, and [migration](migration_30.md) for inert 2.4 archives. Draft and active identities are separate; `open status` returns the active head, while full activities are read through the SDK. Source diagnostics and domain error codes should be retained in automation.

## 2.4 compatibility commands

## Compile and inspect

| Command | Behavior |
| --- | --- |
| `nexa --version` | Print runtime version |
| `nexa build FILE [--harness strict\|warn\|off]` | Write adjacent `.py` output; defaults to warn |
| `nexa run FILE [--harness strict\|warn\|off]` | Compile and execute; defaults to warn |
| `nexa inspect FILE [--format json\|text]` | Inspect through the shared module loader; defaults to JSON |
| `nexa validate FILE [--json] [--quiet]` | Report syntax and semantic diagnostics |
| `nexa harness-check FILE [--harness strict\|warn\|off] [--json]` | Harness checks; defaults to strict |
| `nexa lint FILE [--strict] [--warn-untyped]` | Gradual type checking |
| `nexa test FILE` | Compile and execute language tests |
| `nexa intent check FILE [--intent FILE] [--verbose]` | Intent checks using pass/fail/skip/error |
| `nexa intent coverage FILE [--intent FILE]` | Intent coverage report |

`build` returns `1` on compilation failure. `run` forwards the generated program's exit code and returns `130` on interruption. `validate` returns `1` for invalid programs; use it for scripted validity checks. `inspect` JSON is for structural consumers and may include diagnostic fallback data after parse failures. Its syntax-version metadata serves a different purpose from the runtime version printed by `nexa --version`.

`test` executes generated `test_` functions and returns `1` when any fail. With no test functions, it prints an informational message and returns `0`. When `--intent` is omitted, intent commands automatically locate the corresponding `.nxintent` file.

## Agent execution and resume

```sh
uv run nexa agent analyst.nx Analyst "Analyze evidence" --timeout 120 --max-tool-calls 4
uv run nexa agent analyst.nx Analyst --resume RUN_ID --approve CALL_ID
uv run nexa agent analyst.nx Analyst --resume RUN_ID --deny CALL_ID
```

Use the complete `analyst.nx` declaration from [Quickstart](quickstart_24.md). The first model call needs provider configuration. `RUN_ID` and `CALL_ID` come from that run's JSON output.

| Argument | Default and rules |
| --- | --- |
| `FILE NAME [TASK]` | File, Agent name, initial task; a new run requires TASK |
| `--checkpoint PATH` | `.nexa/runs.sqlite3` |
| `--resume RUN_ID` | Resume the original run, without new TASK text |
| `--approve CALL_ID` / `--deny CALL_ID` | Mutually exclusive, require resume |
| `--timeout SECONDS` | 300; resumed runs use their saved configuration |
| `--max-tool-calls COUNT` | 20; resume retains consumed budget |

JSON includes `run_id`, `status`, `output`, `error`, model/tool counts, input/output tokens, and `pending_calls`. Exit codes: completed `0`, waiting for approval `2`, other stops `1`. Use Python [continue_run](runtime_conversations.md) for a new conversation turn.

### Services and background jobs

| Command | Arguments, output, and effect |
| --- | --- |
| `nexa serve FILE [--port PORT]` | Compile and launch generated code; pass port override through `NEXA_PORT`; forward its exit code, or `130` for Ctrl+C |
| `nexa routes FILE [--json]` | List declared server routes; emit JSON per server, or an informational message when no server is declared |
| `nexa jobs list [--status STATUS] [--limit N]` | Tabular output, up to 50 rows by default; status choices: pending/running/completed/failed/dead/cancelled/expired |
| `nexa jobs status ID` | Print task status, or a not-found message |
| `nexa jobs cancel ID` | Attempt cancellation and print the result |
| `nexa jobs retry ID` | Move a dead-letter job back into pending |
| `nexa jobs clear` | Remove completed/expired/cancelled records and print the count |
| `nexa workers start FILE [--worker-id ID] [--poll-interval SECONDS]` | Compile and import job declarations before worker startup; defaults: ID `worker-1`, poll interval 1.0 seconds |
| `nexa workers status` | Print queue and worker status in the current process |
| `nexa cache clear` | Remove `.nexa_cache` in the current directory; print a message when absent |

The default queue backend is in memory. Sharing jobs across processes and persistence require configuring a suitable backend in the application. Business failures from `jobs status/cancel/retry` currently print messages without setting a nonzero exit code; automation must inspect the result or use the jobs API. Preserve original diagnostics and use [Troubleshooting](troubleshooting.md) to investigate failures.

---

[Source and validation](capability_inventory.md) · `cli` / `compilation` / `checkpoint`
