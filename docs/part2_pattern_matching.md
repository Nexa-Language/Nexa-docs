---
title: "模式匹配"
capabilities: [language, patterns]
---

# 模式匹配

`match` 按分支顺序匹配数据。字面量适合离散值，绑定变量与 `_` 提供捕获与兜底；复杂模式包括元组、数组、映射与 enum 变体。

## 完整匹配程序

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

本例在离线运行中返回 `one`。优先将具体分支放前，通用分支放后。Guard 用于对已匹配的值追加条件；其表达式应保持确定、无副作用。

## 数据模式与意图路由

数据模式匹配检查实际结构和值。`match` 的语义意图路由需要模型推理，相关语法编译与实际路由质量分开验证。模型输入应有明确分类集合和兜底路径。

历史综合示例 `examples/v1.2/test_match.nx` 已在主仓库 manifest 标记为 draft；使用上面的独立完整示例。详细运行和 parser 用例见 `tests/test_pattern_matching.py`。


## 解构

`let` 从已有集合中绑定元素。下面的完整程序返回 `5`。

```nexa
flow main {
    python! """items = [2, 3]"""
    let [a, b] = items;
    result = a + b;
}
```

模式写法：`(a, b)` 匹配元组，`[first..rest]` 捕获数组余项，`{name, age: years}` 绑定映射字段，`Type::Variant(value)` 描述 enum 变体。各模式的 parser/运行时测试单独存在；当前 enum 构造的集成限制见[ADT](part2_adt.md)。

---

[来源与验证](capability_inventory.md) · `language` / `patterns`
