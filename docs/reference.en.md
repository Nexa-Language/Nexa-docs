---
comments: true
---

# Nexa Language Reference Manual

This manual details the syntax specification, semantic rules, and type system of the Nexa language. All grammar rules strictly match the source code in `src/nexa_parser.py`.

---

## 📖 About This Manual

This reference manual is organized according to the following principles:

- **Precision**: Every syntactic construct has a clear semantic definition
- **Completeness**: Covers all language features, including v1.1–v1.3.x additions
- **Practicality**: Provides sufficient examples for understanding

!!! tip "Reading Advice"
    If you're new to Nexa, we recommend reading [Quickstart](quickstart.en.md) and [Basic Syntax](part1_basic.en.md) first, then returning to this manual.

---

## 1. Lexical Structure

### 1.1 Identifiers

Nexa identifiers follow these rules:

```
identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
```

**Valid identifier examples**:

```nexa
MyAgent           // PascalCase (recommended for Agents)
my_tool          // snake_case (recommended for tools)
_process_data    // underscore prefix
Parser2          // contains digits (cannot start)
```

**Invalid identifier examples**:

```nexa
2ndAgent         // starts with digit
my-agent         // contains hyphen
agent.name       // contains dot
```

### 1.2 Keywords

Nexa reserves the following keywords that cannot be used as identifiers:

| Category | Keywords |
|------|--------|
| Declarations | `agent`, `tool`, `protocol`, `flow`, `test`, `type`, `struct`, `enum`, `trait`, `impl`, `fn`, `job`, `server`, `db`, `auth`, `kv` |
| Control Flow | `match`, `intent`, `loop`, `until`, `if`, `else`, `for`, `while`, `break`, `continue` |
| Semantic Control | `semantic_if`, `fast_match`, `against` |
| Exception Handling | `try`, `catch` |
| Error Propagation | `?`, `otherwise` |
| Type Constraints | `implements`, `uses` |
| Design by Contract | `requires`, `ensures`, `invariant` |
| Concurrency | `spawn`, `parallel`, `race`, `channel`, `after`, `schedule`, `select` |
| Deferred Execution | `defer` |
| Pipe | `|>` |
| Null Coalescing | `??` |
| String Interpolation | `#{expr}` |
| Template | `template` |
| Other | `print`, `assert`, `fallback`, `join`, `role`, `model`, `prompt`, `memory`, `stream`, `cache`, `experience`, `include` |

### 1.3 Literals

#### String Literals

```nexa
"Hello, World!"           // Regular string
"Line 1\nLine 2"         // With escape characters
"Quote: \"nested\""      // With quotes
"""Multi-line string"""   // Multi-line string
```

#### String Interpolation Literals (v1.3.x)

```nexa
"Hello #{name}, you are #{age} years old!"   // Ruby-style interpolation
"Status: #{result ?? 'pending'}"             // Interpolation + null coalescing
"Agent #{agent.name} responding"             // Interpolation + dot access
```

**Interpolation expression support**:

| Expression Type | Example | Python Translation |
|-----------|------|-------------|
| Simple identifier | `#{name}` | `name` |
| Dot access | `#{user.name}` | `user["name"]` |
| Bracket access | `#{arr[0]}` | `arr[0]` |
| Combined | `#{data.items[0].name}` | `data["items"][0]["name"]` |

**Escape**: `\#{` → literal `#{`

#### Template String Literals (v1.3.6)

```nexa
template"""Hello {{name | upper}}!"""
template"""{{#for item in items}}{{@index}}:{{item}}{{/for}}"""
template"""{{#if is_admin}}Admin{{#elif is_mod}}Mod{{#else}}User{{/if}}"""
template"""{{> card user_data}}"""
```

#### Regular Expression Literals

```nexa
r"\d{4}-\d{2}-\d{2}"     // Date format
r"^[a-zA-Z_]\w*$"        // Identifier pattern
r"https?://[^\s]+"      // URL pattern
```

#### Number Literals

```nexa
42              // Integer
3.14            // Float
2048            // For max_tokens etc.
```

### 1.4 Comments

```nexa
// Single-line comment

/*
 * Multi-line comment
 * Can span multiple lines
 */

/// Document comment (for Agent, Tool descriptions)
```

