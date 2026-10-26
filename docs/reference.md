---
title: "语言与 API 参考"
capabilities: [language, compilation, execution]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 语言与 API 参考

按对象查找语法、参数、返回值和错误约束。从基础类型与运算符开始，再查 Agent 配置和 Python 接口。

| 对象 | 定义 | 入口 |
| --- | --- | --- |
| `.nx`、flow | 程序与确定性控制流 | [语言基础](part1_basic.md) |
| Agent、`uses`、`@tool` | 模型指令与暴露工具 | [工具与 Protocol](part3_extensions.md) |
| Protocol、ADT | 输出 schema 与本地数据类型 | [Protocol](part3_extensions.md)、[ADT](part2_adt.md) |
| `>>`、fork/merge | 顺序与并行拓扑 | [编排](part2_advanced.md) |
| `context` | 上下文来源、去向、schema | [结构化上下文](part2_context_structure.md) |
| Harness | 循环、快照、hook、验证 | [执行原语](part2_harness.md) |
| Actor | 顺序邮箱与 flow 生命周期 | [Actor](runtime_actors.md) |
| `compile_file` / `compile_source` | 统一编译 | [编译器](part5_compiler.md) |
| `execute` / `aexecute` | 独立运行、预算、取消 | [执行](runtime_execution.md) |
| `continue_run` | 已结束任务的下一轮 | [连续对话](runtime_conversations.md) |
| `SQLiteCheckpointStore` | 持久化、审批、未知结果 | [checkpoint](runtime_checkpoints.md) |
| `RunState` | 运行状态、用量、事件与结果 | [执行状态](runtime_execution.md) |
| CLI | 编译、检查、运行与服务命令 | [CLI 参考](cli_reference.md) |

Nexa 程序可直接调用生成的 Agent 对象；Python 应用通过下方列出的运行接口集成。


## 文件、注释与值

| 写法 | 说明 |
| --- | --- |
| `.nx` / `.nxlib` | 程序与可 include 的源模块 |
| `.nxs` | 本地模型配置，按目录合并，同名配置由最近目录覆盖 |
| `// text` / `/* text */` | 行注释与块注释 |
| `42` / `2.5` / `true` / `false` | 整数、浮点数与布尔值 |
| `"text"` / 三引号字符串 | 单行与多行文本 |
| `value = expression;` | 赋值；普通赋值结尾分号可选 |
| `object.field` / `object["key"]` | 属性或键访问，具体值类型决定有效操作 |

Python 路径采用 Python 整数语义。Rust 支持范围见[后端说明](runtime_rust.md)。复杂计算优先拆成中间赋值，避免对未验证的操作符组合做优先级假设。

## 运算符

| 运算符 | 作用 | 使用条件 |
| --- | --- | --- |
| `+ - * / %` | 算术 | 操作数需要适用类型；`/` 为真除法 |
| `== != > >= < <=` | 比较 | 可放在确定性条件中 |
| `and` / `or` | 条件组合 | `if (...)` / `while (...)` |
| `>>` | Agent 顺序管道 | 向下一 Agent 传递输出或声明的 context |
| `|>` | 普通函数管道 | `x |> f` 调用 `f(x)` |
| `??` | 空值回退 | `None`、Option 空值或空字典触发回退 |
| `fallback` | 失败后的备选表达式 | 对具体失败路径做执行验收 |
| `?` / `otherwise` | `NexaResult` 解包、传播或回退 | 使用返回 `NexaResult` 的入口 |
| `|>>` / `&>>` | DAG 分叉与合流 | 以完整程序和独立会话验证拓扑 |
| `||` / `&&` | 旧 DAG 兼容语法 | 与后台执行/共识的具体行为一起验收，避免只按符号推断 |

### 函数管道

```nexa
flow double(value: int) -> int { result = value * 2; }
flow main { result = 6 |> double; }
```

返回 `12`。`|>` 在函数参数前插入左侧值；Agent 串联通常使用 `>>`。

### 空值回退

```nexa
flow main {
    python! """value = None"""
    result = value ?? "fallback";
}
```

返回 `fallback`。真实空值和字符串 `"None"` 有不同含义。

### 字符串插值

```nexa
flow main {
    name = "Nexa";
    result = "Hello #{name}";
}
```

返回 `Hello Nexa`。插值支持变量、属性和下标访问；任意 Python 表达式不属于插值接口。动态模板使用 `std.template`。

## 类型与输出 schema

