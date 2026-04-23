---
comments: true
---

# 5. Enterprise Architecture Features (v1.3.x)

In Nexa's evolution, it has long ceased to be just a toy scripting language. To support serious large-scale production environment operations, Nexa v1.3.x introduces a series of enterprise-level features including HTTP Server, database integration, authentication system, KV store, structured concurrency, template engine, and background job system.

---

## 🌐 Built-In HTTP Server (v1.3.4)

Nexa v1.3.4 introduces a native HTTP Server DSL, allowing you to publish Agent flows as REST API services without external frameworks.

### Server Declaration

```nexa
server MyApp {
    route GET "/hello" {
        handler: hello_flow
    }
    
    route POST "/analyze" {
        requires: request.body != ""
        handler: analyze_flow
    }
    
    route GET "/report/{id}" {
        handler: report_flow
    }
}
```

### Starting the Server

```bash
# Start HTTP Server
nexa serve main.nexa

# Specify port
nexa serve main.nexa --port 8080
```

### Viewing Routes

```bash
# List all routes
nexa routes main.nexa

# JSON format output
nexa routes main.nexa --json
```

### Contract and HTTP Status Code Mapping

Contract clauses in server routes automatically map to HTTP status codes:

| Contract Type | HTTP Status Code | Description |
|--------------|-----------------|-------------|
| `requires` violation | 401 Unauthorized | Request didn't satisfy precondition |
| `ensures` violation | 403 Forbidden | Response didn't satisfy postcondition |

```nexa
server PaymentAPI {
    route POST "/transfer" {
        requires: amount > 0           // Violation → 401
        requires: sender != ""         // Violation → 401
        ensures: result.success        // Violation → 403
        handler: transfer_flow
    }
}
```

### Complete Example: Agent API Service

```nexa
agent Analyzer {
    role: "Data Analysis Expert",
    prompt: "Analyze input data and return structured report"
}

protocol AnalysisResult {
    summary: "string",
    score: "int",
    details: "list[string]"
}

agent StructuredAnalyzer implements AnalysisResult {
    role: "Structured Analysis Expert",
    prompt: "Analyze data and return JSON with summary, score, and details"
}

server DataAPI {
    route POST "/analyze" {
        requires: request.body != ""
        handler: analyze_flow
    }
    
    route GET "/status" {
        handler: status_flow
    }
}

flow analyze_flow(request) {
    result = StructuredAnalyzer.run(request.body);
    return result;
}

flow status_flow(request) {
    return {"status": "ok", "version": "1.3.4"};
}
```

---

## 🗄️ Database Integration (v1.3.5)

Nexa v1.3.5 introduces native database integration, supporting SQLite, PostgreSQL, and Agent memory storage, operated through `db` declarations and `std.db.*` standard library tools.

### DB Declaration

```nexa
db main_db {
    type: sqlite
    path: "data.db"
}
```

### SQLite Operations (std.db.sqlite)

```nexa
flow main {
    // Connect to database
    handle = std.db.sqlite.connect("data.db");
    defer std.db.sqlite.close(handle);  // Auto-close
    
    // Create table
    std.db.sqlite.execute(handle, 
        "CREATE TABLE IF NOT EXISTS users (id INT, name TEXT, age INT)");
    
    // Insert data
    std.db.sqlite.execute(handle, 
        "INSERT INTO users VALUES (1, 'Alice', 30)",
        []);
    
    // Query all rows
    rows = std.db.sqlite.query(handle, "SELECT * FROM users");
    print(rows);
    
    // Query single row
    row = std.db.sqlite.query_one(handle, 
        "SELECT * FROM users WHERE id = 1");
    print(row);
    
    // Transaction operations
    std.db.sqlite.begin(handle);
    std.db.sqlite.execute(handle, "INSERT INTO users VALUES (2, 'Bob', 25)");
    std.db.sqlite.commit(handle);
}
```

### PostgreSQL Operations (std.db.postgres)

