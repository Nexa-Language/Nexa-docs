---
title: "Large outputs and artifacts"
capabilities: [artifacts]
---

# Large outputs and artifacts

When a tool result exceeds `RunConfig.max_tool_output_chars`, the runtime stores the complete content in `artifact_directory`, defaulting to `.nexa/artifacts`. The model receives a bounded preview, content hash, and the `__nexa_read_artifact` tool name.

## Configure the threshold

```python
from src.runtime.run_state import RunConfig

config = RunConfig(
    max_tool_output_chars=4000,
    artifact_directory=".nexa/artifacts",
)
```

The threshold counts characters and has a minimum of 256. Content is identified by its hash. The model uses `__nexa_read_artifact` to retrieve bounded slices by character offset. These reads also consume the tool-call budget.

## Operational guidance

- Return enough summary to help the model choose useful slices.
- Retain the artifact directory until related runs and recovery work finish.
- Treat text offsets as characters, keeping them distinct from UTF-8 byte positions.
- Apply the task-data policy to artifacts, checkpoints, and traces together.

See the [capability inventory](capability_inventory.md) for behavior checks and source evidence.

---

[Source and validation](capability_inventory.md) · `artifacts`
