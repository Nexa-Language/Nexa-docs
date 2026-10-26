---
title: "Terminal UI"
capabilities: [terminal, stdlib]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Terminal UI

`std.ui` provides Markdown, code blocks, panels, status messages, and interactive input for Nexa programs. Rendering uses `rich`; input uses `prompt_toolkit`.

## Installation and complete example

Install the optional dependencies in your Nexa checkout:

```sh
uv sync --locked --extra terminal
```

This complete program compiles and displays messages in a terminal without a model request.

```nexa
flow main {
    std.ui.banner("Nexa", "Development workspace");
    std.ui.markdown("# Ready\nInspect the source before execution.");
    std.ui.success("Program loaded");
}
```

| Function | Purpose |
| --- | --- |
| `banner(title, subtitle)` | Application heading |
| `markdown(text)` / `code(code, language)` | Formatted text and code |
| `panel(text, title, style)` | Grouped panel |
| `thinking(message, duration)` | Timed waiting indicator |
| `success` / `error` / `warning` / `info` | Status messages |
| `input(prompt)` | Interactive input |
| `agent_reply(name, reply)` / `tool_call(name, args)` | Agent and tool information |

These names belong to the `std.ui` namespace. CJK input behavior depends on the terminal environment; test input, backspace, and cancellation on target terminals when releasing an application. Nexa Code's Ink interface is a separate part of the [toolchain](toolchain.md).

---

[Source and validation](capability_inventory.md) · `terminal` / `stdlib`
