---
comments: true
---

# 3. 高级特性：复杂智能体网络的编排 (Orchestration)

如果说用 `agent` 关键字定义角色只是在打造单个齿轮，那么 Nexa 宇宙中真正的"工业革命"体现在它无可比拟的**协作编排网络**。

Nexa 从 v0.5 架构升级以来的核心设计护城河，就是将复杂的、充斥着异步和竞态条件的多阶段智能体交互提升到了**语言关键字（Language Keywords）**的级别。在本章，我们将详细探讨在企业级 Agent 框架中如何利用管道 (`>>`)、意图路由 (`match intent`)、并发聚合 (`join`)、DAG 操作符以及不可思议的语义循环 (`loop until`)。

---

## 🛤️ 管道操作符：`>>` (流水线数据总线)

在绝大多数任务（如学术翻译、代码编写与测试链）中，多智能体协同只是一条纯粹的流水线：前一个 Agent 的输出（Output Task）以及它所处的历史上下文，应该毫无保留、零损耗地作为输入交给下一个 Agent。

### 传统写法的痛点

如果我们用以 LangChain 为代表的传统写法构建这条链段：

```python
# 传统语言的痛点：充斥中间变量与隐式状态丢失
draft = Writer.run(topic)
translated_draft = Translator.run(draft)
reviewer_feedback = Reviewer.run(translated_draft)
```

你会发现，你不但定义了一堆只用一次的中间变量（导致内存管理不佳），还极易因为类型包装（如 `BaseMessage` 对象与普通 `str`）的不同而抛出各种运行时错误。

### Nexa 管道操作符

在 Nexa 中，我们可以用极富表达力的 Unix-like 管道操作符 `>>` 一气呵成：

```nexa
// 摘自 Nexa 实战代码集 (Pipeline Pattern)
flow main {
    res = Coder.run("Generate a fast sorting algorithm in Python") >> Reviewer >> HumanInterface;
    
    // 返回结果直接将是流水线末端（HumanInterface）产出的最终形态
}
```

### 管道操作符详解

| 操作 | 等价代码 | 说明 |
|-----|---------|------|
| `A >> B` | `B.run(A.run(input))` | 将 A 的输出传给 B |
| `A >> B >> C` | `C.run(B.run(A.run(input)))` | 三阶段流水线 |
| `input >> A >> B` | `B.run(A.run(input))` | 从输入开始 |

!!! success "优雅背后的编译器魔法"
    当你打出 `A >> B` 时，Nexa 编译器不会将其简单转译成了线性的函数阻塞调用。在底层，Nexa 的 Orchestrator 会自动构建 DAG（有向无环图），它保留了从 `Coder` 到 `Reviewer` 的会话窗偏移（Context Sliding Window），并严格遵循 Promise 就绪态去激活下一个节点。这为你省去了无数行状态维护代码。

### 管道操作符完整示例

```nexa
// 翻译流水线
agent Translator {
    role: "专业翻译",
    prompt: "将英文翻译成中文，保持原意，语言流畅"
}

agent Proofreader {
    role: "校对编辑",
    prompt: "校对译文，修正错误，润色语言"
}

agent Formatter {
    role: "格式化专家",
    prompt: "将文本整理为标准格式"
}

flow main {
    english_text = "Artificial intelligence is transforming the world.";
    
    // 三阶段管道
    final_result = english_text >> Translator >> Proofreader >> Formatter;
    
    print(final_result);
}
```

**运行结果**：
```
人工智能正在改变世界。
```

---

## 🔀 意图路由：`match intent` 协议

用户的指令永远是变幻莫测的。在很多客服/支持机器人中，有的用户想要查询天气，有的想发邮件，还有的只是单纯地想听个笑话找人聊天。

如果我们使用一个"超级大模型"来处理所有任务：

1. 它在收到无关紧要的话语时也会消耗大量计费 Token。
2. 上下文严重污染，在回答闲聊时可能会错误触发系统高危的"删库"工具。

因此，业界高并发系统常常推崇"前置微型路由分类器"（NLU/Intent Router）以实现削峰填谷，再将实际处理交给后面挂载的领域专精 Agent（Domain Experts）。

### 基本语法

