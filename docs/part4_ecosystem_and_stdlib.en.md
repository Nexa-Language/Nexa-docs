---
title: "Standard library and MCP"
capabilities: [stdlib, mcp, tools]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Standard library and MCP

Built-in namespaces, custom `@tool` declarations, and MCP share exposure and approval boundaries. Preserve schemas, execution permissions, and outcome semantics when choosing an integration.

## Standard library

`src/runtime/stdlib.py` defines `STD_NAMESPACE_MAP` and tool schemas. Common groups include `std.fs`, `std.http`, `std.json`, `std.shell`, `std.db.sqlite`, `std.auth`, `std.kv`, `std.concurrent`, `std.template`, and `std.ui`. See [Standard library reference](stdlib_reference.md) for functions.

Packaged `stdlib/news.nx` is an includable Nexa module. Resolution follows [the unified compiler](part5_compiler.md).

## MCP connections

Install the official Python SDK extra in the Nexa checkout:

```sh
uv sync --locked --extra mcp
```

The current integration uses MCP Python SDK 2.3 and supports stdio and HTTP URLs supported by that SDK. SDK sessions handle discovery, pagination, and shutdown.

```python
from mcp import StdioServerParameters
from src.runtime.agent import NexaAgent
from src.runtime.mcp_client import MCPClient

with MCPClient(target=StdioServerParameters(command="python", args=["server.py"])) as client:
    agent = NexaAgent("Researcher", tools=client.get_tools_schema())
    state = agent.execute("Inspect available information")
```

This usage requires a real `server.py` and model configuration. Discovered remote tools require approval by default; server annotations do not authorize execution.

`fetch_mcp_tools()` accepts a single `mcpServers` configuration file. Legacy `tools` JSON retains schema loading with a deprecation warning. SDK/API execution closes sessions on exit. Unknown side effects after an MCP disconnect follow the [checkpoint contract](runtime_checkpoints.md).

---

[Source and validation](capability_inventory.md) · `stdlib` / `mcp` / `tools`
