---
comments: true
---

# Troubleshooting Guide

This document summarizes common problems and their solutions when using Nexa. If you encounter a problem, please check this guide first.

---

## 📋 Table of Contents

- [Installation and Environment Issues](#1-installation-and-environment-issues)
- [Syntax Error Troubleshooting](#2-syntax-error-troubleshooting)
- [Runtime Error Troubleshooting](#3-runtime-error-troubleshooting)
- [Model Call Issues](#4-model-call-issues)
- [Tool Call Issues](#5-tool-call-issues)
- [Protocol Related Issues](#6-protocol-related-issues)
- [Contract and Type Issues (v1.2+)](#7-contract-and-type-issues)
- [Database Issues (v1.3.5+)](#8-database-issues)
- [Authentication Issues (v1.3.6+)](#9-authentication-issues)
- [Concurrency Issues (v1.3.6+)](#10-concurrency-issues)
- [HTTP Server Issues (v1.3.4+)](#11-http-server-issues)
- [Job System Issues (v1.3.3+)](#12-job-system-issues)
- [Debugging Tips](#13-debugging-tips)

---

## 1. Installation and Environment Issues

### 1.1 `pip install` Failed

**Symptom**:
```
ERROR: Could not find a version that satisfies the requirement nexa
```

**Reason**: Nexa has not been published to PyPI yet, need to install from source.

**Solution**:
```bash
git clone https://github.com/your-org/nexa.git
cd nexa
pip install -e .
```

---

### 1.2 Python Version Incompatible

**Symptom**:
```
SyntaxError: invalid syntax
```
or
```
TypeError: ... got an unexpected keyword argument
```

**Reason**: Nexa requires Python 3.10 or higher.

**Solution**:
```bash
# Check Python version
python --version

# If version is lower than 3.10, upgrade or use virtual environment
# Using conda
conda create -n nexa python=3.10
conda activate nexa

# Or using venv
python3.10 -m venv nexa-env
source nexa-env/bin/activate  # Linux/macOS
# nexa-env\Scripts\activate   # Windows
```

---

### 1.3 Dependency Conflicts

**Symptom**:
```
ERROR: Cannot install nexa because these package versions have conflicting dependencies
```

**Solution**:
```bash
# Clean and reinstall
pip uninstall nexa -y
pip cache purge
pip install -e . --no-cache-dir
```

---

### 1.4 `nexa: command not found`

**Symptom**:
```bash
$ nexa run hello.nx
bash: nexa: command not found
```

**Reason**: pip installation path is not in PATH, or virtual environment is not activated.

**Solution**:
```bash
# Option 1: Ensure virtual environment is activated
source nexa-env/bin/activate

# Option 2: Use python -m to invoke
python -m nexa run hello.nx

# Option 3: Add pip path to PATH (not recommended)
export PATH="$HOME/.local/bin:$PATH"
```

---

## 2. Syntax Error Troubleshooting

### 2.1 Parse Error: Unexpected token

**Symptom**:
```
ParseError: Unexpected token '}' at line 15
```

**Common Causes**:

1. **Missing comma or semicolon**
```nexa
// ❌ Wrong
agent Bot {
    role: "Assistant"    // Missing comma
    prompt: "..."
}

// ✅ Correct
agent Bot {
    role: "Assistant",
    prompt: "..."
}
```

2. **Mismatched brackets**
```nexa
// ❌ Wrong
flow main {
    result = Bot.run("hello"
}

// ✅ Correct
flow main {
    result = Bot.run("hello");
}
```

3. **Unclosed string**
```nexa
// ❌ Wrong
agent Bot {
    prompt: "This is a very long prompt
            with line break but not closed"
}

// ✅ Correct: Use triple quotes
agent Bot {
    prompt: """
        This is a very long prompt
        line break is fine
    """
}
```

---

### 2.2 Agent Undefined

**Symptom**:
```
NameError: name 'MyAgent' is not defined
```

**Reason**: Agent is defined after flow, or typo.

**Solution**:
```nexa
// ❌ Wrong: Agent defined after flow
flow main {
    result = MyAgent.run("hello");
}

agent MyAgent {
    prompt: "..."
}

// ✅ Correct: Agent defined before flow
agent MyAgent {
    prompt: "..."
}

flow main {
    result = MyAgent.run("hello");
}
```

---

### 2.3 Property Name Typo

**Symptom**: Agent behaves abnormally, property not taking effect.

**Common Typos**:
```nexa
// ❌ Common misspellings
agent Bot {
    promt: "...",        // Should be prompt
    moedl: "gpt-4",      // Should be model
    rol: "Assistant"     // Should be role
}

// ✅ Correct spelling
agent Bot {
    prompt: "...",
    model: "gpt-4",
    role: "Assistant"
}
```

**Checklist**:
| Correct Spelling | Common Errors |
|---------|---------|
| `prompt` | `promt`, `prompts` |
| `model` | `moedl`, `Model` |
| `role` | `rol`, `Role` |
| `tools` | `tool`, `Tool` |
| `memory` | `memmory`, `Memory` |

---

### 2.4 Protocol Syntax Error

**Symptom**:
```
InvalidProtocolError: Protocol field type must be a string
```

**Error Example**:
```nexa
// ❌ Wrong: Type not wrapped in quotes
protocol UserInfo {
    name: string,        // Should be "string"
    age: int             // Should be "int"
}

// ✅ Correct
protocol UserInfo {
    name: "string",
    age: "int"
}
```

---

## 3. Runtime Error Troubleshooting

### 3.1 API Key Not Found

**Symptom**:
```
RuntimeError: API key not found for provider 'openai'
```

**Solution**:

1. **Check if secrets.nxs file exists**
```bash
ls -la secrets.nxs
```

2. **Check if key format is correct**
```bash
# secrets.nxs content example
OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxx"
MINIMAX_API_KEY = "xxxxxxxxxxxx"
MINIMAX_GROUP_ID = "xxxxxxxxxxxx"
```

3. **Check file location**
```
project/
├── secrets.nxs      # Must be in project root
├── main.nx
└── ...
```

---

### 3.2 Network Connection Timeout

**Symptom**:
```
httpx.ConnectTimeout: Connection timed out
```

**Solution**:

1. **Check network connection**
```bash
curl -I https://api.openai.com
```

2. **Configure proxy (if needed)**
```bash
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
```

3. **Increase timeout** (in code)
```nexa
agent Bot {
    model: "openai/gpt-4",
    prompt: "...",
    timeout: 60  // 60 second timeout
}
```

---

### 3.3 Out of Memory

**Symptom**:
```
MemoryError: Unable to allocate array
```

**Reason**: Long conversation history or large number of concurrent Agents.

**Solution**:

1. **Enable context compression**
```nexa
agent Bot {
    prompt: "...",
    max_history_turns: 5  // Limit history turns
}
```

2. **Use cache to reduce repeated computation**
```nexa
agent Bot {
    prompt: "...",
    cache: true  // Enable intelligent cache
}
```

3. **Reduce concurrency**
```nexa
// ❌ Avoid too many parallel Agents
input |>> [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10]

// ✅ Batch processing
input |>> [A1, A2, A3]
```

---

### 3.4 Loop Not Terminating

**Symptom**: `loop until` keeps running until timeout.

**Reason**: Termination condition too vague, LLM cannot accurately judge.

**Solution**:

1. **Use clearer termination conditions**
```nexa
// ❌ Vague condition
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("Article is perfect")  // Too subjective

// ✅ Clearer condition
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("Reviewer explicitly says 'passed' with no modification suggestions")
```

2. **Add maximum loop count protection**
```nexa
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("Article is perfect" or runtime.meta.loop_count >= 5)

// Check if exceeded
if (runtime.meta.loop_count >= 5) {
    print("Reached maximum retry count, please check manually");
}
```

---

## 4. Model Call Issues

### 4.1 Model Name Format Error

**Symptom**:
```
ModelError: Unknown model format: gpt-4
```

**Reason**: Model name must include provider prefix.

**Correct Format**:
```nexa
// ✅ Correct format
model: "openai/gpt-4"
model: "openai/gpt-4-turbo"
model: "deepseek/deepseek-chat"
model: "minimax/minimax-m2.5"
model: "anthropic/claude-3-sonnet"

// ❌ Wrong format
model: "gpt-4"           // Missing provider
model: "GPT-4"           // Case error
model: "deepseek-chat"   // Missing slash
```

---

### 4.2 Model Does Not Support Certain Features

**Symptom**:
```
NotImplementedError: Model 'xxx' does not support function calling
```

**Solution**:

Choose models that support required features:

| Feature | Supported Models |
|-----|----------|
| Function Calling | GPT-4, GPT-3.5-turbo, DeepSeek-Chat |
| Structured Output | GPT-4, Claude-3, DeepSeek-Chat |
| Vision | GPT-4-vision, Claude-3, MiniMax-VL |

---

### 4.3 Rate Limit

**Symptom**:
```
RateLimitError: Rate limit exceeded for model
```

**Solution**:

1. **Configure Fallback model**
```nexa
agent Bot {
    model: ["openai/gpt-4", fallback: "deepseek/deepseek-chat"],
    prompt: "..."
}
```

2. **Add retry configuration**
```nexa
agent Bot {
    model: "openai/gpt-4",
    prompt: "...",
    retry: 3,           // Retry count
    retry_delay: 5      // Retry delay (seconds)
}
```

3. **Use cache to reduce requests**
```nexa
agent Bot {
    cache: true,  // Reuse results for same requests
    prompt: "..."
}
```

---

### 4.4 Output Truncation

**Symptom**: Model output is truncated in the middle.

**Reason**: Reached token limit.

**Solution**:

```nexa
agent Bot {
    prompt: "...",
    max_tokens: 4096  // Increase output length limit
}
```

Or use decorator:
```nexa
@limit(max_tokens=4096)
agent Bot {
    prompt: "..."
}
```

---

## 5. Tool Call Issues

### 5.1 Tool Not Found

**Symptom**:
```
ToolNotFoundError: Tool 'my_tool' not found in registry
```

**Reason**: Tool not properly registered or imported.

**Solution**:

1. **Check uses declaration**
```nexa
// ❌ Wrong: Tool not declared
agent Bot {
    prompt: "..."
}
// Later calling Bot.run() cannot use tools

// ✅ Correct: Declare tools to use
agent Bot uses std.http, std.fs {
    prompt: "..."
}
```

2. **Check standard library import**
```nexa
// If using custom tool, ensure path is correct
agent Bot uses "my_tools.py" {
    prompt: "..."
}
```

---

### 5.2 Tool Parameter Error

**Symptom**:
```
ToolExecutionError: Invalid parameters for tool 'xxx'
```

**Solution**:

Check tool definition parameter format:
```nexa
// ❌ Wrong: Incorrect parameter format
tool MyTool {
    description: "Tool description",
    parameters: {
        param1: string  // Missing quotes
    }
}

// ✅ Correct
tool MyTool {
    description: "Tool description",
    parameters: {
        "param1": "string",
        "param2": "number"
    }
}
```

---

### 5.3 Tool Execution Timeout

**Symptom**:
```
TimeoutError: Tool execution timed out after 30s
```

**Solution**:

```nexa
agent Bot uses std.http {
    prompt: "...",
    tool_timeout: 60  // Increase timeout
}
```

---

## 6. Protocol Related Issues

### 6.1 Output Format Does Not Match Protocol

**Symptom**:
```
ProtocolValidationError: Expected field 'xxx' but got 'yyy'
```

**Reason**: LLM output does not match defined Protocol.

**Auto-fix Mechanism**:

Nexa automatically attempts to fix, but if it fails multiple times, you can:

1. **Simplify Protocol**
```nexa
// ❌ Overly complex Protocol
protocol ComplexData {
    field1: "string",
    field2: "list[dict[string, any]]",  // Too complex
    field3: "dict[string, list[int]]"
}

// ✅ Simplified Protocol
protocol SimpleData {
    field1: "string",
    field2: "string",  // Use string to represent complex structure
    field3: "string"
}
```

2. **Specify format requirements in Prompt**
```nexa
agent DataExtractor implements MyProtocol {
    prompt: """
    Extract data and strictly output in JSON format.
    Must include fields: field1, field2, field3
    """
}
```

---

### 6.2 Protocol Type Mismatch

**Symptom**:
```
TypeError: Expected 'int' but got 'string'
```

**Solution**:

Ensure types in Protocol match expected:
```nexa
// Correct type annotations
protocol DataTypes {
    text: "string",      // String
    number: "int",       // Integer
    price: "float",      // Float
    flag: "boolean",     // Boolean
    tags: "list[string]" // String list
}
```

---

## 7. Contract and Type Issues (v1.2+)

### 7.1 ContractViolation: requires Precondition Violation

**Symptom**:
```
ContractViolation: requires precondition failed: "input must be non-empty"
```

**Cause**: The `requires` contract condition was not satisfied before function/Agent execution.

**Solutions**:

1. **Check input data**: Ensure parameters satisfy the `requires` condition
```nexa
agent Validator {
    requires: "input must be non-empty"
    role: "validator"
    prompt: "validate input"
}

// ✅ Correct: ensure input is non-empty
flow main {
    data = "some content"
    result = Validator.run(data)
}

// ❌ Wrong: passing empty value
flow main {
    data = ""
    result = Validator.run(data)  // ContractViolation!
}
```

2. **Use `??` to provide default values**:
```nexa
flow main {
    data = raw_input ?? "default content"
    result = Validator.run(data)
}
```

3. **Use `otherwise` to handle contract violations**:
```nexa
flow main {
    result = Validator.run(data) otherwise "fallback result"
}
```

### 7.2 ContractViolation: ensures Postcondition Violation

**Symptom**:
```
ContractViolation: ensures postcondition failed: "output must contain summary"
```

**Cause**: Agent output did not satisfy the `ensures` condition.

**Solutions**:

1. **Optimize prompt**: Make Agent output more reliably satisfy postconditions
2. **Use `implements` for automatic retry correction**: Protocol + implements will auto-retry
3. **Relax ensures conditions**: If conditions are too strict, relax them appropriately

### 7.3 ContractViolation: invariant Violation

**Symptom**:
```
ContractViolation: invariant violation: "count must be >= 0"
```

**Cause**: Object state violated invariant constraints during operations.

**Solutions**:

1. **Check state change logic**: Ensure all operations maintain invariants
2. **Use `old` expression to verify state changes**:
```nexa
db MyDB {
    invariant: "count >= 0"
    ensures: "count == old(count) + 1"
}
```

### 7.4 TypeViolation: strict Mode Type Violation

**Symptom**:
```
TypeViolation: expected type 'int', got 'str'
```

**Cause**: In `NEXA_TYPE_MODE=strict` mode, type mismatches throw exceptions directly.

**Solutions**:

1. **Switch to warn mode** (recommended during development):
```bash
export NEXA_TYPE_MODE=warn
nexa run script.nx
```

2. **Add type annotations**: Ensure variables and functions have correct type declarations
3. **Use type narrowing**:
```nexa
flow main {
    value: int = some_input
    // After type narrowing, value is guaranteed to be int
}
```

### 7.5 TypeWarning: warn Mode Type Warning

**Symptom**:
```
TypeWarning: variable 'x' inferred as 'str', annotated as 'int'
```

**Cause**: In `NEXA_TYPE_MODE=warn` mode, type mismatches only produce warnings without interrupting execution.

**Solutions**:

1. **Check warning messages**: Confirm whether it's a genuine type issue
2. **Fix type annotations**: Make annotations consistent with actual values
3. **Use `nexa lint` to check**:
```bash
nexa lint script.nx --warn-untyped
```

---

## 8. Database Issues (v1.3.5+)

### 8.1 DatabaseError: Connection Failed

**Symptom**:
```
DatabaseError: failed to connect to SQLite database: /path/to/db.sqlite
```

**Cause**: Database file path doesn't exist or insufficient permissions.

**Solutions**:

1. **Check file path**: Ensure path is correct and has write permissions
```nexa
db MyDB {
    type: "sqlite"
    path: "./data/app.db"  // Use relative path
}
```

2. **Use in-memory database** (during development):
```nexa
db MyDB {
    type: "sqlite"
    path: ":memory:"  // In-memory database, no file needed
}
```

3. **Create data directory**:
```bash
mkdir -p ./data
```

### 8.2 DatabaseError: Query Failed

**Symptom**:
```
DatabaseError: query failed: SELECT * FROM users
```

**Cause**: SQL syntax error or table doesn't exist.

**Solutions**:

1. **Check SQL syntax**: Ensure SQL statements are correct
2. **Ensure table is created**: Execute CREATE TABLE before querying
```nexa
flow main {
    db_handle = std.db.sqlite.connect(":memory:")
    std.db.sqlite.execute(db_handle, "CREATE TABLE users (id INT, name TEXT)")
    std.db.sqlite.execute(db_handle, "INSERT INTO users VALUES (1, 'Alice')")
    result = std.db.sqlite.query(db_handle, "SELECT * FROM users")
    std.db.sqlite.close(db_handle)
}
```

3. **Use parameterized queries**: Avoid SQL injection
```nexa
result = std.db.sqlite.query(db_handle, "SELECT * FROM users WHERE id = ?", params: [1])
```

### 8.3 DatabaseError: Transaction Failed

**Symptom**:
```
DatabaseError: transaction failed: commit error
```

**Cause**: Transaction commit failed, possibly due to concurrent conflicts or constraint violations.

**Solutions**:

1. **Use explicit transaction control**:
```nexa
std.db.sqlite.begin(db_handle)
std.db.sqlite.execute(db_handle, "INSERT ...")
std.db.sqlite.commit(db_handle)  // Explicit commit
```

2. **Catch errors and rollback**:
```nexa
flow main {
    std.db.sqlite.begin(db_handle)
    result = std.db.sqlite.execute(db_handle, "INSERT ...") otherwise {
        std.db.sqlite.rollback(db_handle)
    }
}
```

---

## 9. Authentication Issues (v1.3.6+)

### 9.1 AuthError: Authentication Failed

**Symptom**:
```
AuthError: authentication failed: invalid credentials
```

**Cause**: Incorrect username/password or misconfigured authentication.

**Solutions**:

1. **Check auth declaration configuration**:
```nexa
auth MyApp {
    type: "jwt"
    secret: secret.JWT_SECRET
    algorithms: ["HS256"]
}
```

2. **Ensure secrets are configured**: Check `secrets.nxs` file
3. **Use `nexa validate` to check configuration**:
```bash
nexa validate script.nx
```

### 9.2 AuthError: JWT Error

**Symptom**:
```
AuthError: JWT error: token expired
```

**Cause**: JWT token expired or signature invalid.

**Solutions**:

1. **Set reasonable expiration time**:
```nexa
auth MyApp {
    type: "jwt"
    secret: secret.JWT_SECRET
    expires_in: 3600  // 1 hour
}
```

2. **Use std.auth.jwt_verify to validate token**:
```nexa
flow main {
    valid = std.auth.jwt_verify(token, secret.JWT_SECRET)
    if valid {
        // Process request
    } otherwise {
        // Return 401
    }
}
```

### 9.3 AuthError: CSRF Validation Failed

**Symptom**:
```
AuthError: CSRF validation failed: missing csrf_token
```

**Cause**: Request missing CSRF token or token mismatch.

**Solutions**:

1. **Include CSRF token in forms**:
```nexa
flow main {
    csrf_token = std.auth.csrf_generate(session_id)
    // Include token in form/request
}
```

2. **Validate CSRF token**:
```nexa
flow main {
    valid = std.auth.csrf_validate(session_id, submitted_token)
    if valid {
        // Process request
    } otherwise {
        // Reject request
    }
}
```

### 9.4 AuthError: OAuth Flow Error

**Symptom**:
```
AuthError: OAuth flow error: invalid redirect_uri
```

**Cause**: OAuth configuration error (redirect_uri mismatch, invalid client_id, etc.).

**Solutions**:

1. **Check OAuth configuration**: Ensure redirect_uri matches what's registered with the OAuth provider
2. **Use std.auth.oauth_* tools for step-by-step debugging**:
```nexa
flow main {
    auth_url = std.auth.oauth_github_authorize(client_id, redirect_uri)
    // User visits auth_url to authorize, then callback
    token = std.auth.oauth_github_callback(code, client_id, client_secret)
}
```

---

## 10. Concurrency Issues (v1.3.6+)

### 10.1 ConcurrencyError: Task Cancelled

**Symptom**:
```
ConcurrencyError: task cancelled: timeout exceeded
```

**Cause**: Concurrent task terminated due to timeout or explicit cancellation.

**Solutions**:

1. **Set reasonable timeout**:
```nexa
flow main {
    result = std.concurrent.spawn(task_fn, timeout: 30)
}
```

2. **Use `otherwise` to handle cancellation**:
```nexa
flow main {
    result = std.concurrent.spawn(task_fn) otherwise "fallback"
}
```

### 10.2 ConcurrencyError: Channel Closed

**Symptom**:
```
ConcurrencyError: channel closed: cannot send to closed channel
```

**Cause**: Attempting to send data to a closed Channel.

**Solutions**:

1. **Check Channel status**: Confirm Channel is not closed before sending
2. **Use `??` to handle empty channel**:
```nexa
flow main {
    ch = std.concurrent.channel(10)
    value = std.concurrent.ch_recv(ch) ?? "default"
}
```

3. **Close Channel correctly**: Only close after all senders are done

### 10.3 ConcurrencyError: race All Failed

**Symptom**:
```
ConcurrencyError: race all failed: no task completed successfully
```

**Cause**: All concurrent tasks in `race` failed.

**Solutions**:

1. **Add more candidate tasks**: Provide more alternatives
2. **Use `otherwise` to provide fallback for each task**:
```nexa
flow main {
    result = std.concurrent.race([
        primary_task otherwise None,
        backup_task otherwise None
    ])
}
```

---

## 11. HTTP Server Issues (v1.3.4+)

### 11.1 Route Not Found (EC01)

**Symptom**:
```
HTTPError: route not found: POST /api/unknown
```

**Cause**: Requested path not defined in server declaration.

**Solutions**:

1. **Check route definition**: Ensure server declaration includes the route
```nexa
server MyApp {
    route "/api/data": DataAgent
    route "/api/process": ProcessAgent
}
```

2. **Use `nexa routes` to view all routes**:
```bash
nexa routes script.nx
```

3. **Check request method and path**: Ensure HTTP method (GET/POST) matches the route

### 11.2 Contract Violation Maps to HTTP Status Code (EC02)

**Symptom**:
```
HTTP 401: ContractViolation (requires precondition failed)
HTTP 403: ContractViolation (ensures postcondition failed)
```

**Cause**: Contract violations automatically map to HTTP status codes (requires → 401, ensures → 403).

**Solutions**:

1. **This is by design**: Contract violations automatically convert to corresponding HTTP error codes
2. **Client should handle HTTP error codes correctly**:
```nexa
flow main {
    response = std.http.post("/api/data", data) otherwise {
        // Handle 401/403 errors
    }
}
```

3. **Relax contract conditions**: If conditions are too strict causing frequent 401/403

### 11.3 Port Conflict

**Symptom**:
```
Error: Port 8080 is already in use
```

**Cause**: Specified port is already occupied by another service.

**Solutions**:

1. **Use a different port**:
```bash
nexa serve script.nx --port 9090
```

2. **Find the process occupying the port**:
```bash
lsof -i :8080
kill <PID>
```

---

## 12. Job System Issues (v1.3.3+)

### 12.1 JobError: Job Execution Failed (EB01)

**Symptom**:
```
JobError: job execution failed: email_job_001
```

**Cause**: Error occurred during background job execution.

**Solutions**:

1. **Check Job definition**: Ensure job declaration and logic are correct
```nexa
job EmailJob {
    agent: EmailAgent
    queue: "email_queue"
    retry: 3
    backoff: 60
}
```

2. **View Job status**:
```bash
nexa jobs script.nx --status
```

3. **Use `otherwise` to handle failures**: Add error recovery in Job logic

### 12.2 JobError: Job Timeout (EB02)

**Symptom**:
```
JobError: job timeout: email_job_001 exceeded 300s
```

**Cause**: Job execution time exceeded the set timeout.

**Solutions**:

1. **Increase timeout**:
```nexa
job EmailJob {
    agent: EmailAgent
    timeout: 600  // Increase to 10 minutes
}
```

2. **Optimize Agent performance**: Reduce prompt complexity or use a faster model

### 12.3 JobError: Dead Letter Job (EB03)

**Symptom**:
```
JobError: dead letter job: email_job_001 failed after 3 retries
```

**Cause**: Job still fails after exhausting retry attempts, enters dead letter queue.

**Solutions**:

1. **Check dead letter jobs**:
```bash
nexa jobs script.nx --dead-letter
```

2. **Retry dead letter job**:
```bash
nexa jobs script.nx --retry-dead-letter email_job_001
```

3. **Increase retry count or adjust backoff strategy**:
```nexa
job EmailJob {
    retry: 5        // Increase retry count
    backoff: 120    // Increase backoff time
}
```

---

## 13. Debugging Tips

### 13.1 Use `nexa build` to View Generated Code

```bash
# Generate Python code for debugging
nexa build script.nx

# Will generate out_script.py
# You can directly run or inspect this file
python out_script.py
```

### 13.2 Enable Verbose Logging

```bash
# Enable debug mode at runtime
nexa run script.nx --debug

# Or set environment variable
export NEXA_DEBUG=1
nexa run script.nx
```

### 13.3 Check Intermediate Results

Use `print` in flow to output intermediate results:
```nexa
flow main {
    step1 = Agent1.run(input);
    print("Step 1 result: " + step1);
    
    step2 = Agent2.run(step1);
    print("Step 2 result: " + step2);
}
```

### 13.4 Debug with Python SDK

```python
from src.nexa_sdk import NexaRuntime

# Create runtime
runtime = NexaRuntime(debug=True)

# Run script
result = runtime.run_script("script.nx")

# Check result
print(result)
```

### 13.5 Check Cache Status

```bash
# View cache statistics
nexa cache stats

# Clear cache
nexa cache clear
```

---

## 14. Error Code Quick Reference

| Error Code | Meaning | Common Cause |
|---------|-----|---------|
| `E001` | Parse error | Syntax error, mismatched brackets |
| `E002` | Undefined identifier | Agent/Tool undefined or typo |
| `E003` | Type error | Parameter type mismatch |
| `E004` | Syntax error | Incorrect keyword usage |
| `E005` | Duplicate declaration | Same-name Agent/Protocol defined twice |
| `E101` | Agent execution failed | Model call failed, prompt error |
| `E102` | Tool execution failed | Tool parameter error, timeout |
| `E103` | Pipeline execution failed | Agent pipeline interrupted |
| `E104` | Intent routing failed | No matching intent |
| `E201` | ContractViolation (requires) | Precondition not satisfied |
| `E202` | ContractViolation (ensures) | Postcondition not satisfied |
| `E203` | ContractViolation (invariant) | Invariant violation |
| `E301` | TypeViolation (strict) | strict mode type violation |
| `E302` | TypeWarning (warn) | warn mode type warning |
| `E303` | Protocol type validation failed | Field type mismatch |
| `E401` | DatabaseError (connection) | Database connection failed |
| `E402` | DatabaseError (query) | SQL syntax error or table not found |
| `E403` | DatabaseError (transaction) | Transaction commit/rollback failed |
| `E501` | AuthError (authentication) | Invalid credentials |
| `E502` | AuthError (JWT) | Token expired or signature invalid |
| `E503` | AuthError (CSRF) | CSRF token mismatch |
| `E504` | AuthError (OAuth) | OAuth flow configuration error |
| `E601` | KVError (operation) | KV store operation failed |
| `E602` | KVError (serialization) | Data serialization/deserialization failed |
| `E701` | ConcurrencyError (cancelled) | Task cancelled or timeout |
| `E702` | ConcurrencyError (channel) | Channel closed |
| `E703` | ConcurrencyError (race) | race all failed |
| `E801` | TemplateError (compilation) | Template syntax error |
| `E802` | TemplateError (rendering) | Template rendering failed |
| `E901` | PatternMatchError (no match) | No matching branch |
| `E902` | PatternMatchError (destructuring) | Destructuring failed |
| `EA01` | ADTError (Struct) | Struct operation failed |
| `EA02` | ADTError (Enum) | Enum operation failed |
| `EA03` | ADTError (Trait) | Trait method call failed |
| `EB01` | JobError (execution) | Job execution failed |
| `EB02` | JobError (timeout) | Job timeout |
| `EB03` | JobError (dead letter) | Dead letter job |
| `EC01` | HTTPError (route) | Route not found |
| `EC02` | ContractViolation (HTTP) | HTTP contract violation |

---

## 15. Getting Help

If the above solutions don't resolve your issue:

1. **Check Documentation**: [Complete Example Collection](examples.md) may have similar scenarios
2. **Submit Issue**: Submit an Issue on GitHub repository, including:
   - Complete error message
   - Your code (sanitized)
   - Runtime environment information
3. **Community Discussion**: Use Giscus at the bottom of the documentation page to participate in discussions

---

<div align="center">
  <p>📖 Don't panic when encountering problems, check this guide or seek community help!</p>
</div>