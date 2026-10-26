---
title: "配置管理与标准库入口"
capabilities: [configuration, stdlib]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    本页说明保留的 2.4 语言与运行时路径，无版本声明的源码继续使用此入口。新 Open Programs 从 [Nexa 3.0](quickstart.md) 开始，合同差异见[迁移指南](migration_30.md)。

# 配置管理与标准库入口

配置分为模型与凭据、编译检查模式，以及运行预算。把这些边界分别设置，有助于复现和诊断。

## 首次配置 {#first-provider-setup}

下面配置适用于提供 OpenAI 兼容 Chat API 的服务；使用 Responses 时还需确认服务支持该协议。在 `analyst.nx` 所在工作目录新建 `secrets.nxs`：

```text
config default {
    BASE_URL = "https://your-provider.example/v1",
    MODEL_NAME = {
        "strong": "openai/YOUR_MODEL_ID",
        "weak": "openai/YOUR_MODEL_ID",
        "super": "openai/YOUR_MODEL_ID"
    }
}
```

将 `BASE_URL` 替换为服务商提供的 API 根地址，将三处 `YOUR_MODEL_ID` 替换为你有权使用的模型 ID。首次配置可以让三个档位使用同一模型；未显式指定 `model` 的 Agent 使用 `strong`。`openai/` 是 Nexa 的 provider 选择前缀，请求发送时会去掉该前缀。

优先通过既有 secret manager 注入 `API_KEY`，或在上述 `openai/...` 配置下使用 `OPENAI_API_KEY`。示例文件故意省略 `API_KEY` 字段；已有 `.nxs` 中的显式凭据可能优先于环境值，应同时检查父目录配置。密钥留在运行环境，不写入 `.nx`、日志或 Git。

如果还没有环境注入，在本地交互终端中运行下面的命令。它隐藏密钥输入，仅把密钥传给子进程，然后执行[快速入门](quickstart_24.md)中的 `analyst.nx`。此步骤会发起真实模型请求；先完成 endpoint 和模型占位符替换。

```sh
uv run python - <<'PY'
import getpass
import os
import subprocess

environment = os.environ.copy()
environment["API_KEY"] = getpass.getpass("Provider API key: ")
command = ["nexa", "agent", "analyst.nx", "Analyst",
           "Explain the supplied evidence", "--timeout", "120"]
raise SystemExit(subprocess.run(command, env=environment).returncode)
PY
```

已有 secret manager 注入时，可直接执行 `uv run nexa agent analyst.nx Analyst "Explain the supplied evidence" --timeout 120`。需要仅检查程序时，运行 `uv run nexa validate analyst.nx --json`；该检查无需密钥，也不会发起 provider 请求。

## 选择命名配置

`.nxs` 还支持扁平配置和命名 `config` block。把上例的 `default` 改为 `development`，就建立了下例所选择的配置。`use config name;` 只选择已有 block：

```nexa
use config development;
agent Analyst {
    prompt: "Analyze supplied evidence."
}
```

`.nxs` 从当前目录或声明脚本目录向上查找，最多 10 层；父目录先合并，同名配置以最近目录为准。配置文件在模块初始化及脚本加载时读取，provider 客户端在首次模型调用时创建。Chat/Responses 使用现有 provider 配置；原生 Anthropic 使用 `ANTHROPIC_API_KEY` 和可选 `ANTHROPIC_BASE_URL`。不要把凭据打印到日志或提交到 Git。

## 工具暴露

`uses std.fs`、`uses std.shell` 等 namespace 展开为标准库工具集。选择与任务相关的最小集合；注册工具与暴露给 Agent 是两个步骤。自定义工具按[工具指南](part3_extensions.md)声明。

## 静态检查与运行预算

- `--harness strict|warn|off` 控制 Harness 编译诊断。
- `nexa lint` 使用渐进式类型检查；`--strict` 要求缺失注解成为错误。
- `RunConfig` 控制实际模型、工具、token 和时间预算，见[执行指南](runtime_execution.md)。

具体工具签名见[标准库 API](stdlib_reference.md)。终端 UI 需要可选 `terminal` extra；MCP 需要 `mcp` extra。

---

[来源与验证](capability_inventory.md) · `configuration` / `stdlib`
