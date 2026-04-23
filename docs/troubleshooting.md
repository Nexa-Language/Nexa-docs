---
comments: true
---

# 常见问题与排查指南

本文档汇总了使用 Nexa 过程中常见的问题及其解决方案。如果你遇到了问题，请先查阅本指南。

---

## 📋 目录

- [安装与环境问题](#1-安装与环境问题)
- [语法错误排查](#2-语法错误排查)
- [运行时错误排查](#3-运行时错误排查)
- [模型调用问题](#4-模型调用问题)
- [工具调用问题](#5-工具调用问题)
- [Protocol 相关问题](#6-protocol-相关问题)
- [契约与类型问题 (v1.2+)](#7-契约与类型问题)
- [数据库问题 (v1.3.5+)](#8-数据库问题)
- [认证问题 (v1.3.6+)](#9-认证问题)
- [并发问题 (v1.3.6+)](#10-并发问题)
- [HTTP Server 问题 (v1.3.4+)](#11-http-server-问题)
- [Job 系统问题 (v1.3.3+)](#12-job-系统问题)
- [调试技巧](#13-调试技巧)

---

## 1. 安装与环境问题

### 1.1 `pip install` 失败

**症状**：
```
ERROR: Could not find a version that satisfies the requirement nexa
```

**原因**：Nexa 尚未发布到 PyPI，需要从源码安装。

**解决方案**：
```bash
git clone https://github.com/your-org/nexa.git
cd nexa
pip install -e .
```

---

### 1.2 Python 版本不兼容

**症状**：
```
SyntaxError: invalid syntax
```
或
```
TypeError: ... got an unexpected keyword argument
```

**原因**：Nexa 需要 Python 3.10 或更高版本。

**解决方案**：
```bash
# 检查 Python 版本
python --version

# 如果版本低于 3.10，请升级或使用虚拟环境
# 使用 conda
conda create -n nexa python=3.10
conda activate nexa

# 或使用 venv
python3.10 -m venv nexa-env
source nexa-env/bin/activate  # Linux/macOS
# nexa-env\Scripts\activate   # Windows
```

---

### 1.3 依赖冲突

**症状**：
```
ERROR: Cannot install nexa because these package versions have conflicting dependencies
```

**解决方案**：
```bash
# 清理并重新安装
pip uninstall nexa -y
pip cache purge
pip install -e . --no-cache-dir
```

---

### 1.4 `nexa: command not found`

**症状**：
```bash
$ nexa run hello.nx
bash: nexa: command not found
```

**原因**：pip 安装路径不在 PATH 中，或未激活虚拟环境。

**解决方案**：
```bash
# 方案1：确保激活了虚拟环境
source nexa-env/bin/activate

# 方案2：使用 python -m 调用
python -m nexa run hello.nx

# 方案3：添加 pip 路径到 PATH（不推荐）
export PATH="$HOME/.local/bin:$PATH"
```

---

## 2. 语法错误排查

### 2.1 解析错误：Unexpected token

**症状**：
```
ParseError: Unexpected token '}' at line 15
```

**常见原因**：

1. **缺少逗号或分号**
```nexa
// ❌ 错误
agent Bot {
    role: "助手"    // 缺少逗号
    prompt: "..."
}

// ✅ 正确
agent Bot {
    role: "助手",
    prompt: "..."
}
```

2. **括号不匹配**
```nexa
// ❌ 错误
flow main {
    result = Bot.run("hello"
}

// ✅ 正确
flow main {
    result = Bot.run("hello");
}
```

3. **字符串未闭合**
```nexa
// ❌ 错误
agent Bot {
    prompt: "这是一个很长的提示词
            换行了但没有闭合"
}

// ✅ 正确：使用三引号
agent Bot {
    prompt: """
        这是一个很长的提示词
        换行也没问题
    """
}
```

---

### 2.2 Agent 未定义

**症状**：
```
NameError: name 'MyAgent' is not defined
```

**原因**：Agent 定义在 flow 之后，或拼写错误。

**解决方案**：
```nexa
// ❌ 错误：Agent 在 flow 之后定义
flow main {
    result = MyAgent.run("hello");
}

agent MyAgent {
    prompt: "..."
}

// ✅ 正确：Agent 在 flow 之前定义
agent MyAgent {
    prompt: "..."
}

flow main {
    result = MyAgent.run("hello");
}
```

---

### 2.3 属性名拼写错误

**症状**：Agent 行为异常，属性未生效。

**常见拼写错误**：
```nexa
// ❌ 常见错误拼写
agent Bot {
    promt: "...",        // 应为 prompt
    moedl: "gpt-4",      // 应为 model
    rol: "助手"          // 应为 role
}

// ✅ 正确拼写
agent Bot {
    prompt: "...",
    model: "gpt-4",
    role: "助手"
}
```

**检查清单**：
| 正确拼写 | 常见错误 |
|---------|---------|
| `prompt` | `promt`, `prompts` |
| `model` | `moedl`, `Model` |
| `role` | `rol`, `Role` |
| `tools` | `tool`, `Tool` |
| `memory` | `memmory`, `Memory` |

---

### 2.4 Protocol 语法错误

**症状**：
```
InvalidProtocolError: Protocol field type must be a string
```

**错误示例**：
```nexa
// ❌ 错误：类型没有用引号包裹
protocol UserInfo {
    name: string,        // 应为 "string"
    age: int             // 应为 "int"
}

// ✅ 正确
protocol UserInfo {
    name: "string",
    age: "int"
}
```

---

## 3. 运行时错误排查

### 3.1 API Key 未找到

**症状**：
```
RuntimeError: API key not found for provider 'openai'
```

**解决方案**：

1. **检查 secrets.nxs 文件是否存在**
```bash
ls -la secrets.nxs
```

2. **检查密钥格式是否正确**
```bash
# secrets.nxs 内容示例
OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxx"
MINIMAX_API_KEY = "xxxxxxxxxxxx"
MINIMAX_GROUP_ID = "xxxxxxxxxxxx"
```

3. **检查文件位置**
```
project/
├── secrets.nxs      # 必须在项目根目录
├── main.nx
└── ...
```

---

### 3.2 网络连接超时

**症状**：
```
httpx.ConnectTimeout: Connection timed out
```

**解决方案**：

1. **检查网络连接**
```bash
curl -I https://api.openai.com
```

2. **配置代理（如需要）**
```bash
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
```

3. **增加超时时间**（在代码中）
```nexa
agent Bot {
    model: "openai/gpt-4",
    prompt: "...",
    timeout: 60  // 60秒超时
}
```

---

### 3.3 内存不足

**症状**：
```
MemoryError: Unable to allocate array
```

**原因**：长对话历史或大量并发 Agent。

**解决方案**：

1. **启用上下文压缩**
```nexa
agent Bot {
    prompt: "...",
    max_history_turns: 5  // 限制历史轮数
}
```

2. **使用缓存减少重复计算**
```nexa
agent Bot {
    prompt: "...",
    cache: true  // 启用智能缓存
}
```

3. **减少并发数量**
```nexa
// ❌ 避免过多并行 Agent
input |>> [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10]

// ✅ 分批处理
input |>> [A1, A2, A3]
```

---

### 3.4 循环未终止

**症状**：`loop until` 循环一直运行，直到超时。

**原因**：终止条件太模糊，LLM 无法准确判断。

**解决方案**：

1. **使用更明确的终止条件**
```nexa
// ❌ 模糊的条件
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("文章完美")  // 太主观

// ✅ 更明确的条件
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("Reviewer 明确表示'通过'且没有修改建议")
```

2. **添加最大循环次数保护**
```nexa
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("文章完美" or runtime.meta.loop_count >= 5)

// 检查是否超限
if (runtime.meta.loop_count >= 5) {
    print("达到最大重试次数，请人工检查");
}
```

---

## 4. 模型调用问题

### 4.1 模型名称格式错误

**症状**：
```
ModelError: Unknown model format: gpt-4
```

**原因**：模型名称必须包含提供商前缀。

**正确格式**：
```nexa
// ✅ 正确格式
model: "openai/gpt-4"
model: "openai/gpt-4-turbo"
model: "deepseek/deepseek-chat"
model: "minimax/minimax-m2.5"
model: "anthropic/claude-3-sonnet"

// ❌ 错误格式
model: "gpt-4"           // 缺少提供商
model: "GPT-4"           // 大小写错误
model: "deepseek-chat"   // 缺少斜杠
```

---

### 4.2 模型不支持某些功能

**症状**：
```
NotImplementedError: Model 'xxx' does not support function calling
```

**解决方案**：

选择支持所需功能的模型：

| 功能 | 支持的模型 |
|-----|----------|
| Function Calling | GPT-4, GPT-3.5-turbo, DeepSeek-Chat |
| Structured Output | GPT-4, Claude-3, DeepSeek-Chat |
| Vision | GPT-4-vision, Claude-3, MiniMax-VL |

---

### 4.3 Rate Limit 限制

**症状**：
```
RateLimitError: Rate limit exceeded for model
```

**解决方案**：

1. **配置 Fallback 模型**
```nexa
agent Bot {
    model: ["openai/gpt-4", fallback: "deepseek/deepseek-chat"],
    prompt: "..."
}
```

2. **添加重试配置**
```nexa
agent Bot {
    model: "openai/gpt-4",
    prompt: "...",
    retry: 3,           // 重试次数
    retry_delay: 5      // 重试延迟（秒）
}
```

3. **使用缓存减少请求**
```nexa
agent Bot {
    cache: true,  // 相同请求复用结果
    prompt: "..."
}
```

---

### 4.4 输出截断

**症状**：模型输出在中间被截断。

**原因**：达到 token 限制。

**解决方案**：

```nexa
agent Bot {
    prompt: "...",
    max_tokens: 4096  // 增加输出长度限制
}
```

或使用装饰器：
```nexa
@limit(max_tokens=4096)
agent Bot {
    prompt: "..."
}
```

---

## 5. 工具调用问题

### 5.1 工具未找到

**症状**：
```
ToolNotFoundError: Tool 'my_tool' not found in registry
```

**原因**：工具未正确注册或导入。

**解决方案**：

1. **检查 uses 声明**
```nexa
// ❌ 错误：工具未声明
agent Bot {
    prompt: "..."
}
// 后面调用 Bot.run() 时无法使用工具

// ✅ 正确：声明使用的工具
agent Bot uses std.http, std.fs {
    prompt: "..."
}
```

2. **检查标准库导入**
```nexa
// 如果使用自定义工具，确保路径正确
agent Bot uses "my_tools.py" {
    prompt: "..."
}
```

---

### 5.2 工具参数错误

**症状**：
```
ToolExecutionError: Invalid parameters for tool 'xxx'
```

**解决方案**：

检查工具定义的参数格式：
```nexa
// ❌ 错误：参数格式不正确
tool MyTool {
    description: "工具描述",
    parameters: {
        param1: string  // 缺少引号
    }
}

// ✅ 正确
tool MyTool {
    description: "工具描述",
    parameters: {
        "param1": "string",
        "param2": "number"
    }
}
```

---

### 5.3 工具执行超时

**症状**：
```
TimeoutError: Tool execution timed out after 30s
```

**解决方案**：

```nexa
agent Bot uses std.http {
    prompt: "...",
    tool_timeout: 60  // 增加超时时间
}
```

---

## 6. Protocol 相关问题

### 6.1 输出格式不符合 Protocol

**症状**：
```
ProtocolValidationError: Expected field 'xxx' but got 'yyy'
```

**原因**：LLM 输出不符合定义的 Protocol。

**自动修复机制**：

Nexa 会自动尝试修复，但如果多次失败，可以：

1. **简化 Protocol**
```nexa
// ❌ 过于复杂的 Protocol
protocol ComplexData {
    field1: "string",
    field2: "list[dict[string, any]]",  // 太复杂
    field3: "dict[string, list[int]]"
}

// ✅ 简化后的 Protocol
protocol SimpleData {
    field1: "string",
    field2: "string",  // 用字符串表示复杂结构
    field3: "string"
}
```

2. **在 Prompt 中明确格式要求**
```nexa
agent DataExtractor implements MyProtocol {
    prompt: """
    提取数据并严格按照 JSON 格式输出。
    必须包含字段：field1, field2, field3
    """
}
```

---

### 6.2 Protocol 类型不匹配

**症状**：
```
TypeError: Expected 'int' but got 'string'
```

**解决方案**：

确保 Protocol 中的类型与预期一致：
```nexa
// 正确的类型标注
protocol DataTypes {
    text: "string",      // 字符串
    number: "int",       // 整数
    price: "float",      // 浮点数
    flag: "boolean",     // 布尔值
    tags: "list[string]" // 字符串列表
}
```

---

## 7. 契约与类型问题 (v1.2+)

### 7.1 ContractViolation: requires 前置条件违反

**症状**:
```
ContractViolation: requires precondition failed: "input must be non-empty"
```

**原因**: `requires` 契约条件在函数/Agent 执行前未满足。

**解决方案**:

1. **检查输入数据**：确保传入的参数满足 `requires` 条件
```nexa
agent Validator {
    requires: "input must be non-empty"
    role: "validator"
    prompt: "validate input"
}

// ✅ 正确：确保输入非空
flow main {
    data = "some content"
    result = Validator.run(data)
}

// ❌ 错误：传入空值
flow main {
    data = ""
    result = Validator.run(data)  // ContractViolation!
}
```

2. **使用 `??` 提供默认值**：
```nexa
flow main {
    data = raw_input ?? "default content"
    result = Validator.run(data)
}
```

3. **使用 `otherwise` 处理契约违反**：
```nexa
flow main {
    result = Validator.run(data) otherwise "fallback result"
}
```

### 7.2 ContractViolation: ensures 后置条件违反

**症状**:
```
ContractViolation: ensures postcondition failed: "output must contain summary"
```

**原因**: Agent 输出未满足 `ensures` 条件。

**解决方案**:

1. **优化 prompt**：使 Agent 输出更可靠地满足后置条件
2. **使用 `implements` 自动重试纠偏**：Protocol + implements 会自动重试
3. **放宽 ensures 条件**：如果条件过于严格，适当放宽

### 7.3 ContractViolation: invariant 不变式违反

**症状**:
```
ContractViolation: invariant violation: "count must be >= 0"
```

**原因**: 对象状态在操作过程中违反了不变式约束。

**解决方案**:

1. **检查状态变更逻辑**：确保所有操作都维护不变式
2. **使用 `old` 表达式验证状态变化**：
```nexa
db MyDB {
    invariant: "count >= 0"
    ensures: "count == old(count) + 1"
}
```

### 7.4 TypeViolation: strict 模式类型违反

**症状**:
```
TypeViolation: expected type 'int', got 'str'
```

**原因**: 在 `NEXA_TYPE_MODE=strict` 模式下，类型不匹配会直接抛出异常。

**解决方案**:

1. **切换到 warn 模式**（开发阶段推荐）：
```bash
export NEXA_TYPE_MODE=warn
nexa run script.nx
```

2. **添加类型标注**：确保变量和函数有正确的类型声明
3. **使用类型收窄**：
```nexa
flow main {
    value: int = some_input
    // 类型收窄后，value 保证为 int
}
```

### 7.5 TypeWarning: warn 模式类型警告

**症状**:
```
TypeWarning: variable 'x' inferred as 'str', annotated as 'int'
```

**原因**: 在 `NEXA_TYPE_MODE=warn` 模式下，类型不匹配只产生警告，不中断执行。

**解决方案**:

1. **检查警告信息**：确认是否为真正的类型问题
2. **修复类型标注**：使标注与实际值一致
3. **使用 `nexa lint` 检查**：
```bash
nexa lint script.nx --warn-untyped
```

---

## 8. 数据库问题 (v1.3.5+)

### 8.1 DatabaseError: 连接失败

**症状**:
```
DatabaseError: failed to connect to SQLite database: /path/to/db.sqlite
```

**原因**: 数据库文件路径不存在或权限不足。

**解决方案**:

1. **检查文件路径**：确保路径正确且有写权限
```nexa
db MyDB {
    type: "sqlite"
    path: "./data/app.db"  // 使用相对路径
}
```

2. **使用内存数据库**（开发阶段）：
```nexa
db MyDB {
    type: "sqlite"
    path: ":memory:"  // 内存数据库，无需文件
}
```

3. **创建数据目录**：
```bash
mkdir -p ./data
```

### 8.2 DatabaseError: 查询失败

**症状**:
```
DatabaseError: query failed: SELECT * FROM users
```

**原因**: SQL 语法错误或表不存在。

**解决方案**:

1. **检查 SQL 语法**：确保 SQL 语句正确
2. **确保表已创建**：先执行 CREATE TABLE 再查询
```nexa
flow main {
    db_handle = std.db.sqlite.connect(":memory:")
    std.db.sqlite.execute(db_handle, "CREATE TABLE users (id INT, name TEXT)")
    std.db.sqlite.execute(db_handle, "INSERT INTO users VALUES (1, 'Alice')")
    result = std.db.sqlite.query(db_handle, "SELECT * FROM users")
    std.db.sqlite.close(db_handle)
}
```

3. **使用参数化查询**：避免 SQL 注入
```nexa
result = std.db.sqlite.query(db_handle, "SELECT * FROM users WHERE id = ?", params: [1])
```

### 8.3 DatabaseError: 事务失败

**症状**:
```
DatabaseError: transaction failed: commit error
```

**原因**: 事务提交失败，可能因为并发冲突或约束违反。

**解决方案**:

1. **使用显式事务控制**：
```nexa
std.db.sqlite.begin(db_handle)
std.db.sqlite.execute(db_handle, "INSERT ...")
std.db.sqlite.commit(db_handle)  // 显式提交
```

2. **捕获错误并回滚**：
```nexa
flow main {
    std.db.sqlite.begin(db_handle)
    result = std.db.sqlite.execute(db_handle, "INSERT ...") otherwise {
        std.db.sqlite.rollback(db_handle)
    }
}
```

---

## 9. 认证问题 (v1.3.6+)

### 9.1 AuthError: 认证失败

**症状**:
```
AuthError: authentication failed: invalid credentials
```

**原因**: 用户名/密码错误或认证配置不正确。

**解决方案**:

1. **检查 auth 声明配置**：
```nexa
auth MyApp {
    type: "jwt"
    secret: secret.JWT_SECRET
    algorithms: ["HS256"]
}
```

2. **确保密钥已配置**：检查 `secrets.nxs` 文件
3. **使用 `nexa validate` 检查配置**：
```bash
nexa validate script.nx
```

### 9.2 AuthError: JWT 错误

**症状**:
```
AuthError: JWT error: token expired
```

**原因**: JWT token 过期或签名无效。

**解决方案**:

1. **设置合理的过期时间**：
```nexa
auth MyApp {
    type: "jwt"
    secret: secret.JWT_SECRET
    expires_in: 3600  // 1 小时
}
```

2. **使用 std.auth.jwt_verify 验证 token**：
```nexa
flow main {
    valid = std.auth.jwt_verify(token, secret.JWT_SECRET)
    if valid {
        // 处理请求
    } otherwise {
        // 返回 401
    }
}
```

### 9.3 AuthError: CSRF 验证失败

**症状**:
```
AuthError: CSRF validation failed: missing csrf_token
```

**原因**: 请求缺少 CSRF token 或 token 不匹配。

**解决方案**:

1. **在表单中包含 CSRF token**：
```nexa
flow main {
    csrf_token = std.auth.csrf_generate(session_id)
    // 将 token 包含在表单/请求中
}
```

2. **验证 CSRF token**：
```nexa
flow main {
    valid = std.auth.csrf_validate(session_id, submitted_token)
    if valid {
        // 处理请求
    } otherwise {
        // 拒绝请求
    }
}
```

### 9.4 AuthError: OAuth 流程错误

**症状**:
```
AuthError: OAuth flow error: invalid redirect_uri
```

**原因**: OAuth 配置错误（redirect_uri 不匹配、client_id 无效等）。

**解决方案**:

1. **检查 OAuth 配置**：确保 redirect_uri 与 OAuth 提供商注册的一致
2. **使用 std.auth.oauth_* 工具逐步调试**：
```nexa
flow main {
    auth_url = std.auth.oauth_github_authorize(client_id, redirect_uri)
    // 用户访问 auth_url 授权后回调
    token = std.auth.oauth_github_callback(code, client_id, client_secret)
}
```

---

## 10. 并发问题 (v1.3.6+)

### 10.1 ConcurrencyError: 任务取消

**症状**:
```
ConcurrencyError: task cancelled: timeout exceeded
```

**原因**: 并发任务因超时或显式取消而被终止。

**解决方案**:

1. **设置合理的超时时间**：
```nexa
flow main {
    result = std.concurrent.spawn(task_fn, timeout: 30)
}
```

2. **使用 `otherwise` 处理取消**：
```nexa
flow main {
    result = std.concurrent.spawn(task_fn) otherwise "fallback"
}
```

### 10.2 ConcurrencyError: 通道关闭

**症状**:
```
ConcurrencyError: channel closed: cannot send to closed channel
```

**原因**: 尝试向已关闭的 Channel 发送数据。

**解决方案**:

1. **检查 Channel 状态**：在发送前确认 Channel 未关闭
2. **使用 `??` 处理空通道**：
```nexa
flow main {
    ch = std.concurrent.channel(10)
    value = std.concurrent.ch_recv(ch) ?? "default"
}
```

3. **正确关闭 Channel**：只在所有发送者完成后关闭

### 10.3 ConcurrencyError: race 全部失败

**症状**:
```
ConcurrencyError: race all failed: no task completed successfully
```

**原因**: `race` 中所有并发任务都失败了。

**解决方案**:

1. **增加更多候选任务**：提供更多备选方案
2. **使用 `otherwise` 为每个任务提供降级**：
```nexa
flow main {
    result = std.concurrent.race([
        primary_task otherwise None,
        backup_task otherwise None
    ])
}
```

---

## 11. HTTP Server 问题 (v1.3.4+)

### 11.1 路由未找到 (EC01)

**症状**:
```
HTTPError: route not found: POST /api/unknown
```

**原因**: 请求的路径未在 server 声明中定义。

**解决方案**:

1. **检查路由定义**：确保 server 声明中包含该路由
```nexa
server MyApp {
    route "/api/data": DataAgent
    route "/api/process": ProcessAgent
}
```

2. **使用 `nexa routes` 查看所有路由**：
```bash
nexa routes script.nx
```

3. **检查请求方法和路径**：确保 HTTP 方法（GET/POST）与路由匹配

### 11.2 契约违反映射为 HTTP 状态码 (EC02)

**症状**:
```
HTTP 401: ContractViolation (requires precondition failed)
HTTP 403: ContractViolation (ensures postcondition failed)
```

**原因**: 契约违反自动映射为 HTTP 状态码（requires → 401, ensures → 403）。

**解决方案**:

1. **这是设计行为**：契约违反会自动转换为对应的 HTTP 错误码
2. **客户端应正确处理 HTTP 错误码**：
```nexa
flow main {
    response = std.http.post("/api/data", data) otherwise {
        // 处理 401/403 错误
    }
}
```

3. **放宽契约条件**：如果条件过于严格导致频繁 401/403

### 11.3 端口冲突

**症状**:
```
Error: Port 8080 is already in use
```

**原因**: 指定端口已被其他服务占用。

**解决方案**:

1. **使用其他端口**：
```bash
nexa serve script.nx --port 9090
```

2. **查找占用端口的进程**：
```bash
lsof -i :8080
kill <PID>
```

---

## 12. Job 系统问题 (v1.3.3+)

### 12.1 JobError: 任务执行失败 (EB01)

**症状**:
```
JobError: job execution failed: email_job_001
```

**原因**: 后台任务执行过程中出错。

**解决方案**:

1. **检查 Job 定义**：确保 job 声明和逻辑正确
```nexa
job EmailJob {
    agent: EmailAgent
    queue: "email_queue"
    retry: 3
    backoff: 60
}
```

2. **查看 Job 状态**：
```bash
nexa jobs script.nx --status
```

3. **使用 `otherwise` 处理失败**：在 Job 逻辑中加入错误恢复

### 12.2 JobError: 任务超时 (EB02)

**症状**:
```
JobError: job timeout: email_job_001 exceeded 300s
```

**原因**: 任务执行时间超过设定超时。

**解决方案**:

1. **增加超时时间**：
```nexa
job EmailJob {
    agent: EmailAgent
    timeout: 600  // 增加到 10 分钟
}
```

2. **优化 Agent 性能**：减少 prompt 复杂度或使用更快的模型

### 12.3 JobError: 死信任务 (EB03)

**症状**:
```
JobError: dead letter job: email_job_001 failed after 3 retries
```

**原因**: 任务重试次数耗尽后仍失败，进入死信队列。

**解决方案**:

1. **检查死信任务**：
```bash
nexa jobs script.nx --dead-letter
```

2. **重试死信任务**：
```bash
nexa jobs script.nx --retry-dead-letter email_job_001
```

3. **增加重试次数或调整退避策略**：
```nexa
job EmailJob {
    retry: 5        // 增加重试次数
    backoff: 120    // 增加退避时间
}
```

---

## 13. 调试技巧

### 13.1 使用 `nexa build` 查看生成的代码

```bash
# 生成 Python 代码供调试
nexa build script.nx

# 会生成 out_script.py
# 你可以直接运行或检查这个文件
python out_script.py
```

### 13.2 启用详细日志

```bash
# 运行时启用调试模式
nexa run script.nx --debug

# 或设置环境变量
export NEXA_DEBUG=1
nexa run script.nx
```

### 13.3 检查中间结果

在 flow 中使用 `print` 输出中间结果：
```nexa
flow main {
    step1 = Agent1.run(input);
    print("Step 1 result: " + step1);
    
    step2 = Agent2.run(step1);
    print("Step 2 result: " + step2);
}
```

### 13.4 使用 Python SDK 调试

```python
from src.nexa_sdk import NexaRuntime

# 创建运行时
runtime = NexaRuntime(debug=True)

# 运行脚本
result = runtime.run_script("script.nx")

# 检查结果
print(result)
```

### 13.5 检查缓存状态

```bash
# 查看缓存统计
nexa cache stats

# 清除缓存
nexa cache clear
```

---

## 14. 错误代码速查表

| 错误代码 | 含义 | 常见原因 |
|---------|-----|---------|
| `E001` | 解析错误 | 语法错误、括号不匹配 |
| `E002` | 未定义标识符 | Agent/Tool 未定义或拼写错误 |
| `E003` | 类型错误 | 参数类型不匹配 |
| `E004` | 语法错误 | 关键字使用不当 |
| `E005` | 重复声明 | 同名 Agent/Protocol 重复定义 |
| `E101` | Agent 执行失败 | 模型调用失败、prompt 错误 |
| `E102` | Tool 执行失败 | 工具参数错误、超时 |
| `E103` | 管道执行失败 | Agent 管道中断 |
| `E104` | Intent 路由失败 | 无匹配意图 |
| `E201` | ContractViolation (requires) | 前置条件未满足 |
| `E202` | ContractViolation (ensures) | 后置条件未满足 |
| `E203` | ContractViolation (invariant) | 不变式违反 |
| `E301` | TypeViolation (strict) | strict 模式类型违反 |
| `E302` | TypeWarning (warn) | warn 模式类型警告 |
| `E303` | Protocol 类型验证失败 | 字段类型不匹配 |
| `E401` | DatabaseError (连接) | 数据库连接失败 |
| `E402` | DatabaseError (查询) | SQL 语法错误或表不存在 |
| `E403` | DatabaseError (事务) | 事务提交/回滚失败 |
| `E501` | AuthError (认证) | 凭证无效 |
| `E502` | AuthError (JWT) | Token 过期或签名无效 |
| `E503` | AuthError (CSRF) | CSRF token 不匹配 |
| `E504` | AuthError (OAuth) | OAuth 流程配置错误 |
| `E601` | KVError (操作) | KV 存储操作失败 |
| `E602` | KVError (序列化) | 数据序列化/反序列化失败 |
| `E701` | ConcurrencyError (取消) | 任务被取消或超时 |
| `E702` | ConcurrencyError (通道) | Channel 已关闭 |
| `E703` | ConcurrencyError (race) | race 全部失败 |
| `E801` | TemplateError (编译) | 模板语法错误 |
| `E802` | TemplateError (渲染) | 模板渲染失败 |
| `E901` | PatternMatchError (无匹配) | 无匹配分支 |
| `E902` | PatternMatchError (解构) | 解构失败 |
| `EA01` | ADTError (Struct) | 结构体操作失败 |
| `EA02` | ADTError (Enum) | 枚举操作失败 |
| `EA03` | ADTError (Trait) | Trait 方法调用失败 |
| `EB01` | JobError (执行) | 任务执行失败 |
| `EB02` | JobError (超时) | 任务超时 |
| `EB03` | JobError (死信) | 死信任务 |
| `EC01` | HTTPError (路由) | 路由未找到 |
| `EC02` | ContractViolation (HTTP) | HTTP 契约违反 |

---

## 15. 获取帮助

如果以上方案都不能解决你的问题：

1. **查看文档**：[完整示例集合](examples.md) 可能有类似场景
2. **提交 Issue**：在 GitHub 仓库提交 Issue，包含：
   - 完整的错误信息
   - 你的代码（脱敏后）
   - 运行环境信息
3. **社区讨论**：在文档页面底部使用 Giscus 参与讨论

---

<div align="center">
  <p>📖 遇到问题不要慌，查阅本指南或寻求社区帮助！</p>
</div>