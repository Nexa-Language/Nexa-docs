---
comments: true
---

# 5. 企业级架构特性 (v1.3.x)

在 Nexa 的演进历程中，它早已不是一个仅供调用的玩具脚本语言。为了支撑严肃的大规模生产环境运转，Nexa v1.3.x 引入了 HTTP Server、数据库集成、认证系统、KV 存储、结构化并发、模板引擎和后台任务系统等一系列企业级功能。

---

## 🌐 内置 HTTP Server (v1.3.4)

Nexa v1.3.4 引入了原生 HTTP Server DSL，让你无需外部框架即可将 Agent 流程发布为 REST API 服务。

### Server 声明

```nexa
server MyApp {
    route GET "/hello" {
        handler: hello_flow
    }
    
    route POST "/analyze" {
        requires: request.body != ""
        handler: analyze_flow
    }
    
    route GET "/report/{id}" {
        handler: report_flow
    }
}
```

### 启动服务

```bash
# 启动 HTTP Server
nexa serve main.nexa

# 指定端口
nexa serve main.nexa --port 8080
```

### 查看路由

```bash
# 列出所有路由
nexa routes main.nexa

# JSON 格式输出
nexa routes main.nexa --json
```

### 契约与 HTTP 状态码映射

Server 路由中的契约条款自动映射为 HTTP 状态码：

| 契约类型 | HTTP 状态码 | 说明 |
|---------|------------|------|
| `requires` 违反 | 401 Unauthorized | 请求未满足前置条件 |
| `ensures` 违反 | 403 Forbidden | 响应未满足后置条件 |

```nexa
server PaymentAPI {
    route POST "/transfer" {
        requires: amount > 0           // 违反 → 401
        requires: sender != ""         // 违反 → 401
        ensures: result.success        // 违反 → 403
        handler: transfer_flow
    }
}
```

### 完整示例：Agent API 服务

```nexa
agent Analyzer {
    role: "数据分析专家",
    prompt: "分析输入数据并返回结构化报告"
}

protocol AnalysisResult {
    summary: "string",
    score: "int",
    details: "list[string]"
}

agent StructuredAnalyzer implements AnalysisResult {
    role: "结构化分析专家",
    prompt: "分析数据并返回包含 summary、score 和 details 的 JSON"
}

server DataAPI {
    route POST "/analyze" {
        requires: request.body != ""
        handler: analyze_flow
    }
    
    route GET "/status" {
        handler: status_flow
    }
}

flow analyze_flow(request) {
    result = StructuredAnalyzer.run(request.body);
    return result;
}

flow status_flow(request) {
    return {"status": "ok", "version": "1.3.4"};
}
```

---

## 🗄️ 数据库集成 (v1.3.5)

Nexa v1.3.5 引入了原生数据库集成，支持 SQLite、PostgreSQL 和 Agent 记忆存储，通过 `db` 声明和 `std.db.*` 标准库工具操作。

### DB 声明

```nexa
db main_db {
    type: sqlite
    path: "data.db"
}
```

### SQLite 操作 (std.db.sqlite)

```nexa
flow main {
    // 连接数据库
    handle = std.db.sqlite.connect("data.db");
    defer std.db.sqlite.close(handle);  // 自动关闭
    
    // 创建表
    std.db.sqlite.execute(handle, 
        "CREATE TABLE IF NOT EXISTS users (id INT, name TEXT, age INT)");
    
    // 插入数据
    std.db.sqlite.execute(handle, 
        "INSERT INTO users VALUES (1, 'Alice', 30)",
        []);
    
    // 查询所有行
    rows = std.db.sqlite.query(handle, "SELECT * FROM users");
    print(rows);
    
    // 查询单行
    row = std.db.sqlite.query_one(handle, 
        "SELECT * FROM users WHERE id = 1");
    print(row);
    
    // 事务操作
    std.db.sqlite.begin(handle);
    std.db.sqlite.execute(handle, "INSERT INTO users VALUES (2, 'Bob', 25)");
    std.db.sqlite.commit(handle);
}
```

### PostgreSQL 操作 (std.db.postgres)

