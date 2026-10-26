---
title: "标准库 API"
capabilities: [stdlib, tools]
language_versions: ["2.4"]
---

!!! note "Nexa 3.0 中的 2.4 兼容路径"
    这些 API 服务于 2.4 兼容入口。Open Programs 使用显式 capabilities 与[控制器适配器](migration_30.md)。

# 标准库 API

本页从 Nexa 3.0 保留的 2.4 工具注册表生成。下列名称为准确的注册表标识符。用 `uses std.fs` 暴露 namespace，或调用受支持的 DSL 包装器，例如 `std.fs.read(path)`。必填与可选参数描述工具 JSON 接口；返回类型采用注册 handler 的注解，`unspecified` 表示该 handler 未声明返回注解。字段说明见完整的 [schema 快照](stdlib-api.json)。

## 执行与错误

Agent 发起的工具调用先检查暴露集与审批；直接标准库调用作为受信任程序代码执行。旧标准库层默认关闭文件系统修改；其 `NEXA_ENABLE_DANGEROUS_TOOLS` 与 `NEXA_ALLOWED_WRITE_ROOTS` 配置独立于 Agent 审批，应仅按已审核任务配置权限。普通 handler 失败可能返回 `Error:` 字符串；结果不确定的传输错误向上传播，保留未知结果恢复语义。数据库句柄与部分集合结果采用 JSON 字符串，需要本地结构化值时应显式解码。PostgreSQL 与外部服务需要应用依赖，`std.ui` 需要 `terminal` extra。


## `std.fs`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `file_read` | `path: string` | `encoding: string` | `str` |
| `file_write` | `path: string`, `content: string` | — | `str` |
| `file_exists` | `path: string` | — | `str` |
| `file_list` | `directory: string` | `pattern: string` | `str` |
| `file_append` | `path: string`, `content: string` | — | `str` |
| `file_delete` | `path: string` | — | `str` |
| `file_edit` | `path: string`, `old_text: string`, `new_text: string` | — | `str` |

## `std.http`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `http_get` | `url: string` | `headers: object`, `timeout: integer` | `str` |
| `http_post` | `url: string`, `data: string` | `headers: object`, `content_type: string` | `str` |
| `http_put` | `url: string`, `data: string` | `headers: object` | `str` |
| `http_delete` | `url: string` | `headers: object` | `str` |

## `std.time`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `time_now` | — | `format: string` | `str` |
| `time_diff` | `start: string`, `end: string` | `unit: string` | `str` |
| `time_format` | `iso_string: string` | `format: string` | `str` |
| `time_sleep` | `seconds: integer` | — | `str` |
| `time_timestamp` | — | — | `str` |

## `std.text`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `text_split` | `text: string` | `delimiter: string` | `str` |
| `text_replace` | `text: string`, `old: string`, `new: string` | — | `str` |

## `std.json`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `json_parse` | `text: string` | — | `str` |
| `json_get` | `text: string`, `path: string` | — | `str` |
| `json_stringify` | `data: string` | `indent: integer` | `str` |

## `std.hash`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `hash_md5` | `text: string` | — | `str` |
| `hash_sha256` | `text: string` | — | `str` |
| `base64_encode` | `text: string` | — | `str` |
| `base64_decode` | `text: string` | — | `str` |

## `std.math`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `math_calc` | `expression: string` | — | `str` |
| `math_random` | `min_val: integer`, `max_val: integer` | — | `str` |

## `std.regex`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `regex_match` | `pattern: string`, `text: string` | `flags: string` | `str` |
| `regex_replace` | `pattern: string`, `replacement: string`, `text: string` | — | `str` |

## `std.shell`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `shell_exec` | `command: string` | `timeout: integer` | `str` |
| `shell_which` | `command: string` | — | `str` |

## `std.code`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `search_files` | `pattern: string` | `directory: string` | `str` |
| `list_directory` | `directory: string` | — | `str` |
| `file_edit` | `path: string`, `old_text: string`, `new_text: string` | — | `str` |

## `std.ask_human`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `ask_human` | `prompt: string` | `default: string` | `str` |

## `std.db.sqlite`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_db_sqlite_connect` | `path: string` | — | `str` |
| `std_db_sqlite_query` | `handle_json: string`, `sql: string` | `params_json: string` | `str` |
| `std_db_sqlite_query_one` | `handle_json: string`, `sql: string` | `params_json: string` | `str` |
| `std_db_sqlite_execute` | `handle_json: string`, `sql: string` | `params_json: string` | `str` |
| `std_db_sqlite_close` | `handle_json: string` | — | `str` |
| `std_db_sqlite_begin` | `handle_json: string` | — | `str` |
| `std_db_sqlite_commit` | `handle_json: string` | — | `str` |
| `std_db_sqlite_rollback` | `handle_json: string` | — | `str` |

