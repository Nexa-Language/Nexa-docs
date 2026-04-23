---
comments: true
---

# Nexa CLI 命令参考

本文档详细描述 Nexa 命令行工具的所有命令、参数和使用示例。所有命令均与源码 `src/cli.py` 严格匹配。

---

## 📖 概述

Nexa CLI 是 Nexa 语言的命令行接口，提供编译、运行、测试、检查、Lint、意图验证、HTTP 服务、后台任务管理等功能。

### 命令总览

| 命令 | 说明 | 版本 |
|------|------|------|
| `nexa build` | 编译 .nx 文件为 .py | v0.9.7+ |
| `nexa run` | 编译并执行 .nx 文件 | v0.9.7+ |
| `nexa test` | 编译并运行测试 | v0.9.7+ |
| `nexa inspect` | 结构分析 (Agent-Native Tooling) | v1.3.0 |
| `nexa validate` | 语义验证 | v1.3.0 |
| `nexa lint` | 类型系统 Lint (渐进式类型系统) | v1.3.1 |
| `nexa intent check` | IDD 意图检查 | v1.1.0 |
| `nexa intent coverage` | IDD 意图覆盖率 | v1.1.0 |
| `nexa serve` | 启动 HTTP Server | v1.3.4 |
| `nexa routes` | 列出 HTTP 路由 | v1.3.4 |
| `nexa jobs` | 后台任务管理 | v1.3.3 |
| `nexa workers` | Worker 管理 | v1.3.3 |
| `nexa cache clear` | 清理缓存 | v0.9.7+ |

### 安装验证

```bash
# 检查安装版本
nexa --version

# 查看帮助信息
nexa --help
```

!!! tip "版本显示"
    `--version` 参数显示当前安装的 Nexa 版本号。当前特性集覆盖 v1.1–v1.3.x。

---

## 1. 核心命令

### 1.1 `nexa build` - 编译程序

将 Nexa 代码编译为 Python 代码，不执行。

**语法**：

```bash
nexa build <FILE>
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要编译的 .nx 源文件路径 | 必需 |

**示例**：

```bash
# 编译为 Python
nexa build main.nx

# 编译指定文件
nexa build examples/01_hello_world.nx
```

**输出说明**：

```
🔨 Compiling main.nx ...
✨ Success! Built target: main.py
```

编译产物为同目录下的 `.py` 文件（如 `main.nx` → `main.py`）。

!!! note "include 支持"
    `build` 命令支持 `include` 语句，可将其他 .nx 文件的内容合并到当前文件的 AST 顶部。

---

### 1.2 `nexa run` - 运行程序

编译并执行 Nexa 程序。

**语法**：

```bash
nexa run <FILE>
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要运行的 .nx 源文件路径 | 必需 |

**示例**：

```bash
# 基本运行
nexa run main.nx

# 运行示例文件
nexa run examples/01_hello_world.nx
```

**输出说明**：

```
🔨 Compiling main.nx ...
✨ Success! Built target: main.py
🚀 Running main.py ...
==================================================
[INFO] Agent 'Analyst' started
[RESULT] 执行结果...
==================================================
✅ Execution Finished (Exit code: 0)
```

!!! warning "中断执行"
    运行中按 `Ctrl+C` 可中断执行，输出 `⚠️ Execution interrupted by user.` 并以退出码 130 结束。

---

### 1.3 `nexa test` - 运行测试

编译 .nx 文件并执行其中所有 `test_` 前缀的测试函数。

**语法**：

```bash
nexa test <FILE>
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要测试的 .nx 源文件路径 | 必需 |

**示例**：

```bash
# 运行测试
nexa test main.nx
```

**输出说明**：

```
🔨 Compiling main.nx ...
✨ Success! Built target: main.py
🧪 Testing main.nx ...
==================================================
[PASS] test_basic_pipeline
[PASS] test_intent_routing
[FAIL] test_edge_case
      AssertionError: 输出不符合预期
==================================================
💥 1 failed, 2 passed.
```

---

## 2. Agent-Native Tooling 命令 (v1.3.0)

### 2.1 `nexa inspect` - 结构分析

对 .nx 文件进行结构分析，输出 Agent、Tool、Flow 等元素的结构描述。

**语法**：

```bash
nexa inspect <FILE> [--format json|text]
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要分析的 .nx 源文件路径 | 必需 |
| `--format` | 输出格式：`json` 或 `text` | `json` |

