---
title: "诊断与停止状态索引"
capabilities: [compilation, execution, verification]
---

# 诊断与停止状态索引

以实际异常、Harness rule ID 和 `RunState.status` 定位问题。旧页面的 E001–EC02 分类曾作为说明性编号；当前 CLI 的权威诊断来自实际输出。

| 标识 | 层次 | 处理入口 |
| --- | --- | --- |
| `CompilationError` | 解析、include、生成物语法 | [统一编译](part5_compiler.md) |
| Harness rule ID | 预算、工具、上下文等静态约束 | [Harness](part2_harness.md) |
| `waiting_approval` | 执行暂停 | [审批](runtime_approval.md) |
| `failed` | provider、工具或输出校验 | [排查](troubleshooting.md) |
| `cancelled` | 协作取消 | [执行](runtime_execution.md) |
| `timed_out` | 总时限 | [预算](runtime_execution.md) |
| `budget_exhausted` | 模型/工具/token 上限 | [预算](runtime_execution.md) |
| `CheckpointConflict` | revision 冲突 | [checkpoint](runtime_checkpoints.md) |
| `ToolOutcomeUnknown` | 副作用结果不确定 | [未知结果](runtime_checkpoints.md) |
| `pass/fail/skip/error` | `.nxintent` 证据状态 | [验证](part2_harness.md) |

向用户显示诊断时保留来源文件、行列、原始消息与 run ID。缺少 source span 的结果应显示解析错误，不推测导航位置。

---

[来源与验证](capability_inventory.md) · `compilation` / `execution` / `verification`
