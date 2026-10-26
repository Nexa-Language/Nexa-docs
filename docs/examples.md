---
title: "可验证示例"
capabilities: [compilation, harness, tools, actors]
language_versions: ["3.0", "2.4"]
---

# 可验证示例

按版本选择原生 3.0 检查、真实 OCI 场景或 2.4 兼容示例。准确数量与检查规则见[能力证据](capability_inventory.md)。

## Open Programs 3.0

| 程序 | 实际验证 |
| --- | --- |
| [Answer](quickstart.md) | 原生检查、OCI 输出 `42`、通过证据、零请求锁定重放 |
| [Sum](open_programs.md) | 原生检查、fixture 提案和评审、OCI 输出 `0`、冻结求和用例、零请求锁定重放 |
| [首页](index.md) | 仅原生合同检查；check 期间无模型或 OCI |

## 2.4 兼容示例

| 主题 | 示例入口 | 文档校验 |
| --- | --- | --- |
| 算术与变量 | [第一个程序](quickstart_24.md) | 编译 + 离线结果 `12` |
| 模型调用 | [Echo](part1_basic.md) | 编译 + 固定回复 `hello` |
| 顺序管道 | [Researcher → Summarizer](part2_advanced.md) | 编译 + 固定两次回复 |
| 真实本地工具 | [add](part3_extensions.md) | 编译 + 工具调用 + 结果 `5` |
| Protocol | [Answer](part3_extensions.md) | 编译 + 结构化结果 |
| flow 快照 | [snapshot/restore](part2_harness.md) | 编译 + 恢复结果 `3` |
| 验证失败 | [verify](part2_harness.md) | 编译 + 预期失败 |
| Actor 邮箱 | [spawn/pass/await](runtime_actors.md) | 编译 + 两次消息与最后结果 |
| 模式匹配 | [match](part2_pattern_matching.md) | 编译 + 结果 `one` |
| Rust 共同子集 | [除法](runtime_rust.md) | Python 离线结果 `2.5`；Rust 来源见共同 fixture |

## 主仓库示例状态

`examples/manifest.json` 为每个主仓库 `.nx` 示例记录 `compiled`、`open_programs` 或具体 `historical_drafts` 原因。`compiled` 记录意味着完整编译通过；执行还可能需要模型、文件、MCP 服务或其他环境。选择具体例子时同时检查环境要求。

本站 [inventory.json](inventory.json) 对每个文档块记录 SHA-256、页面、块序号、验证模式和 fixture。`partial`/`historical` 必须有逐例原因并在页面可见；未登记或内容漂移会令校验失败。

---

[来源与验证](capability_inventory.md) · `compilation` / `harness` / `tools` / `actors`