**示例**：

```bash
# JSON 格式输出
nexa inspect main.nx --format json

# 文本格式输出
nexa inspect main.nx --format text
```

---

### 2.2 `nexa validate` - 语义验证

对 .nx 文件进行语义验证，检查语法和语义错误。

**语法**：

```bash
nexa validate <FILE> [--json] [--quiet]
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要验证的 .nx 源文件路径 | 必需 |
| `--json` | JSON 格式输出 | `false` |
| `--quiet` | 静默模式，只输出错误 | `false` |

**示例**：

```bash
# 基本验证
nexa validate main.nx

# JSON 格式输出
nexa validate main.nx --json

# 静默模式
nexa validate main.nx --quiet
```

!!! warning "退出码"
    验证失败时退出码为 1，可用于 CI/CD 流程。

---

### 2.3 `nexa lint` - 类型系统 Lint (v1.3.1)

对 .nx 文件运行渐进式类型系统的 Lint 检查。

**语法**：

```bash
nexa lint <FILE> [--strict] [--warn-untyped]
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要 lint 的 .nx 源文件路径 | 必需 |
| `--strict` | 严格模式：缺失类型标注 = lint 错误 | `false` |
| `--warn-untyped` | 警告模式：缺失类型标注发出警告 | `false` |

**示例**：

```bash
# 默认 lint（只检查有类型标注的代码）
nexa lint app.nx

# 严格模式
nexa lint app.nx --strict

# 警告未标注代码
nexa lint app.nx --warn-untyped
```

!!! tip "Lint 模式说明"
    - **默认模式**：只检查有类型标注的代码
    - **`--warn-untyped`**：对缺失类型标注发出警告
    - **`--strict`**：缺失类型标注视为 lint 错误（非零退出码）

    Lint 模式也可通过 `NEXA_LINT_MODE` 环境变量或 `nexa.toml` 配置文件设置。

---

## 3. IDD 意图驱动开发命令 (v1.1.0)

### 3.1 `nexa intent check` - 意图检查

验证代码是否符合 `.nxintent` 文件中定义的意图规范。

**语法**：

```bash
nexa intent check <FILE> [--intent <INTENT_FILE>] [--verbose]
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要检查的 .nx 源文件路径 | 必需 |
| `--intent` | 指定 .nxintent 文件路径 | 自动查找 |
| `--verbose` | 显示详细输出 | `false` |

**示例**：

```bash
# 基本意图检查
nexa intent check main.nx

# 指定意图文件
nexa intent check main.nx --intent intents/main.nxintent

# 详细输出
nexa intent check main.nx --verbose
```

!!! warning "退出码"
    所有意图检查未通过时退出码为 1。

---

### 3.2 `nexa intent coverage` - 意图覆盖率

显示代码的意图覆盖率报告。

**语法**：

```bash
nexa intent coverage <FILE> [--intent <INTENT_FILE>]
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 要检查的 .nx 源文件路径 | 必需 |
| `--intent` | 指定 .nxintent 文件路径 | 自动查找 |

**示例**：

```bash
# 查看覆盖率
nexa intent coverage main.nx

# 指定意图文件
nexa intent coverage main.nx --intent intents/main.nxintent
```

!!! tip "提升覆盖率"
    覆盖率低于 100% 时，系统会提示添加 `@implements` 注解来提升覆盖率。

---

## 4. HTTP Server 命令 (v1.3.4)

### 4.1 `nexa serve` - 启动 HTTP Server

编译 .nx 文件并启动内置 HTTP 服务器。

**语法**：

```bash
nexa serve <FILE> [--port <PORT>]
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 包含 server 声明的 .nx 文件路径 | 必需 |
| `--port` | 指定服务端口 | 文件中声明值 |

**示例**：

```bash
# 启动 HTTP Server
nexa serve web_app.nx

