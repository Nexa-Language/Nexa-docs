---
comments: true
---

# 5. 生态集成与标准库：通向物理世界的大门

智能体的强大不仅仅来源于内部的逻辑流与思考，更取决于其触及外部物理世界广度与深度。在最近的版本迭代中，Nexa 引入了极为强大的模块化和原生设备穿透能力（Vision/标准库模块）。本章将详细介绍这些通向"大千世界"的接口。

---

## 📦 标准库扩展 (Standard Library)

在传统的胶水框架中，实现一个爬取网页并保存的 Agent，你需要自行安装 requests，手写 beautifulsoup 解析器，再打包成冗长的 Tool 供大模型调用。Nexa 中内置了原生的 `std` 标准库。

你可以通过 `uses` 关键字直接声明代理权限，Nexa 将自动处理沙盒环境的隔离和调用上下文。

### 标准库命名空间

| 命名空间 | 说明 | 主要工具 |
|---------|------|---------|
| `std.fs` | 文件系统操作 | `read`, `write`, `list`, `delete` |
| `std.http` | HTTP 网络请求 | `get`, `post`, `put`, `delete` |
| `std.time` | 时间相关操作 | `now`, `sleep`, `format` |
| `std.shell` | 系统终端命令 | `execute` |
| `std.ask_human` | 人机交互 | `call` |
| `std.json` | JSON 处理 | `parse`, `stringify` |
| `std.math` | 数学运算 | `calculate`, `random` |

---

## 📁 std.fs - 文件系统操作

文件系统操作是智能体与本地环境交互的基础能力。

### 可用工具

| 工具 | 说明 | 参数 |
|-----|------|------|
| `std.fs.read` | 读取文件内容 | `path: string` |
| `std.fs.write` | 写入文件 | `path: string`, `content: string` |
| `std.fs.append` | 追加内容 | `path: string`, `content: string` |
| `std.fs.list` | 列出目录内容 | `path: string` |
| `std.fs.delete` | 删除文件 | `path: string` |
| `std.fs.exists` | 检查文件是否存在 | `path: string` |

### 使用示例

```nexa
// 文件处理助手
agent FileAssistant uses std.fs {
    role: "文件管理助手",
    model: "deepseek/deepseek-chat",
    prompt: """
    你可以帮用户管理文件：
    - 读取文件内容
    - 创建和写入文件
    - 列出目录内容
    """
}

flow main {
    task = "读取 /tmp/notes.txt 文件内容并总结";
    result = FileAssistant.run(task);
    print(result);
}
```

### 完整示例：日志管理

```nexa
agent LogManager uses std.fs, std.time {
    role: "日志管理器",
    prompt: "管理系统日志文件，支持读取、写入和归档"
}

flow main {
    // 创建日志条目
    timestamp = std.time.now();
    log_entry = f"[{timestamp}] System started";
    
    // 写入日志
    LogManager.run(f"将 '{log_entry}' 写入 /var/log/system.log");
    
    // 读取日志
    logs = LogManager.run("读取 /var/log/system.log 的最后 10 行");
    print(logs);
}
```

---

## 🌐 std.http - HTTP 网络请求

原生的网络请求钩子，不仅能发出请求，内置解析器会自动将庞大的 HTML / 噪音清洗为干净可读的 Markdown 塞回给模型的上下文。

### 可用工具

| 工具 | 说明 | 参数 |
|-----|------|------|
| `std.http.get` | GET 请求 | `url: string`, `headers?: dict` |
| `std.http.post` | POST 请求 | `url: string`, `data: dict`, `headers?: dict` |
| `std.http.put` | PUT 请求 | `url: string`, `data: dict` |
| `std.http.delete` | DELETE 请求 | `url: string` |

### 使用示例

```nexa
// 网络请求助手
agent WebScraper uses std.http {
    role: "网页抓取助手",
    model: "deepseek/deepseek-chat",
    prompt: "抓取网页内容并提取关键信息"
}

flow main {
    url = "https://example.com/api/data";
    result = WebScraper.run(f"获取 {url} 的内容并提取标题");
    print(result);
}
```

### 完整示例：新闻聚合

```nexa
agent NewsAggregator uses std.http, std.fs, std.time {
    role: "新闻聚合器",
    model: "deepseek/deepseek-chat",
    prompt: """
    从多个新闻源获取最新新闻并汇总。
    将结果保存到本地文件。
    """,
    cache: true
}

flow main {
    news_sources = [
        "https://news.example.com/tech",
        "https://news.example.com/business"
    ];
    
    aggregated = NewsAggregator.run(f"""
    从以下源获取今日新闻并汇总：
    {news_sources}
    
    保存到 ~/news_summary.txt
    """);
    
    print(aggregated);
}
```

---

## ⏰ std.time - 时间系统

赋予被困在静态权重里的模型"真实的时间感"。

### 可用工具

| 工具 | 说明 | 返回值 |
|-----|------|--------|
| `std.time.now` | 获取当前时间 | ISO 格式时间字符串 |
| `std.time.timestamp` | 获取时间戳 | 整数 |
| `std.time.sleep` | 休眠 | 无 |
| `std.time.format` | 格式化时间 | 格式化字符串 |

