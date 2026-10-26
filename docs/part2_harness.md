---
title: "Harness 执行原语"
capabilities: [harness, verification, tools]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# Harness 执行原语

Harness 将执行、工具、上下文、状态、生命周期与验证组织为运行约束。编译期诊断与实际运行语义分别检查。

| 原语 | 2.4 行为 |
| --- | --- |
| `autoloop` | 步数和时间限制；`exit_when` 与最后赋值的文本或 `status` 字段精确比较，忽略首尾空白及大小写 |
| `with_context` | 异常时退出作用域；Chat 按完整 user turn 裁剪，保留工具调用与结果配对 |
| `snapshot` / `restore` | 深拷贝恢复 flow 变量、Agent 会话、工具结果与 provider 状态 |
| `fork` / `merge` | 有界执行、独立会话、稳定结果顺序 |
| `verify` | 失败抛出断言并阻止后续成功路径 |
| `reflect` | 把反思文本注入后续 Agent 输入 |
| 生命周期 hook | 绑定当前 flow 的模型和工具事件，flow 结束后清理 |

`before_tool(name)` 和 `after_tool(name)` 只观察指定工具。`on_error(problem: Exception)` 中的 `problem` 绑定事件保存的错误摘要字符串，可用于日志；hook 保留原运行的失败状态。

## 快照范围

完整离线程序，结果恢复为 `3`。

```nexa
flow main {
    result = 3;
    point = snapshot();
    result = 9;
    restore(point);
}
```

当前实现使用深拷贝；复制成本取决于保存的状态大小。外部文件和服务副作用保留。持久化任务恢复使用 [checkpoint](runtime_checkpoints.md)。

## 可执行验证

完整离线程序，在类型验证处失败；`unexpected` 永远不会成为成功结果。

```nexa
flow main {
    result = 3;
    verify result satisfies string;
    result = "unexpected";
}
```

确定性谓词支持类型、数值比较、包含关系和长度。其他语义验证需要显式 evaluator；`.nxintent` 使用 `pass/fail/skip/error`，只有 `pass` 计为通过。缺少 runtime、schema 或语义 evaluator 时为 `skip`；空输出为失败，evaluator 异常为 `error`。

## 编译诊断模式

`build`/`run` 默认 `--harness warn`；`harness-check` 默认 `strict`。`strict` 遇到错误会阻止编译，`warn` 输出诊断，`off` 关闭 Harness 静态检查。工具审批、输出验证等运行行为仍由运行时执行。

---

[来源与验证](capability_inventory.md) · `harness` / `verification` / `tools`
