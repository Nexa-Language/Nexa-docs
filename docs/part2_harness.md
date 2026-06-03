---
comments: true
---

# v2.0 Harness 六元组：运行时原语完整指南

Nexa v2.0 的核心创新是将 **Harness 六元组 H=(E,T,C,S,L,V)** 从编译期验证下沉为运行时一等公民。本章详细介绍每个维度的语法、语义和最佳实践。

---

## 📋 Harness 六元组总览

| 维度 | 原语 | 运行时组件 | 说明 |
|------|------|-----------|------|
| **E** (Execution) | `autoloop`, `try_agent` | HarnessKernel + AutoLoopConfig | 自主执行循环 |
| **T** (Tool) | `@tool` | ToolRegistry + ToolSchema | 零成本工具绑定 |
| **C** (Context) | `with_context`, `context_policy` | ContextManager | 上下文作用域管理 |
| **S** (State) | `snapshot`, `restore`, `fork` | StateStore | 状态快照与回溯 |
| **L** (Lifecycle) | `before_step`, `after_step`, `reflect` | LifecycleHookManager | 生命周期钩子 |
| **V** (Verify) | `verify ... satisfies` | EvaluationInterface | 多层验证接口 |

---

## 🔄 E 维度：自主执行循环 (Execution)

### `autoloop` — 自主 ReAct 循环

`autoloop` 让 Agent 自主执行 Reason→Act→Observe→Reflect 循环，直到满足退出条件。

#### 语法

```nexa
autoloop max_steps: INT, exit_when: STRING, timeout: INT, step_delay: FLOAT {
    // 循环体：Agent 执行逻辑
}
```

#### 参数详解

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_steps` | int | 50 | 最大循环步数 |
| `exit_when` | string | None | 语义退出条件（LLM 评估） |
| `timeout` | int | None | 超时秒数 |
| `step_delay` | float | 0.0 | 步间延迟（秒） |

#### 示例

```nexa
agent Researcher {
    prompt: "研究给定主题，直到收集到足够信息",
    model: "deepseek/deepseek-chat"
}

flow main {
    autoloop max_steps: 10, exit_when: "信息收集完成", timeout: 300 {
        result = Researcher.run("量子计算应用");
        print("Step completed: " + result);
    }
}
```

#### 运行时行为

1. **HarnessKernel** 初始化 AutoLoopConfig
2. **ExecutionEngine** 执行 ReAct 循环
3. 每步生成 **StepResult**（包含 action, observation, reflection）
4. 检查 `exit_when` 条件（语义匹配）
5. 达到 `max_steps` 或 `timeout` 时退出

#### 退出原因

| exit_reason | 说明 |
|-------------|------|
| `exit_when_met` | 满足退出条件 |
| `max_steps` | 达到最大步数 |
| `timeout` | 超时 |
| `error` | 发生错误（strict 模式） |

---

### `try_agent` / `catch_correction` — AI 专属容错

`try_agent` 捕获 Tool 执行错误，并通过 `catch_correction` 注入反思进行自纠错。

#### 语法

```nexa
try_agent {
    // 可能失败的 Agent/Tool 调用
} catch_correction(e: ErrorType) {
    reflect "错误信息：#{e}，请调整策略重试";
}
```

#### 示例

```nexa
agent Coder {
    prompt: "编写 Python 代码",
    tools: [shell_exec]
}

flow main {
    try_agent {
        result = Coder.run("实现快速排序");
    } catch_correction(e: ToolError) {
        reflect "工具执行失败：#{e}，请简化请求或更换工具";
        // 自动重试
    }
}
```

#### 运行时行为

1. 执行 `try_agent` 块
2. 若抛出异常，触发 `catch_correction`
3. 生成 **correction_reflection** 注入 Agent 上下文
4. Agent 基于反思进行自纠错

---

## 🛠 T 维度：零成本工具绑定 (Tool)

### `@tool` 注解

`@tool` 注解将函数自动注册为 Agent 可调用的工具，零运行时开销。

#### 语法

```nexa
@tool("工具描述")
fn tool_name(param: Type): ReturnType {
    // 工具实现
}

