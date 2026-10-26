---
title: "Diagnostics and stop-state index"
capabilities: [compilation, execution, verification]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Diagnostics and stop-state index

Locate failures using actual exceptions, Harness rule IDs, and `RunState.status`. The previous page's E001–EC02 labels were explanatory categories; the current CLI output is authoritative.

| Identifier | Layer | Guidance |
| --- | --- | --- |
| `CompilationError` | Parsing, includes, generated syntax | [Unified compilation](part5_compiler.md) |
| Harness rule ID | Static budgets, tools, context constraints | [Harness](part2_harness.md) |
| `waiting_approval` | Paused execution | [Approval](runtime_approval.md) |
| `failed` | Provider, tool, or output validation | [Troubleshooting](troubleshooting.md) |
| `cancelled` | Cooperative cancellation | [Execution](runtime_execution.md) |
| `timed_out` | Total deadline | [Budgets](runtime_execution.md) |
| `budget_exhausted` | Model/tool/token limit | [Budgets](runtime_execution.md) |
| `CheckpointConflict` | Revision conflict | [Checkpoints](runtime_checkpoints.md) |
| `ToolOutcomeUnknown` | Uncertain side effect | [Unknown outcomes](runtime_checkpoints.md) |
| `pass/fail/skip/error` | `.nxintent` evidence status | [Verification](part2_harness.md) |

Preserve source path, line/column, original message, and run ID when presenting diagnostics. Results without source spans should show parsing errors without guessed navigation targets.

---

[Source and validation](capability_inventory.md) · `compilation` / `execution` / `verification`
