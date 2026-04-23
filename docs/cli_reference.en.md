---
comments: true
---

# Nexa CLI Command Reference

This document details all commands, parameters, and usage examples for the Nexa command-line tool. All commands strictly match the source code in `src/cli.py`.

---

## 📖 Overview

Nexa CLI is the command-line interface for the Nexa language, providing compilation, execution, testing, inspection, linting, intent verification, HTTP serving, and background job management.

### Command Overview

| Command | Description | Version |
|---------|-------------|---------|
| `nexa build` | Compile .nx file to .py | v0.9.7+ |
| `nexa run` | Compile and execute .nx file | v0.9.7+ |
| `nexa test` | Compile and run tests | v0.9.7+ |
| `nexa inspect` | Structural analysis (Agent-Native Tooling) | v1.3.0 |
| `nexa validate` | Semantic validation | v1.3.0 |
| `nexa lint` | Type system lint (Gradual Type System) | v1.3.1 |
| `nexa intent check` | IDD intent check | v1.1.0 |
| `nexa intent coverage` | IDD intent coverage | v1.1.0 |
| `nexa serve` | Start HTTP Server | v1.3.4 |
| `nexa routes` | List HTTP routes | v1.3.4 |
| `nexa jobs` | Background job management | v1.3.3 |
| `nexa workers` | Worker management | v1.3.3 |
| `nexa cache clear` | Clear cache | v0.9.7+ |

### Installation Verification

```bash
# Check installed version
nexa --version

# View help information
nexa --help
```

!!! tip "Version Display"
    The `--version` flag displays the currently installed Nexa version. The current feature set covers v1.1–v1.3.x.

---

## 1. Core Commands

### 1.1 `nexa build` - Compile Program

Compile Nexa code to Python code without execution.

**Syntax**:

```bash
nexa build <FILE>
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to compile | Required |

**Examples**:

```bash
# Compile to Python
nexa build main.nx

# Compile a specific file
nexa build examples/01_hello_world.nx
```

**Output Description**:

```
🔨 Compiling main.nx ...
✨ Success! Built target: main.py
```

The compilation artifact is a `.py` file in the same directory (e.g., `main.nx` → `main.py`).

!!! note "include Support"
    The `build` command supports `include` statements, which merge other .nx files' content into the current file's AST at the top.

---

### 1.2 `nexa run` - Run Program

Compile and execute a Nexa program.

**Syntax**:

```bash
nexa run <FILE>
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to run | Required |

**Examples**:

```bash
# Basic run
nexa run main.nx

# Run an example file
nexa run examples/01_hello_world.nx
```

**Output Description**:

```
🔨 Compiling main.nx ...
✨ Success! Built target: main.py
🚀 Running main.py ...
==================================================
[INFO] Agent 'Analyst' started
[RESULT] Execution result...
==================================================
✅ Execution Finished (Exit code: 0)
```

!!! warning "Interrupting Execution"
    Press `Ctrl+C` during execution to interrupt. Output: `⚠️ Execution interrupted by user.` with exit code 130.

---

### 1.3 `nexa test` - Run Tests

Compile a .nx file and execute all `test_` prefixed test functions.

**Syntax**:

```bash
nexa test <FILE>
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to test | Required |

**Examples**:

```bash
# Run tests
nexa test main.nx
```

**Output Description**:

```
🔨 Compiling main.nx ...
✨ Success! Built target: main.py
🧪 Testing main.nx ...
==================================================
[PASS] test_basic_pipeline
[PASS] test_intent_routing
[FAIL] test_edge_case
      AssertionError: Output not as expected
==================================================
💥 1 failed, 2 passed.
```

---

## 2. Agent-Native Tooling Commands (v1.3.0)

### 2.1 `nexa inspect` - Structural Analysis

Perform structural analysis on a .nx file, outputting descriptions of Agents, Tools, Flows, etc.

**Syntax**:

```bash
nexa inspect <FILE> [--format json|text]
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to inspect | Required |
| `--format` | Output format: `json` or `text` | `json` |

