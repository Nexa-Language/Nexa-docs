---
title: "工具、Protocol 与 Python 扩展"
capabilities: [tools, types]
---

# 工具、Protocol 与 Python 扩展

用 `@tool` 声明参数与输出，用 `uses` 控制 Agent 的工具暴露集。`python!` 让受信任的本地代码参与工具实现。

## 完整工具程序

将下面的程序保存为 `calculator.nx`，配置模型后运行 `uv run nexa run calculator.nx`。Agent 可调用 `add(a=2, b=3)`；工具返回整数 `5`，模型再将结果组织为回复。

```nexa
@tool("Add two integers")
fn add(a: int, b: int): int {
    python! """return a + b"""
}
agent Calculator uses add { prompt: "Calculate with the supplied tool." }
flow main { result = Calculator.run("2 + 3"); }
```

工具参数由 schema 验证。未暴露工具、非法 JSON、类型不符和多余字段会被拒绝。对会写文件或请求外部系统的工具，按[审批指南](runtime_approval.md)声明风险，并处理[未知结果](runtime_checkpoints.md)。

## 结构化输出

下面的完整程序要求模型返回带整数 `value` 的对象，例如 `{"value": 42}`。返回值通过 Protocol 验证后可按字段访问。

```nexa
protocol Answer { value: int }
agent Reader implements Answer { prompt: "Return the answer as structured data." }
flow main { result = Reader.run("Return 42"); }
```

Protocol 输出、流式输出与缓存路径都接受运行时输出校验。结构符合 schema 后，业务上的正确性仍由明确的验证条件判断。

## 扩展边界

`python!` 执行受信任代码，遵循进程权限。`sandbox: true` 需要真实隔离后端；[Rust WASM](runtime_rust.md)有独立的模块执行范围。MCP 工具使用官方 SDK 会话，见[生态与标准库](part4_ecosystem_and_stdlib.md)。

---

[来源与验证](capability_inventory.md) · `tools` / `types`
