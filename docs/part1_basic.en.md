---
comments: true
---

# 2. Basic Syntax: Defining Your First Cross-Dimensional Team

This chapter introduces the most core and fundamental syntax elements in Nexa. After reading this chapter and mastering these structures, you can confidently abandon most of the heavy and unstable traditional Python agent development frameworks and use declarative, expressive methods to build your first generation of agent teams.

---

## 🏗️ Core Primitive: Defining Large Language Model Agents (`agent` Keyword)

In the philosophy of the Nexa language, all entities that can "think", receive context, and output structured or unstructured text are called `agent`. Since Nexa elevates Agent to the position of a "first-class citizen", you can write it just like defining a Struct or Class.

It is the basic block that carries system prompts, preset model routing, identity roles, and tool configurations. Let's first look at a most basic definition method:

```nexa
// All properties are declared within the curly braces, no external redundant Client instantiation
agent FriendlyBot {
    role: "Casual conversationalist",
    model: "minimax/minimax-m2.5",
    prompt: "You are a very friendly ChatBot for casual conversations."
}
```

---

## 📋 Agent Property Details

### Property Overview Table

| Property | Type | Required | Default | Version | Description |
|-----|------|-----|-------|---------|------|
| `role` | string | No | - | v0.5+ | Agent's role description, as part of the system prompt |
| `prompt` | string | **Yes** | - | v0.5+ | Agent's core task instruction |
| `model` | string | No | Default model | v0.5+ | Specifies the LLM model to use |
| `memory` | string | No | - | v0.5+ | Memory mode: `persistent`, etc. |
| `stream` | boolean | No | false | v0.5+ | Whether to enable streaming output |
| `cache` | boolean | No | false | v0.5+ | Whether to enable intelligent caching |
| `experience` | string | No | - | v0.5+ | Long-term memory file path |
| `fallback` | string/list | No | - | v0.5+ | Backup model configuration |
| `tools` | list | No | [] | v0.5+ | Available tools list |
| `max_tokens` | int | No | - | v0.5+ | Maximum output token count |
| `timeout` | int | No | 30 | v0.5+ | Execution timeout (seconds) |
| `retry` | int | No | 3 | v0.5+ | Number of retry attempts on failure |
| `requires` | clause | No | - | v1.2+ | Precondition contract clause |
| `ensures` | clause | No | - | v1.2+ | Postcondition contract clause |

### Property Detailed Explanation

#### `role` (Role Semantic Field)

Defines the system role (System Persona) of this agent. This is not just a label; when compiled to Python runtime at the底层, it serves as a high-weight top-level injection point for the system prompt, empowering the model's context boundaries.

```nexa
agent FinancialAdvisor {
    role: "Senior financial analyst, focusing on tech stock investment strategies",
    prompt: "Provide professional investment advice based on user needs..."
}
```

!!! tip "Best Practice"
    - Role descriptions should be **specific and professional**, avoiding vague descriptions like "you are an assistant"
    - Can include professional field, years of experience, specialized skills, etc.
    - Good role descriptions can significantly improve the professionalism and consistency of model output

#### `prompt` (Task Execution Description)

This is the core instruction area that drives model action, supporting multi-line plain text literal expressions. Here, you don't need to handle escaping or even complex token concatenation, everything happens naturally.

```nexa
// Single-line prompt
agent Translator {
    prompt: "Translate user input into Chinese"
}

// Multi-line prompt (recommended for complex tasks)
agent CodeReviewer {
    prompt: """
    You are a code review expert. Please review submitted code, focusing on:
    
    1. Code quality and readability
    2. Potential bugs and edge cases
    3. Performance optimization suggestions
    4. Security vulnerabilities
    
    Output format:
    - Issue list (if any)
    - Improvement suggestions
    - Overall evaluation
    """
}
```

!!! warning "Common Mistake"
    Don't write specific output examples in the prompt, this may cause the model to overfit. If you need to constrain the output format, use `protocol`.

#### `model` (Dynamic Intelligence Mapping)

**(A feature with disruptive advantages)** Native model hard-wired link. This allows us to seamlessly switch between different agents' underlying engines as needed.

