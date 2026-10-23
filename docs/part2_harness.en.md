---
title: "Harness execution primitives"
capabilities: [harness, verification, tools]
---

# Harness execution primitives

Harness organizes execution, tools, context, state, lifecycle, and verification as runtime constraints. Compiler diagnostics and execution semantics are checked separately.

| Primitive | 2.4 behavior |
| --- | --- |
| `autoloop` | Step/deadline limits; exact comparison of `exit_when` with the last assigned text or `status` field, ignoring surrounding whitespace and case |
| `with_context` | Exits on exceptions; trims Chat by whole user turns while preserving tool-call/result pairs |
| `snapshot` / `restore` | Deep-copy restoration of flow variables, Agent sessions, tool results, and provider state |
| `fork` / `merge` | Bounded execution, isolated sessions, stable result order |
| `verify` | A failed assertion stops the subsequent success path |
| `reflect` | Injects reflection text into later Agent input |
| Lifecycle hooks | Bound to model/tool events in the current flow, then removed when it exits |

`before_tool(name)` and `after_tool(name)` observe only the named tool. In `on_error(problem: Exception)`, `problem` receives the error-summary string stored in the event, suitable for logging. The hook preserves the run's failed status.

## Snapshot scope

This complete offline program restores the result to `3`.

```nexa
flow main {
    result = 3;
    point = snapshot();
    result = 9;
    restore(point);
}
```

The implementation uses deep copies; cost depends on state size. External file and service effects remain. Use [checkpoints](runtime_checkpoints.md) for durable run recovery.

## Executable verification

This complete offline program fails at type verification. `unexpected` is never returned successfully.

```nexa
flow main {
    result = 3;
    verify result satisfies string;
    result = "unexpected";
}
```

Deterministic predicates support types, numeric comparisons, containment, and length. Other semantic checks require an explicit evaluator. `.nxintent` uses `pass/fail/skip/error`; only `pass` counts as passing. Missing runtime, schema, or semantic evaluator produces `skip`; empty output fails, and evaluator exceptions produce `error`.

## Compiler diagnostic modes

`build`/`run` default to `--harness warn`; `harness-check` defaults to `strict`. `strict` errors block compilation, `warn` emits diagnostics, and `off` disables static Harness checks. The runtime continues enforcing tool approval and output validation.

---

[Source and validation](capability_inventory.md) · `harness` / `verification` / `tools`
