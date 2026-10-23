---
title: "设计背景"
capabilities: [compilation, execution, providers]
---

# 设计背景

模型调用之外，Agent 应用还需要组织工具权限、上下文、失败恢复、预算和结果验证。Nexa 将这些边界放到语言声明和运行状态中，使代码生成与人工编程共享同一执行入口。

## 从源码到执行

统一编译器处理 include、AST、诊断和 Python 生成物。AgentRunner 处理 provider、工具和状态转换。SQLite checkpoint 保留运行进度和工具 journal，原生 provider items 保留协议连续性。

## 设计取舍

Python 保留与现有 AI 工具生态的集成能力；Rust AVM 通过共享 fixture 逐步扩展。可恢复执行要求保存足够的历史和结果，未知副作用需要操作者核实；外部系统的幂等机制可增强业务保证。

用[语言基础](part1_basic.md)理解程序结构，再用[运行时契约](runtime_execution.md)理解执行边界。

---

[来源与验证](capability_inventory.md) · `compilation` / `execution` / `providers`