**Correct Format**: `provider/model-name`

```nexa
// ✅ Correct format
agent Bot {
    model: "openai/gpt-4"
}

agent AnotherBot {
    model: "deepseek/deepseek-chat"
}

agent ThirdBot {
    model: "minimax/minimax-m2.5"
}

// ❌ Wrong format - missing provider prefix
agent WrongBot {
    model: "gpt-4"  // Will error!
}
```

**Supported Provider Prefixes**:

| Prefix | Description | Example Models |
|-----|------|---------|
| `openai/` | OpenAI GPT series | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` |
| `deepseek/` | DeepSeek series | `deepseek-chat`, `deepseek-coder` |
| `minimax/` | MiniMax series | `minimax-m2.5` |
| `anthropic/` | Anthropic Claude series | `claude-3-sonnet`, `claude-3-opus` |

!!! tip "Model Selection Recommendations"
    - **Simple tasks** (translation, summarization): Use lightweight models like `deepseek-chat`
    - **Complex reasoning** (code generation, analysis): Use powerful models like `gpt-4`
    - **Real-time response**: Choose models with fast response speed

#### `memory` (Memory Persistence)

Agent's memory mode, allowing Agent to automatically manage multi-turn conversation states.

```nexa
agent ChatBot {
    prompt: "You are a friendly chat assistant",
    memory: "persistent"  // Enable persistent memory
}

flow main {
    // First call
    ChatBot.run("My name is Zhang San");
    
    // Second call - Agent will remember the previous conversation
    ChatBot.run("What's my name?");  // Will answer "Zhang San"
}
```

#### `stream` (Streaming Output Switch)

Setting this to `true` can directly enable token-level streaming response from the large model. Let Agent think and output simultaneously, achieving stutter-free real-time feedback for end users.

```nexa
agent StreamBot {
    prompt: "You are a story creation assistant",
    stream: true  // Enable streaming output
}
```

#### `cache` (Intelligent Cache)

When enabled, identical or similar requests will reuse previous results, significantly reducing token consumption and response time.

```nexa
agent CachedBot {
    prompt: "Answer common questions",
    cache: true  // Enable semantic cache
}
```

!!! info "Cache Mechanism"
    - Based on **semantic similarity** matching, not just exact matching
    - Cache is stored in the `.nexa_cache/` directory
    - Can be cleared via `nexa cache clear`

#### `experience` (Long-term Memory)

Load long-term memory files to give Agent persistent knowledge and experience.

```nexa
agent SmartBot {
    prompt: "Answer questions based on historical experience",
    experience: "bot_memory.md"  // Load memory file
}
```

Memory file format example (`bot_memory.md`):

```markdown
# Bot Memory Library

## User Preferences
- Likes concise answers
- Prefers technical topics

## FAQ
- What is an Agent? An Agent is an entity that can perceive its environment and take action.

## Lessons Learned
- Don't assume user's technical background
- Complex concepts need step-by-step explanation
```

#### `fallback` (Model Disaster Recovery Degradation)

When request fails due to API RateLimit or unexpected downtime, set a `fallback` model as a disaster recovery option for seamless runtime switching.

```nexa
// Single backup model
agent ResilientBot {
    model: "openai/gpt-4",
    fallback: "deepseek/deepseek-chat",  // Auto-switch when gpt-4 unavailable
    prompt: "..."
}

// Multi-level backup (v0.9.7+)
agent HighAvailabilityBot {
    model: ["openai/gpt-4", fallback: "anthropic/claude-3-sonnet", fallback: "deepseek/deepseek-chat"],
    prompt: "..."
}
```

---

## 🎯 Agent Decorators

v1.0 introduces Agent decorator syntax, allowing metadata configuration to be added before Agent definitions.

### Available Decorators

| Decorator | Parameter | Description |
|-------|------|------|
| `@limit` | `max_tokens` | Limit maximum output token count |
| `@timeout` | `seconds` | Set execution timeout |
| `@retry` | `count` | Set failure retry count |
| `@temperature` | `value` | Set model temperature parameter |

### Usage Examples

```nexa
// Limit output length
@limit(max_tokens=500)
agent ConciseBot {
    prompt: "Answer questions concisely",
    model: "deepseek/deepseek-chat"
}