```nexa
flow main {
    // 连接 PostgreSQL
    handle = std.db.postgres.connect("postgresql://user:pass@localhost/mydb");
    defer std.db.postgres.close(handle);
    
    // 查询
    rows = std.db.postgres.query(handle, "SELECT * FROM products");
    
    // 带参数查询
    row = std.db.postgres.query_one(handle, 
        "SELECT * FROM products WHERE id = $1", ["42"]);
    
    // 事务
    std.db.postgres.begin(handle);
    std.db.postgres.execute(handle, "UPDATE products SET price = $1 WHERE id = $2", ["99.99", "42"]);
    std.db.postgres.commit(handle);
}
```

### Agent 记忆存储 (std.db.memory)

```nexa
flow main {
    // 存储 Agent 记忆
    std.db.memory.store(handle, "Analyst", "last_topic", "quantum computing");
    
    // 查询 Agent 记忆
    memory = std.db.memory.query(handle, "Analyst", "last_topic");
    print(memory);  // "quantum computing"
    
    // 列出所有记忆
    all_memories = std.db.memory.list(handle, "Analyst");
    
    // 删除记忆
    std.db.memory.delete(handle, "Analyst", "last_topic");
}
```

---

## 🔐 认证与 OAuth (v1.3.6)

Nexa v1.3.6 引入了完整的认证系统，支持 OAuth 2.0 PKCE 流程、JWT、CSRF 保护、API Key 等多种认证方式。

### Auth 声明

```nexa
auth my_auth {
    providers: ["google", "github"]
    jwt_secret: "your-secret-key"
    csrf_enabled: true
}
```

### OAuth 流程

```nexa
flow main {
    // 启动 OAuth 认证
    auth_url = std.auth.oauth(name: "google");
    print("请访问: #{auth_url}");
    
    // 启用认证中间件
    std.auth.enable_auth(providers: ["google", "github"]);
}
```

### JWT 操作

```nexa
flow main {
    // 签发 JWT
    token = std.auth.jwt_sign(claims: {"user_id": "123", "role": "admin"});
    print("Token: #{token}");
    
    // 验证 JWT
    valid = std.auth.jwt_verify(token: token);
    print("Valid: #{valid}");
    
    // 解码 JWT
    claims = std.auth.jwt_decode(token: token);
    print("Claims: #{claims}");
}
```

### CSRF 保护

```nexa
flow main {
    // 生成 CSRF Token
    csrf_token = std.auth.csrf_token(request: request);
    
    // 生成 CSRF 表单字段
    csrf_field = std.auth.csrf_field(request: request);
    // 输出: <input type="hidden" name="csrf_token" value="xxx">
    
    // 验证 CSRF
    is_valid = std.auth.verify_csrf(request: request);
}
```

### API Key 管理

```nexa
flow main {
    // 生成 API Key（格式: nexa-ak-{32hex}）
    api_key = std.auth.api_key_generate(agent_name: "MyAgent");
    print("API Key: #{api_key}");
    
    // 验证 API Key
    is_valid = std.auth.api_key_verify(api_key: api_key);
    
    // 获取认证上下文
    context = std.auth.auth_context(request: request);
}
```

### 用户会话管理

```nexa
flow main {
    // 获取用户信息
    user = std.auth.get_user(request: request);
    
    // 获取会话数据
    session = std.auth.get_session(request: request);
    
    // 获取会话详细数据
    data = std.auth.session_data(request: request);
    
    // 设置会话
    std.auth.set_session(request: request, data: {"theme": "dark"});
    
    // 登出
    std.auth.logout_user(request: request);
    
    // 要求认证
    std.auth.require_auth(request: request);
}
```

---

## 📦 KV 键值存储 (v1.3.6)

Nexa v1.3.6 引入了内置 KV 存储，支持内存和持久化模式，提供类型安全的读写操作和 TTL 过期机制。

### KV 声明

```nexa
kv my_cache {
    path: ":memory:"
}
```

### 基本操作

