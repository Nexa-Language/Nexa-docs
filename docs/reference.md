---
comments: true
---

# Nexa 语言参考手册

本手册详细描述 Nexa 语言的语法规范、语义规则和类型系统。所有语法规则与源码 `src/nexa_parser.py` 严格匹配。

---

## 📖 关于本手册

本参考手册按照以下原则组织：

- **精确性**：每个语法构造都有明确的语义定义
- **完整性**：覆盖语言的所有特性，包括 v1.1–v1.3.x 新增特性
- **实用性**：提供足够的示例帮助理解

!!! tip "阅读建议"
    如果你是 Nexa 新手，建议先阅读 [快速入门](quickstart.md) 和 [基础语法](part1_basic.md)，再回来查阅本手册。

---

## 1. 词法结构 (Lexical Structure)

### 1.1 标识符 (Identifiers)

Nexa 标识符遵循以下规则：

```
identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
```

**有效标识符示例**：

```nexa
MyAgent           // 大驼峰命名（推荐用于 Agent）
my_tool          // 蛇形命名（推荐用于 tool）
_process_data    // 下划线开头
Parser2          // 包含数字（不能开头）
```

**无效标识符示例**：

```nexa
2ndAgent         // 数字开头
my-agent         // 包含连字符
agent.name       // 包含点号
```

### 1.2 关键字 (Keywords)

Nexa 保留以下关键字，不能用作标识符：

| 类别 | 关键字 |
|------|--------|
| 声明 | `agent`, `tool`, `protocol`, `flow`, `test`, `type`, `struct`, `enum`, `trait`, `impl`, `fn`, `job`, `server`, `db`, `auth`, `kv` |
| 控制流 | `match`, `intent`, `loop`, `until`, `if`, `else`, `for`, `while`, `break`, `continue` |
| 语义控制 | `semantic_if`, `fast_match`, `against` |
| 异常处理 | `try`, `catch` |
| 错误传播 | `?`, `otherwise` |
| 类型约束 | `implements`, `uses` |
| 契约式编程 | `requires`, `ensures`, `invariant` |
| 并发 | `spawn`, `parallel`, `race`, `channel`, `after`, `schedule`, `select` |
| 延迟执行 | `defer` |
| 管道 | `|>` |
| 空值合并 | `??` |
| 字符串插值 | `#{expr}` |
| 模板 | `template` |
| 其他 | `print`, `assert`, `fallback`, `join`, `role`, `model`, `prompt`, `memory`, `stream`, `cache`, `experience`, `include` |

### 1.3 字面量 (Literals)

#### 字符串字面量

```nexa
"Hello, World!"           // 普通字符串
"Line 1\nLine 2"         // 包含转义字符
"Quote: \"nested\""      // 包含引号
"""Multi-line string"""   // 多行字符串
```

#### 字符串插值字面量 (v1.3.x)

```nexa
"Hello #{name}, you are #{age} years old!"   // Ruby 风格插值
"Status: #{result ?? 'pending'}"             // 插值 + 空值合并
"Agent #{agent.name} responding"             // 插值 + 点访问
```

**插值表达式支持**：

| 表达式类型 | 示例 | Python 转译 |
|-----------|------|-------------|
| 简单标识符 | `#{name}` | `name` |
| 点访问 | `#{user.name}` | `user["name"]` |
| 括号访问 | `#{arr[0]}` | `arr[0]` |
| 组合 | `#{data.items[0].name}` | `data["items"][0]["name"]` |

**转义**：`\#{` → 字面量 `#{`

#### 模板字符串字面量 (v1.3.6)

```nexa
template"""Hello {{name | upper}}!"""
template"""{{#for item in items}}{{@index}}:{{item}}{{/for}}"""
template"""{{#if is_admin}}Admin{{#elif is_mod}}Mod{{#else}}User{{/if}}"""
template"""{{> card user_data}}"""
```

#### 正则表达式字面量

```nexa
r"\d{4}-\d{2}-\d{2}"     // 日期格式
r"^[a-zA-Z_]\w*$"        // 标识符模式
r"https?://[^\s]+"      // URL 模式
```

#### 数字字面量

```nexa
42              // 整数
3.14            // 浮点数
2048            // 用于 max_tokens 等参数
```

### 1.4 注释 (Comments)

