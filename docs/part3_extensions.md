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

## 🎯 Semantic Types 语义类型 (v1.0.2+)

Nexa v1.0.2-beta 引入语义类型（Semantic Types），这是一种革命性的类型系统，允许在类型定义中嵌入语义约束，让类型不仅仅是数据格式的约束，还包含语义含义的验证。

### 基本语法

```nexa
// 定义语义类型：基础类型 + 语义约束
type Email = string @ "valid email address format"
type PositiveInt = int @ "must be greater than 0"
type URL = string @ "valid URL format starting with http:// or https://"
```

### 语义类型优势

| 优势 | 说明 |
|-----|------|
| **语义验证** | 不仅验证数据格式，还验证语义正确性 |
| **LLM 理解** | 约束声明使用自然语言，LLM 能更好理解 |
| **自动修正** | 违反约束时自动触发 LLM 修正 |
| **代码简洁** | 无需手写复杂的验证逻辑 |

### 使用示例

```nexa
// 定义语义类型
type UserName = string @ "real person name, 2-50 characters"
type Age = int @ "age between 1 and 150"
type PhoneNumber = string @ "valid phone number format"

// 在 Protocol 中使用语义类型
protocol UserProfile {
    name: UserName,
    age: Age,
    phone: PhoneNumber,
    email: Email
}

agent UserExtractor implements UserProfile {
    prompt: "从文本中提取用户信息"
}

flow main {
    text = "张三，25岁，手机13812345678，邮箱zhangsan@example.com";
    profile = UserExtractor.run(text);
    
    // profile 自动通过语义验证
    print(profile.name);   // "张三"
    print(profile.age);    // 25
}
```

### 语义约束自动验证

当 LLM 输出违反语义约束时，Nexa 会自动触发修正：

```
LLM 输出: {"email": "not-an-email"}
    │
    ▼
语义验证器检测到 "not-an-email" 不符合 Email 约束
    │
    ▼
生成修正提示: "email 字段必须是有效的电子邮件格式"
    │
    ▼
自动重新请求 LLM
    │
    └──► 返回符合约束的结果
```

### 常用语义类型示例

```nexa
// 标识符类
type UUID = string @ "valid UUID format"
type ProductID = string @ "product identifier starting with 'PROD-'"

// 数值类
type Percentage = float @ "value between 0.0 and 100.0"
type Temperature = float @ "temperature in Celsius, -273.15 to 1000"

// 文本类
type NonEmptyString = string @ "non-empty string"
type ChineseText = string @ "text containing only Chinese characters"

// 时间类
type DateString = string @ "valid date in YYYY-MM-DD format"
type TimeString = string @ "valid time in HH:MM format"

// 网络类
type IPAddress = string @ "valid IPv4 or IPv6 address"
type DomainName = string @ "valid domain name format"
```

### 语义类型与 Protocol 组合

```nexa
// 定义严格的语义类型组合
type OrderAmount = float @ "positive number with up to 2 decimal places"
type SKU = string @ "stock keeping unit in format SKU-XXXX-XXXX"

protocol OrderInfo {
    order_id: UUID,
    sku: SKU,
    amount: OrderAmount,
    created_at: DateString
}

agent OrderProcessor implements OrderInfo {
    prompt: "处理订单信息，确保格式正确"
}

flow main {
    raw_order = "订单号123e4567-e89b-12d3，商品SKU-1234-5678，金额99.99元";
    order = OrderProcessor.run(raw_order);
    
    // 所有字段自动通过语义验证
    print(order.order_id);  // UUID 格式
    print(order.sku);       // SKU-XXXX-XXXX 格式
    print(order.amount);    // 正数，两位小数
}
```

!!! tip "最佳实践"
    - 语义约束描述要**清晰具体**，避免模糊表述
    - 使用**可验证的约束**，如"大于0"、"YYYY-MM-DD格式"
    - 约束描述使用**LLM易懂的自然语言**
    - 避免过度复杂的组合约束

---

## 🛡️ 契约式编程 (Design by Contract) — v1.2.0+

Nexa v1.2.0 引入了契约式编程（Design by Contract, DbC），借鉴 Eiffel 语言的设计理念，将 `requires`（前置条件）、`ensures`（后置条件）和 `invariant`（不变式）提升为语言级关键字。这让 Agent 的输入输出验证不再是可选的"防御性编程"，而是编译器强制检查的契约条款。

### 基本语法

```nexa
// 确定性契约：可由运行时直接评估的表达式
flow transfer(amount: int, sender: string) -> Result
    requires: amount > 0
    requires: sender != ""
    ensures: result.success == true
{
    // 函数体
}

// 语义契约：由 LLM 评估的自然语言条件
flow review(code: string) -> Report
    requires: "input contains valid source code"
    ensures: "result includes actionable feedback with specific suggestions"
{
    // 函数体
}
```

