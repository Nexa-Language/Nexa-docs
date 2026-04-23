---
comments: true
---

# Nexa Stdlib Reference Manual

This document details all namespaces, tool functions, parameters, and usage examples for the Nexa standard library (`std`). All tool signatures strictly match the source code in `src/runtime/stdlib.py`.

---

## 📋 Overview

Nexa's standard library provides a set of built-in tools that enable Agents to interact with the external world. After declaring usage permissions via the `uses` keyword, Agents can call these tools.

### Namespace Overview

| Namespace | Description | Tool Count | Version |
|---------|------|---------|------|
| [`std.fs`](#stdfs-file-system-operations) | File system operations | 6 | v0.7+ |
| [`std.http`](#stdhttp-http-network-requests) | HTTP network requests | 4 | v0.7+ |
| [`std.time`](#stdtime-time-date-operations) | Time/date operations | 5 | v0.7+ |
| [`std.json`](#stdjson-json-data-processing) | JSON data processing | 3 | v0.7+ |
| [`std.text`](#stdtext-text-processing) | Text processing | 4 | v0.7+ |
| [`std.hash`](#stdhash-encryption-and-encoding) | Encryption and encoding | 4 | v0.7+ |
| [`std.math`](#stdmath-math-operations) | Math operations | 2 | v0.7+ |
| [`std.regex`](#stdregex-regular-expressions) | Regular expressions | 2 | v0.7+ |
| [`std.shell`](#stdshell-shell-commands) | Shell command execution | 2 | v0.9.7+ |
| [`std.ask_human`](#stdask_human-human-interaction) | Human interaction | 1 | v0.9.7+ |
| [`std.db.sqlite`](#stddbsqlite-sqlite-operations) | SQLite operations | 8 | v1.3.5 |
| [`std.db.postgres`](#stddbpostgres-postgresql-operations) | PostgreSQL operations | 8 | v1.3.5 |
| [`std.db.memory`](#stddbmemory-agent-memory-operations) | Agent memory operations | 4 | v1.3.5 |
| [`std.auth`](#stdauth-authentication-and-oauth) | Authentication & OAuth | 17 | v1.3.6 |
| [`std.kv`](#stdkv-key-value-store) | KV store | 18 | v1.3.6 |
| [`std.concurrent`](#stdconcurrent-structured-concurrency) | Structured concurrency | 18 | v1.3.6 |
| [`std.template`](#stdtemplate-template-system) | Template system | 18+ | v1.3.6 |
| [`std.pipe`](#stdpipe-pipe-operator) | Pipe operator | 1 | v1.3.x |
| [`std.defer`](#stddefer-deferred-execution) | Deferred execution | 1 | v1.3.x |
| [`std.null_coalesce`](#stdnull_coalesce-null-coalescing) | Null coalescing | 1 | v1.3.x |
| [`std.string`](#stdstring-string-interpolation) | String interpolation | 1 | v1.3.x |
| [`std.match`](#stdmatch-pattern-matching) | Pattern matching | 3 | v1.3.x |
| [`std.struct`](#stdstruct-struct) | Struct | 3 | v1.3.x |
| [`std.enum`](#stdenum-enum) | Enum | 3 | v1.3.x |
| [`std.trait`](#stdtrait-trait-and-impl) | Trait and impl | 5 | v1.3.x |

---

## 📁 std.fs - File System Operations

File system operations are the foundational capability for agents to interact with the local environment.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`file_read`](#file_read) | Read file content | `path` |
| [`file_write`](#file_write) | Write file | `path`, `content` |
| [`file_append`](#file_append) | Append file content | `path`, `content` |
| [`file_exists`](#file_exists) | Check if file exists | `path` |
| [`file_list`](#file_list) | List directory files | `directory` |
| [`file_delete`](#file_delete) | Delete file | `path` |

---

#### file_read

Read file content.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |
| `encoding` | string | No | `utf-8` | Encoding format |

**Return value**: File content string, or error message on failure.

**Example**:

```nexa
agent FileReader uses std.fs {
    role: "File reading assistant",
    prompt: "Help users read file content"
}

flow main {
    content = FileReader.run("Read the file /tmp/data.txt");
    print(content);
}
```

---

#### file_write

Write file content. Creates directories automatically if they don't exist.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |
| `content` | string | **Yes** | - | File content |
| `encoding` | string | No | `utf-8` | Encoding format |

**Return value**: Success message including character count written.

---

#### file_append

Append content to the end of a file.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |
| `content` | string | **Yes** | - | Content to append |
| `encoding` | string | No | `utf-8` | Encoding format |

**Return value**: Success message including character count appended.

---

#### file_exists

Check if a file or directory exists.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File/directory path |

**Return value**: JSON format `{ "exists": bool, "path": string }`.

---

#### file_list

List files in a directory.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `directory` | string | **Yes** | - | Directory path |
| `pattern` | string | No | `*` | File matching pattern (glob format) |

**Return value**: JSON format `{ "files": [string], "count": int }`.

---

#### file_delete

Delete a file.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |

**Return value**: Success or error message.

---

## 🌐 std.http - HTTP Network Requests

Native network request capability, supporting RESTful API calls.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`http_get`](#http_get) | GET request | `url` |
| [`http_post`](#http_post) | POST request | `url`, `data` |
| [`http_put`](#http_put) | PUT request | `url`, `data` |
| [`http_delete`](#http_delete) | DELETE request | `url` |

---

#### http_get

Send HTTP GET request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `headers` | object | No | `{}` | Request headers dict |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return value**: Response content string.

---

#### http_post

Send HTTP POST request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `data` | string | **Yes** | - | Request body content |
| `headers` | object | No | `{}` | Request headers dict |
| `content_type` | string | No | `application/json` | Content type |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return value**: JSON format `{ "status": int, "body": string }`.

---

#### http_put

Send HTTP PUT request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `data` | string | **Yes** | - | Request body content |
| `headers` | object | No | `{}` | Request headers dict |
| `content_type` | string | No | `application/json` | Content type |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return value**: JSON format `{ "status": int, "body": string }`.

---

#### http_delete

Send HTTP DELETE request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `headers` | object | No | `{}` | Request headers dict |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return value**: JSON format `{ "status": int, "body": string }`.

---

## 🕐 std.time - Time/Date Operations

Time-related operation tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`time_now`](#time_now) | Get current time | None |
| [`time_diff`](#time_diff) | Calculate time difference | `start`, `end` |
| [`time_format`](#time_format) | Format time | `iso_string` |
| [`time_sleep`](#time_sleep) | Sleep for specified seconds | `seconds` |
| [`time_timestamp`](#time_timestamp) | Get timestamp | None |

---

#### time_now

Get current time.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `format` | string | No | `%Y-%m-%d %H:%M:%S` | Time format |

**Return value**: Formatted time string.

---

#### time_diff

Calculate the difference between two times.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `start` | string | **Yes** | - | Start time (ISO format) |
| `end` | string | **Yes** | - | End time (ISO format) |
| `unit` | string | No | `seconds` | Unit: `seconds`/`minutes`/`hours`/`days` |

**Return value**: JSON format `{ "value": float, "unit": string, "days": int, "seconds": float }`.

---

#### time_format

Convert ISO format time to specified format.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `iso_string` | string | **Yes** | - | ISO time string |
| `format` | string | No | `%Y-%m-%d %H:%M:%S` | Output format |

**Return value**: Formatted time string.

---

#### time_sleep

Pause execution for specified seconds.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `seconds` | int | **Yes** | - | Sleep seconds |

**Return value**: JSON format `{ "sleep": int }`.

---

#### time_timestamp

Get current Unix timestamp.

**Parameters**: None

**Return value**: JSON format `{ "timestamp": int }`.

---

## 📦 std.json - JSON Data Processing

JSON data parsing, querying, and serialization.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`json_parse`](#json_parse) | Parse JSON | `text` |
| [`json_get`](#json_get) | Get JSON path value | `text`, `path` |
| [`json_stringify`](#json_stringify) | Serialize to JSON | `data` |

---

#### json_parse

Parse JSON string.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | JSON string |

**Return value**: Formatted JSON string (readable).

---

#### json_get

Extract value at specified path from JSON.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | JSON string |
| `path` | string | **Yes** | - | Path (e.g., `data.items.0`) |

**Return value**: Value at the path.

---

#### json_stringify

Serialize data to JSON string.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `data` | string | **Yes** | - | Data object (JSON format string) |
| `indent` | int | No | `2` | Indentation spaces |

**Return value**: Formatted JSON string.

---

## 📝 std.text - Text Processing

Text processing tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`text_split`](#text_split) | Split text | `text` |
| [`text_replace`](#text_replace) | Replace text | `text`, `old`, `new` |
| [`text_upper`](#text_upper) | To uppercase | `text` |
| [`text_lower`](#text_lower) | To lowercase | `text` |

---

#### text_split

Split text into multiple parts.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Text to split |
| `delimiter` | string | No | `\n` | Delimiter |
| `max_splits` | int | No | `-1` | Max split count (-1 = unlimited) |

**Return value**: JSON format `{ "parts": [string], "count": int }`.

---

#### text_replace

Replace content in text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Original text |
| `old` | string | **Yes** | - | Content to replace |
| `new` | string | **Yes** | - | Replacement content |
| `count` | int | No | `-1` | Replace count (-1 = all) |

**Return value**: Replaced text.

---

#### text_upper

Convert text to uppercase.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return value**: Uppercase text.

---

#### text_lower

Convert text to lowercase.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return value**: Lowercase text.

---

## 🔐 std.hash - Encryption and Encoding

Hash calculation and encoding tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`hash_md5`](#hash_md5) | MD5 hash | `text` |
| [`hash_sha256`](#hash_sha256) | SHA256 hash | `text` |
| [`base64_encode`](#base64_encode) | Base64 encode | `text` |
| [`base64_decode`](#base64_decode) | Base64 decode | `text` |

---

#### hash_md5

Calculate MD5 hash of text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return value**: 32-character MD5 hash string.

---

#### hash_sha256

Calculate SHA256 hash of text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return value**: 64-character SHA256 hash string.

---

#### base64_encode

Encode text to Base64 format.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return value**: Base64 encoded string.

---

#### base64_decode

Decode Base64 text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Base64 encoded text |

**Return value**: Decoded original text.

---

## 🔢 std.math - Math Operations

Math calculation tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`math_calc`](#math_calc) | Calculate math expression | `expression` |
| [`math_random`](#math_random) | Generate random number | `min_val`, `max_val` |

---

#### math_calc

Safely calculate math expression.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `expression` | string | **Yes** | - | Math expression |

**Return value**: JSON format `{ "result": number, "expression": string }`.

!!! warning "Safety Limit"
    Only numbers and `+-*/.()` characters are allowed; other characters are rejected.

---

#### math_random

Generate a random integer within specified range.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `min_val` | int | **Yes** | - | Minimum value |
| `max_val` | int | **Yes** | - | Maximum value |

**Return value**: Random integer.

---

## 🔍 std.regex - Regular Expressions

Regular expression matching and replacement.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`regex_match`](#regex_match) | Regex match | `pattern`, `text` |
| [`regex_replace`](#regex_replace) | Regex replace | `pattern`, `replacement`, `text` |

---

#### regex_match

Match text using regular expression.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `pattern` | string | **Yes** | - | Regex pattern |
| `text` | string | **Yes** | - | Text to match |
| `flags` | string | No | `""` | Flags: `i`(case-insensitive), `m`(multiline), `s`(singleline) |

**Return value**: JSON format `{ "matches": [string], "count": int }`.

---

#### regex_replace

Replace text using regular expression.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `pattern` | string | **Yes** | - | Regex pattern |
| `replacement` | string | **Yes** | - | Replacement content |
| `text` | string | **Yes** | - | Text to process |
| `flags` | string | No | `""` | Flags |

**Return value**: Replaced text.

---

## 💻 std.shell - Shell Commands

Execute system Shell commands.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`shell_exec`](#shell_exec) | Execute command | `command` |
| [`shell_which`](#shell_which) | Find command path | `command` |

---

#### shell_exec

Execute Shell command.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `command` | string | **Yes** | - | Command to execute |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return value**: JSON format `{ "stdout": string, "stderr": string, "returncode": int, "success": bool }`.

!!! warning "Security Warning"
    Shell command execution has potential risks. Ensure you don't execute dangerous commands, validate input parameters, and set reasonable timeouts.

---

#### shell_which

Find executable file path for a command.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `command` | string | **Yes** | - | Command name |

**Return value**: JSON format `{ "command": string, "path": string, "found": bool }`.

---

## 🙋 std.ask_human - Human Interaction

Human-in-the-Loop interaction tool.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`ask_human`](#ask_human) | Request user input | `prompt` |

---

#### ask_human

Request user input, implementing Human-in-the-Loop interaction.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `prompt` | string | **Yes** | - | Prompt message |
| `default` | string | No | `""` | Default value (used when user doesn't input) |

**Return value**: User input string.

**Example**:

```nexa
agent HumanInterface uses std.ask_human {
    role: "Human interaction assistant",
    prompt: "Interact with user for confirmation"
}

flow main {
    confirmation = HumanInterface.run("Please confirm whether to continue? [y/n]");
}
```

---

## 🗄️ std.db.sqlite - SQLite Operations (v1.3.5)

SQLite database operation toolset.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_db_sqlite_connect` | Connect to SQLite | `path` |
| `std_db_sqlite_query` | Query all rows | `handle_json`, `sql` |
| `std_db_sqlite_query_one` | Query single row | `handle_json`, `sql` |
| `std_db_sqlite_execute` | Execute write operation | `handle_json`, `sql` |
| `std_db_sqlite_close` | Close connection | `handle_json` |
| `std_db_sqlite_begin` | Begin transaction | `handle_json` |
| `std_db_sqlite_commit` | Commit transaction | `handle_json` |
| `std_db_sqlite_rollback` | Rollback transaction | `handle_json` |

**Usage Example**:

```nexa
db app_db = connect("sqlite://data.db")

flow main {
    result = DbAgent.run("Query all records from users table");
}
```

---

## 🗄️ std.db.postgres - PostgreSQL Operations (v1.3.5)

PostgreSQL database operation toolset.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_db_postgres_connect` | Connect to PostgreSQL | `url` |
| `std_db_postgres_query` | Query all rows | `handle_json`, `sql` |
| `std_db_postgres_query_one` | Query single row | `handle_json`, `sql` |
| `std_db_postgres_execute` | Execute write operation | `handle_json`, `sql` |
| `std_db_postgres_close` | Close connection | `handle_json` |
| `std_db_postgres_begin` | Begin transaction | `handle_json` |
| `std_db_postgres_commit` | Commit transaction | `handle_json` |
| `std_db_postgres_rollback` | Rollback transaction | `handle_json` |

---

## 🗄️ std.db.memory - Agent Memory Operations (v1.3.5)

Agent-specific memory database operations.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_db_memory_query` | Agent memory query | `handle_json`, `agent_name`, `key` |
| `std_db_memory_store` | Agent memory store | `handle_json`, `agent_name`, `key`, `value` |
| `std_db_memory_delete` | Agent memory delete | `handle_json`, `agent_name`, `key` |
| `std_db_memory_list` | Agent memory list | `handle_json`, `agent_name` |

---

## 🔐 std.auth - Authentication and OAuth (v1.3.6)

Three-layer authentication system: API Key + JWT (HS256) + OAuth 2.0 (PKCE flow).

### Tool List (17 tools)

| Tool | Description |
|-----|------|
| `std_auth_oauth` | OAuth authentication flow |
| `std_auth_enable_auth` | Enable authentication |
| `std_auth_get_user` | Get current user |
| `std_auth_get_session` | Get session info |
| `std_auth_session_data` | Get session data |
| `std_auth_set_session` | Set session data |
| `std_auth_logout_user` | User logout |
| `std_auth_require_auth` | Auth requirement middleware |
| `std_auth_jwt_sign` | JWT signing |
| `std_auth_jwt_verify` | JWT verification |
| `std_auth_jwt_decode` | JWT decoding |
| `std_auth_csrf_token` | CSRF token generation |
| `std_auth_csrf_field` | CSRF form field |
| `std_auth_verify_csrf` | CSRF verification |
| `std_auth_api_key_generate` | API Key generation (format: `nexa-ak-{random32hex}`) |
| `std_auth_api_key_verify` | API Key verification |
| `std_auth_auth_context` | Agent auth context |

**Usage Example**:

```nexa
auth myAuth = enable_auth("providers_json")

flow main {
    key = std.auth.api_key_generate("my_agent")
    // Format: nexa-ak-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
}
```

---

## 📦 std.kv - Key-Value Store (v1.3.6)

Built-in KV Store with SQLite backend, TTL support, and Agent semantic queries.

### Tool List (18 tools)

**General KV Operations (15)**:

| Tool | Description |
|-----|------|
| `std_kv_open` | Open KV Store |
| `std_kv_get` | Get value |
| `std_kv_get_int` | Get integer value |
| `std_kv_get_str` | Get string value |
| `std_kv_get_json` | Get JSON value |
| `std_kv_set` | Set value |
| `std_kv_set_nx` | Set only if not exists |
| `std_kv_del` | Delete key |
| `std_kv_has` | Check if key exists |
| `std_kv_list` | List all keys |
| `std_kv_expire` | Set TTL |
| `std_kv_ttl` | Get remaining TTL |
| `std_kv_flush` | Flush Store |
| `std_kv_incr` | Increment integer value |

**Agent-Native KV Operations (3)**:

| Tool | Description |
|-----|------|
| `std_kv_agent_kv_query` | Agent semantic query |
| `std_kv_agent_kv_store` | Agent memory store |
| `std_kv_agent_kv_context` | Agent context-aware retrieval |

**Usage Example**:

```nexa
kv myCache = open("sqlite://cache.db")

flow main {
    result = CacheAgent.run("Cache user preference data");
}
```

---

## ⚡ std.concurrent - Structured Concurrency (v1.3.6)

Structured concurrency module providing channel, spawn, parallel, race and 18 APIs.

### Tool List (18 tools)

| Tool | Description |
|-----|------|
| `std_concurrent_channel` | Create channel |
| `std_concurrent_send` | Send message |
| `std_concurrent_recv` | Receive message |
| `std_concurrent_recv_timeout` | Receive with timeout |
| `std_concurrent_try_recv` | Try receive |
| `std_concurrent_close` | Close channel |
| `std_concurrent_select` | Multi-channel select |
| `std_concurrent_spawn` | Spawn task |
| `std_concurrent_await_task` | Await task completion |
| `std_concurrent_try_await` | Try await |
| `std_concurrent_cancel_task` | Cancel task |
| `std_concurrent_parallel` | Parallel execution |
| `std_concurrent_race` | Race execution |
| `std_concurrent_after` | Delayed execution |
| `std_concurrent_schedule` | Periodic scheduling |
| `std_concurrent_cancel_schedule` | Cancel schedule |
| `std_concurrent_sleep_ms` | Millisecond sleep |
| `std_concurrent_thread_count` | Get thread count |

**Concurrency DSL Syntax**:

```nexa
concurrent_decl {
    spawn my_task { ... }
    parallel [task_a, task_b, task_c]
    race [fast_task, slow_task]
    channel ch = channel()
    after 500ms { cleanup() }
    schedule every 30s { health_check() }
}
```

---

## 📄 std.template - Template System (v1.3.6)

Template rendering engine supporting `template"""..."""` syntax, 30+ filters, and Agent template extensions.

### Tool List (18+ tools)

**Core Template Operations**:

| Tool | Description |
|-----|------|
| `std_template_render` | Render template string |
| `std_template_template` | Load external template file |
| `std_template_compile` | Compile template |
| `std_template_render_compiled` | Render compiled template |
| `std_template_filter_apply` | Apply filter chain |

**Agent-Native Template Operations**:

| Tool | Description |
|-----|------|
| `std_template_agent_prompt` | Agent prompt template |
| `std_template_agent_slot_fill` | Agent multi-source slot filling |
| `std_template_agent_register` | Register Agent template |
| `std_template_agent_list` | List Agent templates |

**Filter Tools**:

| Tool | Description |
|-----|------|
| `std_template_filter_upper` | To uppercase |
| `std_template_filter_lower` | To lowercase |
| `std_template_filter_capitalize` | Capitalize first letter |
| `std_template_filter_trim` | Trim whitespace |
| `std_template_filter_default` | Default value |
| `std_template_filter_length` | Length |
| `std_template_filter_json` | JSON serialization |
| `std_template_filter_truncate` | Truncate |
| `std_template_filter_replace` | Replace |
| `std_template_filter_escape` | HTML escape |
| `std_template_filter_date` | Date formatting |
| `std_template_filter_sort` | Sort |
| `std_template_filter_unique` | Unique values |
| `std_template_filter_number` | Number formatting |
| `std_template_filter_url_encode` | URL encoding |
| `std_template_filter_strip_tags` | Strip HTML tags |
| `std_template_filter_word_count` | Word count |
| `std_template_filter_line_count` | Line count |
| `std_template_filter_indent` | Indent |
| `std_template_filter_abs` | Absolute value |
| `std_template_filter_ceil` | Ceiling |
| `std_template_filter_floor` | Floor |

**Template DSL Syntax**:

```nexa
// Template strings
template"""Hello {{name | upper}}!"""
template"""{{#for item in items}}{{@index}}:{{item}}{{/for}}"""
template"""{{#if is_admin}}Admin{{#elif is_mod}}Mod{{#else}}User{{/if}}"""
template"""{{> card user_data}}"""
```

**30+ Filters**: upper/lower/capitalize/trim/truncate(n)/replace(from,to)/escape/raw/safe/default(val)/length/first/last/reverse/join(sep)/slice(start,end)/json/number(n)/url_encode/strip_tags/word_count/line_count/indent/date/sort/unique/abs/ceil/floor

**ForLoop Metadata**: `@index`, `@index1`, `@first`, `@last`, `@length`, `@even`, `@odd`

---

## 🔗 std.pipe - Pipe Operator (v1.3.x)

StdTool wrapper for the pipe operator `|>`.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_pipe_apply` | Pipe function application | `func`, `input` |

**Syntax**:

```nexa
// |> Pipe operator: left-to-right data flow
result |> format_output |> print
data |> std.text.upper
prompt |> agent.run |> extract_answer
```

---

## ⏳ std.defer - Deferred Execution (v1.3.x)

StdTool wrapper for defer statements, ensuring LIFO cleanup.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_defer_schedule` | Register deferred function | `func` |

**Syntax**:

```nexa
defer cleanup(db)
defer log("operation complete")
```

---

## ❓ std.null_coalesce - Null Coalescing (v1.3.x)

StdTool wrapper for the `??` operator.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_null_coalesce_apply` | Null coalescing | `left`, `right` |

**Syntax**:

```nexa
result ?? "fallback"
config.timeout ?? 30
agent.run(prompt) ?? "I couldn't process that"
```

---

## 📝 std.string - String Interpolation (v1.3.x)

StdTool wrapper for `#{expr}` string interpolation.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_string_interpolate` | String interpolation | `template`, `data` |

**Syntax**:

```nexa
"Hello #{name}, you are #{age} years old!"
"Status: #{result ?? 'pending'}"
"Agent #{agent.name} responding"
```

**Interpolation Expression Support**:

| Expression Type | Example | Python Translation |
|-----------|------|-------------|
| Simple identifier | `#{name}` | `name` |
| Dot access | `#{user.name}` | `user["name"]` |
| Bracket access | `#{arr[0]}` | `arr[0]` |
| Combined | `#{data.items[0].name}` | `data["items"][0]["name"]` |

**Type Conversion Rules**:

| Input Type | Output |
|---------|------|
| `None` | `""` (empty string) |
| `bool` | `"true"/"false"` |
| `int/float` | `str(value)` |
| `dict/list` | `json.dumps(value)` |
| `Option::Some` | unwrap inner value |
| `Option::None` | `""` |

---

## 🎯 std.match - Pattern Matching (v1.3.x)

StdTool wrapper for pattern matching and destructuring.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_match_pattern` | Pattern matching | `value`, `pattern` |
| `std_match_destructure` | Destructuring | `value`, `pattern` |
| `std_match_variant` | Construct variant | `enum_name`, `variant_name`, `value` |

**7 Pattern Types**:

1. **Wildcard**: `_` — matches anything
2. **Variable**: `name` — matches and binds variable
3. **Literal**: `42`, `"hello"`, `true`, `false` — matches exact value
4. **Tuple**: `(a, b)` — matches tuple/array
5. **Array**: `[a, b, ..rest]` — matches array + rest collector
6. **Map**: `{ name, age: a, ..other }` — matches dict + rest collector
7. **Variant**: `Option::Some(v)` — matches enum variant

---

## 🏗️ std.struct - Struct (v1.3.x)

StdTool wrapper for ADT struct.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_adt_register_struct` | Register struct | `name`, `fields` |
| `std_adt_make_struct` | Create struct instance | `name`, `values` |
| `std_adt_lookup` | Lookup struct | `name` |

**Syntax**:

```nexa
struct Point { x: Int, y: Int }
let p = Point(x: 1, y: 2)
```

**Handle-as-dict format**:

```json
{"_nexa_struct": "Point", "_nexa_struct_id": 1, "x": 1, "y": 2}
```

---

## 🏷️ std.enum - Enum (v1.3.x)

StdTool wrapper for ADT enum.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_adt_register_enum` | Register enum | `name`, `variants` |
| `std_adt_make_variant` | Create variant | `name`, `variant`, `value` |
| `std_adt_lookup` | Lookup enum | `name` |

**Syntax**:

```nexa
enum Option { Some(value), None }
enum Result { Ok(value), Err(error) }
let opt = Option::Some(42)
```

**Handle-as-dict format**:

```json
// Value variant
{"_nexa_variant": "Some", "_nexa_enum": "Option", "_nexa_variant_id": 1, "value": 42}
// Unit variant
{"_nexa_variant": "None", "_nexa_enum": "Option"}
```

---

## 🧬 std.trait - Trait and Impl (v1.3.x)

StdTool wrapper for ADT trait/impl.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| `std_adt_register_trait` | Register trait | `name`, `methods` |
| `std_adt_register_impl` | Register impl | `trait_name`, `type_name`, `methods` |
| `std_adt_lookup` | Lookup trait/impl | `name` |
| `std_adt_summary` | Get ADT overview | None |
| `std_adt_reset` | Reset all ADT registries | None |

**Syntax**:

```nexa
trait Printable { fn format() -> String }
impl Printable for Point { fn format() -> String { ... } }
```

---

## 🔧 Usage

### Declaring Usage Permissions

Use the `uses` keyword in Agent definitions:

```nexa
// Single namespace
agent MyAgent uses std.fs {
    prompt: "..."
}

// Multiple namespaces
agent MultiToolAgent uses std.fs, std.http, std.time {
    prompt: "..."
}

// New namespaces
agent DbAgent uses std.db.sqlite, std.db.memory {
    prompt: "..."
}

agent AuthAgent uses std.auth {
    prompt: "..."
}

agent CacheAgent uses std.kv {
    prompt: "..."
}

agent ConcurrentAgent uses std.concurrent {
    prompt: "..."
}

agent TemplateAgent uses std.template {
    prompt: "..."
}
```

### Runtime Invocation

Agents call tools via natural language instructions:

```nexa
agent Assistant uses std.fs, std.http {
    role: "Multi-purpose assistant",
    prompt: "Help users with file and network operations"
}

flow main {
    result = Assistant.run("Read /tmp/data.txt and POST to https://api.example.com/upload");
    print(result);
}
```

---

## 📚 Complete Examples

### Log Management Agent

```nexa
agent LogManager uses std.fs, std.time {
    role: "Log management expert",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a log management expert who can:
    - Read and analyze log files
    - Create and append log entries
    - Provide timestamp information
    """
}

flow main {
    task = """
    1. Get current timestamp
    2. Create log entry: [timestamp] System started
    3. Append to /var/log/nexa.log
    """;
    
    result = LogManager.run(task);
    print(result);
}
```

### API Data Fetching Agent

```nexa
agent DataFetcher uses std.http, std.json {
    role: "Data fetching expert",
    prompt: "Fetch data from API and parse JSON"
}

flow main {
    task = """
    1. GET https://api.example.com/users
    2. Parse the returned JSON
    3. Extract the name field of the first user
    """;
    
    name = DataFetcher.run(task);
    print(f"First user: {name}");
}
```

### Database + KV Cache Agent

```nexa
db app_db = connect("sqlite://data.db")
kv cache = open("sqlite://cache.db")

agent DbCacheAgent uses std.db.sqlite, std.kv {
    role: "Database cache assistant",
    prompt: "Query database and cache results"
}

flow main {
    result = DbCacheAgent.run("Query users table and cache popular users");
}
```

---

## 📊 Version History

| Version | Updates |
|-----|---------|
| v1.3.6 | Added `std.auth`, `std.kv`, `std.concurrent`, `std.template` namespaces |
| v1.3.5 | Added `std.db.sqlite`, `std.db.postgres`, `std.db.memory` namespaces |
| v1.3.x | Added `std.pipe`, `std.defer`, `std.null_coalesce`, `std.string`, `std.match`, `std.struct`, `std.enum`, `std.trait` namespaces |
| v1.0 | Added `std.text`, `std.hash`, `std.math`, `std.regex` namespaces |
| v0.9.7 | Added `std.shell`, `std.ask_human` namespaces |
| v0.7 | Initial stdlib release (`std.fs`, `std.http`, `std.time`) |

---

## 🔗 Related Resources

- [Language Reference Manual](reference.en.md)
- [CLI Reference](cli_reference.en.md)
- [Error Index](error_index.en.md)
- [Quickstart](quickstart.en.md)