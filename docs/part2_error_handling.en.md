---
title: "Error propagation and recovery"
capabilities: [language, execution, checkpoint]
---

# Error propagation and recovery

Language-level error handling manages local control flow. Runtime contracts govern durable state and uncertain side effects. Identify the failing layer before choosing a recovery entry.

| Mechanism | Purpose |
| --- | --- |
| `try` / `catch` | Catch exceptions within a statement scope |
| `try_agent` / `catch_correction` | Enter an explicit correction branch |
| `?` | Unwrap `NexaResult` and propagate failure |
| `otherwise` | Provide a local fallback for an error result |
| `defer` | Parser/scheduler support exists; generated programs currently fail, as detailed below |

## Complete correction example

```nexa
flow main {
    result = "before";
    try_agent {
        assert false;
    } catch_correction(e: Exception) {
        result = "corrected";
    }
}
```

The offline result is `corrected`. `NexaAgent.run_result()` returns an explicit `NexaResult` for Python callers. `execute()` returns a `RunState` with `status` and `error`.

## Failures with side effects

Raise `ToolOutcomeUnknown` when a tool sent a request but its outcome is uncertain. Returning an ordinary success string marks the result as known and changes recovery behavior. Preserve the checkpoint and let an operator verify the result before calling `resolve_tool`; see [unknown outcome recovery](runtime_checkpoints.md).

[Execution states](runtime_execution.md) distinguish budget exhaustion, cancellation, and timeout. Use [continue_run](runtime_conversations.md) for a new conversation turn.


## Current lowering limitations

The parser and standalone scheduler have `defer` tests. The complete program `flow main { defer print("closed"); result = 1; }` currently raises `name 'defer' is not defined`. Put critical resource cleanup in a trusted Python tool's `try/finally` until the generated path passes acceptance.

Flows with `requires` / `ensures` currently fail because generated `ContractClause` arguments do not match its constructor. Use executed `verify` checks, tool-argument schemas, and explicit error states for current task constraints.

---

[Source and validation](capability_inventory.md) · `language` / `execution` / `checkpoint`