```nexa
flow main {
    // Connect to PostgreSQL
    handle = std.db.postgres.connect("postgresql://user:pass@localhost/mydb");
    defer std.db.postgres.close(handle);
    
    // Query
    rows = std.db.postgres.query(handle, "SELECT * FROM products");
    
    // Parameterized query
    row = std.db.postgres.query_one(handle, 
        "SELECT * FROM products WHERE id = $1", ["42"]);
    
    // Transaction
    std.db.postgres.begin(handle);
    std.db.postgres.execute(handle, "UPDATE products SET price = $1 WHERE id = $2", ["99.99", "42"]);
    std.db.postgres.commit(handle);
}
```

### Agent Memory Storage (std.db.memory)

```nexa
flow main {
    // Store Agent memory
    std.db.memory.store(handle, "Analyst", "last_topic", "quantum computing");
    
    // Query Agent memory
    memory = std.db.memory.query(handle, "Analyst", "last_topic");
    print(memory);  // "quantum computing"
    
    // List all memories
    all_memories = std.db.memory.list(handle, "Analyst");
    
    // Delete memory
    std.db.memory.delete(handle, "Analyst", "last_topic");
}
```

---

## 🔐 Authentication & OAuth (v1.3.6)

Nexa v1.3.6 introduces a complete authentication system, supporting OAuth 2.0 PKCE flow, JWT, CSRF protection, API Key, and other authentication methods.

### Auth Declaration

```nexa
auth my_auth {
    providers: ["google", "github"]
    jwt_secret: "your-secret-key"
    csrf_enabled: true
}
```

### OAuth Flow

```nexa
flow main {
    // Start OAuth authentication
    auth_url = std.auth.oauth(name: "google");
    print("Please visit: #{auth_url}");
    
    // Enable authentication middleware
    std.auth.enable_auth(providers: ["google", "github"]);
}
```

### JWT Operations

```nexa
flow main {
    // Sign JWT
    token = std.auth.jwt_sign(claims: {"user_id": "123", "role": "admin"});
    print("Token: #{token}");
    
    // Verify JWT
    valid = std.auth.jwt_verify(token: token);
    print("Valid: #{valid}");
    
    // Decode JWT
    claims = std.auth.jwt_decode(token: token);
    print("Claims: #{claims}");
}
```

### CSRF Protection

```nexa
flow main {
    // Generate CSRF Token
    csrf_token = std.auth.csrf_token(request: request);
    
    // Generate CSRF form field
    csrf_field = std.auth.csrf_field(request: request);
    // Output: <input type="hidden" name="csrf_token" value="xxx">
    
    // Verify CSRF
    is_valid = std.auth.verify_csrf(request: request);
}
```

### API Key Management

```nexa
flow main {
    // Generate API Key (format: nexa-ak-{32hex})
    api_key = std.auth.api_key_generate(agent_name: "MyAgent");
    print("API Key: #{api_key}");
    
    // Verify API Key
    is_valid = std.auth.api_key_verify(api_key: api_key);
    
    // Get authentication context
    context = std.auth.auth_context(request: request);
}
```

### User Session Management

```nexa
flow main {
    // Get user info
    user = std.auth.get_user(request: request);
    
    // Get session data
    session = std.auth.get_session(request: request);
    
    // Get session details
    data = std.auth.session_data(request: request);
    
    // Set session
    std.auth.set_session(request: request, data: {"theme": "dark"});
    
    // Logout
    std.auth.logout_user(request: request);
    
    // Require authentication
    std.auth.require_auth(request: request);
}
```

---

## 📦 KV Key-Value Store (v1.3.6)

Nexa v1.3.6 introduces a built-in KV store, supporting in-memory and persistent modes, providing type-safe read/write operations and TTL expiration mechanisms.

### KV Declaration

```nexa
kv my_cache {
    path: ":memory:"
}
```

### Basic Operations

