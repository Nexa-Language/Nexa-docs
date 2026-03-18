---
comments: true
---

# 5. 生态集成与标准库：通向物理世界的大门

智能体的强大不仅仅来源于内部的逻辑流与思考，更取决于其触及外部物理世界广度与深度。在最近的版本迭代中，Nexa 引入了极为强大的模块化和原生设备穿透能力（Vision/标准库模块）。本章将详细介绍这些通向“大千世界”的接口。

---

## 📦 标准库扩展 (Standard Library)
在传统的胶水框架中，实现一个爬取网页并保存的 Agent，你需要自行安装 requests，手写 beautifulsoup 解析器，再打包成冗长的 Tool 供大模型调用。Nexa 中内置了原生的 `std` 标准库。
你可以通过 `uses` 关键字直接声明代理权限，Nexa 将自动处理沙盒环境的隔离和调用上下文。

目前原生的标准库命名空间大幅扩充，包括：
- `std.fs`：文件系统操作（读、写、列出目录属性），支持相对路径和安全拦截。
- `std.http`：原生的网络请求钩子，不仅能发出请求，内置解析器会自动将庞大的 HTML / 噪音清洗为干净可读的 Markdown 塞回给模型的上下文。
- `std.time`：赋予被困在静态权重里的模型“真实的时间感”。
- `std.shell`：系统级终端下沉，执行底层操作。
- `std.ask_human`：原生提供的人在回路（Human-in-the-loop, HITL）询问跳出机制。

**实战：新闻资讯抓取聚合流**
```nexa
// Nexa Agent 直接通过 uses 集成多维度环境
agent Researcher uses std.time, std.http, std.fs {
    prompt: "You are an intelligent news researcher. Your job is to fetch the current date, then fetch top news from a given URL, summarize the top 3 items, and save the result into a local file with the date included in the summary.",
    model: "minimax-m2.5"
}

flow main {
    msg = "Please fetch the current time, then fetch news from https://lite.cnn.com. Extract top 3 headlines and save them to `examples/today_news.md` using the file system tool.";
    Researcher.run(msg);
}
```

---

## 🔐 `secret`：敏感密钥的沙箱隔离 
在处理云端 API 和数据库对接时，绝对不能将 `API_KEY` 明文写在代码和 Prompt 里！Nexa 设计了原生的安全池 `.nxs` (Nexa Secure) 机制和 `secret()` 函数。

开发者可以在同目录的 `secrets.nxs` 中写入真实密钥，而在 `.nx` 代码中，你所流通的仅仅是一个受运行时保护的内存引用：
```nexa
flow main {
    // 仅仅是通过命名获取了加密指针，永远不会被打印或写入普通日志
    my_key = secret("MY_TEST_KEY");
    
    // Agent 在底层通过安全的 RPC 调用附带该密钥连接外部，保障了整个工作流的数据安全
    CloudDeployAgent.run("Deploy using the API credentials: ", my_key);
}
```

---

## 🧩 模块化革命：`include .nxlib` 与 SKILLS.md
要实现大型企业级 AI 系统的大规模协作，就必须允许代码进行微服务级的拆分！Nexa 最新的模块化方案允许你实现优雅复用：
1. **`.nxlib` 文件引用**：
你可以将大量常用的基础 Agent 或通信协议打包成专门的 `.nxlib` 库，主文件只需一行 `include`：
```nexa
include "utils.nxlib";

flow main {
    // LibAgent 来自于已经导入的 utils.nxlib，你可以像原生存放在此一样直接调用
    LibAgent.run("Echo this: module included successfully.");
}
```

2. **跨语言 Markdown 技能挂载 (`uses "SKILLS.md"`)**：
对于极度复杂且需要人工微调的 Tool （比如某个特定业务领域的算法）。Nexa 突破性地支持直接解析外部的 `.md` 技能定义本，只需要在 `uses` 声明对应的文档路径即可，底层 Runtime 会自动读取、解析并挂载那些大段的规则：
```nexa
// SKILLS.md 中存放了冗长的环境指导方针与外部函数
agent StreamBot uses "examples/SKILLS.md" {
    model: "minimax-m2.5",
    prompt: "I am a helpful assistant. Apply the skills strictly to solve this issue."
}
```

---

## 👁️ 多模态先锋：全局内置的视觉原语 `img(...)`
从 V0.8 架构开始，Nexa 正式进入了全多模态感知的阶段。你再也不用手写繁琐的 `Base64` 编码转换或者 `multipart/form-data` 解析装配，语言级别的 `img` 类型函数替你搞定一切：

```nexa
agent ResilientVisionAgent {
    model: "minimax-m2.5",
    description: "I test fallback and vision capabilities."
}

flow main {
    // 将指定路径下的静态图像直接转换为受引擎承认的内存多模态张量对象
    img_data = img("docs/img/logo.jpg");
    
    // 就像传入普通字符串一样传给 Agent，底层会自适应匹配 VLM (Vision Language Model) 数据流！
    result = ResilientVisionAgent.run("Inspect this image", img_data);
}
```

Nexa 对于物理世界模块的封装，永远是以降低开发者的心智门槛、坚守系统沙盒安全性为最高原则。这些功能为你搭建自动化王国奠定了最扎实的水电煤基建。
