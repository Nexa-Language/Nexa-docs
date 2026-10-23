---
title: "Tool approval and resume"
capabilities: [tools, checkpoint]
---

# Tool approval and resume

The runtime only executes tools exposed by the Agent declaration. It validates JSON Schema, argument types, and extra fields first. `requires_approval` or high-risk tools enter `waiting_approval` and require an explicit Boolean decision.

## Declare an approval requirement

This complete declaration module returns reviewed text without writing to an external service. Its approval flow is the same as for a tool with side effects.

```nexa
@tool("Record reviewed text", requires_approval: true, risk_level: "high")
fn record_review(content: string): string {
    python! """return content"""
}

agent Reviewer uses record_review {
    prompt: "Prepare the review and request approval before recording it."
}
```

Save it as `review.nx`, configure a model, and start:

```sh
uv run nexa agent review.nx Reviewer "Review the supplied change" --timeout 900
```

## Decide on one call

1. Read `run_id` and `pending_calls` from the JSON output.
2. Review the tool name, full arguments, target, and expected side effects.
3. Decide using the pending call ID. Replace `RUN_ID` and `CALL_ID` with values from that output.

```sh
uv run nexa agent review.nx Reviewer --resume RUN_ID --approve CALL_ID
```

To deny the call:

```sh
uv run nexa agent review.nx Reviewer --resume RUN_ID --deny CALL_ID
```

Resume with the same source, Agent definition, provider, budgets, and working directory. `--resume` rejects new task text; a new task needs a new run entry. Waiting for a decision counts toward the total timeout.

## Approve through the SDK

```python
from src.runtime.checkpoints import SQLiteCheckpointStore

store = SQLiteCheckpointStore(".nexa/runs.sqlite3")
state = store.approve(run_id, call_id, approved=True)
state = agent.execute(state=state, save=store.save)
```

This fragment requires the same reconstructed `agent` and reviewed `run_id` and `call_id`. `approved` must be `True` or `False`. Server annotations, strings, and truthy objects do not authorize execution.

## Isolation and unknown outcomes

`sandbox: true` requires a real isolation backend and fails when one is unavailable. Ordinary Python tools record `sandboxed=false`. When a request was sent but its outcome is unknown, verify the actual side effect using [checkpoint recovery](runtime_checkpoints.md).

---

[Source and validation](capability_inventory.md) · `tools` / `checkpoint`
