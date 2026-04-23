---
comments: true
---

<div class="portal-hero" style="margin-top: 2rem;">
  <p class="portal-kicker">Agent-Native · Concurrent DAG · LLM</p>
  <h1>开启智能体原生 (Agent-Native) 编程新纪元</h1>
  <p class="portal-lead">
    在这里，我们将彻底告别冗长的胶水代码、复杂的 Prompt 拼接与脆弱的 JSON 解析。Nexa 将意图路由、多智能体协作、管道流传输提权为核心语法，让你能用最优雅的姿态构建最硬核的 LLM 并发图。
  </p>
  <div class="portal-actions">
    <a class="md-button md-button--primary" href="quickstart/">🚀 快速入门</a>
    <a class="md-button" href="part1_basic/">📖 基础语法</a>
    <a class="md-button" href="examples/">💡 完整示例</a>
  </div>
</div>

---

## 🆕 v1.1–v1.3.x 重大更新：16 项核心特性

自 v1.0-alpha 发布以来，Nexa 经历了 4 个优先级层级（P0–P3）的密集迭代，新增 **16 项核心特性**，总计 **~1500+ 测试**覆盖。以下按优先级分层概览：

### 🔴 P0：核心差异化特性

| 特性 | 版本 | 说明 |
|------|------|------|
| **意图驱动开发 (IDD)** | v1.1.0 | `intent` 声明 + `nexa intent-check/coverage` 验证，104 测试 |
| **契约式编程 (DbC)** | v1.2.0 | `requires/ensures/invariant` 前置/后置/不变式条件，47 测试 |
| **Agent-Native 工具链** | v1.3.0 | `nexa inspect/validate/lint` 语义级代码分析，41 测试 |

### 🟡 P1：基础能力特性

| 特性 | 版本 | 说明 |
|------|------|------|
| **渐进式类型系统** | v1.3.1 | `Int/String/Option[T]/Result[T,E]` + `NEXA_TYPE_MODE` 三级模式，79 测试 |
| **错误传播 (`?` / `otherwise`)** | v1.3.2 | Rust 风格 `?` 传播 + `otherwise` 回退，82 测试 |
| **后台 Job 系统** | v1.3.3 | `job` DSL + 优先级队列 + cron + retry，73 测试 |
| **内置 HTTP Server** | v1.3.4 | `server` DSL + CORS/CSP + 路由 + 热重载，94 测试 |
| **Database 集成** | v1.3.5 | SQLite/PostgreSQL + Agent 记忆查询，79+5 测试 |

### 🟢 P2：高级特性

| 特性 | 版本 | 说明 |
|------|------|------|
| **Auth & OAuth** | v1.3.6 | API Key + JWT + OAuth 2.0 PKCE，79+5 测试 |
| **结构化并发** | v1.3.6 | `spawn/parallel/race/channel` + 18 API，172 测试 |
| **KV Store** | v1.3.6 | SQLite 后端 + TTL + Agent KV，81 测试 |
| **Template 系统** | v1.3.6 | `template"""..."""` + 30+ 过滤器 + Agent 模板，209 测试 |

### 🔵 P3：语言表达力

| 特性 | 版本 | 说明 |
|------|------|------|
| **管道操作符 `|>`** | v1.3.x | `x |> f` 左到右数据流，84 测试 |
| **Defer 语句** | v1.3.x | LIFO 清理，类似 Go defer，84 测试 |
| **Null 合并 `??`** | v1.3.x | `expr ?? fallback` 安全回退，84 测试 |
| **字符串插值 `#{}`** | v1.3.x | `"Hello #{name}"` Ruby 风格插值，100 测试 |
| **模式匹配 + 解构** | v1.3.x | 7 种模式类型 + `match/let/for` 解构，91 测试 |
| **ADT (struct/enum/trait/impl)** | v1.3.x | 代数数据类型系统，100 测试 |

---

## 🆕 v1.0-alpha 革命性更新：AVM 时代来临

Nexa v1.0-alpha 引入了革命性的 **Agent Virtual Machine (AVM)** —— 一个用 Rust 编写的高性能、安全隔离的智能体执行引擎：

### 🦀 Rust AVM 底座

从 Python 脚本解释转译模式跨越至基于 Rust 编写的独立编译型 Agent Virtual Machine：

| 特性 | 说明 |
|-----|------|
| **高性能字节码解释器** | 原生执行编译后的 Nexa 字节码 |
| **完整编译器前端** | Lexer → Parser → AST → Bytecode |
| **110+ 测试覆盖** | 全链路测试保证稳定性 |

### 🔒 WASM 安全沙盒

在 AVM 中引入 WebAssembly，对外部 `tool` 执行提供强隔离：

- **wasmtime 集成** - 高性能 WASM 运行时
- **权限分级** - None/Standard/Elevated/Full 四级权限模型
- **资源限制** - 内存、CPU、执行时间限制
- **审计日志** - 完整的操作审计追踪