---

## 2. Declarations

### 2.1 Agent Declaration

```nexa
agent_decl ::= agent_decorator* "agent" IDENTIFIER 
               ["->" return_type]
               ["uses" use_identifier_list]
               ["implements" IDENTIFIER]
               requires_clause*
               ensures_clause*
               "{" agent_property* "}"
```

**Examples**:

```nexa
// Basic definition
agent Greeter {
    role: "Friendly greeting assistant",
    model: "deepseek/deepseek-chat",
    prompt: "You are a warm and friendly assistant."
}

// With decorators
@limit(max_tokens=600)
@timeout(seconds=30)
agent Coder {
    prompt: "Write a short Python implementation.",
    model: "minimax/minimax-m2.5"
}

// With contract clauses
agent Reviewer implements ReviewResult
    requires: "input contains code"
    ensures: "result includes score"
{
    prompt: "Review the provided code.",
    model: "deepseek/deepseek-chat"
}

// With return type
agent Analyzer -> ReportResult uses std.http {
    role: "Data Analyst",
    prompt: "Analyze data and generate reports"
}
```

**Agent Properties**:

| Property | Type | Required | Description |
|-----|------|-----|------|
| `role` | string | No | Agent role description |
| `prompt` | string | **Yes** | Agent core task instruction |
| `model` | string | No | LLM model (format: `provider/model`) |
| `memory` | string | No | Memory mode |
| `stream` | boolean | No | Streaming output |
| `cache` | boolean | No | Smart caching |
| `experience` | string | No | Long-term memory file |
| `fallback` | string/list | No | Fallback model |
| `uses` | identifier_list | No | Stdlib permissions |
| `implements` | identifier | No | Protocol constraint |

**Agent Decorators**:

| Decorator | Parameters | Description |
|--------|------|------|
| `@limit` | `max_tokens=INT` | Max output tokens |
| `@timeout` | `seconds=INT` | Execution timeout |
| `@retry` | `count=INT` | Failure retry count |
| `@temperature` | `value=FLOAT` | Model temperature |

---

### 2.2 Tool Declaration

```nexa
tool_decl ::= "tool" IDENTIFIER "{" tool_body "}"
tool_body ::= tool_body_standard | tool_body_mcp | tool_body_python
```

**Examples**:

```nexa
// Standard tool
tool web_search {
    description: "Search web content",
    parameters: {
        "query": "Search keyword",
        "limit": "Result count limit"
    }
}

// MCP tool
tool search_mcp {
    mcp: "web-search-mcp-server"
}

// Python tool
tool calculator {
    python: "import math; return math.sqrt(input)"
}
```

---

### 2.3 Protocol Declaration

```nexa
protocol_decl ::= "protocol" IDENTIFIER "{" protocol_body* "}"
protocol_body ::= IDENTIFIER ":" STRING_LITERAL ","?
                | IDENTIFIER ":" type_expr ","?
```

**Examples**:

```nexa
// String type annotation (legacy format)
protocol ReviewResult {
    score: "int",
    summary: "string",
    bug_list: "list[string]",
    is_critical: "boolean"
}

// Type expression annotation (v1.3.1+)
protocol UserProfile {
    name: String,
    age: Int,
    email: Option[String]
}
```

---

### 2.4 Flow Declaration

```nexa
flow_decl ::= "flow" IDENTIFIER ["(" param_list ")"] ["->" type_expr]
              requires_clause* ensures_clause* block
```

**Examples**:

```nexa
// Basic definition
flow main {
    result = Greeter.run("Hello!");
    print(result);
}

// With parameters and return type
flow analyze(data: String) -> ReportResult
    requires: data != None
    ensures: "result contains analysis"
{
    return Analyzer.run(data);
}
```

---

### 2.5 Test Declaration

```nexa
test_decl ::= "test" STRING_LITERAL block
```

**Example**:

```nexa
test "Translation test" {
    result = Translator.run("Hello, World!");
    assert "Contains Chinese translation" against result;
}
```

---

### 2.6 Type Declaration (Semantic Types)

