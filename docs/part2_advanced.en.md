---
comments: true
---

# 3. Advanced Features: Orchestration of Complex Agent Networks

If defining roles with the `agent` keyword is just creating individual gears, then the true "industrial revolution" in the Nexa universe is embodied in its unparalleled **collaborative orchestration network**.

Nexa's core design moat since the v0.5 architecture upgrade has been elevating complex, asynchronous and race-condition-filled multi-stage agent interactions to the level of **language keywords**. In this chapter, we'll explore in detail how to leverage pipelines (`>>`), intent routing (`match intent`), concurrent aggregation (`join`), DAG operators, and the incredible semantic loops (`loop until`) in enterprise-grade Agent frameworks.

---

## 🛤️ Pipeline Operator: `>>` (Pipeline Data Bus)

In most tasks (such as academic translation, code writing and testing chains), multi-agent collaboration is simply a pure pipeline: the output of the previous Agent (Output Task) along with its historical context should be passed completely and without loss as input to the next Agent.

### Pain Points of Traditional Approach

If we use the traditional approach represented by LangChain to build this chain segment:

```python
# Pain points of traditional languages: filled with intermediate variables and implicit state loss
draft = Writer.run(topic)
translated_draft = Translator.run(draft)
reviewer_feedback = Reviewer.run(translated_draft)
```

You'll find that not only do you define a bunch of single-use intermediate variables (leading to poor memory management), but you're also prone to various runtime errors due to different type wrappers (like `BaseMessage` objects vs plain `str`).

### Nexa Pipeline Operator

In Nexa, we can use the expressive Unix-like pipeline operator `>>` in one go:

```nexa
// From Nexa practical code collection (Pipeline Pattern)
flow main {
    res = Coder.run("Generate a fast sorting algorithm in Python") >> Reviewer >> HumanInterface;
    
    // The return result will directly be the final form produced by the pipeline end (HumanInterface)
}
```

### Pipeline Operator Details

| Operation | Equivalent Code | Description |
|-----|---------|------|
| `A >> B` | `B.run(A.run(input))` | Pass A's output to B |
| `A >> B >> C` | `C.run(B.run(A.run(input)))` | Three-stage pipeline |
| `input >> A >> B` | `B.run(A.run(input))` | Start from input |

!!! success "Compiler Magic Behind the Elegance"
    When you type `A >> B`, the Nexa compiler doesn't simply transpile it to linear function blocking calls. Under the hood, Nexa's Orchestrator automatically builds a DAG (Directed Acyclic Graph), which preserves the context sliding window from `Coder` to `Reviewer`, and strictly follows Promise ready state to activate the next node. This saves you countless lines of state maintenance code.

### Pipeline Operator Complete Example

```nexa
// Translation pipeline
agent Translator {
    role: "Professional Translator",
    prompt: "Translate English to Chinese, preserve original meaning, fluent language"
}

agent Proofreader {
    role: "Proofreading Editor",
    prompt: "Proofread translation, correct errors, polish language"
}

agent Formatter {
    role: "Formatting Expert",
    prompt: "Organize text into standard format"
}

flow main {
    english_text = "Artificial intelligence is transforming the world.";
    
    // Three-stage pipeline
    final_result = english_text >> Translator >> Proofreader >> Formatter;
    
    print(final_result);
}
```

**Execution Result**:
```
人工智能正在改变世界。
```

---

## 🔀 Intent Routing: `match intent` Protocol

User instructions are always unpredictable. In many customer service/support bots, some users want to check the weather, some want to send emails, and others just want to hear a joke or chat.

If we use a "super large model" to handle all tasks:

1. It consumes a large amount of billing tokens even when receiving trivial messages.
2. Context is severely polluted, potentially incorrectly triggering system high-risk "delete database" tools when chatting.

Therefore, high-concurrency systems in the industry often advocate "front-end micro routing classifiers" (NLU/Intent Router) to achieve peak shaving and valley filling, then hand over actual processing to domain expert agents mounted behind.

