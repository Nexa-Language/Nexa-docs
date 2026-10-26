---
title: "工具审批与恢复"
capabilities: [tools, checkpoint]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 工具审批与恢复

运行时只执行 Agent 声明暴露的工具，并在执行前检查 JSON Schema、参数类型与额外字段。`requires_approval` 或高风险工具进入 `waiting_approval`，需要明确的布尔决定。

## 声明需要审批的工具

完整声明模块。`record_review` 返回已审核的文本，不写外部服务；审批方式与有副作用工具相同。

```nexa
@tool("Record reviewed text", requires_approval: true, risk_level: "high")
fn record_review(content: string): string {
    python! """return content"""
}

agent Reviewer uses record_review {
    prompt: "Prepare the review and request approval before recording it."
}
```

将代码保存为 `review.nx`，配置模型后启动：

```sh
uv run nexa agent review.nx Reviewer "Review the supplied change" --timeout 900
```

## 审批一次调用

1. 从 JSON 输出取得 `run_id` 与 `pending_calls`。
2. 核对工具名、完整参数、作用对象和预期副作用。
3. 使用待审批调用的 ID 作决定。下例中的 `RUN_ID` 与 `CALL_ID` 是输出中的值。

```sh
uv run nexa agent review.nx Reviewer --resume RUN_ID --approve CALL_ID
```

拒绝本次调用：

```sh
uv run nexa agent review.nx Reviewer --resume RUN_ID --deny CALL_ID
```

恢复时保留源文件、Agent 定义、provider、预算与工作目录。`--resume` 不接受新任务文本；下一项任务需要新的运行入口。总超时包含等待决定的时间。

## SDK 审批

```python
from src.runtime.checkpoints import SQLiteCheckpointStore

store = SQLiteCheckpointStore(".nexa/runs.sqlite3")
state = store.approve(run_id, call_id, approved=True)
state = agent.execute(state=state, save=store.save)
```

此片段依赖已重建的同一 `agent` 和已核对的 `run_id`、`call_id`。`approved` 必须是 `True` 或 `False`；服务端注解、字符串和非空对象都不作为授权。

## 隔离与未知结果

`sandbox: true` 要求实际隔离执行器，缺少后端时返回错误。普通 Python 工具记录 `sandboxed=false`。工具请求已发出但结果未知时，先按[checkpoint 恢复保证](runtime_checkpoints.md)核实实际副作用。

---

[来源与验证](capability_inventory.md) · `tools` / `checkpoint`
