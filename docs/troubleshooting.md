---
title: "故障排查"
capabilities: [compilation, execution, checkpoint, providers]
---

# 故障排查

先确定失败层次，再保留能复现问题的最小证据。日志应包含版本、命令、文件位置、运行 ID 和状态，移除凭据及任务敏感数据。

| 现象 | 检查与处理 |
| --- | --- |
| `nexa` 命令缺失 | 在已确认的 2.4 checkout 执行 `uv sync --locked`，使用 `uv run nexa --version` |
| include 未找到 | 以导入文件所在目录检查相对路径，再确认包内标准库路径 |
| 解析失败 | 运行 `nexa validate FILE --json`，从最早的 source span 修复 |
| Harness strict 失败 | 阅读具体 rule ID，补充预算、工具约束或上下文契约 |
| API key 缺失 | 在实际运行进程中确认配置是否存在；仅记录已设置/未设置 |
| structured output 失败 | 核对 schema 与 provider 原始完成状态，保留脱敏错误 |
| `waiting_approval` | 检查 pending 工具与完整参数，使用明确批准或拒绝 |
| `timed_out` | 总时限包含审批等待和恢复间隔；核对墙钟时间 |
| `budget_exhausted` | 检查调用次数及 provider usage，按任务拆分下一轮 |
| checkpoint 冲突 | 停止旧执行器，重新加载最新 revision 后决定后续动作 |
| 未知工具结果 | 先核实外部副作用，再 `resolve_tool`，见[恢复指南](runtime_checkpoints.md) |
| Actor 漏 await | 在 flow 返回前 await 所有 Actor |
| native context 超限 | 缩短输入或开启独立新任务，保留 opaque provider items |

## 可复现材料

提供经过脱敏的最小 `.nx`、准确版本、命令、诊断和预期结果。涉及当前文档示例时附 [inventory](capability_inventory.md) 中的 example ID。不要在 issue 中上传 `.nxs`、真实 checkpoint 或含任务数据的 artifact。

编译、离线 fixture、真实模型验收分别记录。对网络服务的观察应保留发生时间和请求范围。

---

[来源与验证](capability_inventory.md) · `compilation` / `execution` / `checkpoint` / `providers`
