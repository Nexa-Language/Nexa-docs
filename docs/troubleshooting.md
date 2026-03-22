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
- [调试技巧](#7-调试技巧)

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

## 7. 调试技巧

### 7.1 使用 `nexa build` 查看生成的代码

```bash
# 生成 Python 代码供调试
nexa build script.nx

# 会生成 out_script.py
# 你可以直接运行或检查这个文件
python out_script.py
```

### 7.2 启用详细日志

```bash
# 运行时启用调试模式
nexa run script.nx --debug

# 或设置环境变量
export NEXA_DEBUG=1
nexa run script.nx
```

### 7.3 检查中间结果

在 flow 中使用 `print` 输出中间结果：
```nexa
flow main {
    step1 = Agent1.run(input);
    print("Step 1 result: " + step1);
    
    step2 = Agent2.run(step1);
    print("Step 2 result: " + step2);
}
```

### 7.4 使用 Python SDK 调试

```python
from src.nexa_sdk import NexaRuntime

# 创建运行时
runtime = NexaRuntime(debug=True)

# 运行脚本
result = runtime.run_script("script.nx")

# 检查结果
print(result)
```

### 7.5 检查缓存状态

```bash
# 查看缓存统计
nexa cache stats

# 清除缓存
nexa cache clear
```

---

## 8. 错误代码速查表

| 错误代码 | 含义 | 常见原因 |
|---------|-----|---------|
| `E001` | 解析错误 | 语法错误、括号不匹配 |
| `E002` | 未定义标识符 | Agent/Tool 未定义或拼写错误 |
| `E003` | 类型错误 | 参数类型不匹配 |
| `E101` | API Key 错误 | 密钥未配置或无效 |
| `E102` | 网络错误 | 连接超时、代理问题 |
| `E103` | Rate Limit | 请求频率超限 |
| `E201` | 工具未找到 | uses 未声明或路径错误 |
| `E202` | 工具执行错误 | 参数错误、超时 |
| `E301` | Protocol 验证失败 | 输出格式不符合定义 |
| `E302` | Protocol 类型错误 | 字段类型不匹配 |

---

## 9. 获取帮助

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