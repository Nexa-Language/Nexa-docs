---
title: "Usage scenarios"
capabilities: [tools, actors, checkpoint]
---

# Usage scenarios

Choose execution structure from data flow, side effects, and recovery needs.

| Scenario | Suggested structure | Acceptance focus |
| --- | --- | --- |
| Evidence and reports | Sequential Agents + Protocol | Output schema, factual sources, completeness |
| Compare approaches | Isolated sessions + fork/merge | Concurrency bound, ordering, selection criteria |
| Staged research | Sequential Actor mailbox | Retained history, cumulative budgets, await |
| File repair | Scoped tools + approval + checkpoints | Write targets, allow/deny, recovery, unknown effects |
| Service integration | MCP or custom tools | Schemas, authorization, timeout, cleanup |

The [toolchain](toolchain.md) provides coding-task entry points. [Verified examples](examples.md) provide small complete programs. Evaluate task quality, cost, and latency with the selected model.

---

[Source and validation](capability_inventory.md) · `tools` / `actors` / `checkpoint`
