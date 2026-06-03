---
comments: true
---

# 配置管理与标准库 (v2.1.2)

Nexa v2.1.2 引入了多配置切换和标准库系统，让不同环境（开发/测试/生产）使用不同的 API 密钥和模型配置，同时通过标准库提供开箱即用的工具。

---

## 🔧 多配置切换 (`use config`)

### 为什么需要多配置？

在实际开发中，不同环境需要不同的 API 配置：

- **开发环境**：使用测试 API 密钥，低成本模型
- **生产环境**：使用正式 API 密钥，高性能模型
- **CI/CD**：使用专用测试密钥

Nexa 通过 `secrets.nxs` 文件中的 config block 和 `use config` 语句实现这一需求。

### 定义多个配置

在 `secrets.nxs` 中定义多个 config block：

```nexa
// secrets.nxs
config default {
    BASE_URL = "https://aihub.arcsysu.cn/v1"
    API_KEY = "sk-dev-key-xxx"
    MODEL_NAME = {
        "strong": "minimax-m2.5",
        "weak": "deepseek-chat"
    }
}

config production {
    BASE_URL = "https://api.openai.com/v1"
    API_KEY = "sk-prod-key-yyy"
    MODEL_NAME = {
        "strong": "gpt-4-turbo",
        "weak": "gpt-3.5-turbo"
    }
}

config ali {
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    API_KEY = "sk-ali-key-zzz"
    NEWS_API_KEY = "your-newsapi-key"
    MODEL_NAME = {
        "strong": "qwen-max",
        "weak": "deepseek-v4-pro"
    }
}
```

### 在程序中选择配置

在 `.nx` 文件顶部使用 `use config <name>` 语句：

```nexa
// my_program.nx
use config ali;

agent MyAgent {
    model: "deepseek-v4-pro",
    prompt: "You are a helpful assistant."
}

flow main {
    result = MyAgent.run("Hello!");
    print(result);
}
```

### 配置加载优先级

Nexa 按以下顺序加载配置：

1. **当前目录**的 `secrets.nxs`
2. **父目录**的 `secrets.nxs`（向上搜索最多 10 级）
3. **脚本所在目录**的 `secrets.nxs`（通过 `load_from_script_dir`）

后加载的配置会覆盖先加载的同名 config block。

### 配置项说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `BASE_URL` | API 端点 | `"https://api.openai.com/v1"` |
| `API_KEY` | API 密钥 | `"sk-xxx"` |
| `MODEL_NAME` | 模型配置（嵌套 dict） | `{"strong": "gpt-4", "weak": "gpt-3.5"}` |
| `NEWS_API_KEY` | NewsAPI 密钥（标准库用） | `"your-key"` |
| `NEWS_PAGE_SIZE` | 新闻返回条数（默认 5） | `"10"` |
| `NEWS_DAYS_BACK` | 新闻搜索天数范围（默认 7） | `"14"` |

---

## 📦 标准库 (`stdlib/`)

Nexa 标准库位于 `stdlib/` 目录，通过 `include` 语句引入。

### 引入标准库

```nexa
include "stdlib/news.nx";
```

Nexa 编译器会自动在以下路径搜索 include 文件：

1. 当前 `.nx` 文件所在目录
2. `stdlib/` 目录（项目根目录下）

### 工具可见性

**重要**：Agent 只能看到通过 `uses` 声明的工具。这是 Nexa 的安全设计——防止 Agent 意外调用未授权的工具。

```nexa
include "stdlib/news.nx";

// ✅ 正确：声明使用 search_news
agent SearchAgent uses search_news {
    prompt: "Search for news."
}

// ❌ 错误：未声明 uses，Agent 看不到 search_news
agent BadAgent {
    prompt: "Search for news."  // 无法调用 search_news
}
```

### 当前可用的标准库

#### `stdlib/news.nx` — 新闻搜索

使用 [NewsAPI](https://newsapi.org/) 搜索新闻文章。

**配置要求**：在 `secrets.nxs` 中设置 `NEWS_API_KEY`。

**工具函数**：

```nexa
@tool("Search news articles using NewsAPI")
fn search_news(query: string): string
```

**使用示例**：

```nexa
include "stdlib/news.nx";
use config ali;  // 确保 ali config 中有 NEWS_API_KEY

agent NewsAgent uses search_news {
    model: "deepseek-v4-pro",
    prompt: "You are a news search agent. Use search_news to find articles."
}

flow main {
    result = NewsAgent.run("Find latest AI news");
    print(result);
}
```

**返回格式**：

```
Found 5 articles for 'latest AI news':

1. [The Verge] Article Title (2026-06-01)
   Article description...
   URL: https://...

2. [TechCrunch] Another Article (2026-05-30)
   ...
```

---

## 🔒 Harness Validator 模式

Nexa v2.1.2 增强了 Harness Validator 的 strict/warn 模式区分。

### warn 模式（默认）

警告但编译继续。适用于开发阶段：

```bash
$ nexa build program.nx --harness=warn
  ⚡ V-003: autoloop without verify (severity='warning')
  ⚡ X-002: Agent uses only 0 Harness dimensions (severity='warning')
✨ Success! Built target: program.py
```

### strict 模式

所有 warnings 升级为 errors，阻断编译。适用于生产部署：

```bash
$ nexa build program.nx --harness=strict
❌ Harness validation failed (strict mode):
  • V-003: autoloop without verify (severity='error')
  • X-002: Agent uses only 0 Harness dimensions (severity='error')
```

### off 模式

跳过所有验证。适用于快速原型或 v1.x 兼容：

```bash
$ nexa build program.nx --harness=off
✨ Success! Built target: program.py
```

---

## 📝 完整示例

一个使用多配置和标准库的完整示例：

```nexa
/*
  完整示例：多配置 + 标准库 + Harness
*/

// 引入标准库
include "stdlib/news.nx";

// 使用 ali 配置（包含 NEWS_API_KEY）
use config ali;

// 声明使用 search_news 工具
agent NewsResearcher uses search_news {
    model: "deepseek-v4-pro",
    prompt: """
    You are a news research agent.
    Use search_news to find recent articles on the given topic.
    Return a summary of the top 3 most relevant articles.
    """
}

agent Summarizer {
    model: "deepseek-v4-pro",
    prompt: "Summarize the given news research into a concise briefing."
}

flow main {
    print("=== News Research Pipeline ===");
    
    // 搜索新闻
    research = NewsResearcher.run("AI regulation in 2026");
    print("Research:");
    print(research);
    
    // 总结
    briefing = research >> Summarizer;
    print("\nBriefing:");
    print(briefing);
}
```

运行：

```bash
$ nexa run news_research.nx
=== News Research Pipeline ===
Research:
Found 5 articles for 'AI regulation in 2026':
...

Briefing:
...
```
