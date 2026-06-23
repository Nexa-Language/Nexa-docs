# Terminal UI (v2.3.1)

> **v2.3.1 新特性** — 基于 `rich` 的终端 UI 渲染 + CJK 宽字符输入。

## 概述

Nexa v2.3.1 引入终端 UI 库，让 Agent 输出不再是纯文本——支持 markdown 渲染、语法高亮代码块、spinner 动画、样式化面板和状态图标。

## `std.ui` DSL

在 `.nx` 文件中直接调用 UI 函数：

```nexa
flow main {
    std.ui.banner("My App", "Subtitle here");
    std.ui.markdown("# Hello\n\nThis is **bold** and `code`.");
    std.ui.code("print('hello')", "python");
    std.ui.thinking("Analyzing", 1.0);
    std.ui.success("Operation completed!");
    std.ui.error("Something went wrong");
    std.ui.agent_reply("AgentName", "Reply rendered as **markdown**");
}
```

## 可用函数

| 函数 | 说明 |
|------|------|
| `std.ui.banner(title, subtitle)` | 启动 banner（双线边框） |
| `std.ui.markdown(text)` | Markdown 渲染 |
| `std.ui.code(code, language)` | 语法高亮代码块 |
| `std.ui.panel(text, title, style)` | 样式化面板 |
| `std.ui.thinking(msg, duration)` | 思考 spinner 动画 |
| `std.ui.success(msg)` | ✅ 成功消息 |
| `std.ui.error(msg)` | ❌ 错误消息 |
| `std.ui.warning(msg)` | ⚠️ 警告消息 |
| `std.ui.info(msg)` | ℹ️ 信息消息 |
| `std.ui.input(prompt)` | 样式化输入（CJK 兼容） |
| `std.ui.agent_reply(name, reply)` | Agent 回复面板（markdown） |
| `std.ui.tool_call(name, args)` | 工具调用通知 |

## CJK 输入修复

v2.3.1 使用 `prompt_toolkit` 替代 Python 内置 `input()`，正确处理中文/日文/韩文等宽字符的回退（backspace）操作。

## 依赖

```
pip install rich prompt_toolkit
```

未安装时自动降级为纯文本输出。