**Examples**:

```bash
# JSON format output
nexa inspect main.nx --format json

# Text format output
nexa inspect main.nx --format text
```

---

### 2.2 `nexa validate` - Semantic Validation

Perform semantic validation on a .nx file, checking for syntax and semantic errors.

**Syntax**:

```bash
nexa validate <FILE> [--json] [--quiet]
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to validate | Required |
| `--json` | JSON format output | `false` |
| `--quiet` | Quiet mode, only output errors | `false` |

**Examples**:

```bash
# Basic validation
nexa validate main.nx

# JSON format output
nexa validate main.nx --json

# Quiet mode
nexa validate main.nx --quiet
```

!!! warning "Exit Code"
    Exit code is 1 when validation fails, useful for CI/CD pipelines.

---

### 2.3 `nexa lint` - Type System Lint (v1.3.1)

Run the gradual type system linter on a .nx file.

**Syntax**:

```bash
nexa lint <FILE> [--strict] [--warn-untyped]
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to lint | Required |
| `--strict` | Strict mode: missing type annotations = lint error | `false` |
| `--warn-untyped` | Warn mode: warn about missing type annotations | `false` |

**Examples**:

```bash
# Default lint (only check code with type annotations)
nexa lint app.nx

# Strict mode
nexa lint app.nx --strict

# Warn about untyped code
nexa lint app.nx --warn-untyped
```

!!! tip "Lint Mode Explanation"
    - **Default mode**: Only check code that has type annotations
    - **`--warn-untyped`**: Warn about missing type annotations
    - **`--strict`**: Missing type annotations treated as lint errors (non-zero exit code)

    Lint mode can also be set via `NEXA_LINT_MODE` environment variable or `nexa.toml` configuration file.

---

## 3. IDD Intent-Driven Development Commands (v1.1.0)

### 3.1 `nexa intent check` - Intent Check

Verify that code conforms to intent specifications defined in `.nxintent` files.

**Syntax**:

```bash
nexa intent check <FILE> [--intent <INTENT_FILE>] [--verbose]
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to check | Required |
| `--intent` | Specify .nxintent file path | Auto-discover |
| `--verbose` | Show verbose output | `false` |

**Examples**:

```bash
# Basic intent check
nexa intent check main.nx

# Specify intent file
nexa intent check main.nx --intent intents/main.nxintent

# Verbose output
nexa intent check main.nx --verbose
```

!!! warning "Exit Code"
    Exit code is 1 when all intent checks fail.

---

### 3.2 `nexa intent coverage` - Intent Coverage

Display intent coverage report for the code.

**Syntax**:

```bash
nexa intent coverage <FILE> [--intent <INTENT_FILE>]
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx source file to check | Required |
| `--intent` | Specify .nxintent file path | Auto-discover |

**Examples**:

```bash
# View coverage
nexa intent coverage main.nx

# Specify intent file
nexa intent coverage main.nx --intent intents/main.nxintent
```

!!! tip "Improving Coverage"
    When coverage is below 100%, the system suggests adding `@implements` annotations to increase coverage.

---

## 4. HTTP Server Commands (v1.3.4)

### 4.1 `nexa serve` - Start HTTP Server

Compile a .nx file and start the built-in HTTP server.

**Syntax**:

```bash
nexa serve <FILE> [--port <PORT>]
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx file with server declarations | Required |
| `--port` | Specify server port | Value declared in file |

**Examples**:

```bash
# Start HTTP Server
nexa serve web_app.nx