| 类型写法 | 用途 |
| --- | --- |
| `int` / `float` / `str` / `string` / `bool` | 基础注解 |
| `list[T]` / `dict[K, V]` | 泛型集合注解 |
| `T?` / `Option[T]` | 可空值声明 |
| `Result[T, E]` | 成功值或错误值声明 |
| `T \| U` | 联合类型 |
| `type Name = str @ "constraint"` | 语义类型声明；语义判定需要对应评估能力 |
| `protocol Name { field: type }` | Agent 输出契约 |
| `struct` / `enum` / `trait` / `impl` | 本地 ADT 声明；参见[支持边界](part2_adt.md) |

完整类型声明模块：

```nexa
protocol Report {
    title: str,
    score: float,
    tags: list[str],
    note: str?
}
agent Reviewer implements Report {
    prompt: "Return a report matching the declared fields."
}
```

Protocol 输出在完成路径验证，缺失字段或类型错误会失败。静态 lint、渐进式类型模式与模型输出的 JSON/schema 校验分开处理。

## Agent 参数

以下默认值来自 `NexaAgent` 构造函数；`RunConfig` 的单轮累计限制见[执行预算](runtime_execution.md)。

| 属性 | 默认值 | 行为 |
| --- | --- | --- |
| `prompt` | 空字符串 | 系统指令 |
| `role` | 空字符串 | 追加到系统指令的角色信息 |
| `model` | 有效配置的 strong 模型 | 可带 provider 前缀 |
| `provider_api` | Chat；anthropic 前缀选择 Anthropic | `chat` / `responses` / `anthropic` |
| `max_tokens` | `None` | 单次 provider 输出 token 上限 |
| `stream` | `false` | 流式输出，仍需要完成事件与校验 |
| `cache` | `false` | 启用符合条件的精确缓存 |
| `max_history_turns` | `None` | 会话历史回合限制 |
| `timeout` | 30 秒 | 未显式配置 RunConfig 时的总时限 |
| `retry` | 3 | 生成执行配置时换算为最多 2 次重试 |
| `max_tool_calls` | 10 | 未显式配置 RunConfig 时的工具调用上限 |
| `tool_call_strategy` | `auto` | `auto` / `required` / `none`，传入 provider 工具选择 |
| `output_format` | 空字符串 | `json` 请求 JSON 输出 |
| `output_schema` | `None` | 结构化输出约束，与 Protocol 路径共用校验 |
| `memory_scope` | `local` | 旧 `persistent` 模式保存本地消息；可恢复任务使用 checkpoint |
| `experience` | `None` | 将存在的文件内容追加到系统指令 |
| `context` | 未设置 | ContextSpec 的来源、去向、schema 与继承字段 |

`.nx` 的 `max_tokens` 和 `max_history_turns` 属性接受整数。`@limit(max_tokens=...)`、`@timeout(seconds=...)`、`@retry(max_attempts=...)` 优先于同名属性。`@temperature` 当前尚未影响 provider 请求。完整配置声明：

```nexa
agent Analyst {
    prompt: "Use evidence and state assumptions."
    role: "Analyst"
    provider_api: "chat"
    timeout: 120
    retry: 2
    max_tool_calls: 4
    max_tokens: 2000
    max_history_turns: 6
    stream: true
    cache: false
    tool_call_strategy: "auto"
}
```

## Python 调用签名与结果

| 接口 | 返回与主要约束 |
| --- | --- |
| `compile_file(path, *, harness_mode="warn")` | `Compilation`：`python_code`、`ast`、`sources`、`diagnostics` |
| `compile_source(source, *, source_path=None, harness_mode="warn")` | 同上；传 source_path 保留相对 include 基准 |
| `NexaAgent.run(*args)` | 直接值；保留实例会话；失败抛异常 |
| `NexaAgent.run_result(*args)` | `NexaResult` 成功或错误包装 |
| `NexaAgent.execute(*args, config=None, state=None, cancel=None, save=None, on_event=None, on_text=None, provider=None)` | 独立或恢复的 `RunState`；resume 禁止新 args |
| `NexaAgent.aexecute(*args, **kwargs)` | 异步适配；任务取消设置协作取消信号 |
| `NexaAgent.continue_run(previous, *args, config=None, cancel=None, save=None, on_event=None, on_text=None, provider=None)` | 从已结算历史建立新运行；未知结果阻止继续 |

`on_event` 接收事件字典，`on_text` 接收流式文本片段，`save` 接收可持久化 `RunState`。回调属于应用执行路径，应保持有界并显式处理自身失败。

---

[来源与验证](capability_inventory.md) · `language` / `compilation` / `execution`