### 契约条款类型

| 条款类型 | 关键字 | 评估方式 | 说明 |
|---------|--------|---------|------|
| 前置条件 | `requires` | 确定性/语义 | 函数调用前必须满足 |
| 后置条件 | `ensures` | 确定性/语义 | 函数返回后必须满足 |
| 不变式 | `invariant` | 确定性/语义 | 对象生命周期中始终满足 |

### 确定性 vs 语义契约

```nexa
// 确定性契约 — 运行时直接评估（零 LLM 开销）
flow calculate_price(quantity: int, price: float) -> float
    requires: quantity > 0           // 确定性：数值比较
    requires: price >= 0             // 确定性：数值比较
    ensures: result >= 0             // 确定性：数值比较
{
    return quantity * price;
}

// 语义契约 — LLM 评估（适合自然语言判断）
flow analyze_sentiment(text: string) -> SentimentReport
    requires: "input is a coherent English text"       // 语义：需要 LLM 判断
    ensures: "result correctly reflects the emotional tone"  // 语义：需要 LLM 判断
{
    // ...
}
```

### `old` 表达式（引用前置状态）

在 `ensures` 条款中，可以使用 `old(expr)` 引用函数执行前的值：

```nexa
flow increment_counter(counter: Counter) -> Counter
    requires: counter.value >= 0
    ensures: result.value == old(counter.value) + 1
{
    counter.value = counter.value + 1;
    return counter;
}
```

### ContractViolation 与 HTTP 集成

契约违反在 HTTP Server 中自动映射为 HTTP 状态码：

| 契约违反类型 | HTTP 状态码 | 说明 |
|-------------|------------|------|
| `requires` 违反 | 401 Unauthorized | 请求未满足前置条件 |
| `ensures` 违反 | 403 Forbidden | 响应未满足后置条件 |

```nexa
server MyApp {
    route "/transfer" {
        requires: amount > 0       // 违反 → HTTP 401
        ensures: result.success    // 违反 → HTTP 403
        
        handler: transfer_flow
    }
}
```

!!! warning "契约违反是异常"
    当契约被违反时，运行时会抛出 `ContractViolation` 异常（错误码 E201-E203）。在 `strict` 类型模式下，这会导致程序中断；在 `forgiving` 模式下，仅记录警告。

---

## 🔬 渐进式类型系统 — v1.3.1+

Nexa v1.3.1 引入渐进式类型系统（Gradual Type System），支持三种类型检查模式，让你可以根据项目阶段灵活选择类型严格程度。

### 类型检查模式

通过环境变量 `NEXA_TYPE_MODE` 控制：

| 模式 | 值 | 行为 | 适用场景 |
|------|-----|------|---------|
| **strict** | `strict` | 类型不匹配 → 抛出 `TypeViolation` 异常 | 生产环境 |
| **warn** | `warn` | 类型不匹配 → 发出 `TypeWarning`，程序继续 | 开发调试 |
| **forgiving** | `forgiving` | 类型不匹配 → 静默忽略 | 快速原型 |

```bash
# 设置类型检查模式
export NEXA_TYPE_MODE=strict   # 严格模式
export NEXA_TYPE_MODE=warn     # 警告模式
export NEXA_TYPE_MODE=forgiving  # 宽容模式
```

### Lint 模式

通过 `NEXA_LINT_MODE` 或 `nexa lint --warn-untyped` 控制类型标注覆盖率检查：

| Lint 模式 | 值 | 行为 |
|----------|-----|------|
| **off** | `off` | 不检查类型标注 |
| **warn** | `warn` | 未标注的变量/函数发出警告 |
| **strict** | `strict` | 所有公共函数必须标注 |

```bash
# 检查类型标注覆盖率
nexa lint main.nexa --warn-untyped

# 严格 lint 模式
nexa lint main.nexa --strict
```

### 类型表达式

Nexa 支持丰富的类型表达式，用于 `protocol`、`struct`、函数签名等：

```nexa
// 基础类型
let x: Int = 42
let y: String = "hello"
let z: Bool = true

// 泛型类型
let items: List[Int] = [1, 2, 3]
let config: Dict[String, Any] = {"key": "value"}

// Option 类型 — 可能为 None
let maybe: Option[Int] = Option::Some(42)
let nothing: Option[Int] = Option::None

// Result 类型 — 可能成功或失败
let ok: Result[Int, String] = Result::Ok(42)
let err: Result[Int, String] = Result::Err("not found")

// Union 类型 — 多种可能类型
let mixed: Int | String = 42

// 语义类型
type Email = String @ "valid email address format"
```

### 类型收窄（Type Narrowing）

Nexa 支持流敏感的类型收窄，在条件检查后自动缩小变量类型：