```nexa
type_decl ::= "type" IDENTIFIER "=" semantic_type
semantic_type ::= base_type "@" STRING_LITERAL    // Constrained type
               | base_type                          // Simple type
```

**Examples**:

```nexa
type Email = str @ "valid email address format"
type PositiveInt = int @ "must be greater than 0"
type Score = float @ "between 0.0 and 100.0"
```

---

### 2.7 Struct Declaration (v1.3.x)

```nexa
struct_decl ::= "struct" IDENTIFIER "{" struct_field* "}"
struct_field ::= IDENTIFIER ":" type_expr ","?
```

**Examples**:

```nexa
struct Point { x: Int, y: Int }
struct AgentResult { answer: String, confidence: Float, tokens: Int }
struct UserProfile { name: String, email: String, age: Int }
```

**Runtime representation** (handle-as-dict):

```json
{"_nexa_struct": "Point", "_nexa_struct_id": 1, "x": 1, "y": 2}
```

---

### 2.8 Enum Declaration (v1.3.x)

```nexa
enum_decl ::= "enum" IDENTIFIER "{" enum_variant* "}"
enum_variant ::= IDENTIFIER "(" IDENTIFIER ")"    // Value variant
              | IDENTIFIER                          // Unit variant
```

**Examples**:

```nexa
enum Option { Some(value), None }
enum Result { Ok(value), Err(error) }
enum AgentState { Idle, Running, Error(message) }
```

**Runtime representation** (handle-as-dict):

```json
// Value variant
{"_nexa_variant": "Some", "_nexa_enum": "Option", "_nexa_variant_id": 1, "value": 42}
// Unit variant
{"_nexa_variant": "None", "_nexa_enum": "Option"}
```

---

### 2.9 Trait Declaration (v1.3.x)

```nexa
trait_decl ::= "trait" IDENTIFIER "{" trait_method* "}"
trait_method ::= "fn" IDENTIFIER "(" param_list ")" ["->" type_expr]
```

**Examples**:

```nexa
trait Printable { fn format() -> String }
trait Comparable { fn compare(other: Self) -> Int }
trait Serializable { fn serialize() -> String }
```

---

### 2.10 Impl Declaration (v1.3.x)

```nexa
impl_decl ::= "impl" IDENTIFIER "for" IDENTIFIER "{" impl_method* "}"
impl_method ::= "fn" IDENTIFIER "(" param_list ")" ["->" type_expr] block
```

**Example**:

```nexa
impl Printable for Point {
    fn format() -> String {
        return "Point(x=#{self.x}, y=#{self.y})"
    }
}
```

---

### 2.11 Job Declaration (v1.3.3)

```nexa
job_decl ::= "job" IDENTIFIER "on" STRING_LITERAL 
             ["(" job_options ")"] "{" job_body "}"
```

**Example**:

```nexa
job SendEmail on "emails" (retry: 2, timeout: 120) {
    perform(user_id) {
        // Send email logic
    }
    on_failure(error, attempt) {
        // Failure handling logic
    }
}
```

**Job Options**:

| Option | Type | Description |
|------|------|--------|
| `retry` | int | Retry count |
| `timeout` | int | Timeout in seconds |

---

### 2.12 Server Declaration (v1.3.4)

```nexa
server_decl ::= "server" INT "{" server_body "}"
```

**Example**:

```nexa
server 8080 {
    static "/assets" from "./public"
    cors { origins: ["*"], methods: ["GET", "POST"] }
    middleware [auth_middleware]
    require_auth "/admin"
    
    route GET "/chat" => ChatBot
    route POST "/analyze" => DataExtractor |>> Analyzer
    semantic route "/help" => HelpBot
    
    group "/admin" {
        middleware [require_admin]
        route GET "/" => AdminBot
    }
}
```

**Server Directives**:

| Directive | Description |
|------|--------|
| `static` | Static file serving |
| `cors` | CORS configuration |
| `middleware` | Middleware list |
| `require_auth` | Auth-required path |
| `route` | Standard route |
| `semantic route` | Semantic route |
| `group` | Path grouping |

**HTTP Methods**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`

**Route Handlers**:

```nexa
// Single handler
route GET "/chat" => ChatBot

