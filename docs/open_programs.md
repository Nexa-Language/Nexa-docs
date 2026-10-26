---
title: "Open Programs：目标与合同"
capabilities: [open_language, open_execution]
language_versions: ["3.0"]
---

# Open Programs：目标与合同

一个 Open Program 持有目标、可选实现、验收要求和依赖。人和作者 Agent 编写相同的 `.nx` 合同；原生前端负责类型边界、重复条款和依赖关系检查。

## 完整的开放目标

```nexa
language "3.0"
program Sum {
    goal total() -> Int {
        intent "Sum every integer in inputs.get('values', []); return zero for an empty list."
        capabilities [sandbox.exec]
        ensure checks.sum
        review model("Handle all integers, including negatives, without hardcoded case outputs.")
        implementation open
    }
}
```

保存为 `sum.nx` 后运行 `uv run nexa check sum.nx --json`。结果有一个开放义务 `total`。要执行，environment 必须提供 `checks.sum` 和授权的 model binding。本站以固定 provider 回复执行此例：`solve(inputs)` 对 `values` 求和，空输入返回 `0`；额外的冻结用例检查正数与负数，模型评审独立记录。构建发起一次实现请求、一次评审请求；锁定重放为零请求。

## 合同字段

| 字段 | 含义 |
| --- | --- |
| `goal name(arg: Type) -> Type` | 参数必须有类型；返回值经类型检查后使用 |
| `intent` | 非空任务意图；澄清形成子修订 |
| `implementation open` | 留下求解义务 |
| `implementation value <JSON>` | 明确的 JSON 常量 |
| `implementation python "..."` | 在 OCI 内调用 `solve(inputs)`；需要 `sandbox.exec` |
| `ensure checks.name` | environment 中同名的固定检查 |
| `review model("criterion")` | 独立的结构化布尔评审 |
| `depends [name]` | DAG 依赖；结果进入 `inputs["dependencies"]` |
| `stage runtime` | 在活动中求解；默认 stage 为 build |

支持 Int、Float、String、Bool、Unit、Json、Patch、Repository 和 ChangeRequest。build goal 不能依赖 runtime goal。同种 `ensure`/`review` 不得重复，自动 `typecheck` 名称保留。

## 仓库维护合同

发行示例 `examples/open_programs/maintain.nx` 声明 Repository 参数、接收 ChangeRequest 并返回 Patch 的 runtime goal，以及 `on change_request` handler。handler 通过 `resolve` 得到结果，再 `propose repo.apply(result) requires human.approval`。这条路径的候选求解、回归检查、授权与工作区应用分别记录。

命名的 environment、sandbox 与 acceptance 声明选择参考绑定；实际检查要求来自 goal 子句与 environment 配置。原生 `compile_program` 根据显式版本分派；旧 `compile_source`/`compile_file` 保持 2.4 Python lowering。

继续阅读：[环境](open_environments.md) · [证据](open_evidence.md) · [准确授权](open_grants.md)。

---

[来源与验证](capability_inventory.md) · `open_language` / `open_execution`
