---
title: "Verified examples"
capabilities: [compilation, harness, tools, actors]
---

# Verified examples

Use these complete programs to enter each topic. Every block compiles independently. Programs marked for offline execution also check results against fixed fixtures. Model quality is evaluated separately.

| Topic | Example | Documentation check |
| --- | --- | --- |
| Arithmetic and variables | [First program](quickstart.md) | Compile + offline result `12` |
| Model call | [Echo](part1_basic.md) | Compile + fixed reply `hello` |
| Sequential pipeline | [Researcher → Summarizer](part2_advanced.md) | Compile + two fixed replies |
| Real local tool | [add](part3_extensions.md) | Compile + tool execution + result `5` |
| Protocol | [Answer](part3_extensions.md) | Compile + structured result |
| Flow snapshot | [snapshot/restore](part2_harness.md) | Compile + restored result `3` |
| Failed verification | [verify](part2_harness.md) | Compile + expected failure |
| Actor mailbox | [spawn/pass/await](runtime_actors.md) | Compile + two inputs and final result |
| Pattern matching | [match](part2_pattern_matching.md) | Compile + result `one` |
| Shared Rust subset | [Division](runtime_rust.md) | Python offline result `2.5`; Rust provenance in shared fixtures |

## Main repository example status

`examples/manifest.json` classifies every main-repository `.nx` file as `compiled` or records a specific `historical_drafts` reason. A compiled example may still need a model, files, an MCP service, or other execution prerequisites. Check those requirements when selecting a program.

This site's [inventory.json](inventory.json) records a SHA-256, page, block index, validation mode, and fixture for every documentation block. `partial`/`historical` entries require individual reasons visible on the page. Unregistered or changed blocks fail validation.

---

[Source and validation](capability_inventory.md) · `compilation` / `harness` / `tools` / `actors`
