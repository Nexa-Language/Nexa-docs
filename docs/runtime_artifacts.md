---
title: "大结果与 Artifact"
capabilities: [artifacts]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 大结果与 Artifact

工具结果超过 `RunConfig.max_tool_output_chars` 时，运行时将完整内容存入 `artifact_directory`，默认 `.nexa/artifacts`。模型接收受限预览、内容 hash 与 `__nexa_read_artifact` 工具名。

## 配置阈值

```python
from src.runtime.run_state import RunConfig

config = RunConfig(
    max_tool_output_chars=4000,
    artifact_directory=".nexa/artifacts",
)
```

阈值按字符计数，最小值为 256。Artifact 内容以 hash 标识。模型通过 `__nexa_read_artifact` 按字符偏移读取有限片段；读取请求同样进入工具调用预算。

## 使用原则

- 返回足够的摘要，帮助模型选择需要读取的片段。
- 保留 artifact 目录，直到相关运行和恢复工作完成。
- 以字符偏移处理文本切片，避免将字符位置当作 UTF-8 字节位置。
- 将 artifact、checkpoint 和 trace 一并按任务数据策略管理。

具体行为与源码依据见[能力清单](capability_inventory.md)。

---

[来源与验证](capability_inventory.md) · `artifacts`
