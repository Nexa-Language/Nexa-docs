---
comments: true
---

# 5. 未来展望与已实现里程碑

## ✅ 已实现里程碑

| 蓝图 | 状态 | 版本 |
|------|------|------|
| Rust AVM 底座 | ✅ | v1.0-alpha (0 errors, 0 warnings) |
| WASM 安全沙盒 | ✅ | v1.0-alpha (wasmtime v21) |
| 智能调度器 | ✅ | v1.0-alpha |
| 向量虚存分页 | ✅ | v1.0-alpha |
| HITL: wait_for_human() | ✅ | v0.9.7 |
| reason() 原语 | ✅ | v0.9.7 |
| RBAC 权限控制 | ✅ | v0.9.6-rc |
| 传统控制流 | ✅ | v1.0.1-beta |
| IDD 意图驱动开发 | ✅ | v1.1.0 (104 tests) |
| Design by Contract | ✅ | v1.2.0 (47 tests) |
| 16 项 v1.3.x 特性 | ✅ | v1.3.0-v1.3.7 |
| Harness Native Runtime | ✅ | v2.0 (296 tests) |
| Agent 级属性原语 | ✅ | v2.1 |

## 🔮 未来展望

在 Nexa 核心团队（Genesis Team）的架构蓝图中，下一阶段的重点方向：

---

## 🚦 细粒度资源断点与 `@limit` (Resource Governance) 

当我们在谈论“云原生微服务”时，我们讨论的是 CPU/Memory 的限制；但在“智能体原生 (Agent-Native)”时代，最大的风险实际上是**不可控的 Token 费用滑点**。
试想一下，如果因为大模型陷入了某种罕见的逻辑死胡同，触发了无限重试调用，一个晚上的时间这台机器可能会为你产生高达数千美元的 API 账单！

在传统的应用中，成本控制往往散落在业务逻辑层的各种充当补丁的微服务或中间件里。Nexa 决定在编译器层面提供一等公民级别的装饰器机制以锁死物理边界：

```nexa
// 这是在 v0.8 提案中的资源防御壁垒
@limit(max_tokens=2000, context_window_trim="sliding")
@budget(max_cost="$0.50", on_exhaust="fallback_to_open_source")
agent EnterpriseCoder {
    prompt: "You are a very careful software engineer writing mission-critical systems."
    model: "claude-3-5-sonnet"
}
```

**底层机制**：Nexa 的 Runtime 会接管所有的 API 调用统计（基于精确的 Tokenizer），在每个 Chunk 流式返回时进行高频校验。一旦监测到全局或单节点达到阻断阈值，运行时不仅会直接熔断操作，还可以自动触发异常钩子（比如将后续处理无缝桥接至免费的本地小模型 `fallback_to_open_source`），在控制预算的同时保证系统的一定可用性。

---

## 🙋‍♂️ 人机协同：状态机休眠与反馈机制原生化 (HITL)

未来的高危自治系统必然不能是全自动狂奔的野马。任何涉及转账、生产环境发布、核心数据库操作的接口，都必须在关键节点（Approval Checkpoints）引入高等级的人类鉴权介入。

当前的实现往往非常笨拙：要么导致 HTTP 连接长轮询超时，要么开发者要手写极为复杂的 Redis 状态持久化来恢复对话请求。而使用 Nexa，将人类审核作为“状态机制休眠节点”，仅仅只需一行代码：

```nexa
agent DestructiveActor {
    uses [std.os.shell, std.ask_human]
    prompt: "You can execute any bash command, but you MUST ask human via ask_human BEFORE running 'rm' or 'drop'."
}
```

!!! info "挂起与恢复的黑科技 (Suspend & Resume)"
    这背后使用了极其前沿的协程持久化序列化技术。当 Nexa 引擎推断匹配并调用 `std.ask_human` 时，它会瞬间捕获当前 Agent Flow 的全部上下文栈信息，将其序列化并保存到 Memory 层，随后彻底挂起（Yielding），将宝贵的线程让出。
    直到终端（或者绑定的 Slack/Discord Webhook）注入带有审批许可的恢复信号后，这棵庞大的抽象语法树和状态机会完美地“热启动”并延续之前的推理动作。

---

## 🛠️ 多模态交织：视觉与听觉原生算符 (Multi-modal Rivers)

目前的主流框架大多仍停留在文本提示（Text Prompt）和文本生成的阶段，即便支持图片传入，用的也是极为冗长的 Base64 编码拼接代码。

既然大模型的智力已经走向多模态（Omni-modal），Nexa 的控制流算符自然也需随之进化。除了支持文本流级联调用的 `>>` 外，Nexa 正在测试引入空间与多模态数据切片通道。比如未来可能引入的富媒体管道符 `~>`：

```nexa
flow vision_and_audio_routing {
    // std.camera 将图像转化为原生的模态对象，通过 ~> 进入视觉智能体
    img = std.hardware.camera.capture() ~> UI_Designer;
    
    // 视觉和意图相互交织，判断用户的手势或画面核心意图
    match img.intent {
        "User points at screen (Redesign)" => UI_Designer >> Developer,
        "User looks confused (Explain)" => VoiceAssistant.run_audio(img)
    }
}
```

Nexa 在下一个纪元的核心愿景，就是将那些晦涩枯燥的顶级学术研究、复杂的异构多模通信手段，收敛并凝练成开发者指尖几行极具美感的声明式代码。如果你想参与这场改写软件工程史的伟大运动，请务必查看我们的「第八章：社区与生态架构」。