```nexa
flow main {
    // 打开 KV 存储
    kv_handle = std.kv.open(path: ":memory:");
    
    // 写入
    std.kv.set(kv: kv_handle, key: "user_name", value: "Alice");
    
    // 读取
    name = std.kv.get(kv: kv_handle, key: "user_name");
    print(name);  // "Alice"
    
    // 类型安全读取
    count = std.kv.get_int(kv: kv_handle, key: "visit_count");
    label = std.kv.get_str(kv: kv_handle, key: "label");
    config = std.kv.get_json(kv: kv_handle, key: "config");
    
    // 仅当键不存在时设置（SET NX）
    std.kv.set_nx(kv: kv_handle, key: "first_visit", value: "2024-01-01");
    
    // 检查键是否存在
    exists = std.kv.has(kv: kv_handle, key: "user_name");
    
    // 列出所有键
    keys = std.kv.list(kv: kv_handle);
    
    // 删除键
    std.kv.del(kv: kv_handle, key: "temp_data");
    
    // 设置 TTL（秒）
    std.kv.expire(kv: kv_handle, key: "session", ttl: 3600);
    
    // 查看 TTL
    remaining = std.kv.ttl(kv: kv_handle, key: "session");
    
    // 自增
    std.kv.incr(kv: kv_handle, key: "counter");
    
    // 清空
    std.kv.flush(kv: kv_handle);
}
```

### Agent 专属 KV 操作

```nexa
flow main {
    // Agent KV 查询
    result = std.kv.agent_kv_query(kv: kv_handle, agent_name: "Analyst", key: "context");
    
    // Agent KV 存储
    std.kv.agent_kv_store(kv: kv_handle, agent_name: "Analyst", key: "context", value: "market data");
    
    // Agent KV 上下文
    context = std.kv.agent_kv_context(kv: kv_handle, agent_name: "Analyst");
}
```

### 与 `??` 组合使用

```nexa
flow main {
    // KV 读取 + 空值合并
    theme = std.kv.get(kv: kv_handle, key: "theme") ?? "light";
    lang = std.kv.get(kv: kv_handle, key: "language") ?? "en";
}
```

---

## ⚡ 结构化并发 (v1.3.6)

Nexa v1.3.6 引入了结构化并发系统，提供 Channel、spawn、parallel、race 等原语，确保并发任务的生命周期始终受控。

### 并发表达式

```nexa
// spawn — 启动异步任务
task = spawn handler_fn(args)

// await — 等待任务完成
result = await task

// parallel — 并行执行多个任务
results = parallel [handler1, handler2, handler3]

// race — 竞争执行，返回最先完成的结果
winner = race [handler1, handler2]
```

### Channel 操作 (std.concurrent)

```nexa
flow main {
    // 创建通道
    (tx, rx) = std.concurrent.channel();
    
    // 发送消息
    std.concurrent.send(tx: tx, value: "hello");
    
    // 接收消息
    msg = std.concurrent.recv(rx: rx);
    print(msg);  // "hello"
    
    // 超时接收
    msg = std.concurrent.recv_timeout(rx: rx, timeout: 5000);
    
    // 非阻塞接收
    result = std.concurrent.try_recv(rx: rx);
    
    // 关闭通道
    std.concurrent.close(rx: rx);
    
    // Select — 多通道选择
    value = std.concurrent.select(channels: [rx1, rx2]);
}
```

### 任务管理

```nexa
flow main {
    // 启动异步任务
    task = std.concurrent.spawn(handler: "process_data");
    
    // 等待任务完成
    result = std.concurrent.await_task(task: task);
    
    // 非阻塞等待
    result = std.concurrent.try_await(task: task);
    
    // 取消任务
    std.concurrent.cancel_task(task: task);
    
    // 并行执行
    results = std.concurrent.parallel(handlers: ["handler1", "handler2", "handler3"]);
    
    // 竞争执行
    winner = std.concurrent.race(handlers: ["fast_handler", "backup_handler"]);
    
    // 延迟执行
    std.concurrent.after(delay: 1000, handler: "cleanup");
    
    // 定时执行
    schedule = std.concurrent.schedule(interval: 5000, handler: "health_check");
    
    // 取消定时
    std.concurrent.cancel_schedule(schedule: schedule);
    
    // 线程计数
    count = std.concurrent.thread_count();
}
```

### 完整示例：并发数据处理

