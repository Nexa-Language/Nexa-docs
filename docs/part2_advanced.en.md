---
title: "Pipelines and parallel orchestration"
capabilities: [language, harness, context]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Pipelines and parallel orchestration

Choose topology from data dependencies, then set budgets. Sequential pipelines pass one step's output to the next; parallel branches use isolated Agent sessions.

## Sequential pipelines

Configure a model, save this as `pipeline.nx`, and run `uv run nexa run pipeline.nx`. Researcher extracts facts; Summarizer receives those facts and returns a summary.

```nexa
agent Researcher { prompt: "Extract the facts." }
agent Summarizer { prompt: "Summarize the facts." }
flow main {
    result = "evidence" >> Researcher >> Summarizer;
}
```

Each stage receives the previous result. When both endpoints declare context, the pipeline transfers [AgentContext](part2_context_structure.md). Explicit calls such as `facts = Researcher.run("evidence"); result = Summarizer.run(facts);` are useful when you need to inspect an intermediate value.

## fork/merge

The following program explores two approaches in parallel and requires model configuration.

```nexa
agent Explorer { prompt: "Explore one approach." }
flow main {
    fork [Explorer.run("Approach A"), Explorer.run("Approach B")] merge all;
}
```

Concurrency defaults to a bound of 8 and results preserve input order. `all` collects results; `first` and `vote` select according to their strategies. `best`/`best_of` require a numeric `score` in each result and fail when it is absent. Completion order is distinct from input order.

## Repeated messages

Use an [Actor](runtime_actors.md) to send successive messages to one worker. Use [execute and checkpoints](runtime_checkpoints.md) for cross-process approval persistence.

---

[Source and validation](capability_inventory.md) · `language` / `harness` / `context`
