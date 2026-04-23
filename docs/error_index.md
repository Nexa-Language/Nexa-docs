---
comments: true
---

# Nexa 错误索引

本索引收录了 Nexa 编译器和运行时可能产生的所有错误代码、原因分析和解决方案。

---

## 📖 如何使用本索引

1. **按错误码查找**：如果你看到类似 `E001` 的错误码，直接在下方表格中查找
2. **按类别浏览**：错误按编译时错误、运行时错误、契约错误、类型错误等分类
3. **查看解决方案**：每个错误都附带详细的原因分析和解决建议

---

## 1. 编译时错误 (E0xx)

编译时错误在代码编译阶段检测，表示代码存在语法或语义问题。

### E001 - 未声明的标识符

**错误信息**：
```
Error E001: Undeclared identifier 'X'
  --> main.nexa:15:5
   |
15 |     result = UnknownAgent.run(input);
   |              ^^^^^^^^^^^^^ 'UnknownAgent' not found
```

**原因**：
- 引用了未定义的 Agent、Tool 或 Protocol
- 标识符拼写错误
- 忘记引入必要的模块

**解决方案**：

```nexa
// ❌ 错误：未声明
result = WeatherBot.run(input);

// ✅ 正确：先声明再使用
agent WeatherBot {
    role: "天气助手",
    prompt: "回答天气相关问题"
}

result = WeatherBot.run(input);
```

---

### E002 - 类型不匹配

**错误信息**：
```
Error E002: Type mismatch
  --> main.nexa:23:20
   |
23 | protocol Report { score: "number" }
   |                    ^^^^^ expected 'number', found 'string'
```

**原因**：
- Protocol 字段类型与实际输出不匹配
- 类型标注格式错误

**解决方案**：

```nexa
// ❌ 错误：类型标注格式错误
protocol Report {
    score: number    // 类型未加引号
}

// ✅ 正确：类型标注需要加引号
protocol Report {
    score: "number"  // 正确格式
}
```

---

### E003 - 缺少必需属性

**错误信息**：
```
Error E003: Missing required property 'role'
  --> main.nexa:10:1
   |
10 | agent MyAgent {
   | ^^^^^^^^^^^^^ 'role' property is required
```

**原因**：
- Agent 缺少必需的 `role` 属性
- Agent 缺少必需的 `prompt` 属性

**解决方案**：

```nexa
// ❌ 错误：缺少必需属性
agent MyAgent {
    model: "gpt-4"
}

// ✅ 正确：添加必需属性
agent MyAgent {
    role: "助手",
    prompt: "帮助用户解决问题",
    model: "gpt-4"
}
```

---

### E004 - 语法错误

**错误信息**：
```
Error E004: Syntax error
  --> main.nexa:5:1
   |
5 | agent { }
   | ^^^^^^^^ Expected IDENTIFIER after 'agent'
```

**原因**：
- 缺少标识符名称
- 语法结构不完整
- 使用了无效的语法构造

**解决方案**：检查语法是否符合 Nexa 规范，参考 [语言参考手册](reference.md)。

---

### E005 - 重复声明

**错误信息**：
```
Error E005: Duplicate declaration 'MyAgent'
  --> main.nexa:20:1
   |
20 | agent MyAgent { ... }
   | ^^^^^^^^^^^^^ 'MyAgent' already declared
```

**原因**：
- 同一文件中重复声明了相同名称的 Agent、Tool 或 Protocol

**解决方案**：使用不同的名称或删除重复声明。

---

## 2. 运行时错误 (E1xx)

运行时错误在程序执行过程中发生。

### E101 - Agent 执行失败

**错误信息**：
```
Error E101: Agent execution failed
  Agent 'Analyst' failed after 3 retries
```

**原因**：
- LLM API 调用失败（网络错误、API Key 无效）
- 模型返回格式不符合预期
- 执行超时

**解决方案**：

```nexa
// 设置备用模型
agent MyAgent {
    model: "gpt-4",
    fallback: "gpt-3.5-turbo",
    timeout: 60,
    retry: 5
}
```

---

### E102 - Tool 执行失败

**错误信息**：
```
Error E102: Tool execution failed
  Tool 'web_search' returned error: HTTP timeout
```

**原因**：
- 外部服务不可用
- 工具参数不正确
- 执行超时

**解决方案**：检查工具参数、网络连接和超时设置。

---

### E103 - 管道执行失败

**错误信息**：
```
Error E103: Pipeline execution failed
  Pipeline stage 'Reviewer' failed
```

**原因**：
- 管道中某个 Agent 执行失败
- 数据传递格式不匹配

**解决方案**：检查管道中每个 Agent 的独立执行情况，确保数据格式兼容。

---

