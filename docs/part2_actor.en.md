---
title: "Actor syntax and usage"
capabilities: [actors]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Actor syntax and usage

Actors use `spawn`, `pass`, and `await` to express concurrent workers and mailboxes. See [Actor lifecycle](runtime_actors.md) for ownership, concurrency limits, and accounting.

| Syntax | Meaning |
| --- | --- |
| `worker = spawn Agent("task");` | Create an isolated Agent session owned by this flow |
| `pass "next" to worker;` | Queue another input in the Actor's sequential mailbox |
| `result = await worker;` | Close the mailbox, wait, and return the final result |

Successive messages suit staged analysis of one task. Create multiple Actors for independent work, and await each before returning from the flow. On failure, the runtime cancels remaining tasks and waits for their threads.

Standalone `receive()` from older designs requires a custom message handler; model Actors consume their mailboxes automatically. Use [durable runs](runtime_checkpoints.md) across processes.

---

[Source and validation](capability_inventory.md) · `actors`
