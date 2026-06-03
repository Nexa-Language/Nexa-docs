---
comments: true
---

# 模式匹配 (Pattern Matching)

Nexa v1.3.7 引入了强大的模式匹配系统，支持 7 种模式类型，可以在 `match`、`let`、`for` 语句中使用。

---

## 📋 模式类型总览

| 模式类型 | 语法 | 说明 |
|---------|------|------|
| **Wildcard** | `_` | 匹配任意值，不绑定 |
| **Literal** | `42`, `"hello"`, `true` | 匹配字面量 |
| **Variable** | `x`, `name` | 匹配并绑定到变量 |
| **Tuple** | `(a, b, c)` | 匹配元组结构 |
| **Array** | `[a, b, ..rest]` | 匹配数组，支持 rest 模式 |
| **Map** | `{key: value, ..rest}` | 匹配字典，支持 rest 模式 |
| **Variant** | `Option::Some(x)` | 匹配 ADT 变体 |

---

## 🎯 `match` 表达式

### 基本语法

```nexa
result = match expression {
    pattern1 => value1,
    pattern2 => value2,
    _ => default_value
};
```

### 示例：简单值匹配

```nexa
flow main {
    status = "success";
    
    message = match status {
        "success" => "操作成功",
        "error" => "操作失败",
        "pending" => "处理中",
        _ => "未知状态"
    };
    
    print(message);
}
```

---

## 🔢 字面量模式 (Literal Pattern)

匹配整数、浮点数、字符串、布尔值。

```nexa
flow main {
    code = 200;
    
    description = match code {
        200 => "OK",
        404 => "Not Found",
        500 => "Internal Server Error",
        _ => "Unknown"
    };
}
```

---

## 📦 元组模式 (Tuple Pattern)

匹配元组结构，解构绑定。

```nexa
flow main {
    point = (10, 20);
    
    description = match point {
        (0, 0) => "原点",
        (x, 0) => "X 轴上的点",
        (0, y) => "Y 轴上的点",
        (x, y) => "普通点 (" + x + ", " + y + ")"
    };
}
```

---

## 📚 数组模式 (Array Pattern)

匹配数组，支持 rest 模式捕获剩余元素。

```nexa
flow main {
    numbers = [1, 2, 3, 4, 5];
    
    result = match numbers {
        [] => "空数组",
        [x] => "单元素：" + x,
        [first, second] => "两个元素",
        [first, ..rest] => "首元素：" + first + "，剩余：" + rest.length
    };
}
```

### Rest 模式

`..identifier` 捕获剩余元素为数组。

```nexa
[first, second, ..others] = [1, 2, 3, 4, 5];
// first = 1, second = 2, others = [3, 4, 5]
```

---

## 🗂 字典模式 (Map Pattern)

匹配字典键值对，支持 rest 模式。

```nexa
flow main {
    user = {"name": "Alice", "age": 30, "email": "alice@example.com"};
    
    greeting = match user {
        {"name": name} => "Hello, " + name,
        {"name": name, "age": age} => name + " (" + age + "岁)",
        {"name": name, ..rest} => name + " (其他信息：" + rest.keys + ")"
    };
}
```

---

## 🏷 变体模式 (Variant Pattern)

匹配 ADT 枚举变体。

```nexa
enum Option {
    Some(value),
    None
}

flow main {
    opt = Option::Some(42);
    
    result = match opt {
        Option::Some(x) => "值：" + x,
        Option::None => "无值"
    };
}
```

---

## 🛡 Guard 条件

在模式后添加 `if` 条件进行额外检查。

```nexa
flow main {
    number = 42;
    
    category = match number {
        n if n < 0 => "负数",
        0 => "零",
        n if n > 0 and n < 10 => "个位数",
        n if n >= 10 => "多位数"
    };
}
```

---

## 📝 `let` 解构

使用 `let` 语句进行模式解构绑定。

```nexa
flow main {
    point = (10, 20);
    let (x, y) = point;
    print("x=" + x + ", y=" + y);
    
    user = {"name": "Bob", "age": 25};
    let {"name": name, "age": age} = user;
    print(name + " is " + age + " years old");
}
```

---

## 🔄 `for` 解构

在 `for` 循环中使用模式解构。

```nexa
flow main {
    points = [(1, 2), (3, 4), (5, 6)];
    
    for (x, y) in points {
        print("Point: (" + x + ", " + y + ")");
    }
    
    users = [
        {"name": "Alice", "score": 95},
        {"name": "Bob", "score": 87}
    ];
    
    for {"name": name, "score": score} in users {
        print(name + ": " + score);
    }
}
```

---

## 🎨 嵌套模式

模式可以嵌套组合。

```nexa
flow main {
    data = {
        "user": {"name": "Alice", "age": 30},
        "scores": [95, 87, 92]
    };
    
    result = match data {
        {"user": {"name": name}, "scores": [first, ..rest]} => 
            name + " 的首次成绩：" + first,
        _ => "数据格式不匹配"
    };
}
```

---

## 📊 最佳实践

### 1. 穷尽性检查

确保所有可能的情况都被覆盖：

```nexa
// 推荐：使用 _ 作为默认分支
result = match value {
    "a" => 1,
    "b" => 2,
    _ => 0  // 默认情况
};

// 避免：遗漏情况可能导致运行时错误
result = match value {
    "a" => 1,
    "b" => 2
    // ❌ 缺少默认分支
};
```

### 2. 模式顺序

更具体的模式放在前面：

```nexa
// 推荐：具体模式优先
result = match list {
    [] => "空",
    [x] => "单元素",
    [x, y] => "双元素",
    _ => "多元素"
};
```

### 3. 避免过度嵌套

```nexa
// 推荐：适度嵌套
result = match data {
    {"user": {"name": name}} => name,
    _ => "unknown"
};

// 避免：过度嵌套难以阅读
result = match data {
    {"a": {"b": {"c": {"d": value}}}} => value,  // ❌ 太深
    _ => null
};
```

---

## 📚 相关文档

- [ADT (代数数据类型)](part2_adt.md) — Struct/Enum/Trait/Impl
- [错误传播](part2_error_handling.md) — `?` 操作符和 `otherwise`
- [语言参考](reference.md) — 完整语法规范
