# Nexa documentation

Nexa 2.4 的中英文文档。站点保留 MkDocs Material 与 suffix i18n，覆盖语言、Python 参考运行时、Rust 子集、CLI 和开发工具链。当前内容基于已发布的 [Nexa v2.4.0](https://github.com/Nexa-Language/Nexa/releases/tag/v2.4.0)，验证与 CI 固定到下文的完整源码 commit。

- 中文入口：`/quickstart/`；English: `/en/quickstart/`。
- 首次调用模型前，按配置页创建只含 endpoint/模型信息的 `secrets.nxs`，通过环境或隐藏输入提供密钥：[中文配置](docs/part2_config_stdlib.md) / [English setup](docs/part2_config_stdlib.en.md)。
- `docs/inventory.json` 登记页面、能力来源和每个 Nexa 示例。
- `docs/stdlib-api.json` 保存运行时标准库参数 schema；中英文 API 表从该快照对应的 registry 生成。
- `docs/stylesheets/extra.css` 管理 graphite/paper 色彩、排版、间距、边框与响应式 token。字体使用系统字体；站点没有模型后端、远程字体或自动加载的评论脚本。

## 本地预览

文档环境需要 Python 3.11+ 和 uv；本次验证使用 Python 3.12、uv 0.11.30。文档依赖与 Nexa 运行时环境分别管理。

```sh
uv sync --locked
uv run --no-sync mkdocs serve
```

访问 `http://127.0.0.1:8000`。严格生成静态站点：

```sh
uv run --no-sync mkdocs build --strict
```

## 完整验证

先在已经取得的 Nexa 2.4 源码目录运行 `uv sync --locked`，再回到本仓库：

```sh
uv run --no-sync python -m scripts.verify --runtime /path/to/Nexa
```

可用 `--runtime-python /path/to/venv/bin/python` 指定装有 Nexa 依赖的解释器。默认使用 `Nexa/.venv/bin/python`。验证依次执行：

1. 页面登记、Nexa 代码块 hash、可见豁免理由、中英文能力配对、导航及 CSS 资源检查。
2. 校验器回归测试、ruff、isort、ty。
3. MkDocs 严格构建及生成 HTML 的内部链接、锚点、图像、脚本与样式检查。
4. 源码/test fingerprint 核对、全部完整 Nexa 示例编译、登记为 offline 的代表性程序执行、标准库参考与真实 registry 比对。

示例子进程使用临时工作目录、临时 HOME/TMPDIR 和最小环境；不继承 provider 凭据或 Python 用户配置。在任何 Nexa import 前，audit hook 禁止网络访问和 `.nxs` 读取。固定回复只替换模型客户端边界，编译器、SDK、flow、工具和输出校验仍执行实际实现。该工具用于审核过的仓库示例，不是运行任意不可信程序的沙箱。

报告写入 `.reports/docs-check.json`，包含实际编译/执行数量、逐例状态与错误。失败返回非零。单独运行结构与站点检查可省略 `--runtime`；报告会明确记录 `runtime_validation: not_requested`。

```sh
uv run --no-sync python -m scripts.verify
uv run --no-sync python -m scripts.check_docs --runtime /path/to/Nexa --site site
```

外部 URL、真实模型质量、服务连通性、发布和视觉效果分别验收。网页使用 Material 的搜索、语言切换、主题切换、移动导航与复制代码功能。

## 更新页面与证据

页面成对保存为 `topic.md` / `topic.en.md`，front matter 的 `capabilities` 对应 inventory 中的能力 ID。将中文路径加入 `mkdocs.yml` 的导航，并为导航标签提供英文翻译。原有页面路径保留，历史或规划内容必须在正文标明状态。

每个 `nexa` / `nx` fence 单独登记：页面、块序号、稳定 ID、源码 SHA-256、状态和验证模式。完整示例必须 `compile`；需要检查输出、调用次数、错误或 Actor 消息顺序的例子配置 `offline` scenario。`partial` / `historical` 必须有逐例原因，并在页面显示同一句原因。校验器拒绝未登记代码，不能用整页豁免绕过。

新增记录先人工登记声明、来源符号与场景；修改既有记录时，先审阅代码和对应说明，再显式刷新选中的证据：

```sh
uv run --no-sync python -m scripts.refresh_inventory \
  --runtime /path/to/Nexa --capability conversations \
  --page runtime_conversations.md --page runtime_conversations.en.md \
  --note "Reviewed the public conversation contract and updated both examples"
uv run --no-sync python -m scripts.verify --runtime /path/to/Nexa
```

刷新操作保留状态和预期输出，不替代编译或执行验收；review note 与时间保存在 inventory。来源记录采用完整文件 SHA-256，源文件的其他变化也会要求复核。

标准库参考从选定的运行时更新（从本仓库根目录执行）：

```sh
/path/to/Nexa/.venv/bin/python -m scripts.export_stdlib --runtime /path/to/Nexa
```

此命令在 import 前禁止网络和 `.nxs` 读取；常规完整验证会在隔离子进程内自动执行 `--check` 比对。`fallback_to_default: true` 用于复制共享 JSON/图片资源到英文构建；页面配对门禁先运行，缺失翻译会失败。

## CI 与发布

`check-docs.yml` 在 PR 运行两个独立门禁：结构/静态站点，以及真实运行时示例。运行时任务固定到 v2.4.0 的源码 commit [`c2162637236e4a73feea410c4183672411666521`](https://github.com/Nexa-Language/Nexa/commit/c2162637236e4a73feea410c4183672411666521)。校验器核对该 checkout 的来源 hash；ref 格式错误或源码漂移时任务明确失败。

已核对正式 tag `v2.4.0` 指向此 commit。升级基线时，先审阅并验证新源码，再同时更新 inventory 与 workflow 中的完整 SHA。PR 门禁只有 contents:read 权限，不部署。

`deploy-docs.yml` 保留 main 的 GitHub Pages 发布入口，并依赖上述两个门禁全部成功；部署步骤单独授予 Pages 权限。日常内容修改使用锁定依赖，依赖升级必须重新执行完整验证及视觉检查。

## 参考与反馈

依赖配置核对来源：[Material palettes](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/)、[static-i18n suffix layout](https://ultrabug.github.io/mkdocs-static-i18n/getting-started/quick-start/)、[uv locked sync](https://docs.astral.sh/uv/concepts/projects/sync/)、[uv GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/)。

反馈请提交到 [Nexa-docs issues](https://github.com/Nexa-Language/Nexa-docs/issues)，附页面 URL、语言、最小示例及诊断；凭据与任务数据留在本地。