### 使用示例

```nexa
agent TimeAwareBot uses std.time {
    role: "时间感知助手",
    prompt: "你知道当前时间，可以帮用户处理时间相关的任务"
}

flow main {
    // Agent 会自动获取当前时间
    response = TimeAwareBot.run("现在几点了？今天星期几？");
    print(response);
}
```

### 完整示例：日程提醒

```nexa
agent Scheduler uses std.time, std.fs {
    role: "日程管理助手",
    prompt: "管理用户日程，可以创建提醒和查看时间"
}

flow main {
    // 创建日程
    now = std.time.now();
    Scheduler.run(f"""
    当前时间：{now}
    创建一个明天上午 9 点的会议提醒
    """);
}
```

---

## 💻 std.shell - 系统终端命令

系统级终端下沉，执行底层操作。

!!! warning "安全警告"
    `std.shell` 具有较高的系统权限，请谨慎使用。建议配合 RBAC 权限控制。

### 可用工具

| 工具 | 说明 | 参数 |
|-----|------|------|
| `std.shell.execute` | 执行命令 | `command: string` |

### 使用示例

```nexa
agent DevOpsBot uses std.shell, std.fs {
    role: "运维助手",
    model: "deepseek/deepseek-chat",
    prompt: """
    执行系统运维任务：
    - 查看系统状态
    - 管理进程
    - 文件操作
    """
}

flow main {
    // 查看系统状态
    status = DevOpsBot.run("查看当前目录的文件列表");
    print(status);
}
```

---

## 🙋 std.ask_human - 人在回路 (HITL)

原生提供的人在回路（Human-in-the-loop, HITL）询问跳出机制。这是构建可靠 AI 系统的关键组件。

### 工作原理

```
Agent 遇到不确定情况
        │
        ▼
┌─────────────────────┐
│   std.ask_human     │
│   暂停执行，等待    │
└─────────────────────┘
        │
        ▼
    用户输入
        │
        ▼
┌─────────────────────┐
│   继续执行          │
└─────────────────────┘
```

### 使用示例

```nexa
agent RiskyOperationBot uses std.ask_human {
    role: "风险操作助手",
    prompt: """
    执行可能存在风险的操作。
    在执行重要操作前，必须询问用户确认。
    """
}

flow main {
    result = RiskyOperationBot.run("删除 /tmp/old_files 目录下的所有文件");
    print(result);
}
```

### 完整示例：审批流程

```nexa
agent ApprovalBot uses std.ask_human, std.fs {
    role: "审批助手",
    prompt: """
    处理需要审批的请求：
    1. 分析请求的风险等级
    2. 高风险操作必须获得人工确认
    3. 记录审批结果
    """
}

flow main {
    request = "批量更新生产环境的配置文件";
    
    result = ApprovalBot.run(request);
    print(result);
}
```

---

## 🔐 `secret`：敏感密钥的沙箱隔离

在处理云端 API 和数据库对接时，绝对不能将 `API_KEY` 明文写在代码和 Prompt 里！Nexa 设计了原生的安全池 `.nxs` (Nexa Secure) 机制和 `secret()` 函数。

### 配置密钥文件

在项目根目录创建 `secrets.nxs`：

```bash
# secrets.nxs
OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxx"
MINIMAX_API_KEY = "xxxxxxxxxxxx"
DATABASE_URL = "postgresql://user:pass@host:5432/db"
```

### 使用密钥

开发者可以在同目录的 `secrets.nxs` 中写入真实密钥，而在 `.nx` 代码中，你所流通的仅仅是一个受运行时保护的内存引用：

```nexa
flow main {
    // 仅仅是通过命名获取了加密指针，永远不会被打印或写入普通日志
    my_key = secret("MY_TEST_KEY");
    
    // Agent 在底层通过安全的 RPC 调用附带该密钥连接外部，保障了整个工作流的数据安全
    CloudDeployAgent.run("Deploy using the API credentials: ", my_key);
}
```

!!! warning "安全最佳实践"
    - **永远不要**将 `secrets.nxs` 提交到版本控制
    - 在 `.gitignore` 中添加 `secrets.nxs`
    - 生产环境使用环境变量或专用密钥管理服务

---

## 🧩 模块化革命：`include` 与 SKILLS.md

要实现大型企业级 AI 系统的大规模协作，就必须允许代码进行微服务级的拆分！Nexa 最新的模块化方案允许你实现优雅复用。

### 1. `.nxlib` 文件引用

你可以将大量常用的基础 Agent 或通信协议打包成专门的 `.nxlib` 库，主文件只需一行 `include`：

```nexa
include "utils.nxlib";

flow main {
    // LibAgent 来自于已经导入的 utils.nxlib，你可以像原生存放在此一样直接调用
    LibAgent.run("Echo this: module included successfully.");
}
```

**utils.nxlib 内容示例**：

