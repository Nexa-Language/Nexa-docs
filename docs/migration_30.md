---
title: "从 2.4 迁移到 3.0"
capabilities: [open_migration, compilation, checkpoint]
language_versions: ["3.0", "2.4"]
---

# 从 2.4 迁移到 3.0

Nexa 3.0 同时接受显式 `language "3.0"` Open Programs 和已有 2.4 源码。无 language 声明的文件继续走 2.4 路径；`compile_source`/`compile_file` 继续返回 Python lowering，`compile_program` 是版本感知入口。旧页面与命令保留在[兼容快速入门](quickstart_24.md)。

## 按合同迁移源码

| 2.4 结构 | 3.0 目标 |
| --- | --- |
| 纯函数 / 计算 | 带类型的 goal，value 或 Python `solve(inputs)`，OCI 执行 |
| Agent prompt | intent、确定性 checks、独立 review |
| 工具暴露 / sandbox policy | 明确 capabilities 与 controller-owned adapter |
| `verify` / Protocol | 类型边界与冻结 OutputCheck / RepositoryCheck |
| 顺序 flow | build/runtime goal DAG，结果进入 inputs.dependencies |
| 运行期间改源码 | 子 revision → build → 检查点激活 |
| 写前审批 | 绑定准确 baseline、policy、evidence 的 PatchProposal / ApprovalGrant |
| 历史复用 | 有来源、实现条件与当前验收的 capsule |

3.0 维护子集支持 Int/Float/String/Bool/Json/Unit 与 Patch/Repository/ChangeRequest。任意 flow 控制、streaming callbacks、MCP session、动态工具导入、Actor、分布式状态与框架集成继续使用 2.4，或通过显式 adapter 迁移。Rust AVM 保留 2.4 子集。源码翻译需要审阅任务验收合同；prompt 与工具列表本身不足以确定固定检查。

## 归档旧状态

```sh
uv run nexa open migrate .nexa/runs.sqlite3 --target .nexa/open-archive.sqlite3
```

目标路径必须是新的。源库以 SQLite `mode=ro` 在读取事务中打开，包含已提交 WAL 内容。已知 RunState v1 行转为独立 3.0 数据库中的不可变 LegacyRunArchive，保留原状态与来源。报告包含逻辑快照 digest、run IDs、对象 digests 及逐行错误；不支持的 schema 明确报错，源库保持原样。

Archive 是静态归档。它不会创建 active Open Program、工具调用或新授权。`started` 工具结果登记为 `unknown_effects`，`resume_allowed=false`；对照原工具/provider 核实后再开始新的外部操作。旧批准绑定原 2.4 call，3.0 patch 需要新的准确 grant。

旧 checkpoint 留在原路径，继续通过 `nexa agent ... --resume RUN_ID` 恢复。3.0 runtime state migration 由 OCI 中的纯 Candidate 完成并验证目标 JSON schema，失败保留之前的 runtime head。源码 revision CAS 与 active revision 分别跟踪，见[修订与恢复](open_revisions.md)。

## 升级客户端与恢复源码同步

使用新的 Code/extension 前，保留源码、environment、状态库和 `.nx.lock`。Code 原有 `SourceSync` 记录格式与 ID 继续兼容；新的独立 write-intent 支持进程中断后的文件恢复。恢复时还要保留源码旁的 `.nexa-intent-<id>/`，从 `/status` 的 `source_recovery` 查看准确路径。`original` 保留原 inode，已有编辑器可能继续向它写入；先关闭相关编辑器并协调保留的修改，再归档恢复目录。旧版本中断且缺少 write-intent 时，按 `source_recovery_required` 手动恢复保留文件。源码同步保留替换字符串以外的 LF/CRLF、注释和合法参数。

修改 environment 后按客户端重新绑定。Code 在执行、inspect、grant 和 apply 等操作前核对原生语义 digest，允许语义相同的格式化或键顺序变化；语义漂移时重启 Code，再构建并生成、审阅对应证据。Extension Author 绑定私有快照，每次 RPC 实际发送前核对原文件内容，包括排队出队时。内容变化或文件不可用会使旧 client 失效；审阅配置后重新显式发起 Author 操作。自动 check 使用无 provider 的 client。已发出请求的进度按活动状态核对，取消使用准确活动 ID。具体命令与恢复入口见[开发工具链](toolchain.md)。

---

[来源与验证](capability_inventory.md) · `open_migration` / `compilation` / `checkpoint`