```nexa
flow main {
    // Open KV store
    kv_handle = std.kv.open(path: ":memory:");
    
    // Write
    std.kv.set(kv: kv_handle, key: "user_name", value: "Alice");
    
    // Read
    name = std.kv.get(kv: kv_handle, key: "user_name");
    print(name);  // "Alice"
    
    // Type-safe read
    count = std.kv.get_int(kv: kv_handle, key: "visit_count");
    label = std.kv.get_str(kv: kv_handle, key: "label");
    config = std.kv.get_json(kv: kv_handle, key: "config");
    
    // Set only if key doesn't exist (SET NX)
    std.kv.set_nx(kv: kv_handle, key: "first_visit", value: "2024-01-01");
    
    // Check if key exists
    exists = std.kv.has(kv: kv_handle, key: "user_name");
    
    // List all keys
    keys = std.kv.list(kv: kv_handle);
    
    // Delete key
    std.kv.del(kv: kv_handle, key: "temp_data");
    
    // Set TTL (seconds)
    std.kv.expire(kv: kv_handle, key: "session", ttl: 3600);
    
    // View TTL
    remaining = std.kv.ttl(kv: kv_handle, key: "session");
    
    // Increment
    std.kv.incr(kv: kv_handle, key: "counter");
    
    // Flush
    std.kv.flush(kv: kv_handle);
}
```

### Agent-Specific KV Operations

```nexa
flow main {
    // Agent KV query
    result = std.kv.agent_kv_query(kv: kv_handle, agent_name: "Analyst", key: "context");
    
    // Agent KV store
    std.kv.agent_kv_store(kv: kv_handle, agent_name: "Analyst", key: "context", value: "market data");
    
    // Agent KV context
    context = std.kv.agent_kv_context(kv: kv_handle, agent_name: "Analyst");
}
```

### Combined with `??`

```nexa
flow main {
    // KV read + null coalescing
    theme = std.kv.get(kv: kv_handle, key: "theme") ?? "light";
    lang = std.kv.get(kv: kv_handle, key: "language") ?? "en";
}
```

---

## ⚡ Structured Concurrency (v1.3.6)

Nexa v1.3.6 introduces a structured concurrency system, providing Channel, spawn, parallel, race and other primitives, ensuring concurrent task lifecycles are always controlled.

### Concurrency Expressions

```nexa
// spawn — start async task
task = spawn handler_fn(args)

// await — wait for task completion
result = await task

// parallel — execute multiple tasks in parallel
results = parallel [handler1, handler2, handler3]

// race — competitive execution, returns first completed result
winner = race [handler1, handler2]
```

### Channel Operations (std.concurrent)

```nexa
flow main {
    // Create channel
    (tx, rx) = std.concurrent.channel();
    
    // Send message
    std.concurrent.send(tx: tx, value: "hello");
    
    // Receive message
    msg = std.concurrent.recv(rx: rx);
    print(msg);  // "hello"
    
    // Timeout receive
    msg = std.concurrent.recv_timeout(rx: rx, timeout: 5000);
    
    // Non-blocking receive
    result = std.concurrent.try_recv(rx: rx);
    
    // Close channel
    std.concurrent.close(rx: rx);
    
    // Select — multi-channel selection
    value = std.concurrent.select(channels: [rx1, rx2]);
}
```

### Task Management

```nexa
flow main {
    // Start async task
    task = std.concurrent.spawn(handler: "process_data");
    
    // Wait for task completion
    result = std.concurrent.await_task(task: task);
    
    // Non-blocking wait
    result = std.concurrent.try_await(task: task);
    
    // Cancel task
    std.concurrent.cancel_task(task: task);
    
    // Parallel execution
    results = std.concurrent.parallel(handlers: ["handler1", "handler2", "handler3"]);
    
    // Race execution
    winner = std.concurrent.race(handlers: ["fast_handler", "backup_handler"]);
    
    // Delayed execution
    std.concurrent.after(delay: 1000, handler: "cleanup");
    
    // Scheduled execution
    schedule = std.concurrent.schedule(interval: 5000, handler: "health_check");
    
    // Cancel schedule
    std.concurrent.cancel_schedule(schedule: schedule);
    
    // Thread count
    count = std.concurrent.thread_count();
}
```

### Complete Example: Concurrent Data Processing

