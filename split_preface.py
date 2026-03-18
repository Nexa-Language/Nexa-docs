import os

with open('docs/tmp.md', 'r', encoding='utf-8') as f:
    tmp = f.read()

with open('docs/preface.md', 'r', encoding='utf-8') as f:
    preface = f.read()

# Extract from tmp
# tmp.md structure:
# # 人工智能代理与原生面向代理编程：从语言模型演进到Nexa语言的架构重构
# ## 引言
# ## 大型语言模型与人工智能代理的演进纪传
# ## 当前代理编排范式的全景调查与深度局限性分析
# ### 弱代码代理编排范式的困境：以Dify、Coze与n8n为例
# ### 通用编程语言框架的架构债务：以LangGraph与AutoGen为例
# ## Nexa：重塑底层的原生面向代理编程语言
# ### 原生平权...
# ...
# ## 典型应用场景与多维度对比分析
# ...
# ## 结语

def extract_section(text, start_heading, end_heading=None):
    lines = text.split('\n')
    started = False
    extracted = []
    
    for line in lines:
        if line.startswith(start_heading):
            started = True
            
        if started and end_heading and line.startswith(end_heading):
            break
            
        if started:
            extracted.append(line)
            
    return '\n'.join(extracted)

tmp_intro = extract_section(tmp, "## 引言", "## 大型语言模型")
tmp_evolution = extract_section(tmp, "## 大型语言模型", "## 当前代理编排范式")
tmp_current = extract_section(tmp, "## 当前代理编排范式", "## Nexa：重塑底层")
tmp_nexa = extract_section(tmp, "## Nexa：重塑底层", "## 典型应用场景")

tmp_scenarios = extract_section(tmp, "## 典型应用场景", "## 结语")
tmp_conclusion = extract_section(tmp, "## 结语")

# Extract from preface
pref_summary = """
### 1. 将 Agent（智能体）作为一级公民 (First-Class Concept)
在传统语言中，“数字”、“字符串”、“函数”是一级公民；面向对象语言中，“类 (Class)”和“对象”是一级公民。而在 Nexa 中，能够“思考验证”的 Agent 本身就是一等公民。如同函数式编程，你可以将其任意组合、传递甚至高阶调用。

你不再需要去实例那些庞大的跨库模块，只需要用极简的 `agent` 关键字即可创建一个实体的认知单元。

```nexa
// 所有的提示词、角色定义、模型引擎甚至退化逻辑全在同一个原生语义块中完成
agent PythonExpert {
    role: "Senior Backend Developer"
    prompt: "You write memory-efficient, mathematically sound Python code."
}
```
**意义**：这种封装将“人设”与“算力分配”进行了完美的大一统隔离，开发者只需要阅读这个 Block，立马就能掌握该 Agent 的职责范围。

### 2. 拥抱强约与静态检查 (Protocol & Types)
Python 作为动态类型语言的“松散”结构，加上大语言模型本身输出的“不确定性”，一旦相遇便是灾难性的组合。Nexa 在语言底层彻底打通了强类型协议（Protocol）。这种设计将大模型的幻觉拒之门外：

- 当你声明了某个 Agent `implements` (实现) 某个 Protocol 之后，底层运行时引擎将立刻拦截到模型返回的 Raw Token。
- **自动反思纠偏引擎 (Auto-Correction Evaluator)**：即便模型输出了并非格式要求的字符，Nexa 也不再需要你写丑陋的 `try-except` 或报错。它在编译期就已织入了一层隐式的拦截网。格式错误将触发内部微循环，将带红线的错语反馈给模型，强迫其修正至绝对契合的 Protocol 为止。这也是只有“自研语言”才能做到的底层深度干预。

### 3. 用声明式图结构代替过程式的死板轮询 (Declarative Flows)
我们观察到开发者在使用传统流控制执行 Agent Orchestration 时极度折磨，于是决定将复杂的协作直接下沉为语法操作符：

- **流水线数据总线 (`>>`)**：以类似 Unix 的完美流感传递信息，隐式保留上下文连贯性。
- **意图分支调度 (`match ... intent()`)**：语言级的模型轻量化判别钩子。
- **并发状态汇聚 (`join`)**：语言级的多核 Map-Reduce 并行操作。

这些直接写在纸面上的声明操作，能够让 Nexa 编译器在运行前智能地构建出庞大的有向无环图 (DAG)，自动处理那些在 Python 里让你焦头烂额的并行任务池和阻塞等待（Promise Resuming）问题。
"""

pref_closing = extract_section(preface, "## 🎯 总结与寄语")

doc1 = f"""---
comments: true
---

# 调研背景：从语言模型到 Agent 原生计算范式

{tmp_intro}

{tmp_evolution}

{tmp_current}

{tmp_nexa}

{pref_summary}
"""

doc2 = f"""---
comments: true
---

# 典型场景：Nexa 与现有编排方法的深度对比

{tmp_scenarios}

{tmp_conclusion}

{pref_closing}
"""

with open('docs/preface_background.md', 'w', encoding='utf-8') as f:
    f.write(doc1)
    
with open('docs/preface_scenarios.md', 'w', encoding='utf-8') as f:
    f.write(doc2)

# Update preface.md to link to them or be concise
new_preface = """---
comments: true
---

# 1. 前言：重构智能体开发范式

在深入 Nexa 的核心语法之前，让我们退一步思考：当前业界在开发以大语言模型（LLM）为核心的智能体（Agent）系统时，究竟面临着怎样的结构性困境？Nexa 是如何基于编译器理论与语言设计学脱颖而出，实现从“应用层框架”到“底层原语”的降维打击的？

*本前言部分被划分为两个核心深度长文，我们强烈建议您在了解核心语法前阅读它们，以理解 Nexa 的设计初衷：*

- 📖 **[调研背景：从语言模型到 Agent 原生计算范式](preface_background.md)**：全面梳理大语言模型与 Agent 的演进，深度剖析 Dify / Coze（弱代码范式）与 Python / LangChain（通用编程语言范式）所面临的底层工程痛点，并阐述 Nexa 如何作为“范式三”重塑原生原语。
- ⚔️ **[典型场景：Nexa 与现有编排方法的深度对比](preface_scenarios.md)**：通过复杂代码生成、长周期金融研报生成以及需要“人在回路（HITL）”的高风险 IT 运维等三大典型场景，实战化对比 Nexa 与其他框架的降维打击优势。

准备好用极富未来感的语言去支配硅基大脑了吗？请点击阅读文献或进入下一章，一起来定义属于你的第一个真正智能的网络团队。
"""

with open('docs/preface.md', 'w', encoding='utf-8') as f:
    f.write(new_preface)

