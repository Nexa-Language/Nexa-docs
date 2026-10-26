---
title: "连续对话与新一轮运行"
capabilities: [conversations, checkpoint, providers]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 连续对话与新一轮运行

`continue_run` 从已结束运行创建新一轮任务，保留已确定的历史和 provider 状态，为新一轮重置预算、用量、时限与审批。`execute(state=...)` 用于恢复同一次运行。

## 选择入口

| 需求 | 入口 | 运行 ID 与预算 |
| --- | --- | --- |
| 开始独立任务 | `execute("task")` | 新 ID、新会话、新预算 |
| 恢复待审批或中断的原任务 | `execute(state=state)` | 保留原 ID、配置、用量和时限 |
| 沿用已结束任务的历史继续对话 | `continue_run(previous, "next")` | 新 ID、新预算、新审批，保留会话历史 |

## 两轮对话

完整 Python 使用示例；实际执行需要 provider 配置。

```python
from src.runtime.agent import NexaAgent
from src.runtime.checkpoints import SQLiteCheckpointStore
from src.runtime.run_state import RunConfig

agent = NexaAgent("Analyst", prompt="Work from evidence")
store = SQLiteCheckpointStore(".nexa/runs.sqlite3")
first = agent.execute("Analyze the evidence", config=RunConfig(timeout=120), save=store.save)
if first.success:
    second = agent.continue_run(first, "Summarize the conclusion", save=store.save)
    print(second.run_id, second.status.value)
```

`continue_run(previous, *args, config=None, cancel=None, save=None, on_event=None, on_text=None, provider=None)` 返回 `RunState`。未显式提供 `config` 时沿用上一轮的配置值，并把使用量与起始时间归零。上一轮状态对象保持原样。

新状态的 `metadata.parent_run_id` 指向上一轮，`metadata.session_id` 关联整个会话。每轮事件都使用新 `run_id`。原生 Responses/Anthropic 的 opaque items 和游标继续保留。

## 继续前的检查

- `running` 与 `waiting_approval` 需要先恢复或取消原任务。
- journal 中存在未知工具结果时禁止继续；先按[恢复指南](runtime_checkpoints.md)核实。
- 已完成的工具结果从 journal 补回历史；尚未开始的调用以取消结果闭合消息配对，已完成副作用不重放。
- 新输入须非空；Agent 定义、模型、provider 和工作目录仍需匹配。
- 覆盖配置时保留原 artifact 目录，保证历史中的大工具结果仍可读取。
- 旧审批不授权新一轮调用；有风险的工具再次进入审批流程。

已结算的 `completed`、`failed`、`cancelled`、`timed_out`、`budget_exhausted` 可在上述检查后继续。CLI `nexa agent --resume` 仍表示恢复原运行，新轮入口由 Python API 提供。

---

[来源与验证](capability_inventory.md) · `conversations` / `checkpoint` / `providers`
