---
title: Architecture evolution and experiments
capabilities:
- rust
- harness
- cache
- open_language
- open_revisions
language_versions:
- '3.0'
- '2.4'
---

# Architecture evolution and experiments

The current system uses the Python reference runtime for the full language path. Rust AVM expands through shared semantic cases. See [Rust/WASM](runtime_rust.md) for the implemented scope.

## Open Programs 3.0

The Python reference frontend checks typed program IR. OpenCompiler resolves candidates under a frozen environment and policy; OCI performs candidate and repository execution. ProgramSession separates draft CAS, activation, activities, effects, and exact patch grants. Persistent objects carry content digests.

A diagnostic advice pass is the first controlled compiler evolution component. Its `.nx` implementation proposes `{suggestions: [{code, replacement}]}` against fixed frontend diagnostics. The core preserves errors and rejects unknown names. Evaluation permits only `diagnostic_advice.py`, checks a frozen corpus, and compares C1/C2 IR, artifacts, implementations, and observations through zero-generation locked bootstrap. Selecting a successful report requires an expiring grant and seed CAS. Core/environment changes require reevaluation.

The opt-in `3.1-budget` proposal adds per-goal model-call limits through explicit APIs; the stable 3.0 parser and CLI keep the released grammar. See [the pinned evolution specification](https://github.com/Nexa-Language/Nexa/blob/274379606e53c90d2d25774f6bb8984c777d0759/docs/spec/3.0/evolution.md).

## Retained 2.4 runtime evolution

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
