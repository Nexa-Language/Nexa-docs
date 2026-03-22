---
comments: true
---

# 2. 基础语法：定义你的首个跨维度团队

本章将介绍 Nexa 中最核心、最基础的语法元素。读完本章并掌握这些结构之后，你就可以毫无负担地抛弃绝大多数繁重且不稳定的传统 Python 智能体开发框架，使用声明式、富有表达力的方法来构筑你的第一代智能体团队。

---

## 🏗️ 核心原语：定义大语言模型代理 (`agent` 关键字)

在 Nexa 语言的哲学中，所有能够"思考"、接收上下文并输出结构化或非结构化文字的主体都被称为 `agent`。由于 Nexa 将 Agent 提权到了"一等公民"的位置，你可以像定义一个结构体 (Struct) 或类 (Class) 那样去书写它。

它是承载系统 Prompt、预设模型路由、身份角色以及工具配置的基本块（Block）。我们先来看一个最基础的定义方式：

```nexa
// 所有的属性全都在大括号内进行声明，不存在外部多余的 Client 实例化
agent FriendlyBot {
    role: "Casual conversationalist",
    model: "minimax/minimax-m2.5",
    prompt: "You are a very friendly ChatBot for casual conversations."
}
```

---

## 📋 Agent 属性详解

### 属性总览表

| 属性 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `role` | string | 否 | - | Agent 的角色描述，作为系统提示词的一部分 |
| `prompt` | string | **是** | - | Agent 的核心任务指令 |
| `model` | string | 否 | 默认模型 | 指定使用的 LLM 模型 |
| `memory` | string | 否 | - | 记忆模式：`persistent`（持久化）等 |
| `stream` | boolean | 否 | false | 是否启用流式输出 |
| `cache` | boolean | 否 | false | 是否启用智能缓存 |
| `experience` | string | 否 | - | 长期记忆文件路径 |
| `fallback` | string/list | 否 | - | 备用模型配置 |
| `tools` | list | 否 | [] | 可用工具列表 |
| `max_tokens` | int | 否 | - | 最大输出 token 数 |
| `timeout` | int | 否 | 30 | 请求超时时间（秒） |

### 属性详细说明

#### `role`（角色语义场）

定义该代理的系统角色（System Persona）。这不仅仅是一个标签，在底层编译为 Python 运行时时，它会作为系统提示词的极高权重顶层注入点，赋能模型的上下文边界。

```nexa
agent FinancialAdvisor {
    role: "资深金融分析师，专注于科技股投资策略",
    prompt: "根据用户需求提供专业的投资建议..."
}
```

!!! tip "最佳实践"
    - 角色描述应该**具体而专业**，避免模糊的描述如"你是一个助手"
    - 可以包含专业领域、经验年限、专长技能等信息
    - 好的角色描述能显著提升模型输出的专业性和一致性

#### `prompt`（任务执行描述）

这是驱动模型行动的核心指令区，支持多行纯文本字面量表达。在这里，你不需要处理转义甚至复杂的 Token 拼接，一切都自然发生。

```nexa
// 单行 prompt
agent Translator {
    prompt: "将用户输入翻译成中文"
}

// 多行 prompt（推荐用于复杂任务）
agent CodeReviewer {
    prompt: """
    你是一位代码审查专家。请审查提交的代码，关注以下方面：
    
    1. 代码质量和可读性
    2. 潜在的 bug 和边界情况
    3. 性能优化建议
    4. 安全漏洞
    
    输出格式：
    - 问题列表（如有）
    - 改进建议
    - 总体评价
    """
}
```

!!! warning "常见错误"
    不要在 prompt 中写具体的输出示例，这可能导致模型过度拟合。如果需要约束输出格式，请使用 `protocol`。

#### `model`（动态智脑映射）

**（极具破坏性优势的特性）** 原生的模型硬线链接。这使得我们可以在不同的代理之间按需无缝切换背后的引擎。

**正确格式**：`提供商/模型名`