```nexa
match user_input {
    intent("意图描述1") => Agent1.run(user_input),
    intent("意图描述2") => Agent2.run(user_input),
    _ => DefaultAgent.run(user_input)  // 默认分支
}
```

### 完整示例

```nexa
// Nexa 实战：多意图路由
flow main {
    req = "Tell me what is happening in the global tech world today!";
    
    // 利用自然语义与意图匹配机制，直接解耦冗长脆弱的 if-else
    match req {
        intent("Check local weather") => WeatherBot.run(req) >> Translator,
        intent("Check daily news")    => NewsBot.run(req) >> Translator,
        _ => SmallTalkBot.run(req)
    }
}
```

### 意图路由流程图

```
用户输入
    │
    ▼
┌─────────────────────┐
│  意图分类器（内置）   │
│  Embedding + 相似度  │
└─────────────────────┘
    │
    ├── intent("天气") ──────► WeatherBot
    │
    ├── intent("新闻") ──────► NewsBot
    │
    └── 默认 (_) ────────────► SmallTalkBot
```

!!! info "解析 `intent()` 底层实现"
    在这里 `intent("...")` 本质上并不是简单的字符串或正则比对。Nexa 内部搭载了一个专门处理意图分类的超轻量级 Embeddings 匹配模型。在后台它会极速得出与各个分支 `Condition` 的余弦相似度，将执行流无缝劈开进入最合适的分支。在 Python 中实现类似机制，你至少需要维护一个 ChromaDB 服务和复杂的 Top-K 检索池。

### 意图路由最佳实践

1. **意图描述要具体**：避免模糊的描述
2. **设置合理的默认分支**：处理未知意图
3. **考虑使用快速模型**：意图分类不需要复杂推理

```nexa
// ✅ 好的意图描述
intent("查询天气预报或当前天气状况")
intent("查询股票价格或金融数据")
intent("预订机票、酒店或餐厅")

// ❌ 不好的意图描述
intent("天气")  // 太模糊
intent("其他")  // 没有实际意义
```

---

## 🕸️ DAG 拓扑编排：终极多路分叉与聚合 (v0.9.7+)

在涉及智力密集型任务（诸如投资研报生成或者核心系统疑难代码调优）时，必须通过多角色"背靠背"分别独立研究，然后再汇总交叉讨论。Nexa v0.9.7 极具革命性地引入了原生处理复杂图结构（DAG）的拓扑操作符。

### DAG 操作符总览

| 操作符 | 名称 | 说明 | 示例 |
|-------|------|------|------|
| `>>` | 管道 | 顺序传递 | `A >> B` |
| `|>>` | 分叉 (Fan-out) | 并行发送到多个 Agent | `input |>> [A, B, C]` |
| `&>>` | 合流 (Merge/Fan-in) | 合并多个结果到一个 Agent | `[A, B] &>> C` |
| `??` | 条件分支 | 根据条件选择路径 | `input ?? A : B` |
| `||` | 异步分叉 | 发送后不等待结果 | `input || [A, B]` |
| `&&` | 共识合流 | 需要所有 Agent 达成一致 | `[A, B] && Judge` |

### 分叉操作符 `|>>` (Fan-out)

将上游数据**并行克隆**发送到多个 Agent，等待所有结果返回。

```nexa
// 分叉操作符 - 并行发送到多个 Agent
flow main {
    topic = "Quantum Computing Applications";
    
    // 将 topic 同时发送给三个 Agent 并行处理
    results = topic |>> [Researcher, Analyst, Writer];
    
    // results 是一个数组，包含三个 Agent 的输出
    print(results);
}
```

**流程图**：
```
       topic
         │
         ├──────────┬──────────┐
         │          │          │
         ▼          ▼          ▼
    Researcher   Analyst    Writer
         │          │          │
         └──────────┴──────────┘
                    │
                    ▼
               [结果数组]
```

**使用场景**：
- 多角度分析同一问题
- 多语言翻译
- 多模型对比验证

### 合流操作符 `&>>` (Merge/Fan-in)

将多个 Agent 的输出**合并**后发送给下游 Agent。

```nexa
// 合流操作符 - 合并多个 Agent 的输出
flow main {
    // 等待 Researcher 和 Analyst 完成
    // 将两者的输出合并发给 Reviewer
    final_report = [Researcher, Analyst] &>> Reviewer;
    
    print(final_report);
}
```