### E104 - Intent 路由失败

**错误信息**：
```
Error E104: Intent routing failed
  No matching intent for input: "..."
```

**原因**：
- 意图匹配器无法识别用户输入
- 所有 intent 分支都未匹配

**解决方案**：添加 `_` 通配符分支作为默认处理。

```nexa
match user_input {
    intent("查询天气") => WeatherBot.run(user_input),
    intent("查询新闻") => NewsBot.run(user_input),
    _ => ChatBot.run(user_input)    // 默认分支
}
```

---

## 3. 契约错误 (E2xx) — v1.2.0+

### E201 - ContractViolation (requires 前置条件违反)

**错误信息**：
```
ContractViolation(requires:deterministic, message="amount must be positive")
  --> transfer.nexa:5
```

**原因**：
- `requires` 确定性条件不满足（如 `amount > 0` 但传入负数）
- `requires` 语义条件不满足（如 "sender has sufficient balance" 但余额不足）

**解决方案**：

```nexa
// 确定性契约：确保传入参数满足条件
flow transfer(amount: int) -> Result
    requires: amount > 0
{
    if (amount <= 0) {
        return Result::Err("Invalid amount");
    }
    // ...
}

// 语义契约：确保输入满足语义要求
flow review(code: string) -> Report
    requires: "input contains valid source code"
{
    // ...
}
```

---

### E202 - ContractViolation (ensures 后置条件违反)

**错误信息**：
```
ContractViolation(ensures:semantic, message="result must include actionable feedback")
  --> review.nexa:8
```

**原因**：
- `ensures` 确定性条件不满足（如 `result.success == true` 但返回失败）
- `ensures` 语义条件不满足（如 "result includes actionable feedback" 但输出无建议）

**解决方案**：确保函数返回值满足后置条件，或调整条件使其更合理。

---

### E203 - ContractViolation (invariant 不变式违反)

**错误信息**：
```
ContractViolation(invariant:deterministic, message="state must be idle or running")
```

**原因**：
- `invariant` 条件在对象生命周期中被违反

**解决方案**：确保对象状态始终满足不变式约束。

---

## 4. 类型错误 (E3xx) — v1.3.1+

### E301 - TypeViolation (strict 模式类型违反)

**错误信息**：
```
TypeViolation: Expected Int, got String
  --> main.nexa:10
   |
10 | let x: Int = "hello"
   |               ^^^^^^^ Type mismatch
```

**原因**：
- `NEXA_TYPE_MODE=strict` 模式下，类型不匹配导致运行时错误

**解决方案**：

```nexa
// 确保类型匹配
let x: Int = 42           // ✅ 正确
let y: String = "hello"   // ✅ 正确

// 或切换到 warn 模式
// 设置 NEXA_TYPE_MODE=warn
```

---

### E302 - TypeWarning (warn 模式类型警告)

**错误信息**：
```
TypeWarning: Expected Int, got String (mode: warn)
  --> main.nexa:10
```

**原因**：
- `NEXA_TYPE_MODE=warn` 模式下，类型不匹配仅发出警告，程序继续执行

**解决方案**：修复类型标注或值，确保类型一致。

---

### E303 - Protocol 类型验证失败

**错误信息**：
```
Error E303: Protocol validation failed
  Protocol 'ReviewResult' field 'score' expected int, got string
```

**原因**：
- Agent 输出不符合 `protocol` 定义的字段类型
- LLM 返回的 JSON 格式与协议不匹配

**解决方案**：

```nexa
// 使用 implements 约束 Agent 输出
agent Reviewer implements ReviewResult {
    prompt: "Review the code. Return JSON with score (int) and summary (string)."
}
```

---

## 5. 数据库错误 (E4xx) — v1.3.5+

### E401 - DatabaseError (连接失败)

**错误信息**：
```
DatabaseError: Failed to connect to sqlite://data.db
```

**原因**：
- 数据库文件路径不存在
- SQLite 文件权限问题
- PostgreSQL 连接参数错误

**解决方案**：检查数据库路径、权限和连接参数。

---

### E402 - DatabaseError (查询失败)

**错误信息**：
```
DatabaseError: Query failed: SELECT * FROM nonexistent_table
```

**原因**：
- SQL 语法错误
- 表或列不存在
- 参数绑定错误

**解决方案**：检查 SQL 语句和表结构。

---

### E403 - DatabaseError (事务失败)

**错误信息**：
```
DatabaseError: Transaction failed, rolled back
```

**原因**：
- 事务中的操作失败导致回滚

**解决方案**：检查事务中的每个操作，确保数据一致性。

---

## 6. 认证错误 (E5xx) — v1.3.6+

### E501 - AuthError (认证失败)