```nexa
// ✅ 正确格式
agent Bot {
    model: "openai/gpt-4"
}

agent AnotherBot {
    model: "deepseek/deepseek-chat"
}

agent ThirdBot {
    model: "minimax/minimax-m2.5"
}

// ❌ 错误格式 - 缺少提供商前缀
agent WrongBot {
    model: "gpt-4"  // 会报错！
}
```

**支持的提供商前缀**：

| 前缀 | 说明 | 示例模型 |
|-----|------|---------|
| `openai/` | OpenAI GPT 系列 | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` |
| `deepseek/` | DeepSeek 系列 | `deepseek-chat`, `deepseek-coder` |
| `minimax/` | MiniMax 系列 | `minimax-m2.5` |
| `anthropic/` | Anthropic Claude 系列 | `claude-3-sonnet`, `claude-3-opus` |

!!! tip "模型选择建议"
    - **简单任务**（翻译、摘要）：使用轻量模型如 `deepseek-chat`
    - **复杂推理**（代码生成、分析）：使用强模型如 `gpt-4`
    - **实时响应**：选择响应速度快的模型

#### `memory`（记忆持久化）

代理的记忆模式，允许 Agent 自动管理多轮对话状态。

```nexa
agent ChatBot {
    prompt: "你是一个友好的聊天助手",
    memory: "persistent"  // 启用持久化记忆
}

flow main {
    // 第一次调用
    ChatBot.run("我叫张三");
    
    // 第二次调用 - Agent 会记住之前的对话
    ChatBot.run("我叫什么名字？");  // 会回答"张三"
}
```

#### `stream`（流式推写开关）

将其设置为 `true` 可以直接启用大模型的 Token 级流式响应。让 Agent 边思考边输出，实现对终端用户无卡顿的实时反馈。

```nexa
agent StreamBot {
    prompt: "你是一个故事创作助手",
    stream: true  // 启用流式输出
}
```

#### `cache`（智能缓存）

启用后，相同或相似的请求会复用之前的结果，大幅减少 Token 消耗和响应时间。

```nexa
agent CachedBot {
    prompt: "回答常见问题",
    cache: true  // 启用语义缓存
}
```

!!! info "缓存机制"
    - 基于**语义相似度**匹配，不仅是精确匹配
    - 缓存存储在 `.nexa_cache/` 目录下
    - 可通过 `nexa cache clear` 清除缓存

#### `experience`（长期记忆）

加载长期记忆文件，让 Agent 具备持久化的知识和经验。

```nexa
agent SmartBot {
    prompt: "基于历史经验回答问题",
    experience: "bot_memory.md"  // 加载记忆文件
}
```

记忆文件格式示例（`bot_memory.md`）：

```markdown
# Bot 记忆库

## 用户偏好
- 喜欢简洁的回答
- 偏好技术类话题

## 常见问题解答
- 什么是 Agent？Agent 是能够感知环境并采取行动的实体。

## 经验教训
- 不要假设用户的技术背景
- 复杂概念需要分步解释
```

#### `fallback`（模型灾备降级）

由于 API RateLimit 或意外宕机导致请求失败时，通过设定 `fallback` 模型作为容灾选项，在运行时无缝切换。

```nexa
// 单个备用模型
agent ResilientBot {
    model: "openai/gpt-4",
    fallback: "deepseek/deepseek-chat",  // gpt-4 不可用时自动切换
    prompt: "..."
}

// 多级备用（v0.9.7+）
agent HighAvailabilityBot {
    model: ["openai/gpt-4", fallback: "anthropic/claude-3-sonnet", fallback: "deepseek/deepseek-chat"],
    prompt: "..."
}
```

---

## 🌊 控制流枢纽：`flow` 和 `.run()`

只定义 Agent 就像是为不同的部门招募到了世界顶级的员工，但不给他们分配办公桌和网络，他们就永远是沉睡的状态。我们需要一个载体来激活与编排他们。这一切都在 `flow` 中发生。

在 Nexa 中，通常系统的入口流都会被命名为 `flow main`，这就类似于 C 语言或 Java 控制台运行时的 `main` 函数，是单文件乃至整个项目开始执行（Execution Entrypoint）的第一帧。

### ⚡ Hello World 完整实战解析

让我们仔细拆解一个最经典的 `01_hello_world.nx` 脚本：

```nexa
// 1. 定义智能体：我们给了它一个友好的性格，并且不需要指定模型（使用默认降级）
agent HelloWorldBot {
    role: "A very helpful and concise assistant.",
    prompt: "You must always greet the user cheerfully and briefly in less than 20 words."
}

