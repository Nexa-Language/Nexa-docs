---
comments: true
---

# 4. 语法扩展：契约、类型与协议 (Protocols & Types)

在前面我们学习了宏观的、具有拓扑结构的路由控制流。但在真实的、冷酷的企业级生产环境中，最致命的永远是**大模型的非结构化输出**机制带来的不可确定性。

传统的微服务之间使用 Thrift, gRPC 或 RESTful 协议交换严格的 JSON。然而大模型随时可能给你返回一段充满思考和语气的 "Here is your result:\n {...}"。这将轻易击穿后续 Java/Go 系统脆弱的解码器（Decoder）。

本章着眼于介绍 Nexa 针对该痛点独创的高阶重塑特性：**类型协议 (Protocols)** 和 **多模智能路由**。它们是系统稳定性的压舱石。

---

## 📜 引入 `protocol` 关键字 (编译器级别的 Pydantic)

只要业务流需要被下游其他非大语言模型服务（如数据库写入、前端渲染）所消费，我们就必须强制约束大模型仅仅返回特定格式的数据。

以往，你需要导入复杂的 JSON 解析工具（比如 Python 中的 `Pydantic` 或者 TypeScript 的 `Zod`），再将 Schema 序列化为数十行的 JSON 约束强行附加在 Prompt 的末尾。

在 Nexa 语言中，我们直接将约束语法提权成了第一公民，像定义 `struct` 或是 `class` 那样使用 `protocol`。

### 基本语法

```nexa
// Nexa 语言内建的协议定义，支持丰富的类型系统
protocol ReviewResult {
    score: "int",
    summary: "string",
    bug_list: "list[string]",
    is_critical: "boolean"
}
```

### 支持的类型

| 类型 | 说明 | 示例值 |
|-----|------|--------|
| `"string"` | 字符串 | `"hello"` |
| `"int"` | 整数 | `42` |
| `"float"` | 浮点数 | `3.14` |
| `"boolean"` | 布尔值 | `true` |
| `"list[string]"` | 字符串列表 | `["a", "b"]` |
| `"list[int]"` | 整数列表 | `[1, 2, 3]` |
| `"dict"` | 字典 | `{"key": "value"}` |

### 类型标注规范

!!! warning "重要：类型必须是字符串"
    在 `protocol` 中，类型必须用引号包裹：

    ```nexa
    // ✅ 正确
    protocol UserInfo {
        name: "string",
        age: "int"
    }
    
    // ❌ 错误 - 类型没有引号
    protocol UserInfo {
        name: string,  // 编译错误！
        age: int       // 编译错误！
    }
    ```

---

## 🛡️ `implements` 实现保障与黑箱重试机制

定义完协议只是第一步，Agent 应该如何与其产生强制交集？只需要用我们再熟悉不过的面向对象语言当中的继承逻辑——`implements` 接口继承即可。

### 基本用法

```nexa
@limit(max_tokens=600)
agent Coder {
    prompt: "Write a short Python implementation of quicksort.",
    model: "minimax/minimax-m2.5"
}

// Reviewer 这个模型将受到契约约束，确保最终系统只能收到干净的 JSON 属性实体。
agent Reviewer implements ReviewResult {
    prompt: "Review the provided code. Provide your score and list all bugs.",
    model: "deepseek/deepseek-chat"
}

flow main {
    // 整个数据结构将无缝作为 Python Object/JSON 传入外部 API
    result = Coder.run("Generate Quicksort") >> Reviewer;
    
    // result 是一个结构化对象，可以直接访问属性
    print("Score: " + result.score);
    print("Summary: " + result.summary);
}
```

### 运行时魔法：自动重试纠偏

!!! warning "这是你在常规系统里绝不可能轻松写出的机制"
    表面上看，`implements` 只是绑定了一个声明。但在背地里，大模型有时候依然会犯病（比如只给了 `score` 却忘了给 `bug_list`，或者把 `is_critical` 错误地拼成字符串 "true"）。
    
    遇到这种情况，你以前的 Python 脚本由于 `JSONDecodeError` 肯定当场崩溃了。
    
    **但是在 Nexa 的防线中，底层 Evaluator 会拦截这笔返回 Token，立即对比 Schema。如果发现类型脱轨——它会自动将 Pydantic/Traceback 的报错信息转换为自然语言塞回去，静默触发模型的"二次内省"！**
    
    ```
    "对不起，你的输出少了 bug_list，请修正并重新输出"
    ```
    
    这一整个轮回对前台代码编写者是**完全无感**的。

### 自动修正流程