### ⚡ 智能调度器

在 AVM 层基于系统负载动态分配并发资源：

- **优先级队列** - 基于 Agent 优先级的任务调度
- **负载均衡** - RoundRobin/LeastLoaded/Adaptive 策略
- **DAG 拓扑排序** - 自动依赖解析与并行度分析

### 📄 向量虚存分页

AVM 接管内存，自动执行对话历史的向量化置换：

- **LRU/LFU/Hybrid 淘汰策略** - 智能页面置换
- **嵌入向量相似度搜索** - 语义相关性加载
- **透明页面加载** - 无感知的内存管理

### 性能对比

| 指标 | Python 转译器 | Rust AVM |
|------|--------------|----------|
| 编译时间 | ~100ms | ~5ms |
| 启动时间 | ~500ms | ~10ms |
| 内存占用 | ~100MB | ~10MB |
| 并发 Agents | ~100 | ~10000 |

---

## 🚀 v1.0.1 - v1.0.4 持续进化

自 v1.0-alpha 发布以来，Nexa 持续快速迭代，带来了更多强大的语言特性：

### 🔀 v1.0.1-beta: 传统控制流 & Python 逃生舱

为 Agent 开发提供更灵活的编程能力：

| 特性 | 说明 |
|-----|------|
| `if/else if/else` | 传统条件分支语句 |
| `for each` | 集合迭代循环 |
| `while` | 条件循环语句 |
| `break/continue` | 循环控制语句 |
| `python! """..."""` | Python 代码嵌入逃生舱 |

```nexa
// 传统控制流示例
tasks = ["task1", "task2", "task3"];
for each task in tasks {
    if task == "critical" {
        HighPriorityAgent.run(task);
    } else {
        NormalAgent.run(task);
    }
}

// Python 逃生舱示例
stats = python! """
    import statistics
    data = json.loads(raw_data)
    return statistics.mean(data)
"""
```

### 🎯 v1.0.2-beta: Semantic Types 语义类型

革命性的类型系统，让类型携带语义约束：

```nexa
// 类型不再只是格式约束，还包含语义含义
type Email = string @ "valid email address format"
type PositiveInt = int @ "must be greater than 0"

protocol UserProfile {
    name: UserName,
    email: Email  // 自动验证邮箱格式
}
```

### 🐄 v1.0.3-beta: COW Memory & Work-Stealing

为高级推理模式提供底层支持：

| 特性 | 说明 |
|-----|------|
| **COW Memory** | O(1) 状态分支，支持 Tree-of-Thoughts |
| **Work-Stealing Scheduler** | 基于 Actor 模型的高效并发调度 |

```nexa
// Tree-of-Thoughts 探索
agent Thinker {
    memory: "cow"  // 启用 COW 内存
}

// 多路径推理
branch1 = Thinker.run(problem) |>> "技术视角";
branch2 = Thinker.run(problem) |>> "商业视角";
best = branch1 && branch2;  // 共识合并
```

### 🐍 v1.0.4-beta: Python SDK COW Agent 状态

Python SDK 支持 COW Agent 状态管理，实现跨语言的状态分支：

```python
# Python SDK 中使用 COW Agent
from nexa import CowAgent

agent = CowAgent("analyzer")
branch1 = agent.branch()  # O(1) 创建分支
branch2 = agent.branch()
```

---

## 🎯 更多核心特性

除了代码简洁性，Nexa 还提供以下强大的语言级特性：

### 强类型协议约束 (`protocol` & `implements`)

告别不可控的模型字符串输出！原生支持契约式编程：

```nexa
protocol ReviewResult {
    score: "int",
    summary: "string"
}

agent Reviewer implements ReviewResult { 
    prompt: "Review the code..."
}
```

### 契约式编程 (`requires` & `ensures`)

v1.2.0 引入 Design by Contract，在函数签名中声明前置/后置条件：

```nexa
flow transfer(amount: int) -> Result
    requires: amount > 0
    requires: "sender has sufficient balance"
    ensures: result.success == true
{
    // 执行转账逻辑
}
```

### 渐进式类型系统

v1.3.1 引入可选类型标注，支持 `strict/warn/forgiving` 三级模式：

```nexa
flow calculate(x: int, y: int) -> int {
    return x + y
}

// Option 和 Result 类型
let opt: Option[int] = Some(42)
let res: Result[string, Error] = Ok("success")
```

### 错误传播 (`?` & `otherwise`)

v1.3.2 引入 Rust 风格的错误传播操作符：

```nexa
let value = parse(input) ?           // 传播错误
let result = risky_op() otherwise "fallback"  // 提供回退值
```

### 模式匹配与 ADT

v1.3.x 引入 7 种模式类型和代数数据类型系统：