// 2. 启动流入口
flow main {
    // 变量赋值：在 Nexa 中，字符串通常蕴含着自然语义请求，你可以直接通过等号注入
    greeting_request = "Say hello to Nexa developers all around the world!";
    
    // 调用 agent 的 .run() 方法，将指令发送给模型进行推理并返回响应。
    // 这里底层发生的并发、网络请求、RateLimit 回退均对用户隐匿。
    response = HelloWorldBot.run(greeting_request);
    
    // 打印结果
    print(response);
}
```

### 运行结果

```bash
$ nexa run hello_world.nx

Hello, Nexa developers! 🌍 Welcome to the future of agent programming!
```

!!! info "运行时的底层机制"
    当敲下执行命令时，Nexa 编译器首先会建立静态的图节点，对传入传出的数据类型进行静态核对，确保整个脚本没有孤儿死锁。随后将其无缝转译为高效的异步 Python 运行时（利用 `asyncio`），唤醒 `HelloWorldBot` 实例。这不仅是全网最为极简的 Agent Hello World，更是最安全的一个。

### `flow` 语法详解

```nexa
// 基本语法
flow <flow_name> {
    // 语句...
}

// 带参数的 flow（v0.9+）
flow process_user(user_id: string, action: string) {
    // 使用参数
    result = Agent.run(user_id + " wants to " + action);
}
```

### `.run()` 方法详解

```nexa
// 基本调用
result = Agent.run("your input");

// 带多参数调用
result = Agent.run("primary input", "additional context");

// 链式调用（管道）
result = input >> Agent1 >> Agent2 >> Agent3;
```

---

## 🔍 内置工具的挂载与环境沙盒穿透 (`uses` 关键字)

如果仅仅是在控制台里产生字符串，大模型也不过是个会"聊天"的花瓶。真正的大模型智能体（Agent）要能与数字世界互动（比如查天气、删文件、写表格）。

在传统的 Python 胶水代码开发中，要想让大模型调用一个函数，你需要使用极其反人类的 JSON Schema 语法去手写 Function Calling 配置。并且，一旦函数签名发生变更，你的 Schema 如果忘了跟着改，整个调用链就会在运行时崩溃。

而在 Nexa 宇宙中，一切只需要一个原生的 `uses` 关键字声明！Nexa 把函数绑定逻辑通过反射机制（Reflection）直接做进了编译器。

### 基本用法

```nexa
agent Interactor {
    // 原生语法级载入沙盒环境包
    uses [std.ask_human, std.os.file_read]
    
    prompt: "当遇到不确定的风险操作时，优先调用 ask_human 将情况反馈给人类审查并获取许可。必要时使用 file_read 查阅本地配置。"
}
```

!!! success "从根本上消灭 Schema 烦恼"
    上文中使用的 `std.ask_human` 和 `std.os.file_read` 是 Nexa 内置标准包。当使用 `uses` 装载后，**Nexa 的编译器会在背后自动爬取这些 Python 工具内部的函数签名与 `docstring`，并将它们编译组装为各大模型厂商适配的 Native Function Calling Payload！**这意味着开发者完全不需要手写 JSON，甚至不需要思考不同模型对工具调用的不同要求。它甚至支持通过类型提示来进行参数验证！

### 标准库工具一览

| 命名空间 | 工具 | 说明 |
|---------|-----|------|
| `std.fs` | `file_read`, `file_write` | 文件系统操作 |
| `std.http` | `get`, `post` | HTTP 请求 |
| `std.time` | `now`, `sleep` | 时间相关操作 |
| `std.shell` | `execute` | 执行 shell 命令 |
| `std.ask_human` | `call` | 人机交互询问 |
| `std.json` | `parse`, `stringify` | JSON 处理 |

### 使用示例

```nexa
// 文件处理 Agent
agent FileAssistant uses std.fs {
    prompt: "帮助用户管理文件，可以读取和写入文件"
}