```
LLM 输出
    │
    ▼
┌─────────────────────┐
│   Schema 验证器     │
└─────────────────────┘
    │
    ├── 验证通过 ──────► 返回结构化对象
    │
    └── 验证失败
            │
            ▼
    ┌─────────────────────┐
    │  生成错误反馈信息   │
    └─────────────────────┘
            │
            ▼
    ┌─────────────────────┐
    │  自动重新请求 LLM   │
    └─────────────────────┘
            │
            └──► 最多重试 3 次
```

---

## 🎯 Protocol 使用场景详解

### 场景 1：结构化数据提取

当你需要从非结构化文本中提取结构化数据时，Protocol 是最佳选择。

```nexa
// 定义输出协议
protocol UserInfo {
    name: "string",
    age: "int",
    occupation: "string",
    location: "string"
}

agent InfoExtractor implements UserInfo {
    role: "信息提取专家",
    prompt: """
    从用户输入中提取个人信息。
    如果某个字段无法确定，填写 "未知"。
    """
}

flow main {
    user_input = "我叫张三，今年28岁，在北京做软件工程师";
    
    result = InfoExtractor.run(user_input);
    
    // 结果是结构化的
    print("姓名：" + result.name);        // 张三
    print("年龄：" + result.age);          // 28
    print("职业：" + result.occupation);   // 软件工程师
    print("地点：" + result.location);     // 北京
}
```

### 场景 2：API 响应格式约束

当你需要 Agent 输出可直接被 API 消费的数据时：

```nexa
// 定义 API 响应格式
protocol APIResponse {
    status: "string",      // "success" 或 "error"
    code: "int",           // HTTP 状态码
    data: "dict",          // 响应数据
    message: "string"      // 消息
}

agent APIHandler implements APIResponse {
    prompt: "处理用户请求并返回标准 API 响应格式"
}

flow main {
    request = "查询用户 ID 为 123 的订单";
    response = APIHandler.run(request);
    
    // 可以直接返回给前端
    return response;  // {"status": "success", "code": 200, ...}
}
```

### 场景 3：多 Agent 数据传递

当你需要确保 Agent 之间数据格式一致时：

```nexa
// 定义统一的研究报告格式
protocol ResearchReport {
    title: "string",
    summary: "string",
    key_findings: "list[string]",
    confidence: "float"  // 0.0 - 1.0
}

agent Researcher implements ResearchReport {
    role: "研究员",
    prompt: "研究指定主题并生成结构化报告"
}

agent Reviewer {
    role: "审查员",
    prompt: "审查研究报告的完整性和准确性"
}

agent Formatter {
    role: "格式化专家",
    prompt: "将研究报告格式化为最终输出"
}

flow main {
    topic = "2024年 AI 行业趋势";
    
    // Researcher 输出结构化数据
    report = Researcher.run(topic);
    
    // Reviewer 接收结构化数据
    review = Reviewer.run(report);
    
    // Formatter 最终处理
    final = Formatter.run(report);
    
    print(final);
}
```

### 场景 4：表单数据处理

```nexa
protocol ContactForm {
    name: "string",
    email: "string",
    phone: "string",
    message: "string",
    priority: "string"  // "high", "medium", "low"
}

agent FormProcessor implements ContactForm {
    prompt: "从用户输入中提取联系表单信息"
}

flow main {
    user_input = """
    你好，我是李四，邮箱是 lisi@example.com。
    电话 138-1234-5678。
    我想咨询一下产品价格问题，希望能尽快回复。
    """;
    
    form = FormProcessor.run(user_input);
    
    // 可以直接保存到数据库
    save_to_database(form);
}
```

### 场景 5：分类与标签

```nexa
protocol ClassificationResult {
    category: "string",
    confidence: "float",
    tags: "list[string]",
    reasoning: "string"
}

agent Classifier implements ClassificationResult {
    prompt: "对输入内容进行分类，提供分类结果和置信度"
}

flow main {
    content = "新款 iPhone 15 发布，搭载 A17 芯片";
    
    result = Classifier.run(content);
    
    print("分类：" + result.category);     // "科技新闻"
    print("置信度：" + result.confidence);  // 0.95
    print("标签：" + result.tags);          // ["苹果", "手机", "新品"]
}
```

---

## 🧠 Model Routing (按任务能力切分脑区)

不仅仅是数据结构的严格管控，一门优秀的语言还需要为开发者解决"金钱"问题。大模型的 Token 计算力是极其昂贵的。

Nexa 允许你在 `model` 声明上通过数组和字典指定差异化的能力退让（Fallback），构建出健壮的高可用模型中枢。

### 优雅的 Fallback 降级机制

