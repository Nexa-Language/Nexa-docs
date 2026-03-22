---
comments: true
---

# Nexa CLI 命令参考

本文档详细描述 Nexa 命令行工具的所有命令、参数和使用示例。

---

## 📖 概述

Nexa CLI 是 Nexa 语言的命令行接口，提供编译、运行、测试和调试等功能。

### 安装验证

```bash
# 检查安装版本
nexa --version

# 查看帮助信息
nexa --help
```

---

## 1. 核心命令

### 1.1 `nexa run` - 运行程序

执行 Nexa 程序的主要命令。

**语法**：

```bash
nexa run [OPTIONS] <FILE>
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--file` | `-f` | 要运行的 Nexa 文件 | 必需 |
| `--model` | `-m` | 覆盖默认模型 | 配置文件值 |
| `--verbose` | `-v` | 显示详细输出 | `false` |
| `--debug` | `-d` | 启用调试模式 | `false` |
| `--output` | `-o` | 输出目录 | `./out` |
| `--config` | `-c` | 配置文件路径 | `./nexa.yaml` |
| `--dry-run` | | 只编译不执行 | `false` |
| `--env` | `-e` | 环境变量 (KEY=VALUE) | - |

**示例**：

```bash
# 基本运行
nexa run main.nexa

# 指定模型
nexa run main.nexa --model gpt-4

# 调试模式
nexa run main.nexa --debug --verbose

# 设置环境变量
nexa run main.nexa -e API_KEY=sk-xxx -e DEBUG=true

# 只编译不执行
nexa run main.nexa --dry-run

# 指定输出目录
nexa run main.nexa --output ./build
```

**输出说明**：

```
[INFO] Compiling main.nexa...
[INFO] Generated: ./out/main.py
[INFO] Executing...
[INFO] Agent 'Analyst' started
[INFO] Tool 'web_search' called with query: "..."
[RESULT] 执行结果...
```

---

### 1.2 `nexa compile` - 编译程序

将 Nexa 代码编译为 Python 代码，不执行。

**语法**：

```bash
nexa compile [OPTIONS] <FILE>
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--file` | `-f` | 要编译的 Nexa 文件 | 必需 |
| `--output` | `-o` | 输出目录 | `./out` |
| `--optimize` | `-O` | 优化级别 (0-2) | `1` |
| `--target` | `-t` | 目标格式 (`python`, `ast`, `bytecode`) | `python` |

**示例**：

```bash
# 编译为 Python
nexa compile main.nexa

# 指定输出目录
nexa compile main.nexa -o ./dist

# 输出 AST（抽象语法树）
nexa compile main.nexa --target ast

# 输出字节码（AVM）
nexa compile main.nexa --target bytecode

# 最高优化级别
nexa compile main.nexa --optimize 2
```

**编译产物**：

```
out/
├── main.py           # 生成的 Python 代码
├── main.ast.json     # AST 结构（--target ast）
└── main.bytecode     # AVM 字节码（--target bytecode）
```

---

### 1.3 `nexa test` - 运行测试

执行 Nexa 测试声明。

**语法**：

```bash
nexa test [OPTIONS] [FILE_PATTERN]
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--pattern` | `-p` | 测试名称模式 | `*` |
| `--verbose` | `-v` | 显示详细输出 | `false` |
| `--report` | `-r` | 测试报告格式 (`text`, `json`, `html`) | `text` |
| `--fail-fast` | | 首次失败后停止 | `false` |
| `--coverage` | | 生成覆盖率报告 | `false` |

**示例**：

```bash
# 运行所有测试
nexa test

# 运行特定文件的测试
nexa test tests/main_test.nexa

# 运行匹配模式的测试
nexa test --pattern "financial_*"

# 详细输出 + JSON 报告
nexa test --verbose --report json

# 生成覆盖率报告
nexa test --coverage --report html
```

**测试输出示例**：