// 网络请求 Agent
agent WebScraper uses std.http {
    prompt: "从网页获取内容并提取信息"
}

// 多工具 Agent
agent MultiToolAgent uses std.fs, std.http, std.time {
    prompt: "我可以处理文件、访问网络、获取时间"
}
```

---

## 🎯 Agent 定义常见模式

### 模式 1：简单对话 Agent

```nexa
agent ChatBot {
    role: "友好的聊天助手",
    model: "deepseek/deepseek-chat",
    prompt: "与用户进行友好的日常对话"
}
```

### 模式 2：专业领域 Agent

```nexa
agent LegalAdvisor {
    role: "资深法律顾问，专攻合同法",
    model: "openai/gpt-4",
    prompt: """
    为用户提供专业的法律建议，特别是合同相关的问题。
    注意：提醒用户这只是参考建议，不构成正式的法律意见。
    """,
    memory: "persistent"
}
```

### 模式 3：工具增强 Agent

```nexa
agent DataAnalyst uses std.fs, std.http {
    role: "数据分析师",
    model: "deepseek/deepseek-chat",
    prompt: "分析数据并生成报告",
    cache: true
}
```

### 模式 4：高可用 Agent

```nexa
agent ProductionBot {
    role: "生产环境助手",
    model: ["openai/gpt-4", fallback: "deepseek/deepseek-chat"],
    prompt: "...",
    cache: true,
    timeout: 60
}
```

---

## ⚠️ 常见错误与解决方案

### 错误 1：模型格式错误

```nexa
// ❌ 错误
agent Bot {
    model: "gpt-4"  // 缺少提供商前缀
}

// ✅ 正确
agent Bot {
    model: "openai/gpt-4"
}
```

### 错误 2：Agent 定义顺序错误

```nexa
// ❌ 错误：Agent 定义在 flow 之后
flow main {
    result = MyBot.run("hello");
}

agent MyBot {
    prompt: "..."
}

// ✅ 正确：Agent 定义在 flow 之前
agent MyBot {
    prompt: "..."
}

flow main {
    result = MyBot.run("hello");
}
```

### 错误 3：属性名拼写错误

```nexa
// ❌ 常见拼写错误
agent Bot {
    promt: "...",      // 应为 prompt
    moedl: "gpt-4",    // 应为 model
    rol: "助手"        // 应为 role
}

// ✅ 正确拼写
agent Bot {
    prompt: "...",
    model: "openai/gpt-4",
    role: "助手"
}
```

### 错误 4：忘记必要的属性

```nexa
// ❌ 错误：缺少 prompt
agent Bot {
    role: "助手"  // 只有 role 没有 prompt
}

// ✅ 正确
agent Bot {
    role: "助手",
    prompt: "帮助用户解决问题"  // prompt 是必需的
}
```

---

## 📝 本章小结

在这一章里，我们学习了：

1. **Agent 的定义**：使用 `agent` 关键字定义智能体
2. **核心属性**：`role`, `prompt`, `model`, `memory`, `stream`, `cache` 等
3. **流程控制**：使用 `flow main` 作为程序入口
4. **工具挂载**：使用 `uses` 关键字加载标准库工具
5. **常见模式**：简单对话、专业领域、工具增强、高可用等模式
6. **常见错误**：模型格式、定义顺序、属性拼写等

但这仅仅发挥出大语言模型单打独斗（Single-Agent Task）的实力。真实的业务系统充满复杂冗长的协同交错：如何让十几个分工明确的代理接力完成任务？又该如何在各执一词的代理间达成完美共识？

不要眨眼，这正是下一章 **多 Agent 调度与控制（高级特性）** 将为你呈现的真正编排魔法。

---

## 🔗 相关资源

- [快速入门教程](quickstart.md) - 30 分钟掌握 Nexa
- [完整示例集合](examples.md) - 更多实战代码
- [常见问题与排查](troubleshooting.md) - 解决开发问题