```nexa
// ADT 定义
struct Point { x: Int, y: Int }
enum Option { Some(value), None }
enum Result { Ok(value), Err(error) }

// 模式匹配
match result {
    Option::Some(answer) => answer
    Option::None => "no response"
}

// 解构
let (key, value) = entry
```

### 管道操作符 (`|>` & `>>`)

两种管道操作符，分别用于函数链式调用和 Agent 流水线：

```nexa
// |> 函数管道：左到右数据流
result |> format_output |> print

// >> Agent 管道：多智能体流水线
"topic" >> Writer >> Reviewer >> Editor
```

### Null 合并 (`??`) 与 Defer

```nexa
// ?? 安全回退
config.timeout ?? 30

// defer LIFO 清理
defer cleanup(db)
defer log("operation complete")
```

### 字符串插值 (`#{expr}`)

```nexa
"Hello #{name}, you are #{age} years old!"
"Status: #{result ?? 'pending'}"
```

### 内置 HTTP Server

```nexa
server 8080 {
    static "/assets" from "./public"
    cors { origins: ["*"], methods: ["GET", "POST"] }
    route GET "/chat" => ChatBot
    route POST "/analyze" => DataExtractor |>> Analyzer
}
```

### 语义级控制流 (`loop until`)

用自然语言控制循环终止：

```nexa
loop {
    draft = Writer.run(feedback);
    feedback = Critic.run(draft);
} until ("文章质量优秀")
```

### 原生测试框架 (`test` & `assert`)

```nexa
test "翻译功能测试" {
    result = Translator.run("Hello, World!");
    assert "包含中文翻译" against result;
}
```

---

## 🎯 设计哲学：写流程，而非胶水

阅读本文档的开发者，想必已经受够了在传统语言中通过繁杂的 HTTP 请求和嵌套 `if-else` 来处理模型幻觉的折磨。

Nexa 把"语言模型预测"视为一个**原生计算节拍**，将"不确定性"隔离在语法边界内。

### 与传统框架对比

| 特性 | 传统 Python/LangChain | Nexa |
|-----|---------------------|------|
| Agent 定义 | 实例化类 + 配置字典 | 原生 `agent` 关键字 |
| 流程编排 | 手动调用 + 状态管理 | `flow` + 管道操作符 `>>` / `|>` |
| 意图路由 | if-else + 正则 | `match intent` 语义匹配 |
| 输出约束 | 手写 JSON Schema | `protocol` 声明式约束 |
| 并发控制 | asyncio + 锁 | DAG 操作符 + 结构化并发 |
| 错误重试 | try-except + 循环 | 内置自动重试 + `?` / `otherwise` |
| 类型安全 | 无 / Pydantic 后验 | 渐进式类型系统 + 契约式编程 |
| 数据建模 | dict / dataclass | `struct` / `enum` / `trait` ADT |
| HTTP 服务 | Flask/FastAPI 外挂 | 内置 `server` DSL |
| 数据库 | 手动 ORM 集成 | 内置 `db` DSL + Agent 记忆 |
| 认证 | 手写 JWT/OAuth | 内置 `auth` DSL + API Key |
| 缓存 | Redis 手动管理 | 内置 KV Store + 语义缓存 |
| 后台任务 | Celery/队列外挂 | 内置 `job` DSL + 优先级队列 |
| 模板渲染 | Jinja2 外挂 | 内置 `template"""..."""` DSL |

---

## 📚 学习路径

### 新手入门

1. **[快速入门](quickstart.md)** - 30 分钟掌握 Nexa 基础
2. **[基础语法](part1_basic.md)** - 深入了解 Agent 的所有属性
3. **[完整示例](examples.md)** - 查看各种场景的实战代码

### 进阶学习

4. **[高级特性](part2_advanced.md)** - DAG 操作符、管道 `|>`、模式匹配、ADT
5. **[语法扩展](part3_extensions.md)** - 契约式编程、类型系统、错误传播
6. **[最佳实践](part6_best_practices.md)** - 企业级开发经验

### 深入底层

7. **[编译器设计](part5_compiler.md)** - AST 到字节码的全链路
8. **[企业级架构](part5_enterprise.md)** - HTTP Server、Database、Auth、KV、并发
9. **[架构演进](part5_architecture_evolution.md)** - Rust/WASM 技术蓝图

### 参考手册

- **[语言参考](reference.md)** - 完整语法规范
- **[CLI 命令参考](cli_reference.md)** - 所有命令行工具
- **[标准库 API](stdlib_reference.md)** - 所有 std 命名空间
- **[错误索引](error_index.md)** - 所有错误代码与解决方案

### 问题排查

- **[常见问题与排查](troubleshooting.md)** - 解决开发中的各种问题

---

## 🌟 开始你的 Nexa 之旅

<div class="portal-actions" style="margin-top: 1rem;">
    <a class="md-button md-button--primary" href="quickstart.md">🚀 快速入门</a>
    <a class="md-button" href="https://github.com/ouyangyipeng/Nexa">📦 GitHub</a>
</div>