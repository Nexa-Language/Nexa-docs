---
title: "CLI 命令参考"
capabilities: [cli, compilation, checkpoint]
---

# CLI 命令参考

以下命令以本地 2.4 checkout 内的 `uv run nexa` 为入口。CLI 在 `src/cli.py` 定义；执行 Agent 的持久化路径由 `src/agent_cli.py` 实现。

## 编译与检查

| 命令 | 行为 |
| --- | --- |
| `nexa --version` | 输出运行时版本 |
| `nexa build FILE [--harness strict\|warn\|off]` | 生成相邻 `.py` 文件；默认 warn |
| `nexa run FILE [--harness strict\|warn\|off]` | 编译并执行；默认 warn |
| `nexa inspect FILE [--format json\|text]` | 通过统一模块加载器读取结构；默认 JSON |
| `nexa validate FILE [--json] [--quiet]` | 输出语法与语义诊断 |
| `nexa harness-check FILE [--harness strict\|warn\|off] [--json]` | Harness 检查；默认 strict |
| `nexa lint FILE [--strict] [--warn-untyped]` | 渐进式类型检查 |
| `nexa test FILE` | 编译并执行语言测试 |
| `nexa intent check FILE [--intent FILE] [--verbose]` | 按 pass/fail/skip/error 检查意图 |
| `nexa intent coverage FILE [--intent FILE]` | 查看意图覆盖情况 |

`build` 编译失败返回 `1`。`run` 透传生成程序的返回码，中断返回 `130`。`validate` 发现无效程序时返回 `1`；需要脚本化判定时使用此命令。`inspect` 的 JSON 面向结构消费，解析失败时也可能返回带诊断的结构信息；其中的语法版本元数据与 `nexa --version` 输出的运行时版本用途不同。

`test` 执行生成模块中的 `test_` 函数，有失败时返回 `1`；未发现测试函数时输出提示并返回 `0`。`intent` 的 `--intent` 未指定时会自动寻找对应的 `.nxintent` 文件。

## Agent 运行与恢复

```sh
uv run nexa agent analyst.nx Analyst "Analyze evidence" --timeout 120 --max-tool-calls 4
uv run nexa agent analyst.nx Analyst --resume RUN_ID --approve CALL_ID
uv run nexa agent analyst.nx Analyst --resume RUN_ID --deny CALL_ID
```

`analyst.nx` 采用[快速入门](quickstart.md)中的完整声明。首次模型调用需要 provider 配置。`RUN_ID`、`CALL_ID` 来自该次运行的 JSON 输出。

| 参数 | 默认与规则 |
| --- | --- |
| `FILE NAME [TASK]` | 文件、Agent 名称、初始任务；新运行必须提供 TASK |
| `--checkpoint PATH` | `.nexa/runs.sqlite3` |
| `--resume RUN_ID` | 恢复原运行，禁止同时传入新 TASK |
| `--approve CALL_ID` / `--deny CALL_ID` | 互斥，只能与 resume 一起使用 |
| `--timeout SECONDS` | 300；恢复使用 checkpoint 中的配置 |
| `--max-tool-calls COUNT` | 20；恢复保留已用预算 |

JSON 字段包括 `run_id`、`status`、`output`、`error`、模型/工具次数、输入/输出 token 数及 `pending_calls`。返回码：完成 `0`，等待审批 `2`，其他停止状态 `1`。新的对话轮次使用 Python [continue_run](runtime_conversations.md)。

## 服务与后台任务

| 命令 | 参数、输出与作用 |
| --- | --- |
| `nexa serve FILE [--port PORT]` | 编译后启动生成程序；端口覆盖通过 `NEXA_PORT` 传入，返回码透传，Ctrl+C 返回 `130` |
| `nexa routes FILE [--json]` | 列出声明的服务器路由；JSON 按服务器输出；无服务器声明时输出提示文字 |
| `nexa jobs list [--status STATUS] [--limit N]` | 表格输出，默认最多 50 条；状态可选 pending/running/completed/failed/dead/cancelled/expired |
| `nexa jobs status ID` | 输出一个任务的状态；不存在时输出提示 |
| `nexa jobs cancel ID` | 尝试取消任务；输出成功或当前状态不可取消的提示 |
| `nexa jobs retry ID` | 将死信任务重新移入 pending 队列 |
| `nexa jobs clear` | 清理 completed/expired/cancelled 记录并输出数量 |
| `nexa workers start FILE [--worker-id ID] [--poll-interval SECONDS]` | 编译并导入任务定义后启动 worker；ID 默认 `worker-1`，轮询间隔默认 1.0 秒 |
| `nexa workers status` | 输出当前进程中的队列与 worker 状态 |
| `nexa cache clear` | 删除当前目录下的 `.nexa_cache`；目录不存在时输出提示 |

任务队列默认使用内存后端，跨进程共享与持久化需要程序配置相应后端。`jobs status/cancel/retry` 的业务失败目前通过文字输出，未设置非零返回码；自动化需要读取结果或使用任务 API。遇到错误时保留原始诊断，按[故障排查](troubleshooting.md)定位。

---

[来源与验证](capability_inventory.md) · `cli` / `compilation` / `checkpoint`
