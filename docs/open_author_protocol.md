---
title: "Author 协议与源码同步"
capabilities: [open_author, open_revisions]
language_versions: ["3.0"]
---

# Author 协议与源码同步

Author 3.0 使用 stdin/stdout 上逐行 JSON-RPC 2.0。每帧最多 2 Mi 字符，超长帧会先被排空再读取下一请求。先握手读取协议版本及 `max_inflight`；每个 server 最多同时处理两个作者求解。

```sh
uv run nexa author --state .nexa/author.db --environment examples/open_programs/offline.json
```

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocol_version":"3.0","client":"editor"}}
```

请求有 integer/string/null `id`；notification 省略 id 且无响应。客户端按 id 关联结果，按 `events/read` 的单调 cursor 恢复事件。

| 方法 | 关键参数 / 结果 |
| --- | --- |
| `program/check` | source、可选 path → CheckReport、诊断、义务 |
| `revision/propose` | source、program_id、nullable expected_revision → 草稿修订 |
| `goal/resolve` | program_id、expected_revision、goal、可选 input_json/budget → activity_id |
| `activity/read` / `activity/cancel` | object_id → 作者活动及持久取消状态 |
| `author/answer` | program_id、expected_revision、request_id、answer → 带澄清的子修订 |
| `events/read` | program_id、可选 after → 持久事件 |
| `evidence/explain` | object_id、可选 context → 证据及有效性 |

`goal/resolve` 立即返回作者活动 ID；后续轮询直到终态。它的结果属于作者求解。源码草稿由 CLI/ProgramSession 构建并激活，runtime 活动通过 SDK/`nexa open` 管理。

## 澄清回到源码

`author/answer` 要求准确的澄清 ID 和当前草稿 revision。回答后，客户端从 runtime 读取真实新 IR，把目标 intent 的变更作为 diff 展示，并标记“待同步源码”。确认后仍需核对原 source digest/document version，再写入和重新 check，以准确草稿 CAS 同步。

并发源码编辑时保留新编辑与待同步草稿；用户拒绝同步或退出后，待同步状态也应保留。恢复同步前阻止从旧文件直接 build/run。这样下一次构建会使用用户实际确认的澄清。

## 错误与身份

域错误位于 `error.data.code`，如 `revision_conflict`、`model_unavailable`、`author_busy`、`activity_missing`。JSON-RPC 错误码依次为 envelope `-32600`、参数 `-32602`、未知方法 `-32601`、域错误 `-32000`。provider 失败只返回清理后的失败类型。

本地 Author 端点面向可信人类/Agent 客户端。读取诊断、作者活动、active runtime revision、证据有效性及待授权补丁时分别呈现身份。协议 schema 可用 `uv run nexa open schema author-protocol` 从安装包读取。

---

[来源与验证](capability_inventory.md) · `open_author` / `open_revisions`
