---
title: "Troubleshooting"
capabilities: [compilation, execution, checkpoint, providers]
---

# Troubleshooting

Identify the failing layer, then retain the smallest useful reproduction. Include version, command, source location, run ID, and status while removing credentials and sensitive task data.

| Symptom | Check and action |
| --- | --- |
| Missing `nexa` command | Run `uv sync --locked` in the verified 2.4 checkout, then `uv run nexa --version` |
| Missing include | Resolve relative to the importing file, then check packaged standard-library paths |
| Parse failure | Run `nexa validate FILE --json` and fix the earliest source span |
| Strict Harness failure | Read the rule ID and supply budgets, tool constraints, or context contracts |
| Missing API key | Check configuration presence in the actual execution process; log only set/unset |
| Structured-output failure | Compare the schema and provider completion state; preserve a sanitized error |
| `waiting_approval` | Inspect pending tools and full arguments; explicitly approve or deny |
| `timed_out` | Include approval waits and resume gaps in elapsed wall time |
| `budget_exhausted` | Inspect call counts and usage; decide how to split the next turn |
| Checkpoint conflict | Stop the stale executor and load the latest revision before proceeding |
| Unknown tool outcome | Verify external effects before `resolve_tool`; see [recovery](runtime_checkpoints.md) |
| Actor missing await | Await all Actors before the flow returns |
| Native context limit | Shorten input or start an independent task while preserving opaque items |

## Reproduction material

Supply sanitized minimal `.nx` source, the exact version, command, diagnostic, and expected result. For documentation examples, add the example ID from the [inventory](capability_inventory.md). Keep `.nxs`, real checkpoints, and task-bearing artifacts out of issues.

Record compilation, offline fixture checks, and real-model acceptance separately. Include time and request scope for observations involving network services.

---

[Source and validation](capability_inventory.md) · `compilation` / `execution` / `checkpoint` / `providers`
