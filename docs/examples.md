---
comments: true
---

# 完整示例集合

本文档提供一系列完整的、可运行的 Nexa 示例代码，覆盖从基础到企业级的各种应用场景。每个示例都包含完整代码、运行方式和预期输出。

---

## 📋 目录

### 基础示例
- [示例 1：Hello World](#示例-1-hello-world)
- [示例 2：简单对话机器人](#示例-2-简单对话机器人)
- [示例 3：带记忆的聊天助手](#示例-3-带记忆的聊天助手)

### 工具集成示例
- [示例 4：文件处理助手](#示例-4-文件处理助手)
- [示例 5：网页内容抓取](#示例-5-网页内容抓取)
- [示例 6：数据库查询助手](#示例-6-数据库查询助手)

### 多 Agent 协作示例
- [示例 7：翻译流水线](#示例-7-翻译流水线)
- [示例 8：代码审查团队](#示例-8-代码审查团队)
- [示例 9：研究分析师团队](#示例-9-研究分析师团队)

### 高级模式示例
- [示例 10：意图路由客服](#示例-10-意图路由客服)
- [示例 11：批评循环优化](#示例-11-批评循环优化)
- [示例 12：DAG 并行处理](#示例-12-dag-并行处理)
- [示例 13：条件分支处理](#示例-13-条件分支处理)

### 企业级示例
- [示例 14：研报生成系统](#示例-14-研报生成系统)
- [示例 15：智能客服系统](#示例-15-智能客服系统)
- [示例 16：代码生成与测试](#示例-16-代码生成与测试)

### v1.3.x 新特性示例
- [示例 17：契约式编程 (DbC)](#示例-17-契约式编程-dbc)
- [示例 18：错误传播与恢复](#示例-18-错误传播与恢复)
- [示例 19：模式匹配与 ADT](#示例-19-模式匹配与-adt)
- [示例 20：HTTP Server + 数据库](#示例-20-http-server--数据库)
- [示例 21：并发数据处理](#示例-21-并发数据处理)
- [示例 22：后台任务系统](#示例-22-后台任务系统)

---

## 基础示例

### 示例 1：Hello World

**目的**：演示最基本的 Nexa 程序结构。

**完整代码**：

```nexa
// hello_world.nx
// 最简单的 Nexa 程序

agent Greeter {
    role: "友好的问候助手",
    model: "deepseek/deepseek-chat",
    prompt: "你是一个热情的助手。用简洁友好的语言回应每一个问候。"
}

flow main {
    result = Greeter.run("你好，Nexa！");
    print(result);
}
```

**运行方式**：
```bash
nexa run hello_world.nx
```

**预期输出**：
```
你好！欢迎来到 Nexa 的世界！有什么我可以帮助你的吗？😊
```

**代码解析**：
| 行号 | 说明 |
|-----|------|
| 4-8 | 定义一个名为 `Greeter` 的 Agent，设置角色、模型和提示词 |
| 10 | `flow main` 是程序入口，类似于其他语言的 main 函数 |
| 11 | 调用 Agent 的 `run()` 方法，传入用户输入 |
| 12 | 打印结果 |

---

### 示例 2：简单对话机器人

**目的**：演示如何创建一个可以进行多轮对话的聊天机器人。

**完整代码**：

```nexa
// chatbot.nx
// 简单对话机器人

agent ChatBot {
    role: "智能聊天助手",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一个友好、乐于助人的聊天机器人。
    
    规则：
    1. 保持回答简洁明了
    2. 如果不确定，诚实地承认
    3. 对于复杂问题，给出条理清晰的回答
    """,
    memory: "persistent"  // 启用持久化记忆
}

flow main {
    // 第一轮对话
    response1 = ChatBot.run("你好！请介绍一下你自己。");
    print("用户：你好！请介绍一下你自己。");
    print("机器人：" + response1);
    print("");
    
    // 第二轮对话（Agent 会记住上下文）
    response2 = ChatBot.run("我刚才问了你什么？");
    print("用户：我刚才问了你什么？");
    print("机器人：" + response2);
}
```

**运行方式**：
```bash
nexa run chatbot.nx
```

**预期输出**：
```
用户：你好！请介绍一下你自己。
机器人：你好！我是一个智能聊天助手，可以帮助你回答问题、提供建议和进行友好对话。有什么我可以帮你的吗？

用户：我刚才问了你什么？
机器人：你刚才让我介绍一下我自己。我已经回答了，我是一个智能聊天助手。
```

**关键点**：
- `memory: "persistent"` 使 Agent 能够记住对话历史
- 后续调用 `run()` 时，Agent 可以访问之前的对话上下文

---

### 示例 3：带记忆的聊天助手

**目的**：演示如何配置 Agent 的长期记忆功能。

**完整代码**：

```nexa
// memory_assistant.nx
// 带长期记忆的助手

agent SmartAssistant {
    role: "个人智能助手",
    model: "deepseek/deepseek-chat",
    prompt: "你是一个能记住用户偏好的智能助手。",
    memory: "persistent",
    experience: "assistant_memory.md",  // 加载长期记忆
    cache: true  // 启用缓存提高响应速度
}

flow main {
    // 首次交互，告诉助手用户偏好
    SmartAssistant.run("我喜欢科幻小说，特别是刘慈欣的作品。");
    
    // 后续交互，助手应该记住偏好
    result = SmartAssistant.run("给我推荐一本书。");
    print(result);
}
```

**记忆文件示例** (`assistant_memory.md`)：
```markdown
# 用户偏好记忆

## 阅读偏好
- 喜欢科幻小说
- 偏好作者：刘慈欣

## 其他偏好
- （助手会自动更新此文件）
```

---

## 工具集成示例

### 示例 4：文件处理助手

**目的**：演示如何使用标准库工具处理文件。

**完整代码**：

```nexa
// file_assistant.nx
// 文件处理助手

agent FileAssistant uses std.fs, std.time {
    role: "文件管理助手",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一个文件管理助手。你可以：
    - 读取文件内容
    - 创建新文件
    - 获取当前时间
    
    根据用户需求，选择合适的工具完成任务。
    """
}

flow main {
    task = """
    请执行以下操作：
    1. 获取当前时间
    2. 创建一个名为 'note.txt' 的文件
    3. 写入内容：当前时间和一条问候语
    """;
    
    result = FileAssistant.run(task);
    print(result);
}
```

**运行方式**：
```bash
nexa run file_assistant.nx
```

**预期输出**：
```
已完成以下操作：
1. 当前时间：2024-01-15 10:30:00
2. 已创建文件 note.txt
3. 已写入内容："2024-01-15 10:30:00 - 你好，这是一个自动生成的便签！"
```

---

### 示例 5：网页内容抓取

**目的**：演示如何使用 HTTP 工具抓取网页内容。

**完整代码**：

```nexa
// web_scraper.nx
// 网页内容抓取

agent WebScraper uses std.http, std.fs {
    role: "网页抓取助手",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一个网页内容抓取助手。
    
    你的任务是：
    1. 使用 http 工具获取网页内容
    2. 提取关键信息（如标题、正文摘要）
    3. 可选：保存到本地文件
    """
}

agent Summarizer {
    role: "内容总结专家",
    model: "deepseek/deepseek-chat",
    prompt: "将抓取的网页内容总结为 3-5 个要点。"
}

flow main {
    url = "https://example.com";
    
    // 管道：抓取 -> 总结
    summary = url >> WebScraper >> Summarizer;
    
    print("网页摘要：");
    print(summary);
}
```

**预期输出**：
```
网页摘要：
1. 这是示例网站的首页
2. 主要提供产品和服务介绍
3. 包含联系方式和关于我们页面
4. 网站设计简洁现代
```

---

### 示例 6：数据库查询助手

**目的**：演示如何创建能与数据库交互的 Agent。

**完整代码**：

```nexa
// db_assistant.nx
// 数据库查询助手

// 自定义数据库工具
tool DatabaseQuery {
    description: "执行 SQL 查询并返回结果",
    parameters: {
        "query": "string  // SQL 查询语句"
    }
}

agent DBAssistant uses DatabaseQuery {
    role: "数据库助手",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一个数据库查询助手。
    
    根据用户的自然语言需求：
    1. 理解用户意图
    2. 生成合适的 SQL 查询
    3. 使用 DatabaseQuery 工具执行
    4. 用自然语言解释结果
    
    注意：只执行 SELECT 查询，不要执行修改操作。
    """
}

flow main {
    question = "显示最近 10 条订单记录";
    result = DBAssistant.run(question);
    print(result);
}
```

---

## 多 Agent 协作示例

### 示例 7：翻译流水线

**目的**：演示多个 Agent 串联处理数据。

**完整代码**：

```nexa
// translation_pipeline.nx
// 英文 -> 中文翻译流水线

// 第一阶段：翻译
agent Translator {
    role: "专业翻译",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一位专业的英译中翻译。
    
    要求：
    - 准确传达原文含义
    - 使用地道流畅的中文
    - 保留原文的专业术语
    """
}

// 第二阶段：校对
agent Proofreader {
    role: "校对编辑",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一位资深的中文校对编辑。
    
    检查并修正：
    - 语法错误
    - 表达不通顺的地方
    - 标点符号使用
    
    如果译文已经很好，直接返回原文。
    """
}

// 第三阶段：润色
agent Polisher {
    role: "文字润色专家",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一位文字润色专家。
    
    提升：
    - 文字的优美程度
    - 阅读的流畅性
    - 适当增加文学色彩
    """
}

flow main {
    english_text = """
    Artificial intelligence is not just a technology, 
    but a fundamental shift in how we interact with machines 
    and how machines interact with the world.
    """;
    
    // 三阶段流水线
    final_translation = english_text >> Translator >> Proofreader >> Polisher;
    
    print("原文：");
    print(english_text);
    print("\n译文：");
    print(final_translation);
}
```

**预期输出**：
```
原文：
Artificial intelligence is not just a technology, 
but a fundamental shift in how we interact with machines 
and how machines interact with the world.

译文：
人工智能不仅是一项技术，更是我们与机器交互方式、以及机器与世界交互方式的一场根本性变革。
```

---

### 示例 8：代码审查团队

**目的**：演示专业分工的多 Agent 协作。

**完整代码**：

```nexa
// code_review_team.nx
// 代码审查团队

// 定义输出协议
protocol CodeReviewReport {
    code_quality: "string",      // 代码质量评级 (A/B/C/D/F)
    issues: "list[string]",      // 发现的问题列表
    suggestions: "list[string]", // 改进建议
    overall_comment: "string"    // 总体评价
}

// 代码质量审查员
agent QualityReviewer implements CodeReviewReport {
    role: "代码质量审查员",
    model: "deepseek/deepseek-chat",
    prompt: """
    审查代码质量，关注：
    - 代码结构
    - 命名规范
    - 可读性
    - 潜在 bug
    """
}

// 安全审查员
agent SecurityReviewer {
    role: "安全审查员",
    model: "deepseek/deepseek-chat",
    prompt: """
    审查代码安全性，关注：
    - SQL 注入风险
    - XSS 漏洞
    - 敏感信息泄露
    - 权限控制问题
    """
}

// 综合报告员
agent ReportCompiler {
    role: "报告整合员",
    model: "deepseek/deepseek-chat",
    prompt: """
    整合多位审查员的意见，生成综合报告。
    格式清晰，重点突出。
    """
}

flow main {
    code_to_review = """
    def get_user(user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return db.execute(query)
    """;
    
    // 并行审查后整合
    final_report = code_to_review 
        |>> [QualityReviewer, SecurityReviewer] 
        &>> ReportCompiler;
    
    print("=== 代码审查报告 ===");
    print(final_report);
}
```

**预期输出**：
```
=== 代码审查报告 ===

【代码质量】评级：C
- 问题：缺少输入验证、没有异常处理
- 建议：添加参数类型检查

【安全问题】高危
- SQL 注入漏洞：直接拼接用户输入
- 建议：使用参数化查询

【改进建议】
1. 使用参数化查询防止 SQL 注入
2. 添加 try-except 异常处理
3. 添加类型注解提高可读性
```

---

### 示例 9：研究分析师团队

**目的**：演示 DAG 并行处理在研究分析中的应用。

**完整代码**：

```nexa
// research_team.nx
// 研究分析师团队

// 行业研究员
agent TechResearcher {
    role: "科技行业研究员",
    model: "deepseek/deepseek-chat",
    prompt: "分析科技行业的最新趋势和关键技术。"
}

agent FinanceResearcher {
    role: "金融行业研究员",
    model: "deepseek/deepseek-chat",
    prompt: "分析金融行业的市场动态和投资机会。"
}

agent HealthcareResearcher {
    role: "医疗健康研究员",
    model: "deepseek/deepseek-chat",
    prompt: "分析医疗健康行业的创新和监管动态。"
}

// 综合分析师
agent ChiefAnalyst {
    role: "首席分析师",
    model: "deepseek/deepseek-chat",
    prompt: """
    整合各行业研究员的分析报告，
    找出跨行业的共同趋势和投资机会。
    """
}

// 报告撰写员
agent ReportWriter {
    role: "报告撰写员",
    model: "deepseek/deepseek-chat",
    prompt: "将分析内容整理为专业的研究报告格式。"
}

flow main {
    topic = "2024年投资机会分析";
    
    // 并行研究 -> 整合 -> 撰写
    final_report = topic 
        |>> [TechResearcher, FinanceResearcher, HealthcareResearcher]
        &>> ChiefAnalyst 
        >> ReportWriter;
    
    print("=== 研究报告 ===");
    print(final_report);
}
```

**流程图**：
```
         ┌─────────────────┐
         │    输入主题      │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌───────┐   ┌───────┐   ┌──────────┐
│ Tech  │   │Finance│   │Healthcare│
│Research│   │Research│   │ Research │
└───┬───┘   └───┬───┘   └────┬─────┘
    │           │            │
    └─────────┬─┴────────────┘
              │
              ▼
        ┌───────────┐
        │  Chief    │
        │ Analyst   │
        └─────┬─────┘
              │
              ▼
        ┌───────────┐
        │  Report   │
        │  Writer   │
        └───────────┘
```

---

## 高级模式示例

### 示例 10：意图路由客服

**目的**：演示使用 `match intent` 实现智能客服路由。

**完整代码**：

```nexa
// customer_service.nx
// 智能客服路由系统

// 意图分类后的专业 Agent
agent OrderBot {
    role: "订单服务专员",
    model: "deepseek/deepseek-chat",
    prompt: "处理订单查询、修改、取消等请求。"
}

agent RefundBot {
    role: "退款服务专员",
    model: "deepseek/deepseek-chat",
    prompt: "处理退款申请、进度查询等请求。"
}

agent ProductBot {
    role: "产品咨询专员",
    model: "deepseek/deepseek-chat",
    prompt: "回答产品功能、规格、对比等咨询。"
}

agent TechBot {
    role: "技术支持专员",
    model: "deepseek/deepseek-chat",
    prompt: "解决技术问题、故障排查、使用指导。"
}

agent GeneralBot {
    role: "通用客服",
    model: "deepseek/deepseek-chat",
    prompt: "处理一般性问题和问候，无法处理时引导用户。"
}

flow main {
    user_message = "我的订单 #12345 为什么还没发货？";
    
    response = match user_message {
        intent("订单查询或修改") => OrderBot.run(user_message),
        intent("退款申请或查询") => RefundBot.run(user_message),
        intent("产品咨询") => ProductBot.run(user_message),
        intent("技术支持") => TechBot.run(user_message),
        _ => GeneralBot.run(user_message)
    };
    
    print("客服回复：" + response);
}
```

**测试用例**：
| 用户输入 | 路由到 | 说明 |
|---------|-------|------|
| "我的订单 #12345 为什么还没发货？" | OrderBot | 订单相关 |
| "我要退款，商品有质量问题" | RefundBot | 退款相关 |
| "这款手机支持 5G 吗？" | ProductBot | 产品咨询 |
| "App 打不开怎么办？" | TechBot | 技术支持 |
| "你好" | GeneralBot | 默认处理 |

---

### 示例 11：批评循环优化

**目的**：演示使用 `loop until` 实现 Agent 自我优化。

**完整代码**：

```nexa
// critic_loop.nx
// 批评循环优化系统

agent Writer {
    role: "内容创作者",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一位专业的内容创作者。
    
    根据反馈修改你的文章，每次修改都要：
    1. 认真考虑反馈意见
    2. 保持文章的整体风格
    3. 逐步提升质量
    """
}

agent Critic {
    role: "内容评论家",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是一位严格的评论家。
    
    审查文章并提出具体的改进意见：
    - 内容完整性
    - 逻辑连贯性
    - 语言表达
    - 格式规范
    
    如果文章已经足够好，回复"通过"。
    """
}

flow main {
    topic = "写一篇关于人工智能未来发展的短文（200字以内）";
    
    // 初始草稿
    draft = Writer.run(topic);
    
    loop {
        // 获取批评意见
        feedback = Critic.run(draft);
        
        // 如果通过，退出循环
        if ("通过" in feedback) {
            break;
        }
        
        // 根据反馈修改
        draft = Writer.run(f"根据以下反馈修改文章：\n{feedback}\n\n原文：\n{draft}");
        
    } until ("文章质量优秀，评论家表示通过" or runtime.meta.loop_count >= 3);
    
    print("=== 最终文章 ===");
    print(draft);
    
    if (runtime.meta.loop_count >= 3) {
        print("\n（已达到最大修改次数）");
    }
}
```

**运行流程**：
```
第1轮：Writer 产出初稿 -> Critic 指出问题
第2轮：Writer 修改 -> Critic 仍有意见
第3轮：Writer 再次修改 -> Critic 通过
输出最终文章
```

---

### 示例 12：DAG 并行处理

**目的**：演示 Nexa v0.9.7 引入的 DAG 操作符。

**完整代码**：

```nexa
// dag_parallel.nx
// DAG 并行处理示例

// 分叉操作符 |>> 示例
agent TranslatorCN {
    model: "deepseek/deepseek-chat",
    prompt: "翻译成中文"
}

agent TranslatorEN {
    model: "deepseek/deepseek-chat",
    prompt: "翻译成英文"
}

agent TranslatorJP {
    model: "deepseek/deepseek-chat",
    prompt: "翻译成日语"
}

// 合流操作符 &>> 示例
agent Merger {
    model: "deepseek/deepseek-chat",
    prompt: "整合多个翻译版本，输出对照表"
}

// 条件分支操作符 ?? 示例
agent UrgentHandler {
    model: "deepseek/deepseek-chat",
    prompt: "紧急处理，快速响应"
}

agent NormalHandler {
    model: "deepseek/deepseek-chat",
    prompt: "标准处理，详细分析"
}

flow main {
    input_text = "Hello, World!";
    
    // 示例1：分叉 - 并行翻译成多种语言
    print("=== 多语言翻译 ===");
    translations = input_text |>> [TranslatorCN, TranslatorEN, TranslatorJP];
    print(translations);
    
    // 示例2：合流 - 整合多个结果
    print("\n=== 翻译对照表 ===");
    comparison = [TranslatorCN, TranslatorJP] &>> Merger;
    print(comparison);
    
    // 示例3：条件分支 - 根据内容选择处理方式
    print("\n=== 智能路由 ===");
    urgent_input = "URGENT: 系统崩溃！";
    normal_input = "请帮我分析一下销售数据";
    
    urgent_result = urgent_input ?? UrgentHandler : NormalHandler;
    normal_result = normal_input ?? UrgentHandler : NormalHandler;
    
    print("紧急处理结果：" + urgent_result);
    print("标准处理结果：" + normal_result);
    
    // 示例4：复杂 DAG 组合
    print("\n=== 复杂 DAG ===");
    complex_result = input_text 
        |>> [TranslatorCN, TranslatorJP] 
        &>> Merger;
    print(complex_result);
}
```

**操作符说明**：

| 操作符 | 名称 | 作用 | 示例 |
|-------|------|------|------|
| `>>` | 管道 | 顺序传递 | `A >> B` |
| `|>>` | 分叉 | 并行发送 | `input |>> [A, B, C]` |
| `&>>` | 合流 | 合并结果 | `[A, B] &>> C` |
| `??` | 条件分支 | 条件路由 | `input ?? A : B` |
| `||` | 异步分叉 | 不等待结果 | `input || [A, B]` |
| `&&` | 共识合流 | 需要一致 | `[A, B] && Judge` |

---

### 示例 13：条件分支处理

**目的**：演示 `semantic_if` 语义条件判断。

**完整代码**：

```nexa
// semantic_condition.nx
// 语义条件判断示例

agent DataAnalyzer {
    model: "deepseek/deepseek-chat",
    prompt: "分析用户输入的数据类型和内容"
}

agent JSONProcessor {
    model: "deepseek/deepseek-chat",
    prompt: "处理 JSON 格式的数据"
}

agent TextProcessor {
    model: "deepseek/deepseek-chat",
    prompt: "处理普通文本数据"
}

flow main {
    user_input = '{"name": "张三", "age": 25, "city": "北京"}';
    
    // 语义条件判断 - 判断是否为 JSON
    semantic_if "输入内容是有效的 JSON 格式" fast_match r"^\s*[\[{]" against user_input {
        result = JSONProcessor.run(user_input);
        print("作为 JSON 处理：" + result);
    } else {
        result = TextProcessor.run(user_input);
        print("作为文本处理：" + result);
    }
    
    // 另一个示例：日期检测
    date_input = "会议定于 2024-03-15 举行";
    
    semantic_if "包含具体日期" fast_match r"\d{4}-\d{2}-\d{2}" against date_input {
        print("检测到日期信息，可以创建日程");
    } else {
        print("未检测到日期信息");
    }
}
```

**`fast_match` 说明**：

`fast_match` 是一个正则表达式预过滤器，可以在调用 LLM 之前快速判断：

- 如果正则匹配成功，直接进入分支（节省 Token）
- 如果正则不匹配，仍会调用 LLM 进行语义判断

---

## 企业级示例

### 示例 14：研报生成系统

**目的**：演示完整的企业级研报生成流程。

**完整代码**：

```nexa
// research_report.nx
// 企业研报生成系统

// 输出协议
protocol ResearchReport {
    title: "string",
    executive_summary: "string",
    key_findings: "list[string]",
    recommendations: "list[string]",
    risk_analysis: "string",
    conclusion: "string"
}

// 数据收集员
agent DataCollector uses std.http, std.fs {
    role: "数据收集员",
    model: "deepseek/deepseek-chat",
    prompt: "收集指定主题的相关数据和信息",
    cache: true
}

// 数据分析师
agent DataAnalyst {
    role: "数据分析师",
    model: "deepseek/deepseek-chat",
    prompt: "分析数据，提取关键洞察和趋势"
}

// 行业研究员
agent IndustryResearcher {
    role: "行业研究员",
    model: "deepseek/deepseek-chat",
    prompt: "研究行业背景、竞争格局和发展趋势"
}

// 报告撰写员
agent ReportWriter implements ResearchReport {
    role: "报告撰写员",
    model: "deepseek/deepseek-chat",
    prompt: """
    撰写专业的研究报告，包含：
    - 标题
    - 执行摘要
    - 关键发现
    - 建议
    - 风险分析
    - 结论
    """
}

// 质量审核员
agent QualityReviewer {
    role: "质量审核员",
    model: "deepseek/deepseek-chat",
    prompt: "审核报告质量，确保专业性和完整性"
}

flow main {
    topic = "中国新能源汽车市场 2024 年度分析";
    
    // 并行收集和分析
    research_data = topic |>> [DataCollector, IndustryResearcher];
    
    // 分析数据
    analysis = research_data &>> DataAnalyst;
    
    // 撰写报告
    draft_report = analysis >> ReportWriter;
    
    // 质量审核（循环优化）
    loop {
        review = QualityReviewer.run(draft_report);
    } until ("报告质量合格" or runtime.meta.loop_count >= 2);
    
    print("=== 研究报告 ===");
    print(draft_report);
}
```

---

### 示例 15：智能客服系统

**目的**：演示完整的智能客服系统。

**完整代码**：

```nexa
// smart_customer_service.nx
// 智能客服系统

// 用户信息协议
protocol UserInfo {
    user_id: "string",
    name: "string",
    membership_level: "string",
    recent_orders: "list[string]"
}

// 意图识别
agent IntentClassifier {
    role: "意图识别器",
    model: "deepseek/deepseek-chat",  // 使用快速模型
    prompt: "识别用户意图，返回意图类型"
}

// 订单查询
agent OrderQuery uses std.fs {
    role: "订单查询专员",
    model: "deepseek/deepseek-chat",
    prompt: "查询订单状态和物流信息"
}

// 售后服务
agent AfterSalesService {
    role: "售后服务专员",
    model: "deepseek/deepseek-chat",
    prompt: "处理退换货、维修等售后问题"
}

// 投诉处理
agent ComplaintHandler uses std.ask_human {
    role: "投诉处理专员",
    model: "deepseek/deepseek-chat",
    prompt: "处理客户投诉，必要时请示人工"
}

// 知识库问答
agent KnowledgeBaseQA {
    role: "知识库问答",
    model: "deepseek/deepseek-chat",
    prompt: "基于知识库回答产品相关问题",
    experience: "product_knowledge.md"
}

// 人工转接判断
agent HumanHandoff {
    role: "人工转接判断",
    model: "deepseek/deepseek-chat",
    prompt: "判断是否需要转接人工客服"
}

flow main {
    user_message = "我上周买的手机有问题，想退货";
    
    // 1. 意图识别
    intent = IntentClassifier.run(user_message);
    
    // 2. 路由到对应专员
    response = match intent {
        intent("订单查询") => OrderQuery.run(user_message),
        intent("售后服务") => AfterSalesService.run(user_message),
        intent("投诉建议") => ComplaintHandler.run(user_message),
        intent("产品咨询") => KnowledgeBaseQA.run(user_message),
        _ => KnowledgeBaseQA.run(user_message)
    };
    
    // 3. 判断是否需要人工介入
    need_human = HumanHandoff.run(response);
    
    if ("需要人工" in need_human) {
        std.ask_human.call("复杂问题，请人工介入：" + user_message);
    }
    
    print("客服回复：" + response);
}
```

---

### 示例 16：代码生成与测试

**目的**：演示代码生成、测试、修复的完整流程。

**完整代码**：

```nexa
// code_gen_test.nx
// 代码生成与自动测试

// 输出协议
protocol GeneratedCode {
    code: "string",
    language: "string",
    description: "string",
    test_cases: "list[string]"
}

// 代码生成器
agent CodeGenerator implements GeneratedCode {
    role: "代码生成专家",
    model: "deepseek/deepseek-chat",
    prompt: """
    生成高质量代码，要求：
    - 代码清晰、有注释
    - 遵循最佳实践
    - 包含边界处理
    """
}

// 测试生成器
agent TestGenerator {
    role: "测试工程师",
    model: "deepseek/deepseek-chat",
    prompt: "为代码生成单元测试"
}

// 代码审查员
agent CodeReviewer {
    role: "代码审查员",
    model: "deepseek/deepseek-chat",
    prompt: "审查代码质量，发现问题"
}

// 修复工程师
agent BugFixer {
    role: "Bug修复工程师",
    model: "deepseek/deepseek-chat",
    prompt: "根据审查意见修复代码问题"
}

flow main {
    requirement = "实现一个 Python 函数，计算斐波那契数列的第 n 项";
    
    // 1. 生成代码
    initial_code = CodeGenerator.run(requirement);
    print("=== 初始代码 ===");
    print(initial_code.code);
    
    // 2. 生成测试
    tests = TestGenerator.run(initial_code.code);
    print("\n=== 测试用例 ===");
    print(tests);
    
    // 3. 审查与修复循环
    loop {
        review = CodeReviewer.run(initial_code.code);
        
        if ("通过" in review or "无问题" in review) {
            break;
        }
        
        initial_code = BugFixer.run(f"问题：{review}\n代码：{initial_code.code}");
        
    } until ("代码通过审查" or runtime.meta.loop_count >= 3);
    
    print("\n=== 最终代码 ===");
    print(initial_code.code);
}
```

---

## v1.3.x 新特性示例

### 示例 17：契约式编程 (DbC)

**目的**：演示 requires/ensures/invariant 契约的使用，以及 ContractViolation 与 HTTP 的集成。

**完整代码**：

```nexa
// contract_demo.nx
// 契约式编程示例

agent DataProcessor {
    role: "数据处理专家"
    model: "deepseek/deepseek-chat"
    prompt: "处理输入数据并返回结构化结果"
    requires: "input must be non-empty and contain valid data"
    ensures: "output contains processed summary"
}

agent QualityChecker {
    role: "质量检查员"
    model: "deepseek/deepseek-chat"
    prompt: "检查数据质量"
    requires: "data must be formatted as JSON"
    ensures: "quality_score is between 0 and 100"
}

flow main {
    // ✅ 正常调用 — 满足 requires 条件
    raw_data = '{"items": [1, 2, 3], "status": "active"}'
    result = DataProcessor.run(raw_data)
    print("处理结果: " + result)

    // ✅ 使用 otherwise 处理契约违反
    empty_data = ""
    safe_result = DataProcessor.run(empty_data) otherwise "默认结果"
    print("安全结果: " + safe_result)

    // ✅ 契约链 — 多个 Agent 的契约依次验证
    processed = DataProcessor.run(raw_data)
    quality = QualityChecker.run(processed) otherwise "质量未知"
    print("质量评分: " + quality)
}
```

**运行方式**：
```bash
nexa run contract_demo.nx
```

**代码解析**：
| 行号 | 说明 |
|-----|------|
| 7-8 | `requires` 定义前置条件，调用前必须满足 |
| 9 | `ensures` 定义后置条件，输出必须满足 |
| 20 | `otherwise` 在契约违反时提供降级结果 |
| 23-24 | 契约链：多个 Agent 的契约依次验证 |

---

### 示例 18：错误传播与恢复

**目的**：演示 `?` 错误传播操作符和 `otherwise` 错误恢复操作符的使用。

**完整代码**：

```nexa
// error_propagation_demo.nx
// 错误传播与恢复示例

agent Fetcher {
    role: "数据获取器"
    model: "deepseek/deepseek-chat"
    prompt: "从指定来源获取数据"
}

agent Parser {
    role: "数据解析器"
    model: "deepseek/deepseek-chat"
    prompt: "解析原始数据为结构化格式"
}

agent Analyzer {
    role: "数据分析器"
    model: "deepseek/deepseek-chat"
    prompt: "分析数据并生成洞察"
}

flow main {
    // ✅ 使用 ? 传播错误 — 任何步骤失败则整个链失败
    result = Fetcher.run("source_url")
        |> Parser.run?
        |> Analyzer.run?

    // ✅ 使用 otherwise 在每步提供降级
    safe_result = Fetcher.run("source_url") otherwise "无数据"
        |> Parser.run? otherwise "解析失败"
        |> Analyzer.run? otherwise "分析不可用"

    print("安全结果: " + safe_result)

    // ✅ 组合使用 ? 和 otherwise
    data = Fetcher.run("source_url")?
    if data != None {
        parsed = Parser.run(data) otherwise "原始数据: " + data
        print("解析结果: " + parsed)
    } otherwise {
        print("数据获取失败，使用缓存")
        cached = std.kv.get("cache_key") ?? "默认缓存数据"
        print("缓存数据: " + cached)
    }
}
```

**运行方式**：
```bash
nexa run error_propagation_demo.nx
```

**代码解析**：
| 行号 | 说明 |
|-----|------|
| 19-21 | `?` 操作符：错误自动向上传播，链中任一步失败则整链失败 |
| 24-26 | `otherwise` 操作符：每步提供降级值，确保链不中断 |
| 30-37 | `?` 与 `otherwise` 组合使用，配合 `??` 空值合并 |

---

### 示例 19：模式匹配与 ADT

**目的**：演示 struct/enum/trait 代数数据类型与模式匹配的组合使用。

**完整代码**：

```nexa
// pattern_adt_demo.nx
// 模式匹配与 ADT 示例

// 定义结构体
struct User {
    name: string
    age: int
    email: string
}

// 定义枚举
enum Status {
    Active
    Inactive
    Suspended(reason: string)
}

// 定义特质
trait Displayable {
    fn display(self) -> string
}

impl Displayable for User {
    fn display(self) -> string {
        "#{self.name} (#{self.age}) — #{self.email}"
    }
}

flow main {
    // 创建 struct 实例
    user = User{name: "Alice", age: 30, email: "alice@example.com"}

    // 创建 enum variant
    status = Status.Active
    suspended = Status.Suspended{reason: "违规操作"}

    // ✅ 模式匹配
    match status {
        Status.Active -> print("用户活跃")
        Status.Inactive -> print("用户未激活")
        Status.Suspended{reason} -> print("用户被暂停: " + reason)
    }

    // ✅ Let 解构
    let User{name, age} = user
    print("姓名: " + name + ", 年龄: " + age)

    // ✅ Trait 方法调用
    display_text = user.display()
    print("展示: " + display_text)

    // ✅ For 解构
    users = [User{name: "Bob", age: 25, email: "bob@test.com"},
             User{name: "Carol", age: 28, email: "carol@test.com"}]
    for let User{name, age} in users {
        print("#{name}: #{age}岁")
    }
}
```

**运行方式**：
```bash
nexa run pattern_adt_demo.nx
```

**代码解析**：
| 行号 | 说明 |
|-----|------|
| 6-10 | `struct` 定义数据结构，字段有类型标注 |
| 13-17 | `enum` 定义枚举，支持带数据的 variant |
| 20-22 | `trait` 定义行为接口 |
| 24-27 | `impl` 为具体类型实现 trait 方法 |
| 32-36 | `match` 模式匹配，按 variant 分支处理 |
| 39 | `let` 解构提取 struct 字段 |
| 42 | Trait 方法调用 |
| 45-48 | `for let` 解构遍历集合 |

---

### 示例 20：HTTP Server + 数据库

**目的**：演示 HTTP Server 与数据库的集成使用，构建一个完整的 API 服务。

**完整代码**：

```nexa
// http_db_demo.nx
// HTTP Server + 数据库集成示例

db AppDB {
    type: "sqlite"
    path: ":memory:"
}

agent ItemHandler {
    role: "物品管理助手"
    model: "deepseek/deepseek-chat"
    prompt: "处理物品相关的请求"
    requires: "request must contain valid item data"
    ensures: "response contains item details"
}

server ItemAPI {
    route "/api/items": ItemHandler
    route "/api/items/search": ItemHandler
}

flow main {
    // 初始化数据库
    db_handle = std.db.sqlite.connect(":memory:")
    std.db.sqlite.execute(db_handle, "CREATE TABLE items (id INT, name TEXT, price FLOAT)")
    std.db.sqlite.execute(db_handle, "INSERT INTO items VALUES (1, 'Widget', 9.99)")
    std.db.sqlite.execute(db_handle, "INSERT INTO items VALUES (2, 'Gadget', 19.99)")

    // 查询数据
    items = std.db.sqlite.query(db_handle, "SELECT * FROM items")
    print("数据库中的物品: " + items)

    // 启动 HTTP Server
    // nexa serve http_db_demo.nx --port 8080
    // 契约违反自动映射: requires → 401, ensures → 403

    std.db.sqlite.close(db_handle)
}
```

**运行方式**：
```bash
# 先编译
nexa build http_db_demo.nx

# 启动 HTTP Server
nexa serve http_db_demo.nx --port 8080

# 查看路由
nexa routes http_db_demo.nx
```

**代码解析**：
| 行号 | 说明 |
|-----|------|
| 6-9 | `db` 声明数据库配置 |
| 17-20 | `server` 声明 HTTP 路由 |
| 24-28 | SQLite 初始化：建表、插入数据 |
| 30 | 查询数据 |
| 33 | 契约违反自动映射为 HTTP 状态码 |

---

### 示例 21：并发数据处理

**目的**：演示结构化并发、Channel 和 race 的使用。

**完整代码**：

```nexa
// concurrent_demo.nx
// 并发数据处理示例

agent FastSource {
    role: "快速数据源"
    model: "deepseek/deepseek-chat"
    prompt: "快速返回数据"
}

agent SlowSource {
    role: "慢速数据源"
    model: "deepseek/deepseek-chat"
    prompt: "返回数据但可能较慢"
}

agent Aggregator {
    role: "数据聚合器"
    model: "deepseek/deepseek-chat"
    prompt: "聚合多个来源的数据"
}

flow main {
    // ✅ race — 多源竞争，取最快结果
    result = std.concurrent.race([
        FastSource.run("query1"),
        SlowSource.run("query2")
    ])
    print("最快结果: " + result)

    // ✅ Channel — 生产者-消费者模式
    ch = std.concurrent.channel(10)

    // 发送数据到 Channel
    std.concurrent.ch_send(ch, "data_item_1")
    std.concurrent.ch_send(ch, "data_item_2")

    // 从 Channel 接收数据
    item1 = std.concurrent.ch_recv(ch) ?? "无数据"
    item2 = std.concurrent.ch_recv(ch) ?? "无数据"
    print("接收: " + item1 + ", " + item2)

    // ✅ spawn — 启动并发任务
    task1 = std.concurrent.spawn(FastSource.run("task_a"))
    task2 = std.concurrent.spawn(SlowSource.run("task_b"))

    // 等待所有任务完成
    results = std.concurrent.join_all([task1, task2])
    print("所有结果: " + results)

    // ✅ |> 管道组合并发结果
    final = results |> Aggregator.run
    print("聚合结果: " + final)
}
```

**运行方式**：
```bash
nexa run concurrent_demo.nx
```

**代码解析**：
| 行号 | 说明 |
|-----|------|
| 23-26 | `race` 多源竞争，取最快返回的结果 |
| 29-38 | `channel` 生产者-消费者模式，`??` 处理空通道 |
| 41-42 | `spawn` 启动并发任务 |
| 45 | `join_all` 等待所有任务完成 |
| 48 | `|>` 管道组合并发结果 |

---

### 示例 22：后台任务系统

**目的**：演示 Job 声明、Worker 启动和任务生命周期管理。

**完整代码**：

```nexa
// job_demo.nx
// 后台任务系统示例

agent EmailSender {
    role: "邮件发送助手"
    model: "deepseek/deepseek-chat"
    prompt: "发送通知邮件"
}

agent ReportGenerator {
    role: "报告生成助手"
    model: "deepseek/deepseek-chat"
    prompt: "生成数据分析报告"
}

job EmailJob {
    agent: EmailSender
    queue: "email_queue"
    retry: 3
    backoff: 60
    timeout: 300
}

job ReportJob {
    agent: ReportGenerator
    queue: "report_queue"
    retry: 2
    backoff: 120
    timeout: 600
}

flow main {
    // ✅ defer — 确保资源清理
    defer {
        print("清理完成")
    }

    // 发送邮件任务
    print("邮件任务已注册")

    // 生成报告任务
    print("报告任务已注册")

    // 使用 KV 存储任务状态
    std.kv.set("email_status", "pending")
    std.kv.set("report_status", "pending")

    // 查询任务状态
    email_status = std.kv.get("email_status") ?? "unknown"
    report_status = std.kv.get("report_status") ?? "unknown"
    print("邮件状态: " + email_status)
    print("报告状态: " + report_status)
}
```

**运行方式**：
```bash
# 编译
nexa build job_demo.nx

# 启动 Worker
nexa workers job_demo.nx --start --queue email_queue,report_queue

# 查看任务状态
nexa jobs job_demo.nx --status

# 查看死信任务
nexa jobs job_demo.nx --dead-letter

# 停止 Worker
nexa workers job_demo.nx --stop
```

**代码解析**：
| 行号 | 说明 |
|-----|------|
| 17-22 | `job` 声明后台任务，配置重试和超时 |
| 24-29 | 多个 Job 声明，不同队列和参数 |
| 33-35 | `defer` 确保函数退出时执行清理 |
| 41-42 | KV 存储跟踪任务状态 |
| 45-46 | `??` 处理 KV 中可能不存在键的情况 |

---

## 示例运行检查清单

在运行这些示例之前，请确保：

- [ ] 已正确安装 Nexa
- [ ] 已配置 `secrets.nxs` 文件，包含所需 API 密钥
- [ ] 网络连接正常（需要访问 LLM API）
- [ ] 对于使用文件系统的示例，确保有相应权限

---

## 贡献示例

如果你有好的 Nexa 示例想要分享，欢迎：

1. 在文档底部留言讨论
2. 提交 Pull Request 到 Nexa 仓库
3. 在社区分享你的使用经验

---

<div align="center">
  <p>💡 更多示例持续更新中，敬请关注！</p>
</div>