# 指定端口
nexa serve web_app.nx --port 3000
```

!!! note "server DSL"
    .nx 文件中使用 `server` DSL 定义 HTTP 服务器：
    ```nexa
    server 8080 {
        static "/assets" from "./public"
        cors { origins: ["*"], methods: ["GET", "POST"] }
        route GET "/chat" => ChatBot
        route POST "/analyze" => DataExtractor |>> Analyzer
    }
    ```

---

### 4.2 `nexa routes` - 列出路由

解析 .nx 文件并列出所有 HTTP 路由。

**语法**：

```bash
nexa routes <FILE> [--json]
```

**参数**：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `FILE` | 包含 server 声明的 .nx 文件路径 | 必需 |
| `--json` | JSON 格式输出 | `false` |

**示例**：

```bash
# 列出路由
nexa routes web_app.nx

# JSON 格式输出
nexa routes web_app.nx --json
```

---

## 5. 后台任务管理命令 (v1.3.3)

### 5.1 `nexa jobs` - 任务管理

管理后台 Job 系统中的任务。

**子命令**：

| 子命令 | 参数 | 说明 |
|--------|------|------|
| `list` | `[--status <STATUS>]` | 列出所有任务，可按状态过滤 |
| `status` | `<JOB_ID>` | 查看指定任务状态 |
| `cancel` | `<JOB_ID>` | 取消指定任务 |
| `retry` | `<JOB_ID>` | 重试死信任务 |
| `clear` | - | 清理已完成/过期/取消的任务 |

**状态过滤选项**（`--status`）：

`pending`, `running`, `completed`, `failed`, `dead`, `cancelled`, `expired`

**示例**：

```bash
# 列出所有任务
nexa jobs list

# 只列出失败任务
nexa jobs list --status failed

# 查看任务状态
nexa jobs status job_123

# 取消任务
nexa jobs cancel job_123

# 重试死信任务
nexa jobs retry job_456

# 清理已完成任务
nexa jobs clear
```

---

### 5.2 `nexa workers` - Worker 管理

管理后台 Job Worker。

**子命令**：

| 子命令 | 参数 | 说明 |
|--------|------|------|
| `start` | `<FILE>` | 启动 Worker（需先编译含 job 定义的 .nx 文件） |
| `status` | - | 查看 Worker 和队列状态 |

**示例**：

```bash
# 启动 Worker
nexa workers start jobs_app.nx

# 查看 Worker 状态
nexa workers status
```

!!! note "job DSL"
    .nx 文件中使用 `job` DSL 定义后台任务：
    ```nexa
    job SendEmail on "emails" (retry: 2, timeout: 120) {
        perform(user_id) { ... }
        on_failure(error, attempt) { ... }
    }
    ```

---

## 6. 缓存管理命令

### 6.1 `nexa cache clear` - 清理缓存

清理 `.nexa_cache/` 缓存目录。

**语法**：

```bash
nexa cache clear
```

**示例**：

```bash
nexa cache clear
# 输出: ✅ Cache cleared successfully.
```

!!! tip "缓存说明"
    如果缓存目录不存在，输出 `ℹ️ No cache directory found.`

---

## 7. 全局选项

| 选项 | 描述 |
|------|------|
| `--version` / `-v` | 显示版本号并退出 |
| `--help` | 显示帮助信息 |

---

## 8. 环境变量

Nexa CLI 支持以下环境变量：

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `NEXA_TYPE_MODE` | 运行时类型检查模式 (`strict`, `warn`, `forgiving`) | `warn` |
| `NEXA_LINT_MODE` | Lint 类型检查模式 (`default`, `warn`, `strict`) | `default` |
| `NEXA_PORT` | HTTP Server 端口覆盖 | 文件声明值 |
| `PYTHONPATH` | Python 模块搜索路径 | 自动设置 |

!!! tip "类型模式优先级"
    `NEXA_TYPE_MODE` 的优先级：CLI flag > 环境变量 > `nexa.toml` 配置 > 默认值 (`warn`)

---

## 9. 退出码

| 退出码 | 描述 |
|--------|------|
| `0` | 成功 |
| `1` | 一般错误 / 验证失败 / 意图检查失败 |
| `130` | 用户中断 (Ctrl+C) |

---

## 🔗 相关资源

- [语言参考手册](reference.md)
- [标准库 API](stdlib_reference.md)
- [常见问题与排查](troubleshooting.md)
- [快速入门](quickstart.md)