---
title: "Start with Nexa 3.0"
capabilities: [open_language, open_execution]
language_versions: ["3.0"]
---

# Start with Nexa 3.0

Nexa 3.0 puts goals, implementations, and acceptance requirements in one program. Check a contract offline, build an artifact returning `42` inside OCI, then replay its lock. This guide uses released [v3.0.0](https://github.com/Nexa-Language/Nexa/releases/tag/v3.0.0), pinned to source [`2743796`](https://github.com/Nexa-Language/Nexa/commit/274379606e53c90d2d25774f6bb8984c777d0759).

## 1. Install the pinned release

You need Python 3.10+, Git, and uv. Execution supports Linux/macOS: Docker Engine on Linux, or Docker Desktop / Colima on macOS.

```sh
git clone --branch v3.0.0 --depth 1 https://github.com/Nexa-Language/Nexa.git
cd Nexa
uv sync --locked --all-extras
uv run nexa --version
```

Confirm `Nexa v3.0.0`. Run the following commands from this directory. Standalone wheels are on the [release page](https://github.com/Nexa-Language/Nexa/releases/tag/v3.0.0); the `nexa-lang` name on PyPI belongs to a different project.

## 2. Write a complete contract

Save this as `answer.nx`:

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

`check` returns program IR, diagnostics, and open obligations; this example has no open obligations. This step needs no Docker, provider, or credentials and starts neither candidates nor models. `language "3.0"` selects Open Programs explicitly; existing programs retain the [2.4 compatibility entry point](quickstart_24.md).

## 3. Build and replay

Start Docker and obtain the image pinned by the runtime example:

```sh
docker pull python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704
uv run nexa build answer.nx --environment examples/open_programs/offline.json --state .nexa/answer.db --json
uv run nexa build answer.nx --environment examples/open_programs/offline.json --state .nexa/answer.db --locked --json
```

The first build executes the literal implementation in real OCI. Its accepted `answer` result is `42`, with passing `typecheck` evidence. Both builds use zero model calls; the second returns the same artifact digest. The default lock is `answer.nx.lock`. Preserve it with `.nexa/answer.db`, which stores the objects referenced by the lock. A missing image or unavailable Docker returns `executor_unavailable`.

## 4. Leave an implementation open

[Goals and contracts](open_programs.md) introduces `implementation open`: a model proposes implementations within a budget, while deterministic checks and model reviews produce separate evidence. Read [environment setup](open_environments.md) and [budgets](open_budgets.md) before explicitly requesting resolution. Repository writes follow the [exact patch authorization](open_grants.md) workflow.

Continue with [evidence](open_evidence.md), [revision and recovery](open_revisions.md), [developer tools](toolchain.md), or [2.4 → 3.0 migration](migration_30.md).

---

[Source and validation](capability_inventory.md) · `open_language` / `open_execution`