```
Running tests...

✓ test_basic_pipeline (0.45s)
✓ test_intent_routing (1.23s)
✓ test_protocol_validation (0.89s)
✗ test_edge_case (0.12s) - Assertion failed: "输出不符合预期"

Summary: 3 passed, 1 failed
Total time: 2.69s
```

---

### 1.4 `nexa check` - 语法检查

静态检查 Nexa 代码的语法和类型。

**语法**：

```bash
nexa check [OPTIONS] <FILE>
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--strict` | | 启用严格模式 | `false` |
| `--format` | `-f` | 输出格式 (`text`, `json`) | `text` |

**示例**：

```bash
# 基本检查
nexa check main.nexa

# 严格模式
nexa check main.nexa --strict

# JSON 格式输出
nexa check main.nexa --format json
```

**检查输出示例**：

```
Checking main.nexa...

Warning: Line 15 - Unused agent 'TempAgent'
Error: Line 23 - Undefined protocol 'ReportFormat'
  --> main.nexa:23:5
   |
23 | agent Reporter implements ReportFormat {
   |                          ^^^^^^^^^^^^ not found
   |

Found 1 error, 1 warning
```

---

## 2. 项目管理命令

### 2.1 `nexa init` - 初始化项目

创建新的 Nexa 项目结构。

**语法**：

```bash
nexa init [OPTIONS] [PROJECT_NAME]
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--template` | `-t` | 项目模板 (`basic`, `web`, `cli`, `api`) | `basic` |
| `--path` | `-p` | 项目路径 | 当前目录 |

**示例**：

```bash
# 在当前目录初始化
nexa init

# 创建命名项目
nexa init my-agent-app

# 使用模板
nexa init my-web-bot --template web

# 指定路径
nexa init my-project --path ~/projects/
```

**生成的项目结构**：

```
my-agent-app/
├── main.nexa          # 主入口文件
├── agents/            # Agent 定义目录
│   └── example.nexa
├── tools/             # 工具定义目录
│   └── helper.nexa
├── tests/             # 测试目录
│   └── main_test.nexa
├── config/
│   └── nexa.yaml      # 配置文件
└── secrets.nxs        # 密钥文件（需配置）
```

---

### 2.2 `nexa config` - 配置管理

查看和管理 Nexa 配置。

**语法**：

```bash
nexa config [COMMAND] [OPTIONS]
```

**子命令**：

| 命令 | 描述 |
|------|------|
| `list` | 列出所有配置 |
| `get <KEY>` | 获取配置值 |
| `set <KEY> <VALUE>` | 设置配置值 |
| `init` | 初始化配置文件 |

**示例**：

```bash
# 列出所有配置
nexa config list

# 获取特定配置
nexa config get model.default

# 设置配置
nexa config set model.default gpt-4
nexa config set debug.verbose true

# 初始化配置文件
nexa config init
```

**配置文件示例** (`nexa.yaml`)：

```yaml
# Nexa 配置文件
model:
  default: gpt-4
  fallback: gpt-3.5-turbo
  
runtime:
  timeout: 300
  max_retries: 3
  
cache:
  enabled: true
  ttl: 3600
  
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
secrets:
  file: secrets.nxs
```

---

### 2.3 `nexa doctor` - 环境诊断

检查运行环境和依赖。

**语法**：

```bash
nexa doctor
```

**输出示例**：

```
Nexa Environment Diagnostic

✓ Nexa version: 1.0.0-alpha
✓ Python version: 3.11.5
✓ Python path: /usr/bin/python3
✓ Dependencies installed
✓ Configuration valid

Model Connectivity:
✓ OpenAI API: Connected
✓ Anthropic API: Connected
✗ Local LLM: Not configured

Warnings:
! OpenAI API key expires in 7 days
! Cache directory is large (2.3GB)

Environment Status: HEALTHY (with warnings)
```

---

## 3. 交互模式命令

### 3.1 `nexa repl` - 交互式 REPL

启动交互式 Nexa 解释器。

