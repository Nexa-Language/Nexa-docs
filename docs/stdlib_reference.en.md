---
title: "Standard library API"
capabilities: [stdlib, tools]
---

# Standard library API

This reference is generated from the selected 2.4 runtime's registered tool schemas. Names below are exact registry identifiers. Expose a namespace with `uses std.fs`, or call supported DSL wrappers such as `std.fs.read(path)`. Required and optional parameters describe the JSON tool interface. Return types are the registered handler's annotations; `unspecified` means no annotation is declared. See the full [schema snapshot](stdlib-api.json) for property descriptions.

## Execution and errors

Agent-dispatched tools check exposure and approval before execution. Direct standard-library calls run as trusted program code. Filesystem mutation is disabled by default in the legacy standard-library layer; its `NEXA_ENABLE_DANGEROUS_TOOLS` and `NEXA_ALLOWED_WRITE_ROOTS` configuration is separate from Agent approval. Configure only reviewed, task-specific permissions. Regular handler failures may return an `Error:` string; uncertain transport failures propagate to preserve unknown-outcome recovery. Database handles and several collection results are JSON strings; explicitly decode them when local structured values are required. PostgreSQL and external services require their application dependencies. `std.ui` needs the `terminal` extra.


## `std.fs`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `file_read` | `path: string` | `encoding: string` | `str` |
| `file_write` | `path: string`, `content: string` | — | `str` |
| `file_exists` | `path: string` | — | `str` |
| `file_list` | `directory: string` | `pattern: string` | `str` |
| `file_append` | `path: string`, `content: string` | — | `str` |
| `file_delete` | `path: string` | — | `str` |
| `file_edit` | `path: string`, `old_text: string`, `new_text: string` | — | `str` |

## `std.http`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `http_get` | `url: string` | `headers: object`, `timeout: integer` | `str` |
| `http_post` | `url: string`, `data: string` | `headers: object`, `content_type: string` | `str` |
| `http_put` | `url: string`, `data: string` | `headers: object` | `str` |
| `http_delete` | `url: string` | `headers: object` | `str` |

## `std.time`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `time_now` | — | `format: string` | `str` |
| `time_diff` | `start: string`, `end: string` | `unit: string` | `str` |
| `time_format` | `iso_string: string` | `format: string` | `str` |
| `time_sleep` | `seconds: integer` | — | `str` |
| `time_timestamp` | — | — | `str` |

## `std.text`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `text_split` | `text: string` | `delimiter: string` | `str` |
| `text_replace` | `text: string`, `old: string`, `new: string` | — | `str` |

## `std.json`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `json_parse` | `text: string` | — | `str` |
| `json_get` | `text: string`, `path: string` | — | `str` |
| `json_stringify` | `data: string` | `indent: integer` | `str` |

## `std.hash`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `hash_md5` | `text: string` | — | `str` |
| `hash_sha256` | `text: string` | — | `str` |
| `base64_encode` | `text: string` | — | `str` |
| `base64_decode` | `text: string` | — | `str` |

## `std.math`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `math_calc` | `expression: string` | — | `str` |
| `math_random` | `min_val: integer`, `max_val: integer` | — | `str` |

## `std.regex`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `regex_match` | `pattern: string`, `text: string` | `flags: string` | `str` |
| `regex_replace` | `pattern: string`, `replacement: string`, `text: string` | — | `str` |

## `std.shell`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `shell_exec` | `command: string` | `timeout: integer` | `str` |
| `shell_which` | `command: string` | — | `str` |

## `std.code`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `search_files` | `pattern: string` | `directory: string` | `str` |
| `list_directory` | `directory: string` | — | `str` |
| `file_edit` | `path: string`, `old_text: string`, `new_text: string` | — | `str` |

## `std.ask_human`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `ask_human` | `prompt: string` | `default: string` | `str` |

## `std.db.sqlite`

| Registry name | Required parameters | Optional parameters | Return annotation |
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

| Registry name | Required parameters | Optional parameters | Return annotation |
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

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_db_memory_query` | `handle_json: string`, `agent_name: string`, `key: string` | — | `str` |
| `std_db_memory_store` | `handle_json: string`, `agent_name: string`, `key: string`, `value: string` | — | `str` |
| `std_db_memory_delete` | `handle_json: string`, `agent_name: string`, `key: string` | — | `str` |
| `std_db_memory_list` | `handle_json: string`, `agent_name: string` | — | `str` |

## `std.auth`

| Registry name | Required parameters | Optional parameters | Return annotation |
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

| Registry name | Required parameters | Optional parameters | Return annotation |
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

| Registry name | Required parameters | Optional parameters | Return annotation |
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

| Registry name | Required parameters | Optional parameters | Return annotation |
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

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_pipe_apply` | `value: string`, `func: string` | `extra_args: string` | `unspecified` |

## `std.defer`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_defer_schedule` | `expression: string` | — | `unspecified` |

## `std.null_coalesce`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_null_coalesce_apply` | `value: string`, `fallback: string` | — | `unspecified` |

## `std.string`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_string_interpolate` | `template: string` | `context: string` | `unspecified` |

## `std.match`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_match_pattern` | `value: string`, `pattern: string` | — | `unspecified` |
| `std_match_destructure` | `value: string`, `pattern: string` | — | `unspecified` |
| `std_match_variant` | `enum: string`, `variant: string` | `fields: string` | `unspecified` |

## `std.ui`

| Registry name | Required parameters | Optional parameters | Return annotation |
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

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_adt_register_struct` | `name: string`, `fields: string` | — | `unspecified` |
| `std_adt_make_struct` | `name: string` | `fields: string` | `unspecified` |
| `std_adt_lookup` | `kind: string`, `name: string` | — | `unspecified` |

## `std.enum`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_adt_register_enum` | `name: string`, `variants: string` | — | `unspecified` |
| `std_adt_make_variant` | `enum: string`, `variant: string` | `fields: string` | `unspecified` |
| `std_adt_lookup` | `kind: string`, `name: string` | — | `unspecified` |

## `std.trait`

| Registry name | Required parameters | Optional parameters | Return annotation |
| --- | --- | --- | --- |
| `std_adt_register_trait` | `name: string`, `methods: string` | — | `unspecified` |
| `std_adt_register_impl` | `trait: string`, `type: string` | `methods: string` | `unspecified` |
| `std_adt_lookup` | `kind: string`, `name: string` | — | `unspecified` |
| `std_adt_summary` | — | — | `unspecified` |
| `std_adt_reset` | — | — | `unspecified` |

---

[Source and validation](capability_inventory.md) · `stdlib` / `tools`
