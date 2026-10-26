---
title: "迁移到 2.4"
capabilities: [compilation, execution, conversations, harness, verification, rust]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 迁移到 2.4

迁移基线是Nexa 3.0 内保留的 2.4 兼容源码。先保留原运行数据和旧源码，再在隔离工作区执行以下检查。

## 编译与接口

- 将嵌入式编译统一到 `src.compiler.compile_file` / `compile_source`，使用返回的 `python_code`、`ast`、`sources` 与 `diagnostics`。
- include 相对导入文件解析；循环依赖和缺失文件会返回具体诊断。
- 声明模块可以独立编译。运行模型前完成 `validate` 和完整程序编译。
- 连续会话直接返回值使用 `run`；独立可检查运行使用 `execute`；已结束状态的新一轮使用 [continue_run](runtime_conversations.md)。

## 执行语义变化

| 原有依赖 | 迁移动作 |
| --- | --- |
| `exit_when` 自由文本包含判断 | 改为与最终文本或 `status` 精确匹配的状态值 |
| 忽略 `verify` 或结构化输出错误继续执行 | 修复条件、schema 或输出，保留失败路径 |
| 默认允许风险工具 | 显式处理 `waiting_approval` 和布尔决定 |
| `sandbox` 仅作为注解 | 配置实际隔离执行器，或重新设计工具执行边界 |
| 将 flow 快照视为外部事务回滚 | 按深拷贝内存恢复设计，外部副作用单独处理 |
| 将缓存命中率作为固定属性 | 按无工具 Chat 新运行与完整缓存键重新评测 |
| Rust 与 Python 全量等价 | 按 [Rust 支持子集](runtime_rust.md)选择后端 |

## 持久化与验证

保留 checkpoint 的源码、Agent 定义、provider 与工作目录。未知工具结果须先核实。总时限包含审批与恢复间隔；新任务通过新的运行入口取得新预算，旧审批不会跨轮沿用。

`.nxintent` 的 `skip` 和 `error` 单独统计，只有 `pass` 算通过。重新检查 `examples/manifest.json` 中每个例子的 `compiled` 或 `historical_drafts` 状态，不按文件夹版本推断可运行性。

## 建议验收顺序

1. 无凭据编译完整程序，核对诊断。
2. 用固定 provider fixture 检查输出、工具、副作用和终态。
3. 验证审批允许/拒绝、跨进程恢复、未知结果停止。
4. 验证预算、取消、超时与新一轮对话。
5. 确定 provider、模型、预算后再测真实质量、成本与延迟。

---

[来源与验证](capability_inventory.md) · `compilation` / `execution` / `conversations` / `harness` / `verification` / `rust`