// Set timeout and retry
@timeout(seconds=60)
@retry(count=5)
agent ResilientBot {
    prompt: "Handle potentially time-consuming tasks",
    model: "openai/gpt-4"
}

// Combine multiple decorators
@limit(max_tokens=1000)
@timeout(seconds=120)
@retry(count=3)
@temperature(value=0.7)
agent ProductionBot {
    role: "Production environment intelligent assistant",
    prompt: "Provide high-quality professional answers",
    model: "anthropic/claude-3-sonnet"
}
```

### Decorator and Property Equivalence

Decorator syntax is equivalent to Agent properties:

```nexa
// Using decorators
@timeout(seconds=60)
@retry(count=3)
agent Bot1 {
    prompt: "..."
}

// Equivalent to using properties
agent Bot1 {
    prompt: "...",
    timeout: 60,
    retry: 3
}
```

!!! tip "Selection Advice"
    - **Use decorators**: When you need to highlight runtime configurations (like timeout, retry)
    - **Use properties**: When there are many configurations that need unified management
    - Both approaches can be mixed, decorators have higher priority

---

## � Control Flow Hub: `flow` and `.run()`

Just defining Agents is like recruiting world-class employees for different departments, but without giving them desks and network access, they remain forever dormant. We need a carrier to activate and orchestrate them. All this happens in `flow`.

In Nexa, the system entry flow is usually named `flow main`, similar to the `main` function in C or Java console runtime, which is the first frame where a single file or even an entire project begins execution (Execution Entrypoint).

### ⚡ Hello World Complete Practical Analysis

Let's carefully break down a classic `01_hello_world.nx` script:

```nexa
// 1. Define agent: We gave it a friendly personality, and don't need to specify a model (use default fallback)
agent HelloWorldBot {
    role: "A very helpful and concise assistant.",
    prompt: "You must always greet the user cheerfully and briefly in less than 20 words."
}

// 2. Start flow entry
flow main {
    // Variable assignment: In Nexa, strings usually contain natural semantic requests, you can inject them directly via equals sign
    greeting_request = "Say hello to Nexa developers all around the world!";
    
    // Call agent's .run() method to send instruction to model for reasoning and return response.
    // The underlying concurrency, network requests, RateLimit fallback are all hidden from the user.
    response = HelloWorldBot.run(greeting_request);
    
    // Print result
    print(response);
}
```

### Execution Result

```bash
$ nexa run hello_world.nx

Hello, Nexa developers! 🌍 Welcome to the future of agent programming!
```

!!! info "Underlying Runtime Mechanism"
    When the execution command is entered, Nexa compiler first establishes static graph nodes, performs static verification on incoming and outgoing data types, ensuring the entire script has no orphan deadlocks. Then it seamlessly transpiles to efficient asynchronous Python runtime (using `asyncio`), awakening the `HelloWorldBot` instance. This is not only the simplest Agent Hello World on the web, but also the safest one.

### `flow` Syntax Details

```nexa
// Basic syntax
flow <flow_name> {
    // statements...
}

// Parameterized flow (v0.9+)
flow process_user(user_id: string, action: string) {
    // Use parameters
    result = Agent.run(user_id + " wants to " + action);
}
```

### `.run()` Method Details

```nexa
// Basic call
result = Agent.run("your input");

// Multi-parameter call
result = Agent.run("primary input", "additional context");

// Chained call (pipeline)
result = input >> Agent1 >> Agent2 >> Agent3;
```

---

## 🔀 Traditional Control Flow (v1.0.1+)

Nexa v1.0.1-beta introduces traditional control flow statements, providing more flexible programming capabilities.

### if/else if/else Statements

```nexa
// Basic if statement
if score >= 90 {
    print("Excellent!");
}

// if/else statement
if temperature > 30 {
    print("It's hot today");
} else {
    print("The weather is comfortable");
}

// if/else if/else chain
if user_level == "admin" {
    grant_full_access();
} else if user_level == "moderator" {
    grant_partial_access();
} else {
    grant_basic_access();
}
```

### for each Loop

Iterates over each element in a collection:

```nexa
// Iterate over list
tasks = ["task1", "task2", "task3"];
for each task in tasks {
    result = Agent.run(task);
    print(result);
}