```nexa
// 单行注释

/*
 * 多行注释
 * 可以跨越多行
 */

/// 文档注释（用于 Agent、Tool 说明）
```

---

## 2. 声明 (Declarations)

### 2.1 Agent 声明

```nexa
agent_decl ::= agent_decorator* "agent" IDENTIFIER 
               ["->" return_type]
               ["uses" use_identifier_list]
               ["implements" IDENTIFIER]
               requires_clause*
               ensures_clause*
               "{" agent_property* "}"
```

**示例**：

```nexa
// 基本定义
agent Greeter {
    role: "友好的问候助手",
    model: "deepseek/deepseek-chat",
    prompt: "你是一个热情友好的助手。"
}

// 带修饰器
@limit(max_tokens=600)
@timeout(seconds=30)
agent Coder {
    prompt: "Write a short Python implementation.",
    model: "minimax/minimax-m2.5"
}

// 契约条款
agent Reviewer implements ReviewResult
    requires: "input contains code"
    ensures: "result includes score"
{
    prompt: "Review the provided code.",
    model: "deepseek/deepseek-chat"
}

// 带返回类型
agent Analyzer -> ReportResult uses std.http {
    role: "数据分析师",
    prompt: "分析数据并生成报告"
}
```

**Agent 属性**：

| 属性 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| `role` | string | 否 | Agent 角色描述 |
| `prompt` | string | **是** | Agent 核心任务指令 |
| `model` | string | 否 | LLM 模型（格式：`提供商/模型名`） |
| `memory` | string | 否 | 记忆模式 |
| `stream` | boolean | 否 | 流式输出 |
| `cache` | boolean | 否 | 智能缓存 |
| `experience` | string | 否 | 长期记忆文件 |
| `fallback` | string/list | 否 | 备用模型 |
| `uses` | identifier_list | 否 | 标准库权限 |
| `implements` | identifier | 否 | 协议约束 |

**Agent 修饰器**：

| 修饰器 | 参数 | 说明 |
|--------|------|------|
| `@limit` | `max_tokens=INT` | 最大输出 token 数 |
| `@timeout` | `seconds=INT` | 执行超时 |
| `@retry` | `count=INT` | 失败重试次数 |
| `@temperature` | `value=FLOAT` | 模型温度 |

---

### 2.2 Tool 声明

```nexa
tool_decl ::= "tool" IDENTIFIER "{" tool_body "}"
tool_body ::= tool_body_standard | tool_body_mcp | tool_body_python
```

**示例**：

```nexa
// 标准工具
tool web_search {
    description: "搜索网页内容",
    parameters: {
        "query": "搜索关键词",
        "limit": "结果数量限制"
    }
}

// MCP 工具
tool search_mcp {
    mcp: "web-search-mcp-server"
}

// Python 工具
tool calculator {
    python: "import math; return math.sqrt(input)"
}
```

---

### 2.3 Protocol 声明

```nexa
protocol_decl ::= "protocol" IDENTIFIER "{" protocol_body* "}"
protocol_body ::= IDENTIFIER ":" STRING_LITERAL ","?
                | IDENTIFIER ":" type_expr ","?
```

**示例**：

```nexa
// 字符串类型标注（旧格式）
protocol ReviewResult {
    score: "int",
    summary: "string",
    bug_list: "list[string]",
    is_critical: "boolean"
}

// 类型表达式标注（v1.3.1+）
protocol UserProfile {
    name: String,
    age: Int,
    email: Option[String]
}
```

---

### 2.4 Flow 声明

```nexa
flow_decl ::= "flow" IDENTIFIER ["(" param_list ")"] ["->" type_expr]
              requires_clause* ensures_clause* block
```

**示例**：

```nexa
// 基本定义
flow main {
    result = Greeter.run("你好！");
    print(result);
}

// 带参数和返回类型
flow analyze(data: String) -> ReportResult
    requires: data != None
    ensures: "result contains analysis"
{
    return Analyzer.run(data);
}
```

---

### 2.5 Test 声明

```nexa
test_decl ::= "test" STRING_LITERAL block
```

**示例**：

```nexa
test "翻译功能测试" {
    result = Translator.run("Hello, World!");
    assert "包含中文翻译" against result;
}
```

---

### 2.6 Type 声明 (语义类型)