### Basic Syntax

```nexa
match user_input {
    intent("intent description 1") => Agent1.run(user_input),
    intent("intent description 2") => Agent2.run(user_input),
    _ => DefaultAgent.run(user_input)  // Default branch
}
```

### Complete Example

```nexa
// Nexa in action: Multi-intent routing
flow main {
    req = "Tell me what is happening in the global tech world today!";
    
    // Using natural semantics and intent matching mechanism to directly decouple verbose and fragile if-else
    match req {
        intent("Check local weather") => WeatherBot.run(req) >> Translator,
        intent("Check daily news")    => NewsBot.run(req) >> Translator,
        _ => SmallTalkBot.run(req)
    }
}
```

### Intent Routing Flow Diagram

```
User Input
    │
    ▼
┌─────────────────────┐
│  Intent Classifier  │
│    (Built-in)       │
│ Embedding + Similarity │
└─────────────────────┘
    │
    ├── intent("weather") ──────► WeatherBot
    │
    ├── intent("news") ──────► NewsBot
    │
    └── default (_) ────────────► SmallTalkBot
```

!!! info "Parsing `intent()` Underlying Implementation"
    Here `intent("...")` is essentially not simple string or regex matching. Nexa internally carries an ultra-lightweight Embeddings matching model specifically for intent classification. In the background, it rapidly calculates cosine similarity with each branch's `Condition`, seamlessly routing execution flow into the most appropriate branch. To implement a similar mechanism in Python, you would need at least a ChromaDB service and a complex Top-K retrieval pool.

### Intent Routing Best Practices

1. **Be specific with intent descriptions**: Avoid vague descriptions
2. **Set reasonable default branch**: Handle unknown intents
3. **Consider using fast models**: Intent classification doesn't require complex reasoning

```nexa
// ✅ Good intent descriptions
intent("Check weather forecast or current weather conditions")
intent("Check stock prices or financial data")
intent("Book flights, hotels, or restaurants")

// ❌ Bad intent descriptions
intent("weather")  // Too vague
intent("other")    // No practical meaning
```

---

## 🕸️ DAG Topology Orchestration: Ultimate Multi-way Fork and Merge (v0.9.7+)

When dealing with intelligence-intensive tasks (such as investment research report generation or core system difficult code optimization), it's necessary to have multiple roles conduct "back-to-back" independent research separately, then aggregate for cross-discussion. Nexa v0.9.7 revolutionarily introduced native handling of complex graph structures (DAG) topology operators.

### DAG Operator Overview

| Operator | Name | Description | Example |
|-------|------|------|------|
| `>>` | Pipeline | Sequential passing | `A >> B` |
| `|>>` | Fan-out | Parallel send to multiple Agents | `input |>> [A, B, C]` |
| `&>>` | Merge/Fan-in | Merge multiple results to one Agent | `[A, B] &>> C` |
| `??` | Conditional Branch | Select path based on condition | `input ?? A : B` |
| `||` | Async Fork | Send without waiting for result | `input || [A, B]` |
| `&&` | Consensus Merge | Require all Agents to agree | `[A, B] && Judge` |

### Fork Operator `|>>` (Fan-out)

**Parallel clone** upstream data and send to multiple Agents, waiting for all results to return.

```nexa
// Fork operator - Parallel send to multiple Agents
flow main {
    topic = "Quantum Computing Applications";
    
    // Send topic to three Agents in parallel simultaneously
    results = topic |>> [Researcher, Analyst, Writer];
    
    // results is an array containing outputs from all three Agents
    print(results);
}
```

**Flow Diagram**:
```
       topic
         │
         ├──────────┬──────────┐
         │          │          │
         ▼          ▼          ▼
    Researcher   Analyst    Writer
         │          │          │
         └──────────┴──────────┘
                    │
                    ▼
               [Result Array]
```

**Use Cases**:
- Multi-angle analysis of the same problem
- Multi-language translation
- Multi-model comparison verification

### Merge Operator `&>>` (Merge/Fan-in)