当主线模型宕机、被平台限流（Rate Limit）或者遭遇超时（Timeout）时，通常需要大段的 `try...except...retry` 与轮换逻辑进行保护。在 Nexa 中仅需一句宣告：

```nexa
// 如果主力超大杯模型无法响应，甚至发生内部错误，自动降级去请求 Opus 或更小的开源模型。
agent HeavyMathBot {
    model: ["gpt-4-turbo", fallback: "claude-3-opus", fallback: "llama-3-8b"],
    prompt: "You solve extreme math problems."
}
```

### 模型选择策略

```nexa
// 任务类型与模型选择
agent QuickRouter {
    // 简单任务用快速模型
    model: "deepseek/deepseek-chat",
    prompt: "..."
}

agent HeavyThinker {
    // 复杂任务用强力模型
    model: "openai/gpt-4",
    prompt: "..."
}

agent BudgetFriendly {
    // 成本敏感场景用便宜模型
    model: "minimax/minimax-m2.5",
    prompt: "..."
}
```

### 高可用配置

```nexa
agent ProductionBot {
    // 主模型 + 多级备用
    model: [
        "openai/gpt-4",
        fallback: "anthropic/claude-3-sonnet",
        fallback: "deepseek/deepseek-chat"
    ],
    prompt: "...",
    timeout: 30,    // 30秒超时
    retry: 3        // 重试3次
}
```

---

## 📊 Protocol 高级技巧

### 技巧 1：嵌套结构（使用字符串表示）

虽然 Protocol 不支持直接嵌套，但可以用字符串表示复杂结构：

```nexa
protocol ComplexReport {
    title: "string",
    metadata: "string",   // JSON 字符串表示复杂结构
    sections: "list[string]"  // 每个元素是 JSON 字符串
}
```

### 技巧 2：可选字段处理

在 Prompt 中说明字段的处理方式：

```nexa
protocol FlexibleData {
    required_field: "string",
    optional_field: "string"  // Prompt 中说明可以为空
}

agent FlexibleAgent implements FlexibleData {
    prompt: """
    提取数据。
    required_field 必须有值。
    optional_field 如果找不到，填写 "N/A"。
    """
}
```

### 技巧 3：枚举值约束

在 Prompt 中明确枚举值：

```nexa
protocol StatusReport {
    status: "string",  // 必须是 "pending", "processing", "completed", "failed"
    message: "string"
}

agent StatusAgent implements StatusReport {
    prompt: """
    报告任务状态。
    status 只能是以下值之一：
    - "pending"
    - "processing"  
    - "completed"
    - "failed"
    """
}
```

---

## ⚠️ Protocol 常见错误

### 错误 1：类型未加引号

```nexa
// ❌ 错误
protocol Bad {
    name: string,  // 编译错误
    age: int       // 编译错误
}

// ✅ 正确
protocol Good {
    name: "string",
    age: "int"
}
```

### 错误 2：忘记 implements 关键字

```nexa
// ❌ 错误：定义了 Protocol 但 Agent 没有实现
protocol MyProtocol {
    field: "string"
}

agent MyAgent {  // 缺少 implements MyProtocol
    prompt: "..."
}

// ✅ 正确
agent MyAgent implements MyProtocol {
    prompt: "..."
}
```

### 错误 3：Protocol 过于复杂

```nexa
// ❌ 过于复杂，LLM 难以准确输出
protocol TooComplex {
    nested: "dict[string, list[dict[string, any]]]"
}

// ✅ 简化设计
protocol SimpleAndClear {
    data: "string"  // JSON 字符串
}
```

---

## 📝 本章小结

在本章中，我们学习了：

| 特性 | 说明 | 使用场景 |
|-----|------|---------|
| `protocol` | 定义输出格式约束 | 结构化数据提取 |
| `implements` | Agent 实现协议 | 确保输出格式一致 |
| 自动重试 | 验证失败自动修正 | 提高系统可靠性 |
| Model Routing | 多模型路由 | 成本优化、高可用 |

通过将 `protocol` 的刚性契约与动态 `fallback` 流转网络相结合，Nexa 在赋予高度"思考灵活性"的同时，从未抛弃几十年来传统软件工程所积累的"鲁棒性与边界确定性"基因。这也是 Agent 开发向正规化轨道迈出的决定性一步。

---

## 🔗 相关资源

- [完整示例集合](examples.md) - 查看 Protocol 更多示例
- [最佳实践](part6_best_practices.md) - 企业级 Protocol 设计模式
- [常见问题与排查](troubleshooting.md) - Protocol 相关问题解决