// Iterate over dictionary
config = {"model": "gpt-4", "timeout": 60};
for each key, value in config {
    print(key + ": " + value);
}
```

### while Loop

Executes repeatedly while a condition is true:

```nexa
// Basic while loop
count = 0;
while count < 5 {
    print("Current count: " + count);
    count = count + 1;
}

// while loop with Agent call
attempts = 0;
max_attempts = 3;
while attempts < max_attempts {
    result = Agent.run("Try task");
    if result == "success" {
        break;  // Exit loop on success
    }
    attempts = attempts + 1;
}
```

### break and continue

Control loop execution flow:

```nexa
// break: Exit loop early
for each item in items {
    if item == "stop_signal" {
        break;  // Stop iteration immediately
    }
    process(item);
}

// continue: Skip current iteration
for each number in numbers {
    if number == 0 {
        continue;  // Skip zero values
    }
    calculate(number);
}
```

---

## 🔢 Binary and Comparison Operators (v1.0.1+)

### Arithmetic Operators

| Operator | Description | Example |
|---------|-----|------|
| `+` | Addition | `a + b` |
| `-` | Subtraction | `a - b` |
| `*` | Multiplication | `a * b` |
| `/` | Division | `a / b` |
| `%` | Modulo | `a % b` |

```nexa
// Arithmetic operations
total = price * quantity + shipping_fee;
average = sum / count;
remainder = total % divisor;
```

### Comparison Operators

| Operator | Description | Example |
|---------|-----|------|
| `==` | Equal | `a == b` |
| `!=` | Not equal | `a != b` |
| `<` | Less than | `a < b` |
| `>` | Greater than | `a > b` |
| `<=` | Less than or equal | `a <= b` |
| `>=` | Greater than or equal | `a >= b` |

```nexa
// Comparison operations
if score >= 60 {
    print("Passed");
}

if status != "completed" {
    retry_task();
}
```

### Logical Operators

| Operator | Description | Example |
|---------|-----|------|
| `and` | Logical AND | `a and b` |
| `or` | Logical OR | `a or b` |
| `not` | Logical NOT | `not a` |

```nexa
// Logical operations
if is_valid and has_permission {
    execute_action();
}

if retry_count > 3 or timeout_occurred {
    report_failure();
}
```

---

## 🐍 Python Escape Hatch (v1.0.1+)

When you need advanced Python features that Nexa doesn't directly support, use the Python escape hatch to embed Python code directly.

### Basic Syntax

```nexa
python! """
    # Your Python code here
    result = complex_calculation()
    return result
"""
```

### Use Cases

1. **Complex Data Processing**: Use NumPy, Pandas, etc.
2. **Third-party Library Integration**: Call any Python library
3. **Performance Optimization**: Use optimized Python implementations
4. **Legacy Code Integration**: Reuse existing Python code

### Complete Example

```nexa
agent DataAnalyzer {
    prompt: "Analyze data and provide insights"
    uses std.fs
}