```nexa
type_decl ::= "type" IDENTIFIER "=" semantic_type
semantic_type ::= base_type "@" STRING_LITERAL    // 约束类型
               | base_type                          // 简单类型
```

**示例**：

```nexa
type Email = str @ "valid email address format"
type PositiveInt = int @ "must be greater than 0"
type Score = float @ "between 0.0 and 100.0"
```

---

### 2.7 Struct 声明 (v1.3.x)

```nexa
struct_decl ::= "struct" IDENTIFIER "{" struct_field* "}"
struct_field ::= IDENTIFIER ":" type_expr ","?
```

**示例**：

```nexa
struct Point { x: Int, y: Int }
struct AgentResult { answer: String, confidence: Float, tokens: Int }
struct UserProfile { name: String, email: String, age: Int }
```

**运行时表示**（handle-as-dict）：

```json
{"_nexa_struct": "Point", "_nexa_struct_id": 1, "x": 1, "y": 2}
```

---

### 2.8 Enum 声明 (v1.3.x)

```nexa
enum_decl ::= "enum" IDENTIFIER "{" enum_variant* "}"
enum_variant ::= IDENTIFIER "(" IDENTIFIER ")"    // 带值变体
              | IDENTIFIER                          // 单元变体
```

**示例**：

```nexa
enum Option { Some(value), None }
enum Result { Ok(value), Err(error) }
enum AgentState { Idle, Running, Error(message) }
```

**运行时表示**（handle-as-dict）：

```json
// 带值变体
{"_nexa_variant": "Some", "_nexa_enum": "Option", "_nexa_variant_id": 1, "value": 42}
// 单元变体
{"_nexa_variant": "None", "_nexa_enum": "Option"}
```

---

### 2.9 Trait 声明 (v1.3.x)

```nexa
trait_decl ::= "trait" IDENTIFIER "{" trait_method* "}"
trait_method ::= "fn" IDENTIFIER "(" param_list ")" ["->" type_expr]
```

**示例**：

```nexa
trait Printable { fn format() -> String }
trait Comparable { fn compare(other: Self) -> Int }
trait Serializable { fn serialize() -> String }
```

---

### 2.10 Impl 声明 (v1.3.x)

```nexa
impl_decl ::= "impl" IDENTIFIER "for" IDENTIFIER "{" impl_method* "}"
impl_method ::= "fn" IDENTIFIER "(" param_list ")" ["->" type_expr] block
```

**示例**：

```nexa
impl Printable for Point {
    fn format() -> String {
        return "Point(x=#{self.x}, y=#{self.y})"
    }
}
```

---

### 2.11 Job 声明 (v1.3.3)

```nexa
job_decl ::= "job" IDENTIFIER "on" STRING_LITERAL 
             ["(" job_options ")"] "{" job_body "}"
```

**示例**：

```nexa
job SendEmail on "emails" (retry: 2, timeout: 120) {
    perform(user_id) {
        // 发送邮件逻辑
    }
    on_failure(error, attempt) {
        // 失败处理逻辑
    }
}
```

**Job 选项**：

| 选项 | 类型 | 说明 |
|------|------|------|
| `retry` | int | 重试次数 |
| `timeout` | int | 超时秒数 |

---

### 2.12 Server 声明 (v1.3.4)

```nexa
server_decl ::= "server" INT "{" server_body "}"
```

**示例**：

```nexa
server 8080 {
    static "/assets" from "./public"
    cors { origins: ["*"], methods: ["GET", "POST"] }
    middleware [auth_middleware]
    require_auth "/admin"
    
    route GET "/chat" => ChatBot
    route POST "/analyze" => DataExtractor |>> Analyzer
    semantic route "/help" => HelpBot
    
    group "/admin" {
        middleware [require_admin]
        route GET "/" => AdminBot
    }
}
```

**Server 指令**：

| 指令 | 说明 |
|------|------|
| `static` | 静态文件服务 |
| `cors` | CORS 配置 |
| `middleware` | 中间件列表 |
| `require_auth` | 认证要求路径 |
| `route` | 标准路由 |
| `semantic route` | 语义路由 |
| `group` | 路径分组 |

**HTTP 方法**：`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`

**路由处理器**：

```nexa
// 单个处理器
route GET "/chat" => ChatBot

// DAG 链式处理器
route POST "/analyze" => DataExtractor |>> Analyzer |>> Reporter
```