**Merge** outputs from multiple Agents and send to downstream Agent.

```nexa
// Merge operator - Combine outputs from multiple Agents
flow main {
    // Wait for Researcher and Analyst to complete
    // Merge both outputs and send to Reviewer
    final_report = [Researcher, Analyst] &>> Reviewer;
    
    print(final_report);
}
```

**Flow Diagram**:
```
    Researcher ────┐
                   │
                   ▼
               Reviewer ──► Final Output
                   ▲
                   │
    Analyst ───────┘
```

**Use Cases**:
- Multi-source information aggregation
- Expert consultation
- Cross-validation

### Conditional Branch Operator `??`

**Automatically select** execution path based on input characteristics.

```nexa
// Conditional branch operator
flow main {
    user_query = "URGENT: System outage detected";
    
    // Automatically select processing Agent based on input content
    handled = user_query ?? UrgentHandler : NormalHandler;
    
    print(handled);
}
```

**Flow Diagram**:
```
         Input
          │
          ▼
    ┌─────────────┐
    │  Condition  │
    │  Judgment   │
    └─────────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
UrgentHandler  NormalHandler
    │           │
    └─────┬─────┘
          │
          ▼
        Output
```

**Use Cases**:
- Urgency classification
- Simple/complex task routing
- Different request type handling

### Fire-and-Forget Operator `||`

**Parallel execute** multiple Agents, **without waiting for results**. Suitable for notifications, logging and other "fire-and-forget" scenarios.

```nexa
// Fire-and-Forget operator
flow main {
    notification = "System maintenance scheduled at 2AM";
    
    // Parallel send notifications, not waiting for response
    notification || [EmailBot, SlackBot, SMSBot];
    
    // Main flow continues, not blocked
    print("Notifications sent, continuing with other tasks...");
}
```

**Flow Diagram**:
```
         Input
           │
           ▼
    ┌──────┴──────┐
    │             │
    ▼             ▼
 EmailBot     SlackBot
    │             │
    ▼             ▼
 (Background)  (Background)
```

**Use Cases**:
- Batch notification sending
- Log recording
- Non-critical task triggering

### Consensus Operator `&&`

**Parallel execute** multiple Agents, **wait for all results** and perform voting/consensus decision.

```nexa
// Consensus operator - Multi-expert voting decision
flow main {
    question = "Should we approve this loan application?";
    
    // Three experts parallel evaluate, wait for all results
    decision = question && [RiskAnalyst, CreditChecker, ComplianceOfficer];
    
    // decision contains all experts' opinions, can vote or comprehensive analysis
    print(decision);
}
```

**Flow Diagram**:
```
              Input
                │
        ┌───────┼───────┐
        │       │       │
        ▼       ▼       ▼
    ExpertA  ExpertB  ExpertC
        │       │       │
        └───────┼───────┘
                │
                ▼
          Consensus Decision
```

**Use Cases**:
- Multi-expert review
- Voting decision systems
- Cross-validation

### DAG Operator Complete Comparison Table

| Operator | Name | Behavior | Use Case |
| |-------|------|------|---------|
| `>>` | Pipeline | Sequential passing | Unidirectional pipeline |
| `|>>` | Fan-out | Parallel send to multiple Agents | Parallel processing |
| `&>>` | Merge/Fan-in | Wait for multiple results then merge | Result integration |
| `??` | Conditional Branch | Select path based on condition | Intelligent routing |
| `||` | Fire-forget | Parallel execute without waiting | Async notification |
| `&&` | Consensus | Parallel execute wait for all results | Voting decision |

### Combining DAG Operators

Build complex processing flows:

```nexa
// From Nexa code example 15_dag_topology.nx
flow main {
    topic = "Quantum Computing business impact";

    // 1. Fork: topic is fed to Tech and Biz researchers for parallel analysis
    // 2. Merge: After both produce output, aggregate and send to Summarizer to write final report
    final_report = topic |>> [Researcher_Tech, Researcher_Biz] &>> Summarizer;

    // Branch routing: If report is abnormal, use backup bot; otherwise execute logging and dispatch
    final_report ?? RecoveryBot : Logger;
}
```

