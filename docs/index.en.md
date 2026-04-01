---
comments: true
---

<div class="portal-hero" style="margin-top: 2rem;">
  <p class="portal-kicker">Agent-Native · Concurrent DAG · LLM</p>
  <h1>Empowering the New Era of Agent-Native Programming</h1>
  <p class="portal-lead">
    Say goodbye to verbose glue code, complex prompt concatenation, and fragile JSON parsing. Nexa elevates intent routing, multi-agent collaboration, and pipeline streaming into core syntax, enabling you to build hardcore LLM concurrency graphs with ultimate elegance.
  </p>
  <div class="portal-actions">
    <a class="md-button md-button--primary" href="en/quickstart/">🚀 Quickstart</a>
    <a class="md-button" href="en/part1_basic/">📖 Basic Syntax</a>
    <a class="md-button" href="en/examples/">💡 Examples</a>
  </div>
</div>

---

## 🔥 Core Advantage: Code Comparison

Nexa simplifies complex multi-agent collaboration into elegant declarative syntax. Click the button below to experience the difference between Nexa and traditional approaches:

---

<span class="example-badge">Example 1</span>
<span class="example-title">Agent Definition & Invocation</span>

<div class="code-comparison">
<div class="flip-card" id="flip-1">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 Traditional Python + LangChain</span>
      <span class="code-lines">12 lines</span>
    </div>
    <div class="card-content">
```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# Define chain
llm = ChatOpenAI(model="gpt-4", temperature=0.7)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional English-Chinese translator"),
    ("human", "{input}")
])
chain = prompt | llm | StrOutputParser()

# Invoke
result = chain.invoke({"input": "Hello, World!"})
print(result)
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">4 lines</span>
    </div>
    <div class="card-content">
```nexa
agent Translator {
    role: "English-Chinese Translator",
    model: "gpt-4"
}

result = Translator.run("Hello, World!")
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-1').classList.toggle('flipped')">
  🔄 Click to compare with Nexa
</button>
<div class="comparison-note">
<strong>Key Advantage:</strong> From 12 lines down to 4, no need to understand Chain, PromptTemplate, StrOutputParser and other complex concepts. Agent definition is configuration, invocation is execution.<span class="reduction-badge">67% reduction</span>
</div>
</div>

---

<span class="example-badge">Example 2</span>
<span class="example-title">Pipeline Orchestration</span>

<div class="code-comparison">
<div class="flip-card" id="flip-2">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 Traditional Python + LangChain</span>
      <span class="code-lines">18 lines</span>
    </div>
    <div class="card-content">
```python
import asyncio
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

async def pipeline(topic: str):
    # Step 1: Writing
    writer_prompt = f"Write an article about {topic}"
    draft = await llm.ainvoke(writer_prompt)
    
    # Step 2: Review
    reviewer_prompt = f"Review and identify issues: {draft.content}"
    review = await llm.ainvoke(reviewer_prompt)
    
    # Step 3: Polish
    editor_prompt = f"Polish based on review: {draft.content}"
    final = await llm.ainvoke(editor_prompt)
    
    return final.content

result = asyncio.run(pipeline("Artificial Intelligence"))
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">5 lines</span>
    </div>
    <div class="card-content">
```nexa
agent Writer { role: "Writer", prompt: "Write articles" }
agent Reviewer { role: "Reviewer", prompt: "Review articles" }
agent Editor { role: "Editor", prompt: "Polish articles" }

flow main {
    result = "Artificial Intelligence" >> Writer >> Reviewer >> Editor;
}
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-2').classList.toggle('flipped')">
  🔄 Click to compare with Nexa
</button>
<div class="comparison-note">
<strong>Key Advantage:</strong> Pipeline operator <code>>></code> makes data flow crystal clear, no need to manually pass intermediate variables or handle async context. The compiler automatically optimizes execution order.<span class="reduction-badge">72% reduction</span>
</div>
</div>

---

<span class="example-badge">Example 3</span>
<span class="example-title">Intent Routing</span>

<div class="code-comparison">
<div class="flip-card" id="flip-3">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 Traditional Python + re</span>
      <span class="code-lines">17 lines</span>
    </div>
    <div class="card-content">
