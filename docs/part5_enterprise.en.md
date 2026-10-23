---
title: "Services and durable tasks"
capabilities: [stdlib, execution, checkpoint]
---

# Services and durable tasks

Nexa includes HTTP services, background jobs, databases, KV, authentication, templates, and concurrency modules. Distinguish application-module capabilities from durable Agent execution guarantees when designing deployment.

| Capability | Runtime entry | Test provenance |
| --- | --- | --- |
| HTTP routing | `nexa serve` / `routes`, `src/runtime/http_server.py` | `tests/test_http_server.py` |
| Background jobs | `nexa jobs` / `workers`, `src/runtime/jobs.py` | `tests/test_jobs.py` |
| Databases | `std.db.sqlite` / `std.db.postgres` | `tests/test_database.py` |
| KV | `std.kv` | `tests/test_kv_store.py` |
| Authentication/CSRF | `std.auth` | `tests/test_auth.py` |
| Templates | `std.template` | `tests/test_template.py` |

Applications own configuration and external dependencies for these modules. Deployment high availability, tenant isolation, and operational SLAs require application-level design and acceptance against real traffic, storage, permissions, and failures.

## Agent execution layer

Tool execution persists `started` first and saves results before appending messages. SQLite revisions detect conflicting writes. See [Execution](runtime_execution.md) and [Checkpoints](runtime_checkpoints.md) for approvals, budgets, and unknown outcomes.

Database transactions cover their database operations. Workflows spanning HTTP, files, and model calls need application-defined idempotency keys, compensation, and operator verification.

---

[Source and validation](capability_inventory.md) · `stdlib` / `execution` / `checkpoint`
