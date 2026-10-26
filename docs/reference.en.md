---
title: "Language and API reference"
capabilities: [language, compilation, execution]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Language and API reference

Look up syntax, parameters, return values, and error conditions by object. Start with values and operators, then find Agent settings and Python interfaces.

| Object | Definition | Entry |
| --- | --- | --- |
| `.nx`, flow | Programs and deterministic control flow | [Language basics](part1_basic.md) |
| Agent, `uses`, `@tool` | Model instructions and exposed tools | [Tools and Protocols](part3_extensions.md) |
| Protocol, ADT | Output schemas and local data types | [Protocols](part3_extensions.md), [ADT](part2_adt.md) |
| `>>`, fork/merge | Sequential and parallel topology | [Orchestration](part2_advanced.md) |
| `context` | Context source, sink, and schemas | [Structured context](part2_context_structure.md) |
| Harness | Loops, snapshots, hooks, verification | [Execution primitives](part2_harness.md) |
| Actor | Sequential mailboxes and flow ownership | [Actors](runtime_actors.md) |
| `compile_file` / `compile_source` | Unified compilation | [Compiler](part5_compiler.md) |
| `execute` / `aexecute` | Isolated runs, budgets, cancellation | [Execution](runtime_execution.md) |
| `continue_run` | Next turn after a finished task | [Conversations](runtime_conversations.md) |
| `SQLiteCheckpointStore` | Persistence, approval, unknown outcomes | [Checkpoints](runtime_checkpoints.md) |
| `RunState` | Status, usage, events, and output | [Run states](runtime_execution.md) |
| CLI | Build, inspect, execute, and service commands | [CLI reference](cli_reference.md) |

Nexa programs can call their generated Agent objects directly. Python applications integrate through the runtime interfaces below.


## Files, comments, and values

| Form | Meaning |
| --- | --- |
| `.nx` / `.nxlib` | Program and includable source module |
| `.nxs` | Local model configuration; nearest-directory definitions override ancestors |
| `// text` / `/* text */` | Line/block comments |
| `42` / `2.5` / `true` / `false` | Integer, float, Boolean literals |
| `"text"` / triple-quoted strings | Single-line and multiline text |
| `value = expression;` | Assignment; ordinary assignment semicolons are optional |
| `object.field` / `object["key"]` | Property/key access, subject to the actual value type |

The Python path uses Python integer semantics. See the [backend guide](runtime_rust.md) for Rust support. Split complex calculations into intermediate assignments instead of assuming precedence for unverified operator combinations.

## Operators

| Operator | Purpose | Conditions |
| --- | --- | --- |
| `+ - * / %` | Arithmetic | Compatible operands; `/` is true division |
| `== != > >= < <=` | Comparison | Used in deterministic conditions |
| `and` / `or` | Combine conditions | `if (...)` / `while (...)` |
| `>>` | Sequential Agent pipeline | Downstream accepts output or declared context |
| `|>` | Function pipe | `x |> f` calls `f(x)` |
| `??` | Null coalescing | Fallback for `None`, empty Option, or empty map |
| `fallback` | Alternative after failure | Exercise the specific failure path |
| `?` / `otherwise` | Unwrap, propagate, or recover `NexaResult` | Use an entry returning `NexaResult` |
| `|>>` / `&>>` | DAG fork and merge | Validate topology with complete programs and isolated sessions |
| `||` / `&&` | Legacy DAG compatibility syntax | Verify actual background/consensus behavior rather than inferring it from symbols |

### Function pipe

```nexa
flow double(value: int) -> int { result = value * 2; }
flow main { result = 6 |> double; }
```

Returns `12`. `|>` inserts its left value before function arguments. Agent chains usually use `>>`.

### Null coalescing

```nexa
flow main {
    python! """value = None"""
    result = value ?? "fallback";
}
```

Returns `fallback`. A null value is different from the string `"None"`.

### String interpolation

```nexa
flow main {
    name = "Nexa";
    result = "Hello #{name}";
}
```

