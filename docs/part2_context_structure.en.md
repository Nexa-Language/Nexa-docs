---
title: "Structured context"
capabilities: [context, providers]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Structured context

An Agent's `context` declaration defines context source, sink, schemas, and inherited fields. Pipelines whose endpoints both declare context transfer `AgentContext`. Python applications can also call `agent.run(previous.last_context())` explicitly.

## Complete declarations

This module declares upstream and downstream Agents and compiles without a model.

```nexa
protocol Findings { summary: string }
agent Researcher {
    prompt: "Extract the facts."
    context {
        source: upstream,
        sink: downstream,
        output_schema: Findings,
        inherit: [messages]
    }
}
agent Writer {
    prompt: "Write from the facts."
    context {
        source: upstream,
        sink: downstream,
        input_schema: Findings,
        inherit: [messages, artifacts]
    }
}
```

| Field | Purpose |
| --- | --- |
| `source` / `sink` | Select upstream input and downstream output behavior |
| `input_schema` / `output_schema` | Declare context contracts, compared by nominal name equality |
| `inherit` | Select inherited message or artifact fields |
| `max_history_turns` | Bound retained conversation turns |

`shared:name` shares deep-copied snapshots within one flow; `discard` creates no downstream context. Different schema names require explicit conversion even if their fields resemble each other.

## Context budget

Context limits currently use serialized UTF-8 byte size as a conservative token upper bound. Provider usage is accounted separately. Chat trimming keeps complete user turns and preserves tool-call/result pairs. A newest turn that exceeds the limit fails.

Native Responses/Anthropic retain opaque items. When their history or context exceeds a limit, shorten input to preserve protocol state. See [Provider protocols](runtime_providers.md).

---

[Source and validation](capability_inventory.md) · `context` / `providers`
