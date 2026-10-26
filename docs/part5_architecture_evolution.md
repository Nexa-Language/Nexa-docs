---
title: 架构演进与实验方向
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

# 架构演进与实验方向

当前系统以 Python 参考运行时为完整语言路径，Rust AVM 按共同语义用例扩展。当前可用范围见 [Rust/WASM](runtime_rust.md)。

## Open Programs 3.0

Python 参考前端检查带类型的 ProgramIR，OpenCompiler 在冻结 environment/policy 下求解，OCI 执行候选和仓库检查。ProgramSession 分别管理草稿 CAS、版本激活、活动、外部作用和准确补丁 grant；持久对象采用内容 digest。

诊断 advice pass 是首个受控编译器演进组件。`.nx` 实现针对固定前端诊断提出 `{suggestions: [{code, replacement}]}`；核心保留错误并拒绝未知名字。评估只允许修改 `diagnostic_advice.py`，运行固定 corpus，并通过零生成请求的 locked bootstrap 比较 C1/C2 的 IR、产物、实现与观察。选择通过的报告仍需有期限 grant 和 seed CAS；core/environment 改变后重新评估。

显式 API 中的 `3.1-budget` 提案试验每个 goal 的 model-call limit；稳定 3.0 parser 与 CLI 保持发行语法。见[固定版本演进规范](https://github.com/Nexa-Language/Nexa/blob/274379606e53c90d2d25774f6bb8984c777d0759/docs/spec/3.0/evolution.md)。

## 保留的 2.4 运行时演进

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