**语法**：

```bash
nexa repl [OPTIONS]
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--model` | `-m` | 默认模型 | 配置值 |
| `--history` | | 历史记录文件 | `~/.nexa/history` |

**REPL 命令**：

| 命令 | 描述 |
|------|------|
| `.help` | 显示帮助 |
| `.load <file>` | 加载文件 |
| `.run <agent>` | 运行指定 Agent |
| `.clear` | 清除会话 |
| `.exit` | 退出 REPL |

**示例会话**：

```bash
$ nexa repl

Nexa REPL v1.0.0-alpha
Type .help for commands

>>> agent Greeter {
...     role: "友好问候者",
...     prompt: "向用户友好地问候"
... }
Created agent: Greeter

>>> Greeter.run("你好")
Hello! 很高兴见到你！有什么我可以帮助的吗？

>>> .load examples/chat.nexa
Loaded 3 agents, 2 tools

>>> .exit
Goodbye!
```

---

### 3.2 `nexa chat` - 对话模式

直接与 Agent 进行对话交互。

**语法**：

```bash
nexa chat [OPTIONS] [AGENT_NAME]
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--model` | `-m` | 指定模型 | 配置值 |
| `--system` | `-s` | 系统提示词 | - |
| `--stream` | | 启用流式输出 | `true` |

**示例**：

```bash
# 启动默认对话
nexa chat

# 指定 Agent
nexa chat Assistant

# 指定模型和提示词
nexa chat --model claude-3 --system "你是一个专业的编程助手"

# 禁用流式输出
nexa chat --no-stream
```

---

## 4. 工具与包管理

### 4.1 `nexa tool` - 工具管理

管理自定义工具。

**子命令**：

| 命令 | 描述 |
|------|------|
| `list` | 列出可用工具 |
| `add <name>` | 添加新工具 |
| `remove <name>` | 移除工具 |
| `validate <file>` | 验证工具定义 |

**示例**：

```bash
# 列出工具
nexa tool list

# 添加工具
nexa tool add my_custom_tool

# 验证工具定义
nexa tool validate tools/api.nexa
```

---

### 4.2 `nexa mcp` - MCP 管理

管理 MCP (Model Context Protocol) 服务器。

**子命令**：

| 命令 | 描述 |
|------|------|
| `list` | 列出已配置的 MCP 服务器 |
| `add <name> <url>` | 添加 MCP 服务器 |
| `remove <name>` | 移除 MCP 服务器 |
| `test <name>` | 测试 MCP 连接 |

**示例**：

```bash
# 列出 MCP 服务器
nexa mcp list

# 添加 MCP 服务器
nexa mcp add web-search "github.com/nexa-ai/web-search-mcp"

# 测试连接
nexa mcp test web-search

# 移除服务器
nexa mcp remove web-search
```

---

## 5. 调试与诊断命令

### 5.1 `nexa debug` - 调试模式

启用详细调试输出运行程序。

**语法**：

```bash
nexa debug [OPTIONS] <FILE>
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--breakpoint` | `-b` | 设置断点（行号） | - |
| `--trace` | | 启用执行追踪 | `false` |
| `--profile` | | 启用性能分析 | `false` |

**示例**：

```bash
# 调试模式运行
nexa debug main.nexa

# 设置断点
nexa debug main.nexa --breakpoint 25

# 执行追踪
nexa debug main.nexa --trace

# 性能分析
nexa debug main.nexa --profile --output ./profile
```

**调试输出示例**：

```
[DEBUG] Loading main.nexa...
[DEBUG] Parsing AST (12ms)
[DEBUG] Type checking (5ms)
[DEBUG] Compiling to Python (23ms)

[TRACE] main() started
[TRACE] → Agent 'Analyst' called with input: "..."
[TRACE]   → Tool 'web_search' called
[TRACE]   ← Tool returned (1.2s)
[TRACE] ← Agent returned (2.5s)
[TRACE] main() completed

Profile Summary:
- Agent calls: 3
- Tool calls: 5
- Total time: 4.2s
- Token usage: 2,450
```

