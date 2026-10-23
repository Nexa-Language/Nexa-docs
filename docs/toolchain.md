---
title: "开发工具链"
capabilities: [ecosystem, cli, conversations]
---

# 开发工具链

Nexa 的三个开发入口共享语言与运行时契约：CLI 运行程序，Nexa Code 执行编程任务，VS Code 提供编辑与诊断。当前 2.4 适配基于本地开发 checkout。

## CLI

按[快速入门](quickstart.md)准备 Python 3.10+、uv 和本地 Nexa。`validate --json`、`inspect --format json`、`agent` 分别提供诊断、结构和持久运行入口。

## Nexa Code

[Nexa-Code 仓库](https://github.com/Nexa-Language/Nexa-Code)提供 Ink/React 终端助手。使用该 checkout 的 README 建立开发运行时链接，再在独立工作区验收读写、审批、取消与会话恢复。运行层的入口为 `execute`、`continue_run` 和 checkpoint，详见[连续对话](runtime_conversations.md)。

## VS Code

[Nexa-extension 仓库](https://github.com/Nexa-Language/Nexa-extension)维护编辑器集成。扩展开发与打包工具需要 Node.js 22+、pnpm；VS Code API 基线为 1.96。安装本地 VSIX 后，按扩展 README 指定已确认的 Nexa CLI 路径。

结构化 `inspect` 的声明条目包含 `source: {file, line, column, end_line, end_column}`，位置从 1 开始，结束位置为开区间。include 声明保留原文件位置。编辑器在没有 source span 时显示诊断。

## 发布状态

本轮安装以显式本地路径为准。公开 CLI 包、Nexa Code 包或 VSIX 发布需要各仓库独立的版本、打包和发布验收；本站不提供未建立的 2.4 发布链接。

---

[来源与验证](capability_inventory.md) · `ecosystem` / `cli` / `conversations`
