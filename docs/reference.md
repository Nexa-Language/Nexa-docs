---
comments: true
---

# Nexa 语言参考手册

本手册详细描述 Nexa 语言的语法规范、语义规则和类型系统。它是 Nexa 语言的权威参考文档。

---

## 📖 关于本手册

本参考手册按照以下原则组织：

- **精确性**：每个语法构造都有明确的语义定义
- **完整性**：覆盖语言的所有特性，包括边缘情况
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
| 声明 | `agent`, `tool`, `protocol`, `flow`, `test` |
| 控制流 | `match`, `intent`, `loop`, `until`, `if`, `else` |
| 语义控制 | `semantic_if`, `fast_match`, `against` |
| 异常处理 | `try`, `catch` |
| 类型约束 | `implements`, `uses` |
| 其他 | `print`, `assert`, `fallback`, `join`, `agent`, `role`, `model`, `prompt`, `memory`, `stream`, `cache`, `experience` |

### 1.3 字面量 (Literals)

#### 字符串字面量

```nexa
"Hello, World!"           // 普通字符串
"Line 1\nLine 2"         // 包含转义字符
"Quote: \"nested\""      // 包含引号
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
agent MyAgent {
    role: "文档注释示例"
}
```

---

## 2. 顶层声明 (Top-Level Declarations)

Nexa 程序由一系列顶层声明组成。每个声明都是一等公民。

### 2.1 Agent 声明 (Agent Declaration)

**完整语法**：

```ebnf
agent_decl ::= [agent_modifier] "agent" IDENTIFIER 
                ["implements" IDENTIFIER] 
                ["uses" identifier_list] 
                "{" agent_body "}"

agent_modifier ::= "@" IDENTIFIER "(" parameter_list ")"

agent_body ::= (IDENTIFIER ":" value ",")*
```

**属性规范**：

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `role` | string | ✅ | Agent 的角色定位 |
| `prompt` | string | ✅ | 任务执行指令 |
| `model` | string | ❌ | 模型标识符，默认使用配置 |
| `memory` | string | ❌ | 记忆策略：`short`、`long`、`session` |
| `stream` | bool | ❌ | 流式输出开关，默认 `false` |
| `cache` | bool/string | ❌ | 缓存策略：`true`、`false`、`"smart"` |
| `experience` | bool | ❌ | 长期记忆开关，默认 `false` |
| `fallback` | string | ❌ | 模型降级备选 |

**修饰器规范**：

```nexa
@limit(max_tokens=2048)
@timeout(seconds=30)
@retry(max_attempts=3)
agent MyAgent {
    role: "受限 Agent",
    prompt: "输出不超过 2048 tokens"
}
```

**语义规则**：

1. **命名唯一性**：同一作用域内 Agent 名称必须唯一
2. `implements` 引用的 `protocol` 必须已声明
3. `uses` 引用的 `tool` 必须已声明或为标准库工具
4. 属性 `role` 和 `prompt` 为必需项

### 2.2 Tool 声明 (Tool Declaration)

**完整语法**：

```ebnf
tool_decl ::= "tool" IDENTIFIER "{" tool_body "}"

tool_body ::= ("description:" STRING_LITERAL "," "parameters:" json_object)
            | ("mcp:" STRING_LITERAL)
            | ("python:" STRING_LITERAL)
```

**本地工具声明**：

```nexa
tool WeatherAPI {
    description: "获取指定城市的天气信息",
    parameters: {
        "city": {
            "type": "string",
            "description": "城市名称",
            "required": true
        },
        "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "default": "celsius"
        }
    }
}
```

**MCP 工具声明**：

```nexa
tool WebSearch {
    mcp: "github.com/nexa-ai/web-search-mcp"
}
```

**语义规则**：

1. Tool 名称在同一作用域内必须唯一
2. `parameters` 必须符合 JSON Schema 规范
3. MCP 工具需要在运行时配置 MCP 服务器

### 2.3 Protocol 声明 (Protocol Declaration)

**完整语法**：

```ebnf
protocol_decl ::= "protocol" IDENTIFIER "{" field_list "}"

field_list ::= (IDENTIFIER ":" type_annotation ",")*

type_annotation ::= "string" | "number" | "boolean" | "array" | "object" 
                  | STRING_LITERAL  // 枚举值
```

**类型标注规范**：

```nexa
protocol UserResponse {
    name: "string",                    // 字符串类型
    age: "number",                     // 数字类型
    active: "boolean",                 // 布尔类型
    tags: "array",                     // 数组类型
    metadata: "object",                // 对象类型
    status: "active|inactive|pending"  // 枚举值（v0.9+）
}
```

