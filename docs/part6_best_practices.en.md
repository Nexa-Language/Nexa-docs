---
title: "Build inspectable Agent programs"
capabilities: [tools, execution, verification, cache]
---

# Build inspectable Agent programs

Establish a complete end-to-end path, then add constraints for actual risks. This sequence supports moving from a prototype to a maintainable application.

1. Define the objective, input, output schema, and acceptance criteria.
2. Expose the smallest useful tool set and distinguish reads from risky side effects.
3. Set explicit time, model-call, tool-call, and token budgets.
4. Save `RunState`, events, and checkpoints; remove credentials from logs.
5. Test completion, approval/denial, cancellation, timeouts, exhaustion, unknown outcomes, and recovery.
6. Verify mechanisms with fixed fixtures, then evaluate task quality with the chosen model.

## Context and caching

Manage Chat history by complete turns and preserve tool protocol pairs. Retain opaque native-provider items. Exact caching applies to fresh Chat runs without tools; measure hit rate on the actual workload.

## Tool failures

Reject invalid arguments before side effects. Raise `ToolOutcomeUnknown` for uncertain network or shell outcomes so callers can verify them. Preserve failures instead of wrapping them as ordinary success text.

## Regression evidence

Record source version, environment, fixture, assertions, and results. Successful compilation, offline semantics, and real-model quality are separate acceptance items. This site's [capability/example inventory](capability_inventory.md) provides one working pattern.

---

[Source and validation](capability_inventory.md) · `tools` / `execution` / `verification` / `cache`
