---
title: "典型使用场景"
capabilities: [tools, actors, checkpoint]
---

# 典型使用场景

按任务的数据流、副作用与恢复要求选择运行方式。

| 场景 | 建议结构 | 重点验收 |
| --- | --- | --- |
| 证据整理与报告 | 顺序 Agent 管道 + Protocol | 输出 schema、事实来源与完整性 |
| 多方案分析 | 独立会话 + fork/merge | 并发上限、结果顺序与选择标准 |
| 分阶段研究 | Actor 顺序邮箱 | 历史保留、累计预算与 await |
| 文件修复 | 受限工具 + 审批 + checkpoint | 写入目标、允许/拒绝、恢复与未知结果 |
| 服务集成 | MCP 或自定义工具 | schema、授权、超时和资源清理 |

[工具链](toolchain.md)提供编程任务入口；[可验证示例](examples.md)提供小型完整程序。真实任务的质量、成本和时延需结合选定模型评测。

---

[来源与验证](capability_inventory.md) · `tools` / `actors` / `checkpoint`
