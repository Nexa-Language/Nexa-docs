---
title: "构建可核验的 Agent 程序"
capabilities: [tools, execution, verification, cache]
---

# 构建可核验的 Agent 程序

先建立完整端到端路径，再按实际风险补充约束。以下顺序适合从原型迁移到可维护应用。

1. 将任务目标、输入、输出 schema 与成功条件写清楚。
2. 暴露完成任务所需的最小工具集合，区分读操作与高风险副作用。
3. 显式设置时间、模型调用、工具调用与 token 预算。
4. 保存 `RunState`、事件和 checkpoint；日志移除凭据。
5. 测试完成、审批允许/拒绝、取消、超时、预算耗尽、未知结果和恢复。
6. 用固定 fixture 验证机制，再用选定模型评测任务质量。

## 上下文与缓存

按完整回合管理 Chat 历史，保留工具协议配对。原生 provider 保留 opaque items。精确缓存仅用于无工具 Chat 新运行，命中率应随工作负载测量。

## 工具失败

参数错误应在副作用前拒绝。网络和 shell 操作发生结果不确定的失败时抛出 `ToolOutcomeUnknown`，让调用方核实。不要把失败包装为普通成功文本。

## 回归证据

记录源码版本、环境、fixture、断言与结果。编译通过、离线语义通过、真实模型质量达标分别对应不同验收项。可参考本站的[能力与示例清单](capability_inventory.md)。

---

[来源与验证](capability_inventory.md) · `tools` / `execution` / `verification` / `cache`