// DAG chain handler
route POST "/analyze" => DataExtractor |>> Analyzer |>> Reporter
```

---

### 2.13 DB Declaration (v1.3.5)

```nexa
db_decl ::= "db" IDENTIFIER "=" "connect" "(" STRING_LITERAL ")"
```

**Examples**:

```nexa
db app_db = connect("sqlite://data.db")
db prod_db = connect("postgresql://user:pass@localhost/mydb")
```

---

### 2.14 Auth Declaration (v1.3.6)

```nexa
auth_decl ::= "auth" IDENTIFIER "=" "enable_auth" "(" STRING_LITERAL ")"
```

**Example**:

```nexa
auth myAuth = enable_auth('{"providers": ["google", "github"]}')
```

---

### 2.15 KV Declaration (v1.3.6)

```nexa
kv_decl ::= "kv" IDENTIFIER "=" "open" "(" STRING_LITERAL ")"
```

**Example**:

```nexa
kv myCache = open("sqlite://cache.db")
```

---

## 3. Expressions

### 3.1 Pipe Operator `|>` (v1.3.x)

Left-to-right data flow pipe, LHS becomes the first argument of the RHS function.

```nexa
x |> f          // Equivalent to f(x)
x |> f(a, b)    // Equivalent to f(x, a, b)
data |> std.text.upper
prompt |> agent.run |> extract_answer
```

!!! note "Difference from `>>`"
    `|>` is a function pipe (left value passed as first argument), `>>` is an Agent pipeline (left value passed as input to next Agent).

---

### 3.2 Agent Pipeline Operator `>>`

Agent pipeline data transfer.

```nexa
A >> B              // B.run(A.run(input))
A >> B >> C         // C.run(B.run(A.run(input)))
input >> A >> B     // Starting from input
```

---

### 3.3 DAG Operators `|>>` and `&>>`

```nexa
// |>> Fan-out: input sent to multiple Agents simultaneously
input |>> [AgentA, AgentB, AgentC]

// &>> Merge: collect multiple results then pass to next Agent
[results] &>> Summarizer

// Combined usage
"topic" |>> [Writer, Reviewer, Editor] &>> Publisher
```

---

### 3.4 Null Coalescing Operator `??` (v1.3.x)

```nexa
expr ?? fallback    // If expr is None/Option::None/empty dict, return fallback
result ?? "fallback"
config.timeout ?? 30
agent.run(prompt) ?? "I couldn't process that"
```

**Semantics**:

| Left Value | Result |
|------|------|
| `None` | Right value |
| `Option::None` dict | Right value |
| Empty dict `{}` | Right value |
| Any other value | Left value |

---

### 3.5 Error Propagation Operator `?` (v1.3.2)

Rust-style error propagation, propagates errors upward on failure.

```nexa
let value = parse(input) ?           // If parse returns error, propagate error
let result = risky_operation() ?     // Same
```

---

### 3.6 Otherwise Operator (v1.3.2)

Provides error fallback value.

```nexa
let result = risky_op() otherwise "fallback"   // If error, return "fallback"
```

---

### 3.7 Match Expression (v1.3.x)

```nexa
match_expr ::= "match" expression "{" match_arm* "}"
match_arm ::= pattern "=>" expression
```

**7 Pattern Types**:

| Pattern | Syntax | Description |
|------|------|------|
| Wildcard | `_` | Matches anything, no binding |
| Variable | `name` | Matches anything, binds variable |
| Literal | `42`, `"hello"`, `true` | Matches exact value |
| Tuple | `(a, b)` | Matches tuple/array |
| Array | `[a, b, ..rest]` | Matches array + rest collector |
| Map | `{ name, age: a, ..other }` | Matches dict + rest collector |
| Variant | `Option::Some(v)` | Matches enum variant |

**Examples**:

```nexa
// Basic matching
match result {
    Option::Some(answer) => answer
    Option::None => "no response"
}

// Literal matching
match status {
    200 => "success"
    404 => "not found"
    _ => "unknown"
}

// Destructuring match
match entry {
    (key, value) => "#{key}: #{value}"
}

// Array destructuring
match items {
    [first, second, ..rest] => "first=#{first}, rest=#{rest.length}"
}

