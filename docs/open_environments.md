---
title: "Environment 与 OCI 执行"
capabilities: [open_execution, open_evidence]
language_versions: ["3.0"]
---

# Environment 与 OCI 执行

Environment 绑定镜像、固定检查、模型身份、provider 变量名和依赖。它的 digest 参与产物与证据身份；改变 endpoint 或检查配置会改变执行上下文。

## 无模型环境

将下面内容保存为 `offline.json`。镜像来自 3.0 发行示例，按 digest 固定。

```json
{"image": "python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704"}
```

```sh
docker pull python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704
uv run nexa build answer.nx --environment offline.json --state .nexa/answer.db --json
```

`answer.nx` 使用[快速入门](quickstart.md)中的完整程序。执行器使用当前 Docker context；CLI 的 `--docker-context NAME` 可显式选择。Linux/macOS 上的本地 Docker 必须已运行，构建不会自动拉取镜像。

候选容器没有网络、宿主目录挂载或 provider 凭据；运行用户为 `65534:65534`，根文件系统只读，能力集清空，启用 no-new-privileges，并限制内存、CPU、PID、输出与时间。运行时检查实际 Docker 配置。源码快照经 stdin 传入容器，RepositoryCheck 的期望值留在宿主控制器。单次 OCI 调用上限 30 秒。

## 模型与固定检查
这份完整 environment 同样适配组织首页的 Sum 程序。保存为 `sum-environment.json`，在 shell 中设置指定变量，构建时使用 `--environment sum-environment.json`。三个冻结用例覆盖空列表、负数和正数输入。

```json
{
  "image": "python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704",
  "model": "qwen3.8-max-0902",
  "model_pinned": true,
  "allow_model": true,
  "provider": {
    "protocol": "chat",
    "api_key_env": "ALIYUN_API_KEY",
    "base_url_env": "ALIYUN_BASE_URL",
    "enable_thinking": false
  },
  "checks": [{
    "name": "checks.sum",
    "cases": [
      {"input_json": "{\"values\":[]}", "expected_json": "0"},
      {"input_json": "{\"values\":[-8,3,7]}", "expected_json": "2"},
      {"input_json": "{\"values\":[10,20,30,40]}", "expected_json": "100"}
    ]
  }]
}
```


`examples/open_programs/aliyun.json` 使用 `qwen3.8-max-0902`，通过 `ALIYUN_API_KEY` 和 `ALIYUN_BASE_URL` 环境变量绑定。配置文件只记录变量名；凭据在实际创建模型客户端时读取。模型请求发生在控制器端，候选容器仍无外网。`provider.endpoint` 是控制器派生的保留依赖，手工配置只填写原始依赖。

```sh
uv run nexa build examples/open_programs/sum.nx --environment examples/open_programs/aliyun.json --state .nexa/sum.db --max-model-calls 4 --max-tokens 16000 --timeout 90 --json
```

这条命令会发起已配置 provider 的真实请求。本站自动门禁使用固定回复并阻断 Python 网络访问；实际 OCI 门禁必须显式传 `--oci`。OutputCheck 在固定 JSON 输入上比较期望值；RepositoryCheck 运行控制器配置的 argv 并比较退出码与输出。维护其他仓库前，先为目标仓库编写冻结的检查配置。

环境错误按具体状态处理：`executor_unavailable` 核对 Docker 与镜像，`checker_missing` 核对 ensure 名称，`model_unavailable` 核对授权 binding，`credential_unavailable` 核对变量是否设置，`endpoint_changed` 重新读取 environment 后重建。

---

[来源与验证](capability_inventory.md) · `open_execution` / `open_evidence`
