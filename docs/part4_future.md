---
title: "后续方向"
capabilities: [rust, verification]
language_versions: ["3.0", "2.4"]
---

# 后续方向

本页记录演进方向。当前可用能力以[运行时指南](runtime_execution.md)和[能力清单](capability_inventory.md)为准。

| 方向 | 推进条件 |
| --- | --- |
| 扩大 Rust 语义覆盖 | 与 Python 共享可执行 fixture，显式处理未支持指令 |
| 扩展 WASM 接口 | 为 WASI imports、引用类型和资源限制建立独立验收 |
| 增强语义评测 | 明确 evaluator、数据集、成本和失败状态 |
| 完善工具链 | 同步 source span、运行状态、审批与恢复契约 |

公开版本发布需要可访问的 tag/commit 或包版本。本站固定到已发布的 Nexa 3.0.0；Rust 继续保留 2.4 子集。

---

[来源与验证](capability_inventory.md) · `rust` / `verification`