// Map destructuring
match user {
    { name, age: a, ..other } => "#{name} is #{a} years old"
}
```

---

### 3.8 Let Destructuring (v1.3.x)

```nexa
let_pattern_stmt ::= "let" pattern "=" expression
```

**Examples**:

```nexa
let (key, value) = entry
let [first, ..rest] = items
let { name, age: a } = user_data
```

---

### 3.9 For Destructuring (v1.3.x)

```nexa
for_pattern_stmt ::= "for" pattern "in" expression block
```

**Example**:

```nexa
for (name, score) in rankings {
    print("#{name}: #{score}")
}
```

---

### 3.10 Variant Call Expression (v1.3.x)

```nexa
variant_call_expr ::= IDENTIFIER "::" IDENTIFIER ["(" expression ")"]
```

**Examples**:

```nexa
let opt = Option::Some(42)
let res = Result::Ok("success")
let state = AgentState::Running
let err = AgentState::Error("connection failed")
```

---

### 3.11 Field Init Expression (v1.3.x)

```nexa
field_init ::= IDENTIFIER ":" expression
```

**Examples**:

```nexa
let p = Point(x: 1, y: 2)
let result = AgentResult(answer: "yes", confidence: 0.95, tokens: 150)
```

---

### 3.12 Concurrency Expressions (v1.3.6)

```nexa
spawn_expr ::= "spawn" "(" expression ")"
parallel_expr ::= "parallel" "(" expression ")"
race_expr ::= "race" "(" expression ")"
channel_expr ::= "channel" "(" ")"
after_expr ::= "after" "(" expression "," expression ")"
schedule_expr ::= "schedule" "(" expression "," expression ")"
select_expr ::= "select" "(" expression ["," expression] ")"
```

**Examples**:

```nexa
spawn(my_task)
parallel([task_a, task_b, task_c])
race([fast_task, slow_task])
channel()
after(500ms, cleanup())
schedule(every 30s, health_check())
```

---

## 4. Statements

### 4.1 Defer Statement (v1.3.x)

```nexa
defer_stmt ::= "defer" expression ";"
```

Executes in LIFO order, even if errors occur (similar to Go defer).

**Examples**:

```nexa
defer cleanup(db)
defer log("operation complete")
defer agent_cleanup(agent)
```

---

### 4.2 Contract Clauses (v1.2.0)

```nexa
requires_clause ::= "requires" STRING_LITERAL        // Semantic precondition
                  | "requires" comparison_expr        // Deterministic precondition

ensures_clause ::= "ensures" STRING_LITERAL           // Semantic postcondition
                | "ensures" comparison_expr           // Deterministic postcondition
```

**Examples**:

```nexa
// Deterministic contract
flow transfer(amount: int) -> Result
    requires: amount > 0
    ensures: result.success == true
{
    // Transfer logic
}

// Semantic contract (evaluated by LLM at runtime)
flow review(code: string) -> Report
    requires: "input contains valid source code"
    ensures: "result includes actionable feedback"
{
    // Review logic
}
```

---

### 4.3 Traditional Control Flow (v1.0.1+)

```nexa
// if/else if/else
if condition {
    // ...
} else if other_condition {
    // ...
} else {
    // ...
}

// for each loop
for each item in collection {
    // ...
}

// while loop
while condition {
    // ...
}

// break/continue
for each item in items {
    if item == "skip" { continue; }
    if item == "stop" { break; }
}
```

---

### 4.4 Semantic Control Flow

```nexa
// loop until — natural language loop termination control
loop {
    draft = Writer.run(feedback);
    feedback = Critic.run(draft);
} until ("Article quality is excellent")

// semantic_if — semantic condition judgment
semantic_if "user is frustrated" {
    SupportBot.run("Provide comfort and help");
}

// fast_match — fast intent matching
result = fast_match user_input {
    intent("Check weather") => WeatherBot.run(user_input),
    intent("Check news") => NewsBot.run(user_input),
    _ => ChatBot.run(user_input)
}
```

---

### 4.5 Python Escape Hatch (v1.0.1+)

```nexa
stats = python! """
    import statistics
    data = json.loads(raw_data)
    return statistics.mean(data)
"""
```

---

## 5. Type System (v1.3.1)

### 5.1 Type Expressions

```nexa
type_expr ::= type_union_expr | type_non_union_expr

