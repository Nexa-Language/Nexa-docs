---
comments: true
---

<div class="portal-hero" style="margin-top: 2rem;">
  <p class="portal-kicker">Agent-Native · Concurrent DAG · LLM</p>
  <h1>Empowering the New Era of Agent-Native Programming</h1>
  <p class="portal-lead">
    Say goodbye to verbose glue code, complex prompt concatenation, and fragile JSON parsing. Nexa elevates intent routing, multi-agent collaboration, and pipeline streaming into core syntax, enabling you to build hardcore LLM concurrency graphs with ultimate elegance.
  </p>
  <div class="portal-actions">
    <a class="md-button md-button--primary" href="en/quickstart/">🚀 Quickstart</a>
    <a class="md-button" href="en/part1_basic/">📖 Basic Syntax</a>
    <a class="md-button" href="en/examples/">💡 Examples</a>
  </div>
</div>

---

## 🆕 v1.1–v1.3.x Major Updates: 16 Core Features

Since the v1.0-alpha release, Nexa has undergone intensive iteration across 4 priority tiers (P0–P3), adding **16 core features** with **~1500+ tests** in total. Here's an overview by priority tier:

### 🔴 P0: Core Differentiation Features

| Feature | Version | Description |
|---------|---------|-------------|
| **Intent-Driven Development (IDD)** | v1.1.0 | `intent` declarations + `nexa intent-check/coverage` verification, 104 tests |
| **Design by Contract (DbC)** | v1.2.0 | `requires/ensures/invariant` pre/post/invariant conditions, 47 tests |
| **Agent-Native Tooling** | v1.3.0 | `nexa inspect/validate/lint` semantic-level code analysis, 41 tests |

### 🟡 P1: Essential Features

| Feature | Version | Description |
|---------|---------|-------------|
| **Gradual Type System** | v1.3.1 | `Int/String/Option[T]/Result[T,E]` + `NEXA_TYPE_MODE` three-tier mode, 79 tests |
| **Error Propagation (`?` / `otherwise`)** | v1.3.2 | Rust-style `?` propagation + `otherwise` fallback, 82 tests |
| **Background Job System** | v1.3.3 | `job` DSL + priority queue + cron + retry, 73 tests |
| **Built-In HTTP Server** | v1.3.4 | `server` DSL + CORS/CSP + routing + hot reload, 94 tests |
| **Database Integration** | v1.3.5 | SQLite/PostgreSQL + Agent memory queries, 79+5 tests |

### 🟢 P2: Advanced Features

| Feature | Version | Description |
|---------|---------|-------------|
| **Auth & OAuth** | v1.3.6 | API Key + JWT + OAuth 2.0 PKCE, 79+5 tests |
| **Structured Concurrency** | v1.3.6 | `spawn/parallel/race/channel` + 18 APIs, 172 tests |
| **KV Store** | v1.3.6 | SQLite backend + TTL + Agent KV, 81 tests |
| **Template System** | v1.3.6 | `template"""..."""` + 30+ filters + Agent templates, 209 tests |

### 🔵 P3: Language Expressiveness

| Feature | Version | Description |
|---------|---------|-------------|
| **Pipe Operator `|>`** | v1.3.x | `x |> f` left-to-right data flow, 84 tests |
| **Defer Statement** | v1.3.x | LIFO cleanup, similar to Go defer, 84 tests |
| **Null Coalescing `??`** | v1.3.x | `expr ?? fallback` safe fallback, 84 tests |
| **String Interpolation `#{}`** | v1.3.x | `"Hello #{name}"` Ruby-style interpolation, 100 tests |
| **Pattern Matching + Destructuring** | v1.3.x | 7 pattern types + `match/let/for` destructuring, 91 tests |
| **ADT (struct/enum/trait/impl)** | v1.3.x | Algebraic Data Type system, 100 tests |

---

## 🆕 v1.0-alpha Revolutionary Update: The AVM Era

Nexa v1.0-alpha introduces the revolutionary **Agent Virtual Machine (AVM)** — a high-performance, securely isolated agent execution engine written in Rust:

### 🦀 Rust AVM Foundation

Transitioning from Python script transpilation to a standalone compiled Agent Virtual Machine written in Rust:

| Feature | Description |
|---------|-------------|
| **High-Performance Bytecode Interpreter** | Native execution of compiled Nexa bytecode |
| **Complete Compiler Frontend** | Lexer → Parser → AST → Bytecode |
| **110+ Test Coverage** | Full-link testing ensuring stability |

### 🔒 WASM Security Sandbox

Introducing WebAssembly in AVM to provide strong isolation for external `tool` execution:

- **wasmtime Integration** - High-performance WASM runtime
- **Permission Grading** - Four-tier model: None/Standard/Elevated/Full
- **Resource Limits** - Constraints on memory, CPU, and execution time
- **Audit Logs** - Complete operation audit tracking