**语义规则**：

1. Protocol 名称在同一作用域内必须唯一
2. 类型标注必须加引号
3. 枚举值使用 `|` 分隔多个选项
4. Agent 声明 `implements` 后，运行时会验证输出符合 Protocol

### 2.4 Flow 声明 (Flow Declaration)

**完整语法**：

```ebnf
flow_decl ::= "flow" IDENTIFIER ["(" parameter_list ")"] "{" flow_body "}"

flow_body ::= flow_stmt*

flow_stmt ::= assignment_stmt 
            | expr_stmt 
            | semantic_if_stmt 
            | loop_stmt 
            | match_stmt 
            | assert_stmt 
            | try_catch_stmt
            | print_stmt
```

**示例**：

```nexa
flow main(input: string) {
    // 赋值语句
    result = Agent1.run(input);
    
    // 管道表达式
    final = input >> Agent1 >> Agent2;
    
    // 意图路由
    match input {
        intent("查询天气") => WeatherBot.run(input),
        intent("设置提醒") => ReminderBot.run(input),
        _ => DefaultBot.run(input)
    }
    
    // 输出
    print(result);
}
```

### 2.5 Test 声明 (Test Declaration)

**完整语法**：

```ebnf
test_decl ::= "test" STRING_LITERAL "{" test_body "}"

test_body ::= flow_stmt*
```

**示例**：

```nexa
test "天气查询测试" {
    mock_input = "北京今天天气怎么样";
    result = WeatherBot.run(mock_input);
    
    assert "包含天气信息" against result;
    assert "包含温度数据" against result;
}
```

---

## 3. 表达式系统 (Expression System)

### 3.1 基础表达式

**语法**：

```ebnf
base_expr ::= method_call 
            | join_call 
            | STRING_LITERAL 
            | IDENTIFIER

method_call ::= IDENTIFIER ("." IDENTIFIER)? "(" argument_list? ")"

join_call ::= "join" "(" identifier_list ")" ["." IDENTIFIER "(" argument_list ")"]

argument_list ::= expression ("," expression)*
```

**方法调用**：

```nexa
Agent.run(input)           // Agent 运行
tool.execute(param)        // 工具执行
result.toString()          // 结果转换
```

**Join 调用**：

```nexa
join([result1, result2])             // 合并结果
join([result1, result2]).format()   // 合并后格式化
```

### 3.2 管道表达式 (Pipeline Expression)

**语法**：

```ebnf
pipeline_expr ::= base_expr (">>" base_expr)+
```

**语义**：

`>>` 操作符将左侧表达式的输出作为右侧表达式的输入。

```nexa
// 等价于 Agent2.run(Agent1.run(input))
result = input >> Agent1 >> Agent2 >> Agent3
```

### 3.3 DAG 表达式 (DAG Expression)

Nexa v0.9.7+ 支持复杂的 DAG（有向无环图）拓扑编排。

#### 分叉操作符 `|>>`

**语法**：

```ebnf
dag_fork_expr ::= base_expr ("|>>" | "||") "[" identifier_list "]"
```

**语义**：

- `|>>`：并行执行，等待所有结果返回
- `||`：并行执行，不等待结果（fire-and-forget）

```nexa
// 并行处理，等待所有结果
results = input |>> [Agent1, Agent2, Agent3];

// 并行处理，不等待结果
input || [Logger, Analytics];
```

#### 合流操作符 `&>>`

**语法**：

```ebnf
dag_merge_expr ::= "[" identifier_list "]" ("&>>" | "&&") base_expr
```

**语义**：

- `&>>`：顺序合流，按顺序传递结果
- `&&`：共识合流，需要多个 Agent 达成一致

```nexa
// 顺序合流
result = [Researcher, Analyst] &>> Reviewer;

// 共识合流
consensus = [Agent1, Agent2] && JudgeAgent;
```

#### 条件分支操作符 `??`

**语法**：

```ebnf
dag_branch_expr ::= base_expr "??" base_expr ":" base_expr
```

**语义**：

根据输入特征选择执行路径。如果输入匹配第一个 Agent 的处理条件，执行第一个；否则执行第二个。

```nexa
result = input ?? UrgentHandler : NormalHandler;
```

#### 复杂 DAG 拓扑

