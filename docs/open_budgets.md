---
title: "预算与停止状态"
capabilities: [open_execution]
language_versions: ["3.0"]
---

# 预算与停止状态

一个命令中的 build 与 runtime 阶段共享模型调用次数、累计 token 和截止时间。预算先于求解显式设置，日志保留实际 usage；固定重放无需模型预算消费。

```sh
uv run nexa build examples/open_programs/sum.nx --environment examples/open_programs/aliyun.json --state .nexa/sum.db --max-model-calls 4 --max-tokens 16000 --timeout 90 --json
```

| 控制项 | 默认值与规则 |
| --- | --- |
| `--max-model-calls` | 4；硬上限；实现请求和模型评审都计数 |
| `--max-tokens` | 20000；累计 provider 报告的 input/output token |
| `--timeout` | 120 秒；共享 deadline；每次 OCI 至多 30 秒 |
| `ResolutionBudget.max_output_tokens` | SDK 默认 4096；每次请求还受剩余 token 预算限制 |

provider 返回后才能观察 input usage。缺少 usage 会以 `usage_unreported` 阻止接纳；超出累计预算返回 `model_token_budget`。请求失败仍占用已发起的调用次数。费用需结合具体模型与价格基准单独计算。

## 处理停止

`model_call_budget` / `model_token_budget` / `resolution_timeout` 表示耗尽对应预算；保留已经产生的候选、证据和活动记录后再决定下一次操作。`clarification_required` 需要作者回答，按[源码同步](open_author_protocol.md)收敛。`cancelled` 来自对准确 activity ID 的协作取消。

取消请求持久保存，正在执行的 provider/OCI 调用在返回或超时后检查取消状态，随后停止后续步骤。终止客户端进程的即时状态与 runtime 的持久活动状态应分别核对，见[恢复](open_revisions.md)。

---

[来源与验证](capability_inventory.md) · `open_execution`
