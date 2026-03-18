---
comments: true
---

# 2. 基础语法：定义你的首个跨维度团队

本章将介绍 Nexa 中最核心、最基础的语法元素。读完本章并掌握这些结构之后，你就可以毫无负担地抛弃绝大多数繁重且不稳定的传统 Python 智能体开发框架，使用声明式、富有表达力的方法来构筑你的第一代智能体团队。

---

## 🏗️ 核心原语：定义大语言模型代理 (`agent` 关键字)

在 Nexa 语言的哲学中，所有能够“思考”、接收上下文并输出结构化或非结构化文字的主体都被称为 `agent`。由于 Nexa 将 Agent 提权到了“一等公民”的位置，你可以像定义一个结构体 (Struct) 或类 (Class) 那样去书写它。

它是承载系统 Prompt、预设模型路由、身份角色以及工具配置的基本块（Block）。我们先来看一个最基础的定义方式：

```nexa
// 所有的属性全都在大括号内进行声明，不存在外部多余的 Client 实例化
agent FriendlyBot {
    role: "Casual conversationalist",
    model: "minimax-m2.5",
    prompt: "You are a very friendly ChatBot for casual conversations."
}
```

### 深入 Agent 属性拆解

- **`role`** (角色语义场)：定义该代理的系统角色（System Persona）。这不仅仅是一个标签，在底层编译为 Python 运行时时，它会作为系统提示词的极高权重顶层注入点，赋能模型的上下文边界。
- **`model`** (动态智脑映射)：**（极具破坏性优势的特性）**原生的模型硬线链接。这使得我们可以在不同的代理之间按需无缝切换背后的引擎（从 `gpt-4` 到轻量的开源大模型）。在其它框架中，更改模型往往意味着大改 `LLMConfig`，但在 Nexa 中只需改动这一行字符串。
- **`prompt`** (任务执行描述)：这是驱动模型行动的核心指令区，支持多行纯文本字面量表达。在这里，你不需要处理转义甚至复杂的 Token 拼接，一切都自然发生。
- **`memory`** (记忆持久化)：代理的记忆模式，如 `persistent` 等。允许你的 agent 自动管理多轮对话状态，不再需要手动拼接 `messages` 历史，像原生认知一样记录上下文。
- **`stream`** (流式推写开关)：将其设置为 `"true"` 可以直接启用大模型的 Token 级流式响应。让 Agent 边思考边输出，实现对终端用户无卡顿的实时反馈。
- **`fallback`** (模型灾备降级)：由于 API RateLimit 或意外宕机导致请求失败时，通过设定 `fallback` 模型作为容灾选项，在运行时无缝切换。

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
    
    // 当该节点执行完毕，流(Flow)将自然退出
}
```

!!! info "运行时的底层机制"
    当敲下执行命令时，Nexa 编译器首先会建立静态的图节点，对传入传出的数据类型进行静态核对，确保整个脚本没有孤儿死锁。随后将其无缝转译为高效的异步 Python 运行时（利用 `asyncio`），唤醒 `HelloWorldBot` 实例。这不仅是全网最为极简的 Agent Hello World，更是最安全的一个。

---

## 🔍 内置工具的挂载与环境沙盒穿透 (`uses` 关键字)

如果仅仅是在控制台里产生字符串，大模型也不过是个会“聊天”的花瓶。真正的大模型智能体（Agent）要能与数字世界互动（比如查天气、删文件、写表格）。

在传统的 Python 胶水代码开发中，要想让大模型调用一个函数，你需要使用极其反人类的 JSON Schema 语法去手写 Function Calling 配置。并且，一旦函数签名发生变更，你的 Schema 如果忘了跟着改，整个调用链就会在运行时崩溃。

而在 Nexa 宇宙中，一切只需要一个原生的 `uses` 关键字声明！Nexa 把函数绑定逻辑通过反射机制（Reflection）直接做进了编译器。

```nexa
agent Interactor {
    // 原生语法级载入沙盒环境包
    uses [std.ask_human, std.os.file_read]
    
    prompt: "当遇到不确定的风险操作时，优先调用 ask_human 将情况反馈给人类审查并获取许可。必要时使用 file_read 查阅本地配置。"
}
```

!!! success "从根本上消灭 Schema 烦恼"
    上文中使用的 `std.ask_human` 和 `std.os.file_read` 是 Nexa 内置标准包。当使用 `uses` 装载后，**Nexa 的编译器会在背后自动爬取这些 Python 工具内部的函数签名与 `docstring`，并将它们编译组装为各大模型厂商适配的 Native Function Calling Payload！**这意味着开发者完全不需要手写 JSON，甚至不需要思考不同模型对工具调用的不同要求。它甚至支持通过类型提示来进行参数验证！

---

## 本章小结

在这一章里，我们见识了如何使用极少的代码定义具备特定属性与沙盒环境穿透能力的 `agent`；我们还看到了如何让它们在 `flow` 枢纽内通过简单的 `.run()` 唤醒工作。

但这仅仅发挥出大语言模型单打独斗（Single-Agent Task）的实力。真实的业务系统充满复杂冗长的协同交错：如何让十几个分工明确的代理接力完成任务？又该如何在各执一词的代理间达成完美共识？

不要眨眼，这正是下一章 **多 Agent 调度与控制（高级特性）** 将为你呈现的真正编排魔法。
