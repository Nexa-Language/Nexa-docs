---
title: "错误传播与恢复边界"
capabilities: [language, execution, checkpoint]
---

# 错误传播与恢复边界

语法级错误处理适合局部控制流；持久运行状态和未知副作用由运行时契约处理。先判断错误发生在哪一层，再选择恢复入口。

| 机制 | 用途 |
| --- | --- |
| `try` / `catch` | 捕获语句范围内的异常 |
| `try_agent` / `catch_correction` | 进入明确的纠正分支 |
| `?` | 解包 `NexaResult`，失败向调用方传播 |
| `otherwise` | 对错误结果提供本地回退 |
| `defer` | 已有解析与调度器支持；当前生成程序执行失败，见下方限制 |

## 完整纠正示例

```nexa
flow main {
    result = "before";
    try_agent {
        assert false;
    } catch_correction(e: Exception) {
        result = "corrected";
    }
}
```

离线执行得到 `corrected`。`NexaAgent.run_result()` 为 Python 调用方提供显式 `NexaResult`；`execute()` 返回含 `status` 和 `error` 的 `RunState`。

## 有副作用的失败

工具已发出请求且结果未知时，抛出 `ToolOutcomeUnknown`。普通成功字符串会成为已知结果，影响恢复判断。保留 checkpoint，由操作者核实结果后调用 `resolve_tool`。详见[未知结果恢复](runtime_checkpoints.md)。

预算耗尽、取消和超时由[执行状态](runtime_execution.md)区分；继续新一轮任务使用 [continue_run](runtime_conversations.md)。


## 当前生成路径限制

`defer` 的 parser 和独立调度器测试存在；完整 `flow main { defer print("closed"); result = 1; }` 目前执行时报告 `name 'defer' is not defined`。关键资源清理应放在受信任 Python 工具的 `try/finally` 中，直到生成路径完成验收。

带 `requires` / `ensures` 的 flow 在当前生成路径中会因 `ContractClause` 构造参数不匹配失败。使用已执行验证的 `verify`、工具参数 schema 与明确错误状态建立当前任务的约束。

---

[来源与验证](capability_inventory.md) · `language` / `execution` / `checkpoint`
