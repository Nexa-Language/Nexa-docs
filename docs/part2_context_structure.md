# Context-as-Structure (v2.2.1)

> **v2.2.1 新特性** — 把 Context 提升为 agent 声明的结构属性。

## 设计动机

面试官观点：**Agent = (Model, Tools, Context) 三元组完全定义**。

在 v2.1 及之前，Nexa 的 `agent` 声明只定义了 `model` 和 `uses`（tools），但 **context 缺失** —— 运行时 `self.messages = []` 硬编码为空，导致 pipeline `A >> B` 只能传字符串，agent 间的上下文无法结构化传递。

v2.2.1 在 agent 声明块里增加 `context { ... }` 子块，让 context 行为像 model/tools 一样**在结构上完全定义**。

## 语法

```nexa
agent Researcher {
    model: "deepseek/deepseek-chat",
    uses: [web_search],
    
    // v2.2.1: Context 声明（结构属性，与 model/tools 同级）
    context {
        source: upstream,                    // "upstream" | "shared:name" | "fresh"
        sink: downstream,                   // "downstream" | "shared:name" | "discard"
        input_schema: ResearchInput,        // Protocol 类型（可选）
        output_schema: ResearchOutput,      // Protocol 类型（可选）
        max_history_turns: 20,
        inherit: [messages, artifacts]       // 从上游继承的字段
    }
    
    prompt: "..."
}
```

### 字段说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `source` | `str` | `"upstream"` | context 来源：`upstream`（从上游继承）、`shared:name`（共享内存）、`fresh`（全新） |
| `sink` | `str` | `"downstream"` | context 去向：`downstream`（传给下游）、`shared:name`、`discard`（丢弃） |
| `input_schema` | `Protocol` | `None` | 声明此 agent 需要的输入 context 类型（编译期检查） |
| `output_schema` | `Protocol` | `None` | 声明此 agent 产出的 context 类型 |
| `max_history_turns` | `int` | `None` | 最大保留对话轮数 |
| `inherit` | `List[str]` | `[]` | 从上游继承的字段：`messages`、`artifacts`、`tool_results` |

## 编译期类型检查（C-004）

Harness Validator 在编译期检查 pipeline `A >> B` 中，A 的 `output_schema` 是否匹配 B 的 `input_schema`。不匹配则编译失败：

```
C-004: Context incompatible in pipeline 'A >> B':
       output_schema='ResearchOutput' is not a subtype of input_schema='WeatherInput'
       Suggestion: Align A.context.output_schema with B.context.input_schema
```

### 示例：不兼容的 pipeline

```nexa
protocol ResearchOutput { summary: "string" }
protocol WrongInput { foo: "string" }

agent A {
    model: "x",
    context { output_schema: ResearchOutput }
    prompt: "a"
}

agent B {
    model: "x",
    context { input_schema: WrongInput }   // ❌ 与 A 的 output_schema 不匹配
    prompt: "b"
}

flow main {
    result = "test" >> A >> B;   // 编译失败：C-004
}
```

### 示例：兼容的 pipeline

```nexa
protocol ResearchOutput { summary: "string", key_points: "string" }
protocol SummaryResult { title: "string", abstract: "string" }

agent Researcher {
    model: "deepseek/deepseek-chat",
    context {
        source: upstream,
        sink: downstream,
        output_schema: ResearchOutput,
        max_history_turns: 10,
        inherit: [messages]
    }
    prompt: "Research the topic."
}

agent Summarizer {
    model: "deepseek/deepseek-chat",
    context {
        source: upstream,
        sink: downstream,
        input_schema: ResearchOutput,    // ✅ 匹配 Researcher 的 output_schema
        output_schema: SummaryResult,
        max_history_turns: 5,
        inherit: [messages, artifacts]
    }
    prompt: "Summarize the research."
}

flow main {
    result = "quantum computing 2024" >> Researcher >> Summarizer;
}
```

## 运行时行为

### AgentContext 数据结构

每个 agent 在 `run()` 结束时会 snapshot 一个 `AgentContext` 对象，包含：

- `messages` — 完整对话历史
- `tool_results` — 工具调用记录
- `artifacts` — 结构化产物
- `output_text` — 最终输出文本
- `output_schema` — 声明的输出 schema 名

### Pipeline handoff

`A >> B` 在 v2.2.1 中默认走 `nexa_context_pipeline`：

1. A 执行，产出 `AgentContext`
2. B 的 `run()` 检测到上游 `AgentContext`，根据 B 声明的 `inherit` 字段选择性继承
3. B 执行后产出自己的 `AgentContext`，传给下游

### 向后兼容

**不加 `context { ... }` 块的 agent 行为完全不变**（保持 v2.1 的字符串传递语义）。`nexa_context_pipeline` 会自动检测：无 `context_spec` 的 agent 走旧路径。

## 与 Harness 六元组的关系

v2.2.1 不是推翻现有设计，而是补全它：

| Harness 维度 | v2.2.1 关系 |
|-------------|------------|
| **C（Context）** | `context { ... }` 块是 C 维度的声明式扩展 |
| **S（State）** | 每次 handoff 自动 snapshot，支持回溯 |
| **V（Verification）** | verify 结果作为 context artifact 流转 |
| **L（Lifecycle）** | handoff 触发 `before_step` / `after_step` 钩子 |

## 完整示例

见 [`examples/v2.2/01_context_handoff.nx`](https://github.com/Nexa-Language/Nexa/blob/main/examples/v2.2/01_context_handoff.nx)。

## 测试

见 [`tests/test_context_handoff.py`](https://github.com/Nexa-Language/Nexa/blob/main/tests/test_context_handoff.py)（18 个测试用例，覆盖 grammar、AST、runtime、validator、codegen、向后兼容）。
