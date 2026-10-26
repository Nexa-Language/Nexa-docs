---
title: "开发工具链"
capabilities: [ecosystem, cli, open_author, open_revisions, open_grants]
language_versions: ["3.0", "2.4"]
---

# 开发工具链

Nexa 3.0 的 CLI、Nexa Code 与 VS Code 扩展共享原生合同、修订和验收规则。工具负责显示和编排，权限、CAS 和 evidence 由 runtime 判断。本文对应 Nexa Code `3.0.0.dev0` / Ink `3.0.0-dev.0`、extension `0.3.0` 的本地源码与安装包；安装步骤使用各仓库当前构建说明。

## CLI

按[快速入门](quickstart.md)安装 Nexa 3.0.0。3.0 文件用 `check --json` 自动检查；显式 build/run 才进入 OCI 与模型求解。无版本声明的 2.4 文件继续用 `validate`、`inspect`、`agent`。完整参数见 [CLI 参考](cli_reference.md)。

## Nexa Code

[Nexa-Code](https://github.com/Nexa-Language/Nexa-Code) 提供 Python host 与 Ink/React 终端。按仓库安装说明准备 Python 3.10+、uv、Node.js 20+ 和 pnpm 10.18.3，再构建 Ink。从 Nexa-Code 仓库启动：

```sh
./nexa-cc.sh --cwd /absolute/project --program sum.nx --environment sum.environment.json --state .nexa/open-programs.sqlite3 --program-id sum-demo --max-model-calls 4 --max-tokens 20000 --timeout 120
```

`--program` 显式打开原生 Open Program 入口；省略它保留旧 Agent 会话。`--environment` 必须指向已审阅配置，路径从 `--cwd` 解析；`--docker-context` 可选。`uv run nexa-code-engine` 提供相同 flags 的 JSON Lines host 入口。终端展示 environment、预算、goal/obligation、草稿与 active revision、活动、证据和 proposal diff。

Code 的预算作用于每次显式操作，`/build` 与 `/run` 分别计量。`/build` 会构建并激活修订；新的作者草稿先 `/draft`，再 `/resolve`。`/sync` 和 `/approve` 展示具体 diff/提案后要求 `y/n` 确认。

Code 在 build、执行、Author resolve、proposal inspect、grant、apply 和 runtime resume 前，通过原生 environment loader 重新读取配置，并与会话绑定的语义 digest 比较。检查器、镜像、capabilities 或 provider binding 变化会返回 `environment_changed`；文件缺失或无效会返回 `environment_unavailable`。JSON 格式化或键顺序变化在语义相同时允许继续。遇到漂移后，重启 Code 绑定审阅后的 environment，再构建并重新生成、审阅相关证据。`/check`、`/status`、准确取消和 patch recovery 仍可使用。这些核验发生在新操作进入 runtime 前；已运行活动通过其准确 ID 查看状态或取消。

以下是已实现的原生命令形态，ID 均取自当前真实输出：

```text
/check
/draft
/build
/locked
/status
/resolve total {}
/cancel author ACTIVITY_ID
/answer CLARIFICATION_ID Answer text
/sync SYNC_ID
/reject-sync SYNC_ID
/proposal PROPOSAL_ID
/approve PROPOSAL_ID local-operator
/apply PROPOSAL_ID GRANT_ID
/recover PROPOSAL_ID
/import repair.capsule.json
```

`/run <goal> [JSON]` 运行选中的 runtime goal；`/maintain {"paths":["calc.py"],"request":"Fix add"}` 提出维护补丁，JSON 可增加 `event` 和导入后的 `capsule_id`。`/revise` 构建并激活修订，`/resume` 恢复控制器。`/cancel runtime ACTIVITY_ID` 取消准确 runtime 活动，作者活动使用 `author`。Capsule 导出使用 `/export`，JSON 包含 path、activity_id、source、creator、license。保留的 2.4 `/permissions` 与工具批准作用于旧会话；3.0 Apply 要求准确 grant。

Code 的源码同步只替换目标 goal 内的 intent 字符串，并核对替换后的完整 ProgramIR。其余字节保持原样，包括 LF/CRLF、注释与名为 `intent` 的合法参数。原有 `SourceSync` 记录格式和 ID 保持兼容；独立持久 write-intent 在移动源码前登记恢复目录。进程中断后，启动、`/check`、`/status` 和 `/sync` 会恢复文件阶段；完成原生修订仍需 `/sync` 的显式确认。

`/status` 与原生面板的 `source_recovery` 显示 `original_path`、`temporary_path`、`state` 和 `sync_id`。源码旁的 `.nexa-intent-<id>/original` 保留原 inode，以及已打开该 inode 的编辑器后续保存的内容；成功同步后仍保留。恢复时将这些目录与状态库一起保存，先审阅原副本和当前源码的差异，再继续同步。恢复会保留已存在的用户文件。相关编辑器关闭、保留的修改已保存或协调完成后，再手动归档恢复目录。旧版本中断若缺少 write-intent，会报告 `source_recovery_required`，需人工确认并恢复保留的文件。

## VS Code 0.3.0

[Nexa-extension](https://github.com/Nexa-Language/Nexa-extension) 的本地 VSIX 包含最小只读 Python SDK bridge。开发打包需要 Node.js 22+、pnpm，VS Code API 基线为 1.96。安装后，在资源所属 workspace 设置明确 CLI 与装有 Nexa 3.0.0 的 Python 路径：

```json
{
  "nexa.executablePath": "/absolute/path/to/Nexa/.venv/bin/nexa",
  "nexa.executableArgs": [],
  "nexa.open.pythonPath": "/absolute/path/to/Nexa/.venv/bin/python",
  "nexa.open.pythonArgs": [],
  "nexa.open.environment": "sum.environment.json",
  "nexa.open.state": ".nexa/open-programs.sqlite3",
  "nexa.open.programId": "sum-demo",
  "nexa.open.maxModelCalls": 4,
  "nexa.open.maxTokens": 20000,
  "nexa.open.timeoutSeconds": 120
}
```

`nexa.open.pythonPath` 必须显式配置，扩展启动时核对版本和能力。`pythonArgs` 默认 `[]`；不执行 shell 展开、不自动安装 Python。environment、state 等相对路径从当前资源所属根目录解析，适用于多根 workspace。environment 推荐命名 `*.environment.json`，JSON schema 同时关联 `*.nx.lock`、`*.capsule.json`、`*.program.json`、`*.patch.json`。

| 设置 | 默认值 / 作用 |
| --- | --- |
| `nexa.open.environment` | 空；显式 build/resolve/run/apply 需要 |
| `nexa.open.state` | `.nexa/open-programs.sqlite3` |
| `nexa.open.programId` | 空；回退源码文件 stem |
| `nexa.open.pythonPath` / `pythonArgs` | 空 / `[]`；显式 bridge 解释器与参数 |
| `nexa.open.capsule` | 空；为 run/maintenance 显式选择导入 capsule digest |
| `nexa.open.dockerContext` | 空；沿用 Docker context |
| `nexa.open.maxModelCalls` / `maxTokens` / `timeoutSeconds` | `4` / `20000` / `120` 秒 |

原 `Nexa: Build` / `Nexa: Run`（`nexa.build` / `nexa.run`）按版本路由。新命令可在 Command Palette 查找：

| Command ID | 标题 |
| --- | --- |
| `nexa.open.check` | Nexa: Check Open Program |
| `nexa.open.buildLocked` | Nexa: Build Locked Open Program |
| `nexa.open.resolve` | Nexa: Resolve Goal |
| `nexa.open.revise` | Nexa: Revise and Activate Program |
| `nexa.open.maintain` | Nexa: Maintain Repository |
| `nexa.open.status` | Nexa: Refresh Open Program Status |
| `nexa.open.cancel` | Nexa: Cancel Activity |
| `nexa.open.answer` | Nexa: Answer Clarification |
| `nexa.open.syncSource` | Nexa: Synchronize Clarification Source |
| `nexa.open.proposal` | Nexa: Review Exact Patch |
| `nexa.open.apply` | Nexa: Authorize and Apply Exact Patch |
| `nexa.open.recover` | Nexa: Recover Open Program or Patch |
| `nexa.open.resumeApply` | Nexa: Resume Exact Patch Application |
| `nexa.open.capsuleImport` | Nexa: Import Capsule |
| `nexa.open.capsuleExport` | Nexa: Export Activity Capsule |

3.0 diagnostics 来自 CheckReport，Outline 来自 ProgramIR 的真实 spans。自动检查使用无 provider 的 check client，为零模型、零候选执行。Restricted Mode 只提供静态语法和 snippets；信任 workspace 后才可启动 CLI/Author/bridge。各进程使用该资源的配置，关闭/修改文档后丢弃迟到结果。

显式 Author 操作绑定私有 environment 文件快照。每次实际发送 RPC 前都会核对原配置文件内容，包括排队请求出队发送时；内容变化、替换为不同内容或删除会使旧 client 失效，并拒绝该请求。确认当前配置后，再显式发起 Author 操作以创建新 client。这里按文件内容比较，重新格式化也会触发重新绑定。核验边界是发送新请求；已发送请求的进度与终态按活动状态核对。

## 两个客户端共有的状态规则

回答澄清会产生数据库子草稿。客户端先读取新 IR，展示目标 intent 的源码 diff；用户确认后校验 source digest/document version，写入、重新 check 并按准确 CAS 同步。冲突、拒绝或退出保留待同步状态，旧文件的 build/run 需等待同步完成，包括另一客户端发起的澄清。

作者活动与 runtime 活动分别列出，按用户选择的准确 ID 取消。接受候选、证据有效、准确 grant 与应用成功分别显示。Apply 前查看实际 diff；状态过期、文件变化或 evidence 失效时按 runtime 返回重新处理。恢复与未知副作用见[修订指南](open_revisions.md)。
