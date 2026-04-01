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

## 🔥 核心优势：代码对比展示

Nexa 将复杂的多智能体协作简化为优雅的声明式语法。点击下方按钮体验 Nexa 与传统方案的差异：

---

<span class="example-badge">示例 1</span>
<span class="example-title">Agent 定义与调用</span>

<div class="code-comparison">
<div class="flip-card" id="flip-1">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 传统 Python + LangChain</span>
      <span class="code-lines">12 行代码</span>
    </div>
    <div class="card-content">
```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# 定义 chain
llm = ChatOpenAI(model="gpt-4", temperature=0.7)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的英中翻译助手"),
    ("human", "{input}")
])
chain = prompt | llm | StrOutputParser()

# 调用
result = chain.invoke({"input": "Hello, World!"})
print(result)
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">4 行代码</span>
    </div>
    <div class="card-content">
```nexa
agent Translator {
    role: "英中翻译助手",
    model: "gpt-4"
}

result = Translator.run("Hello, World!")
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-1').classList.toggle('flipped')">
  🔄 点击对比 Nexa 写法
</button>
<div class="comparison-note">
<strong>核心优势：</strong>从 12 行代码缩减到 4 行，无需理解 Chain、PromptTemplate、StrOutputParser 等复杂概念。Agent 定义即配置，调用即执行。<span class="reduction-badge">缩减 67%</span>
</div>
</div>

---

<span class="example-badge">示例 2</span>
<span class="example-title">管道流程编排</span>

<div class="code-comparison">
<div class="flip-card" id="flip-2">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 传统 Python + LangChain</span>
      <span class="code-lines">18 行代码</span>
    </div>
    <div class="card-content">
```python
import asyncio
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

async def pipeline(topic: str):
    # 第一步：写作
    writer_prompt = f"写一篇关于{topic}的文章"
    draft = await llm.ainvoke(writer_prompt)
    
    # 第二步：审核
    reviewer_prompt = f"审核并指出问题：{draft.content}"
    review = await llm.ainvoke(reviewer_prompt)
    
    # 第三步：润色
    editor_prompt = f"根据审核意见润色：{draft.content}"
    final = await llm.ainvoke(editor_prompt)
    
    return final.content

result = asyncio.run(pipeline("人工智能"))
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">5 行代码</span>
    </div>
    <div class="card-content">
```nexa
agent Writer { role: "作家", prompt: "撰写文章" }
agent Reviewer { role: "审核员", prompt: "审核文章" }
agent Editor { role: "编辑", prompt: "润色文章" }

flow main {
    result = "人工智能" >> Writer >> Reviewer >> Editor;
}
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-2').classList.toggle('flipped')">
  🔄 点击对比 Nexa 写法
</button>
<div class="comparison-note">
<strong>核心优势：</strong>管道操作符 <code>>></code> 让数据流一目了然，无需手动传递中间变量、处理异步上下文。编译器自动优化执行顺序。<span class="reduction-badge">缩减 72%</span>
</div>
</div>

---

<span class="example-badge">示例 3</span>
<span class="example-title">意图路由分发</span>

<div class="code-comparison">
<div class="flip-card" id="flip-3">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 传统 Python + re</span>
      <span class="code-lines">17 行代码</span>
    </div>
    <div class="card-content">
```python
import re
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

def route_request(user_input: str):
    # 手写正则匹配 - 脆弱且难维护
    if re.search(r'天气|weather|气温', user_input, re.I):
        prompt = f"回答天气问题：{user_input}"
        return llm.invoke(prompt).content
    elif re.search(r'新闻|news|头条', user_input, re.I):
        prompt = f"回答新闻问题：{user_input}"
        return llm.invoke(prompt).content
    elif re.search(r'翻译|translate', user_input, re.I):
        prompt = f"翻译：{user_input}"
        return llm.invoke(prompt).content
    else:
        return llm.invoke(f"一般对话：{user_input}").content

result = route_request("今天北京天气怎么样？")
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">10 行代码</span>
    </div>
    <div class="card-content">
```nexa
agent WeatherBot { role: "天气助手" }
agent NewsBot { role: "新闻助手" }
agent Translator { role: "翻译助手" }
agent ChatBot { role: "聊天助手" }

flow main {
    result = match user_input {
        intent("查询天气") => WeatherBot.run(user_input),
        intent("查询新闻") => NewsBot.run(user_input),
        intent("翻译内容") => Translator.run(user_input),
        _ => ChatBot.run(user_input)
    };
}
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-3').classList.toggle('flipped')">
  🔄 点击对比 Nexa 写法
</button>
<div class="comparison-note">
<strong>核心优势：</strong><code>intent()</code> 语义匹配替代脆弱的正则表达式，使用嵌入向量进行语义相似度匹配，更智能、更灵活。<span class="reduction-badge">缩减 41%</span>
</div>
</div>

---

<span class="example-badge">示例 4</span>
<span class="example-title">并发 DAG 执行</span>

<div class="code-comparison">
<div class="flip-card" id="flip-4">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 传统 Python + asyncio</span>
      <span class="code-lines">23 行代码</span>
    </div>
    <div class="card-content">
```python
import asyncio
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

async def researcher(task: str, name: str):
    prompt = f"{name}分析：{task}"
    return {name: await llm.ainvoke(prompt)}

async def parallel_research(topic: str):
    # 并行执行 3 个研究员
    tasks = [
        researcher(topic, "技术研究员"),
        researcher(topic, "市场研究员"),
        researcher(topic, "财务研究员")
    ]
    results = await asyncio.gather(*tasks)
    
    # 汇总结果
    combined = "\n".join([str(r) for r in results])
    summary_prompt = f"汇总以下研究报告：\n{combined}"
    final = await llm.ainvoke(summary_prompt)
    
    return final.content

result = asyncio.run(parallel_research("AI 行业前景"))
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">6 行代码</span>
    </div>
    <div class="card-content">
```nexa
agent TechResearcher { role: "技术研究员" }
agent MarketResearcher { role: "市场研究员" }
agent FinanceResearcher { role: "财务研究员" }
agent Summarizer { role: "报告汇总者" }

flow main {
    result = "AI 行业前景" 
        |>> [TechResearcher, MarketResearcher, FinanceResearcher] 
        &>> Summarizer;
}
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-4').classList.toggle('flipped')">
  🔄 点击对比 Nexa 写法
</button>
<div class="comparison-note">
<strong>核心优势：</strong>DAG 操作符 <code>|>></code> (分叉) 和 <code>&>></code> (合流) 一行代码实现并发编排，无需理解 asyncio、gather、协程等概念。<span class="reduction-badge">缩减 74%</span>
</div>
</div>

---

### 📊 代码量对比总结

| 功能场景 | 传统方案 | Nexa | 缩减比例 |
|:--------|:-------:|:----:|:--------:|
| Agent 定义与调用 | 12 行 | 4 行 | **67%** ↓ |
| 管道流程编排 | 18 行 | 5 行 | **72%** ↓ |
| 意图路由分发 | 17 行 | 10 行 | **41%** ↓ |
| 并发 DAG 执行 | 23 行 | 6 行 | **74%** ↓ |
| **平均** | **17.5 行** | **6.25 行** | **63%** ↓ |

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
    <a class="md-button md-button--primary" href="quickstart.md">🚀 快速入门</a>
    <a class="md-button" href="https://github.com/your-org/nexa">📦 GitHub</a>
</div>