---

### 2.13 DB 声明 (v1.3.5)

```nexa
db_decl ::= "db" IDENTIFIER "=" "connect" "(" STRING_LITERAL ")"
```

**示例**：

```nexa
db app_db = connect("sqlite://data.db")
db prod_db = connect("postgresql://user:pass@localhost/mydb")
```

---

### 2.14 Auth 声明 (v1.3.6)

```nexa
auth_decl ::= "auth" IDENTIFIER "=" "enable_auth" "(" STRING_LITERAL ")"
```

**示例**：

```nexa
auth myAuth = enable_auth('{"providers": ["google", "github"]}')
```

---

### 2.15 KV 声明 (v1.3.6)

```nexa
kv_decl ::= "kv" IDENTIFIER "=" "open" "(" STRING_LITERAL ")"
```

**示例**：

```nexa
kv myCache = open("sqlite://cache.db")
```

---

## 3. 表达式 (Expressions)

### 3.1 管道操作符 `|>` (v1.3.x)

左到右数据流管道，LHS 作为 RHS 函数的第一个参数。

```nexa
x |> f          // 等价于 f(x)
x |> f(a, b)    // 等价于 f(x, a, b)
data |> std.text.upper
prompt |> agent.run |> extract_answer
```

!!! note "与 `>>` 的区别"
    `|>` 是函数管道（左值作为第一个参数传入），`>>` 是 Agent 流水线（左值作为输入传给下一个 Agent）。

---

### 3.2 Agent 管道操作符 `>>`

Agent 间流水线数据传递。

```nexa
A >> B              // B.run(A.run(input))
A >> B >> C         // C.run(B.run(A.run(input)))
input >> A >> B     // 从输入开始
```

---

### 3.3 DAG 操作符 `|>>` 和 `&>>`

```nexa
// |>> 分叉（fan-out）：输入同时发送给多个 Agent
input |>> [AgentA, AgentB, AgentC]

// &>> 合流（merge）：收集多个结果后传给下一个 Agent
[results] &>> Summarizer

// 组合使用
"topic" |>> [Writer, Reviewer, Editor] &>> Publisher
```

---

### 3.4 Null 合并操作符 `??` (v1.3.x)

```nexa
expr ?? fallback    // 如果 expr 为 None/Option::None/空字典，返回 fallback
result ?? "fallback"
config.timeout ?? 30
agent.run(prompt) ?? "I couldn't process that"
```

**语义**：

| 左值 | 结果 |
|------|------|
| `None` | 右值 |
| `Option::None` dict | 右值 |
| 空字典 `{}` | 右值 |
| 其他任何值 | 左值 |

---

### 3.5 错误传播操作符 `?` (v1.3.2)

Rust 风格错误传播，遇到错误时向上传播。

```nexa
let value = parse(input) ?           // 如果 parse 返回错误，传播错误
let result = risky_operation() ?     // 同上
```

---

### 3.6 Otherwise 操作符 (v1.3.2)

提供错误回退值。

```nexa
let result = risky_op() otherwise "fallback"   // 如果出错，返回 "fallback"
```

---

### 3.7 Match 表达式 (v1.3.x)

```nexa
match_expr ::= "match" expression "{" match_arm* "}"
match_arm ::= pattern "=>" expression
```

**7 种模式类型**：

| 模式 | 语法 | 说明 |
|------|------|------|
| Wildcard | `_` | 匹配任何值，不绑定 |
| Variable | `name` | 匹配任何值，绑定变量 |
| Literal | `42`, `"hello"`, `true` | 匹配精确值 |
| Tuple | `(a, b)` | 匹配元组/数组 |
| Array | `[a, b, ..rest]` | 匹配数组 + rest 收集 |
| Map | `{ name, age: a, ..other }` | 匹配字典 + rest 收集 |
| Variant | `Option::Some(v)` | 匹配枚举变体 |

**示例**：

```nexa
// 基本匹配
match result {
    Option::Some(answer) => answer
    Option::None => "no response"
}

// 字面量匹配
match status {
    200 => "success"
    404 => "not found"
    _ => "unknown"
}

// 解构匹配
match entry {
    (key, value) => "#{key}: #{value}"
}

// 数组解构
match items {
    [first, second, ..rest] => "first=#{first}, rest=#{rest.length}"
}

// Map 解构
match user {
    { name, age: a, ..other } => "#{name} is #{a} years old"
}
```

