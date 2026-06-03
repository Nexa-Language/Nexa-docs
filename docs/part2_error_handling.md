---
comments: true
---

# 错误传播与延迟执行

Nexa v1.3.2 引入了 `?` 操作符和 `otherwise` 关键字，提供优雅的错误传播机制。v1.3.7 进一步添加了 `defer` 语句用于资源清理。

---

## 📋 错误处理机制总览

| 机制 | 语法 | 说明 |
|------|------|------|
| **错误传播** | `expr?` | 失败时 early-return |
| **内联处理** | `expr otherwise handler` | 失败时执行 handler |
| **延迟执行** | `defer expr;` | 作用域退出时执行 |

---

## ❓ `?` 操作符 — 错误传播

`?` 操作符在表达式失败时自动 early-return，避免嵌套的 if-else 检查。

### 基本语法

```nexa
result = expression?;
```

### 运行时行为

1. 执行 `expression`
2. 若返回 `Result::Err` 或 `Option::None`，立即从当前 flow 返回
3. 若成功，解包值并继续执行

### 示例：链式调用

```nexa
enum Result {
    Ok(value),
    Err(error)
}

flow parse_and_double(text: String): Result {
    // 解析失败时自动 early-return
    num = parse_int(text)?;
    
    // 只有解析成功才会执行到这里
    return Result::Ok(num * 2);
}

flow main {
    result1 = parse_and_double("21");  // Ok(42)
    result2 = parse_and_double("abc"); // Err(...)
}
```

### 对比：传统写法 vs `?` 操作符

```nexa
// 传统写法：嵌套 if-else
flow process(data: String): Result {
    result1 = step1(data);
    if result1 is Err {
        return result1;
    }
    
    result2 = step2(result1.value);
    if result2 is Err {
        return result2;
    }
    
    return step3(result2.value);
}

// 使用 ? 操作符：简洁清晰
flow process(data: String): Result {
    v1 = step1(data)?;
    v2 = step2(v1)?;
    return step3(v2);
}
```

---

## 🛡 `otherwise` — 内联错误处理

`otherwise` 在表达式失败时执行备用逻辑，而不是 early-return。

### 基本语法

```nexa
result = expression otherwise handler;
```

### Handler 类型

| Handler 类型 | 语法 | 说明 |
|-------------|------|------|
| **值** | `otherwise "default"` | 返回默认值 |
| **变量** | `otherwise fallback_var` | 返回变量值 |
| **Agent 调用** | `otherwise Agent.run(...)` | 调用 Agent 处理 |
| **代码块** | `otherwise { ... }` | 执行代码块 |

### 示例：默认值

```nexa
flow main {
    // 解析失败时使用默认值
    num = parse_int("abc") otherwise 0;
    print(num);  // 输出: 0
    
    // 文件不存在时返回空字符串
    content = read_file("missing.txt") otherwise "";
}
```

### 示例：Agent 回退

```nexa
agent PrimaryParser {
    prompt: "解析复杂数据"
}

agent FallbackParser {
    prompt: "使用简单方法解析"
}

flow main {
    // 主 Agent 失败时调用备用 Agent
    result = PrimaryParser.run(data) otherwise FallbackParser.run(data);
}
```

### 示例：代码块处理

```nexa
flow main {
    result = risky_operation() otherwise {
        print("操作失败，执行回退逻辑");
        backup_result = backup_operation();
        return backup_result;
    };
}
```

---

## 🔄 `defer` — 延迟执行

`defer` 语句在当前作用域退出时执行，用于资源清理（LIFO 顺序）。

### 基本语法

```nexa
defer expression;
```

### 执行时机

- Flow 正常返回时
- Flow 因错误 early-return 时
- 循环迭代结束时（如果在循环内）

### 示例：文件操作

```nexa
flow process_file(path: String): Result {
    file = open_file(path)?;
    defer file.close();  // 确保文件关闭
    
    content = file.read()?;
    result = process(content)?;
    
    return Result::Ok(result);
    // file.close() 在这里自动执行
}
```

### 示例：多个 defer（LIFO 顺序）

```nexa
flow main {
    defer print("First defer");
    defer print("Second defer");
    defer print("Third defer");
    
    print("Main logic");
    
    // 输出顺序:
    // Main logic
    // Third defer
    // Second defer
    // First defer
}
```

### 示例：资源管理

```nexa
flow with_database(db_url: String): Result {
    conn = connect_db(db_url)?;
    defer conn.close();
    
    transaction = conn.begin()?;
    defer {
        if not transaction.committed {
            transaction.rollback();
        }
    };
    
    result = execute_query(conn)?;
    transaction.commit();
    
    return Result::Ok(result);
}
```

---

## 🎯 组合使用

### 示例：完整的错误处理流程

```nexa
enum Result {
    Ok(value),
    Err(error)
}

flow fetch_and_process(url: String): Result {
    // 设置超时清理
    timer = start_timer(30);
    defer timer.cancel();
    
    // 请求失败时使用缓存
    response = http_get(url)? otherwise load_cache(url);
    
    // 解析失败时 early-return
    data = parse_json(response)?;
    
    // 处理数据
    result = process(data)?;
    
    return Result::Ok(result);
}

flow main {
    match fetch_and_process("https://api.example.com/data") {
        Result::Ok(data) => print("成功：" + data),
        Result::Err(e) => print("失败：" + e)
    }
}
```

---

## 📊 最佳实践

### 1. 优先使用 `?` 而非嵌套检查

```nexa
// 推荐
flow process(): Result {
    a = step1()?;
    b = step2(a)?;
    return step3(b);
}

// 避免
flow process(): Result {
    a = step1();
    if a is Err { return a; }
    b = step2(a.value);
    if b is Err { return b; }
    return step3(b.value);
}
```

### 2. 使用 `otherwise` 提供合理的默认值

```nexa
// 推荐：提供有意义的默认值
config = load_config() otherwise default_config();

// 避免：静默忽略错误
config = load_config() otherwise null;  // ❌
```

### 3. 使用 `defer` 管理资源

```nexa
// 推荐：确保资源释放
flow with_resource(): Result {
    res = acquire_resource()?;
    defer res.release();
    // 使用资源...
}

// 避免：手动管理容易遗漏
flow with_resource(): Result {
    res = acquire_resource()?;
    result = use_resource(res);
    res.release();  // 如果 use_resource 失败，这里不会执行 ❌
    return result;
}
```

### 4. defer 中避免复杂逻辑

```nexa
// 推荐：defer 只做清理
defer file.close();
defer conn.disconnect();

// 避免：defer 中做复杂计算
defer {
    result = complex_calculation();  // ❌
    save_to_database(result);
}
```

---

## 📚 相关文档

- [模式匹配](part2_pattern_matching.md) — 7 种模式类型
- [ADT (代数数据类型)](part2_adt.md) — Struct/Enum/Trait/Impl
- [语言参考](reference.md) — 完整语法规范