```python
import re
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

def route_request(user_input: str):
    # Hand-written regex - fragile and hard to maintain
    if re.search(r'weather|temperature|forecast', user_input, re.I):
        prompt = f"Answer weather question: {user_input}"
        return llm.invoke(prompt).content
    elif re.search(r'news|headline|latest', user_input, re.I):
        prompt = f"Answer news question: {user_input}"
        return llm.invoke(prompt).content
    elif re.search(r'translate|translation', user_input, re.I):
        prompt = f"Translate: {user_input}"
        return llm.invoke(prompt).content
    else:
        return llm.invoke(f"General chat: {user_input}").content

result = route_request("What's the weather like in Beijing?")
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">10 lines</span>
    </div>
    <div class="card-content">
```nexa
agent WeatherBot { role: "Weather Assistant" }
agent NewsBot { role: "News Assistant" }
agent Translator { role: "Translation Assistant" }
agent ChatBot { role: "Chat Assistant" }

flow main {
    result = match user_input {
        intent("Check weather") => WeatherBot.run(user_input),
        intent("Check news") => NewsBot.run(user_input),
        intent("Translate content") => Translator.run(user_input),
        _ => ChatBot.run(user_input)
    };
}
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-3').classList.toggle('flipped')">
  🔄 Click to compare with Nexa
</button>
<div class="comparison-note">
<strong>Key Advantage:</strong> <code>intent()</code> semantic matching replaces fragile regex expressions, using embedding vectors for semantic similarity matching - smarter and more flexible.<span class="reduction-badge">41% reduction</span>
</div>
</div>

---

<span class="example-badge">Example 4</span>
<span class="example-title">Concurrent DAG Execution</span>

<div class="code-comparison">
<div class="flip-card" id="flip-4">
  <div class="flip-card-front">
    <div class="card-header">
      <span class="card-title">🐍 Traditional Python + asyncio</span>
      <span class="code-lines">23 lines</span>
    </div>
    <div class="card-content">
```python
import asyncio
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

async def researcher(task: str, name: str):
    prompt = f"{name} analysis: {task}"
    return {name: await llm.ainvoke(prompt)}

async def parallel_research(topic: str):
    # Execute 3 researchers in parallel
    tasks = [
        researcher(topic, "Tech Researcher"),
        researcher(topic, "Market Researcher"),
        researcher(topic, "Finance Researcher")
    ]
    results = await asyncio.gather(*tasks)
    
    # Summarize results
    combined = "\n".join([str(r) for r in results])
    summary_prompt = f"Summarize these reports:\n{combined}"
    final = await llm.ainvoke(summary_prompt)
    
    return final.content

result = asyncio.run(parallel_research("AI Industry Outlook"))
```
    </div>
  </div>
  <div class="flip-card-back">
    <div class="card-header">
      <span class="card-title">✨ Nexa</span>
      <span class="code-lines">6 lines</span>
    </div>
    <div class="card-content">
```nexa
agent TechResearcher { role: "Tech Researcher" }
agent MarketResearcher { role: "Market Researcher" }
agent FinanceResearcher { role: "Finance Researcher" }
agent Summarizer { role: "Report Summarizer" }

flow main {
    result = "AI Industry Outlook" 
        |>> [TechResearcher, MarketResearcher, FinanceResearcher] 
        &>> Summarizer;
}
```
    </div>
  </div>
</div>
<button class="flip-button" onclick="document.getElementById('flip-4').classList.toggle('flipped')">
  🔄 Click to compare with Nexa
</button>
<div class="comparison-note">
<strong>Key Advantage:</strong> DAG operators <code>|>></code> (fan-out) and <code>&>></code> (merge) implement concurrent orchestration in a single line, without needing to understand asyncio, gather, coroutines.<span class="reduction-badge">74% reduction</span>
</div>
</div>

---

### 📊 Code Volume Comparison Summary

| Scenario | Traditional | Nexa | Reduction |
|:---------|:-----------:|:----:|:---------:|
| Agent Definition & Invocation | 12 lines | 4 lines | **67%** ↓ |
| Pipeline Orchestration | 18 lines | 5 lines | **72%** ↓ |
| Intent Routing | 17 lines | 10 lines | **41%** ↓ |
| Concurrent DAG Execution | 23 lines | 6 lines | **74%** ↓ |
| **Average** | **17.5 lines** | **6.25 lines** | **63%** ↓ |

---

## 🆕 v1.0-alpha Revolutionary Update: The AVM Era

Nexa v1.0-alpha introduces the revolutionary **Agent Virtual Machine (AVM)** — a high-performance, securely isolated agent execution engine written in Rust:

### 🦀 Rust AVM Foundation

Transitioning from Python script transpilation to a standalone compiled Agent Virtual Machine written in Rust:

