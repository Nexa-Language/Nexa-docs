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

### Fire-and-Forget 操作符 `||`

并行执行多个 Agent，**不等待结果**返回。适用于通知、日志等"发射后不管"的场景。

```nexa
// Fire-and-Forget 操作符
flow main {
    notification = "System maintenance scheduled at 2AM";
    
    // 并行发送通知，不等待响应
    notification || [EmailBot, SlackBot, SMSBot];
    
    // 主流程继续执行，不会被阻塞
    print("通知已发送，继续处理其他任务...");
}
```

**流程图**：
```
         输入
           │
           ▼
    ┌──────┴──────┐
    │             │
    ▼             ▼
 EmailBot     SlackBot
    │             │
    ▼             ▼
 (后台执行)   (后台执行)
```

**使用场景**：
- 批量通知发送
- 日志记录
- 非关键任务触发

### Consensus 操作符 `&&`

并行执行多个 Agent，**等待所有结果**并进行投票/共识决策。

```nexa
// Consensus 操作符 - 多专家投票决策
flow main {
    question = "Should we approve this loan application?";
    
    // 三个专家并行评估，等待所有结果
    decision = question && [RiskAnalyst, CreditChecker, ComplianceOfficer];
    
    // decision 包含所有专家的意见，可进行投票或综合分析
    print(decision);
}
```

**流程图**：
```
              输入
               │
       ┌───────┼───────┐
       │       │       │
       ▼       ▼       ▼
   ExpertA  ExpertB  ExpertC
       │       │       │
       └───────┼───────┘
               │
               ▼
         共识决策
```

**使用场景**：
- 多专家评审
- 投票决策系统
- 交叉验证

### DAG 操作符完整对照表

| 操作符 | 名称 | 行为 | 使用场景 |
|-------|------|------|---------|
| `>>` | 管道 | 顺序传递 | 单向流水线 |
| `|>>` | 分叉 | 并行发送到多个 Agent | 并行处理 |
| `&>>` | 合流 | 等待多个结果后合并 | 结果整合 |
| `??` | 条件分支 | 根据条件选择路径 | 智能路由 |
| `||` | Fire-forget | 并行执行不等待 | 异步通知 |
| `&&` | Consensus | 并行执行等待所有结果 | 投票决策 |

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

## 🔗 函数管道操作符 `|>` (v1.3.x)

与 Agent 管道 `>>` 不同，`|>` 是**函数级**管道操作符：将左侧的值作为右侧函数的第一个参数传入。这让你可以像 Unix 管道一样链式调用标准库工具和自定义函数。

### 基本语法

```nexa
// x |> f  等价于  f(x)
// x |> f |> g  等价于  g(f(x))
```

### 与 Agent 管道 `>>` 的区别

| 操作符 | 级别 | 语义 | 示例 |
|-------|------|------|------|
| `>>` | Agent 级 | `B.run(A.run(input))` | `input >> Translator >> Reviewer` |
| `|>` | 函数级 | `f(x)` | `data |> json_parse |> json_get` |

### 完整示例

```nexa
flow main {
    raw_text = '{"name": "Nexa", "version": "1.3"}';
    
    // 函数管道：解析 JSON → 提取字段 → 格式化
    result = raw_text
        |> std.json.json_parse
        |> std.json.json_get("name");
    
    print(result);  // 输出: Nexa
    
    // 与字符串插值组合
    greeting = "Hello, #{result}!";
    print(greeting);  // 输出: Hello, Nexa!
}
```

!!! tip "何时使用 `|>` vs `>>`"
    - 处理**数据变换**（JSON 解析、文本处理、数学计算）时使用 `|>`
    - 处理**Agent 串联**（翻译→校对→格式化）时使用 `>>`
    - 两者可以组合：`input |> preprocess |> format >> Agent1 >> Agent2`

---

## ❓ 空值合并操作符 `??` (v1.3.x)

`??` 在 DAG 操作符中用于条件分支，但在 v1.3.x 中它还承担了**空值合并**的角色：当左侧为 `None`、`Option::None` 或空字典时，返回右侧的默认值。

### 基本语法

```nexa
// value ?? fallback
// 如果 value 为 None/Option::None/空dict，返回 fallback
// 否则返回 value 本身
```

### 完整示例