```nexa
// utils.nxlib - 工具库

agent LibAgent {
    role: "通用工具 Agent",
    prompt: "处理通用任务"
}

protocol StandardResponse {
    status: "string",
    message: "string"
}

agent StandardAgent implements StandardResponse {
    prompt: "返回标准格式响应"
}
```

### 2. 跨语言 Markdown 技能挂载 (`uses "SKILLS.md"`)

对于极度复杂且需要人工微调的 Tool（比如某个特定业务领域的算法），Nexa 突破性地支持直接解析外部的 `.md` 技能定义本，只需要在 `uses` 声明对应的文档路径即可，底层 Runtime 会自动读取、解析并挂载那些大段的规则：

```nexa
// SKILLS.md 中存放了冗长的环境指导方针与外部函数
agent StreamBot uses "examples/SKILLS.md" {
    model: "minimax/minimax-m2.5",
    prompt: "I am a helpful assistant. Apply the skills strictly to solve this issue."
}
```

**SKILLS.md 格式示例**：

```markdown
# Agent 技能定义

## Tool: analyze_data
描述：分析数据并生成报告
参数：
- data: 要分析的数据（字符串）
- format: 输出格式（可选）

## Tool: send_notification
描述：发送通知消息
参数：
- message: 通知内容
- channel: 通知渠道（email/slack/sms）
```

---

## 👁️ 多模态先锋：全局内置的视觉原语 `img(...)`

从 V0.8 架构开始，Nexa 正式进入了全多模态感知的阶段。你再也不用手写繁琐的 `Base64` 编码转换或者 `multipart/form-data` 解析装配，语言级别的 `img` 类型函数替你搞定一切：

### 基本用法

```nexa
agent ResilientVisionAgent {
    model: "minimax/minimax-m2.5",
    prompt: "I test fallback and vision capabilities."
}

flow main {
    // 将指定路径下的静态图像直接转换为受引擎承认的内存多模态张量对象
    img_data = img("docs/img/logo.jpg");
    
    // 就像传入普通字符串一样传给 Agent，底层会自适应匹配 VLM (Vision Language Model) 数据流！
    result = ResilientVisionAgent.run("Inspect this image", img_data);
    print(result);
}
```

### 完整示例：图像分析流水线

```nexa
// 支持视觉的模型
agent ImageAnalyzer {
    model: "openai/gpt-4-vision-preview",
    prompt: "分析图像内容，识别主要元素和场景"
}

agent ImageDescriber {
    model: "deepseek/deepseek-chat",
    prompt: "将图像分析结果转换为自然语言描述"
}

flow main {
    // 加载图像
    image_path = "photos/landscape.jpg";
    image_data = img(image_path);
    
    // 分析图像
    analysis = ImageAnalyzer.run("描述这张图片", image_data);
    
    // 生成描述
    description = analysis >> ImageDescriber;
    
    print(description);
}
```

### 支持的图像格式

| 格式 | 扩展名 |
|-----|-------|
| JPEG | `.jpg`, `.jpeg` |
| PNG | `.png` |
| GIF | `.gif` |
| WebP | `.webp` |
| BMP | `.bmp` |

---

## 📊 标准库使用最佳实践

### 1. 最小权限原则

只授予 Agent 必要的工具权限：

```nexa
// ✅ 好的做法：只授予必要的权限
agent FileReader uses std.fs {
    prompt: "只读取文件"
}

// ❌ 不好的做法：授予过多权限
agent SimpleBot uses std.fs, std.http, std.shell {
    prompt: "只是简单对话"
}
```

### 2. 缓存常用请求

对于重复的网络请求启用缓存：

```nexa
agent CachedScraper uses std.http {
    cache: true,  // 减少重复请求
    prompt: "抓取网页内容"
}
```

### 3. 安全处理敏感信息

```nexa
// ✅ 使用 secret 函数
api_key = secret("API_KEY");
agent.run("使用 API", api_key);

// ❌ 不要硬编码
agent.run("使用 API key: sk-xxx");  // 危险！
```

---

## 📝 本章小结

在本章中，我们学习了：

| 模块 | 功能 | 使用场景 |
|-----|------|---------|
| `std.fs` | 文件系统 | 读写文件、目录管理 |
| `std.http` | 网络请求 | API 调用、网页抓取 |
| `std.time` | 时间操作 | 日程管理、时间感知 |
| `std.shell` | 系统命令 | 运维操作、脚本执行 |
| `std.ask_human` | 人机交互 | 审批流程、确认操作 |
| `secret()` | 密钥管理 | API 认证、数据库连接 |
| `img()` | 多模态 | 图像分析、视觉任务 |

Nexa 对于物理世界模块的封装，永远是以降低开发者的心智门槛、坚守系统沙盒安全性为最高原则。这些功能为你搭建自动化王国奠定了最扎实的水电煤基建。

---

## 🔗 相关资源

- [完整示例集合](examples.md) - 查看更多标准库使用示例
- [最佳实践](part6_best_practices.md) - 企业级开发经验
- [常见问题与排查](troubleshooting.md) - 工具调用问题解决
