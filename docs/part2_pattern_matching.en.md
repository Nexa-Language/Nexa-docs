---
title: "Pattern matching"
capabilities: [language, patterns]
language_versions: ["2.4"]
---

!!! note "2.4 compatibility in Nexa 3.0"
    This page describes the retained 2.4 language/runtime path. Sources without a version declaration use this path. Start new Open Programs with [Nexa 3.0](quickstart.md); compare contracts in the [migration guide](migration_30.md).

# Pattern matching

`match` evaluates data patterns in branch order. Literals match discrete values, bound variables capture values, and `_` provides a fallback. More complex patterns cover tuples, arrays, maps, and enum variants.

## Complete matching program

```nexa
flow main {
    value = 1;
    result = match value {
        0 => "zero",
        1 => "one",
        _ => "other"
    }
}
```

The offline run returns `one`. Put specific branches before broad ones. Guards add conditions to matched values; keep guard expressions deterministic and free of side effects.

## Data patterns and intent routing

Data patterns check actual structure and values. Semantic intent routing requires model inference, so compile validity and routing quality have separate checks. Define explicit categories and a fallback for model-based routing.

The runtime manifest classifies the historical `examples/v1.2/test_match.nx` collection as a draft. Use the standalone complete example above. Runtime and parser cases are in `tests/test_pattern_matching.py`.


## Destructuring

`let` binds elements of an existing collection. This complete program returns `5`.

```nexa
flow main {
    python! """items = [2, 3]"""
    let [a, b] = items;
    result = a + b;
}
```

Pattern forms include `(a, b)` for tuples, `[first..rest]` for an array remainder, `{name, age: years}` for map fields, and `Type::Variant(value)` for enum variants. Parser/runtime tests cover these forms individually; see [ADT](part2_adt.md) for current enum-construction integration limits.

---

[Source and validation](capability_inventory.md) · `language` / `patterns`