**Complete Flow Diagram**:
```
                    topic
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Researcher_Tech         Researcher_Biz
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
                  Summarizer
                      │
                      ▼
              final_report
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    RecoveryBot               Logger
    (Exception)            (Normal)
```

### DAG Operator Complete Example

```nexa
// DAG topology example - Research report generation system
agent Researcher_Tech {
    role: "Technical Researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze quantum computing's technical level impact"
}

agent Researcher_Biz {
    role: "Business Researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze quantum computing's business level impact"
}

agent Summarizer {
    role: "Report Writer",
    model: "deepseek/deepseek-chat",
    prompt: "Integrate research results and write comprehensive report"
}

agent UrgentHandler {
    role: "Urgent Handler",
    prompt: "Quickly handle urgent issues"
}

agent NormalHandler {
    role: "Standard Handler",
    prompt: "Process according to standard procedures"
}

flow main {
    // Example 1: Simple pipeline
    simple_result = "What is AI?" >> Researcher_Tech >> Summarizer;
    
    // Example 2: Fork - Parallel processing
    parallel_results = "Quantum Computing" |>> [Researcher_Tech, Researcher_Biz];
    
    // Example 3: Merge - Integrate results
    merged_report = [Researcher_Tech, Researcher_Biz] &>> Summarizer;
    
    // Example 4: Conditional branch
    urgent_query = "URGENT: System crash!";
    handled = urgent_query ?? UrgentHandler : NormalHandler;
    
    // Example 5: Complex combination
    complex_flow = "AI trends 2024" 
        |>> [Researcher_Tech, Researcher_Biz] 
        &>> Summarizer;
}
```

---

## 🔁 Semantic Review and Reflection Loop: `loop ... until`

In many automated programming and long-text collaboration applications, the industry has concluded that a "reflective critic" mechanism must be adopted: i.e., `Model A produces draft -> Model B acts as reviewer to correct errors -> Model A receives error feedback and rewrites`.

How do traditional languages handle this logic? Developers need to hand-write an extremely fragile `while True`, then use a few awkward regex lines `if "SUCCESS" in text: break` praying the large model can precisely output the break word.

Nexa's philosophy is: **Since even computation is done by large models, why can't judgment logic be natively returned to the semantic field?** This gave birth to a **language-level loop engine** for semantic termination conditions.

### Basic Syntax

```nexa
loop {
    // Loop body
} until ("natural language termination condition")
```

### Complete Example

```nexa
flow main {
    // First step: initial production
    poem = Writer.run("Write a beautiful poem about AGI.");
    
    loop {
        // Use pipeline thinking to get critique feedback
        feedback = Critic.run(poem);
        
        // Use feedback as context guidance, rewrite in-place (Mutate)
        poem = Editor.run(poem, feedback);
        
    // Unique in the entire field: natural language judgment break condition
    } until ("The poem effectively rhymes and crucially mentions the technological singularity")
}
```

### Preventing Infinite Loops

Use loop counter protection:

```nexa
flow critic_pipeline(task: string) {
    loop {
        draft = Writer.run(task);
        feedback = Reviewer.run(draft);
        
    // Combine natural language semantic reasoning and programming strong logic interception (dual insurance mechanism)
    } until ("Code has exactly 0 bugs inside feedback" or runtime.meta.loop_count >= 4)
    
    // If hit the iteration limit, can throw manual interception exception
    if (runtime.meta.loop_count >= 4) {
        raise SuspendExecution("Reviewer and Writer entered deadlock. Need Human Check.");
    }
}
```

### Loop Control Variables

Nexa provides the following built-in variables in loops:

| Variable | Description |
|-----|------|
| `runtime.meta.loop_count` | Current loop count |
| `runtime.meta.last_result` | Result from last loop iteration |

---

