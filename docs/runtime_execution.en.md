---
title: "Execution, budgets, and cancellation"
capabilities: [execution]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Execution, budgets, and cancellation

`NexaAgent.execute()` creates an isolated session and returns `RunState`; `aexecute()` is its asynchronous adapter. `run()` preserves a continuous session on the same instance and returns output directly. Calls on that instance are serialized.

## Configure a run

This Python example requires model configuration. Budgets apply to one `execute` run; resuming retains saved limits and usage.

```python
from src.runtime.agent import NexaAgent
from src.runtime.run_state import RunConfig

agent = NexaAgent("Analyst", prompt="Work from evidence")
state = agent.execute("Explain the findings", config=RunConfig(
    timeout=120,
    max_model_calls=8,
    max_tool_calls=4,
    max_tokens=12000,
))
print(state.status.value, state.output, state.error)
```

| Field | Default | Meaning |
| --- | --- | --- |
| `timeout` | 30 seconds | Wall-clock deadline, including approval waits and time before resume |
| `max_model_calls` | 20 | Model requests, including retries |
| `max_tool_calls` | 10 | Individual tool executions |
| `max_tokens` | `None` | Cumulative input and output usage limit |
| `retries` | 2 | Separate limits for transient retries per provider request and structured-output corrections across the run |
| `max_tool_output_chars` | 16000 | Inline tool-output character threshold, minimum 256 |
| `artifact_directory` | `.nexa/artifacts` | Content-addressed storage for large tool outputs |

The `nexa agent` CLI explicitly passes a 300-second timeout and a 20-tool budget by default; these differ from SDK defaults above.

## Act on the returned state

| Status | Meaning | Next action |
| --- | --- | --- |
| `running` | Execution is active | Consume events or wait |
| `waiting_approval` | A tool needs an explicit decision | Inspect `pending_calls`, then approve or deny |
| `completed` | Output validation completed | Read `output` |
| `failed` | Provider, tool, protocol, or validation failure | Read `error` and the journal; resolve unknown side effects first |
| `cancelled` | Cancellation was observed | Inspect effects that already completed |
| `timed_out` | Total deadline exhausted | Inspect state before configuring a new task |
| `budget_exhausted` | Call or token budget exhausted | Review usage before deciding what follows |

Token accounting uses provider usage. When `max_tokens` is configured and usage is missing, the run fails explicitly. Actual input cost is known after the request returns; exceeding the cumulative budget prevents subsequent requests.

For malformed JSON, Protocol, or schema output, the runtime appends correction requests within the `retries` limit and retains completed tool results. Correction counts persist in checkpoints, so approval resume uses the remaining allowance. Every attempt counts toward model, token, and deadline budgets. Correction messages belong to the original user turn, and `ensures` still receives that turn's original input. Failed `ensures` or `verify` checks terminate immediately.

Once the tool budget is used, subsequent model requests omit tools so the model can give a final answer from existing results. The execution boundary still rejects additional tool calls beyond the allowance.

## Cancellation and parallel work

Pass a `threading.Event` as `execute(cancel=event)` and call `event.set()` to request cancellation. The runtime checks cooperatively at model, streaming, and tool boundaries. An arbitrary Python tool already running must provide its own cancellation behavior. Provider request timeouts use the remaining deadline.

Parallel orchestration creates isolated sessions, defaults to at most 8 concurrent tasks, and preserves input order in results. Repeated Actor messages follow [Actor lifecycle](runtime_actors.md) accounting. See [checkpoints](runtime_checkpoints.md) for persistence.

---

[Source and validation](capability_inventory.md) · `execution`
