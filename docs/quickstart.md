---
title: "开始使用 Nexa 2.4"
capabilities: [compilation, execution]
---

# 开始使用 Nexa 2.4

先运行一个无需模型的程序，再编译 Agent。本文使用已发布的 [Nexa v2.4.0](https://github.com/Nexa-Language/Nexa/releases/tag/v2.4.0)。

## 1. 安装运行时

需要 Git、Python 3.10+ 和 uv。在工作目录中取得发行源码，并安装锁定的依赖：

发行 tag `v2.4.0` 对应已验证的 [commit c216263](https://github.com/Nexa-Language/Nexa/commit/c2162637236e4a73feea410c4183672411666521)。

```sh
git clone --branch v2.4.0 --depth 1 https://github.com/Nexa-Language/Nexa.git
cd Nexa
uv sync --locked
uv run nexa --version
```

确认输出为 `Nexa v2.4.0`。后续命令均在这个源码目录执行。

## 2. 运行第一个程序

保存为 `hello.nx`。本例的编译和执行都无需凭据，结果为 `12`。

```nexa
flow main {
    first = 3;
    print(first * 4);
    result = first * 4;
}
```

```sh
uv run nexa validate hello.nx --json
uv run nexa run hello.nx
```

`validate` 返回结构化诊断；`run` 编译并执行程序。需要查看生成物时运行 `uv run nexa build hello.nx`，生成 `hello.py`。

## 3. 定义第一个 Agent

保存为 `analyst.nx`。这是完整声明模块，编译不访问模型。

```nexa
agent Analyst {
    prompt: "Work from evidence. State assumptions explicitly."
    timeout: 120
    max_tool_calls: 4
}
```

```sh
uv run nexa build analyst.nx
uv run nexa inspect analyst.nx --format json
```

执行 Agent 前，完成[首次 provider 配置](part2_config_stdlib.md#first-provider-setup)：创建含 endpoint 和模型 ID 的 `secrets.nxs`，通过环境或隐藏输入提供密钥。协议差异见[模型协议](runtime_providers.md)。下面的命令使用已配置的环境发起模型请求，并将运行状态写入 `.nexa/runs.sqlite3`。

```sh
uv run nexa agent analyst.nx Analyst "Explain the supplied evidence" --timeout 120
```

完成时返回 `status: completed`。等待工具审批时返回 `waiting_approval`，按[审批与恢复](runtime_approval.md)处理；其他停止状态按[执行与预算](runtime_execution.md)排查。

## 4. 选择下一步

- 学习[语言基础](part1_basic.md)和[工具声明](part3_extensions.md)。
- 用[checkpoint](runtime_checkpoints.md)保存与恢复任务。
- 通过[工具链](toolchain.md)接入 Nexa Code 或 VS Code。
- 从旧版本迁移时，先核对[2.4 迁移清单](migration_24.md)。

---

[来源与验证](capability_inventory.md) · `compilation` / `execution`
