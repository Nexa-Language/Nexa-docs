---
title: "Capsule：有条件复用"
capabilities: [open_capsules, open_evidence]
language_versions: ["3.0"]
---

# Capsule：有条件复用

Capsule 保存实现、来源、许可、合同条件、能力、依赖与证据。接收任务显式选择后，runtime 重新匹配并验收；新输入带来新的验证义务。

```sh
uv run nexa open capsule export repair.capsule.json --activity ACTIVITY_ID --source local-repository --creator local-operator --license MIT --state .nexa/maintain.db
uv run nexa open capsule import repair.capsule.json --state .nexa/second.db
```

从实际已完成活动取得 `ACTIVITY_ID`；导入返回 capsule ID。在新的 `nexa run` 命令增加 `--capsule CAPSULE_ID`，选择该实现。显式源码 implementation 优先，capsule 实现必须与其完全相同；只有开放实现可以选择其他匹配候选。

## 复用判定

文件 hash 验证完整性，本地可信证据登记决定哪些结果可以复用。合同、能力、原始来源和依赖条件都参与匹配。新任务持续保留原实现约束，删除导入文件中的条件会破坏匹配或完整性。

复用候选可以省掉生成请求；当前任务仍按 policy 检查输入和证据。可变模型别名跨任务重新评审，人工授权不随 capsule 转移。即使复用产物通过验收，写入仍需针对当前 proposal 的准确 grant。

锁定产物的重放保存 lock 与对象数据库；capsule 的跨任务复用保存来源和可验证条件。两条路径的运行结果与证据可分别查看，见[验收](open_evidence.md)。

---

[来源与验证](capability_inventory.md) · `open_capsules` / `open_evidence`
