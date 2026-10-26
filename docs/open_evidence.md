---
title: "证据与验收"
capabilities: [open_evidence]
language_versions: ["3.0"]
---

# 证据与验收

每个结果同时具有验收状态与证据有效性。验收要求在 policy 中冻结；证据记录绑定 candidate、policy、checker、dependencies、task、签发时间和可选过期时间。

| 记录 | 执行与判断 |
| --- | --- |
| `typecheck` | OCI 执行结果是否符合返回类型；每个 policy 的自动要求 |
| OutputCheck | 使用冻结 JSON 输入运行候选，与宿主持有的期望值比较 |
| RepositoryCheck | 在新 OCI 中应用 typed Patch，执行固定命令并检查退出码和输出 |
| model_review | 独立模型请求返回结构化 boolean 及 detail |
| ApprovalGrant | 用户对准确 proposal 的独立写入授权 |

一个通过的检查只覆盖其输入与 requirement。候选修改仓库测试后，控制器持有的验收 oracle 继续按原配置判断。模型评审与确定性检查分别计量、分别保留，界面应同时展示结果和证据状态。

## 有效性与更新

被撤销、已过期、来自未来时间、缺少所需依赖，或绑定不同 candidate/policy/input 的证据失效。同一个候选、策略和依赖上下文下，更新的失败会阻止旧成功继续满足要求。不同输入保留各自上下文。可变模型别名跨任务重新评审，人工决策绑定 task。

接纳产物、锁定重放、签发补丁授权及应用都通过 runtime 重新核验。源码 span 记录在对象中，语义 digest 排除 span；source content 有独立 hash，客户端需同时保留两种身份。

```sh
uv run nexa open evidence PROPOSAL_ID --environment environment.json --state .nexa/program.db
```

`PROPOSAL_ID` 使用实际运行返回值；Author `evidence/explain` 则接受 evidence object ID 及可选 context。排查时保留 requirement、失败 detail、对象 digest 与上下文；模型“认为已完成”的自然语言通过正式 policy 接纳后才产生可用结果。

---

[来源与验证](capability_inventory.md) · `open_evidence`