---

### 5.2 `nexa inspect` - 代码检查

检查 Agent、Tool 和 Protocol 的结构。

**语法**：

```bash
nexa inspect [OPTIONS] <FILE> [ELEMENT]
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--format` | `-f` | 输出格式 (`text`, `json`, `tree`) | `text` |

**示例**：

```bash
# 检查文件中的所有元素
nexa inspect main.nexa

# 检查特定 Agent
nexa inspect main.nexa Analyst

# 树形结构输出
nexa inspect main.nexa --format tree

# JSON 格式输出（便于程序解析）
nexa inspect main.nexa --format json
```

**输出示例**：

```
Agent: Analyst
├── Role: Financial Analyst
├── Model: gpt-4
├── Memory: session
├── Tools:
│   ├── web_search
│   └── calculator
├── Protocol: Report
│   ├── title: string
│   ├── summary: string
│   └── score: number
└── Modifiers:
    ├── @limit(max_tokens=2048)
    └── @timeout(seconds=60)
```

---

## 6. 输出与日志命令

### 6.1 `nexa logs` - 日志查看

查看运行日志。

**语法**：

```bash
nexa logs [OPTIONS]
```

**参数**：

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--follow` | `-f` | 实时跟踪日志 | `false` |
| `--lines` | `-n` | 显示行数 | `100` |
| `--level` | `-l` | 日志级别 (`DEBUG`, `INFO`, `WARN`, `ERROR`) | `INFO` |
| `--since` | | 时间范围 (`1h`, `1d`, `1w`) | - |

**示例**：

```bash
# 查看最近日志
nexa logs

# 实时跟踪
nexa logs --follow

# 查看最近 500 行
nexa logs --lines 500

# 只看错误日志
nexa logs --level ERROR

# 查看最近一小时的日志
nexa logs --since 1h
```

---

## 7. 全局选项

以下选项适用于所有命令：

| 选项 | 简写 | 描述 |
|------|------|------|
| `--help` | `-h` | 显示帮助信息 |
| `--version` | `-V` | 显示版本号 |
| `--quiet` | `-q` | 静默模式，只输出错误 |
| `--verbose` | `-v` | 详细输出 |
| `--color` | | 控制颜色输出 (`auto`, `always`, `never`) |
| `--config` | `-c` | 指定配置文件路径 |

**示例**：

```bash
# 静默运行
nexa run main.nexa --quiet

# 详细输出
nexa run main.nexa -vvv

# 禁用颜色输出
nexa run main.nexa --color never

# 指定配置文件
nexa run main.nexa --config ./custom/nexa.yaml
```

---

## 8. 环境变量

Nexa CLI 支持以下环境变量：

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `NEXA_CONFIG` | 配置文件路径 | `./nexa.yaml` |
| `NEXA_MODEL` | 默认模型 | 配置值 |
| `NEXA_API_KEY` | API 密钥 | - |
| `NEXA_LOG_LEVEL` | 日志级别 | `INFO` |
| `NEXA_CACHE_DIR` | 缓存目录 | `~/.nexa/cache` |
| `NEXA_OUTPUT_DIR` | 输出目录 | `./out` |

**示例**：

```bash
# 设置环境变量
export NEXA_MODEL=gpt-4
export NEXA_LOG_LEVEL=DEBUG
nexa run main.nexa
```

---

## 9. 退出码

| 退出码 | 描述 |
|--------|------|
| `0` | 成功 |
| `1` | 一般错误 |
| `2` | 配置错误 |
| `3` | 编译错误 |
| `4` | 运行时错误 |
| `5` | 测试失败 |
| `6` | 网络错误 |
| `7` | 认证错误 |

---

## 🔗 相关资源

- [语言参考手册](reference.md)
- [常见问题与排查](troubleshooting.md)
- [快速入门](quickstart.md)