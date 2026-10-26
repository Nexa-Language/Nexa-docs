---
title: "Configuration and standard library entry"
capabilities: [configuration, stdlib]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Configuration and standard library entry

Configuration covers three separate boundaries: models/credentials, compiler diagnostics, and execution budgets. Configure each explicitly for reproducibility and diagnosis.

## First provider setup {#first-provider-setup}

This setup targets a provider with an OpenAI-compatible Chat API. For Responses, also confirm that the provider supports that protocol. Create `secrets.nxs` in the working directory containing `analyst.nx`:

```text
config default {
    BASE_URL = "https://your-provider.example/v1",
    MODEL_NAME = {
        "strong": "openai/YOUR_MODEL_ID",
        "weak": "openai/YOUR_MODEL_ID",
        "super": "openai/YOUR_MODEL_ID"
    }
}
```

Replace `BASE_URL` with your provider's API root and all three `YOUR_MODEL_ID` placeholders with a model ID you can access. All tiers can initially use the same model. An Agent without an explicit `model` uses `strong`. The `openai/` prefix selects Nexa's provider configuration and is removed before sending the model ID.

Prefer injecting `API_KEY` through your existing secret manager, or use `OPENAI_API_KEY` with the `openai/...` configuration above. The file deliberately omits an `API_KEY` field. Explicit credentials in existing `.nxs` files may take precedence over environment values, so also check parent-directory configuration. Keep keys in the execution environment, outside `.nx` files, logs, and Git.

If environment injection is not available yet, run the following in a local interactive terminal. It hides the key input, passes it only to the child process, and runs `analyst.nx` from [Quickstart](quickstart_24.md). This step makes a real model request; replace the endpoint and model placeholders first.

```sh
uv run python - <<'PY'
import getpass
import os
import subprocess

environment = os.environ.copy()
environment["API_KEY"] = getpass.getpass("Provider API key: ")
command = ["nexa", "agent", "analyst.nx", "Analyst",
           "Explain the supplied evidence", "--timeout", "120"]
raise SystemExit(subprocess.run(command, env=environment).returncode)
PY
```

With secret-manager injection already configured, run `uv run nexa agent analyst.nx Analyst "Explain the supplied evidence" --timeout 120` directly. To check the program only, use `uv run nexa validate analyst.nx --json`; it needs no key and makes no provider request.

## Select a named configuration

`.nxs` also supports flat configuration and named `config` blocks. Rename `default` to `development` in the example above to create the configuration selected by this declaration. `use config name;` selects an existing block:

```nexa
use config development;
agent Analyst {
    prompt: "Analyze supplied evidence."
}
```

`.nxs` discovery walks upward from the working or declaring script directory, up to 10 levels. Parent configuration loads first; the nearest directory wins for matching names. Configuration files load during module initialization and script loading; provider clients are created at the first model call. Chat/Responses use existing provider configuration. Native Anthropic uses `ANTHROPIC_API_KEY` and optional `ANTHROPIC_BASE_URL`. Keep credentials out of logs and Git.

## Tool exposure

Namespaces such as `uses std.fs` and `uses std.shell` expand into standard-library tool sets. Expose the smallest set needed for the task. Registration and exposure to an Agent are separate steps. Declare custom tools with the [tool guide](part3_extensions.md).

## Diagnostics and budgets

- `--harness strict|warn|off` controls Harness compiler diagnostics.
- `nexa lint` runs gradual type checks; `--strict` makes missing annotations errors.
- `RunConfig` enforces model, tool, token, and time budgets; see [Execution](runtime_execution.md).

Find tool signatures in [Standard library API](stdlib_reference.md). Terminal UI requires the optional `terminal` extra; MCP requires the `mcp` extra.

---

[Source and validation](capability_inventory.md) · `configuration` / `stdlib`