@tool("工具描述", risk_level: "high", requires_approval: true)
fn dangerous_tool(cmd: string): string {
    // 高风险工具
}
```

#### 参数详解

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| 描述 | string | 必填 | 工具功能描述（注入 LLM 上下文） |
| `risk_level` | string | "low" | 风险等级：low/medium/high/critical |
| `requires_approval` | bool | false | 是否需要 HITL 人工审批 |
| `sandbox` | bool | false | 是否在 WASM 沙盒中执行 |
| `category` | string | "general" | 工具分类 |

#### 示例

```nexa
@tool("执行 shell 命令")
fn shell_exec(command: string): string {
    python! """
    import subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr
    """
}

@tool("删除文件", risk_level: "high", requires_approval: true)
fn delete_file(path: string): string {
    python! """
    import os
    os.remove(path)
    return f"Deleted: {path}"
    """
}

agent DevOps uses shell_exec, delete_file {
    prompt: "执行 DevOps 任务"
}
```

#### Schema 自动生成

编译器从函数签名自动生成 JSON Schema：

```python
# 生成的 Schema
{
    "name": "shell_exec",
    "description": "执行 shell 命令",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "A string value"}
        },
        "required": ["command"]
    },
    "risk_level": "low",
    "requires_approval": false
}
```

#### HITL 审批流程

当 `requires_approval: true` 时：

1. Tool 执行前检查 HITLManager
2. 若未批准，暂停执行等待人工确认
3. 批准后继续执行

---

## 📦 C 维度：上下文作用域管理 (Context)

### `with_context` — 上下文窗口管理

`with_context` 创建独立的上下文作用域，自动管理 Token 溢出。

#### 语法

```nexa
with_context max_tokens: INT, strategy: IDENTIFIER, priority_tags: [TAGS] {
    // 作用域内的 Agent 调用
}
```

#### 参数详解

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_tokens` | int | 100000 | 上下文窗口大小限制 |
| `strategy` | string | "sliding_window" | 淘汰策略 |
| `priority_tags` | list | [] | 高优先级标签（不被淘汰） |

#### 三种淘汰策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `sliding_window` | 滑动窗口，淘汰最旧消息 | 简单对话，无需长期记忆 |
| `importance_weighted` | 按重要性加权淘汰 | 需要保留关键信息 |
| `smart_summarization` | 智能摘要压缩 | 长对话，需要压缩历史 |

#### 示例

```nexa
agent Analyst {
    prompt: "分析数据并生成报告"
}

flow main {
    with_context max_tokens: 50000, strategy: importance_weighted {
        // 高优先级消息不会被淘汰
        result = Analyst.run("分析这份大型数据集");
    }
}
```

#### 运行时行为

1. **ContextManager** 创建 ContextScope
2. 每条消息自动估算 Token 数
3. 超出 `max_tokens` 时触发淘汰
4. 大型 Tool 输出卸载到 **ToolOutputStore**，仅保留摘要

---

### `context_policy` — Agent 级上下文策略

在 Agent 定义中声明默认上下文策略。

#### 语法

```nexa
agent MyAgent {
    prompt: "...",
    context_policy: {
        max_tokens: 80000,
        strategy: smart_summarization
    }
}
```

---

## 💾 S 维度：状态快照与回溯 (State)

### `snapshot` / `restore` — O(1) COW 快照

基于 Copy-on-Write 的高效状态快照，支持任意时间点回溯。

#### 语法

```nexa
snap = snapshot();           // 创建快照
restore(snap);               // 恢复到快照
restore(snap) if condition;  // 条件恢复
```

#### 示例

```nexa
agent Explorer {
    prompt: "探索解决方案"
}

flow main {
    state = {"counter": 0, "path": []};
    
    // 创建检查点
    checkpoint = snapshot();
    
    // 尝试探索
    result = Explorer.run("探索路径 A");
    state.counter = state.counter + 1;
    
    // 如果失败，回溯
    if result.failed {
        restore(checkpoint);
        // 尝试另一条路径
        result = Explorer.run("探索路径 B");
    }
}
```

#### 运行时行为

1. **StateStore** 使用浅拷贝创建快照（O(1)）
2. 修改状态时触发 COW（Copy-on-Write）
3. `restore` 恢复到指定快照状态

---

### `fork` / `merge` — 多分支并行探索

创建多个独立分支并行探索，最后合并结果。

#### 语法

```nexa
fork [branch1, branch2, ...] merge STRATEGY;
```

#### 合并策略

| 策略 | 说明 |
|------|------|
| `best_of` | 选择最优分支结果 |
| `vote` | 多数投票决定 |
| `weighted_average` | 加权平均 |

#### 示例

