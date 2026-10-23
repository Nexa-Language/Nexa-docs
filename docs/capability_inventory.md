---
title: "能力与示例证据"
capabilities: [compilation, verification]
---

# 能力与示例证据

本站以 [Nexa v2.4.0 源码](https://github.com/Nexa-Language/Nexa/commit/c2162637236e4a73feea410c4183672411666521) 为验证基线。机器可读 [inventory.json](inventory.json) 记录运行时版本、Git 基线、工作区状态，以及每个能力的准确源码与测试符号、SHA-256。已核对正式 tag `v2.4.0` 指向此 commit；安装步骤使用该发行源码。

## 三类记录

| 记录 | 字段与用途 |
| --- | --- |
| 页面 | 路径、语言、能力 ID；中英文必须成对且能力一致 |
| 能力 | 当前/规划状态、具体声明、源码或测试文件与符号、内容 hash |
| 示例 | 页面、块序号、代码 hash、complete/partial/historical、编译或离线执行方式 |

完整 Nexa 块通过本地 `src.compiler.compile_source` 编译。代表性示例在网络禁用的临时工作目录运行，模型边界使用固定 fixture。SDK、工具、flow 与输出验证仍走真实实现。

## 更新规则

新增代码块必须登记；修改代码必须重新编译并更新 hash。片段和历史草案需要逐例、可见的缺失依赖或失败原因。源码 provenance 改变时先复核相关声明，再显式刷新证据。

严格构建检查 Markdown 与导航；HTML 检查覆盖内部目标、fragment、图像、样式与脚本；语言检查要求每个页面都有中英版本。生成的标准库 schema 保存为 [stdlib-api.json](stdlib-api.json)，与实际注册表比对。

本地与 CI 命令见 [Nexa-docs README](https://github.com/Nexa-Language/Nexa-docs)。外部 URL 的可达性、真实模型质量和发布结果需要单独验证。

---

[来源与验证](capability_inventory.md) · `compilation` / `verification`
