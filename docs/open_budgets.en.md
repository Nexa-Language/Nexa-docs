---
title: "Budgets and stopping states"
capabilities: [open_execution]
language_versions: ["3.0"]
---

# Budgets and stopping states

Build and runtime phases within one command share model call count, cumulative tokens, and a deadline. Set budgets explicitly before resolution and retain observed usage. Locked replay consumes no model requests.

```sh
uv run nexa build examples/open_programs/sum.nx --environment examples/open_programs/aliyun.json --state .nexa/sum.db --max-model-calls 4 --max-tokens 16000 --timeout 90 --json
```

| Control | Default and rule |
| --- | --- |
| `--max-model-calls` | 4; hard cap; implementation and model review requests both count |
| `--max-tokens` | 20000; cumulative provider-reported input/output tokens |
| `--timeout` | 120 seconds; shared deadline; each OCI call is limited to 30 seconds |
| `ResolutionBudget.max_output_tokens` | SDK default 4096; each request is also capped by remaining token budget |

Input usage becomes observable after the provider returns. Missing usage blocks admission with `usage_unreported`; excess cumulative usage returns `model_token_budget`. A failed request still consumes its initiated call. Calculate cost separately against the actual model and price baseline.

## Handle a stop

`model_call_budget`, `model_token_budget`, and `resolution_timeout` identify the exhausted budget. Preserve existing candidates, evidence, and activity records before choosing the next operation. `clarification_required` needs an author answer followed by [source synchronization](open_author_protocol.md). `cancelled` follows cooperative cancellation of an exact activity ID.

Cancellation is durable. An ongoing provider/OCI call checks it after returning or timing out, then stops subsequent steps. Check client process termination and the runtime's durable activity state separately; see [recovery](open_revisions.md).

---

[Source and validation](capability_inventory.md) · `open_execution`
