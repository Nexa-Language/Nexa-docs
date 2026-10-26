---
title: "结构化上下文"
capabilities: [context, providers]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 结构化上下文

`context` 是 Agent 声明的一部分，定义上下文来源、去向、schema 和继承字段。两端都声明 context 的管道会传递 `AgentContext`。Python 应用也可通过 `agent.run(previous.last_context())` 显式传递。

## 完整声明

本例只声明上游与下游 Agent，编译无需模型。

```nexa
protocol Findings { summary: string }
agent Researcher {
    prompt: "Extract the facts."
    context {
        source: upstream,
        sink: downstream,
        output_schema: Findings,
        inherit: [messages]
    }
}
agent Writer {
    prompt: "Write from the facts."
    context {
        source: upstream,
        sink: downstream,
        input_schema: Findings,
        inherit: [messages, artifacts]
    }
}
```

| 字段 | 用途 |
| --- | --- |
| `source` / `sink` | 选择上游输入与下游输出方式 |
| `input_schema` / `output_schema` | 声明上下文契约；名称按名义相等比较 |
| `inherit` | 选择继承的消息或 artifact 字段 |
| `max_history_turns` | 限制保留的历史回合 |

`shared:name` 在同一 flow 内共享深拷贝快照；`discard` 不生成下游 context。跨 schema 传递需要显式转换，单纯字段相似不会通过名称检查。

## 上下文预算

当前上下文限制把序列化 UTF-8 字节数作为保守 token 上界；provider 的实际 usage 单独记账。Chat 按完整 user turn 裁剪，保持工具调用与结果配对。最新单回合超限会失败。

原生 Responses/Anthropic 保留 opaque items；历史或上下文超限时要求缩短输入，避免丢失协议状态。详见[模型协议](runtime_providers.md)。

---

[来源与验证](capability_inventory.md) · `context` / `providers`