| Feature | Description |
|-----|------|
| **High-Performance Bytecode Interpreter** | Native execution of compiled Nexa bytecode |
| **Complete Compiler Frontend** | Lexer → Parser → AST → Bytecode |
| **110+ Test Coverage** | Full-link testing ensuring stability |

### 🔒 WASM Security Sandbox

Introducing WebAssembly in AVM to provide strong isolation for external `tool` execution:

- **wasmtime Integration** - High-performance WASM runtime
- **Permission Grading** - Four-tier model: None/Standard/Elevated/Full
- **Resource Limits** - Constraints on memory, CPU, and execution time
- **Audit Logs** - Complete operation audit tracking

### ⚡ Smart Scheduler

Dynamic allocation of concurrency resources at the AVM layer based on system load:

- **Priority Queue** - Task scheduling based on Agent priority
- **Load Balancing** - Strategies: RoundRobin, LeastLoaded, Adaptive
- **DAG Topological Sorting** - Automatic dependency resolution and parallelism analysis

### 📄 Vector Virtual Memory Paging

AVM manages memory, automatically performing vectorized swapping of conversation history:

- **LRU/LFU/Hybrid Eviction Policies** - Intelligent page replacement
- **Embedding Similarity Search** - Loading based on semantic relevance
- **Transparent Page Loading** - Seamless memory management

### Performance Comparison

| Metric | Python Transpiler | Rust AVM |
|------|--------------|----------|
| Compile Time | ~100ms | ~5ms |
| Startup Time | ~500ms | ~10ms |
| Memory Usage | ~100MB | ~10MB |
| Concurrent Agents | ~100 | ~10000 |

---

## 🎯 More Core Features

Beyond code simplicity, Nexa provides these powerful language-level features:

### Strong Type Protocol Constraints (`protocol` & `implements`)

No more uncontrollable model string outputs! Native support for contract-based programming:

```nexa
protocol ReviewResult {
    score: "int",
    summary: "string"
}

agent Reviewer implements ReviewResult { 
    prompt: "Review the code..."
}
```

### Semantic Control Flow (`loop until`)

Control loop termination with natural language:

```nexa
loop {
    draft = Writer.run(feedback);
    feedback = Critic.run(draft);
} until ("Article quality is excellent")
```

### Native Test Framework (`test` & `assert`)

```nexa
test "Translation test" {
    result = Translator.run("Hello, World!");
    assert "Contains Chinese translation" against result;
}
```

---

## 🎯 Design Philosophy: Write Flows, Not Glue

Developers reading this documentation have likely endured the torment of handling model hallucinations through complex HTTP requests and nested `if-else` statements in traditional languages.

Nexa treats "language model prediction" as a **native computational beat**, isolating "uncertainty" within syntactic boundaries.

### Comparison with Traditional Frameworks

| Feature | Traditional Python/LangChain | Nexa |
|-----|---------------------|------|
| Agent Definition | Instantiate class + config dict | Native `agent` keyword |
| Flow Orchestration | Manual calls + state management | `flow` + pipeline operators |
| Intent Routing | if-else + regex | `match intent` semantic matching |
| Output Constraints | Hand-written JSON Schema | `protocol` declarative constraints |
| Concurrency Control | asyncio + locks | DAG operators auto-scheduling |
| Error Retry | try-except + loops | Built-in auto-retry mechanism |

---

## 📚 Learning Path

### Getting Started

1. **[Quickstart](quickstart.en.md)** - Master Nexa basics in 30 minutes
2. **[Basic Syntax](part1_basic.en.md)** - Deep dive into all Agent properties
3. **[Examples](examples.en.md)** - View real-world code for various scenarios

### Advanced Learning

4. **[Advanced Features](part2_advanced.en.md)** - DAG operators, concurrent processing
5. **[Syntax Extensions](part3_extensions.en.md)** - Advanced Protocol usage
6. **[Best Practices](part6_best_practices.en.md)** - Enterprise development experience

### Deep Dive

7. **[Compiler Design](part5_compiler.en.md)** - Full pipeline from AST to bytecode
8. **[Architecture Evolution](part5_architecture_evolution.en.md)** - Rust/WASM technology roadmap

### Troubleshooting

- **[FAQ & Troubleshooting](troubleshooting.en.md)** - Solve various development issues

---

## 🌟 Start Your Nexa Journey

<div class="portal-actions" style="margin-top: 1rem;">
    <a class="md-button md-button--primary" href="quickstart.en.md">🚀 Quickstart</a>
    <a class="md-button" href="https://github.com/your-org/nexa">📦 GitHub</a>
</div>
