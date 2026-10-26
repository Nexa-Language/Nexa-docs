---
title: Design background
capabilities:
- compilation
- execution
- providers
- open_execution
language_versions:
- '3.0'
- '2.4'
---

# Design background

Beyond model calls, Agent applications need tool permissions, context, recovery, budgets, and output validation. Nexa places these boundaries in language declarations and run state, giving generated and handwritten programs a shared execution entry.

## Open Programs 3.0

OpenCompiler binds contracts to an environment, resolves implementations in a budget, and executes candidates in OCI. ProgramSession separates source drafts, activated revisions, runtime activities, proposals, and grants. Evidence is checked against current dependencies before acceptance or reuse.

## The retained 2.4 execution path

The unified compiler handles includes, ASTs, diagnostics, and Python output. AgentRunner handles providers, tools, and state transitions. SQLite checkpoints preserve progress and tool journals; native provider items preserve protocol continuity.

## Design trade-offs

Python retains integration with the AI tooling ecosystem. Rust AVM expands through shared fixtures. Recoverable execution needs enough history and durable results; uncertain effects need operator verification. External idempotency mechanisms can strengthen application guarantees.

Start with [Language basics](part1_basic.md) for program structure and [Runtime contracts](runtime_execution.md) for execution boundaries.

---

[Source and validation](capability_inventory.md) · `compilation` / `execution` / `providers`