## `std.db.postgres`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_db_postgres_connect` | `url: string` | — | `str` |
| `std_db_postgres_query` | `handle_json: string`, `sql: string` | `params_json: string` | `str` |
| `std_db_postgres_query_one` | `handle_json: string`, `sql: string` | `params_json: string` | `str` |
| `std_db_postgres_execute` | `handle_json: string`, `sql: string` | `params_json: string` | `str` |
| `std_db_postgres_close` | `handle_json: string` | — | `str` |
| `std_db_postgres_begin` | `handle_json: string` | — | `str` |
| `std_db_postgres_commit` | `handle_json: string` | — | `str` |
| `std_db_postgres_rollback` | `handle_json: string` | — | `str` |

## `std.db.memory`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_db_memory_query` | `handle_json: string`, `agent_name: string`, `key: string` | — | `str` |
| `std_db_memory_store` | `handle_json: string`, `agent_name: string`, `key: string`, `value: string` | — | `str` |
| `std_db_memory_delete` | `handle_json: string`, `agent_name: string`, `key: string` | — | `str` |
| `std_db_memory_list` | `handle_json: string`, `agent_name: string` | — | `str` |

## `std.auth`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_auth_oauth` | `name: string`, `client_id: string`, `client_secret: string` | `opts: string` | `unspecified` |
| `std_auth_enable_auth` | `providers: string` | `options: string` | `unspecified` |
| `std_auth_get_user` | `request: string` | — | `unspecified` |
| `std_auth_get_session` | `request: string` | — | `unspecified` |
| `std_auth_session_data` | `request: string` | — | `unspecified` |
| `std_auth_set_session` | `request: string`, `data: string` | — | `unspecified` |
| `std_auth_logout_user` | `request: string` | — | `unspecified` |
| `std_auth_require_auth` | `request: string` | — | `unspecified` |
| `std_auth_jwt_sign` | `claims: string`, `secret: string` | `options: string` | `unspecified` |
| `std_auth_jwt_verify` | `token: string`, `secret: string` | — | `unspecified` |
| `std_auth_jwt_decode` | `token: string` | — | `unspecified` |
| `std_auth_csrf_token` | `request: string` | — | `unspecified` |
| `std_auth_csrf_field` | `request: string` | — | `unspecified` |
| `std_auth_verify_csrf` | `request: string`, `token: string` | — | `unspecified` |
| `std_auth_api_key_generate` | `agent_name: string` | `ttl: string` | `unspecified` |
| `std_auth_api_key_verify` | `api_key: string` | — | `unspecified` |
| `std_auth_auth_context` | `request: string` | `agent: string` | `unspecified` |

## `std.kv`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_kv_open` | `path: string` | — | `unspecified` |
| `std_kv_get` | `kv: string`, `key: string` | `default: string` | `unspecified` |
| `std_kv_get_int` | `kv: string`, `key: string` | `default: string` | `unspecified` |
| `std_kv_get_str` | `kv: string`, `key: string` | `default: string` | `unspecified` |
| `std_kv_get_json` | `kv: string`, `key: string` | — | `unspecified` |
| `std_kv_set` | `kv: string`, `key: string`, `value: string` | `opts: string` | `unspecified` |
| `std_kv_set_nx` | `kv: string`, `key: string`, `value: string` | `opts: string` | `unspecified` |
| `std_kv_del` | `kv: string`, `key: string` | — | `unspecified` |
| `std_kv_has` | `kv: string`, `key: string` | — | `unspecified` |
| `std_kv_list` | `kv: string` | `prefix: string` | `unspecified` |
| `std_kv_expire` | `kv: string`, `key: string`, `ttl_seconds: string` | — | `unspecified` |
| `std_kv_ttl` | `kv: string`, `key: string` | — | `unspecified` |
| `std_kv_flush` | `kv: string` | — | `unspecified` |
| `std_kv_incr` | `kv: string`, `key: string` | `amount: string` | `unspecified` |
| `std_kv_agent_kv_query` | `kv: string`, `semantic_query: string` | — | `unspecified` |
| `std_kv_agent_kv_store` | `kv: string`, `key: string`, `value: string` | `context: string` | `unspecified` |
| `std_kv_agent_kv_context` | `kv: string`, `agent: string` | — | `unspecified` |

## `std.concurrent`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_concurrent_channel` | — | — | `unspecified` |
| `std_concurrent_send` | `tx: string`, `value: string` | — | `unspecified` |
| `std_concurrent_recv` | `rx: string` | — | `unspecified` |
| `std_concurrent_recv_timeout` | `rx: string`, `ms: string` | — | `unspecified` |
| `std_concurrent_try_recv` | `rx: string` | — | `unspecified` |
| `std_concurrent_close` | `rx: string` | — | `unspecified` |
| `std_concurrent_select` | `channels: string` | `timeout_ms: string` | `unspecified` |
| `std_concurrent_spawn` | `handler: string` | — | `unspecified` |
| `std_concurrent_await_task` | `task: string` | — | `unspecified` |
| `std_concurrent_try_await` | `task: string` | — | `unspecified` |
| `std_concurrent_cancel_task` | `task: string` | — | `unspecified` |
| `std_concurrent_parallel` | `handlers: string` | — | `unspecified` |
| `std_concurrent_race` | `handlers: string` | — | `unspecified` |
| `std_concurrent_after` | `delay: string`, `handler: string` | — | `unspecified` |
| `std_concurrent_schedule` | `interval: string`, `handler: string` | — | `unspecified` |
| `std_concurrent_cancel_schedule` | `schedule: string` | — | `unspecified` |
| `std_concurrent_sleep_ms` | `ms: string` | — | `unspecified` |
| `std_concurrent_thread_count` | — | — | `unspecified` |