```nexa
flow main {
    // KV 存储中键可能不存在
    user_name = kv.get("user_name") ?? "Guest";
    
    // Agent 可能返回 Option::None
    result = Analyzer.run(input) ?? "No analysis available";
    
    // 数据库查询可能返回空
    record = db.query_one("SELECT * FROM users WHERE id = 1") ?? {"name": "Unknown"};
    
    print(user_name);   // Guest（如果键不存在）
    print(result);      // No analysis available（如果 Agent 返回 None）
}
```

!!! warning "注意 `??` 的双重语义"
    - 在 DAG 上下文中：`input ?? AgentA : AgentB` 表示条件分支
    - 在表达式上下文中：`value ?? fallback` 表示空值合并
    - 编译器根据上下文自动区分两种用法

---

## ⏳ 延迟执行 `defer` (v1.3.x)

`defer` 语句将表达式推迟到当前作用域退出时执行，遵循 **LIFO（后进先出）** 顺序。常用于资源清理、日志记录和事务回滚。

### 基本语法

```nexa
defer expression;
// expression 会在当前 scope 退出时执行（LIFO 顺序）
```

### 完整示例

```nexa
flow main {
    db_handle = std.db.sqlite.connect("data.db");
    defer std.db.sqlite.close(db_handle);  // 退出时自动关闭连接
    
    kv_handle = std.kv.open(":memory:");
    defer std.kv.flush(kv_handle);  // 退出时自动刷新 KV
    
    // 正常业务逻辑
    std.db.sqlite.execute(db_handle, "INSERT INTO users VALUES (1, 'Alice')");
    result = std.db.sqlite.query(db_handle, "SELECT * FROM users");
    
    // 无论正常退出还是异常，defer 都会按 LIFO 执行：
    // 1. 先 flush KV
    // 2. 再 close DB
}
```

!!! tip "defer 执行顺序"
    多个 `defer` 按 **LIFO** 顺序执行（类似 Go/Rust 的 defer）：
    ```nexa
    defer print("first");   // 最后执行
    defer print("second");  // 第二执行
    defer print("third");   // 最先执行
    // 输出顺序: third → second → first
    ```

---

## 🎯 模式匹配 (v1.3.x)

Nexa v1.3.x 引入了强大的模式匹配系统，支持 7 种模式类型，让你可以优雅地解构和处理复杂数据结构。

### 基本语法

```nexa
match value {
    Pattern1 => expression1,
    Pattern2 => expression2,
    _ => default_expression
}
```

### 支持的模式类型

| 模式类型 | 语法 | 示例 |
|---------|------|------|
| 通配符模式 | `_` | `_ => "default"` |
| 变量绑定模式 | `name` | `x => x + 1` |
| 字面量模式 | `value` | `0 => "zero"` |
| 构造器模式 | `Type::Variant(args)` | `Option::Some(v) => v` |
| 元组模式 | `(a, b, ...)` | `(x, y) => x + y` |
| 字段模式 | `{field: pattern}` | `{name: n} => n` |
| 或模式 | `P1 | P2` | `1 | 2 => "small"` |

### 完整示例

```nexa
flow main {
    // 匹配 Option 类型
    result = Analyzer.run(input);
    
    match result {
        Option::Some(data) => print("Got data: #{data}"),
        Option::None => print("No data available"),
        _ => print("Unexpected result")
    }
    
    // 匹配 Result 类型
    response = http_get("https://api.example.com/data");
    
    match response {
        Result::Ok(body) => process(body),
        Result::Err(error) => print("Error: #{error}"),
        _ => print("Unknown response")
    }
    
    // 解构元组
    coords = (10, 20);
    match coords {
        (0, 0) => print("Origin"),
        (x, 0) => print("On x-axis at #{x}"),
        (0, y) => print("On y-axis at #{y}"),
        (x, y) => print("At (#{x}, #{y})")
    }
    
    // 解构 struct
    match user_record {
        {name: n, age: a} => print("#{n} is #{a} years old"),
        {name: n} => print("#{n}, age unknown")
    }
}
```

### Let 解构

```nexa
// 在 let 语句中直接解构
let (x, y) = coords;
let {name: user_name, age: user_age} = user_record;
let Option::Some(value) = result;  // 如果是 None 则抛出 PatternMatchError
```

