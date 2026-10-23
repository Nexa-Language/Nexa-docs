---
title: "管道与并行编排"
capabilities: [language, harness, context]
---

# 管道与并行编排

先按数据依赖选择拓扑，再选择执行预算。顺序管道将前一步输出传给下一步；并行分支使用独立 Agent 会话。

## 顺序管道

先配置模型，将下面的程序保存为 `pipeline.nx`，运行 `uv run nexa run pipeline.nx`。Researcher 提取事实，Summarizer 接收事实并返回摘要。

```nexa
agent Researcher { prompt: "Extract the facts." }
agent Summarizer { prompt: "Summarize the facts." }
flow main {
    result = "evidence" >> Researcher >> Summarizer;
}
```

各阶段接收前一阶段的结果；两端声明 context 时，管道传递 [AgentContext](part2_context_structure.md)。需要检查中间值时，也可显式写作 `facts = Researcher.run("evidence"); result = Summarizer.run(facts);`。

## fork/merge

下例并行探索两种方案，需要模型配置。

```nexa
agent Explorer { prompt: "Explore one approach." }
flow main {
    fork [Explorer.run("Approach A"), Explorer.run("Approach B")] merge all;
}
```

并发默认有界于 8；结果按输入顺序保存。`all` 聚合所有结果，`first` 和 `vote` 按对应策略选择；`best`/`best_of` 需要结果携带数值 `score`，缺失时失败。不要依赖分支完成顺序作为输入顺序。

## 持续消息

对单个工作者连续发消息时使用 [Actor](runtime_actors.md)。跨进程保存审批状态时使用 [execute 与 checkpoint](runtime_checkpoints.md)。

---

[来源与验证](capability_inventory.md) · `language` / `harness` / `context`