## `std.template`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_template_render` | `template_str: string` | `data: string` | `unspecified` |
| `std_template_template` | `path: string` | `data: string` | `unspecified` |
| `std_template_compile` | `path: string` | — | `unspecified` |
| `std_template_render_compiled` | `compiled: string` | `data: string` | `unspecified` |
| `std_template_filter_apply` | `value: string`, `filter_name: string` | `filter_args: string` | `unspecified` |
| `std_template_agent_prompt` | `agent: string`, `template_str: string` | `context: string` | `unspecified` |
| `std_template_agent_slot_fill` | `agent: string`, `template_str: string` | `slot_sources: string` | `unspecified` |
| `std_template_agent_register` | `agent: string`, `name: string`, `template_str: string` | — | `unspecified` |
| `std_template_agent_list` | — | — | `unspecified` |
| `std_template_filter_upper` | `value: string` | — | `unspecified` |
| `std_template_filter_lower` | `value: string` | — | `unspecified` |
| `std_template_filter_capitalize` | `value: string` | — | `unspecified` |
| `std_template_filter_trim` | `value: string` | — | `unspecified` |
| `std_template_filter_default` | `value: string` | `default: string` | `unspecified` |
| `std_template_filter_length` | `value: string` | — | `unspecified` |
| `std_template_filter_json` | `value: string` | — | `unspecified` |
| `std_template_filter_escape` | `value: string` | — | `unspecified` |
| `std_template_filter_url_encode` | `value: string` | — | `unspecified` |

## `std.pipe`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_pipe_apply` | `value: string`, `func: string` | `extra_args: string` | `unspecified` |

## `std.defer`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_defer_schedule` | `expression: string` | — | `unspecified` |

## `std.null_coalesce`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_null_coalesce_apply` | `value: string`, `fallback: string` | — | `unspecified` |

## `std.string`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_string_interpolate` | `template: string` | `context: string` | `unspecified` |

## `std.match`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_match_pattern` | `value: string`, `pattern: string` | — | `unspecified` |
| `std_match_destructure` | `value: string`, `pattern: string` | — | `unspecified` |
| `std_match_variant` | `enum: string`, `variant: string` | `fields: string` | `unspecified` |

## `std.ui`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_ui_banner` | `title: string` | `subtitle: string` | `str` |
| `std_ui_markdown` | `text: string` | — | `str` |
| `std_ui_code` | `code: string` | `language: string` | `str` |
| `std_ui_panel` | `text: string` | `title: string`, `style: string` | `str` |
| `std_ui_thinking` | — | `message: string`, `duration: number` | `str` |
| `std_ui_success` | `msg: string` | — | `str` |
| `std_ui_error` | `msg: string` | — | `str` |
| `std_ui_warning` | `msg: string` | — | `str` |
| `std_ui_info` | `msg: string` | — | `str` |
| `std_ui_input` | — | `prompt: string` | `str` |
| `std_ui_agent_reply` | `agent_name: string`, `reply: string` | — | `str` |
| `std_ui_tool_call` | `tool_name: string` | `args: string` | `str` |

## `std.struct`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_adt_register_struct` | `name: string`, `fields: string` | — | `unspecified` |
| `std_adt_make_struct` | `name: string` | `fields: string` | `unspecified` |
| `std_adt_lookup` | `kind: string`, `name: string` | — | `unspecified` |

## `std.enum`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_adt_register_enum` | `name: string`, `variants: string` | — | `unspecified` |
| `std_adt_make_variant` | `enum: string`, `variant: string` | `fields: string` | `unspecified` |
| `std_adt_lookup` | `kind: string`, `name: string` | — | `unspecified` |

## `std.trait`

| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |
| --- | --- | --- | --- |
| `std_adt_register_trait` | `name: string`, `methods: string` | — | `unspecified` |
| `std_adt_register_impl` | `trait: string`, `type: string` | `methods: string` | `unspecified` |
| `std_adt_lookup` | `kind: string`, `name: string` | — | `unspecified` |
| `std_adt_summary` | — | — | `unspecified` |
| `std_adt_reset` | — | — | `unspecified` |

---

[来源与验证](capability_inventory.md) · `stdlib` / `tools`