```nexa
agent Solver {
    prompt: "解决问题"
}

flow main {
    // 创建三个分支并行探索
    fork [
        Solver.run("策略 A"),
        Solver.run("策略 B"),
        Solver.run("策略 C")
    ] merge best_of;
}
```

---

## 🔔 L 维度：生命周期钩子 (Lifecycle)

### `before_step` / `after_step` / `on_error`

在 autoloop 循环的每个步骤前后注入自定义逻辑。

#### 语法

```nexa
before_step {
    // 步骤开始前执行
}

after_step {
    // 步骤完成后执行
}

on_error(e: ErrorType) {
    // 错误发生时执行
}
```

#### 示例

```nexa
flow main {
    before_step {
        print("Starting step...");
    }
    
    after_step {
        print("Step completed");
    }
    
    on_error(e: Exception) {
        print("Error occurred: " + e);
    }
    
    autoloop max_steps: 5 {
        result = Agent.run("task");
    }
}
```

---

### `before_tool` / `after_tool` — Tool 级钩子

针对特定 Tool 的调用前后注入逻辑。

#### 语法

```nexa
before_tool(tool_name) {
    // Tool 调用前执行
}

after_tool(tool_name) {
    // Tool 调用后执行
}
```

#### 示例

```nexa
before_tool(shell_exec) {
    print("About to execute shell command");
    // 可以阻止执行：return false;
}

after_tool(shell_exec) {
    print("Shell command completed");
}
```

---

### `reflect` — 反思注入

向 Agent 上下文注入反思信息，引导自纠错。

#### 语法

```nexa
reflect "反思内容";
```

#### 示例

```nexa
try_agent {
    result = Coder.run("complex task");
} catch_correction(e: ToolError) {
    reflect "工具执行失败：#{e}。请考虑：(1) 简化请求 (2) 更换工具 (3) 分步执行";
}
```

---

## ✅ V 维度：多层验证接口 (Verify)

### `verify ... satisfies` — 类型合规验证

验证输出是否满足 Protocol 规范。

#### 语法

```nexa
verify result satisfies ProtocolName;
```

#### 示例

```nexa
protocol ReportFormat {
    title: "string",
    score: "int",
    summary: "string"
}

agent Reporter implements ReportFormat {
    prompt: "生成结构化报告"
}

flow main {
    result = Reporter.run("分析数据");
    verify result satisfies ReportFormat;
    // 若验证失败，自动触发 reflect 进行自纠错
}
```

---

### `verify ... semantic` — 语义验收

使用 LLM 评估输出是否满足语义条件。

#### 语法

```nexa
verify "语义条件" against result;
```

#### 示例

```nexa
flow main {
    result = Writer.run("写一篇关于 AI 的文章");
    verify "文章包含至少 3 个具体例子" against result;
}
```

---

### `verify ... behavioral` — 行为轨迹验证

验证 Agent 执行轨迹是否符合预期行为模式。

#### 示例

```nexa
flow main {
    result = Agent.run("task");
    verify result.trace contains "tool_call:search";
}
```

---

### `verify ... method` — 自定义方法验证

调用自定义验证方法。

#### 语法

```nexa
verify result.validate();
```

---

## 🎯 最佳实践

### 1. autoloop 配置

```nexa
// 推荐：设置合理的退出条件和超时
autoloop max_steps: 20, exit_when: "任务完成", timeout: 600 {
    // ...
}

// 避免：无限制的循环
autoloop max_steps: 1000 {  // ❌ 可能无限循环
    // ...
}
```

### 2. 上下文策略选择

| 场景 | 推荐策略 |
|------|----------|
| 简单问答 | `sliding_window` |
| 复杂分析 | `importance_weighted` |
| 长对话 | `smart_summarization` |

### 3. 状态快照时机

```nexa
// 推荐：在关键决策点创建快照
checkpoint = snapshot();
result = risky_operation();
if result.failed {
    restore(checkpoint);
}

// 避免：频繁创建快照（内存开销）
for each item in large_list {
    snap = snapshot();  // ❌ 内存爆炸
}
```

### 4. 验证链

```nexa
// 推荐：多层验证
verify result satisfies Protocol;
verify "语义条件" against result;
verify result.validate();
```

---

## 📚 相关文档

- [基础语法](part1_basic.md) — Agent、Flow、Protocol 基础
- [高级特性](part2_advanced.md) — 管道、DAG、意图路由
- [Actor Model](part2_actor.md) — 多 Agent 并发编排
- [语言参考](reference.md) — 完整语法规范