**错误信息**：
```
AuthError: Invalid API key format
```

**原因**：
- API Key 格式不正确（应为 `nexa-ak-{32hex}` 格式）
- API Key 已过期或被撤销

**解决方案**：使用 `std.auth.api_key_generate` 生成正确格式的 API Key。

---

### E502 - AuthError (JWT 错误)

**错误信息**：
```
AuthError: JWT signature verification failed
```

**原因**：
- JWT 签名验证失败
- JWT 过期
- JWT 格式不正确

**解决方案**：检查 JWT 密钥配置和 Token 有效期。

---

### E503 - AuthError (CSRF 验证失败)

**错误信息**：
```
AuthError: CSRF token validation failed
```

**原因**：
- CSRF Token 不匹配
- Token 过期

**解决方案**：确保表单中包含正确的 CSRF Token。

---

### E504 - AuthError (OAuth 流程错误)

**错误信息**：
```
AuthError: OAuth PKCE flow failed
```

**原因**：
- OAuth Provider 配置错误
- PKCE code_verifier 不匹配
- redirect_uri 不匹配

**解决方案**：检查 OAuth Provider 配置（client_id, client_secret, redirect_uri）。

---

## 7. KV 存储错误 (E6xx) — v1.3.6+

### E601 - KVError (操作失败)

**错误信息**：
```
KVError: Key 'user_prefs' not found
```

**原因**：
- 键不存在
- KV Store 未打开
- TTL 过期

**解决方案**：使用 `??` 操作符提供默认值，或先检查键是否存在。

```nexa
value = kv.get("user_prefs") ?? "default"
if (kv.has("user_prefs")) {
    value = kv.get("user_prefs")
}
```

---

### E602 - KVError (序列化失败)

**错误信息**：
```
KVError: Failed to deserialize value for key 'config'
```

**原因**：
- 存储的数据类型与读取类型不匹配
- 数据损坏

**解决方案**：使用类型安全的读取方法（`kv_get_int`, `kv_get_str`, `kv_get_json`）。

---

## 8. 并发错误 (E7xx) — v1.3.6+

### E701 - ConcurrencyError (任务取消)

**错误信息**：
```
ConcurrencyError: Task 'my_task' was cancelled
```

**原因**：
- 任务被 `cancel_task` 主动取消
- 任务超时被自动取消

**解决方案**：检查任务逻辑，确保取消是预期行为。

---

### E702 - ConcurrencyError (通道关闭)

**错误信息**：
```
ConcurrencyError: Channel is closed
```

**原因**：
- 向已关闭的通道发送消息
- 从已关闭的通道接收消息

**解决方案**：在发送/接收前检查通道状态，或使用 `try_recv` 避免阻塞。

---

### E703 - ConcurrencyError (race 全部失败)

**错误信息**：
```
ConcurrencyError: All tasks in race failed
```

**原因**：
- `race` 中所有任务都失败

**解决方案**：确保至少有一个任务能够成功完成。

---

## 9. 模板错误 (E8xx) — v1.3.6+

### E801 - TemplateError (编译失败)

**错误信息**：
```
TemplateError: Failed to compile template: unclosed {{#for}} block
```

**原因**：
- 模板语法错误（未闭合的块）
- 过滤器名称不存在

**解决方案**：检查模板语法，确保所有块正确闭合。

---

### E802 - TemplateError (渲染失败)

**错误信息**：
```
TemplateError: Failed to render template: variable 'name' not found
```

**原因**：
- 模板中引用的变量在数据中不存在
- 数据格式不匹配

**解决方案**：使用 `| default(val)` 过滤器提供默认值。

```nexa
template"""Hello {{name | default("Guest")}}!"""
```

---

## 10. 模式匹配错误 (E9xx) — v1.3.x+

### E901 - PatternMatchError (无匹配分支)

**错误信息**：
```
PatternMatchError: No matching pattern for value
```

**原因**：
- `match` 表达式中没有分支匹配当前值
- 缺少 `_` 通配符分支

**解决方案**：添加 `_` 通配符分支作为默认匹配。

```nexa
match result {
    Option::Some(v) => v
    Option::None => "no response"
    _ => "unknown"    // 通配符兜底
}
```

---

### E902 - PatternMatchError (解构失败)

**错误信息**：
```
PatternMatchError: Destructuring failed for pattern (a, b)
```

**原因**：
- 解构模式与数据结构不匹配（如对非元组值使用元组模式）

**解决方案**：确保解构模式与数据结构类型一致。

---

## 11. ADT 错误 (EAx) — v1.3.x+

### EA01 - ADTError (结构体操作失败)

**错误信息**：
```
ADTError: Struct 'Point' not found
```

