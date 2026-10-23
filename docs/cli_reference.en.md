---
title: "CLI reference"
capabilities: [cli, compilation, checkpoint]
---

# CLI reference

Use `uv run nexa` inside the local 2.4 checkout. `src/cli.py` defines the CLI; `src/agent_cli.py` implements durable Agent execution.

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

Use the complete `analyst.nx` declaration from [Quickstart](quickstart.md). The first model call needs provider configuration. `RUN_ID` and `CALL_ID` come from that run's JSON output.

| Argument | Default and rules |
| --- | --- |
| `FILE NAME [TASK]` | File, Agent name, initial task; a new run requires TASK |
| `--checkpoint PATH` | `.nexa/runs.sqlite3` |
| `--resume RUN_ID` | Resume the original run, without new TASK text |
| `--approve CALL_ID` / `--deny CALL_ID` | Mutually exclusive, require resume |
| `--timeout SECONDS` | 300; resumed runs use their saved configuration |
| `--max-tool-calls COUNT` | 20; resume retains consumed budget |

JSON includes `run_id`, `status`, `output`, `error`, model/tool counts, input/output tokens, and `pending_calls`. Exit codes: completed `0`, waiting for approval `2`, other stops `1`. Use Python [continue_run](runtime_conversations.md) for a new conversation turn.

## Services and background jobs

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