```nexa
// 分叉后合流
final = topic |>> [Researcher, Analyst] &>> Writer >> Reviewer;

// 多阶段并行
report = data |>> [Preprocess1, Preprocess2] &>> Aggregator >> Formatter;

// 条件分支 + 并行处理
result = input ?? FastPath : StandardPath |>> [Step1, Step2] &>> FinalStep;
```

### 3.4 Fallback 表达式

**语法**：

```ebnf
fallback_expr ::= base_expr "fallback" expression
```

**示例**：

```nexa
result = PrimaryAgent.run(input) fallback BackupAgent.run(input);
```

---

## 4. 控制流 (Control Flow)

### 4.1 意图路由 (Match Intent)

**语法**：

```ebnf
match_stmt ::= "match" IDENTIFIER "{" match_branch+ ("_=>" expression)? "}"

match_branch ::= "intent" "(" STRING_LITERAL ")" "=>" expression ","
```

**示例**：

```nexa
match user_input {
    intent("查询天气") => WeatherBot.run(user_input),
    intent("设置提醒") => ReminderBot.run(user_input),
    intent("播放音乐") => MusicBot.run(user_input),
    _ => DefaultBot.run(user_input)  // 默认分支
}
```

**语义规则**：

1. `intent()` 使用 LLM 进行语义匹配
2. 分支按顺序评估，第一个匹配的分支执行
3. `_` 为默认分支，必须放在最后
4. 返回匹配分支表达式的结果

### 4.2 语义条件判断 (Semantic If)

**语法**：

```ebnf
semantic_if_stmt ::= "semantic_if" STRING_LITERAL 
                     ["fast_match" REGEX_LITERAL] 
                     "against" IDENTIFIER
                     "{" flow_stmt* "}"
                     ("else" "{" flow_stmt* "}")?
```

**示例**：

```nexa
semantic_if "包含日期和地点信息" 
    fast_match r"\d{4}-\d{2}-\d{2}" 
    against user_input {
    Scheduler.run(user_input);
} else {
    Clarifier.run(user_input);
}
```

**语义规则**：

1. `semantic_if` 使用 LLM 判断语义条件
2. `fast_match` 提供正则预过滤，避免重复 Token 消耗
3. 如果 `fast_match` 通过，才会执行语义判断
4. 条件为真执行 `if` 块，否则执行 `else` 块

### 4.3 语义循环 (Loop Until)

**语法**：

```ebnf
loop_stmt ::= "loop" "{" flow_stmt* "}" "until" "(" STRING_LITERAL ")"
```

**示例**：

```nexa
loop {
    draft = Editor.run(feedback);
    feedback = Critic.run(draft);
} until ("文章语法正确且内容吸引人")
```

**语义规则**：

1. 循环体至少执行一次
2. `until` 条件使用 LLM 进行语义判断
3. 建议添加最大迭代次数限制，防止无限循环

**防死锁最佳实践**：

```nexa
max_iterations = 5;
current = 0;
loop {
    draft = Editor.run(feedback);
    feedback = Critic.run(draft);
    current = current + 1;
    
    // 安全退出条件
    if current >= max_iterations {
        print("达到最大迭代次数，退出循环");
        break;
    }
} until ("文章语法正确且内容吸引人")
```

### 4.4 异常处理 (Try/Catch)

**语法**：

```ebnf
try_catch_stmt ::= "try" "{" flow_stmt* "}" "catch" "(" IDENTIFIER ")" "{" flow_stmt* "}"
```

**示例**：

```nexa
try {
    result = APIAgent.run(input);
    print(result);
} catch (error) {
    print("执行失败: " + error);
    result = FallbackAgent.run(input);
}
```

**语义规则**：

1. `try` 块中的代码正常执行时，`catch` 块被忽略
2. 如果 `try` 块发生异常，控制转移到 `catch` 块
3. `catch` 子句的参数绑定异常信息

---

## 5. 断言系统 (Assertion System)

### 5.1 Assert 语句

**语法**：

```ebnf
assert_stmt ::= "assert" STRING_LITERAL "against" IDENTIFIER ";"
```

**示例**：

```nexa
test "输出验证测试" {
    result = Analyst.run("分析 Apple 股票");
    
    assert "包含股票价格信息" against result;
    assert "包含市场趋势分析" against result;
    assert "不包含敏感信息" against result;
}
```

**语义**：

1. `assert` 使用 LLM 验证语义条件
2. 条件为真时测试通过，否则测试失败
3. 可用于测试声明中进行自动化验证

---

## 6. 类型系统 (Type System)

