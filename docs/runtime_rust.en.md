---
title: "Rust AVM and WASM support"
capabilities: [rust]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Rust AVM and WASM support

The Python compiler and runtime are the Nexa 2.4 reference implementation. Rust AVM expands its coverage through shared semantic fixtures and currently supports this subset.

| Path | Current behavior |
| --- | --- |
| Rust compilation and interpretation | Declaration initialization, integer/float arithmetic, local/global variables, jumps, returns, and Agent calls |
| Provider boundary | `Interpreter::set_agent_executor`; the CLI text provider uses `NEXA_API_KEY`, optional `NEXA_BASE_URL`, and a 30-second request timeout |
| Tools, structured output, full Harness | Use the Python reference runtime |
| Unimplemented opcode or call | Explicit error |

The Rust compiler rejects tool declarations with `Tool … requires the Python runtime`. Run programs containing tools on the Python backend.

## Shared semantics

Python and Rust tests consume `tests/fixtures/conformance/programs.json`, covering integer precision, division, variables, and Agent calls. This complete program is part of that shared path and returns `2.5` offline.

```nexa
flow main {
    result = 5 / 2;
}
```

Run Rust checks from the Nexa checkout:

```sh
cargo test --manifest-path avm/Cargo.toml
```

## WASM executor

WASM uses Wasmtime 48 LTS. With the `wasm` feature enabled, it executes real modules with scalar parameters, retained instance state, memory limits, fuel, and epoch interruption. Without the feature, execution returns an explicit error.

```sh
cargo test --manifest-path avm/Cargo.toml --features wasm
```

WASI imports and reference-type parameters are not yet integrated. Configure WASM isolation and ordinary Python tool execution separately. A Python tool declaring `sandbox: true` still requires an actual isolation backend.

## Evaluation scope

Shared fixtures check the semantics of their specified programs. Real model quality, cost, and latency require a reproducible provider, model, input, budget, and environment. [Architecture evolution](part5_architecture_evolution.md) retains the historical design context. Performance ratios from older baselines are omitted until remeasured on the current runtime.

---

[Source and validation](capability_inventory.md) · `rust`
