---
comments: true
---

# Nexa 标准库参考手册

本文档详细描述 Nexa 标准库 (`std`) 的所有命名空间、工具函数、参数和使用示例。所有工具签名与源码 `src/runtime/stdlib.py` 严格匹配。

---

## 📋 概述

Nexa 标准库提供了一系列内置工具，使 Agent 能够与外部世界交互。通过 `uses` 关键字声明使用权限后，Agent 即可调用这些工具。

### 命名空间总览

| 命名空间 | 说明 | 工具数量 | 版本 |
|---------|------|---------|------|
| [`std.fs`](#stdfs-文件系统操作) | 文件系统操作 | 6 | v0.7+ |
| [`std.http`](#stdhttp-http-网络请求) | HTTP 网络请求 | 4 | v0.7+ |
| [`std.time`](#stdtime-时间日期操作) | 时间日期操作 | 5 | v0.7+ |
| [`std.json`](#stdjson-json-数据处理) | JSON 数据处理 | 3 | v0.7+ |
| [`std.text`](#stdtext-文本处理) | 文本处理 | 4 | v0.7+ |
| [`std.hash`](#stdhash-加密与编码) | 加密与编码 | 4 | v0.7+ |
| [`std.math`](#stdmath-数学运算) | 数学运算 | 2 | v0.7+ |
| [`std.regex`](#stdregex-正则表达式) | 正则表达式 | 2 | v0.7+ |
| [`std.shell`](#stdshell-shell-命令) | Shell 命令执行 | 2 | v0.9.7+ |
| [`std.ask_human`](#stdask_human-人机交互) | 人机交互 | 1 | v0.9.7+ |
| [`std.db.sqlite`](#stddbsqlite-sqlite-操作) | SQLite 操作 | 8 | v1.3.5 |
| [`std.db.postgres`](#stddbpostgres-postgresql-操作) | PostgreSQL 操作 | 8 | v1.3.5 |
| [`std.db.memory`](#stddbmemory-agent-记忆操作) | Agent 记忆操作 | 4 | v1.3.5 |
| [`std.auth`](#stdauth-认证与-oauth) | 认证与 OAuth | 17 | v1.3.6 |
| [`std.kv`](#stdkv-键值存储) | KV 存储 | 18 | v1.3.6 |
| [`std.concurrent`](#stdconcurrent-结构化并发) | 结构化并发 | 18 | v1.3.6 |
| [`std.template`](#stdtemplate-模板系统) | 模板系统 | 18+ | v1.3.6 |
| [`std.pipe`](#stdpipe-管道操作符) | 管道操作符 | 1 | v1.3.x |
| [`std.defer`](#stddefer-延迟执行) | 延迟执行 | 1 | v1.3.x |
| [`std.null_coalesce`](#stdnull_coalesce-空值合并) | 空值合并 | 1 | v1.3.x |
| [`std.string`](#stdstring-字符串插值) | 字符串插值 | 1 | v1.3.x |
| [`std.match`](#stdmatch-模式匹配) | 模式匹配 | 3 | v1.3.x |
| [`std.struct`](#stdstruct-结构体) | 结构体 | 3 | v1.3.x |
| [`std.enum`](#stdenum-枚举) | 枚举 | 3 | v1.3.x |
| [`std.trait`](#stdtrait-特质与实现) | 特质与实现 | 5 | v1.3.x |

---

## 📁 std.fs - 文件系统操作

文件系统操作是智能体与本地环境交互的基础能力。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`file_read`](#file_read) | 读取文件内容 | `path` |
| [`file_write`](#file_write) | 写入文件 | `path`, `content` |
| [`file_append`](#file_append) | 追加文件内容 | `path`, `content` |
| [`file_exists`](#file_exists) | 检查文件是否存在 | `path` |
| [`file_list`](#file_list) | 列出目录文件 | `directory` |
| [`file_delete`](#file_delete) | 删除文件 | `path` |

---

#### file_read

读取文件内容。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |
| `encoding` | string | 否 | `utf-8` | 编码格式 |

**返回值**：文件内容字符串，或在出错时返回错误信息。

**示例**：

```nexa
agent FileReader uses std.fs {
    role: "文件读取助手",
    prompt: "帮助用户读取文件内容"
}

flow main {
    content = FileReader.run("读取 /tmp/data.txt 文件");
    print(content);
}
```

---

#### file_write

写入文件内容。如果目录不存在，会自动创建。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |
| `content` | string | **是** | - | 文件内容 |
| `encoding` | string | 否 | `utf-8` | 编码格式 |

**返回值**：成功信息，包含写入的字符数。

**示例**：

```nexa
agent FileWriter uses std.fs {
    role: "文件写入助手",
    prompt: "帮助用户写入文件"
}

flow main {
    result = FileWriter.run("将 'Hello Nexa' 写入 /tmp/output.txt");
    print(result);
}
```

---

#### file_append

追加内容到文件末尾。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |
| `content` | string | **是** | - | 追加内容 |
| `encoding` | string | 否 | `utf-8` | 编码格式 |

**返回值**：成功信息，包含追加的字符数。

---

#### file_exists

检查文件或目录是否存在。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件/目录路径 |

**返回值**：JSON 格式 `{ "exists": bool, "path": string }`。

---

#### file_list

列出目录中的文件。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `directory` | string | **是** | - | 目录路径 |
| `pattern` | string | 否 | `*` | 文件匹配模式（glob 格式） |

**返回值**：JSON 格式 `{ "files": [string], "count": int }`。

---

#### file_delete

删除文件。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |

**返回值**：成功或错误信息。

---

## 🌐 std.http - HTTP 网络请求

原生网络请求能力，支持 RESTful API 调用。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`http_get`](#http_get) | GET 请求 | `url` |
| [`http_post`](#http_post) | POST 请求 | `url`, `data` |
| [`http_put`](#http_put) | PUT 请求 | `url`, `data` |
| [`http_delete`](#http_delete) | DELETE 请求 | `url` |

---

#### http_get

发送 HTTP GET 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：响应内容字符串。

---

#### http_post

发送 HTTP POST 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `data` | string | **是** | - | 请求体内容 |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `content_type` | string | 否 | `application/json` | 内容类型 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "status": int, "body": string }`。

---

#### http_put

发送 HTTP PUT 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `data` | string | **是** | - | 请求体内容 |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `content_type` | string | 否 | `application/json` | 内容类型 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "status": int, "body": string }`。

---

#### http_delete

发送 HTTP DELETE 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "status": int, "body": string }`。

---

## 🕐 std.time - 时间日期操作

时间相关的操作工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`time_now`](#time_now) | 获取当前时间 | 无 |
| [`time_diff`](#time_diff) | 计算时间差 | `start`, `end` |
| [`time_format`](#time_format) | 格式化时间 | `iso_string` |
| [`time_sleep`](#time_sleep) | 休眠指定秒数 | `seconds` |
| [`time_timestamp`](#time_timestamp) | 获取时间戳 | 无 |

---

#### time_now

获取当前时间。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `format` | string | 否 | `%Y-%m-%d %H:%M:%S` | 时间格式 |

**返回值**：格式化后的时间字符串。

---

#### time_diff

计算两个时间之间的差值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `start` | string | **是** | - | 开始时间 (ISO 格式) |
| `end` | string | **是** | - | 结束时间 (ISO 格式) |
| `unit` | string | 否 | `seconds` | 单位：`seconds`/`minutes`/`hours`/`days` |

**返回值**：JSON 格式 `{ "value": float, "unit": string, "days": int, "seconds": float }`。

---

#### time_format

将 ISO 格式时间转换为指定格式。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `iso_string` | string | **是** | - | ISO 时间字符串 |
| `format` | string | 否 | `%Y-%m-%d %H:%M:%S` | 输出格式 |

**返回值**：格式化后的时间字符串。

---

#### time_sleep

暂停执行指定秒数。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `seconds` | int | **是** | - | 休眠秒数 |

**返回值**：JSON 格式 `{ "sleep": int }`。

---

#### time_timestamp

获取当前 Unix 时间戳。

**参数**：无

**返回值**：JSON 格式 `{ "timestamp": int }`。

---

## 📦 std.json - JSON 数据处理

JSON 数据的解析、查询和序列化。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`json_parse`](#json_parse) | 解析 JSON | `text` |
| [`json_get`](#json_get) | 获取 JSON 路径值 | `text`, `path` |
| [`json_stringify`](#json_stringify) | 序列化为 JSON | `data` |

---

#### json_parse

解析 JSON 字符串。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | JSON 字符串 |

**返回值**：格式化后的 JSON 字符串（便于阅读）。

---

#### json_get

从 JSON 中提取指定路径的值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | JSON 字符串 |
| `path` | string | **是** | - | 路径（如 `data.items.0`） |

**返回值**：路径对应的值。

---

#### json_stringify

将数据序列化为 JSON 字符串。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `data` | string | **是** | - | 数据对象（JSON 格式字符串） |
| `indent` | int | 否 | `2` | 缩进空格数 |

**返回值**：格式化的 JSON 字符串。

---

## 📝 std.text - 文本处理

文本处理工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`text_split`](#text_split) | 分割文本 | `text` |
| [`text_replace`](#text_replace) | 替换文本 | `text`, `old`, `new` |
| [`text_upper`](#text_upper) | 转大写 | `text` |
| [`text_lower`](#text_lower) | 转小写 | `text` |

---

#### text_split

分割文本为多个部分。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 待分割文本 |
| `delimiter` | string | 否 | `\n` | 分隔符 |
| `max_splits` | int | 否 | `-1` | 最大分割次数 (-1 表示不限) |

**返回值**：JSON 格式 `{ "parts": [string], "count": int }`。

---

#### text_replace

替换文本中的内容。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 原文本 |
| `old` | string | **是** | - | 被替换内容 |
| `new` | string | **是** | - | 替换内容 |
| `count` | int | 否 | `-1` | 替换次数 (-1 表示全部) |

**返回值**：替换后的文本。

---

#### text_upper

将文本转换为大写。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：大写文本。

---

#### text_lower

将文本转换为小写。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：小写文本。

---

## 🔐 std.hash - 加密与编码

哈希计算和编码工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`hash_md5`](#hash_md5) | MD5 哈希 | `text` |
| [`hash_sha256`](#hash_sha256) | SHA256 哈希 | `text` |
| [`base64_encode`](#base64_encode) | Base64 编码 | `text` |
| [`base64_decode`](#base64_decode) | Base64 解码 | `text` |

---

#### hash_md5

计算文本的 MD5 哈希值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：32 字符的 MD5 哈希字符串。

---

#### hash_sha256

计算文本的 SHA256 哈希值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：64 字符的 SHA256 哈希字符串。

---

#### base64_encode

将文本编码为 Base64 格式。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：Base64 编码字符串。

---

#### base64_decode

解码 Base64 文本。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | Base64 编码文本 |

**返回值**：解码后的原始文本。

---

## 🔢 std.math - 数学运算

数学计算工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`math_calc`](#math_calc) | 计算数学表达式 | `expression` |
| [`math_random`](#math_random) | 生成随机数 | `min_val`, `max_val` |

---

#### math_calc

安全计算数学表达式。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `expression` | string | **是** | - | 数学表达式 |

**返回值**：JSON 格式 `{ "result": number, "expression": string }`。

!!! warning "安全限制"
    只允许数字和 `+-*/.()` 字符，其他字符会被拒绝。

---

#### math_random

生成指定范围内的随机整数。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `min_val` | int | **是** | - | 最小值 |
| `max_val` | int | **是** | - | 最大值 |

**返回值**：随机整数。

---

## 🔍 std.regex - 正则表达式

正则表达式匹配和替换。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`regex_match`](#regex_match) | 正则匹配 | `pattern`, `text` |
| [`regex_replace`](#regex_replace) | 正则替换 | `pattern`, `replacement`, `text` |

---

#### regex_match

使用正则表达式匹配文本。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `pattern` | string | **是** | - | 正则表达式模式 |
| `text` | string | **是** | - | 待匹配文本 |
| `flags` | string | 否 | `""` | 标志：`i`(忽略大小写)、`m`(多行)、`s`(单行) |

**返回值**：JSON 格式 `{ "matches": [string], "count": int }`。

---

#### regex_replace

使用正则表达式替换文本。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `pattern` | string | **是** | - | 正则表达式模式 |
| `replacement` | string | **是** | - | 替换内容 |
| `text` | string | **是** | - | 待处理文本 |
| `flags` | string | 否 | `""` | 标志 |

**返回值**：替换后的文本。

---

## 💻 std.shell - Shell 命令

执行系统 Shell 命令。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`shell_exec`](#shell_exec) | 执行命令 | `command` |
| [`shell_which`](#shell_which) | 查找命令路径 | `command` |

---

#### shell_exec

执行 Shell 命令。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `command` | string | **是** | - | 要执行的命令 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "stdout": string, "stderr": string, "returncode": int, "success": bool }`。

!!! warning "安全警告"
    Shell 命令执行具有潜在风险，请确保不执行危险命令、验证输入参数、设置合理的超时时间。

---

#### shell_which

查找命令的可执行文件路径。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `command` | string | **是** | - | 命令名称 |

**返回值**：JSON 格式 `{ "command": string, "path": string, "found": bool }`。

---

## 🙋 std.ask_human - 人机交互

Human-in-the-Loop 交互工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`ask_human`](#ask_human) | 请求用户输入 | `prompt` |

---

#### ask_human

请求用户输入，实现 Human-in-the-Loop 交互。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `prompt` | string | **是** | - | 提示信息 |
| `default` | string | 否 | `""` | 默认值（用户不输入时使用） |

**返回值**：用户输入的字符串。

**示例**：

```nexa
agent HumanInterface uses std.ask_human {
    role: "人机交互助手",
    prompt: "与用户交互获取确认"
}

flow main {
    confirmation = HumanInterface.run("请确认是否继续执行？[y/n]");
}
```

---

## 🗄️ std.db.sqlite - SQLite 操作 (v1.3.5)

SQLite 数据库操作工具集。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_db_sqlite_connect` | 连接 SQLite | `path` |
| `std_db_sqlite_query` | 查询所有行 | `handle_json`, `sql` |
| `std_db_sqlite_query_one` | 查询单行 | `handle_json`, `sql` |
| `std_db_sqlite_execute` | 执行写操作 | `handle_json`, `sql` |
| `std_db_sqlite_close` | 关闭连接 | `handle_json` |
| `std_db_sqlite_begin` | 开始事务 | `handle_json` |
| `std_db_sqlite_commit` | 提交事务 | `handle_json` |
| `std_db_sqlite_rollback` | 回滚事务 | `handle_json` |

**使用示例**：

```nexa
db app_db = connect("sqlite://data.db")

flow main {
    // 通过 Agent 自然语言调用数据库操作
    result = DbAgent.run("查询 users 表中所有记录");
}
```

---

## 🗄️ std.db.postgres - PostgreSQL 操作 (v1.3.5)

PostgreSQL 数据库操作工具集。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_db_postgres_connect` | 连接 PostgreSQL | `url` |
| `std_db_postgres_query` | 查询所有行 | `handle_json`, `sql` |
| `std_db_postgres_query_one` | 查询单行 | `handle_json`, `sql` |
| `std_db_postgres_execute` | 执行写操作 | `handle_json`, `sql` |
| `std_db_postgres_close` | 关闭连接 | `handle_json` |
| `std_db_postgres_begin` | 开始事务 | `handle_json` |
| `std_db_postgres_commit` | 提交事务 | `handle_json` |
| `std_db_postgres_rollback` | 回滚事务 | `handle_json` |

---

## 🗄️ std.db.memory - Agent 记忆操作 (v1.3.5)

Agent 专属记忆数据库操作。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_db_memory_query` | Agent 记忆查询 | `handle_json`, `agent_name`, `key` |
| `std_db_memory_store` | Agent 记忆存储 | `handle_json`, `agent_name`, `key`, `value` |
| `std_db_memory_delete` | Agent 记忆删除 | `handle_json`, `agent_name`, `key` |
| `std_db_memory_list` | Agent 记忆列表 | `handle_json`, `agent_name` |

---

## 🔐 std.auth - 认证与 OAuth (v1.3.6)

三层认证系统：API Key + JWT (HS256) + OAuth 2.0 (PKCE flow)。

### 工具列表 (17 工具)

| 工具 | 说明 |
|-----|------|
| `std_auth_oauth` | OAuth 认证流程 |
| `std_auth_enable_auth` | 启用认证 |
| `std_auth_get_user` | 获取当前用户 |
| `std_auth_get_session` | 获取会话信息 |
| `std_auth_session_data` | 获取会话数据 |
| `std_auth_set_session` | 设置会话数据 |
| `std_auth_logout_user` | 用户登出 |
| `std_auth_require_auth` | 认证要求中间件 |
| `std_auth_jwt_sign` | JWT 签名 |
| `std_auth_jwt_verify` | JWT 验证 |
| `std_auth_jwt_decode` | JWT 解码 |
| `std_auth_csrf_token` | CSRF Token 生成 |
| `std_auth_csrf_field` | CSRF 表单字段 |
| `std_auth_verify_csrf` | CSRF 验证 |
| `std_auth_api_key_generate` | API Key 生成（格式：`nexa-ak-{random32hex}`） |
| `std_auth_api_key_verify` | API Key 验证 |
| `std_auth_auth_context` | Agent 认证上下文 |

**使用示例**：

```nexa
auth myAuth = enable_auth("providers_json")

flow main {
    // Agent API Key 生成
    key = std.auth.api_key_generate("my_agent")
    // 格式: nexa-ak-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
}
```

---

## 📦 std.kv - 键值存储 (v1.3.6)

内置 KV Store，SQLite 后端，支持 TTL 和 Agent 语义查询。

### 工具列表 (18 工具)

**通用 KV 操作 (15)**：

| 工具 | 说明 |
|-----|------|
| `std_kv_open` | 打开 KV Store |
| `std_kv_get` | 获取值 |
| `std_kv_get_int` | 获取整数值 |
| `std_kv_get_str` | 获取字符串值 |
| `std_kv_get_json` | 获取 JSON 值 |
| `std_kv_set` | 设置值 |
| `std_kv_set_nx` | 仅当不存在时设置 |
| `std_kv_del` | 删除键 |
| `std_kv_has` | 检查键是否存在 |
| `std_kv_list` | 列出所有键 |
| `std_kv_expire` | 设置 TTL |
| `std_kv_ttl` | 获取剩余 TTL |
| `std_kv_flush` | 清空 Store |
| `std_kv_incr` | 递增整数值 |

**Agent-Native KV 操作 (3)**：

| 工具 | 说明 |
|-----|------|
| `std_kv_agent_kv_query` | Agent 语义查询 |
| `std_kv_agent_kv_store` | Agent 记忆存储 |
| `std_kv_agent_kv_context` | Agent 上下文感知检索 |

**使用示例**：

```nexa
kv myCache = open("sqlite://cache.db")

flow main {
    // 通过 Agent 自然语言操作 KV
    result = CacheAgent.run("缓存用户偏好数据");
}
```

---

## ⚡ std.concurrent - 结构化并发 (v1.3.6)

结构化并发模块，提供 channel、spawn、parallel、race 等 18 个 API。

### 工具列表 (18 工具)

| 工具 | 说明 |
|-----|------|
| `std_concurrent_channel` | 创建通道 |
| `std_concurrent_send` | 发送消息 |
| `std_concurrent_recv` | 接收消息 |
| `std_concurrent_recv_timeout` | 超时接收 |
| `std_concurrent_try_recv` | 尝试接收 |
| `std_concurrent_close` | 关闭通道 |
| `std_concurrent_select` | 多通道选择 |
| `std_concurrent_spawn` | 启动任务 |
| `std_concurrent_await_task` | 等待任务完成 |
| `std_concurrent_try_await` | 尝试等待 |
| `std_concurrent_cancel_task` | 取消任务 |
| `std_concurrent_parallel` | 并行执行 |
| `std_concurrent_race` | 竞争执行 |
| `std_concurrent_after` | 延迟执行 |
| `std_concurrent_schedule` | 定时调度 |
| `std_concurrent_cancel_schedule` | 取消调度 |
| `std_concurrent_sleep_ms` | 毫秒级休眠 |
| `std_concurrent_thread_count` | 获取线程数 |

**并发 DSL 语法**：

```nexa
concurrent_decl {
    spawn my_task { ... }
    parallel [task_a, task_b, task_c]
    race [fast_task, slow_task]
    channel ch = channel()
    after 500ms { cleanup() }
    schedule every 30s { health_check() }
}
```

---

## 📄 std.template - 模板系统 (v1.3.6)

模板渲染引擎，支持 `template"""..."""` 语法、30+ 过滤器、Agent 模板扩展。

### 工具列表 (18+ 工具)

**核心模板操作**：

| 工具 | 说明 |
|-----|------|
| `std_template_render` | 渲染模板字符串 |
| `std_template_template` | 加载外部模板文件 |
| `std_template_compile` | 编译模板 |
| `std_template_render_compiled` | 渲染已编译模板 |
| `std_template_filter_apply` | 应用过滤器链 |

**Agent-Native 模板操作**：

| 工具 | 说明 |
|-----|------|
| `std_template_agent_prompt` | Agent 提示词模板 |
| `std_template_agent_slot_fill` | Agent 多源槽位填充 |
| `std_template_agent_register` | 注册 Agent 模板 |
| `std_template_agent_list` | 列出 Agent 模板 |

**过滤器工具**：

| 工具 | 说明 |
|-----|------|
| `std_template_filter_upper` | 转大写 |
| `std_template_filter_lower` | 转小写 |
| `std_template_filter_capitalize` | 首字母大写 |
| `std_template_filter_trim` | 去除空白 |
| `std_template_filter_default` | 默认值 |
| `std_template_filter_length` | 长度 |
| `std_template_filter_json` | JSON 序列化 |
| `std_template_filter_truncate` | 截断 |
| `std_template_filter_replace` | 替换 |
| `std_template_filter_escape` | HTML 转义 |
| `std_template_filter_date` | 日期格式化 |
| `std_template_filter_sort` | 排序 |
| `std_template_filter_unique` | 唯一值 |
| `std_template_filter_number` | 数字格式化 |
| `std_template_filter_url_encode` | URL 编码 |
| `std_template_filter_strip_tags` | 剥离 HTML 标签 |
| `std_template_filter_word_count` | 词数统计 |
| `std_template_filter_line_count` | 行数统计 |
| `std_template_filter_indent` | 缩进 |
| `std_template_filter_abs` | 绝对值 |
| `std_template_filter_ceil` | 向上取整 |
| `std_template_filter_floor` | 向下取整 |

**模板 DSL 语法**：

```nexa
// 模板字符串
template"""Hello {{name | upper}}!"""
template"""{{#for item in items}}{{@index}}:{{item}}{{/for}}"""
template"""{{#if is_admin}}Admin{{#elif is_mod}}Mod{{#else}}User{{/if}}"""
template"""{{> card user_data}}"""
```

**30+ 过滤器**：upper/lower/capitalize/trim/truncate(n)/replace(from,to)/escape/raw/safe/default(val)/length/first/last/reverse/join(sep)/slice(start,end)/json/number(n)/url_encode/strip_tags/word_count/line_count/indent/date/sort/unique/abs/ceil/floor

**ForLoop 元数据**：`@index`, `@index1`, `@first`, `@last`, `@length`, `@even`, `@odd`

---

## 🔗 std.pipe - 管道操作符 (v1.3.x)

管道操作符 `|>` 的 StdTool 封装。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_pipe_apply` | 管道函数应用 | `func`, `input` |

**语法**：

```nexa
// |> 管道操作符：左到右数据流
result |> format_output |> print
data |> std.text.upper
prompt |> agent.run |> extract_answer
```

---

## ⏳ std.defer - 延迟执行 (v1.3.x)

defer 语句的 StdTool 封装，确保 LIFO 清理。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_defer_schedule` | 注册延迟执行函数 | `func` |

**语法**：

```nexa
defer cleanup(db)
defer log("operation complete")
```

---

## ❓ std.null_coalesce - 空值合并 (v1.3.x)

`??` 操作符的 StdTool 封装。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_null_coalesce_apply` | 空值合并 | `left`, `right` |

**语法**：

```nexa
result ?? "fallback"
config.timeout ?? 30
agent.run(prompt) ?? "I couldn't process that"
```

---

## 📝 std.string - 字符串插值 (v1.3.x)

`#{expr}` 字符串插值的 StdTool 封装。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_string_interpolate` | 字符串插值 | `template`, `data` |

**语法**：

```nexa
"Hello #{name}, you are #{age} years old!"
"Status: #{result ?? 'pending'}"
"Agent #{agent.name} responding"
```

**插值表达式支持**：

| 表达式类型 | 示例 | Python 转译 |
|-----------|------|-------------|
| 简单标识符 | `#{name}` | `name` |
| 点访问 | `#{user.name}` | `user["name"]` |
| 括号访问 | `#{arr[0]}` | `arr[0]` |
| 组合 | `#{data.items[0].name}` | `data["items"][0]["name"]` |

**类型转换规则**：

| 输入类型 | 输出 |
|---------|------|
| `None` | `""` (空字符串) |
| `bool` | `"true"/"false"` |
| `int/float` | `str(value)` |
| `dict/list` | `json.dumps(value)` |
| `Option::Some` | unwrap 内部值 |
| `Option::None` | `""` |

---

## 🎯 std.match - 模式匹配 (v1.3.x)

模式匹配和解构的 StdTool 封装。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_match_pattern` | 模式匹配 | `value`, `pattern` |
| `std_match_destructure` | 解构 | `value`, `pattern` |
| `std_match_variant` | 构造变体 | `enum_name`, `variant_name`, `value` |

**7 种模式类型**：

1. **Wildcard**: `_` — 匹配任何值
2. **Variable**: `name` — 匹配并绑定变量
3. **Literal**: `42`, `"hello"`, `true`, `false` — 匹配精确值
4. **Tuple**: `(a, b)` — 匹配元组/数组
5. **Array**: `[a, b, ..rest]` — 匹配数组 + rest 收集
6. **Map**: `{ name, age: a, ..other }` — 匹配字典 + rest 收集
7. **Variant**: `Option::Some(v)` — 匹配枚举变体

---

## 🏗️ std.struct - 结构体 (v1.3.x)

ADT struct 的 StdTool 封装。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_adt_register_struct` | 注册结构体 | `name`, `fields` |
| `std_adt_make_struct` | 创建结构体实例 | `name`, `values` |
| `std_adt_lookup` | 查找结构体 | `name` |

**语法**：

```nexa
struct Point { x: Int, y: Int }
let p = Point(x: 1, y: 2)
```

**Handle-as-dict 格式**：

```json
{"_nexa_struct": "Point", "_nexa_struct_id": 1, "x": 1, "y": 2}
```

---

## 🏷️ std.enum - 枚举 (v1.3.x)

ADT enum 的 StdTool 封装。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_adt_register_enum` | 注册枚举 | `name`, `variants` |
| `std_adt_make_variant` | 创建变体 | `name`, `variant`, `value` |
| `std_adt_lookup` | 查找枚举 | `name` |

**语法**：

```nexa
enum Option { Some(value), None }
enum Result { Ok(value), Err(error) }
let opt = Option::Some(42)
```

**Handle-as-dict 格式**：

```json
// 带值变体
{"_nexa_variant": "Some", "_nexa_enum": "Option", "_nexa_variant_id": 1, "value": 42}
// 单元变体
{"_nexa_variant": "None", "_nexa_enum": "Option"}
```

---

## 🧬 std.trait - 特质与实现 (v1.3.x)

ADT trait/impl 的 StdTool 封装。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| `std_adt_register_trait` | 注册特质 | `name`, `methods` |
| `std_adt_register_impl` | 注册实现 | `trait_name`, `type_name`, `methods` |
| `std_adt_lookup` | 查找特质/实现 | `name` |
| `std_adt_summary` | 获取 ADT 概览 | 无 |
| `std_adt_reset` | 重置所有 ADT 注册表 | 无 |

**语法**：

```nexa
trait Printable { fn format() -> String }
impl Printable for Point { fn format() -> String { ... } }
```

---

## 🔧 使用方式

### 声明使用权限

在 Agent 定义中使用 `uses` 关键字声明：

```nexa
// 单个命名空间
agent MyAgent uses std.fs {
    prompt: "..."
}

// 多个命名空间
agent MultiToolAgent uses std.fs, std.http, std.time {
    prompt: "..."
}

// 新增命名空间
agent DbAgent uses std.db.sqlite, std.db.memory {
    prompt: "..."
}

agent AuthAgent uses std.auth {
    prompt: "..."
}

agent CacheAgent uses std.kv {
    prompt: "..."
}

agent ConcurrentAgent uses std.concurrent {
    prompt: "..."
}

agent TemplateAgent uses std.template {
    prompt: "..."
}
```

### 运行时调用

Agent 通过自然语言指令调用工具：

```nexa
agent Assistant uses std.fs, std.http {
    role: "多功能助手",
    prompt: "帮助用户完成文件和网络操作"
}

flow main {
    result = Assistant.run("读取 /tmp/data.txt 并 POST 到 https://api.example.com/upload");
    print(result);
}
```

---

## 📚 完整示例

### 日志管理 Agent

```nexa
agent LogManager uses std.fs, std.time {
    role: "日志管理专家",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是日志管理专家，可以：
    - 读取和分析日志文件
    - 创建和追加日志条目
    - 提供时间戳信息
    """
}

flow main {
    task = """
    1. 获取当前时间戳
    2. 创建日志条目：[时间戳] 系统启动
    3. 追加到 /var/log/nexa.log
    """;
    
    result = LogManager.run(task);
    print(result);
}
```

### API 数据抓取 Agent

```nexa
agent DataFetcher uses std.http, std.json {
    role: "数据抓取专家",
    prompt: "从 API 获取数据并解析 JSON"
}

flow main {
    task = """
    1. GET https://api.example.com/users
    2. 解析返回的 JSON
    3. 提取第一个用户的 name 字段
    """;
    
    name = DataFetcher.run(task);
    print(f"第一个用户: {name}");
}
```

### 数据库 + KV 缓存 Agent

```nexa
db app_db = connect("sqlite://data.db")
kv cache = open("sqlite://cache.db")

agent DbCacheAgent uses std.db.sqlite, std.kv {
    role: "数据库缓存助手",
    prompt: "查询数据库并缓存结果"
}

flow main {
    result = DbCacheAgent.run("查询用户表并缓存热门用户");
}
```

---

## 📊 版本历史

| 版本 | 更新内容 |
|-----|---------|
| v1.3.6 | 新增 `std.auth`, `std.kv`, `std.concurrent`, `std.template` 命名空间 |
| v1.3.5 | 新增 `std.db.sqlite`, `std.db.postgres`, `std.db.memory` 命名空间 |
| v1.3.x | 新增 `std.pipe`, `std.defer`, `std.null_coalesce`, `std.string`, `std.match`, `std.struct`, `std.enum`, `std.trait` 命名空间 |
| v1.0 | 新增 `std.text`, `std.hash`, `std.math`, `std.regex` 命名空间 |
| v0.9.7 | 新增 `std.shell`, `std.ask_human` 命名空间 |
| v0.7 | 初始标准库发布 (`std.fs`, `std.http`, `std.time`) |

---

## 🔗 相关资源

- [语言参考手册](reference.md)
- [CLI 命令参考](cli_reference.md)
- [错误索引](error_index.md)
- [快速入门](quickstart.md)