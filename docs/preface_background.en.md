---
title: "Design background"
capabilities: [compilation, execution, providers]
---

# Design background

Beyond model calls, Agent applications need tool permissions, context, recovery, budgets, and output validation. Nexa places these boundaries in language declarations and run state, giving generated and handwritten programs a shared execution entry.

## Source to execution

The unified compiler handles includes, ASTs, diagnostics, and Python output. AgentRunner handles providers, tools, and state transitions. SQLite checkpoints preserve progress and tool journals; native provider items preserve protocol continuity.

## Design trade-offs

Python retains integration with the AI tooling ecosystem. Rust AVM expands through shared fixtures. Recoverable execution needs enough history and durable results; uncertain effects need operator verification. External idempotency mechanisms can strengthen application guarantees.

Start with [Language basics](part1_basic.md) for program structure and [Runtime contracts](runtime_execution.md) for execution boundaries.

---

[Source and validation](capability_inventory.md) · `compilation` / `execution` / `providers`