Returns `Hello Nexa`. Interpolation supports variables, attributes, and index access; arbitrary Python expressions are outside its interface. Use `std.template` for dynamic templates.

## Types and output schemas

| Type form | Purpose |
| --- | --- |
| `int` / `float` / `str` / `string` / `bool` | Primitive annotations |
| `list[T]` / `dict[K, V]` | Generic collection annotations |
| `T?` / `Option[T]` | Optional values |
| `Result[T, E]` | Success/error value declarations |
| `T \| U` | Union types |
| `type Name = str @ "constraint"` | Semantic type declaration; judgment requires evaluation support |
| `protocol Name { field: type }` | Agent output contract |
| `struct` / `enum` / `trait` / `impl` | Local ADT declarations; see [support boundaries](part2_adt.md) |

Complete typed declaration module:

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

Protocol outputs are validated on completion; missing fields or wrong types fail. Static lint, gradual typing modes, and model JSON/schema validation are separate checks.

## Agent parameters

Defaults below come from the `NexaAgent` constructor. See [budgets](runtime_execution.md) for cumulative per-run `RunConfig` limits.

| Property | Default | Behavior |
| --- | --- | --- |
| `prompt` | Empty string | System instructions |
| `role` | Empty string | Role information appended to instructions |
| `model` | Effective strong-model configuration | Optional provider prefix |
| `provider_api` | Chat; anthropic prefix selects Anthropic | `chat` / `responses` / `anthropic` |
| `max_tokens` | `None` | Per-request provider output-token limit |
| `stream` | `false` | Streaming still requires completion and validation |
| `cache` | `false` | Enables eligible exact caching |
| `max_history_turns` | `None` | Retained conversation-turn limit |
| `timeout` | 30 seconds | Total deadline when RunConfig is not explicit |
| `retry` | 3 | Converted to at most 2 retries in execution config |
| `max_tool_calls` | 10 | Tool-call limit when RunConfig is not explicit |
| `tool_call_strategy` | `auto` | `auto` / `required` / `none`, passed as provider tool choice |
| `output_format` | Empty string | `json` requests JSON output |
| `output_schema` | `None` | Structured-output constraint sharing Protocol validation |
| `memory_scope` | `local` | Legacy `persistent` saves local messages; use checkpoints for recoverable tasks |
| `experience` | `None` | Appends an existing file's content to instructions |
| `context` | Unset | ContextSpec source, sink, schemas, and inheritance |

The `.nx` properties `max_tokens` and `max_history_turns` accept integers. `@limit(max_tokens=...)`, `@timeout(seconds=...)`, and `@retry(max_attempts=...)` override the matching properties. `@temperature` currently has no provider effect. Complete configuration declaration:

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

## Python signatures and results

| API | Result and key constraints |
| --- | --- |
| `compile_file(path, *, harness_mode="warn")` | `Compilation`: `python_code`, `ast`, `sources`, `diagnostics` |
| `compile_source(source, *, source_path=None, harness_mode="warn")` | Same; source_path provides relative include context |
| `NexaAgent.run(*args)` | Direct value, retained instance session; raises on failure |
| `NexaAgent.run_result(*args)` | Success/error `NexaResult` wrapper |
| `NexaAgent.execute(*args, config=None, state=None, cancel=None, save=None, on_event=None, on_text=None, provider=None)` | Isolated/resumed `RunState`; resume rejects new args |
| `NexaAgent.aexecute(*args, **kwargs)` | Async adapter; task cancellation sets cooperative cancellation |
| `NexaAgent.continue_run(previous, *args, config=None, cancel=None, save=None, on_event=None, on_text=None, provider=None)` | New run from settled history; unknown outcomes block it |

`on_event` receives an event dictionary, `on_text` receives streaming text fragments, and `save` receives a serializable `RunState`. Callbacks are part of the application execution path; keep them bounded and handle their own failures explicitly.

---

[Source and validation](capability_inventory.md) · `language` / `compilation` / `execution`
