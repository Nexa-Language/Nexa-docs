---
title: "Actor 生命周期"
capabilities: [actors, execution]
---

# Actor 生命周期

一个 flow 拥有它创建的 Actor。每个 Actor 使用独立 Agent 会话和顺序邮箱；后续消息保留该 Actor 的历史，累计模型与工具预算以及总时限。

## 启动、发送与等待

先配置模型，再保存为 `actor.nx` 并运行 `uv run nexa run actor.nx`。Worker 按顺序处理两条消息，第二条消息可以使用第一条的会话历史；flow 返回第二条回复。

```nexa
agent Worker {
    prompt: "Process messages in order and retain prior context."
}

flow main {
    worker = spawn Worker("Inspect the evidence");
    pass "Summarize the evidence" to worker;
    result = await worker;
}
```

`spawn` 启动 Actor，`pass` 排队后续输入，`await` 关闭邮箱并返回最后一次结果。flow 最多同时拥有 8 个活跃 Actor；已 await 的 Actor 释放并发名额。

## 结束与失败

所有 Actor 必须在 flow 返回前 await。flow 异常或漏掉 await 时，运行时取消其余任务并等待线程退出，再报告失败。工具本身的取消行为仍受[协作取消](runtime_execution.md)约束。

模型 Actor 自动消费邮箱。独立 `receive()` 需要自定义消息处理器，当前语言运行路径会明确报错。Actor 会话只存在于当前 flow；跨进程审批和恢复使用 `execute()` 或 `nexa agent`。

多个 Actor 的独立会话与同一个 Actor 的连续消息分别适合并行分工和有序工作。若只是有界并行并聚合结果，阅读 [fork/merge](part2_advanced.md)。

---

[来源与验证](capability_inventory.md) · `actors` / `execution`
