---
title: "Conversation turns and continuation"
capabilities: [conversations, checkpoint, providers]
---

# Conversation turns and continuation

`continue_run` starts a new task turn from a finished run. It preserves settled history and provider state while resetting usage, deadlines, and approvals. `execute(state=...)` resumes the original run.

## Choose an entry

| Need | Entry | Run identity and budget |
| --- | --- | --- |
| Start an independent task | `execute("task")` | New ID, session, and budget |
| Resume the original interrupted/approval run | `execute(state=state)` | Original ID, configuration, usage, and deadline |
| Continue conversation from a finished task | `continue_run(previous, "next")` | New ID, budget, and approvals with retained history |

## Two conversation turns

This complete Python usage example requires configured provider access for execution.

```python
from src.runtime.agent import NexaAgent
from src.runtime.checkpoints import SQLiteCheckpointStore
from src.runtime.run_state import RunConfig

agent = NexaAgent("Analyst", prompt="Work from evidence")
store = SQLiteCheckpointStore(".nexa/runs.sqlite3")
first = agent.execute("Analyze the evidence", config=RunConfig(timeout=120), save=store.save)
if first.success:
    second = agent.continue_run(first, "Summarize the conclusion", save=store.save)
    print(second.run_id, second.status.value)
```

`continue_run(previous, *args, config=None, cancel=None, save=None, on_event=None, on_text=None, provider=None)` returns `RunState`. Without an explicit `config`, it reuses configuration values from the previous run and starts with zero usage and a new start time. The previous state object remains unchanged.

`metadata.parent_run_id` points to the preceding turn and `metadata.session_id` links the conversation. Events use the new `run_id`. Native Responses/Anthropic opaque items and cursors are retained.

## Checks before continuation

- Resume or cancel `running` and `waiting_approval` runs first.
- Unknown tool outcomes block continuation; resolve them with the [recovery guide](runtime_checkpoints.md).
- Saved tool results complete history from the journal. Unstarted calls receive cancellation results to close protocol pairs; completed side effects are not replayed.
- Input must be nonempty. Agent definition, model, provider, and working directory must still match.
- Retain the original artifact directory when overriding configuration so earlier history can still read its large tool results.
- Earlier approvals do not authorize a new turn. Risky tools require another approval.

Settled `completed`, `failed`, `cancelled`, `timed_out`, and `budget_exhausted` states can continue after these checks. CLI `nexa agent --resume` still resumes the original run; the Python API provides the new-turn entry.

---

[Source and validation](capability_inventory.md) · `conversations` / `checkpoint` / `providers`
