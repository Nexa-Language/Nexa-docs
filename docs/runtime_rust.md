---
title: "Rust AVM 与 WASM 支持范围"
capabilities: [rust]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# Rust AVM 与 WASM 支持范围

Python 编译器与运行时是 Nexa 2.4 的参考实现。Rust AVM 通过共同语义 fixture 扩展覆盖范围，当前支持以下子集。

| 路径 | 当前行为 |
| --- | --- |
| Rust 编译与解释 | 声明初始化、整数与浮点算术、局部和全局变量、跳转、返回、Agent 调用 |
| Provider 边界 | `Interpreter::set_agent_executor`；CLI 文本 provider 使用 `NEXA_API_KEY`、可选 `NEXA_BASE_URL`，请求超时 30 秒 |
| 工具、结构化输出、完整 Harness | 使用 Python 参考运行时 |
| 未实现 opcode 或调用 | 显式错误 |

Rust 编译器遇到工具声明时会返回 `Tool … requires the Python runtime`；包含工具的程序请使用 Python 后端。

## 共同语义

`tests/fixtures/conformance/programs.json` 由 Python 和 Rust 测试共同消费，覆盖整数精度、除法、变量和 Agent 调用。下面的完整程序属于共同语义路径，离线结果为 `2.5`。

```nexa
flow main {
    result = 5 / 2;
}
```

从 Nexa checkout 运行 Rust 检查：

```sh
cargo test --manifest-path avm/Cargo.toml
```

## WASM 执行器

WASM 使用 Wasmtime 48 LTS。启用 `wasm` feature 后执行真实模块，支持标量参数、实例状态保留、内存上限、fuel 与 epoch 中断；未启用时返回明确错误。

```sh
cargo test --manifest-path avm/Cargo.toml --features wasm
```

WASI imports 和引用类型参数尚未接入。WASM 模块的隔离能力与普通 Python 工具的执行方式应分别配置；为 Python 工具声明 `sandbox: true` 仍需要实际隔离后端。

## 评测边界

共同 fixture 检查指定程序的语义。真实模型质量、成本和延迟需要可复现的 provider、模型、输入、预算与测量环境。历史架构讨论保留在[架构演进](part5_architecture_evolution.md)，本站不展示未经当前基线复测的倍数指标。

---

[来源与验证](capability_inventory.md) · `rust`