```nexa
flow main {
    // Parallel analysis of multiple data sources
    results = std.concurrent.parallel(handlers: [
        "analyze_market_data",
        "analyze_social_data",
        "analyze_news_data"
    ]);
    
    // Race: fast response + backup plan
    quick_result = std.concurrent.race(handlers: [
        "fast_analysis",
        "deep_analysis"
    ]);
    
    // Use Channel for coordination
    (tx, rx) = std.concurrent.channel();
    
    // Send task
    std.concurrent.send(tx: tx, value: raw_data);
    
    // Receive result
    processed = std.concurrent.recv_timeout(rx: rx, timeout: 10000);
    
    std.concurrent.close(rx: rx);
}
```

---

## 📄 Template System (v1.3.6)

Nexa v1.3.6 introduces a built-in template engine, supporting variable interpolation, conditional rendering, loops, filters, Agent slot filling, and other advanced features.

### Template String Literal

```nexa
// Use template"""...""" to define template
template"""Hello {{name}}, your score is {{score | default(0)}}!"""
```

### Template Operations (std.template)

```nexa
flow main {
    // Render template string
    result = std.template.render(
        template_str: "Hello {{name}}!",
        data: {"name": "Alice"}
    );
    print(result);  // "Hello Alice!"
    
    // Load template from file
    compiled = std.template.template(path: "report_template.nxt");
    
    // Compile template
    compiled = std.template.compile(path: "email_template.nxt");
    
    // Render compiled template
    output = std.template.render_compiled(
        compiled: compiled,
        data: {"user": "Bob", "date": "2024-01-01"}
    );
    
    // Apply filter
    formatted = std.template.filter_apply(
        value: "hello world",
        filter: "upper"
    );
}
```

### Agent Template Operations

```nexa
flow main {
    // Agent Prompt template
    prompt = std.template.agent_prompt(
        agent: Analyzer,
        template: "Analyze the following: {{input}}"
    );
    
    // Agent Slot fill
    filled = std.template.agent_slot_fill(
        agent: Analyzer,
        slots: {"topic": "AI trends", "depth": "detailed"}
    );
    
    // Register Agent template
    std.template.agent_register(
        agent: Analyzer,
        template: "report_template"
    );
}
```

### Template Syntax Reference

| Syntax | Description | Example |
|--------|-------------|---------|
| `{{var}}` | Variable interpolation | `{{name}}` |
| `{{var | filter}}` | Filter | `{{price | round(2)}}` |
| `{{var | default(val)}}` | Default value | `{{age | default(0)}}` |
| `{{#for item in list}}` | Loop | `{{#for p in products}}...{{/for}}` |
| `{{#if condition}}` | Conditional | `{{#if score > 80}}...{{/if}}` |
| `{{#include path}}` | Include sub-template | `{{#include header.nxt}}` |

---

## 📋 Background Job System (v1.3.3)

Nexa v1.3.3 introduces a background job system, supporting async execution, retry, timeout, dead letter queue, and worker management.

### Job Declaration

```nexa
job SendEmail {
    handler: email_handler
    retry: 3
    timeout: 120
    on_failure: notify_admin
}
```

### Job Management CLI

```bash
# View all jobs
nexa jobs main.nexa --all

# View jobs with specific status
nexa jobs main.nexa --status failed

# View dead letter queue
nexa jobs main.nexa --dead-letter

# Clear completed jobs
nexa jobs main.nexa --clear-completed

# Retry dead letter job
nexa jobs main.nexa --retry <job_id>
```

### Worker Management CLI

```bash
# View worker status
nexa workers main.nexa

# Add extra workers
nexa workers main.nexa --add 2

# Stop worker
nexa workers main.nexa --stop <worker_id>
```

### Complete Example: Async Email System

