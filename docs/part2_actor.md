---
title: "Actor 语法与使用路径"
capabilities: [actors]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# Actor 语法与使用路径

Actor 使用 `spawn`、`pass` 和 `await` 表达并发工作者及其邮箱。实际生命周期、并发上限和计账规则见 [Actor 生命周期](runtime_actors.md)。

| 语法 | 含义 |
| --- | --- |
| `worker = spawn Agent("task");` | 在当前 flow 中创建独立 Agent 会话 |
| `pass "next" to worker;` | 将后续输入加入该 Actor 的顺序邮箱 |
| `result = await worker;` | 关闭邮箱，等待结束并返回最后结果 |

多次消息适合分阶段分析同一任务。并行独立任务可创建多个 Actor，但每个 Actor 都需要在 flow 返回前 await。异常时运行时取消剩余任务并等待其线程退出。

旧设计中的独立 `receive()` 需要自定义消息处理器；当前模型 Actor 自动消费邮箱。跨进程任务使用[持久化运行](runtime_checkpoints.md)。

---

[来源与验证](capability_inventory.md) · `actors`