# Specify port
nexa serve web_app.nx --port 3000
```

!!! note "server DSL"
    Use the `server` DSL in .nx files to define HTTP servers:
    ```nexa
    server 8080 {
        static "/assets" from "./public"
        cors { origins: ["*"], methods: ["GET", "POST"] }
        route GET "/chat" => ChatBot
        route POST "/analyze" => DataExtractor |>> Analyzer
    }
    ```

---

### 4.2 `nexa routes` - List Routes

Parse a .nx file and list all HTTP routes.

**Syntax**:

```bash
nexa routes <FILE> [--json]
```

**Parameters**:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILE` | Path to the .nx file with server declarations | Required |
| `--json` | JSON format output | `false` |

**Examples**:

```bash
# List routes
nexa routes web_app.nx

# JSON format output
nexa routes web_app.nx --json
```

---

## 5. Background Job Management Commands (v1.3.3)

### 5.1 `nexa jobs` - Job Management

Manage background jobs in the Job system.

**Subcommands**:

| Subcommand | Parameters | Description |
|------------|------------|-------------|
| `list` | `[--status <STATUS>]` | List all jobs, optionally filter by status |
| `status` | `<JOB_ID>` | View status of a specific job |
| `cancel` | `<JOB_ID>` | Cancel a specific job |
| `retry` | `<JOB_ID>` | Retry a dead letter job |
| `clear` | - | Clear completed/expired/cancelled jobs |

**Status filter options** (`--status`):

`pending`, `running`, `completed`, `failed`, `dead`, `cancelled`, `expired`

**Examples**:

```bash
# List all jobs
nexa jobs list

# List only failed jobs
nexa jobs list --status failed

# View job status
nexa jobs status job_123

# Cancel a job
nexa jobs cancel job_123

# Retry a dead letter job
nexa jobs retry job_456

# Clear completed jobs
nexa jobs clear
```

---

### 5.2 `nexa workers` - Worker Management

Manage background Job Workers.

**Subcommands**:

| Subcommand | Parameters | Description |
|------------|------------|-------------|
| `start` | `<FILE>` | Start a worker (requires compiling .nx file with job definitions) |
| `status` | - | View worker and queue status |

**Examples**:

```bash
# Start a worker
nexa workers start jobs_app.nx

# View worker status
nexa workers status
```

!!! note "job DSL"
    Use the `job` DSL in .nx files to define background jobs:
    ```nexa
    job SendEmail on "emails" (retry: 2, timeout: 120) {
        perform(user_id) { ... }
        on_failure(error, attempt) { ... }
    }
    ```

---

## 6. Cache Management Commands

### 6.1 `nexa cache clear` - Clear Cache

Clear the `.nexa_cache/` cache directory.

**Syntax**:

```bash
nexa cache clear
```

**Examples**:

```bash
nexa cache clear
# Output: ✅ Cache cleared successfully.
```

!!! tip "Cache Information"
    If the cache directory doesn't exist, output: `ℹ️ No cache directory found.`

---

## 7. Global Options

| Option | Description |
|--------|-------------|
| `--version` / `-v` | Display version number and exit |
| `--help` | Display help information |

---

## 8. Environment Variables

Nexa CLI supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXA_TYPE_MODE` | Runtime type checking mode (`strict`, `warn`, `forgiving`) | `warn` |
| `NEXA_LINT_MODE` | Lint type checking mode (`default`, `warn`, `strict`) | `default` |
| `NEXA_PORT` | HTTP Server port override | Value declared in file |
| `PYTHONPATH` | Python module search path | Auto-set |

!!! tip "Type Mode Priority"
    `NEXA_TYPE_MODE` priority: CLI flag > Environment variable > `nexa.toml` config > Default (`warn`)

---

## 9. Exit Codes

| Exit Code | Description |
|------------|-------------|
| `0` | Success |
| `1` | General error / Validation failed / Intent check failed |
| `130` | User interrupt (Ctrl+C) |

---

## 🔗 Related Resources

- [Language Reference Manual](reference.en.md)
- [Stdlib API](stdlib_reference.en.md)
- [Troubleshooting Guide](troubleshooting.en.md)
- [Quickstart](quickstart.en.md)