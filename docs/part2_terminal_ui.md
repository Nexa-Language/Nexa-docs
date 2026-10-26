---
title: "终端 UI"
capabilities: [terminal, stdlib]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 终端 UI

`std.ui` 为 Nexa 程序提供 Markdown、代码、面板、状态消息与交互输入。渲染通过 `rich`，交互输入通过 `prompt_toolkit`。

## 安装与完整示例

在 Nexa checkout 安装可选依赖：

```sh
uv sync --locked --extra terminal
```

下面的完整程序编译后可在终端显示消息，无需模型调用。

```nexa
flow main {
    std.ui.banner("Nexa", "Development workspace");
    std.ui.markdown("# Ready\nInspect the source before execution.");
    std.ui.success("Program loaded");
}
```

| 函数 | 用途 |
| --- | --- |
| `banner(title, subtitle)` | 应用标题 |
| `markdown(text)` / `code(code, language)` | 格式化正文与代码 |
| `panel(text, title, style)` | 分组面板 |
| `thinking(message, duration)` | 有时长的等待提示 |
| `success` / `error` / `warning` / `info` | 状态消息 |
| `input(prompt)` | 交互输入 |
| `agent_reply(name, reply)` / `tool_call(name, args)` | Agent 与工具信息 |

这些名称属于 `std.ui` namespace。中文等宽字符输入的实际表现受终端环境影响，发布应用时在目标终端检查输入、退格与取消。Nexa Code 的 Ink 界面属于独立[工具链](toolchain.md)。

---

[来源与验证](capability_inventory.md) · `terminal` / `stdlib`
