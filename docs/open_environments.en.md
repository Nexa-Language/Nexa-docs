---
title: "Environments and OCI execution"
capabilities: [open_execution, open_evidence]
language_versions: ["3.0"]
---

# Environments and OCI execution

An environment binds the image, frozen checks, model identity, provider variable names, and dependencies. Its digest participates in artifact and evidence identity; changing an endpoint or check configuration changes the execution context.

## An environment without a model

Save this as `offline.json`. The image is pinned by digest in the 3.0 release example.

```json
{"image": "python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704"}
```

```sh
docker pull python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704
uv run nexa build answer.nx --environment offline.json --state .nexa/answer.db --json
```

Use the complete `answer.nx` from [Quickstart](quickstart.md). The executor uses the current Docker context; `--docker-context NAME` selects one explicitly. Local Docker on Linux/macOS must be running. Build does not pull images automatically.

Candidate containers have no network, host directory mounts, or provider credentials. They run as `65534:65534`, with a read-only root filesystem, dropped capabilities, no-new-privileges, and bounded memory, CPU, PIDs, output, and time. The runtime verifies the actual Docker configuration. Source snapshots enter through stdin; RepositoryCheck expectations stay in the host controller. Each OCI call has a maximum duration of 30 seconds.

## Models and frozen checks
This complete environment also matches the Sum program on the organization profile. Save it as `sum-environment.json`, set the named variables in your shell, and pass `--environment sum-environment.json` when building. The three cases freeze empty, negative, and positive inputs.

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


`examples/open_programs/aliyun.json` uses `qwen3.8-max-0902`, with `ALIYUN_API_KEY` and `ALIYUN_BASE_URL` environment variables. Configuration stores variable names only; credentials are read when the model client is actually created. Model requests run in the controller; candidates retain their network isolation. `provider.endpoint` is a reserved derived dependency; configuration supplies only original dependencies.

```sh
uv run nexa build examples/open_programs/sum.nx --environment examples/open_programs/aliyun.json --state .nexa/sum.db --max-model-calls 4 --max-tokens 16000 --timeout 90 --json
```

This command sends real requests to your configured provider. The site's automatic gate uses fixed replies and blocks Python network access; actual OCI verification requires explicit `--oci`. OutputCheck compares results against frozen JSON cases. RepositoryCheck runs controller-owned argv and compares exit codes and output. Define checks for your repository before maintaining it.

Handle environment failures by their code: check Docker and the image for `executor_unavailable`, ensure names for `checker_missing`, authorized bindings for `model_unavailable`, variable presence for `credential_unavailable`, and reload the environment for `endpoint_changed`.

---

[Source and validation](capability_inventory.md) · `open_execution` / `open_evidence`