## 🔧 Semantic Conditional Judgment: `semantic_if`

Besides `loop until`, Nexa also provides `semantic_if` for semantic-level conditional judgment.

### Basic Syntax

```nexa
semantic_if "natural language condition" against input_variable {
    // Execute when condition is true
} else {
    // Execute when condition is false
}
```

### Fast Match Mode

Use `fast_match` for regex pre-filtering to avoid unnecessary LLM calls:

```nexa
semantic_if "contains specific date and location" fast_match r"\d{4}-\d{2}-\d{2}" against user_input {
    schedule_tool.run(user_input);
} else {
    print("Need further clarification");
}
```

!!! tip "How fast_match Works"
    1. First check with regex quickly
    2. If regex matches, enter branch directly (saves tokens)
    3. If regex doesn't match, still call LLM for semantic judgment

### Complete Example

```nexa
flow main {
    user_input = '{"name": "Zhang San", "age": 25}';
    
    // Semantic conditional judgment - Determine if it's JSON
    semantic_if "Input content is valid JSON format" fast_match r"^\s*[\[{]" against user_input {
        result = JSONProcessor.run(user_input);
        print("Processed as JSON: " + result);
    } else {
        result = TextProcessor.run(user_input);
        print("Processed as text: " + result);
    }
}
```

---

## 🧩 Exception Handling: `try/catch`

Nexa v0.9.5 introduced native exception handling mechanism.

### Basic Syntax

```nexa
try {
    // Code that might error
} catch (error) {
    // Error handling
}
```

### Complete Example

```nexa
flow main {
    try {
        result = RiskyAgent.run("dangerous operation");
        print(result);
    } catch (error) {
        print("Error occurred: " + error);
        // Use fallback solution
        result = FallbackAgent.run("safe operation");
    }
}
```

---

## 🔗 Function Pipe Operator `|>` (v1.3.x)

Unlike the Agent pipeline `>>`, `|>` is a **function-level** pipe operator: it passes the left-hand value as the first argument to the right-hand function. This lets you chain standard library tools and custom functions like Unix pipes.

### Basic Syntax

```nexa
// x |> f  equivalent to  f(x)
// x |> f |> g  equivalent to  g(f(x))
```

### Difference from Agent Pipeline `>>`

| Operator | Level | Semantics | Example |
|----------|-------|-----------|---------|
| `>>` | Agent level | `B.run(A.run(input))` | `input >> Translator >> Reviewer` |
| `|>` | Function level | `f(x)` | `data |> json_parse |> json_get` |

### Complete Example

```nexa
flow main {
    raw_text = '{"name": "Nexa", "version": "1.3"}';
    
    // Function pipe: parse JSON → extract field → format
    result = raw_text
        |> std.json.json_parse
        |> std.json.json_get("name");
    
    print(result);  // Output: Nexa
    
    // Combined with string interpolation
    greeting = "Hello, #{result}!";
    print(greeting);  // Output: Hello, Nexa!
}
```

!!! tip "When to Use `|>` vs `>>`"
    - Use `|>` for **data transformation** (JSON parsing, text processing, math calculations)
    - Use `>>` for **Agent chaining** (translate → proofread → format)
    - They can be combined: `input |> preprocess |> format >> Agent1 >> Agent2`

---

## ❓ Null Coalescing Operator `??` (v1.3.x)

`??` is used for conditional branching in DAG operators, but in v1.3.x it also serves as a **null coalescing** operator: when the left side is `None`, `Option::None`, or an empty dict, it returns the right side's default value.

### Basic Syntax

```nexa
// value ?? fallback
// If value is None/Option::None/empty dict, return fallback
// Otherwise return value itself
```

### Complete Example

```nexa
flow main {
    // Key may not exist in KV store
    user_name = kv.get("user_name") ?? "Guest";
    
    // Agent may return Option::None
    result = Analyzer.run(input) ?? "No analysis available";
    
    // Database query may return empty
    record = db.query_one("SELECT * FROM users WHERE id = 1") ?? {"name": "Unknown"};
    
    print(user_name);   // Guest (if key doesn't exist)
    print(result);      // No analysis available (if Agent returns None)
}
```

