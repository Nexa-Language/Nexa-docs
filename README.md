# Nexa documentation

Nexa 3.0 Open Programs 的中英文文档，保留完整 2.4 兼容入口与全部旧路由。主入口为[快速入门](docs/quickstart.md) / [English](docs/quickstart.en.md)；[Open Programs](docs/open_programs.md)覆盖目标合同、环境/OCI、Author、证据、预算、修订恢复、准确授权、capsule 与迁移。

文档包版本为 `3.0.0.dev0`，运行时固定到已发布的 [Nexa v3.0.0](https://github.com/Nexa-Language/Nexa/releases/tag/v3.0.0)，准确 commit 为 `274379606e53c90d2d25774f6bb8984c777d0759`，tree 为 `b090cc6503ea70318667031925480e36c352a913`。文档环境与 runtime 环境分别管理。

- `docs/inventory.json`：104 页、52 双语对、68 个完整示例；含语言版本、检查/执行声明、场景与 source/test fingerprints。
- `docs/stdlib-api.json`：实际 2.4 兼容标准库 registry；API 页面由 `scripts.export_stdlib` 生成。
- `docs/stylesheets/extra.css`：graphite/paper 视觉 token、排版和响应式布局；系统字体与 Material 搜索/语言/主题/移动导航沿用。
- 84 条旧页面路径保留；旧快速入门的全部例子在 `quickstart_24`，既有 62 个例子继续通过 3.0 兼容路径验证。

## 本地预览

文档需要 Python 3.11+ 和 uv，本轮使用 Python 3.12、uv 0.11.30。日常使用锁定依赖，不升级无关包。

```sh
uv sync --locked
uv run --no-sync mkdocs serve
uv run --no-sync mkdocs build --strict
```

## 验证

准备干净的固定 Nexa checkout，在该目录执行 `uv sync --locked`。检查要求准确 HEAD、完整 Git tree 和 clean worktree；暂存、未暂存和未忽略的新文件都会导致失败。`--runtime-python` 可指定装有 runtime 依赖的解释器，默认 `RUNTIME/.venv/bin/python`。

```sh
uv run --no-sync python -m scripts.verify --runtime /absolute/path/to/Nexa
```

此命令执行 inventory/语言配对/旧路由/导航检查、pytest、ruff、isort、ty、严格 MkDocs 构建、生成 HTML 链接与资源检查、源码 provenance、全部示例的版本匹配检查、40 个旧运行时离线场景和标准库 registry 比对。3.0 原生 check 断言零模型、零子进程；报告中的 `oci_deferred` 明确列出尚未执行的 OCI 场景。

真实 OCI 验收需要 Linux/macOS 的本地 Docker daemon 与固定镜像。准备镜像后显式运行：

```sh
docker pull python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704
uv run --no-sync python -m scripts.verify --runtime /absolute/path/to/Nexa --oci
```

该门禁额外执行 4 个登记的 3.0 场景（中英文 Answer、Sum），核对实际输出、accepted 状态、通过的 evidence、fixture 调用数、artifact digest，以及 locked replay 的零请求与相同产物。Sum 的冻结用例覆盖空列表、负数与正数；固定 provider 回复仅替代模型边界。候选、policy、数据库、Docker 隔离和证据判断使用真实 runtime。

子进程使用临时 HOME/TMPDIR 和最小环境，不继承个人 provider 凭据。在任何 runtime import 前阻断 Python 网络访问和 `.nxs` 读取。OCI 通过当前 context 的本地 Unix Docker endpoint 连接；候选 network=none、无宿主目录挂载。远程 Docker endpoint 不在本站验证支持范围。此工具运行经过审阅的仓库示例。

报告位于 `.reports/docs-check.json`，包含实际编译、原生检查、离线/OCI 执行数量、deferred 场景、逐例输出/evidence 与错误。失败退出非零。结构检查可省略 runtime，结果明确标为 `runtime_validation: not_requested`。单独执行：

```sh
uv run --no-sync python -m scripts.check_docs --site site
uv run --no-sync python -m scripts.check_docs --runtime /absolute/path/to/Nexa --oci --report .reports/oci.json
```

## 内容与证据更新

页面按 `topic.md` / `topic.en.md` 成对保存。Front matter 的 `capabilities` 和 `language_versions` 与 inventory 对齐；导航登记中文路径并提供英文标签。旧路由在 `preserved_pages` 中受到检查。

每个 `nexa` / `nx` fence 单独登记稳定 ID、页面/块索引、源码 SHA-256、status、language_version、claim 和 validation：

| 语言 | 模式 | 声明与要求 |
| --- | --- | --- |
| 2.4 | `compile` | `claim: check`，真实兼容编译 |
| 2.4 | `offline` | `claim: execute`，明确输出/错误/模型调用/工具结果等预期 |
| 3.0 | `nativecheck` | `claim: check`，真实原生合同检查 |
| 3.0 | `oci` | `claim: execute`，`build-replay` scenario、非空 expected_outputs、model_calls 与按需 replies/checks |

翻译必须共享语言版本、验证模式及 scenario。完整 3.0 示例使用旧 compiler 标记、只检查却声明已执行、遗漏真实预期或移除旧路由都会失败。`partial` / `historical` 必须填写具体原因并在正文显示。

改变 provenance 后先复核声明、实际实现、回归测试与预期结果，再显式刷新已审阅的选择：

```sh
uv run --no-sync python -m scripts.refresh_inventory \
  --runtime /absolute/path/to/Nexa --capability open_execution \
  --page open_programs.md --page open_programs.en.md \
  --note "Reviewed OCI execution, native checks, fixtures and locked replay"
uv run --no-sync python -m scripts.verify --runtime /absolute/path/to/Nexa --oci
```

刷新保留场景与预期，不替代执行。源码升级需同时审核所有改变的指纹及对应声明，再更新 CI 完整 SHA。标准库更新与比对：

```sh
/absolute/path/to/Nexa/.venv/bin/python -m scripts.export_stdlib --runtime /absolute/path/to/Nexa
```

`fallback_to_default: true` 仅供共享 JSON/图片资源复制；双语页面门禁先执行。产品集成页按实际 Nexa Code flags、extension commands/settings 编写，并说明澄清回写源码、CAS、活动身份及准确授权。

## CI 与发布

`check-docs.yml` 保留 Ubuntu 上的结构/静态站点与 runtime 两个 job。Runtime 固定正式 3.0 SHA，先执行离线验证，再明确拉取固定 digest 镜像并运行 OCI/locked replay step。PR 只需 contents:read。

`deploy-docs.yml` 保留 main 的 Pages 入口，并等待全部检查成功后构建和发布；部署步骤单独授予 Pages 权限。日常文档任务只生成本地 site，发布按仓库授权流程执行。外部 URL 可达性、真实 provider 质量/费用与部署结果分别验收。

反馈请提交 [Nexa-docs issues](https://github.com/Nexa-Language/Nexa-docs/issues)，附页面 URL、语言、版本、最小示例与脱敏诊断。