### 6.1 内置类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `string` | 字符串类型 | `"Hello"` |
| `number` | 数字类型 | `42`, `3.14` |
| `boolean` | 布尔类型 | `true`, `false` |
| `array` | 数组类型 | `["a", "b", "c"]` |
| `object` | 对象类型 | `{"key": "value"}` |

### 6.2 Protocol 类型约束

Protocol 定义结构化输出约束：

```nexa
protocol Report {
    title: "string",
    summary: "string",
    score: "number",
    tags: "array"
}

agent Reporter implements Report {
    role: "报告生成器",
    prompt: "生成结构化报告，包含标题、摘要、评分和标签"
}
```

**运行时验证**：

1. Agent 输出必须符合 Protocol 定义的字段
2. 类型不匹配时自动重试
3. 重试次数由系统配置控制

### 6.3 枚举类型

v0.9+ 支持枚举约束：

```nexa
protocol Status {
    state: "pending|processing|completed|failed"
}
```

---

## 7. 修饰器系统 (Decorator System)

修饰器用于为 Agent 添加元数据和行为约束。

### 7.1 内置修饰器

| 修饰器 | 参数 | 描述 |
|--------|------|------|
| `@limit` | `max_tokens=N` | 限制输出 Token 数量 |
| `@timeout` | `seconds=N` | 设置执行超时时间 |
| `@retry` | `max_attempts=N` | 设置最大重试次数 |
| `@temperature` | `value=N` | 设置模型温度参数 |

### 7.2 使用示例

```nexa
@limit(max_tokens=1024)
@timeout(seconds=30)
@retry(max_attempts=3)
@temperature(value=0.7)
agent ConstrainedAgent {
    role: "受限 Agent",
    prompt: "严格遵守 Token 和时间限制"
}
```

---

## 8. 模块系统 (Module System)

### 8.1 Include 指令

**语法**：

```nexa
include "path/to/module.nxlib"
```

**示例**：

```nexa
// 引入本地库文件
include "lib/tools.nxlib"
include "lib/agents.nxlib"
```

### 8.2 Import 指令

**语法**：

```nexa
import namespace.module as alias
```

**示例**：

```nexa
import std.fs
import std.http
import community.tools as ct
```

---

## 9. 内存模型 (Memory Model)

### 9.1 记忆类型

| 类型 | 描述 | 生命周期 |
|------|------|----------|
| `short` | 短期记忆 | 单次会话 |
| `session` | 会话记忆 | 用户会话期间 |
| `long` | 长期记忆 | 持久化存储 |

### 9.2 记忆属性

```nexa
agent RememberingAgent {
    role: "具备记忆的 Agent",
    prompt: "记住用户的偏好和历史对话",
    memory: "long",
    experience: true
}
```

---

## 10. 错误处理参考 (Error Handling Reference)

详细错误码和解决方案请参考 [错误索引](error_index.md)。

### 10.1 编译时错误

| 错误码 | 描述 |
|--------|------|
| E001 | 未声明的标识符 |
| E002 | 类型不匹配 |
| E003 | 缺少必需属性 |
| E004 | 重复声明 |

### 10.2 运行时错误

| 错误码 | 描述 |
|--------|------|
| E101 | Agent 执行超时 |
| E102 | 模型调用失败 |
| E103 | Protocol 验证失败 |
| E104 | 工具执行错误 |

---

## 📝 附录

### A. EBNF 语法总结

完整的 EBNF 语法定义请参考 [语法参考](../nexa/docs/01_nexa_syntax_reference.md)。

### B. 关键字索引

- [`agent`](#21-agent-声明-agent-declaration) - 定义智能体
- [`tool`](#22-tool-声明-tool-declaration) - 定义工具
- [`protocol`](#23-protocol-声明-protocol-declaration) - 定义输出协议
- [`flow`](#24-flow-声明-flow-declaration) - 定义主流程
- [`test`](#25-test-声明-test-declaration) - 定义测试
- [`match`](#41-意图路由-match-intent) - 意图路由
- [`semantic_if`](#42-语义条件判断-semantic-if) - 语义条件
- [`loop`](#43-语义循环-loop-until) - 循环控制
- [`try/catch`](#44-异常处理-trycatch) - 异常处理
- [`assert`](#51-assert-语句) - 断言验证

---

## 🔗 相关资源

- [快速入门](quickstart.md)
- [完整示例集合](examples.md)
- [常见问题与排查](troubleshooting.md)
- [基础语法](part1_basic.md)