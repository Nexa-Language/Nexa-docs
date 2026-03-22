---
comments: true
---

# Nexa 错误索引

本索引收录了 Nexa 编译器和运行时可能产生的所有错误代码、原因分析和解决方案。

---

## 📖 如何使用本索引

1. **按错误码查找**：如果你看到类似 `E001` 的错误码，直接在下方表格中查找
2. **按类别浏览**：错误按编译时错误、运行时错误、工具错误等分类
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
    role: "智能助手",       // 必需
    prompt: "帮助用户解决问题", // 必需
    model: "gpt-4"          // 可选
}
```

---

### E004 - 重复声明

**错误信息**：
```
Error E004: Duplicate declaration 'Analyst'
  --> main.nexa:25:1
   |
25 | agent Analyst {
   | ^^^^^^^^^^^^^ 'Analyst' already declared at line 10
```

**原因**：
- 同一作用域内定义了多个同名 Agent、Tool 或 Protocol

**解决方案**：

```nexa
// ❌ 错误：重复声明
agent Analyst { role: "分析师", prompt: "..." }
agent Analyst { role: "数据分析师", prompt: "..." }  // 重复！

// ✅ 正确：使用不同名称
agent DataAnalyst { role: "数据分析师", prompt: "..." }
agent MarketAnalyst { role: "市场分析师", prompt: "..." }
```

---

### E005 - 无效的模型标识符

**错误信息**：
```
Error E005: Invalid model identifier 'gpt5'
  --> main.nexa:12:12
   |
12 |     model: "gpt5",
   |            ^^^^^ 'gpt5' is not a valid model
```

**原因**：
- 模型名称拼写错误
- 使用了不支持的模型

**解决方案**：

```nexa
// ❌ 错误：无效模型名
agent MyAgent {
    role: "助手",
    prompt: "...",
    model: "gpt5"  // 不存在
}

// ✅ 正确：使用有效模型
agent MyAgent {
    role: "助手",
    prompt: "...",
    model: "gpt-4"  // 或 gpt-4o, claude-3-sonnet 等
}
```

**支持的模型列表**：
- OpenAI: `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-3.5-turbo`
- Anthropic: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- Local: `llama-2`, `mistral`, 等（需配置本地模型）

---

### E006 - Protocol 未找到

**错误信息**：
```
Error E006: Protocol 'ReportFormat' not found
  --> main.nexa:18:30
   |
18 | agent Reporter implements ReportFormat {
   |                              ^^^^^^^^^^^^^ not declared
```

**原因**：
- `implements` 引用的 Protocol 未声明
- Protocol 名称拼写错误

**解决方案**：

```nexa
// ❌ 错误：引用未声明的 Protocol
agent Reporter implements ReportFormat {
    role: "报告员",
    prompt: "..."
}

// ✅ 正确：先声明 Protocol
protocol ReportFormat {
    title: "string",
    content: "string"
}

agent Reporter implements ReportFormat {
    role: "报告员",
    prompt: "..."
}
```

---

### E007 - Tool 未找到

**错误信息**：
```
Error E007: Tool 'web_search' not found
  --> main.nexa:20:20
   |
20 | agent Searcher uses web_search {
   |                    ^^^^^^^^^^ not declared
```

**原因**：
- `uses` 引用的 Tool 未声明
- Tool 名称拼写错误
- 未引入标准库

**解决方案**：

```nexa
// ❌ 错误：引用未声明的 Tool
agent Searcher uses web_search {
    role: "搜索助手",
    prompt: "..."
}

// ✅ 正确方式 1：声明 Tool
tool web_search {
    description: "搜索网页",
    parameters: {"query": "string"}
}

agent Searcher uses web_search {
    role: "搜索助手",
    prompt: "..."
}

// ✅ 正确方式 2：使用标准库
agent Searcher uses std.web_search {
    role: "搜索助手",
    prompt: "..."
}
```

---

### E008 - 语法错误

**错误信息**：
```
Error E008: Syntax error
  --> main.nexa:30:1
   |
30 | agent MyAgent
   | ^^^^^^^^^^^^^ expected '{' after agent name
```

**原因**：
- 缺少必要的语法元素（括号、逗号等）
- 关键字拼写错误
- 缩进或格式问题

**解决方案**：

```nexa
// ❌ 错误：缺少大括号
agent MyAgent
    role: "助手"

// ✅ 正确：完整语法
agent MyAgent {
    role: "助手",
    prompt: "..."
}
```

---

### E009 - 无效的正则表达式

**错误信息**：
```
Error E009: Invalid regex pattern
  --> main.nexa:15:20
   |
15 |     fast_match r"[a-z" against input
   |                 ^^^^^ unterminated character class
```

**原因**：
- `fast_match` 中使用的正则表达式语法错误

**解决方案**：

```nexa
// ❌ 错误：正则表达式不完整
semantic_if "匹配邮箱" fast_match r"[a-z+@" against input {
    ...
}

// ✅ 正确：完整的正则表达式
semantic_if "匹配邮箱" fast_match r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" against input {
    ...
}
```

---

### E010 - 无效的属性值

**错误信息**：
```
Error E010: Invalid property value for 'memory'
  --> main.nexa:12:14
   |
12 |     memory: "permanent",
   |              ^^^^^^^^^^ expected 'short', 'long', or 'session'
```

**原因**：
- 属性值不在允许的选项范围内

**解决方案**：

```nexa
// ❌ 错误：无效的 memory 值
agent MyAgent {
    role: "助手",
    prompt: "...",
    memory: "permanent"  // 无效
}

// ✅ 正确：使用有效值
agent MyAgent {
    role: "助手",
    prompt: "...",
    memory: "long"  // 有效值: short, session, long
}
```

---

## 2. 运行时错误 (E1xx)

运行时错误在程序执行过程中发生，通常与外部资源或配置相关。

### E101 - Agent 执行超时

**错误信息**：
```
Runtime Error E101: Agent execution timeout
  Agent: 'Analyst'
  Timeout: 60 seconds
```

**原因**：
- Agent 执行时间超过限制
- 模型响应缓慢
- 网络连接问题

**解决方案**：

```nexa
// 方案 1：增加超时时间
@timeout(seconds=120)
agent Analyst {
    role: "分析师",
    prompt: "..."
}

// 方案 2：使用更快的模型
agent Analyst {
    role: "分析师",
    prompt: "...",
    model: "gpt-3.5-turbo"  // 比 gpt-4 更快
}

// 方案 3：添加 fallback
agent Analyst {
    role: "分析师",
    prompt: "...",
    fallback: "gpt-3.5-turbo"
}
```

---

### E102 - 模型调用失败

**错误信息**：
```
Runtime Error E102: Model API call failed
  Model: 'gpt-4'
  Status: 429 - Rate limit exceeded
  Message: You have exceeded your API rate limit
```

**原因**：
- API 密钥无效或过期
- API 配额用尽
- 网络连接问题
- 模型服务不可用

**解决方案**：

```bash
# 检查 API 密钥
nexa doctor

# 更新密钥配置
nexa config set api.openai_key "sk-xxx"
```

```nexa
// 添加 fallback 模型
agent MyAgent {
    role: "助手",
    prompt: "...",
    model: "gpt-4",
    fallback: "gpt-3.5-turbo"  // 主模型失败时降级
}
```

---

### E103 - Protocol 验证失败

**错误信息**：
```
Runtime Error E103: Protocol validation failed
  Agent: 'Reporter'
  Protocol: 'Report'
  Missing fields: ['summary']
  Invalid fields: {'score': 'expected number, got string'}
```

**原因**：
- Agent 输出不符合 Protocol 定义的格式
- 字段类型不匹配

**解决方案**：

```nexa
// 检查 Protocol 定义
protocol Report {
    title: "string",
    summary: "string",   // 确保必需字段
    score: "number"      // 确保类型正确
}

// 优化 Agent 的 prompt 以确保输出格式
agent Reporter implements Report {
    role: "报告员",
    prompt: """
    生成结构化报告，必须包含以下字段：
    - title: 报告标题（字符串）
    - summary: 报告摘要（字符串）
    - score: 评分（数字，0-100）
    """
}
```

---

### E104 - 工具执行错误

**错误信息**：
```
Runtime Error E104: Tool execution error
  Tool: 'web_search'
  Error: Connection timeout
```

**原因**：
- 工具依赖的外部服务不可用
- 网络连接问题
- 工具参数错误

**解决方案**：

```nexa
// 添加错误处理
try {
    result = web_search.run(query);
} catch (error) {
    print("搜索失败: " + error);
    result = "无法执行搜索";
}
```

---

### E105 - 认证失败

**错误信息**：
```
Runtime Error E105: Authentication failed
  Service: OpenAI API
  Reason: Invalid API key
```

**原因**：
- API 密钥无效或过期
- 密钥未正确配置

**解决方案**：

```bash
# 检查环境配置
nexa doctor

# 配置密钥
# 方式 1：环境变量
export OPENAI_API_KEY="sk-xxx"

# 方式 2：secrets.nxs 文件
echo 'OPENAI_API_KEY: "sk-xxx"' > secrets.nxs

# 方式 3：配置命令
nexa config set api.openai_key "sk-xxx"
```

---

### E106 - 循环超过最大迭代次数

**错误信息**：
```
Runtime Error E106: Loop exceeded maximum iterations
  Loop: line 45
  Max iterations: 10
```

**原因**：
- `loop until` 循环条件一直未满足
- 逻辑错误导致无限循环

**解决方案**：

```nexa
// ❌ 错误：可能无限循环
loop {
    draft = Editor.run(feedback);
    feedback = Critic.run(draft);
} until ("完美无缺")  // 条件太严格，可能永远无法满足

// ✅ 正确：添加安全退出
max_iterations = 5;
count = 0;
loop {
    draft = Editor.run(feedback);
    feedback = Critic.run(draft);
    count = count + 1;
    if count >= max_iterations {
        print("达到最大迭代次数");
        break;
    }
} until ("文章质量可接受")
```

---

### E107 - 意图匹配失败

**错误信息**：
```
Runtime Error E107: No intent matched
  Input: "帮我订一张机票"
  Available intents: ["查询天气", "设置提醒", "播放音乐"]
```

**原因**：
- `match intent` 没有匹配到任何分支
- 缺少默认分支 `_`

**解决方案**：

```nexa
// ❌ 错误：缺少默认分支
match user_input {
    intent("查询天气") => WeatherBot.run(user_input),
    intent("设置提醒") => ReminderBot.run(user_input)
    // 如果都不匹配会报错
}

// ✅ 正确：添加默认分支
match user_input {
    intent("查询天气") => WeatherBot.run(user_input),
    intent("设置提醒") => ReminderBot.run(user_input),
    _ => DefaultBot.run(user_input)  // 兜底处理
}
```

---

## 3. 配置错误 (E2xx)

配置错误与项目配置、环境设置相关。

### E201 - 配置文件未找到

**错误信息**：
```
Error E201: Configuration file not found
  Path: ./nexa.yaml
```

**原因**：
- 配置文件不存在
- 配置文件路径错误

**解决方案**：

```bash
# 初始化配置文件
nexa config init

# 或指定配置文件路径
nexa run main.nexa --config ./config/nexa.yaml
```

---

### E202 - 无效的配置值

**错误信息**：
```
Error E202: Invalid configuration value
  Key: model.temperature
  Value: "hot"
  Expected: number between 0 and 2
```

**原因**：
- 配置值类型或范围错误

**解决方案**：

```yaml
# ❌ 错误
model:
  temperature: "hot"

# ✅ 正确
model:
  temperature: 0.7  # 0.0 - 2.0
```

---

### E203 - 密钥文件错误

**错误信息**：
```
Error E203: Secrets file error
  File: secrets.nxs
  Reason: File format invalid
```

**原因**：
- `secrets.nxs` 文件格式错误
- 密钥文件权限问题

**解决方案**：

```bash
# 检查文件格式
cat secrets.nxs

# 确保格式正确
echo 'OPENAI_API_KEY: "sk-xxx"' > secrets.nxs
echo 'ANTHROPIC_API_KEY: "sk-ant-xxx"' >> secrets.nxs

# 设置正确的文件权限
chmod 600 secrets.nxs
```

---

## 4. 工具与 MCP 错误 (E3xx)

### E301 - MCP 服务器连接失败

**错误信息**：
```
Error E301: MCP server connection failed
  Server: web-search-mcp
  Reason: Connection refused
```

**原因**：
- MCP 服务器未启动或不可达
- 网络连接问题

**解决方案**：

```bash
# 检查 MCP 服务器状态
nexa mcp test web-search

# 重新添加 MCP 服务器
nexa mcp remove web-search
nexa mcp add web-search "github.com/nexa-ai/web-search-mcp"
```

---

### E302 - 工具参数验证失败

**错误信息**：
```
Error E302: Tool parameter validation failed
  Tool: 'web_search'
  Parameter: 'query'
  Error: Required parameter missing
```

**原因**：
- 调用工具时缺少必需参数
- 参数类型不匹配

**解决方案**：

```nexa
// ❌ 错误：缺少必需参数
result = web_search.run();

// ✅ 正确：提供必需参数
result = web_search.run(query: "Nexa 语言");
```

---

## 5. 警告信息 (W0xx)

警告不会阻止程序运行，但建议修复以避免潜在问题。

### W001 - 未使用的声明

**警告信息**：
```
Warning W001: Unused agent 'TempAgent'
  --> main.nexa:15:1
```

**解决方案**：
- 删除未使用的声明，或
- 在代码中使用该声明

---

### W002 - 性能警告

**警告信息**：
```
Warning W002: Potential performance issue
  Agent 'SlowAgent' has high temperature (1.5) and long prompt
  This may cause inconsistent or slow responses
```

**解决方案**：
- 降低 `temperature` 值
- 简化 prompt
- 使用更快的模型

---

### W003 - 弃用警告

**警告信息**：
```
Warning W003: Deprecated feature
  'semantic_match' is deprecated, use 'semantic_if' instead
```

**解决方案**：
- 更新代码使用新语法

---

## 6. 错误处理最佳实践

### 6.1 使用 try/catch

```nexa
flow main(input: string) {
    try {
        result = RiskyAgent.run(input);
        print(result);
    } catch (error) {
        print("执行失败: " + error);
        result = FallbackAgent.run(input);
    }
}
```

### 6.2 添加 Fallback

```nexa
agent MyAgent {
    role: "助手",
    prompt: "...",
    model: "gpt-4",
    fallback: "gpt-3.5-turbo"  // 主模型失败时自动降级
}
```

### 6.3 设置合理的超时

```nexa
@timeout(seconds=30)
agent QuickAgent {
    role: "快速响应助手",
    prompt: "简洁回答用户问题"
}
```

### 6.4 防止无限循环

```nexa
max_iterations = 5;
count = 0;
loop {
    // ... 循环体
    count = count + 1;
    if count >= max_iterations {
        break;
    }
} until ("条件满足")
```

---

## 🔗 相关资源

- [常见问题与排查](troubleshooting.md)
- [CLI 命令参考](cli_reference.md)
- [语言参考手册](reference.md)