---
title: "准确补丁授权与应用"
capabilities: [open_grants, open_evidence, open_revisions]
language_versions: ["3.0"]
---

# 准确补丁授权与应用

维护任务产生 PatchProposal，其中包含准确 diff、工作区基线、策略及证据。用户审查后签发 ApprovalGrant，再用准确 grant ID 应用。模型、2.4 tool approval 和旧 bypass 配置均不签发此授权。

## 从提案到应用

在临时演示仓库放入 `calc.py`，令 `add(a, b)` 当前返回错误的差值；发行环境的固定检查期望 `5` 与 `-5`。下面的显式操作会调用已配置模型，并在 OCI 中执行候选和回归检查。

```sh
uv run nexa run examples/open_programs/maintain.nx --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db --program-id demo --repository /absolute/path/to/repository --include calc.py --request 'Fix calc.add to return the mathematical sum.' --json
uv run nexa open evidence PROPOSAL_ID --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db
uv run nexa open approve PROPOSAL_ID --actor local-operator --state .nexa/maintain.db
uv run nexa open apply PROPOSAL_ID --grant GRANT_ID --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db
```

先阅读实际返回的 diff 与每项 evidence；将返回的 proposal/grant ID 原样用于后续命令。Grant 绑定 proposal、路径作用域、baseline、policy、evidence、task 和 expiry。每次 apply 重新核验这些约束。`--actor` 记录可信本地客户端的操作者，本地状态库是信任边界。候选容器无法访问该库。多用户身份认证由外部服务另行建立。

## 并发修改与中断

应用前后检查文件基线；旧文件先原子移入同目录 `.nexa-preserved-*/original`，核对内容后用排他创建安装新文件。删除也保留原文件。写前 journal 的 `preserved` 字段记录恢复路径，源码快照会排除这些内部目录。

`workspace_conflict` 时，保留并核对用户内容，按当前工作区重新提出补丁。中断后执行：

```sh
uv run nexa open recover PROPOSAL_ID --state .nexa/maintain.db
uv run nexa open apply PROPOSAL_ID --grant GRANT_ID --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db --resume
```

先核对 recover 结果再 resume。恢复识别已经完成的写入，也可还原移走原文件后中断的基线。成功后原 inode 仍被保留；编辑器沿旧文件描述符写入的内容留在恢复文件，后续 recover 会报告差异。确认后由用户归档或清理恢复目录。跨文件写入采用 journal，存储量约等于修改量；文件名切换有短暂空窗，应用时协调编辑器与构建器。

---

[来源与验证](capability_inventory.md) · `open_grants` / `open_evidence` / `open_revisions`
