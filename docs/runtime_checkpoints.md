---
title: "Checkpoint 与未知结果"
capabilities: [checkpoint, tools]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# Checkpoint 与未知结果

SQLite checkpoint 保存 `RunState`，包含配置、会话、provider items、用量、审批和工具 journal。事务与递增 `revision` 检测并发写入；旧执行器保存旧 revision 会抛出 `CheckpointConflict`。

## 保存与加载

下面的 Python 片段需要已经创建并配置的 `agent`。

```python
from src.runtime.checkpoints import SQLiteCheckpointStore

store = SQLiteCheckpointStore(".nexa/runs.sqlite3")
state = agent.execute("Inspect the workspace", save=store.save)
restored = store.load(state.run_id)
state = agent.execute(state=restored, save=store.save)
```

跨进程恢复时重新建立相同 Agent 定义，回到原工作目录，使用原来的程序与 provider 配置。CLI 还校验编译生成物的 hash，源文件或 include 改变会阻止恢复。

## 工具 journal 的三个阶段

| 持久化状态 | 恢复行为 |
| --- | --- |
| 调用尚未开始 | 按预算与审批规则决定是否执行 |
| `started`，结果尚未保存 | 停止并报告未知结果，等待操作者核实 |
| `completed`，结果已保存 | 复用结果并完成消息拼接，避免重复执行 |

工具返回结果后先持久化，再追加 provider 消息。文件、数据库或服务的副作用可能早于 checkpoint 写入；外部系统的幂等键可以进一步降低重复风险。

## 处理未知结果

网络超时、连接中断、响应流读取或解码失败、shell 超时、MCP 断连可能产生未知结果。自定义工具应抛出 `ToolOutcomeUnknown` 保留这一事实；吞掉异常会把自定义返回值当作真实结果。

1. 保留 checkpoint 和相关外部日志。
2. 根据工具名、参数及外部系统记录核实实际结果。
3. 仅在结果已核实后，将实际输出和成功状态写入 journal。
4. 重建同一 Agent 并恢复。

```python
state = store.resolve_tool(
    run_id,
    call_id,
    "Operator-verified result from the external system",
    success=True,
)
state = agent.execute(state=state, save=store.save)
```

这个片段依赖已核实的 `run_id`、`call_id` 与原 `store`、`agent`。`resolve_tool` 只接受仍在 pending 且 journal 为 `started` 的调用。

## 数据管理

checkpoint、trace 和 [artifact](runtime_artifacts.md) 可能包含任务数据。按项目访问策略保管，默认 `.nexa` 运行数据应留在 Git ignore 中。保存运行状态与 [flow 快照](part2_harness.md)各自承担不同范围：前者面向持久运行，后者恢复当前 flow 的内存状态。

---

[来源与验证](capability_inventory.md) · `checkpoint` / `tools`