flow main {
    # Read data
    raw_data = std.fs.file_read("data.csv");
    
    # Use Python for complex analysis
    stats = python! """
        import json
        import statistics
        
        # Parse data
        data = json.loads(raw_data)
        values = [item['value'] for item in data]
        
        # Calculate statistics
        result = {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0
        }
        
        return json.dumps(result)
    """
    
    # Display results
    print(stats);
    
    # Agent provides insights
    insights = DataAnalyzer.run(stats);
    print(insights);
}
```

!!! warning "Security Note"
    Python escape hatch bypasses Nexa's sandbox. Use with caution in production environments and ensure code comes from trusted sources.

---

## 🔍 Built-in Tool Mounting and Environment Sandbox Penetration (`uses` Keyword)

If it only produces strings in the console, the large model is just a "chatting" vase. A true large model agent (Agent) needs to interact with the digital world (like checking weather, deleting files, writing spreadsheets).

In traditional Python glue code development, to let a large model call a function, you need to use extremely anti-human JSON Schema syntax to hand-write Function Calling configuration. Moreover, once the function signature changes, if you forget to update the Schema accordingly, the entire call chain will crash at runtime.

In the Nexa universe, all it takes is a native `uses` keyword declaration! Nexa builds function binding logic directly into the compiler through reflection mechanism.

### Basic Usage

```nexa
agent Interactor {
    // Native syntax-level loading of sandbox environment packages
    uses [std.ask_human, std.os.file_read]
    
    prompt: "When encountering uncertain risky operations, prioritize calling ask_human to report the situation to human review and obtain permission. Use file_read when necessary to check local configuration."
}
```

!!! success "Eliminating Schema Troubles from the Root"
    The `std.ask_human` and `std.os.file_read` used above are Nexa built-in standard packages. When loaded with `uses`, **Nexa's compiler will automatically crawl the function signatures and `docstrings` inside these Python tools in the background, and compile them into Native Function Calling Payloads adapted for each major model vendor!** This means developers don't need to hand-write JSON at all, or even think about different models' different requirements for tool calling. It even supports parameter validation through type hints!

### Standard Library Tool Overview

| Namespace | Tool | Description |
|---------|-----|------|
| `std.fs` | `file_read`, `file_write` | File system operations |
| `std.http` | `get`, `post` | HTTP requests |
| `std.time` | `now`, `sleep` | Time-related operations |
| `std.shell` | `execute` | Execute shell commands |
| `std.ask_human` | `call` | Human-computer interaction inquiry |
| `std.json` | `parse`, `stringify` | JSON processing |

### Usage Examples

```nexa
// File processing Agent
agent FileAssistant uses std.fs {
    prompt: "Help users manage files, can read and write files"
}

// Network request Agent
agent WebScraper uses std.http {
    prompt: "Get content from web pages and extract information"
}

// Multi-tool Agent
agent MultiToolAgent uses std.fs, std.http, std.time {
    prompt: "I can handle files, access the network, and get time"
}
```

---

## 🎯 Agent Definition Common Patterns

### Pattern 1: Simple Conversation Agent

```nexa
agent ChatBot {
    role: "Friendly chat assistant",
    model: "deepseek/deepseek-chat",
    prompt: "Have friendly daily conversations with users"
}
```

### Pattern 2: Professional Domain Agent

```nexa
agent LegalAdvisor {
    role: "Senior legal consultant, specializing in contract law",
    model: "openai/gpt-4",
    prompt: """
    Provide professional legal advice to users, especially contract-related issues.
    Note: Remind users that this is only reference advice and does not constitute formal legal opinion.
    """,
    memory: "persistent"
}
```

### Pattern 3: Tool-Enhanced Agent

```nexa
agent DataAnalyst uses std.fs, std.http {
    role: "Data analyst",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze data and generate reports",
    cache: true
}
```

### Pattern 4: High Availability Agent

```nexa
agent ProductionBot {
    role: "Production environment assistant",
    model: ["openai/gpt-4", fallback: "deepseek/deepseek-chat"],
    prompt: "...",
    cache: true,
    timeout: 60
}
```

---

## ⚠️ Common Errors and Solutions

### Error 1: Model Format Error

```nexa
// ❌ Wrong
agent Bot {
    model: "gpt-4"  // Missing provider prefix
}

// ✅ Correct
agent Bot {
    model: "openai/gpt-4"
}
```

### Error 2: Agent Definition Order Error

```nexa
// ❌ Wrong: Agent defined after flow
flow main {
    result = MyBot.run("hello");
}

agent MyBot {
    prompt: "..."
}

// ✅ Correct: Agent defined before flow
agent MyBot {
    prompt: "..."
}

flow main {
    result = MyBot.run("hello");
}
```

### Error 3: Property Name Spelling Error

```nexa
// ❌ Common spelling errors
agent Bot {
    promt: "...",      // Should be prompt
    moedl: "gpt-4",    // Should be model
    rol: "assistant"   // Should be role
}

// ✅ Correct spelling
agent Bot {
    prompt: "...",
    model: "openai/gpt-4",
    role: "assistant"
}
```

### Error 4: Forgetting Required Properties

```nexa
// ❌ Wrong: Missing prompt
agent Bot {
    role: "assistant"  // Only role, no prompt
}