```nexa
flow main {
    // 并行分析多个数据源
    results = std.concurrent.parallel(handlers: [
        "analyze_market_data",
        "analyze_social_data",
        "analyze_news_data"
    ]);
    
    // 竞争：快速响应 + 备用方案
    quick_result = std.concurrent.race(handlers: [
        "fast_analysis",
        "deep_analysis"
    ]);
    
    // 使用 Channel 协调
    (tx, rx) = std.concurrent.channel();
    
    // 发送任务
    std.concurrent.send(tx: tx, value: raw_data);
    
    // 接收结果
    processed = std.concurrent.recv_timeout(rx: rx, timeout: 10000);
    
    std.concurrent.close(rx: rx);
}
```

---

## 📄 模板系统 (v1.3.6)

Nexa v1.3.6 引入了内置模板引擎，支持变量插值、条件渲染、循环、过滤器、Agent 插槽填充等高级功能。

### 模板字符串字面量

```nexa
// 使用 template"""...""" 定义模板
template"""Hello {{name}}, your score is {{score | default(0)}}!"""
```

### 模板操作 (std.template)

```nexa
flow main {
    // 渲染模板字符串
    result = std.template.render(
        template_str: "Hello {{name}}!",
        data: {"name": "Alice"}
    );
    print(result);  // "Hello Alice!"
    
    // 从文件加载模板
    compiled = std.template.template(path: "report_template.nxt");
    
    // 编译模板
    compiled = std.template.compile(path: "email_template.nxt");
    
    // 渲染已编译模板
    output = std.template.render_compiled(
        compiled: compiled,
        data: {"user": "Bob", "date": "2024-01-01"}
    );
    
    // 应用过滤器
    formatted = std.template.filter_apply(
        value: "hello world",
        filter: "upper"
    );
}
```

### Agent 模板操作

```nexa
flow main {
    // Agent Prompt 模板
    prompt = std.template.agent_prompt(
        agent: Analyzer,
        template: "Analyze the following: {{input}}"
    );
    
    // Agent Slot 填充
    filled = std.template.agent_slot_fill(
        agent: Analyzer,
        slots: {"topic": "AI trends", "depth": "detailed"}
    );
    
    // 注册 Agent 模板
    std.template.agent_register(
        agent: Analyzer,
        template: "report_template"
    );
}
```

### 模板语法参考

| 语法 | 说明 | 示例 |
|-----|------|------|
| `{{var}}` | 变量插值 | `{{name}}` |
| `{{var | filter}}` | 过滤器 | `{{price | round(2)}}` |
| `{{var | default(val)}}` | 默认值 | `{{age | default(0)}}` |
| `{{#for item in list}}` | 循环 | `{{#for p in products}}...{{/for}}` |
| `{{#if condition}}` | 条件 | `{{#if score > 80}}...{{/if}}` |
| `{{#include path}}` | 包含子模板 | `{{#include header.nxt}}` |

---

## 📋 后台任务系统 (v1.3.3)

Nexa v1.3.3 引入了后台任务（Job）系统，支持异步执行、重试、超时、死信队列和 Worker 管理。

### Job 声明

```nexa
job SendEmail {
    handler: email_handler
    retry: 3
    timeout: 120
    on_failure: notify_admin
}
```

### Job 管理 CLI

```bash
# 查看所有任务
nexa jobs main.nexa --all

# 查看特定状态的任务
nexa jobs main.nexa --status failed

# 查看死信队列
nexa jobs main.nexa --dead-letter

# 清理已完成任务
nexa jobs main.nexa --clear-completed

# 重试死信任务
nexa jobs main.nexa --retry <job_id>
```

### Worker 管理 CLI

```bash
# 查看 Worker 状态
nexa workers main.nexa

# 启动额外 Worker
nexa workers main.nexa --add 2

# 停止 Worker
nexa workers main.nexa --stop <worker_id>
```

### 完整示例：异步邮件系统