**流程图**：
```
    Researcher ────┐
                   │
                   ▼
               Reviewer ──► 最终输出
                   ▲
                   │
    Analyst ───────┘
```

**使用场景**：
- 多源信息汇总
- 专家会诊
- 交叉验证

### 条件分支操作符 `??`

根据输入特征**自动选择**执行路径。

```nexa
// 条件分支操作符
flow main {
    user_query = "URGENT: System outage detected";
    
    // 根据输入内容自动选择处理 Agent
    handled = user_query ?? UrgentHandler : NormalHandler;
    
    print(handled);
}
```

**流程图**：
```
         输入
          │
          ▼
    ┌─────────────┐
    │  条件判断   │
    └─────────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
UrgentHandler  NormalHandler
    │           │
    └─────┬─────┘
          │
          ▼
        输出
```

**使用场景**：
- 紧急程度分类
- 简单/复杂任务分流
- 不同类型请求处理

### 组合 DAG 操作符

构建复杂的处理流程：

```nexa
// 摘自 Nexa 代码示例 15_dag_topology.nx
flow main {
    topic = "Quantum Computing business impact";

    // 1. 分叉：topic 分别喂给 Tech 与 Biz 两个研究员并行分析
    // 2. 合流：等两人产出后，汇总发给 Summarizer 打包撰写最终报告
    final_report = topic |>> [Researcher_Tech, Researcher_Biz] &>> Summarizer;

    // 分支路由：如果报告异常，使用备用机器人；否则执行日志打印并下发
    final_report ?? RecoveryBot : Logger;
}
```

**完整流程图**：
```
                    topic
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Researcher_Tech         Researcher_Biz
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
                  Summarizer
                      │
                      ▼
              final_report
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    RecoveryBot               Logger
    (异常情况)              (正常情况)
```

### DAG 操作符完整示例

```nexa
// DAG 拓扑示例 - 研报生成系统
agent Researcher_Tech {
    role: "技术研究员",
    model: "deepseek/deepseek-chat",
    prompt: "分析量子计算的技术层面影响"
}

agent Researcher_Biz {
    role: "商业研究员",
    model: "deepseek/deepseek-chat",
    prompt: "分析量子计算的商业层面影响"
}

agent Summarizer {
    role: "报告撰写员",
    model: "deepseek/deepseek-chat",
    prompt: "整合研究结果，撰写综合报告"
}

agent UrgentHandler {
    role: "紧急处理专员",
    prompt: "快速处理紧急问题"
}

agent NormalHandler {
    role: "标准处理专员",
    prompt: "按标准流程处理"
}

flow main {
    // 示例1: 简单管道
    simple_result = "What is AI?" >> Researcher_Tech >> Summarizer;
    
    // 示例2: 分叉 - 并行处理
    parallel_results = "Quantum Computing" |>> [Researcher_Tech, Researcher_Biz];
    
    // 示例3: 合流 - 整合结果
    merged_report = [Researcher_Tech, Researcher_Biz] &>> Summarizer;
    
    // 示例4: 条件分支
    urgent_query = "URGENT: 系统崩溃！";
    handled = urgent_query ?? UrgentHandler : NormalHandler;
    
    // 示例5: 复杂组合
    complex_flow = "AI trends 2024" 
        |>> [Researcher_Tech, Researcher_Biz] 
        &>> Summarizer;
}
```

---

## 🔁 语义审查与反思循环：`loop ... until`

在很多自动化编程、长文本协作应用中，业界总结出必须采用"自我审校（Reflective Critic）"机制：即 `模型 A 产出稿件 -> 模型 B 担任审查者纠错 -> 模型 A 接收错误反馈重写`。

传统语言如何处理这个逻辑？开发者需要手写一层极其脆弱的 `while True`，然后用几行极其变扭的正则 `if "SUCCESS" in text: break` 祈祷大模型能精准输出跳出词。

Nexa 的哲学是：**既然连计算都是靠大模型完成的，判断逻辑为何不能原生地交还给语义场呢？**这就催生了针对语义结束条件的**语言级循环引擎**。

### 基本语法

```nexa
loop {
    // 循环体
} until ("自然语言终止条件")
```

### 完整示例

