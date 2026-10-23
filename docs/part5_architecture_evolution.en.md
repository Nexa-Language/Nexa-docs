---
title: "Architecture evolution and experiments"
capabilities: [rust, harness, cache]
---

# Architecture evolution and experiments

The current system uses the Python reference runtime for the full language path. Rust AVM expands through shared semantic cases. See [Rust/WASM](runtime_rust.md) for the implemented scope.

## Implemented evolution

- The CLI, SDK, and API share compilation and include loading.
- Native providers preserve their protocol state.
- `RunState`, budgets, approvals, SQLite journals, and artifacts form an inspectable execution path.
- Flow snapshots restore in-memory state through deep copies.
- Rust supports declarations, basic computation, and Agent calls; the WASM feature uses Wasmtime 48.

## Historical designs and research

Earlier designs proposed COW snapshots, a complete Rust runtime, virtual-memory paging, and distributed execution. These remain research or planning directions until backed by implementation and acceptance evidence. Current flow snapshots use deep copies; exact response caching is limited to fresh Chat runs without tools.

Extend shared semantic fixtures before broadening backend support, then define resource boundaries, failure semantics, and migration costs. Performance conclusions need a version, environment, workload, measurement method, and baseline.

---

[Source and validation](capability_inventory.md) · `rust` / `harness` / `cache`
