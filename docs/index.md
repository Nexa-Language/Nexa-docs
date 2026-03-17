---
comments: true
hide:
  - toc
---

<div class="portal-hero" style="margin-top: 2rem;">
  <p class="portal-kicker">Agent-Native · Concurrent DAG · LLM</p>
  <h1>开启智能体原生 (Agent-Native) 编程新纪元</h1>
  <p class="portal-lead">
    在这里，我们将彻底告别冗长的胶水代码、复杂的 Prompt 拼接与脆弱的 JSON 解析。Nexa 将意图路由、多智能体协作、管道流传输提权为核心语法，让你能用最优雅的姿态构建最硬核的 LLM 并发图。
  </p>
  <div class="portal-actions">
    <a class="md-button md-button--primary" href="preface/">阅读前言与理念</a>
    <a class="md-button" href="part1_basic/">基础语法入门</a>
    <a class="md-button" href="part5_compiler/">探索编译器设计</a>
  </div>
</div>

---

## 🔥 Nexa 的核心优势：Cognitive Architecture

Nexa 最新版本引入了全新的认知架构（Cognitive Architecture）功能，重点强化了**类型安全**、**资源治理**以及**人机协同（HITL）**：

### 1. 强类型协议约束 (`protocol` & `implements`)
告别不可控的模型字符串输出！原生支持契约式编程，利用内部 Pydantic 动态编译引擎，让 Agent 的输出严格遵守指定 Schema，并自带语法级别的**自修正重试循环**机制。

```nexa
protocol ReviewResult {
    score: "int"
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
agent Translator { model: "minimax/m2.5", prompt: "..." }
```

### 3. 原生管道与高并发结构 (`>>` & `join`)
如同 Unix 管道一样的爽快体验，或并发控制的自动 Map-Reduce：

```nexa
flow main {
    // 数据无缝串联与并发流转
    res = info >> join(Analyst_A, Analyst_B) >> Merger;
}
```

---

## 🎯 设计哲学：写流程，而非胶水

阅读本文档的开发者，想必已经受够了在传统语言中通过繁杂的 HTTP 请求和嵌套 `if-else` 来处理模型幻觉的折磨。

Nexa 把“语言模型预测”视为一个**原生计算节拍**，将“不确定性”隔离在语法边界内。准备体验未来的编程范式了吗？请从上方入口启程！