---

### 3.8 Let 解构 (v1.3.x)

```nexa
let_pattern_stmt ::= "let" pattern "=" expression
```

**示例**：

```nexa
let (key, value) = entry
let [first, ..rest] = items
let { name, age: a } = user_data
```

---

### 3.9 For 解构 (v1.3.x)

```nexa
for_pattern_stmt ::= "for" pattern "in" expression block
```

**示例**：

```nexa
for (name, score) in rankings {
    print("#{name}: #{score}")
}
```

---

### 3.10 Variant Call 表达式 (v1.3.x)

```nexa
variant_call_expr ::= IDENTIFIER "::" IDENTIFIER ["(" expression ")"]
```

**示例**：

```nexa
let opt = Option::Some(42)
let res = Result::Ok("success")
let state = AgentState::Running
let err = AgentState::Error("connection failed")
```

---

### 3.11 Field Init 表达式 (v1.3.x)

```nexa
field_init ::= IDENTIFIER ":" expression
```

**示例**：

```nexa
let p = Point(x: 1, y: 2)
let result = AgentResult(answer: "yes", confidence: 0.95, tokens: 150)
```

---

### 3.12 并发表达式 (v1.3.6)

```nexa
spawn_expr ::= "spawn" "(" expression ")"
parallel_expr ::= "parallel" "(" expression ")"
race_expr ::= "race" "(" expression ")"
channel_expr ::= "channel" "(" ")"
after_expr ::= "after" "(" expression "," expression ")"
schedule_expr ::= "schedule" "(" expression "," expression ")"
select_expr ::= "select" "(" expression ["," expression] ")"
```

**示例**：

```nexa
spawn(my_task)
parallel([task_a, task_b, task_c])
race([fast_task, slow_task])
channel()
after(500ms, cleanup())
schedule(every 30s, health_check())
```

---

## 4. 语句 (Statements)

### 4.1 Defer 语句 (v1.3.x)

```nexa
defer_stmt ::= "defer" expression ";"
```

LIFO 顺序执行，即使发生错误也会执行（类似 Go defer）。

**示例**：

```nexa
defer cleanup(db)
defer log("operation complete")
defer agent_cleanup(agent)
```

---

### 4.2 契约条款 (v1.2.0)

```nexa
requires_clause ::= "requires" STRING_LITERAL        // 语义前置条件
                  | "requires" comparison_expr        // 确定性前置条件

ensures_clause ::= "ensures" STRING_LITERAL           // 语义后置条件
                | "ensures" comparison_expr           // 确定性后置条件
```

**示例**：

```nexa
// 确定性契约
flow transfer(amount: int) -> Result
    requires: amount > 0
    ensures: result.success == true
{
    // 转账逻辑
}

// 语义契约（用 LLM 在运行时判断）
flow review(code: string) -> Report
    requires: "input contains valid source code"
    ensures: "result includes actionable feedback"
{
    // 审查逻辑
}
```

---

### 4.3 传统控制流 (v1.0.1+)

```nexa
// if/else if/else
if condition {
    // ...
} else if other_condition {
    // ...
} else {
    // ...
}

// for each 循环
for each item in collection {
    // ...
}

// while 循环
while condition {
    // ...
}

// break/continue
for each item in items {
    if item == "skip" { continue; }
    if item == "stop" { break; }
}
```

---

### 4.4 语义控制流

```nexa
// loop until — 自然语言控制循环终止
loop {
    draft = Writer.run(feedback);
    feedback = Critic.run(draft);
} until ("文章质量优秀")

// semantic_if — 语义条件判断
semantic_if "user is frustrated" {
    SupportBot.run("提供安慰和帮助");
}

// fast_match — 快速意图匹配
result = fast_match user_input {
    intent("查询天气") => WeatherBot.run(user_input),
    intent("查询新闻") => NewsBot.run(user_input),
    _ => ChatBot.run(user_input)
}
```

---

### 4.5 Python 逃生舱 (v1.0.1+)

```nexa
stats = python! """
    import statistics
    data = json.loads(raw_data)
    return statistics.mean(data)
"""
```

---

## 5. 类型系统 (v1.3.1)

### 5.1 类型表达式