### ⚡ Smart Scheduler

Dynamic allocation of concurrency resources at the AVM layer based on system load:

- **Priority Queue** - Task scheduling based on Agent priority
- **Load Balancing** - Strategies: RoundRobin, LeastLoaded, Adaptive
- **DAG Topological Sorting** - Automatic dependency resolution and parallelism analysis

### 📄 Vector Virtual Memory Paging

AVM manages memory, automatically performing vectorized swapping of conversation history:

- **LRU/LFU/Hybrid Eviction Policies** - Intelligent page replacement
- **Embedding Similarity Search** - Loading based on semantic relevance
- **Transparent Page Loading** - Seamless memory management

### Performance Comparison

| Metric | Python Transpiler | Rust AVM |
|--------|-------------------|----------|
| Compile Time | ~100ms | ~5ms |
| Startup Time | ~500ms | ~10ms |
| Memory Usage | ~100MB | ~10MB |
| Concurrent Agents | ~100 | ~10000 |

---

## 🚀 v1.0.1 - v1.0.4 Continuous Evolution

Since the v1.0-alpha release, Nexa has been rapidly iterating with powerful language features:

### 🔀 v1.0.1-beta: Traditional Control Flow & Python Escape Hatch

Providing more flexible programming capabilities for Agent development:

| Feature | Description |
|---------|-------------|
| `if/else if/else` | Traditional conditional statements |
| `for each` | Collection iteration loop |
| `while` | Conditional loop |
| `break/continue` | Loop control statements |
| `python! """..."""` | Python code embedding escape hatch |

```nexa
// Traditional control flow example
tasks = ["task1", "task2", "task3"];
for each task in tasks {
    if task == "critical" {
        HighPriorityAgent.run(task);
    } else {
        NormalAgent.run(task);
    }
}

// Python escape hatch example
result = python! """
    import statistics
    data = json.loads(raw_data)
    return statistics.mean(data)
"""
```

### 🎯 v1.0.2-beta: Semantic Types

Revolutionary type system that makes types carry semantic constraints:

```nexa
// Types are not just formats, but include semantic meaning
type Email = string @ "valid email address format"
type PositiveInt = int @ "must be greater than 0"

protocol UserProfile {
    name: UserName,
    email: Email  // Automatically validates email format
}
```

### 🐄 v1.0.3-beta: COW Memory & Work-Stealing

Providing foundational support for advanced reasoning patterns:

| Feature | Description |
|---------|-------------|
| **COW Memory** | O(1) state branching, enabling Tree-of-Thoughts |
| **Work-Stealing Scheduler** | Efficient concurrent scheduling based on Actor model |

```nexa
// Tree-of-Thought exploration
agent Thinker {
    memory: "cow"  // Enable COW memory
}

// Multi-path reasoning
branch1 = Thinker.run(problem) |>> "technical perspective";
branch2 = Thinker.run(problem) |>> "business perspective";
best = branch1 && branch2;  // Consensus merge
```

### 🐍 v1.0.4-beta: Python SDK COW Agent State

Python SDK adds COW Agent state management, enabling cross-language state branching:

```python
# Using COW in Python SDK
from nexa import CowAgent

agent = CowAgent("analyzer")
branch1 = agent.branch()  # O(1) branch creation
branch2 = agent.branch()
```

---

## 🎯 More Core Features

Beyond code simplicity, Nexa provides these powerful language-level features:

### Strong Type Protocol Constraints (`protocol` & `implements`)

No more uncontrollable model string outputs! Native support for contract-based programming:

```nexa
protocol ReviewResult {
    score: "int",
    summary: "string"
}

agent Reviewer implements ReviewResult { 
    prompt: "Review the code..."
}
```

### Design by Contract (`requires` & `ensures`)

v1.2.0 introduces Design by Contract, declaring pre/post conditions in function signatures:

```nexa
flow transfer(amount: int) -> Result
    requires: amount > 0
    requires: "sender has sufficient balance"
    ensures: result.success == true
{
    // Execute transfer logic
}
```

### Gradual Type System

v1.3.1 introduces optional type annotations with `strict/warn/forgiving` three-tier mode:

```nexa
flow calculate(x: int, y: int) -> int {
    return x + y
}

// Option and Result types
let opt: Option[int] = Some(42)
let res: Result[string, Error] = Ok("success")
```

### Error Propagation (`?` & `otherwise`)

v1.3.2 introduces Rust-style error propagation operators:

```nexa
let value = parse(input) ?           // Propagate error
let result = risky_op() otherwise "fallback"  // Provide fallback value
```

### Pattern Matching & ADT

v1.3.x introduces 7 pattern types and an Algebraic Data Type system:

