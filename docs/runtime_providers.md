---
title: "模型协议与配置"
capabilities: [providers, cache]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 模型协议与配置

`provider_api` 选择消息协议。Python 参考运行时支持 Chat Completions、Responses 和原生 Anthropic。编译无需模型凭据，也不会发起 provider 请求；导入编译器或运行时模块时可能初始化配置对象并读取本地 `.nxs`。首次使用先完成[provider 配置](part2_config_stdlib.md#first-provider-setup)。

| 值 | 选择与凭据 | 会话保留内容 |
| --- | --- | --- |
| `chat` | 默认协议；沿用 `.nxs` 与现有 provider 配置 | Chat 消息、工具调用与结果 |
| `responses` | 显式选择；沿用现有 OpenAI client 配置 | 原始 output items、encrypted reasoning、原生工具结果 |
| `anthropic` | 显式选择，或模型名前缀 `anthropic/` | 原始 content blocks、thinking 签名、原生 tool_result |

## 声明协议

完整声明模块；实际运行还需选择可用模型和配置凭据。

```nexa
agent Analyst {
    prompt: "Analyze the supplied evidence."
    provider_api: "responses"
    timeout: 120
    max_tool_calls: 8
}
```

`model` 可在声明中指定，未指定时从有效配置读取。`use config name;` 选择已有配置，见[配置管理](part2_config_stdlib.md)。凭据应通过本地环境或既有 `.nxs` 配置提供，避免写入 `.nx` 与版本控制。

原生 Anthropic 需要在 Nexa checkout 安装 extra，并在运行环境设置 `ANTHROPIC_API_KEY`。可选 `ANTHROPIC_BASE_URL` 指定 endpoint。

```sh
uv sync --locked --extra anthropic
```

## 完成与失败

流式、非流式、Protocol 输出和缓存命中共用输出验证与完成处理。截断、拒绝、或流结束前没有完成事件会让运行失败。需要保留的 opaque provider items 会进入 checkpoint，恢复时仍使用原协议。

## 精确响应缓存

缓存适用于**无工具的 Chat 新运行**。键包含有效上下文、系统指令、模型、endpoint 和输出契约；命中前仍执行上下文预算检查。Responses 与 Anthropic 当前不缓存响应。会话历史、provider 状态与缓存应分别管理。

缓存效果由工作负载决定。本站的离线 fixture 检查键隔离、输出验证和请求是否跳过；模型质量、成本与延迟需用指定 provider 和预算单独测量。

继续阅读[执行与预算](runtime_execution.md)及[上下文结构](part2_context_structure.md)。

---

[来源与验证](capability_inventory.md) · `providers` / `cache`
