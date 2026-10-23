---
title: "Get started with Nexa 2.4"
capabilities: [compilation, execution]
---

# Get started with Nexa 2.4

Run a program without a model, then compile an Agent. These pages use the released [Nexa v2.4.0](https://github.com/Nexa-Language/Nexa/releases/tag/v2.4.0).

## 1. Install the runtime

Use Git, Python 3.10+ and uv. Obtain the release source in your working directory and install its locked dependencies:

Release tag `v2.4.0` points to the verified [commit c216263](https://github.com/Nexa-Language/Nexa/commit/c2162637236e4a73feea410c4183672411666521).

```sh
git clone --branch v2.4.0 --depth 1 https://github.com/Nexa-Language/Nexa.git
cd Nexa
uv sync --locked
uv run nexa --version
```

Confirm the output is `Nexa v2.4.0`. Run the remaining commands from this source directory.

## 2. Run your first program

Save this as `hello.nx`. Compilation and execution need no credentials. The result is `12`.

```nexa
flow main {
    first = 3;
    print(first * 4);
    result = first * 4;
}
```

```sh
uv run nexa validate hello.nx --json
uv run nexa run hello.nx
```

`validate` returns structured diagnostics; `run` compiles and executes the program. `uv run nexa build hello.nx` writes the generated `hello.py` for inspection.

## 3. Define an Agent

Save this as `analyst.nx`. It is a complete declaration module and compiles without contacting a model.

```nexa
agent Analyst {
    prompt: "Work from evidence. State assumptions explicitly."
    timeout: 120
    max_tool_calls: 4
}
```

```sh
uv run nexa build analyst.nx
uv run nexa inspect analyst.nx --format json
```

Before execution, complete [First provider setup](part2_config_stdlib.md#first-provider-setup): create `secrets.nxs` with an endpoint and model ID, and supply a key through the environment or hidden input. See [Provider protocols](runtime_providers.md) for protocol choices. The next command uses the configured environment to make a model request and checkpoint the run in `.nexa/runs.sqlite3`.

```sh
uv run nexa agent analyst.nx Analyst "Explain the supplied evidence" --timeout 120
```

A successful run returns `status: completed`. Tools requiring approval return `waiting_approval`; follow [Approval and resume](runtime_approval.md). Diagnose other stops with [Execution and budgets](runtime_execution.md).

## 4. Continue building

- Read [Language basics](part1_basic.md) and [Tools and Protocols](part3_extensions.md).
- Save and recover tasks with [checkpoints](runtime_checkpoints.md).
- Use [the toolchain](toolchain.md) to work with Nexa Code or VS Code.
- Check the [2.4 migration checklist](migration_24.md) when upgrading.

---

[Source and validation](capability_inventory.md) · `compilation` / `execution`