!!! warning "Note the Dual Semantics of `??`"
    - In DAG context: `input ?? AgentA : AgentB` means conditional branching
    - In expression context: `value ?? fallback` means null coalescing
    - The compiler automatically distinguishes between the two usages based on context

---

## ⏳ Deferred Execution `defer` (v1.3.x)

The `defer` statement postpones expression evaluation until the current scope exits, following **LIFO (Last-In-First-Out)** order. Commonly used for resource cleanup, logging, and transaction rollback.

### Basic Syntax

```nexa
defer expression;
// expression will execute when the current scope exits (LIFO order)
```

### Complete Example

```nexa
flow main {
    db_handle = std.db.sqlite.connect("data.db");
    defer std.db.sqlite.close(db_handle);  // Auto-close connection on exit
    
    kv_handle = std.kv.open(":memory:");
    defer std.kv.flush(kv_handle);  // Auto-flush KV on exit
    
    // Normal business logic
    std.db.sqlite.execute(db_handle, "INSERT INTO users VALUES (1, 'Alice')");
    result = std.db.sqlite.query(db_handle, "SELECT * FROM users");
    
    // Whether normal exit or exception, defer executes in LIFO order:
    // 1. First flush KV
    // 2. Then close DB
}
```

!!! tip "defer Execution Order"
    Multiple `defer` statements execute in **LIFO** order (similar to Go/Rust):
    ```nexa
    defer print("first");   // Executes last
    defer print("second");  // Executes second
    defer print("third");   // Executes first
    // Output order: third → second → first
    ```

---

## 🎯 Pattern Matching (v1.3.x)

Nexa v1.3.x introduces a powerful pattern matching system supporting 7 pattern types, allowing you to elegantly destructure and process complex data structures.

### Basic Syntax

```nexa
match value {
    Pattern1 => expression1,
    Pattern2 => expression2,
    _ => default_expression
}
```

### Supported Pattern Types

| Pattern Type | Syntax | Example |
|-------------|--------|---------|
| Wildcard Pattern | `_` | `_ => "default"` |
| Variable Binding Pattern | `name` | `x => x + 1` |
| Literal Pattern | `value` | `0 => "zero"` |
| Constructor Pattern | `Type::Variant(args)` | `Option::Some(v) => v` |
| Tuple Pattern | `(a, b, ...)` | `(x, y) => x + y` |
| Field Pattern | `{field: pattern}` | `{name: n} => n` |
| Or Pattern | `P1 | P2` | `1 | 2 => "small"` |

### Complete Example

```nexa
flow main {
    // Match Option type
    result = Analyzer.run(input);
    
    match result {
        Option::Some(data) => print("Got data: #{data}"),
        Option::None => print("No data available"),
        _ => print("Unexpected result")
    }
    
    // Match Result type
    response = http_get("https://api.example.com/data");
    
    match response {
        Result::Ok(body) => process(body),
        Result::Err(error) => print("Error: #{error}"),
        _ => print("Unknown response")
    }
    
    // Destructure tuple
    coords = (10, 20);
    match coords {
        (0, 0) => print("Origin"),
        (x, 0) => print("On x-axis at #{x}"),
        (0, y) => print("On y-axis at #{y}"),
        (x, y) => print("At (#{x}, #{y})")
    }
    
    // Destructure struct
    match user_record {
        {name: n, age: a} => print("#{n} is #{a} years old"),
        {name: n} => print("#{n}, age unknown")
    }
}
```

### Let Destructuring

```nexa
// Direct destructuring in let statement
let (x, y) = coords;
let {name: user_name, age: user_age} = user_record;
let Option::Some(value) = result;  // Throws PatternMatchError if None
```

### For Destructuring

```nexa
// Destructuring in for loop
for each (key, value) in kv.list(kv_handle) {
    print("#{key}: #{value}");
}
```

