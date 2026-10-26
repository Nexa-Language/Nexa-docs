---
title: 为什么使用 Nexa
capabilities:
- open_language
- open_evidence
- open_revisions
language_versions:
- '3.0'
- '2.4'
---

# 为什么使用 Nexa

Nexa 3.0 让程序持有目标、实现、证据和修订。人和模型编写同一种 `.nx` 合同；原生编译器检查合同、在预算内求解实现，并在 OCI 中执行验收。通过的结果保留证据，仓库写入还需要独立的准确授权。

目标声明说明需要完成什么，冻结检查说明如何判断，状态记录说明当前处于哪一步。源码草稿与 active runtime revision 分开保存；相关依赖变化时重新验证，未知外部副作用先核对再恢复。

从[快速入门](quickstart.md)运行常量实现，再用[开放目标](open_programs.md)学习模型辅助求解。已有 Agent、tool、flow、Actor 和 MCP 应用继续走 [2.4 兼容入口](quickstart_24.md)，迁移时按[合同与状态清单](migration_30.md)逐项处理。
