---
title: "Future directions"
capabilities: [rust, verification]
language_versions: ["3.0", "2.4"]
---

# Future directions

This page records future directions. [Runtime guides](runtime_execution.md) and the [capability inventory](capability_inventory.md) define current support.

| Direction | Evidence needed |
| --- | --- |
| Expand Rust semantics | Executable fixtures shared with Python and explicit unsupported-instruction errors |
| Extend WASM interfaces | Acceptance for WASI imports, reference types, and resource limits |
| Improve semantic evaluation | Defined evaluators, datasets, costs, and failure states |
| Complete toolchain integration | Synchronized source spans, run states, approvals, and recovery |

Public installation requires an accessible tag/commit or package version. This site pins the released Nexa 3.0.0; Rust retains its 2.4 subset.

---

[Source and validation](capability_inventory.md) · `rust` / `verification`