---

## 🏗️ Algebraic Data Types: Struct, Enum, Trait (v1.3.x)

Nexa v1.3.x introduces a complete ADT (Algebraic Data Type) system including structs, enums, and traits, providing a type-safe foundation for Agent data modeling.

### Struct Declaration

```nexa
struct Point {
    x: Int,
    y: Int
}

struct User {
    name: String,
    age: Int,
    email: Option[String]
}
```

### Creating Struct Instances

```nexa
// Using Field Init expression
p = Point { x: 10, y: 20 };
u = User { name: "Alice", age: 30, email: Option::Some("alice@example.com") };
```

### Enum Declaration

```nexa
enum Color {
    Red,
    Green,
    Blue
}

enum Option[T] {
    Some(T),
    None
}

enum Result[T, E] {
    Ok(T),
    Err(E)
}
```

### Creating Enum Variants

```nexa
// Variant Call expression
c = Color::Red;
some_val = Option::Some(42);
none_val = Option::None;
ok_result = Result::Ok("success");
err_result = Result::Err("file not found");
```

### Trait Declaration and Impl

```nexa
// Define Trait
trait Printable {
    fn format() -> String
}

trait Serializable {
    fn to_json() -> String
    fn from_json(data: String) -> Self
}

// Implement Trait for a type
impl Printable for Point {
    fn format() -> String {
        "Point(#{self.x}, #{self.y})"
    }
}

impl Printable for User {
    fn format() -> String {
        "#{self.name} (age: #{self.age})"
    }
}
```

### ADT Combined with Pattern Matching

```nexa
// Struct + pattern matching
match shape {
    Point { x: 0, y: 0 } => "Origin",
    Point { x, y } => "At (#{x}, #{y})"
}

// Enum + pattern matching
match result {
    Result::Ok(data) => process(data),
    Result::Err(msg) => handle_error(msg)
}

// Trait method call
formatted = p.format();  // Call Printable trait's format method
```

!!! info "ADT Runtime Implementation"
    Nexa's ADTs use the **handle-as-dict** pattern at runtime: all struct instances and enum variants are dictionaries under the hood, with `_nexa_type`, `_nexa_variant`, and other prefixed keys. This allows ADTs to seamlessly interact with Agent JSON output.

---

## 📊 Chapter Summary

In this chapter, we learned Nexa's advanced orchestration features:

| Feature | Keyword | Version | Use Case |
|---------|---------|---------|----------|
| Agent Pipeline | `>>` | v0.5+ | Agent chaining |
| Function Pipe | `|>` | v1.3.x | Function chaining |
| Intent Routing | `match intent` | v0.5+ | Request dispatching |
| Fork Operation | `|>>` | v0.9.7+ | Parallel processing |
| Merge Operation | `&>>` | v0.9.7+ | Result integration |
| DAG Conditional Branch | `??` | v0.9.7+ | Path selection |
| Null Coalescing | `??` | v1.3.x | None default value |
| Semantic Loop | `loop until` | v0.5+ | Iterative optimization |
| Semantic Condition | `semantic_if` | v0.5+ | Intelligent judgment |
| Exception Handling | `try/catch` | v0.9.5+ | Error handling |
| Deferred Execution | `defer` | v1.3.x | Resource cleanup |
| Pattern Matching | `match` | v1.3.x | Data destructuring |
| Algebraic Data Types | `struct/enum/trait` | v1.3.x | Type-safe modeling |

These features enable Nexa to elegantly handle the most complex agent orchestration scenarios, from simple pipelines to complex DAG topologies, from deterministic branching to semantic-level conditional judgment, to type-safe data modeling.

---

## 🔗 Related Resources

- [Complete Example Collection](examples.en.md) - View more DAG operator examples
- [Syntax Extensions](part3_extensions.en.md) - Learn Protocol and contract advanced usage
- [Language Reference Manual](reference.en.md) - View complete syntax specification
- [Best Practices](part6_best_practices.en.md) - Enterprise development experience
