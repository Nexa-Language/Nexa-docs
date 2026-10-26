---
title: "修订、取消与恢复"
capabilities: [open_revisions, open_author]
language_versions: ["3.0"]
---

# 修订、取消与恢复

源码草稿、active runtime revision、作者活动和 runtime 活动有不同身份。一次修改先成为草稿，再构建接纳，最后切换 runtime head；旧活动保持创建时绑定的源码与产物，新活动使用已激活版本。

## CAS 修订与活动

```sh
uv run nexa open revise program.nx --environment environment.json --state .nexa/program.db --program-id demo --expected-revision CURRENT_REVISION
uv run nexa open status demo --state .nexa/program.db
uv run nexa open cancel ACTIVITY_ID --environment environment.json --state .nexa/program.db
```

`CURRENT_REVISION` 来自当前草稿，`ACTIVITY_ID` 来自用户选中的准确活动。遇到 `revision_conflict`，重新读取真实 revision 并展示冲突；保留并发编辑。`open status` 返回 RuntimeHead；完整 runtime 活动及其历史由 ProgramSession/ProgramStore 查询。Author `activity/read` 返回作者活动。

活动按 revision 和 artifact digest 固定。跨进程恢复时按 program 查询持久事件，从事件对象读取 RuntimeActivity，再按原 activity ID 取最新状态。多个并行活动应逐个列出，取消只作用于用户选中的 ID。

## 控制器恢复

```sh
uv run nexa open resume demo --environment environment.json --state .nexa/program.db
```

仍运行的操作所有者持有内核锁，恢复返回 `operation_busy`。中断活动保留历史，恢复后由客户端显式发起新活动。SQLite 在同一事务中提交 revision、对象和事件；未知 schema、其他应用数据库与内容 digest 不符的对象会被拒绝。

外部作用写入 `prepared` / `started` / `completed` journal。幂等适配器沿用原 operation key；未知非幂等结果先通过 `EffectJournal.reconcile` 记录核对结果。核对完成前，新活动、版本切换及补丁应用保持阻塞。

状态 schema 迁移在 OCI 内执行纯 Candidate，并检查返回 JSON 是否符合目标 schema；失败保留之前的 runtime head。准确补丁写入后的恢复使用[补丁 journal](open_grants.md)，旧 2.4 checkpoint 使用[兼容恢复](runtime_checkpoints.md)。

---

[来源与验证](capability_inventory.md) · `open_revisions` / `open_author`