**原因**：
- 引用未注册的结构体
- 字段访问不存在

**解决方案**：确保结构体已声明，字段名正确。

---

### EA02 - ADTError (枚举操作失败)

**错误信息**：
```
ADTError: Variant 'Some' not found in enum 'Option'
```

**原因**：
- 引用未注册的枚举变体
- 变体名称拼写错误

**解决方案**：确保枚举和变体名称正确。

---

### EA03 - ADTError (Trait 方法调用失败)

**错误信息**：
```
ADTError: No impl found for trait 'Printable' on type 'Point'
```

**原因**：
- 类型未实现该 trait
- impl 声明缺失

**解决方案**：添加 `impl` 声明。

```nexa
impl Printable for Point {
    fn format() -> String { ... }
}
```

---

## 12. Job 系统错误 (EBx) — v1.3.3+

### EB01 - JobError (任务执行失败)

**错误信息**：
```
JobError: Job 'SendEmail' failed after 2 retries
```

**原因**：
- 任务逻辑执行失败
- 重试次数耗尽

**解决方案**：检查 `on_failure` 处理逻辑，增加 retry 次数。

---

### EB02 - JobError (任务超时)

**错误信息**：
```
JobError: Job 'AnalyzeDoc' timed out after 120s
```

**原因**：
- 任务执行时间超过 timeout 设置

**解决方案**：增加 timeout 值或优化任务逻辑。

---

### EB03 - JobError (死信任务)

**错误信息**：
```
JobError: Job 'SendEmail' is in dead letter queue
```

**原因**：
- 任务重试全部失败，进入死信队列

**解决方案**：使用 `nexa jobs retry <job_id>` 重试死信任务。

---

## 13. HTTP Server 错误 (ECx) — v1.3.4+

### EC01 - HTTPError (路由未找到)

**错误信息**：
```
HTTPError: No route found for GET /unknown
```

**原因**：
- 请求路径未在 server DSL 中定义

**解决方案**：在 server 声明中添加对应路由。

---

### EC02 - ContractViolation (HTTP 契约违反)

**错误信息**：
```
ContractViolation(requires) → HTTP 401 Unauthorized
ContractViolation(ensures) → HTTP 403 Forbidden
```

**原因**：
- HTTP 请求违反了路由的 `requires` 前置条件 → 401
- HTTP 响应违反了 `ensures` 后置条件 → 403

**解决方案**：确保请求满足前置条件，响应满足后置条件。

---

## 📊 错误码速查表

| 错误码 | 类别 | 说明 |
|--------|------|------|
| E001 | 编译时 | 未声明的标识符 |
| E002 | 编译时 | 类型不匹配 |
| E003 | 编译时 | 缺少必需属性 |
| E004 | 编译时 | 语法错误 |
| E005 | 编译时 | 重复声明 |
| E101 | 运行时 | Agent 执行失败 |
| E102 | 运行时 | Tool 执行失败 |
| E103 | 运行时 | 管道执行失败 |
| E104 | 运行时 | Intent 路由失败 |
| E201 | 契约 | requires 前置条件违反 |
| E202 | 契约 | ensures 后置条件违反 |
| E203 | 契约 | invariant 不变式违反 |
| E301 | 类型 | TypeViolation (strict) |
| E302 | 类型 | TypeWarning (warn) |
| E303 | 类型 | Protocol 类型验证失败 |
| E401 | 数据库 | 连接失败 |
| E402 | 数据库 | 查询失败 |
| E403 | 数据库 | 事务失败 |
| E501 | 认证 | 认证失败 |
| E502 | 认证 | JWT 错误 |
| E503 | 认证 | CSRF 验证失败 |
| E504 | 认证 | OAuth 流程错误 |
| E601 | KV | 操作失败 |
| E602 | KV | 序列化失败 |
| E701 | 并发 | 任务取消 |
| E702 | 并发 | 通道关闭 |
| E703 | 并发 | race 全部失败 |
| E801 | 模板 | 编译失败 |
| E802 | 模板 | 渲染失败 |
| E901 | 模式匹配 | 无匹配分支 |
| E902 | 模式匹配 | 解构失败 |
| EA01 | ADT | 结构体操作失败 |
| EA02 | ADT | 枚举操作失败 |
| EA03 | ADT | Trait 方法调用失败 |
| EB01 | Job | 任务执行失败 |
| EB02 | Job | 任务超时 |
| EB03 | Job | 死信任务 |
| EC01 | HTTP | 路由未找到 |
| EC02 | HTTP | 契约违反 |

---

## 🔗 相关资源

- [语言参考手册](reference.md)
- [标准库 API](stdlib_reference.md)
- [常见问题与排查](troubleshooting.md)
- [快速入门](quickstart.md)