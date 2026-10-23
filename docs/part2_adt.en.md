---
title: "Algebraic data types"
capabilities: [types]
---

# Algebraic data types

`struct` describes named fields, `enum` describes variants, `trait` describes behavior interfaces, and `impl` implements an interface for a type. The Python path maintains runtime registries for these definitions.

## Complete declaration module

```nexa
struct Point { x: int, y: int }
enum Direction { North, South }
```

This module compiles independently. `src/runtime/adt.py` and `tests/test_adt.py` cover fields and variants. Prefer [Protocols](part3_extensions.md) for structured Agent output schemas; validate custom data types and model output contracts separately.

## Usage and migration

The runtime supports struct instances, field reads/updates, variant construction, and trait method lookup. Keep fields explicit and design interfaces around domain operations.

The historical `examples/v1.2/test_adt.nx` collection fails parsing at its construction syntax on line 60 and is listed as a historical draft. Validate and execute complete examples before adopting them.


## Declaration syntax and execution boundaries

| Declaration | Form |
| --- | --- |
| struct | `struct Point { x: int, y: int }` |
| enum | `enum Choice { Some(value), Empty }` |
| trait | `trait Printable { fn format() : String }` |
| impl | `impl Printable for Point { fn format() { "Point" } }` |

The parser and type registry support these declarations. In the current complete-program path, `Point(x: 2, y: 3)` raises `name 'Point' is not defined`; `Choice::Some(42)` reports a variant field-count mismatch. Both integration paths are recorded development-baseline limitations.

Use [Protocols](part3_extensions.md) for currently executable structured model output. Trusted Python tools can manage complex local data and expose explicit JSON Schemas to Agents. ADT construction will join executable tutorials when constructor/lowering end-to-end checks pass.

---

[Source and validation](capability_inventory.md) · `types`
