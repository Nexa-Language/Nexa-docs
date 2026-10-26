---
title: Usage scenarios
capabilities:
- tools
- actors
- checkpoint
- open_language
- open_grants
language_versions:
- '3.0'
- '2.4'
---

# Usage scenarios

Choose execution structure from data flow, side effects, and recovery needs.

## Open Programs 3.0

Use typed goals and frozen output checks for bounded computations. For repository maintenance, use runtime Patch goals, controller-owned regression checks, exact grants, and recovery journals. See [Open Programs](open_programs.md) and [patch authorization](open_grants.md). The table below describes retained 2.4 integrations.

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
