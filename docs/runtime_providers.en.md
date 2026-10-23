---
title: "Provider protocols and configuration"
capabilities: [providers, cache]
---

# Provider protocols and configuration

`provider_api` selects the message protocol. The Python reference runtime supports Chat Completions, Responses, and native Anthropic. Compilation needs no model credentials and makes no provider request. Importing compiler or runtime modules may initialize configuration objects and read local `.nxs` files. Start with [First provider setup](part2_config_stdlib.md#first-provider-setup).

| Value | Selection and credentials | Preserved session content |
| --- | --- | --- |
| `chat` | Default; existing `.nxs` and provider configuration | Chat messages, tool calls and results |
| `responses` | Explicit; existing OpenAI client configuration | Raw output items, encrypted reasoning, native tool results |
| `anthropic` | Explicit, or the `anthropic/` model prefix | Raw content blocks, thinking signatures, native tool_result blocks |

## Declare the protocol

This complete declaration module compiles offline. Execution also requires an available model and credentials.

```nexa
agent Analyst {
    prompt: "Analyze the supplied evidence."
    provider_api: "responses"
    timeout: 120
    max_tool_calls: 8
}
```

Set `model` in the declaration or use the effective configuration. `use config name;` selects an existing configuration; see [Configuration](part2_config_stdlib.md). Supply credentials through the local environment or existing `.nxs` configuration, keeping them out of `.nx` files and version control.

For native Anthropic, install the extra in your Nexa checkout and set `ANTHROPIC_API_KEY` in the execution environment. `ANTHROPIC_BASE_URL` optionally selects the endpoint.

```sh
uv sync --locked --extra anthropic
```

## Completion and failure

Streaming, non-streaming, Protocol output, and cache hits share output validation and completion handling. Truncation, refusal, or a stream without a completion event fails the run. Opaque provider items needed for continuation are checkpointed and restored with their original protocol.

## Exact response cache

Caching applies to **fresh Chat runs without tools**. The key includes effective context, system instructions, model, endpoint, and output contract. Context limits are checked before a hit is accepted. Responses and Anthropic responses are currently uncached. Manage conversation history, provider state, and caches as separate resources.

Cache effectiveness depends on the workload. Offline fixtures check key isolation, output validation, and skipped requests. Measure model quality, cost, and latency separately with a selected provider and budget.

Continue with [Execution and budgets](runtime_execution.md) and [Context structure](part2_context_structure.md).

---

[Source and validation](capability_inventory.md) · `providers` / `cache`
