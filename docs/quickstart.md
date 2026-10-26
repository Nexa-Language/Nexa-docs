---
title: "开始使用 Nexa 3.0"
capabilities: [open_language, open_execution]
language_versions: ["3.0"]
---

# 开始使用 Nexa 3.0

Nexa 3.0 把目标、实现和验收条件写进同一个程序。先离线检查合同，再在 OCI 中构建一个返回 `42` 的产物，最后用锁文件重放。全部步骤使用已发布的 [v3.0.0](https://github.com/Nexa-Language/Nexa/releases/tag/v3.0.0)，源码固定到 [`2743796`](https://github.com/Nexa-Language/Nexa/commit/274379606e53c90d2d25774f6bb8984c777d0759)。

## 1. 安装固定版本

需要 Python 3.10+、Git 和 uv；3.0 执行支持 Linux/macOS。Linux 使用 Docker Engine；macOS 使用 Docker Desktop 或 Colima。

```sh
git clone --branch v3.0.0 --depth 1 https://github.com/Nexa-Language/Nexa.git
cd Nexa
uv sync --locked --all-extras
uv run nexa --version
```

确认输出 `Nexa v3.0.0`。下列命令在此目录执行。独立 wheel 的安装地址见[发行页](https://github.com/Nexa-Language/Nexa/releases/tag/v3.0.0)；PyPI 上同名 `nexa-lang` 属于其他项目。

## 2. 写下完整合同

保存为 `answer.nx`：

```nexa
language "3.0"
program Answer {
    goal answer() -> Int {
        intent "Return 42"
        implementation value 42
    }
}
```

```sh
uv run nexa check answer.nx --json
```

`check` 返回程序 IR、诊断和开放义务；本例没有开放义务。此步无需 Docker、provider 或凭据，不启动候选或模型。`language "3.0"` 显式选择 Open Programs；旧程序继续使用[2.4 兼容入口](quickstart_24.md)。

## 3. 构建并重放

先启动 Docker，再取得源码示例所固定的镜像：

```sh
docker pull python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704
uv run nexa build answer.nx --environment examples/open_programs/offline.json --state .nexa/answer.db --json
uv run nexa build answer.nx --environment examples/open_programs/offline.json --state .nexa/answer.db --locked --json
```

第一次构建实际在 OCI 中执行常量实现，接受的 `answer` 结果为 `42`，附带通过的 `typecheck` 证据。两次构建都为零模型调用；第二次返回相同产物 digest。锁文件默认是 `answer.nx.lock`，需要连同 `.nexa/answer.db` 保存，数据库持有锁所引用的对象。镜像缺失或 Docker 不可用时，执行返回 `executor_unavailable`。

## 4. 让实现保持开放

[目标与合同](open_programs.md)展示 `implementation open`：模型可以在预算内提出实现，确定性检查与模型评审分别形成证据。先读[环境配置](open_environments.md)和[预算](open_budgets.md)，再显式运行求解。仓库写入按[准确补丁授权](open_grants.md)执行。

下一步：[证据与验收](open_evidence.md) · [修订与恢复](open_revisions.md) · [开发工具](toolchain.md) · [2.4 → 3.0](migration_30.md)

---

[来源与验证](capability_inventory.md) · `open_language` / `open_execution`
