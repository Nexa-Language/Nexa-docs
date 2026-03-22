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

## 🔥 核心优势：认知架构 (Cognitive Architecture)

Nexa 最新版本引入了全新的认知架构功能，重点强化了**类型安全**、**资源治理**以及**人机协同（HITL）**：

### 1. 强类型协议约束 (`protocol` & `implements`)

告别不可控的模型字符串输出！原生支持契约式编程，利用内部 Pydantic 动态编译引擎，让 Agent 的输出严格遵守指定 Schema，并自带语法级别的**自修正重试循环**机制。

```nexa
protocol ReviewResult {
    score: "int",
    summary: "string"
}

// 代理自动继承并遵守上述协议
agent Reviewer implements ReviewResult { 
    prompt: "Review the code..."
}
```

### 2. 多模型动态路由 (`model` & Routing)

解绑厂商依赖。你可以针对每个智能体动态指定运行时的模型端点，构建灵活的跨厂商数据流。

```nexa
// 复杂任务交给推理级模型
agent Coder { model: "deepseek/deepseek-chat", prompt: "..." }

// 轻量任务交给响应极速模型
agent Translator { model: "minimax/minimax-m2.5", prompt: "..." }
```

### 3. 原生管道与高并发结构 (`>>` & DAG 操作符)

如同 Unix 管道一样的爽快体验，或并发控制的自动 Map-Reduce：

```nexa
flow main {
    // 管道串联
    result = input >> Agent1 >> Agent2 >> Agent3;
    
    // 并行分叉 (v0.9.7+)
    results = input |>> [Researcher, Analyst, Writer];
    
    // 合流整合 (v0.9.7+)
    final = [Researcher, Analyst] &>> Reviewer;
    
    // 条件分支 (v0.9.7+)
    handled = urgent_input ?? UrgentHandler : NormalHandler;
}
```

### 4. 语义级控制流 (`match intent` & `loop until`)

用自然语言而非正则表达式来控制程序流程：

```nexa
// 意图路由
match user_input {
    intent("查询天气") => WeatherBot.run(user_input),
    intent("查询新闻") => NewsBot.run(user_input),
    _ => ChatBot.run(user_input)
}

// 语义循环
loop {
    draft = Writer.run(feedback);
    feedback = Critic.run(draft);
} until ("文章质量优秀")
```

### 5. 原生测试框架 (`test` & `assert`)

v0.9 引入的原生测试支持，让智能体开发也能享受 TDD：

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
| 流程编排 | 手动调用 + 状态管理 | `flow` + 管道操作符 |
| 意图路由 | if-else + 正则 | `match intent` 语义匹配 |
| 输出约束 | 手写 JSON Schema | `protocol` 声明式约束 |
| 并发控制 | asyncio + 锁 | DAG 操作符自动调度 |
| 错误重试 | try-except + 循环 | 内置自动重试机制 |

---

## 📚 学习路径

### 新手入门

1. **[快速入门](quickstart.md)** - 30 分钟掌握 Nexa 基础
2. **[基础语法](part1_basic.md)** - 深入了解 Agent 的所有属性
3. **[完整示例](examples.md)** - 查看各种场景的实战代码

### 进阶学习

4. **[高级特性](part2_advanced.md)** - DAG 操作符、并发处理
5. **[语法扩展](part3_extensions.md)** - Protocol 高级用法
6. **[最佳实践](part6_best_practices.md)** - 企业级开发经验

### 深入底层

7. **[编译器设计](part5_compiler.md)** - AST 到字节码的全链路
8. **[架构演进](part5_architecture_evolution.md)** - Rust/WASM 技术蓝图

### 问题排查

- **[常见问题与排查](troubleshooting.md)** - 解决开发中的各种问题

---

## 🌟 开始你的 Nexa 之旅

<div class="portal-actions" style="margin-top: 1rem;">
  <a class="md-button md-button--primary" href="quickstart/">开始快速入门</a>
</div>

准备体验未来的编程范式了吗？
