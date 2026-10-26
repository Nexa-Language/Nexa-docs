---
title: "Actor lifecycle"
capabilities: [actors, execution]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Actor lifecycle

A flow owns the Actors it creates. Each Actor has an isolated Agent session and a sequential mailbox. Later messages retain its history and accumulate model/tool usage and the total deadline.

## Spawn, send, and join

Configure a model, save this program as `actor.nx`, and run `uv run nexa run actor.nx`. Worker processes both messages in order; the second message can use the first turn’s history. The flow returns the second reply.

```nexa
agent Worker {
    prompt: "Process messages in order and retain prior context."
}

flow main {
    worker = spawn Worker("Inspect the evidence");
    pass "Summarize the evidence" to worker;
    result = await worker;
}
```

`spawn` starts an Actor, `pass` queues another input, and `await` closes its mailbox and returns the last result. A flow allows up to 8 active Actors at once. Awaited Actors release their concurrency slots.

## Completion and failure

Every Actor must be awaited before its flow returns. On a flow exception or missing await, the runtime cancels remaining work, waits for its threads, and reports failure. Tool cancellation still follows the [cooperative cancellation](runtime_execution.md) contract.

Model Actors consume their mailboxes automatically. Standalone `receive()` requires a custom message handler and currently raises an explicit error on the language runtime path. Actor sessions live within one flow; use `execute()` or `nexa agent` for cross-process approval and recovery.

Separate Actors suit parallel work, while successive messages to one Actor suit ordered tasks. For bounded parallel work followed by aggregation, see [fork/merge](part2_advanced.md).

---

[Source and validation](capability_inventory.md) · `actors` / `execution`
