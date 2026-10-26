---
title: "Checkpoints and unknown outcomes"
capabilities: [checkpoint, tools]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Checkpoints and unknown outcomes

A SQLite checkpoint stores `RunState`: configuration, conversation, provider items, usage, approvals, and the tool journal. Transactions and an incrementing `revision` detect concurrent writes. An executor saving a stale revision raises `CheckpointConflict`.

## Save and load

This Python fragment requires an existing, configured `agent`.

```python
from src.runtime.checkpoints import SQLiteCheckpointStore

store = SQLiteCheckpointStore(".nexa/runs.sqlite3")
state = agent.execute("Inspect the workspace", save=store.save)
restored = store.load(state.run_id)
state = agent.execute(state=restored, save=store.save)
```

Across processes, rebuild the same Agent definition in the original working directory using the original program and provider configuration. The CLI also checks the hash of compiled output, so source or include changes prevent resume.

## Three journal stages

| Durable state | Recovery behavior |
| --- | --- |
| Call has not started | Apply budget and approval policy before execution |
| `started`, result not saved | Stop with an unknown outcome for operator verification |
| `completed`, result saved | Reuse the result and finish assembling messages without executing again |

Tool results are saved before provider messages are appended. File, database, or service side effects can precede a checkpoint write. Idempotency keys in the external system can further reduce duplication risk.

## Resolve an unknown outcome

Network timeouts, disconnected transports, stream reading or decoding failures, shell timeouts, and MCP disconnects can leave unknown outcomes. Custom tools should raise `ToolOutcomeUnknown` to preserve this fact. If a tool swallows the exception, the runtime sees only the value it returns.

1. Preserve the checkpoint and external logs.
2. Verify the actual result from the tool name, arguments, and external records.
3. Once verified, write the real output and success flag into the journal.
4. Rebuild the same Agent and resume.

```python
state = store.resolve_tool(
    run_id,
    call_id,
    "Operator-verified result from the external system",
    success=True,
)
state = agent.execute(state=state, save=store.save)
```

This fragment requires verified `run_id` and `call_id` values and the original `store` and `agent`. `resolve_tool` accepts only a pending call whose journal entry remains `started`.

## Data management

Checkpoints, traces, and [artifacts](runtime_artifacts.md) may contain task data. Apply the project's access policy and keep default `.nexa` runtime data in Git ignore. Durable checkpoints preserve runs across processes; [flow snapshots](part2_harness.md) restore the current flow's in-memory state.

---

[Source and validation](capability_inventory.md) · `checkpoint` / `tools`