// ✅ Correct
agent Bot {
    role: "assistant",
    prompt: "Help users solve problems"  // prompt is required
}
```

---

## 🆕 v1.3.x New Declaration Keywords Quick Reference

Nexa v1.3.x introduces multiple new declaration keywords that extend the language's expressiveness and enterprise capabilities. Here's a quick overview; for detailed usage, refer to the corresponding chapters.

### Data Modeling Keywords

| Keyword | Version | Description | Example |
|---------|---------|-------------|---------|
| `struct` | v1.3.x | Define struct | `struct Point { x: Int, y: Int }` |
| `enum` | v1.3.x | Define enum | `enum Option[T] { Some(T), None }` |
| `trait` | v1.3.x | Define trait | `trait Printable { fn format() -> String }` |
| `impl` | v1.3.x | Implement trait | `impl Printable for Point { ... }` |
| `type` | v1.0.2+ | Define semantic type | `type Email = string @ "valid email"` |

### Enterprise Declaration Keywords

| Keyword | Version | Description | Example |
|---------|---------|-------------|---------|
| `job` | v1.3.3 | Define background job | `job SendEmail { handler: ..., retry: 3 }` |
| `server` | v1.3.4 | Define HTTP server | `server MyApp { route GET "/hello" { ... } }` |
| `db` | v1.3.5 | Define database | `db main_db { type: sqlite, path: "data.db" }` |
| `auth` | v1.3.6 | Define authentication | `auth my_auth { providers: ["google"] }` |
| `kv` | v1.3.7 | Define KV store | `kv my_cache { path: ":memory:" }` |

### Contract Keywords

| Keyword | Version | Description | Example |
|---------|---------|-------------|---------|
| `requires` | v1.2.0 | Precondition | `requires: amount > 0` |
| `ensures` | v1.2.0 | Postcondition | `ensures: result.success == true` |
| `invariant` | v1.2.0 | Invariant | `invariant: state in ["idle", "running"]` |

!!! info "Deep Learning"
    - Data modeling keywords (struct/enum/trait/impl) detailed usage: [Advanced Features](part2_advanced.en.md)
    - Enterprise declaration keywords (job/server/db/auth/kv) detailed usage: [Enterprise Architecture Features](part5_enterprise.en.md)
    - Contract keywords (requires/ensures/invariant) detailed usage: [Syntax Extensions](part3_extensions.en.md)

---

## 📝 Chapter Summary

In this chapter, we learned:

1. **Agent Definition**: Using the `agent` keyword to define intelligent agents
2. **Core Properties**: `role`, `prompt`, `model`, `memory`, `stream`, `cache`, `requires`, `ensures`, etc.
3. **Flow Control**: Using `flow main` as program entry point
4. **Tool Mounting**: Using the `uses` keyword to load standard library tools
5. **Common Patterns**: Simple conversation, professional domain, tool-enhanced, high-availability patterns
6. **Common Errors**: Model format, definition order, property spelling, etc.
7. **v1.3.x New Keywords**: struct/enum/trait/impl/type/job/server/db/auth/kv/requires/ensures/invariant

But this only unleashes the large language model's single-agent task capability. Real business systems are filled with complex and lengthy collaborative interleaving: How to make a dozen agents with clear divisions of labor complete tasks in relay? How to achieve perfect consensus among agents with different opinions?

Don't blink, this is exactly what the next chapter **Multi-Agent Scheduling and Control (Advanced Features)** will present for you - the true orchestration magic.

---

## 🔗 Related Resources

- [Quickstart Tutorial](quickstart.en.md) - Master Nexa in 30 minutes
- [Advanced Features](part2_advanced.en.md) - Pipe/Pattern Matching/ADT details
- [Syntax Extensions](part3_extensions.en.md) - Contract/Type/Error Propagation
- [Enterprise Architecture](part5_enterprise.en.md) - HTTP Server/Database/Auth
- [Complete Example Collection](examples.en.md) - More practical code
- [Troubleshooting Guide](troubleshooting.en.md) - Solve development issues
