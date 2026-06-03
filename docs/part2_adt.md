---
comments: true
---

# ADT：代数数据类型 (Algebraic Data Types)

Nexa v1.3.7 引入了完整的 ADT 系统，包括 `struct`、`enum`、`trait` 和 `impl`，让你能够定义类型安全的数据结构和行为接口。

---

## 📋 ADT 组件总览

| 组件 | 语法 | 说明 |
|------|------|------|
| **struct** | `struct Name { fields }` | 定义记录类型 |
| **enum** | `enum Name { variants }` | 定义枚举类型 |
| **trait** | `trait Name { methods }` | 定义行为接口 |
| **impl** | `impl Trait for Type { methods }` | 实现 trait |

---

## 🏗 `struct` — 记录类型

### 基本语法

```nexa
struct Point {
    x: Int,
    y: Int
}

struct User {
    name: String,
    age: Int,
    email: String
}
```

### 创建实例

```nexa
flow main {
    p = Point(x: 10, y: 20);
    print("x=" + p.x + ", y=" + p.y);
    
    user = User(name: "Alice", age: 30, email: "alice@example.com");
    print(user.name);
}
```

### 字段访问与修改

```nexa
flow main {
    p = Point(x: 10, y: 20);
    
    // 访问字段
    print(p.x);
    
    // 修改字段（如果 struct 是可变的）
    p.x = 15;
}
```

---

## 🏷 `enum` — 枚举类型

### 基本语法

```nexa
enum Color {
    Red,
    Green,
    Blue
}

enum Option {
    Some(value),
    None
}

enum Result {
    Ok(value),
    Err(error)
}
```

### 创建变体

```nexa
flow main {
    color = Color::Red;
    
    opt = Option::Some(42);
    empty = Option::None;
    
    success = Result::Ok("data");
    failure = Result::Err("error message");
}
```

### 模式匹配

```nexa
flow main {
    opt = Option::Some(42);
    
    result = match opt {
        Option::Some(x) => "值：" + x,
        Option::None => "无值"
    };
    
    print(result);
}
```

---

## 🎯 `trait` — 行为接口

### 基本语法

```nexa
trait Printable {
    fn format(): String
}

trait Comparable {
    fn compare(other: Self): Int
}

trait Container {
    fn size(): Int,
    fn isEmpty(): Bool
}
```

### 方法签名

- 方法可以有参数和返回类型
- 方法体在 `impl` 中实现

---

## 🔧 `impl` — 实现 trait

### 基本语法

```nexa
struct Point {
    x: Int,
    y: Int
}

trait Printable {
    fn format(): String
}

impl Printable for Point {
    fn format(): String {
        return "(" + self.x + ", " + self.y + ")";
    }
}
```

### 调用 trait 方法

```nexa
flow main {
    p = Point(x: 10, y: 20);
    
    // 调用 trait 方法
    formatted = p.format();
    print(formatted);  // 输出: (10, 20)
}
```

---

## 🎨 完整示例：Option 类型

```nexa
// 定义 Option 枚举
enum Option {
    Some(value),
    None
}

// 定义 Printable trait
trait Printable {
    fn format(): String
}

// 为 Option 实现 Printable
impl Printable for Option {
    fn format(): String {
        return match self {
            Option::Some(v) => "Some(" + v + ")",
            Option::None => "None"
        };
    }
}

// 定义可空除法函数
flow safe_divide(a: Int, b: Int): Option {
    if b == 0 {
        return Option::None;
    } else {
        return Option::Some(a / b);
    }
}

flow main {
    result1 = safe_divide(10, 2);
    result2 = safe_divide(10, 0);
    
    print(result1.format());  // Some(5)
    print(result2.format());  // None
    
    // 模式匹配处理
    match result1 {
        Option::Some(v) => print("结果：" + v),
        Option::None => print("除零错误")
    }
}
```

---

## 🔄 Result 类型

```nexa
enum Result {
    Ok(value),
    Err(error)
}

flow parse_int(text: String): Result {
    python! """
    try:
        return {"_nexa_option_variant": "Ok", "value": int(text)}
    except ValueError as e:
        return {"_nexa_option_variant": "Err", "error": str(e)}
    """
}

flow main {
    result = parse_int("42");
    
    match result {
        Result::Ok(v) => print("解析成功：" + v),
        Result::Err(e) => print("解析失败：" + e)
    }
}
```

---

## 📊 最佳实践

### 1. 使用 Option 表示可空值

```nexa
// 推荐：使用 Option
flow find_user(id: Int): Option {
    // ...
}

// 避免：使用 null
flow find_user(id: Int): User {
    // 可能返回 null ❌
}
```

### 2. 使用 Result 表示可能失败的操作

```nexa
// 推荐：使用 Result
flow read_file(path: String): Result {
    // Ok(content) 或 Err(error)
}

// 避免：抛出异常
flow read_file(path: String): String {
    // 可能抛出异常 ❌
}
```

### 3. Trait 命名规范

```nexa
// 推荐：使用形容词或能力描述
trait Printable { }
trait Comparable { }
trait Serializable { }

// 避免：使用名词
trait Printer { }  // ❌
```

---

## 📚 相关文档

- [模式匹配](part2_pattern_matching.md) — 7 种模式类型
- [错误传播](part2_error_handling.md) — `?` 操作符和 `otherwise`
- [语言参考](reference.md) — 完整语法规范
