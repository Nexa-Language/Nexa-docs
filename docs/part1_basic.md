---
title: "语言基础"
capabilities: [language, compilation]
---

# 语言基础

Nexa 程序把 Agent 声明、工具声明和 flow 控制流放在 `.nx` 文件中。编译器将程序规范化为 AST，再生成 Python；声明模块可独立编译。

## 值与控制流

变量用赋值建立，`result` 是 flow 的返回约定。字符串使用双引号；语句可用分号结束。以下完整程序离线执行得到 `12`。

```nexa
flow main {
    first = 3;
    print(first * 4);
    result = first * 4;
}
```

基础表达式包括整数、浮点数、字符串、布尔值、列表、映射、算术与比较；`if`、`for`、`while` 组织确定性控制流。依赖模型语义的路由应给出实际模型与验证条件。

## Agent 与调用

Agent 的 `prompt` 定义任务指令，`model` 与 `provider_api` 选择模型和协议，`uses` 限定可用工具。下面是完整程序，模型调用由 `run` 发起。

```nexa
agent Echo {
    prompt: "Repeat the supplied text."
}

flow main {
    result = Echo.run("hello");
    verify result satisfies string;
}
```

先按[模型配置](runtime_providers.md)选择 provider，再用 `uv run nexa run echo.nx` 执行。模型应返回输入文本；`verify` 检查返回值为字符串。

## 模块

`include "helpers.nxlib";` 先相对当前导入文件解析，再查找包内标准库。相同规范路径只导入一次，循环依赖诊断包含路径链。`.nxs` 保存本地配置；秘密值不应写入示例或版本控制。

继续阅读[工具与 Protocol](part3_extensions.md)、[高级编排](part2_advanced.md)和[编译器](part5_compiler.md)。


## 分支

`if` 与 `while` 的确定性条件使用括号。比较支持 `==`、`!=`、`>`、`>=`、`<`、`<=`；条件可用 `and` / `or` 组合。

```nexa
flow main {
    value = 7;
    label = "";
    if (value > 5) {
        label = "large";
    } else {
        label = "small";
    }
    result = label;
}
```

本例返回 `large`。在 flow 末尾保留一个顶层赋值，明确返回值；当前生成器对以 `if`、`while` 或 `print` 结束的 flow 返回 `None`。

## 集合与遍历

`for each item in items` 遍历集合；`for each index, item in items` 同时取得索引和值。当前表达式 parser 的数组/字典字面量位置有限，应用可通过受信任的 `python!` 或工具结果建立集合。`std.json.parse` 返回标准库的 JSON 文本结果，若需要本地 Python 集合，应显式反序列化。

```nexa
flow main {
    python! """items = [1, 2, 3]"""
    total = 0;
    for each item in items {
        total = total + item;
    }
    result = total;
}
```

本例返回 `6`。`break;` 退出当前循环，`continue;` 进入下一次迭代。

## while 循环

```nexa
flow main {
    counter = 0;
    while (counter < 3) {
        counter = counter + 1;
    }
    result = counter;
}
```

本例返回 `3`。模型自主循环使用 [autoloop](part2_harness.md) 以显式设置步数和时间。

## 带参数的 flow

参数写作 `name: type`，返回类型写作 `-> type`。从另一 flow 按名称调用。

```nexa
flow double(value: int) -> int {
    result = value * 2;
}
flow main {
    result = double(6);
}
```

本例返回 `12`。完整运算符、类型和 Agent 参数表见[语言参考](reference.md)。

---

[来源与验证](capability_inventory.md) · `language` / `compilation`
