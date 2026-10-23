---
title: "服务与持久任务"
capabilities: [stdlib, execution, checkpoint]
---

# 服务与持久任务

Nexa 包含 HTTP 服务、后台 job、数据库、KV、认证、模板与并发模块。选择部署方案时，先区分应用模块能力与 Agent 的持久执行保证。

| 应用能力 | 运行时入口 | 验证来源 |
| --- | --- | --- |
| HTTP 路由 | `nexa serve` / `routes`，`src/runtime/http_server.py` | `tests/test_http_server.py` |
| 后台 job | `nexa jobs` / `workers`，`src/runtime/jobs.py` | `tests/test_jobs.py` |
| 数据库 | `std.db.sqlite` / `std.db.postgres` | `tests/test_database.py` |
| KV | `std.kv` | `tests/test_kv_store.py` |
| 认证与 CSRF | `std.auth` | `tests/test_auth.py` |
| 模板 | `std.template` | `tests/test_template.py` |

这些模块的配置与外部依赖由应用负责。基础运行时不提供部署平台的高可用、租户隔离或运维 SLA。部署前按真实流量、存储、权限、故障恢复要求验收。

## Agent 运行层

工具执行前持久化 `started`，结果保存后再添加消息。SQLite revision 检测写入冲突。审批、预算和未知结果处理见[运行时指南](runtime_execution.md)与[checkpoint](runtime_checkpoints.md)。

数据库事务只覆盖相应数据库操作。跨 HTTP、文件和模型调用的工作流应由业务定义幂等键、补偿与人工核实步骤。

---

[来源与验证](capability_inventory.md) · `stdlib` / `execution` / `checkpoint`