```nexa
job SendEmail {
    handler: send_email_flow
    retry: 3
    timeout: 60
    on_failure: log_failure
}

flow send_email_flow(to: string, subject: string, body: string) {
    result = EmailAgent.run("Send email to #{to} with subject #{subject}");
    return result;
}

flow log_failure(job_info) {
    std.fs.file_append("failed_emails.log", 
        "Failed: #{job_info.id} at #{std.time.time_now()}");
}

server EmailAPI {
    route POST "/send" {
        handler: api_send_email
    }
}

flow api_send_email(request) {
    // 异步发送邮件（不阻塞 HTTP 响应）
    job_id = spawn SendEmail(
        to: request.to,
        subject: request.subject,
        body: request.body
    );
    return {"status": "queued", "job_id": job_id};
}
```

---

## 🧠 认知架构与复合长短期记忆 (Memory Engine)

在之前的传统开发中，如果让机器人具备持久化的上下文，我们常需要对接庞杂的 Pinecone、Redis 栈以及复杂的手动消息裁剪逻辑。在 Nexa 中只需切换参数即可接入极具威力的底层架构：

- **长效外接记忆系统 (Long-term Memory)**：支持高阶语义记忆，自动总结归档用户体验、偏好和隐式法则，并在未来相关对谈中全自动抽取投喂。
- **动态知识图谱映射 (Knowledge Graph)**：原生记忆系统可在幕后提取文本三元组，自行维护 SQLite 和 Vector FTS，使 Agent 可以自主建立、追踪事物的图谱式关联。
- **内置上下文压缩器 (Context Compactor)**：当长对话逼近 Token 上限时，Nexa 嵌入了可插拔的实体提取型压缩策略，将千字长文在保留核心关键决策的前提下挤压至极小的上下文结构。

---

## ⚡ 多层语义计算缓存 (L1/L2 Cache)

1. **L1 内存热缓存 (In-Memory)**：拦截极高频、极低延时的请求碰撞。
2. **L2 磁盘冷缓存**：确保持久化查询留存并提供 TTL 生存期超时支持和按需 LRU 驱逐。
3. **语义映射命中 (Semantic Match)**：内嵌局部相似度算法，哪怕用户换了一个词询问同一个意思，也能直接击中缓存屏障省去一次昂贵的 LLM API 呼叫。

---

## 🛡️ 基于角色的访问控制模型 (RBAC Sandbox)

- **预设系统角色**：为各个运行时沙盒实体分配安全类别，如 `admin`、`agent_standard`、`agent_readonly`。
- **细粒度工具锁**：当外部不受信任的用户企图让 Agent 调用危险指令时，后台守护栈会自动拦截，触发鉴权拒绝，从根本上防止 Prompt 注入越权造成的灾难。

---

## 📊 本章小结

在本章中，我们学习了 Nexa 的企业级架构特性：

| 特性 | 版本 | 说明 | 使用场景 |
|-----|------|------|---------|
| HTTP Server | v1.3.4 | 原生 REST API 服务 | Agent API 发布 |
| Database | v1.3.5 | SQLite/PostgreSQL/Agent Memory | 数据持久化 |
| Auth & OAuth | v1.3.6 | JWT/CSRF/API Key/OAuth | 认证与安全 |
| KV Store | v1.3.6 | 类型安全键值存储 | 缓存与配置 |
| Concurrency | v1.3.6 | Channel/spawn/parallel/race | 结构化并发 |
| Template | v1.3.6 | 模板引擎+Agent插槽 | 动态内容生成 |
| Job System | v1.3.3 | 异步任务+重试+死信队列 | 后台任务处理 |
| Memory Engine | v0.9+ | 长短期记忆+知识图谱 | Agent 记忆持久化 |
| L1/L2 Cache | v0.9+ | 语义计算缓存 | 成本优化 |
| RBAC Sandbox | v0.9+ | 角色访问控制 | 安全防护 |

这些企业级特性让 Nexa 从一个 Agent 编排语言进化为完整的 Agent 应用平台，能够支撑从原型到大规模生产的全生命周期。

---

## 🔗 相关资源

- [CLI 命令参考](cli_reference.md) - serve/routes/jobs/workers 命令详解
- [标准库 API](stdlib_reference.md) - std.db/std.auth/std.kv/std.concurrent/std.template 工具详解
- [语言参考手册](reference.md) - server/db/auth/kv/job 声明语法
- [错误索引](error_index.md) - 数据库/认证/KV/并发/模板/HTTP 错误码
- [最佳实践](part6_best_practices.md) - 企业级开发经验