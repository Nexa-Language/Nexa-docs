---
title: "执行状态、预算与取消"
capabilities: [execution]
---

# 执行状态、预算与取消

`NexaAgent.execute()` 创建独立会话并返回 `RunState`；`aexecute()` 提供异步适配。`run()` 保留同一实例的连续会话并直接返回输出，同一实例的调用串行化。

## 显式运行配置

以下 Python 示例需要模型配置。所有预算为单次 `execute` 运行的上限；恢复会沿用已保存的预算和用量。

```python
from src.runtime.agent import NexaAgent
from src.runtime.run_state import RunConfig

agent = NexaAgent("Analyst", prompt="Work from evidence")
state = agent.execute("Explain the findings", config=RunConfig(
    timeout=120,
    max_model_calls=8,
    max_tool_calls=4,
    max_tokens=12000,
))
print(state.status.value, state.output, state.error)
```

| 字段 | 默认值 | 含义 |
| --- | --- | --- |
| `timeout` | 30 秒 | 总墙钟时限，包含审批等待和恢复前时间 |
| `max_model_calls` | 20 | 包括重试的模型请求数 |
| `max_tool_calls` | 10 | 实际单个工具调用数 |
| `max_tokens` | `None` | 输入与输出 usage 累计上限 |
| `retries` | 2 | 分别限制每次 provider 请求的瞬态错误重试、整次运行的结构化输出修正 |
| `max_tool_output_chars` | 16000 | 工具结果内联字符数阈值，至少 256 |
| `artifact_directory` | `.nexa/artifacts` | 超大工具结果的内容寻址目录 |

`nexa agent` 的 CLI 默认 timeout 为 300 秒、工具预算为 20；这些默认值由 CLI 显式传入，与上表的 SDK 默认值不同。

## 根据状态采取行动

| 状态 | 含义 | 后续动作 |
| --- | --- | --- |
| `running` | 正在执行 | 消费事件或等待 |
| `waiting_approval` | 工具在等待明确决定 | 核对 `pending_calls`，批准或拒绝 |
| `completed` | 已完成输出验证 | 读取 `output` |
| `failed` | provider、工具、协议或验证失败 | 读取 `error` 与 journal；先核实未知副作用 |
| `cancelled` | 已观察到取消信号 | 检查已完成的副作用 |
| `timed_out` | 总时限已耗尽 | 核对状态后为新任务配置预算 |
| `budget_exhausted` | 调用或 token 预算已耗尽 | 核对用量后决定后续工作 |

Token 预算依据 provider 返回的 usage 累计。设置 `max_tokens` 后若 provider 缺少 usage，运行明确失败。单次请求的实际输入成本在返回后确认，累计超限会阻止后续请求。

JSON、Protocol 或 schema 输出格式错误时，运行时在 `retries` 限额内追加修正请求，保留已执行工具的结果。修正次数保存在 checkpoint，审批恢复后继续使用剩余额度；所有尝试都计入模型、token 与总时限预算。修正消息属于原用户回合，`ensures` 仍使用该回合原始输入；`ensures` 或 `verify` 失败直接终止。

工具额度用完后，后续模型请求移除工具，让模型基于已有结果给出最终回答。执行边界仍会拒绝超出额度的额外工具调用。

## 取消和并行

向 `execute(cancel=event)` 传入 `threading.Event`，用 `event.set()` 请求取消。运行时在模型、流式输出与工具边界协作检查；正在执行的任意 Python 工具需要自行实现可取消行为。请求超时使用剩余总时间。

并行编排创建独立会话，默认最多 8 个任务并发，结果按输入顺序返回。Actor 的持续消息另按[Actor 生命周期](runtime_actors.md)计账。持久化语义见[checkpoint](runtime_checkpoints.md)。

---

[来源与验证](capability_inventory.md) · `execution`