### For 解构

```nexa
// 在 for 循环中解构
for each (key, value) in kv.list(kv_handle) {
    print("#{key}: #{value}");
}
```

---

## 🏗️ 代数数据类型：Struct、Enum、Trait (v1.3.x)

Nexa v1.3.x 引入了完整的 ADT（代数数据类型）系统，包括结构体（Struct）、枚举（Enum）和特质（Trait），为 Agent 数据建模提供类型安全的基础。

### Struct 声明

```nexa
struct Point {
    x: Int,
    y: Int
}

struct User {
    name: String,
    age: Int,
    email: Option[String]
}
```

### 创建 Struct 实例

```nexa
// 使用 Field Init 表达式
p = Point { x: 10, y: 20 };
u = User { name: "Alice", age: 30, email: Option::Some("alice@example.com") };
```

### Enum 声明

```nexa
enum Color {
    Red,
    Green,
    Blue
}

enum Option[T] {
    Some(T),
    None
}

enum Result[T, E] {
    Ok(T),
    Err(E)
}
```

### 创建 Enum Variant

```nexa
// Variant Call 表达式
c = Color::Red;
some_val = Option::Some(42);
none_val = Option::None;
ok_result = Result::Ok("success");
err_result = Result::Err("file not found");
```

### Trait 声明与 Impl

```nexa
// 定义 Trait
trait Printable {
    fn format() -> String
}

trait Serializable {
    fn to_json() -> String
    fn from_json(data: String) -> Self
}

// 为类型实现 Trait
impl Printable for Point {
    fn format() -> String {
        "Point(#{self.x}, #{self.y})"
    }
}

impl Printable for User {
    fn format() -> String {
        "#{self.name} (age: #{self.age})"
    }
}
```

### ADT 与模式匹配组合

```nexa
// Struct + 模式匹配
match shape {
    Point { x: 0, y: 0 } => "Origin",
    Point { x, y } => "At (#{x}, #{y})"
}

// Enum + 模式匹配
match result {
    Result::Ok(data) => process(data),
    Result::Err(msg) => handle_error(msg)
}

// Trait 方法调用
formatted = p.format();  // 调用 Printable trait 的 format 方法
```

!!! info "ADT 运行时实现"
    Nexa 的 ADT 在运行时采用 **handle-as-dict** 模式：所有 struct 实例和 enum variant 在底层都是字典，带有 `_nexa_type`、`_nexa_variant` 等 prefixed key。这使得 ADT 可以无缝与 Agent 的 JSON 输出交互。

---

## 📊 本章小结

在本章中，我们学习了 Nexa 的高级编排特性：

| 特性 | 关键字 | 版本 | 用途 |
|-----|-------|------|------|
| Agent 管道 | `>>` | v0.5+ | Agent 串联 |
| 函数管道 | `|>` | v1.3.x | 函数链式调用 |
| 意图路由 | `match intent` | v0.5+ | 请求分发 |
| 分叉操作 | `|>>` | v0.9.7+ | 并行处理 |
| 合流操作 | `&>>` | v0.9.7+ | 结果整合 |
| DAG 条件分支 | `??` | v0.9.7+ | 路径选择 |
| 空值合并 | `??` | v1.3.x | None 默认值 |
| 语义循环 | `loop until` | v0.5+ | 迭代优化 |
| 语义条件 | `semantic_if` | v0.5+ | 智能判断 |
| 异常处理 | `try/catch` | v0.9.5+ | 错误处理 |
| 延迟执行 | `defer` | v1.3.x | 资源清理 |
| 模式匹配 | `match` | v1.3.x | 数据解构 |
| 代数数据类型 | `struct/enum/trait` | v1.3.x | 类型安全建模 |

这些特性让 Nexa 能够优雅地处理最复杂的智能体编排场景，从简单的流水线到复杂的 DAG 拓扑，从确定性的分支到语义级别的条件判断，再到类型安全的数据建模。

---

## 🔗 相关资源

- [完整示例集合](examples.md) - 查看更多 DAG 操作符示例
- [语法扩展](part3_extensions.md) - 学习 Protocol 与契约高级用法
- [语言参考手册](reference.md) - 查看完整语法规范
- [最佳实践](part6_best_practices.md) - 企业级开发经验
