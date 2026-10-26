---
title: 能力与示例证据
capabilities:
- compilation
- verification
- open_language
- open_execution
- open_evidence
language_versions:
- '3.0'
- '2.4'
---

# 能力与示例证据

本站固定到已发布的 [Nexa v3.0.0 源码](https://github.com/Nexa-Language/Nexa/commit/274379606e53c90d2d25774f6bb8984c777d0759)：commit `274379606e53c90d2d25774f6bb8984c777d0759`，Git tree `b090cc6503ea70318667031925480e36c352a913`。机器可读 [inventory.json](inventory.json) 保存源码/test 符号、完整文件 SHA-256、运行时版本和审阅记录。

## 按语言与声明核验

当前登记 **104 页、52 组中英配对、68 个完整 Nexa 示例**。旧 84 条页面路径全部保留。62 个 2.4 示例经 3.0 兼容编译，其中 40 个检查实际离线输出；6 个 3.0 示例通过原生合同检查，其中 4 个登记 OCI 构建与锁定重放（中英文各两个）。

| 模式 | 语言与实际检查 |
| --- | --- |
| `compile` | 2.4：真实 `compile_source`，生成 Python 并验证语法 |
| `offline` | 2.4：编译后执行 SDK/工具/flow，核对输出、错误、请求数或邮箱顺序 |
| `nativecheck` | 3.0：原生 `compile_program`，验证 CheckReport，无模型请求、无子进程 |
| `oci` | 3.0：先 nativecheck，再用真实固定镜像执行，核对实际输出与证据，锁定重放必须零请求 |

每个 complete 示例有显式 `language_version`、`claim`（check/execute）及验证模式。执行声明必须有实际 scenario；3.0 执行场景指定 expected_outputs、model_calls 与 build-replay。中英文版本、验证模式和场景保持一致。只运行离线检查时报告准确列出 `oci_deferred`；显式 OCI 门禁才计入真实执行。

## 来源与隔离

验证要求干净 checkout、准确 commit、完整 Git tree、文件 hash 与源码符号；暂存/未暂存/未忽略的新文件均使门禁失败。此次升级重新审阅发生变化的 compiler、CLI、provider、manifest、示例测试、README 和依赖配置；保留的 2.4 语义使用 3.0 包实测。

子进程使用临时 HOME/TMPDIR 和最小环境，不继承 provider 凭据；在 runtime import 前阻断 Python 网络和 `.nxs` 读取。fixture 仅提供固定模型回复，执行器与验收使用实际 runtime。OCI 通过本地 Docker Unix socket 运行固定 digest，候选 network=none。完整报告记录产物 digest、输出与每项 evidence digest。

新增或变化的源码必须复核说明和预期后刷新。partial/historical 块的具体原因需在页面可见。严格 MkDocs 构建与 HTML 链接/锚点/资源检查覆盖双语页面；[stdlib-api.json](stdlib-api.json) 与真实兼容 registry 比对。命令与 CI 门禁见 [README](https://github.com/Nexa-Language/Nexa-docs)。
