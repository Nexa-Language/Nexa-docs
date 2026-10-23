---
title: "Tools, Protocols, and Python extensions"
capabilities: [tools, types]
---

# Tools, Protocols, and Python extensions

Use `@tool` to declare arguments and output, and `uses` to select exposed tools. `python!` embeds trusted local code in a tool implementation.

## Complete tool program

Save this as `calculator.nx`, configure a model, and run `uv run nexa run calculator.nx`. The Agent can call `add(a=2, b=3)`; the tool returns integer `5`, which the model uses in its reply.

```nexa
@tool("Add two integers")
fn add(a: int, b: int): int {
    python! """return a + b"""
}
agent Calculator uses add { prompt: "Calculate with the supplied tool." }
flow main { result = Calculator.run("2 + 3"); }
```

Schemas validate tool arguments. Unexposed tools, malformed JSON, wrong types, and extra fields are rejected. For tools writing files or contacting services, declare risk with the [approval guide](runtime_approval.md) and handle [unknown outcomes](runtime_checkpoints.md).

## Structured output

This complete program asks for an object with an integer `value`, such as `{"value": 42}`. Once validated against the Protocol, the result is available by field.

```nexa
protocol Answer { value: int }
agent Reader implements Answer { prompt: "Return the answer as structured data." }
flow main { result = Reader.run("Return 42"); }
```

Protocol, streaming, and cached outputs all pass through runtime output validation. Task-specific correctness needs explicit acceptance conditions after schema validation.

## Extension boundary

`python!` executes trusted code with process permissions. `sandbox: true` requires a real isolation backend. [Rust WASM](runtime_rust.md) has its own module execution scope. MCP tools use official SDK sessions; see [Ecosystem and standard library](part4_ecosystem_and_stdlib.md).

---

[Source and validation](capability_inventory.md) · `tools` / `types`