```nexa
let value: Option[Int] = Option::Some(42);

// None 检查后收窄为 Int
if (value != Option::None) {
    // 此处 value 类型收窄为 Int
    print(value + 1);  // 安全：value 已确认非 None
}

// isinstance 检查后收窄
let mixed: Int | String = get_value();
if (mixed is Int) {
    // 此处 mixed 类型收窄为 Int
    print(mixed * 2);
}
```

---

## 🚨 错误传播 (`?` 与 `otherwise`) — v1.3.2+

Nexa v1.3.2 引入了 Rust 风格的错误传播操作符 `?` 和 `otherwise`，让你可以优雅地处理 Agent 执行中的错误，无需层层嵌套 `try/catch`。

### `?` 错误传播操作符

当 Agent 或函数返回 `Result` 类型时，`?` 操作符会：

- 如果是 `Result::Ok(value)` → 直接提取 `value` 继续执行
- 如果是 `Result::Err(error)` → 立即向上层传播错误，中断当前 flow

```nexa
flow main {
    // 传统写法：需要手动处理每个错误
    result1 = Agent1.run(input);
    if (result1 is Result::Err) { return result1; }
    value1 = result1.value;
    
    result2 = Agent2.run(value1);
    if (result2 is Result::Err) { return result2; }
    value2 = result2.value;
    
    // ? 操作符写法：一行搞定
    value1 = Agent1.run(input)?;     // 错误自动向上传播
    value2 = Agent2.run(value1)?;    // 错误自动向上传播
    print(value2);                   // 只有全部成功才到达这里
}
```

### `otherwise` 错误恢复操作符

当 `?` 传播错误过于激进时，`otherwise` 提供了就地恢复的能力：

```nexa
flow main {
    // otherwise：错误时执行恢复逻辑
    result = RiskyAgent.run(input) otherwise FallbackAgent.run(input);
    
    // otherwise 也可以使用 lambda
    data = db.query("SELECT * FROM users") otherwise {"users": []};
    
    // 组合使用
    value = Agent1.run(input)?
        |> process
        |> format
        otherwise "default output";
}
```

### `?` 与 `otherwise` 的区别

| 操作符 | 行为 | 适用场景 |
|-------|------|---------|
| `?` | 错误向上传播，中断当前 flow | 错误不可恢复，必须中止 |
| `otherwise` | 错误就地恢复，继续执行 | 错误可恢复，有备用方案 |

### 完整示例：带错误传播的数据处理流水线

```nexa
flow process_data(raw: string) -> Result[Report, string] {
    // 每一步都可能失败，? 自动传播错误
    parsed = std.json.json_parse(raw)?;
    validated = Validator.run(parsed)?;
    enriched = Enricher.run(validated) otherwise validated;  // Enricher 失败时用原始数据
    report = Formatter.run(enriched)?;
    
    return Result::Ok(report);
}

flow main {
    // 顶层处理错误
    result = process_data(raw_input);
    
    match result {
        Result::Ok(report) => print("Success: #{report.title}"),
        Result::Err(error) => print("Failed: #{error}")
    }
}
```

---

## 📝 本章小结

在本章中，我们学习了：

| 特性 | 版本 | 说明 | 使用场景 |
|-----|------|------|---------|
| `protocol` | v0.5+ | 定义输出格式约束 | 结构化数据提取 |
| `implements` | v0.5+ | Agent 实现协议 | 确保输出格式一致 |
| 自动重试 | v0.5+ | 验证失败自动修正 | 提高系统可靠性 |
| Model Routing | v0.5+ | 多模型路由 | 成本优化、高可用 |
| Semantic Types | v1.0.2+ | 语义类型约束 | 智能数据验证 |
| Design by Contract | v1.2.0+ | requires/ensures/invariant | 输入输出契约验证 |
| Gradual Type System | v1.3.1+ | strict/warn/forgiving | 渐进式类型安全 |
| Error Propagation | v1.3.2+ | `?` 与 `otherwise` | 优雅错误处理 |

通过将 `protocol` 的刚性契约与动态 `fallback` 流转网络相结合，再配合 v1.2.0 的契约式编程、v1.3.1 的渐进式类型系统和 v1.3.2 的错误传播机制，Nexa 在赋予高度"思考灵活性"的同时，从未抛弃几十年来传统软件工程所积累的"鲁棒性与边界确定性"基因。这也是 Agent 开发向正规化轨道迈出的决定性一步。

---

## 🔗 相关资源

- [完整示例集合](examples.md) - 查看 Protocol 更多示例
- [高级特性](part2_advanced.md) - 模式匹配与 ADT
- [语言参考手册](reference.md) - 查看完整语法规范
- [最佳实践](part6_best_practices.md) - 企业级 Protocol 设计模式
- [常见问题与排查](troubleshooting.md) - Protocol 相关问题解决