```nexa
type_expr ::= type_union_expr | type_non_union_expr

type_union_expr ::= type_non_union_expr ("|" type_non_union_expr)+
type_non_union_expr ::= type_compound_expr "?" | type_compound_expr

type_compound_expr ::= "str" | "int" | "float" | "bool" | "unit"
                    | "Option" "[" type_expr "]"
                    | "Result" "[" type_expr "," type_expr "]"
                    | "list" "[" type_expr "]"
                    | "dict" "[" type_expr "," type_expr "]"
                    | IDENTIFIER    // 类型别名
```

**类型示例**：

| 类型 | 说明 | 示例值 |
|------|------|--------|
| `Int` | 整数 | `42` |
| `String` / `str` | 字符串 | `"hello"` |
| `Float` / `float` | 浮点数 | `3.14` |
| `Bool` / `bool` | 布尔值 | `true` |
| `Unit` / `unit` | 单元类型 | `()` |
| `Option[T]` | 可选类型 | `Some(42)` / `None` |
| `Result[T, E]` | 结果类型 | `Ok("success")` / `Err("error")` |
| `list[T]` | 列表 | `[1, 2, 3]` |
| `dict[K, V]` | 字典 | `{"key": "value"}` |
| `T | U` | 联合类型 | `Int | String` |
| `T?` | 可选简写 | 等价于 `Option[T]` |

### 5.2 类型检查模式

| 模式 | 环境变量 | 说明 |
|------|---------|------|
| `strict` | `NEXA_TYPE_MODE=strict` | 类型不匹配 = 运行时错误 |
| `warn` | `NEXA_TYPE_MODE=warn` | 类型不匹配 = 日志警告（默认） |
| `forgiving` | `NEXA_TYPE_MODE=forgiving` | 类型不匹配 = 静默忽略 |

**优先级**：CLI flag > 环境变量 > `nexa.toml` > 默认值 (`warn`)

### 5.3 Lint 模式

| 模式 | 环境变量 | 说明 |
|------|---------|------|
| `default` | `NEXA_LINT_MODE=default` | 只检查有类型标注的代码（默认） |
| `warn` | `NEXA_LINT_MODE=warn` | 缺失类型标注发出警告 |
| `strict` | `NEXA_LINT_MODE=strict` | 缺失类型标注 = lint 错误 |

---

## 6. 错误处理 (Error Handling)

### 6.1 错误类型

| 错误类型 | 说明 | 触发场景 |
|---------|------|---------|
| `ContractViolation` | 契约违反 | `requires`/`ensures`/`invariant` 条件不满足 |
| `TypeViolation` | 类型违反 | `strict` 模式下类型不匹配 |
| `TypeWarning` | 类型警告 | `warn` 模式下类型不匹配 |
| `ValidationError` | 验证错误 | 语义验证失败 |
| `NexaResult.Err` | 结果错误 | `Result[T, E]` 类型的错误分支 |
| `NexaOption.None` | 空值 | `Option[T]` 类型的空值 |

### 6.2 错误传播

```nexa
// ? 操作符：传播错误
let value = parse(input) ?

// otherwise 操作符：提供回退值
let result = risky_op() otherwise "fallback"

// try/catch
try {
    result = risky_operation();
} catch (error) {
    print("Error: #{error}");
}
```

---

## 7. 运行时架构模式

### 7.1 Handle-as-dict 模式

所有运行时句柄（DB 连接、KV Store、Auth Session、编译模板、struct 实例、enum 变体）都是普通 Python dict，使用 `_nexa_*` 前缀键，保证 JSON 兼容性。

### 7.2 Thread-safe Registry 模式

所有运行时模块使用全局注册表 + `_registry_lock` (threading.Lock) + `_id_counter`。

### 7.3 StdTool Namespace 模式

标准库工具通过 `StdTool` 注册到命名空间：`std.db`, `std.auth`, `std.kv`, `std.concurrent`, `std.template`, `std.match`, `std.struct`, `std.enum`, `std.trait` 等。

### 7.4 BOILERPLATE 代码生成模式

每个特性在 `CodeGenerator` 的 BOILERPLATE 区段添加导入和辅助函数。

---

## 🔗 相关资源

- [标准库 API](stdlib_reference.md)
- [CLI 命令参考](cli_reference.md)
- [错误索引](error_index.md)
- [快速入门](quickstart.md)