```nexa
// ADT definitions
struct Point { x: Int, y: Int }
enum Option { Some(value), None }
enum Result { Ok(value), Err(error) }

// Pattern matching
match result {
    Option::Some(answer) => answer
    Option::None => "no response"
}

// Destructuring
let (key, value) = entry
```

### Pipe Operators (`|>` & `>>`)

Two pipe operators for function chaining and Agent pipelines respectively:

```nexa
// |> Function pipe: left-to-right data flow
result |> format_output |> print

// >> Agent pipeline: multi-agent pipeline
"topic" >> Writer >> Reviewer >> Editor
```

### Null Coalescing (`??`) & Defer

```nexa
// ?? Safe fallback
config.timeout ?? 30

// defer LIFO cleanup
defer cleanup(db)
defer log("operation complete")
```

### String Interpolation (`#{expr}`)

```nexa
"Hello #{name}, you are #{age} years old!"
"Status: #{result ?? 'pending'}"
```

### Built-In HTTP Server

```nexa
server 8080 {
    static "/assets" from "./public"
    cors { origins: ["*"], methods: ["GET", "POST"] }
    route GET "/chat" => ChatBot
    route POST "/analyze" => DataExtractor |>> Analyzer
}
```

### Semantic Control Flow (`loop until`)

Control loop termination with natural language:

```nexa
loop {
    draft = Writer.run(feedback);
    feedback = Critic.run(draft);
} until ("Article quality is excellent")
```

### Native Test Framework (`test` & `assert`)

```nexa
test "Translation test" {
    result = Translator.run("Hello, World!");
    assert "Contains Chinese translation" against result;
}
```

---

## 🎯 Design Philosophy: Write Flows, Not Glue

Developers reading this documentation have likely endured the torment of handling model hallucinations through complex HTTP requests and nested `if-else` statements in traditional languages.

Nexa treats "language model prediction" as a **native computational beat**, isolating "uncertainty" within syntactic boundaries.

### Comparison with Traditional Frameworks

| Feature | Traditional Python/LangChain | Nexa |
|---------|------------------------------|------|
| Agent Definition | Instantiate class + config dict | Native `agent` keyword |
| Flow Orchestration | Manual calls + state management | `flow` + pipe operators `>>` / `|>` |
| Intent Routing | if-else + regex | `match intent` semantic matching |
| Output Constraints | Hand-written JSON Schema | `protocol` declarative constraints |
| Concurrency Control | asyncio + locks | DAG operators + structured concurrency |
| Error Retry | try-except + loops | Built-in auto-retry + `?` / `otherwise` |
| Type Safety | None / Pydantic post-validation | Gradual type system + Design by Contract |
| Data Modeling | dict / dataclass | `struct` / `enum` / `trait` ADT |
| HTTP Server | Flask/FastAPI external | Built-in `server` DSL |
| Database | Manual ORM integration | Built-in `db` DSL + Agent memory |
| Authentication | Hand-written JWT/OAuth | Built-in `auth` DSL + API Key |
| Caching | Redis manual management | Built-in KV Store + semantic cache |
| Background Jobs | Celery/queue external | Built-in `job` DSL + priority queue |
| Template Rendering | Jinja2 external | Built-in `template"""..."""` DSL |

---

## 📚 Learning Path

### Getting Started

1. **[Quickstart](quickstart.en.md)** - Master Nexa basics in 30 minutes
2. **[Basic Syntax](part1_basic.en.md)** - Deep dive into all Agent properties
3. **[Examples](examples.en.md)** - View real-world code for various scenarios

### Advanced Learning

4. **[Advanced Features](part2_advanced.en.md)** - DAG operators, pipe `|>`, pattern matching, ADT
5. **[Syntax Extensions](part3_extensions.en.md)** - Design by Contract, type system, error propagation
6. **[Best Practices](part6_best_practices.en.md)** - Enterprise development experience

### Deep Dive

7. **[Compiler Design](part5_compiler.en.md)** - Full pipeline from AST to bytecode
8. **[Enterprise Features](part5_enterprise.en.md)** - HTTP Server, Database, Auth, KV, Concurrency
9. **[Architecture Evolution](part5_architecture_evolution.en.md)** - Rust/WASM technology roadmap

### Reference Manual

- **[Language Reference](reference.en.md)** - Complete syntax specification
- **[CLI Reference](cli_reference.en.md)** - All command-line tools
- **[Stdlib API](stdlib_reference.en.md)** - All std namespaces
- **[Error Index](error_index.en.md)** - All error codes and solutions

### Troubleshooting

- **[FAQ & Troubleshooting](troubleshooting.en.md)** - Solve various development issues

---

## 🌟 Start Your Nexa Journey

<div class="portal-actions" style="margin-top: 1rem;">
    <a class="md-button md-button--primary" href="quickstart.en.md">🚀 Quickstart</a>
    <a class="md-button" href="https://github.com/ouyangyipeng/Nexa">📦 GitHub</a>
</div>