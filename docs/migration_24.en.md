---
title: "Migrate to 2.4"
capabilities: [compilation, execution, conversations, harness, verification, rust]
---

# Migrate to 2.4

The migration baseline is the current local 2.4 development source. Preserve previous runtime data and source, then perform these checks in an isolated workspace.

## Compiler and interfaces

- Route embedded compilation through `src.compiler.compile_file` / `compile_source`; use returned `python_code`, `ast`, `sources`, and `diagnostics`.
- Includes resolve relative to their importing files. Cycles and missing files produce specific diagnostics.
- Declaration-only modules compile independently. Validate and compile complete programs before invoking models.
- Use `run` for direct output in a continuous instance session, `execute` for isolated inspectable runs, and [continue_run](runtime_conversations.md) for a new turn after a run ends.

## Execution changes

| Previous assumption | Migration action |
| --- | --- |
| Free-text substring checks in `exit_when` | Use a state value matching the final text or `status` exactly |
| Continue after ignored `verify`/structured-output failures | Fix conditions, schemas, or outputs and preserve failure paths |
| Automatically allow risky tools | Handle `waiting_approval` and explicit Boolean decisions |
| Treat `sandbox` as an annotation | Configure a real isolation executor or redesign the tool boundary |
| Treat flow snapshots as external transaction rollback | Design around deep-copy memory restoration and handle side effects separately |
| Assume a fixed cache hit rate | Reevaluate fresh tool-free Chat runs with complete cache keys |
| Assume full Rust/Python parity | Select a backend using the [Rust subset](runtime_rust.md) |

## Persistence and verification

Keep the source, Agent definition, provider, and working directory associated with checkpoints. Resolve unknown tool outcomes first. The deadline includes approval and resume gaps. A new run entry starts a new task budget; approvals do not carry across turns.

Count `.nxintent` `skip` and `error` outcomes separately; only `pass` passes. Inspect each example's `compiled` or `historical_drafts` classification in `examples/manifest.json` rather than inferring support from the directory version.

## Suggested acceptance sequence

1. Compile complete programs without credentials and inspect diagnostics.
2. Use fixed provider fixtures to check output, tools, side effects, and terminal states.
3. Test approval/denial, cross-process recovery, and unknown-outcome stops.
4. Test budgets, cancellation, timeouts, and a new conversation turn.
5. Select a provider, model, and budget before measuring real quality, cost, and latency.

---

[Source and validation](capability_inventory.md) · `compilation` / `execution` / `conversations` / `harness` / `verification` / `rust`