type_union_expr ::= type_non_union_expr ("|" type_non_union_expr)+
type_non_union_expr ::= type_compound_expr "?" | type_compound_expr

type_compound_expr ::= "str" | "int" | "float" | "bool" | "unit"
                    | "Option" "[" type_expr "]"
                    | "Result" "[" type_expr "," type_expr "]"
                    | "list" "[" type_expr "]"
                    | "dict" "[" type_expr "," type_expr "]"
                    | IDENTIFIER    // Type alias
```

**Type Examples**:

| Type | Description | Example Value |
|------|------|--------|
| `Int` | Integer | `42` |
| `String` / `str` | String | `"hello"` |
| `Float` / `float` | Float | `3.14` |
| `Bool` / `bool` | Boolean | `true` |
| `Unit` / `unit` | Unit type | `()` |
| `Option[T]` | Optional type | `Some(42)` / `None` |
| `Result[T, E]` | Result type | `Ok("success")` / `Err("error")` |
| `list[T]` | List | `[1, 2, 3]` |
| `dict[K, V]` | Dictionary | `{"key": "value"}` |
| `T | U` | Union type | `Int | String` |
| `T?` | Optional shorthand | Equivalent to `Option[T]` |

### 5.2 Type Checking Modes

| Mode | Environment Variable | Description |
|------|---------|------|
| `strict` | `NEXA_TYPE_MODE=strict` | Type mismatch = runtime error |
| `warn` | `NEXA_TYPE_MODE=warn` | Type mismatch = log warning (default) |
| `forgiving` | `NEXA_TYPE_MODE=forgiving` | Type mismatch = silently ignore |

**Priority**: CLI flag > Environment variable > `nexa.toml` > Default (`warn`)

### 5.3 Lint Modes

| Mode | Environment Variable | Description |
|------|---------|------|
| `default` | `NEXA_LINT_MODE=default` | Only check code with type annotations (default) |
| `warn` | `NEXA_LINT_MODE=warn` | Warn about missing type annotations |
| `strict` | `NEXA_LINT_MODE=strict` | Missing type annotations = lint error |

---

## 6. Error Handling

### 6.1 Error Types

| Error Type | Description | Trigger Scenario |
|---------|------|---------|
| `ContractViolation` | Contract violation | `requires`/`ensures`/`invariant` condition not satisfied |
| `TypeViolation` | Type violation | Type mismatch in `strict` mode |
| `TypeWarning` | Type warning | Type mismatch in `warn` mode |
| `ValidationError` | Validation error | Semantic validation failure |
| `NexaResult.Err` | Result error | Error branch of `Result[T, E]` type |
| `NexaOption.None` | Null value | Null value of `Option[T]` type |

### 6.2 Error Propagation

```nexa
// ? operator: propagate error
let value = parse(input) ?

// otherwise operator: provide fallback
let result = risky_op() otherwise "fallback"

// try/catch
try {
    result = risky_operation();
} catch (error) {
    print("Error: #{error}");
}
```

---

## 7. Runtime Architecture Patterns

### 7.1 Handle-as-dict Pattern

All runtime handles (DB connections, KV stores, Auth sessions, compiled templates, struct instances, enum variants) are plain Python dicts with `_nexa_*` prefixed keys for JSON compatibility.

### 7.2 Thread-safe Registry Pattern

All runtime modules use global registries with `_registry_lock` (threading.Lock) + `_id_counter`.

### 7.3 StdTool Namespace Pattern

Standard library tools are registered via `StdTool` into namespaces: `std.db`, `std.auth`, `std.kv`, `std.concurrent`, `std.template`, `std.match`, `std.struct`, `std.enum`, `std.trait`, etc.

### 7.4 BOILERPLATE Code Generation Pattern

Each feature adds imports and helper functions to the `CodeGenerator`'s BOILERPLATE section.

---

## 🔗 Related Resources

- [Stdlib API](stdlib_reference.en.md)
- [CLI Reference](cli_reference.en.md)
- [Error Index](error_index.en.md)
- [Quickstart](quickstart.en.md)