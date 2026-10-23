---
title: "架构演进与实验方向"
capabilities: [rust, harness, cache]
---

# 架构演进与实验方向

当前系统以 Python 参考运行时为完整语言路径，Rust AVM 按共同语义用例扩展。当前可用范围见 [Rust/WASM](runtime_rust.md)。

## 已实现的演进

- CLI、SDK 和 API 共用编译入口与 include 加载器。
- 原生 provider 保存各自协议状态。
- `RunState`、预算、审批、SQLite journal 与 artifact 构成可检查的执行路径。
- flow 快照使用深拷贝恢复内存状态。
- Rust 支持声明、基础计算和 Agent 调用；WASM feature 使用 Wasmtime 48。

## 历史设计与后续研究

旧架构草案提出 COW 快照、全量 Rust runtime、虚拟内存分页与分布式执行。这些是研究或规划方向，交付状态应由独立实现和验收记录更新。当前 flow snapshot 的语义为深拷贝，精确响应缓存限于无工具 Chat 新运行。

后续扩展应优先增加跨后端语义 fixture，再明确资源边界、失败语义和迁移成本。性能结论需要说明版本、环境、工作负载、测量方法和基线。

---

[来源与验证](capability_inventory.md) · `rust` / `harness` / `cache`