```nexa
flow main {
    // 第一步初代产出
    poem = Writer.run("Write a beautiful poem about AGI.");
    
    loop {
        // 利用管线思维获取批判反馈
        feedback = Critic.run(poem);
        
        // 利用反馈作为语境指导，原地重写(Mutate)
        poem = Editor.run(poem, feedback);
        
    // 全领域仅此一家：自然语言判定跳出条件
    } until ("The poem effectively rhymes and crucially mentions the technological singularity")
}
```

### 防止无限循环

使用循环计数器保护：

```nexa
flow critic_pipeline(task: string) {
    loop {
        draft = Writer.run(task);
        feedback = Reviewer.run(draft);
        
    // 结合自然语言语义推演和编程强逻辑拦截（双保险机制）
    } until ("Code has exactly 0 bugs inside feedback" or runtime.meta.loop_count >= 4)
    
    // 如果是因为触碰了次数墙，可以抛出人工拦截异常
    if (runtime.meta.loop_count >= 4) {
        raise SuspendExecution("Reviewer and Writer entered deadlock. Need Human Check.");
    }
}
```

### 循环控制变量

Nexa 在循环中提供以下内置变量：

| 变量 | 说明 |
|-----|------|
| `runtime.meta.loop_count` | 当前循环次数 |
| `runtime.meta.last_result` | 上一次循环的结果 |

---

## 🔧 语义条件判断：`semantic_if`

除了 `loop until`，Nexa 还提供了 `semantic_if` 用于语义级别的条件判断。

### 基本语法

```nexa
semantic_if "自然语言条件" against input_variable {
    // 条件为真时执行
} else {
    // 条件为假时执行
}
```

### 快速匹配模式

使用 `fast_match` 进行正则预过滤，避免不必要的 LLM 调用：

```nexa
semantic_if "包含具体的日期和地点" fast_match r"\d{4}-\d{2}-\d{2}" against user_input {
    schedule_tool.run(user_input);
} else {
    print("需要进一步澄清");
}
```

!!! tip "fast_match 工作原理"
    1. 首先用正则表达式快速检查
    2. 如果正则匹配，直接进入分支（节省 Token）
    3. 如果正则不匹配，仍会调用 LLM 进行语义判断

### 完整示例

```nexa
flow main {
    user_input = '{"name": "张三", "age": 25}';
    
    // 语义条件判断 - 判断是否为 JSON
    semantic_if "输入内容是有效的 JSON 格式" fast_match r"^\s*[\[{]" against user_input {
        result = JSONProcessor.run(user_input);
        print("作为 JSON 处理：" + result);
    } else {
        result = TextProcessor.run(user_input);
        print("作为文本处理：" + result);
    }
}
```

---

## 🧩 异常处理：`try/catch`

Nexa v0.9.5 引入了原生的异常处理机制。

### 基本语法

```nexa
try {
    // 可能出错的代码
} catch (error) {
    // 错误处理
}
```

### 完整示例

```nexa
flow main {
    try {
        result = RiskyAgent.run("dangerous operation");
        print(result);
    } catch (error) {
        print("发生错误：" + error);
        // 使用备用方案
        result = FallbackAgent.run("safe operation");
    }
}
```

---

## 📊 本章小结

在本章中，我们学习了 Nexa 的高级编排特性：

| 特性 | 关键字 | 用途 |
|-----|-------|------|
| 管道操作 | `>>` | Agent 串联 |
| 意图路由 | `match intent` | 请求分发 |
| 分叉操作 | `|>>` | 并行处理 |
| 合流操作 | `&>>` | 结果整合 |
| 条件分支 | `??` | 路径选择 |
| 语义循环 | `loop until` | 迭代优化 |
| 语义条件 | `semantic_if` | 智能判断 |
| 异常处理 | `try/catch` | 错误处理 |

这些特性让 Nexa 能够优雅地处理最复杂的智能体编排场景，从简单的流水线到复杂的 DAG 拓扑，从确定性的分支到语义级别的条件判断。

---

## 🔗 相关资源

- [完整示例集合](examples.md) - 查看更多 DAG 操作符示例
- [语法扩展](part3_extensions.md) - 学习 Protocol 高级用法
- [最佳实践](part6_best_practices.md) - 企业级开发经验
