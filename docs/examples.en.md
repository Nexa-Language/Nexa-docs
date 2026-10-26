---
title: "Verified examples"
capabilities: [compilation, harness, tools, actors]
language_versions: ["3.0", "2.4"]
---

# Verified examples

The inventory distinguishes native 3.0 checks, actual OCI scenarios, and the retained 2.4 compatibility examples. Full counts and verification rules are in [capability evidence](capability_inventory.md).

## Open Programs 3.0

| Program | Actual verification |
| --- | --- |
| [Answer](quickstart.md) | Native check, OCI output `42`, passing evidence, zero-request locked replay |
| [Sum](open_programs.md) | Native check, fixture proposal and review, OCI output `0`, frozen sum cases, zero-request locked replay |
| [Homepage](index.md) | Native contract check only; no model or OCI execution during check |

## 2.4 compatibility examples

| Topic | Example | Documentation check |
| --- | --- | --- |
| Arithmetic and variables | [First program](quickstart_24.md) | Compile + offline result `12` |
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

`examples/manifest.json` classifies every main-repository `.nx` file as `compiled`, `open_programs`, or a specific `historical_drafts` reason. A compiled example may still need a model, files, an MCP service, or other execution prerequisites. Check those requirements when selecting a program.

This site's [inventory.json](inventory.json) records a SHA-256, page, block index, validation mode, and fixture for every documentation block. `partial`/`historical` entries require individual reasons visible on the page. Unregistered or changed blocks fail validation.

---

[Source and validation](capability_inventory.md) · `compilation` / `harness` / `tools` / `actors`
