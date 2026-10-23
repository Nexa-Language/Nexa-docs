---
title: "代数数据类型"
capabilities: [types]
---

# 代数数据类型

`struct` 描述命名字段，`enum` 描述变体，`trait` 描述行为接口，`impl` 为类型实现接口。当前 Python 路径维护类型与实现的运行时注册表。

## 完整声明模块

```nexa
struct Point { x: int, y: int }
enum Direction { North, South }
```

这个模块独立编译。字段结构和变体语义由 `src/runtime/adt.py` 与 `tests/test_adt.py` 核验。协议化 Agent 输出优先使用 [Protocol](part3_extensions.md) 表达 schema；自定义数据结构与模型输出契约分别验证。

## 使用与迁移

运行时提供结构实例、字段读取/更新、变体构造和 trait 方法查找。设计数据类型时保留显式字段，围绕业务操作建立接口。

旧综合示例 `examples/v1.2/test_adt.nx` 的第 60 行构造语法在当前 parser 中失败，已列为 historical draft。采用完整示例前先通过 `nexa validate` 和实际执行验收。


## 声明语法与运行边界

| 声明 | 写法 |
| --- | --- |
| struct | `struct Point { x: int, y: int }` |
| enum | `enum Choice { Some(value), Empty }` |
| trait | `trait Printable { fn format() : String }` |
| impl | `impl Printable for Point { fn format() { "Point" } }` |

上述形式由 parser 与类型注册表支持。当前完整程序中的 `Point(x: 2, y: 3)` 会在运行时报告 `name 'Point' is not defined`；`Choice::Some(42)` 报告变体字段数量不符。这两个集成路径已记录为开发基线限制。

需要当前可用的结构化模型输出时，使用 [Protocol](part3_extensions.md)。本地复杂数据可由受信任的 Python 工具管理，并以明确的 JSON Schema 暴露给 Agent。待构造与生成物的端到端用例通过后，再把 ADT 构造列入可执行教程。

---

[来源与验证](capability_inventory.md) · `types`
