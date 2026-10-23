---
title: "标准库与 MCP"
capabilities: [stdlib, mcp, tools]
---

# 标准库与 MCP

内置 namespace、自定义 `@tool` 与 MCP 都进入工具暴露和审批边界。选择接入方式时，保留 schema、执行权限和结果语义。

## 标准库

`src/runtime/stdlib.py` 定义 `STD_NAMESPACE_MAP` 与工具 schema。常见分组包括 `std.fs`、`std.http`、`std.json`、`std.shell`、`std.db.sqlite`、`std.auth`、`std.kv`、`std.concurrent`、`std.template` 和 `std.ui`。具体函数见[标准库参考](stdlib_reference.md)。

包内 `stdlib/news.nx` 是可 include 的 Nexa 源模块。include 解析遵循[统一编译入口](part5_compiler.md)。

## MCP 连接

在 Nexa checkout 安装官方 Python SDK extra：

```sh
uv sync --locked --extra mcp
```

当前使用 MCP Python SDK 2.3，支持 stdio 与 SDK 支持的 HTTP URL。SDK 会话负责协议发现、分页和关闭。

```python
from mcp import StdioServerParameters
from src.runtime.agent import NexaAgent
from src.runtime.mcp_client import MCPClient

with MCPClient(target=StdioServerParameters(command="python", args=["server.py"])) as client:
    agent = NexaAgent("Researcher", tools=client.get_tools_schema())
    state = agent.execute("Inspect available information")
```

此用法需要实际的 `server.py` 和模型配置。发现的远程工具默认要求审批，服务端注解不会自动授予执行权限。

`fetch_mcp_tools()` 兼容单个 `mcpServers` 配置文件。旧 `tools` JSON 保留 schema 读取并提示弃用。SDK/API 在执行结束时关闭会话；MCP 断连造成未知副作用时遵循[checkpoint 契约](runtime_checkpoints.md)。

---

[来源与验证](capability_inventory.md) · `stdlib` / `mcp` / `tools`
