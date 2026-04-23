---
comments: true
---

# Complete Examples Collection

This document provides a series of complete, runnable Nexa example code covering various application scenarios from basic to enterprise level. Each example includes complete code, how to run it, and expected output.

---

## 📋 Table of Contents

### Basic Examples
- [Example 1: Hello World](#example-1-hello-world)
- [Example 2: Simple Chatbot](#example-2-simple-chatbot)
- [Example 3: Chat Assistant with Memory](#example-3-chat-assistant-with-memory)

### Tool Integration Examples
- [Example 4: File Processing Assistant](#example-4-file-processing-assistant)
- [Example 5: Web Content Scraper](#example-5-web-content-scraper)
- [Example 6: Database Query Assistant](#example-6-database-query-assistant)

### Multi-Agent Collaboration Examples
- [Example 7: Translation Pipeline](#example-7-translation-pipeline)
- [Example 8: Code Review Team](#example-8-code-review-team)
- [Example 9: Research Analyst Team](#example-9-research-analyst-team)

### Advanced Pattern Examples
- [Example 10: Intent Routing Customer Service](#example-10-intent-routing-customer-service)
- [Example 11: Critic Loop Optimization](#example-11-critic-loop-optimization)
- [Example 12: DAG Parallel Processing](#example-12-dag-parallel-processing)
- [Example 13: Conditional Branch Processing](#example-13-conditional-branch-processing)

### Enterprise Examples
- [Example 14: Research Report Generation System](#example-14-research-report-generation-system)
- [Example 15: Intelligent Customer Service System](#example-15-intelligent-customer-service-system)
- [Example 16: Code Generation and Testing](#example-16-code-generation-and-testing)

### v1.3.x New Feature Examples
- [Example 17: Design by Contract (DbC)](#example-17-design-by-contract-dbc)
- [Example 18: Error Propagation and Recovery](#example-18-error-propagation-and-recovery)
- [Example 19: Pattern Matching and ADT](#example-19-pattern-matching-and-adt)
- [Example 20: HTTP Server + Database](#example-20-http-server--database)
- [Example 21: Concurrent Data Processing](#example-21-concurrent-data-processing)
- [Example 22: Background Job System](#example-22-background-job-system)

---

## Basic Examples

### Example 1: Hello World

**Purpose**: Demonstrate the most basic Nexa program structure.

**Complete Code**:

```nexa
// hello_world.nx
// The simplest Nexa program

agent Greeter {
    role: "Friendly greeting assistant",
    model: "deepseek/deepseek-chat",
    prompt: "You are an enthusiastic assistant. Respond to every greeting with concise and friendly language."
}

flow main {
    result = Greeter.run("Hello, Nexa!");
    print(result);
}
```

**How to Run**:
```bash
nexa run hello_world.nx
```

**Expected Output**:
```
Hello! Welcome to the world of Nexa! How can I help you? 😊
```

**Code Explanation**:
| Line | Description |
|-----|------|
| 4-8 | Define an Agent named `Greeter`, setting role, model, and prompt |
| 10 | `flow main` is the program entry point, similar to main function in other languages |
| 11 | Call the Agent's `run()` method, passing user input |
| 12 | Print the result |

---

### Example 2: Simple Chatbot

**Purpose**: Demonstrate how to create a chatbot capable of multi-turn conversations.

**Complete Code**:

```nexa
// chatbot.nx
// Simple chatbot

agent ChatBot {
    role: "Intelligent chat assistant",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a friendly, helpful chatbot.
    
    Rules:
    1. Keep responses concise and clear
    2. If unsure, honestly admit it
    3. For complex questions, provide well-organized answers
    """,
    memory: "persistent"  // Enable persistent memory
}

flow main {
    // First round of conversation
    response1 = ChatBot.run("Hello! Please introduce yourself.");
    print("User: Hello! Please introduce yourself.");
    print("Bot: " + response1);
    print("");
    
    // Second round of conversation (Agent will remember context)
    response2 = ChatBot.run("What did I just ask you?");
    print("User: What did I just ask you?");
    print("Bot: " + response2);
}
```

**How to Run**:
```bash
nexa run chatbot.nx
```

**Expected Output**:
```
User: Hello! Please introduce yourself.
Bot: Hello! I am an intelligent chat assistant that can help you answer questions, provide suggestions, and have friendly conversations. How can I help you?

User: What did I just ask you?
Bot: You just asked me to introduce myself. I've already answered that I am an intelligent chat assistant.
```

**Key Points**:
- `memory: "persistent"` enables the Agent to remember conversation history
- In subsequent `run()` calls, the Agent can access previous conversation context

---

### Example 3: Chat Assistant with Memory

**Purpose**: Demonstrate how to configure an Agent's long-term memory feature.

**Complete Code**:

```nexa
// memory_assistant.nx
// Assistant with long-term memory

agent SmartAssistant {
    role: "Personal intelligent assistant",
    model: "deepseek/deepseek-chat",
    prompt: "You are an intelligent assistant that can remember user preferences.",
    memory: "persistent",
    experience: "assistant_memory.md",  // Load long-term memory
    cache: true  // Enable caching to improve response speed
}

flow main {
    // First interaction, tell the assistant user preferences
    SmartAssistant.run("I like science fiction novels, especially Liu Cixin's works.");
    
    // Subsequent interaction, assistant should remember preferences
    result = SmartAssistant.run("Recommend a book for me.");
    print(result);
}
```

**Memory File Example** (`assistant_memory.md`):
```markdown
# User Preference Memory

## Reading Preferences
- Likes science fiction novels
- Preferred author: Liu Cixin

## Other Preferences
- (Assistant will automatically update this file)
```

---

## Tool Integration Examples

### Example 4: File Processing Assistant

**Purpose**: Demonstrate how to use standard library tools to process files.

**Complete Code**:

```nexa
// file_assistant.nx
// File processing assistant

agent FileAssistant uses std.fs, std.time {
    role: "File management assistant",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a file management assistant. You can:
    - Read file contents
    - Create new files
    - Get current time
    
    Choose appropriate tools based on user needs to complete tasks.
    """
}

flow main {
    task = """
    Please perform the following operations:
    1. Get the current time
    2. Create a file named 'note.txt'
    3. Write content: current time and a greeting
    """;
    
    result = FileAssistant.run(task);
    print(result);
}
```

**How to Run**:
```bash
nexa run file_assistant.nx
```

**Expected Output**:
```
Completed the following operations:
1. Current time: 2024-01-15 10:30:00
2. Created file note.txt
3. Wrote content: "2024-01-15 10:30:00 - Hello, this is an auto-generated note!"
```

---

### Example 5: Web Content Scraper

**Purpose**: Demonstrate how to use HTTP tools to scrape web content.

**Complete Code**:

```nexa
// web_scraper.nx
// Web content scraper

agent WebScraper uses std.http, std.fs {
    role: "Web scraping assistant",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a web content scraping assistant.
    
    Your tasks are:
    1. Use http tool to fetch web content
    2. Extract key information (such as title, content summary)
    3. Optional: Save to local file
    """
}

agent Summarizer {
    role: "Content summarization expert",
    model: "deepseek/deepseek-chat",
    prompt: "Summarize the scraped web content into 3-5 key points."
}

flow main {
    url = "https://example.com";
    
    // Pipeline: scrape -> summarize
    summary = url >> WebScraper >> Summarizer;
    
    print("Web Summary:");
    print(summary);
}
```

**Expected Output**:
```
Web Summary:
1. This is the homepage of the example website
2. Mainly provides product and service introductions
3. Contains contact and about us pages
4. Website design is clean and modern
```

---

### Example 6: Database Query Assistant

**Purpose**: Demonstrate how to create an Agent that can interact with databases.

**Complete Code**:

```nexa
// db_assistant.nx
// Database query assistant

// Custom database tool
tool DatabaseQuery {
    description: "Execute SQL queries and return results",
    parameters: {
        "query": "string  // SQL query statement"
    }
}

agent DBAssistant uses DatabaseQuery {
    role: "Database assistant",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a database query assistant.
    
    Based on user's natural language needs:
    1. Understand user intent
    2. Generate appropriate SQL queries
    3. Execute using DatabaseQuery tool
    4. Explain results in natural language
    
    Note: Only execute SELECT queries, do not perform modification operations.
    """
}

flow main {
    question = "Show the last 10 order records";
    result = DBAssistant.run(question);
    print(result);
}
```

---

## Multi-Agent Collaboration Examples

### Example 7: Translation Pipeline

**Purpose**: Demonstrate multiple Agents processing data in series.

**Complete Code**:

```nexa
// translation_pipeline.nx
// English -> Chinese translation pipeline

// Stage 1: Translation
agent Translator {
    role: "Professional translator",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a professional English-to-Chinese translator.
    
    Requirements:
    - Accurately convey the original meaning
    - Use authentic and fluent Chinese
    - Preserve professional terminology from the original
    """
}

// Stage 2: Proofreading
agent Proofreader {
    role: "Proofreading editor",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a senior Chinese proofreading editor.
    
    Check and correct:
    - Grammar errors
    - Unclear expressions
    - Punctuation usage
    
    If the translation is already good, return the original text directly.
    """
}

// Stage 3: Polishing
agent Polisher {
    role: "Text polishing expert",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a text polishing expert.
    
    Enhance:
    - Beauty of the text
    - Reading fluency
    - Add appropriate literary flair
    """
}

flow main {
    english_text = """
    Artificial intelligence is not just a technology, 
    but a fundamental shift in how we interact with machines 
    and how machines interact with the world.
    """;
    
    // Three-stage pipeline
    final_translation = english_text >> Translator >> Proofreader >> Polisher;
    
    print("Original:");
    print(english_text);
    print("\nTranslation:");
    print(final_translation);
}
```

**Expected Output**:
```
Original:
Artificial intelligence is not just a technology, 
but a fundamental shift in how we interact with machines 
and how machines interact with the world.

Translation:
Artificial intelligence is not only a technology, but a fundamental revolution in how we interact with machines and how machines interact with the world.
```

---

### Example 8: Code Review Team

**Purpose**: Demonstrate multi-Agent collaboration with specialized division of labor.

**Complete Code**:

```nexa
// code_review_team.nx
// Code review team

// Define output protocol
protocol CodeReviewReport {
    code_quality: "string",      // Code quality rating (A/B/C/D/F)
    issues: "list[string]",      // List of found issues
    suggestions: "list[string]", // Improvement suggestions
    overall_comment: "string"    // Overall evaluation
}

// Code quality reviewer
agent QualityReviewer implements CodeReviewReport {
    role: "Code quality reviewer",
    model: "deepseek/deepseek-chat",
    prompt: """
    Review code quality, focusing on:
    - Code structure
    - Naming conventions
    - Readability
    - Potential bugs
    """
}

// Security reviewer
agent SecurityReviewer {
    role: "Security reviewer",
    model: "deepseek/deepseek-chat",
    prompt: """
    Review code security, focusing on:
    - SQL injection risks
    - XSS vulnerabilities
    - Sensitive information leakage
    - Permission control issues
    """
}

// Report compiler
agent ReportCompiler {
    role: "Report compiler",
    model: "deepseek/deepseek-chat",
    prompt: """
    Integrate opinions from multiple reviewers into a comprehensive report.
    Clear format, highlighting key points.
    """
}

flow main {
    code_to_review = """
    def get_user(user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return db.execute(query)
    """;
    
    // Parallel review then compile
    final_report = code_to_review 
        |>> [QualityReviewer, SecurityReviewer] 
        &>> ReportCompiler;
    
    print("=== Code Review Report ===");
    print(final_report);
}
```

**Expected Output**:
```
=== Code Review Report ===

[Code Quality] Rating: C
- Issues: Missing input validation, no exception handling
- Suggestions: Add parameter type checking

[Security Issues] High Risk
- SQL injection vulnerability: Direct concatenation of user input
- Suggestion: Use parameterized queries

[Improvement Suggestions]
1. Use parameterized queries to prevent SQL injection
2. Add try-except exception handling
3. Add type annotations for readability
```

---

### Example 9: Research Analyst Team

**Purpose**: Demonstrate DAG parallel processing in research analysis applications.

**Complete Code**:

```nexa
// research_team.nx
// Research analyst team

// Industry researchers
agent TechResearcher {
    role: "Tech industry researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze latest trends and key technologies in the tech industry."
}

agent FinanceResearcher {
    role: "Finance industry researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze market dynamics and investment opportunities in the finance industry."
}

agent HealthcareResearcher {
    role: "Healthcare researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze innovations and regulatory developments in the healthcare industry."
}

// Chief analyst
agent ChiefAnalyst {
    role: "Chief analyst",
    model: "deepseek/deepseek-chat",
    prompt: """
    Integrate analysis reports from various industry researchers,
    identify cross-industry common trends and investment opportunities.
    """
}

// Report writer
agent ReportWriter {
    role: "Report writer",
    model: "deepseek/deepseek-chat",
    prompt: "Organize analysis content into professional research report format."
}

flow main {
    topic = "2024 Investment Opportunity Analysis";
    
    // Parallel research -> integrate -> write
    final_report = topic 
        |>> [TechResearcher, FinanceResearcher, HealthcareResearcher]
        &>> ChiefAnalyst 
        >> ReportWriter;
    
    print("=== Research Report ===");
    print(final_report);
}
```

**Flow Diagram**:
```
         ┌─────────────────┐
         │   Input Topic    │
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

## Advanced Pattern Examples

### Example 10: Intent Routing Customer Service

**Purpose**: Demonstrate using `match intent` for intelligent customer service routing.

**Complete Code**:

```nexa
// customer_service.nx
// Intelligent customer service routing system

// Specialized Agents after intent classification
agent OrderBot {
    role: "Order service specialist",
    model: "deepseek/deepseek-chat",
    prompt: "Handle order queries, modifications, cancellations, etc."
}

agent RefundBot {
    role: "Refund service specialist",
    model: "deepseek/deepseek-chat",
    prompt: "Handle refund applications, progress inquiries, etc."
}

agent ProductBot {
    role: "Product consultation specialist",
    model: "deepseek/deepseek-chat",
    prompt: "Answer product features, specifications, comparisons, etc."
}

agent TechBot {
    role: "Technical support specialist",
    model: "deepseek/deepseek-chat",
    prompt: "Resolve technical issues, troubleshooting, usage guidance."
}

agent GeneralBot {
    role: "General customer service",
    model: "deepseek/deepseek-chat",
    prompt: "Handle general questions and greetings, guide users when unable to help."
}

flow main {
    user_message = "Why hasn't my order #12345 shipped yet?";
    
    response = match user_message {
        intent("Order query or modification") => OrderBot.run(user_message),
        intent("Refund application or inquiry") => RefundBot.run(user_message),
        intent("Product consultation") => ProductBot.run(user_message),
        intent("Technical support") => TechBot.run(user_message),
        _ => GeneralBot.run(user_message)
    };
    
    print("Customer service reply: " + response);
}
```

**Test Cases**:
| User Input | Routes To | Description |
|---------|-------|------|
| "Why hasn't my order #12345 shipped yet?" | OrderBot | Order related |
| "I want a refund, the product has quality issues" | RefundBot | Refund related |
| "Does this phone support 5G?" | ProductBot | Product consultation |
| "The app won't open, what should I do?" | TechBot | Technical support |
| "Hello" | GeneralBot | Default handling |

---

### Example 11: Critic Loop Optimization

**Purpose**: Demonstrate using `loop until` for Agent self-optimization.

**Complete Code**:

```nexa
// critic_loop.nx
// Critic loop optimization system

agent Writer {
    role: "Content creator",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a professional content creator.
    
    When modifying your article based on feedback:
    1. Carefully consider feedback
    2. Maintain the overall style of the article
    3. Gradually improve quality
    """
}

agent Critic {
    role: "Content critic",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a strict critic.
    
    Review articles and provide specific improvement suggestions:
    - Content completeness
    - Logical coherence
    - Language expression
    - Format standards
    
    If the article is already good enough, reply "approved".
    """
}

flow main {
    topic = "Write a short article about the future of AI (under 200 words)";
    
    // Initial draft
    draft = Writer.run(topic);
    
    loop {
        // Get criticism
        feedback = Critic.run(draft);
        
        // If approved, exit loop
        if ("approved" in feedback) {
            break;
        }
        
        // Modify based on feedback
        draft = Writer.run(f"Modify the article based on the following feedback:\n{feedback}\n\nOriginal:\n{draft}");
        
    } until ("Article quality is excellent, critic approved" or runtime.meta.loop_count >= 3);
    
    print("=== Final Article ===");
    print(draft);
    
    if (runtime.meta.loop_count >= 3) {
        print("\n(Maximum revision count reached)");
    }
}
```

**Execution Flow**:
```
Round 1: Writer produces initial draft -> Critic points out issues
Round 2: Writer revises -> Critic still has feedback
Round 3: Writer revises again -> Critic approves
Output final article
```

---

### Example 12: DAG Parallel Processing

**Purpose**: Demonstrate DAG operators introduced in Nexa v0.9.7.

**Complete Code**:

```nexa
// dag_parallel.nx
// DAG parallel processing example

// Fork operator |>> example
agent TranslatorCN {
    model: "deepseek/deepseek-chat",
    prompt: "Translate to Chinese"
}

agent TranslatorEN {
    model: "deepseek/deepseek-chat",
    prompt: "Translate to English"
}

agent TranslatorJP {
    model: "deepseek/deepseek-chat",
    prompt: "Translate to Japanese"
}

// Merge operator &>> example
agent Merger {
    model: "deepseek/deepseek-chat",
    prompt: "Integrate multiple translation versions, output comparison table"
}

// Conditional branch operator ?? example
agent UrgentHandler {
    model: "deepseek/deepseek-chat",
    prompt: "Urgent handling, quick response"
}

agent NormalHandler {
    model: "deepseek/deepseek-chat",
    prompt: "Standard handling, detailed analysis"
}

flow main {
    input_text = "Hello, World!";
    
    // Example 1: Fork - parallel translation to multiple languages
    print("=== Multi-language Translation ===");
    translations = input_text |>> [TranslatorCN, TranslatorEN, TranslatorJP];
    print(translations);
    
    // Example 2: Merge - integrate multiple results
    print("\n=== Translation Comparison Table ===");
    comparison = [TranslatorCN, TranslatorJP] &>> Merger;
    print(comparison);
    
    // Example 3: Conditional branch - choose processing method based on content
    print("\n=== Intelligent Routing ===");
    urgent_input = "URGENT: System crash!";
    normal_input = "Please help me analyze the sales data";
    
    urgent_result = urgent_input ?? UrgentHandler : NormalHandler;
    normal_result = normal_input ?? UrgentHandler : NormalHandler;
    
    print("Urgent handling result: " + urgent_result);
    print("Standard handling result: " + normal_result);
    
    // Example 4: Complex DAG combination
    print("\n=== Complex DAG ===");
    complex_result = input_text 
        |>> [TranslatorCN, TranslatorJP] 
        &>> Merger;
    print(complex_result);
}
```

**Operator Description**:

| Operator | Name | Purpose | Example |
|-------|------|------|------|
| `>>` | Pipe | Sequential passing | `A >> B` |
| `|>>` | Fork | Parallel send | `input |>> [A, B, C]` |
| `&>>` | Merge | Combine results | `[A, B] &>> C` |
| `??` | Conditional Branch | Conditional routing | `input ?? A : B` |
| `||` | Async Fork | Don't wait for results | `input || [A, B]` |
| `&&` | Consensus Merge | Need agreement | `[A, B] && Judge` |

---

### Example 13: Conditional Branch Processing

**Purpose**: Demonstrate `semantic_if` semantic conditional judgment.

**Complete Code**:

```nexa
// semantic_condition.nx
// Semantic conditional judgment example

agent DataAnalyzer {
    model: "deepseek/deepseek-chat",
    prompt: "Analyze data type and content of user input"
}

agent JSONProcessor {
    model: "deepseek/deepseek-chat",
    prompt: "Process JSON format data"
}

agent TextProcessor {
    model: "deepseek/deepseek-chat",
    prompt: "Process plain text data"
}

flow main {
    user_input = '{"name": "Zhang San", "age": 25, "city": "Beijing"}';
    
    // Semantic conditional judgment - check if it's JSON
    semantic_if "Input content is valid JSON format" fast_match r"^\s*[\[{]" against user_input {
        result = JSONProcessor.run(user_input);
        print("Processing as JSON: " + result);
    } else {
        result = TextProcessor.run(user_input);
        print("Processing as text: " + result);
    }
    
    // Another example: date detection
    date_input = "The meeting is scheduled for 2024-03-15";
    
    semantic_if "Contains specific date" fast_match r"\d{4}-\d{2}-\d{2}" against date_input {
        print("Date information detected, can create schedule");
    } else {
        print("No date information detected");
    }
}
```

**`fast_match` Explanation**:

`fast_match` is a regex pre-filter that can quickly judge before calling the LLM:

- If regex matches successfully, enter branch directly (saves tokens)
- If regex doesn't match, still call LLM for semantic judgment

---

## Enterprise Examples

### Example 14: Research Report Generation System

**Purpose**: Demonstrate a complete enterprise-level research report generation process.

**Complete Code**:

```nexa
// research_report.nx
// Enterprise research report generation system

// Output protocol
protocol ResearchReport {
    title: "string",
    executive_summary: "string",
    key_findings: "list[string]",
    recommendations: "list[string]",
    risk_analysis: "string",
    conclusion: "string"
}

// Data collector
agent DataCollector uses std.http, std.fs {
    role: "Data collector",
    model: "deepseek/deepseek-chat",
    prompt: "Collect relevant data and information on specified topics",
    cache: true
}

// Data analyst
agent DataAnalyst {
    role: "Data analyst",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze data, extract key insights and trends"
}

// Industry researcher
agent IndustryResearcher {
    role: "Industry researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Research industry background, competitive landscape, and development trends"
}

// Report writer
agent ReportWriter implements ResearchReport {
    role: "Report writer",
    model: "deepseek/deepseek-chat",
    prompt: """
    Write professional research reports including:
    - Title
    - Executive summary
    - Key findings
    - Recommendations
    - Risk analysis
    - Conclusion
    """
}

// Quality reviewer
agent QualityReviewer {
    role: "Quality reviewer",
    model: "deepseek/deepseek-chat",
    prompt: "Review report quality, ensure professionalism and completeness"
}

flow main {
    topic = "China New Energy Vehicle Market 2024 Annual Analysis";
    
    // Parallel collection and analysis
    research_data = topic |>> [DataCollector, IndustryResearcher];
    
    // Analyze data
    analysis = research_data &>> DataAnalyst;
    
    // Write report
    draft_report = analysis >> ReportWriter;
    
    // Quality review (loop optimization)
    loop {
        review = QualityReviewer.run(draft_report);
    } until ("Report quality approved" or runtime.meta.loop_count >= 2);
    
    print("=== Research Report ===");
    print(draft_report);
}
```

---

### Example 15: Intelligent Customer Service System

**Purpose**: Demonstrate a complete intelligent customer service system.

**Complete Code**:

```nexa
// smart_customer_service.nx
// Intelligent customer service system

// User info protocol
protocol UserInfo {
    user_id: "string",
    name: "string",
    membership_level: "string",
    recent_orders: "list[string]"
}

// Intent classification
agent IntentClassifier {
    role: "Intent classifier",
    model: "deepseek/deepseek-chat",  // Use fast model
    prompt: "Identify user intent, return intent type"
}

// Order query
agent OrderQuery uses std.fs {
    role: "Order query specialist",
    model: "deepseek/deepseek-chat",
    prompt: "Query order status and logistics information"
}

// After-sales service
agent AfterSalesService {
    role: "After-sales service specialist",
    model: "deepseek/deepseek-chat",
    prompt: "Handle returns, exchanges, repairs, and other after-sales issues"
}

// Complaint handling
agent ComplaintHandler uses std.ask_human {
    role: "Complaint handling specialist",
    model: "deepseek/deepseek-chat",
    prompt: "Handle customer complaints, request human assistance when necessary"
}

// Knowledge base Q&A
agent KnowledgeBaseQA {
    role: "Knowledge base Q&A",
    model: "deepseek/deepseek-chat",
    prompt: "Answer product-related questions based on knowledge base",
    experience: "product_knowledge.md"
}

// Human handoff judgment
agent HumanHandoff {
    role: "Human handoff judgment",
    model: "deepseek/deepseek-chat",
    prompt: "Determine if human customer service handoff is needed"
}

flow main {
    user_message = "The phone I bought last week has issues, I want to return it";
    
    // 1. Intent classification
    intent = IntentClassifier.run(user_message);
    
    // 2. Route to corresponding specialist
    response = match intent {
        intent("Order query") => OrderQuery.run(user_message),
        intent("After-sales service") => AfterSalesService.run(user_message),
        intent("Complaints and suggestions") => ComplaintHandler.run(user_message),
        intent("Product consultation") => KnowledgeBaseQA.run(user_message),
        _ => KnowledgeBaseQA.run(user_message)
    };
    
    // 3. Determine if human intervention is needed
    need_human = HumanHandoff.run(response);
    
    if ("Need human" in need_human) {
        std.ask_human.call("Complex issue, human intervention needed: " + user_message);
    }
    
    print("Customer service reply: " + response);
}
```

---

### Example 16: Code Generation and Testing

**Purpose**: Demonstrate the complete process of code generation, testing, and fixing.

**Complete Code**:

```nexa
// code_gen_test.nx
// Code generation and automated testing

// Output protocol
protocol GeneratedCode {
    code: "string",
    language: "string",
    description: "string",
    test_cases: "list[string]"
}

// Code generator
agent CodeGenerator implements GeneratedCode {
    role: "Code generation expert",
    model: "deepseek/deepseek-chat",
    prompt: """
    Generate high-quality code with requirements:
    - Clear, commented code
    - Follow best practices
    - Include boundary handling
    """
}

// Test generator
agent TestGenerator {
    role: "Test engineer",
    model: "deepseek/deepseek-chat",
    prompt: "Generate unit tests for code"
}

// Code reviewer
agent CodeReviewer {
    role: "Code reviewer",
    model: "deepseek/deepseek-chat",
    prompt: "Review code quality, identify issues"
}

// Bug fixer
agent BugFixer {
    role: "Bug fix engineer",
    model: "deepseek/deepseek-chat",
    prompt: "Fix code issues based on review feedback"
}

flow main {
    requirement = "Implement a Python function to calculate the nth Fibonacci number";
    
    // 1. Generate code
    initial_code = CodeGenerator.run(requirement);
    print("=== Initial Code ===");
    print(initial_code.code);
    
    // 2. Generate tests
    tests = TestGenerator.run(initial_code.code);
    print("\n=== Test Cases ===");
    print(tests);
    
    // 3. Review and fix loop
    loop {
        review = CodeReviewer.run(initial_code.code);
        
        if ("approved" in review or "no issues" in review) {
            break;
        }
        
        initial_code = BugFixer.run(f"Issues: {review}\nCode: {initial_code.code}");
        
    } until ("Code passed review" or runtime.meta.loop_count >= 3);
    
    print("\n=== Final Code ===");
    print(initial_code.code);
}
```

---

## v1.3.x New Feature Examples

### Example 17: Design by Contract (DbC)

**Purpose**: Demonstrate the use of requires/ensures/invariant contracts and ContractViolation integration with HTTP.

**Complete Code**:

```nexa
// contract_demo.nx
// Design by Contract example

agent DataProcessor {
    role: "Data processing expert"
    model: "deepseek/deepseek-chat"
    prompt: "Process input data and return structured results"
    requires: "input must be non-empty and contain valid data"
    ensures: "output contains processed summary"
}

agent QualityChecker {
    role: "Quality inspector"
    model: "deepseek/deepseek-chat"
    prompt: "Check data quality"
    requires: "data must be formatted as JSON"
    ensures: "quality_score is between 0 and 100"
}

flow main {
    // ✅ Normal call — satisfies requires condition
    raw_data = '{"items": [1, 2, 3], "status": "active"}'
    result = DataProcessor.run(raw_data)
    print("Processing result: " + result)

    // ✅ Use otherwise to handle contract violations
    empty_data = ""
    safe_result = DataProcessor.run(empty_data) otherwise "default result"
    print("Safe result: " + safe_result)

    // ✅ Contract chain — multiple Agent contracts verified sequentially
    processed = DataProcessor.run(raw_data)
    quality = QualityChecker.run(processed) otherwise "quality unknown"
    print("Quality score: " + quality)
}
```

**How to Run**:
```bash
nexa run contract_demo.nx
```

**Code Explanation**:
| Line | Description |
|-----|------|
| 7-8 | `requires` defines preconditions that must be satisfied before calling |
| 9 | `ensures` defines postconditions that output must satisfy |
| 20 | `otherwise` provides a fallback result when contract is violated |
| 23-24 | Contract chain: multiple Agent contracts verified sequentially |

---

### Example 18: Error Propagation and Recovery

**Purpose**: Demonstrate the use of `?` error propagation operator and `otherwise` error recovery operator.

**Complete Code**:

```nexa
// error_propagation_demo.nx
// Error propagation and recovery example

agent Fetcher {
    role: "Data fetcher"
    model: "deepseek/deepseek-chat"
    prompt: "Fetch data from specified source"
}

agent Parser {
    role: "Data parser"
    model: "deepseek/deepseek-chat"
    prompt: "Parse raw data into structured format"
}

agent Analyzer {
    role: "Data analyzer"
    model: "deepseek/deepseek-chat"
    prompt: "Analyze data and generate insights"
}

flow main {
    // ✅ Use ? to propagate errors — any step failure propagates up the chain
    result = Fetcher.run("source_url")
        |> Parser.run?
        |> Analyzer.run?

    // ✅ Use otherwise to provide fallback at each step
    safe_result = Fetcher.run("source_url") otherwise "no data"
        |> Parser.run? otherwise "parse failed"
        |> Analyzer.run? otherwise "analysis unavailable"

    print("Safe result: " + safe_result)

    // ✅ Combine ? and otherwise
    data = Fetcher.run("source_url")?
    if data != None {
        parsed = Parser.run(data) otherwise "raw data: " + data
        print("Parsed result: " + parsed)
    } otherwise {
        print("Data fetch failed, using cache")
        cached = std.kv.get("cache_key") ?? "default cache data"
        print("Cached data: " + cached)
    }
}
```

**How to Run**:
```bash
nexa run error_propagation_demo.nx
```

**Code Explanation**:
| Line | Description |
|-----|------|
| 19-21 | `?` operator: errors propagate automatically, any step failure fails the whole chain |
| 24-26 | `otherwise` operator: provides fallback at each step, ensuring chain doesn't break |
| 30-37 | Combining `?` with `otherwise`, plus `??` null coalescing |

---

### Example 19: Pattern Matching and ADT

**Purpose**: Demonstrate the combined use of struct/enum/trait algebraic data types with pattern matching.

**Complete Code**:

```nexa
// pattern_adt_demo.nx
// Pattern matching and ADT example

// Define struct
struct User {
    name: string
    age: int
    email: string
}

// Define enum
enum Status {
    Active
    Inactive
    Suspended(reason: string)
}

// Define trait
trait Displayable {
    fn display(self) -> string
}

impl Displayable for User {
    fn display(self) -> string {
        "#{self.name} (#{self.age}) — #{self.email}"
    }
}

flow main {
    // Create struct instance
    user = User{name: "Alice", age: 30, email: "alice@example.com"}

    // Create enum variant
    status = Status.Active
    suspended = Status.Suspended{reason: "rule violation"}

    // ✅ Pattern matching
    match status {
        Status.Active -> print("User is active")
        Status.Inactive -> print("User is inactive")
        Status.Suspended{reason} -> print("User suspended: " + reason)
    }

    // ✅ Let destructuring
    let User{name, age} = user
    print("Name: " + name + ", Age: " + age)

    // ✅ Trait method call
    display_text = user.display()
    print("Display: " + display_text)

    // ✅ For destructuring
    users = [User{name: "Bob", age: 25, email: "bob@test.com"},
             User{name: "Carol", age: 28, email: "carol@test.com"}]
    for let User{name, age} in users {
        print("#{name}: #{age} years old")
    }
}
```

**How to Run**:
```bash
nexa run pattern_adt_demo.nx
```

**Code Explanation**:
| Line | Description |
|-----|------|
| 6-10 | `struct` defines data structure with typed fields |
| 13-17 | `enum` defines enumeration with data-carrying variants |
| 20-22 | `trait` defines behavior interface |
| 24-27 | `impl` implements trait methods for a concrete type |
| 32-36 | `match` pattern matching, branching by variant |
| 39 | `let` destructuring to extract struct fields |
| 42 | Trait method call |
| 45-48 | `for let` destructuring iteration over collections |

---

### Example 20: HTTP Server + Database

**Purpose**: Demonstrate the integration of HTTP Server with database, building a complete API service.

**Complete Code**:

```nexa
// http_db_demo.nx
// HTTP Server + Database integration example

db AppDB {
    type: "sqlite"
    path: ":memory:"
}

agent ItemHandler {
    role: "Item management assistant"
    model: "deepseek/deepseek-chat"
    prompt: "Handle item-related requests"
    requires: "request must contain valid item data"
    ensures: "response contains item details"
}

server ItemAPI {
    route "/api/items": ItemHandler
    route "/api/items/search": ItemHandler
}

flow main {
    // Initialize database
    db_handle = std.db.sqlite.connect(":memory:")
    std.db.sqlite.execute(db_handle, "CREATE TABLE items (id INT, name TEXT, price FLOAT)")
    std.db.sqlite.execute(db_handle, "INSERT INTO items VALUES (1, 'Widget', 9.99)")
    std.db.sqlite.execute(db_handle, "INSERT INTO items VALUES (2, 'Gadget', 19.99)")

    // Query data
    items = std.db.sqlite.query(db_handle, "SELECT * FROM items")
    print("Items in database: " + items)

    // Start HTTP Server
    // nexa serve http_db_demo.nx --port 8080
    // Contract violations auto-map: requires → 401, ensures → 403

    std.db.sqlite.close(db_handle)
}
```

**How to Run**:
```bash
# Build first
nexa build http_db_demo.nx

# Start HTTP Server
nexa serve http_db_demo.nx --port 8080

# View routes
nexa routes http_db_demo.nx
```

**Code Explanation**:
| Line | Description |
|-----|------|
| 6-9 | `db` declares database configuration |
| 17-20 | `server` declares HTTP routes |
| 24-28 | SQLite initialization: create table, insert data |
| 30 | Query data |
| 33 | Contract violations automatically map to HTTP status codes |

---

### Example 21: Concurrent Data Processing

**Purpose**: Demonstrate the use of structured concurrency, Channel, and race.

**Complete Code**:

```nexa
// concurrent_demo.nx
// Concurrent data processing example

agent FastSource {
    role: "Fast data source"
    model: "deepseek/deepseek-chat"
    prompt: "Return data quickly"
}

agent SlowSource {
    role: "Slow data source"
    model: "deepseek/deepseek-chat"
    prompt: "Return data but may be slower"
}

agent Aggregator {
    role: "Data aggregator"
    model: "deepseek/deepseek-chat"
    prompt: "Aggregate data from multiple sources"
}

flow main {
    // ✅ race — multi-source competition, take fastest result
    result = std.concurrent.race([
        FastSource.run("query1"),
        SlowSource.run("query2")
    ])
    print("Fastest result: " + result)

    // ✅ Channel — producer-consumer pattern
    ch = std.concurrent.channel(10)

    // Send data to Channel
    std.concurrent.ch_send(ch, "data_item_1")
    std.concurrent.ch_send(ch, "data_item_2")

    // Receive data from Channel
    item1 = std.concurrent.ch_recv(ch) ?? "no data"
    item2 = std.concurrent.ch_recv(ch) ?? "no data"
    print("Received: " + item1 + ", " + item2)

    // ✅ spawn — launch concurrent tasks
    task1 = std.concurrent.spawn(FastSource.run("task_a"))
    task2 = std.concurrent.spawn(SlowSource.run("task_b"))

    // Wait for all tasks to complete
    results = std.concurrent.join_all([task1, task2])
    print("All results: " + results)

    // ✅ |> pipe to combine concurrent results
    final = results |> Aggregator.run
    print("Aggregated result: " + final)
}
```

**How to Run**:
```bash
nexa run concurrent_demo.nx
```

**Code Explanation**:
| Line | Description |
|-----|------|
| 23-26 | `race` multi-source competition, take fastest result |
| 29-38 | `channel` producer-consumer pattern, `??` handles empty channel |
| 41-42 | `spawn` launches concurrent tasks |
| 45 | `join_all` waits for all tasks to complete |
| 48 | `|>` pipe to combine concurrent results |

---

### Example 22: Background Job System

**Purpose**: Demonstrate Job declaration, Worker startup, and task lifecycle management.

**Complete Code**:

```nexa
// job_demo.nx
// Background job system example

agent EmailSender {
    role: "Email sending assistant"
    model: "deepseek/deepseek-chat"
    prompt: "Send notification emails"
}

agent ReportGenerator {
    role: "Report generation assistant"
    model: "deepseek/deepseek-chat"
    prompt: "Generate data analysis reports"
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
    // ✅ defer — ensure resource cleanup
    defer {
        print("Cleanup completed")
    }

    // Email job registered
    print("Email job registered")

    // Report job registered
    print("Report job registered")

    // Use KV store to track job status
    std.kv.set("email_status", "pending")
    std.kv.set("report_status", "pending")

    // Query job status
    email_status = std.kv.get("email_status") ?? "unknown"
    report_status = std.kv.get("report_status") ?? "unknown"
    print("Email status: " + email_status)
    print("Report status: " + report_status)
}
```

**How to Run**:
```bash
# Build
nexa build job_demo.nx

# Start Worker
nexa workers job_demo.nx --start --queue email_queue,report_queue

# View job status
nexa jobs job_demo.nx --status

# View dead letter jobs
nexa jobs job_demo.nx --dead-letter

# Stop Worker
nexa workers job_demo.nx --stop
```

**Code Explanation**:
| Line | Description |
|-----|------|
| 17-22 | `job` declares background task with retry and timeout configuration |
| 24-29 | Multiple Job declarations with different queues and parameters |
| 33-35 | `defer` ensures cleanup on function exit |
| 41-42 | KV store tracks task status |
| 45-46 | `??` handles potentially missing keys in KV |

---

## Example Running Checklist

Before running these examples, please ensure:

- [ ] Nexa is correctly installed
- [ ] `secrets.nxs` file is configured with required API keys
- [ ] Network connection is working (need to access LLM API)
- [ ] For examples using file system, ensure appropriate permissions

---

## Contributing Examples

If you have good Nexa examples to share, welcome to:

1. Leave a comment at the bottom of the document for discussion
2. Submit a Pull Request to the Nexa repository
3. Share your experience in the community

---

<div align="center">
  <p>💡 More examples are continuously being updated, stay tuned!</p>
</div>