```nexa
job SendEmail {
    handler: send_email_flow
    retry: 3
    timeout: 60
    on_failure: log_failure
}

flow send_email_flow(to: string, subject: string, body: string) {
    result = EmailAgent.run("Send email to #{to} with subject #{subject}");
    return result;
}

flow log_failure(job_info) {
    std.fs.file_append("failed_emails.log", 
        "Failed: #{job_info.id} at #{std.time.time_now()}");
}

server EmailAPI {
    route POST "/send" {
        handler: api_send_email
    }
}

flow api_send_email(request) {
    // Async email sending (doesn't block HTTP response)
    job_id = spawn SendEmail(
        to: request.to,
        subject: request.subject,
        body: request.body
    );
    return {"status": "queued", "job_id": job_id};
}
```

---

## 🧠 Cognitive Architecture and Composite Long-Short Term Memory (Memory Engine)

In previous traditional development, if we wanted robots to have persistent context, we often needed to interface with complex Pinecone and Redis stacks, as well as intricate manual message truncation logic. In Nexa, you can access a powerful underlying architecture just by toggling parameters:

- **Long-term External Memory System**: Supports high-level semantic memory, automatic summarization and archiving of user experience, preferences, and implicit rules, and fully automatic extraction and feeding in future related conversations.
- **Dynamic Knowledge Graph Mapping**: The native memory system can extract text triples behind the scenes, autonomously maintain SQLite and Vector FTS, enabling Agents to independently establish and track graph-style associations.
- **Built-in Context Compactor**: When long conversations approach the Token limit, Nexa has embedded a pluggable entity extraction-type compression strategy, squeezing thousand-word long texts into extremely small context structures while preserving core key decisions.

---

## ⚡ Multi-Layer Semantic Computing Cache (L1/L2 Cache)

1. **L1 In-Memory Hot Cache**: Intercepts extremely high-frequency, extremely low-latency request collisions.
2. **L2 Disk Cold Cache**: Ensures persistent query retention and provides TTL timeout support and on-demand LRU eviction.
3. **Semantic Mapping Hit**: Embedded local similarity algorithms. Even if a user uses different words to ask about the same meaning, it can directly hit the cache barrier and save an expensive LLM API call.

---

## 🛡️ Role-Based Access Control Model (RBAC Sandbox)

- **Preset System Roles**: Assign security categories to various runtime sandbox entities, such as `admin`, `agent_standard`, `agent_readonly`.
- **Fine-grained Tool Locks**: When untrusted external users attempt to make Agents call dangerous instructions, the backend guardian stack will automatically intercept and trigger authentication rejection, fundamentally preventing disasters caused by Prompt injection privilege escalation.

---

## 📊 Chapter Summary

In this chapter, we learned Nexa's enterprise architecture features:

| Feature | Version | Description | Use Case |
|---------|---------|-------------|----------|
| HTTP Server | v1.3.4 | Native REST API service | Agent API publishing |
| Database | v1.3.5 | SQLite/PostgreSQL/Agent Memory | Data persistence |
| Auth & OAuth | v1.3.6 | JWT/CSRF/API Key/OAuth | Authentication & security |
| KV Store | v1.3.6 | Type-safe key-value store | Caching & configuration |
| Concurrency | v1.3.6 | Channel/spawn/parallel/race | Structured concurrency |
| Template | v1.3.6 | Template engine + Agent slots | Dynamic content generation |
| Job System | v1.3.3 | Async tasks + retry + dead letter queue | Background task processing |
| Memory Engine | v0.9+ | Long-short term memory + knowledge graph | Agent memory persistence |
| L1/L2 Cache | v0.9+ | Semantic computing cache | Cost optimization |
| RBAC Sandbox | v0.9+ | Role-based access control | Security protection |

These enterprise-level features have evolved Nexa from an Agent orchestration language into a complete Agent application platform, capable of supporting the full lifecycle from prototype to large-scale production.

---

## 🔗 Related Resources

- [CLI Command Reference](cli_reference.en.md) - serve/routes/jobs/workers command details
- [Standard Library API](stdlib_reference.en.md) - std.db/std.auth/std.kv/std.concurrent/std.template tool details
- [Language Reference Manual](reference.en.md) - server/db/auth/kv/job declaration syntax
- [Error Index](error_index.en.md) - database/auth/KV/concurrency/template/HTTP error codes
- [Best Practices](part6_best_practices.en.md) - Enterprise development experience