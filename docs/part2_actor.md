---
comments: true
---

# Actor Model：多 Agent 并发编排

Nexa v2.0 引入了基于 **Actor Model** 的多 Agent 并发编排系统，让多个 Agent 能够独立运行、通过消息传递协作，避免共享状态带来的竞态条件。

---

## 📋 Actor Model 核心概念

| 概念 | 说明 |
|------|------|
| **Actor** | 独立的执行单元，拥有自己的状态和邮箱 |
| **Mailbox** | 消息队列，Actor 通过邮箱接收消息 |
| **Message** | Actor 之间传递的数据 |
| **Handle** | Actor 的引用，用于发送消息和等待结果 |

---

## 🚀 `spawn` — 创建子 Agent Actor

`spawn` 创建一个新的 Actor，在独立线程中运行。

### 语法

```nexa
handle = spawn AgentName("初始消息");
handle = spawn AgentName(args);
```

### 示例

```nexa
agent Analyzer {
    prompt: "分析数据并返回结果"
}

flow main {
    // 创建三个并行 Actor
    a1 = spawn Analyzer("分析数据集 A");
    a2 = spawn Analyzer("分析数据集 B");
    a3 = spawn Analyzer("分析数据集 C");
    
    // 等待所有结果
    r1 = await a1;
    r2 = await a2;
    r3 = await a3;
    
    print("All analysis completed");
}
```

### 运行时行为

1. **ActorSystem** 创建 ActorHandle
2. 启动独立线程运行 Agent
3. 返回 Handle 供后续操作

---

## 📨 `pass` — 异步消息发送

`pass` 向 Actor 发送消息，不阻塞当前执行。

### 语法

```nexa
pass handle, message;
pass handle, "消息内容";
```

### 示例

```nexa
agent Worker {
    prompt: "处理任务"
}

flow main {
    worker = spawn Worker("ready");
    
    // 异步发送多个任务
    pass worker, "任务 1";
    pass worker, "任务 2";
    pass worker, "任务 3";
    
    // 等待最终结果
    result = await worker;
}
```

---

## ⏳ `await` — 同步等待结果

`await` 阻塞等待 Actor 完成并获取结果。

### 语法

```nexa
result = await handle;
result = await handle, timeout;  // 带超时（秒）
```

### 示例

```nexa
flow main {
    worker = spawn LongRunningTask("start");
    
    // 等待最多 30 秒
    result = await worker, 30;
    
    if result == timeout {
        print("Task timed out");
    } else {
        print("Result: " + result);
    }
}
```

---

## 📥 `receive` — Actor 内部消息接收

在 Actor 内部从邮箱接收消息。

### 语法

```nexa
msg = receive();
msg = receive(timeout);  // 带超时
```

### 示例

```nexa
agent MessageProcessor {
    prompt: "处理接收到的消息"
}

flow main {
    processor = spawn MessageProcessor("start");
    
    // 发送消息
    pass processor, "Hello";
    pass processor, "World";
    
    // Actor 内部会依次 receive 并处理
    result = await processor;
}
```

---

## 🎯 DAG 管道与 Actor 结合

Actor 可以与 DAG 操作符 `|>>` 结合，实现复杂的并发编排。

### 示例：Fan-out / Fan-in

```nexa
agent Researcher {
    prompt: "研究主题"
}

agent Synthesizer {
    prompt: "综合多个研究结果"
}

flow main {
    topic = "量子计算应用";
    
    // Fan-out: 并行启动多个研究 Actor
    researchers = topic |>> [
        spawn Researcher("角度 A"),
        spawn Researcher("角度 B"),
        spawn Researcher("角度 C")
    ];
    
    // Fan-in: 等待所有结果并综合
    final = researchers &>> Synthesizer;
    
    print(final);
}
```

---

## 🔄 Actor 生命周期

```
spawn
  │
  ▼
┌─────────────┐
│   Running   │ ◄── pass (接收消息)
└─────────────┘
  │
  ├── 完成 ──► Completed
  │
  ├── 错误 ──► Failed
  │
  └── 超时 ──► Timeout
```

### 状态说明

| 状态 | 说明 |
|------|------|
| `running` | Actor 正在运行 |
| `completed` | Actor 正常完成 |
| `failed` | Actor 发生错误 |
| `timeout` | Actor 执行超时 |

---

## 📊 最佳实践

### 1. 合理设置超时

```nexa
// 推荐：为长时间任务设置超时
result = await worker, 300;  // 5 分钟超时

// 避免：无限等待
result = await worker;  // ❌ 可能永久阻塞
```

### 2. 错误处理

```nexa
flow main {
    worker = spawn RiskyTask("start");
    
    try_agent {
        result = await worker;
    } catch_correction(e: ActorError) {
        reflect "Actor 失败：#{e}，启动备用 Actor";
        backup = spawn BackupTask("start");
        result = await backup;
    }
}
```

### 3. 资源管理

```nexa
// 推荐：限制并发 Actor 数量
max_concurrent = 10;
actors = [];

for each task in task_list {
    if actors.length >= max_concurrent {
        // 等待一个完成
        completed = await actors[0];
        actors = actors[1:];
    }
    actors.append(spawn Worker(task));
}
```

---

## 🆚 Actor vs DAG 操作符

| 特性 | Actor (`spawn/await`) | DAG (`|>>/&>>`) |
|------|----------------------|-----------------|
| 执行模型 | 独立线程 | 协程/异步 |
| 状态隔离 | 完全隔离 | 共享上下文 |
| 消息传递 | 显式 `pass` | 隐式管道 |
| 适用场景 | 长时间任务、需要隔离 | 快速流水线、数据流 |

### 选择建议

- **使用 Actor**：任务需要长时间运行、需要状态隔离、需要动态消息传递
- **使用 DAG**：任务快速完成、数据流清晰、需要简洁语法

---

## 📚 相关文档

- [Harness 六元组](part2_harness.md) — E/T/C/S/L/V 运行时原语
- [高级特性](part2_advanced.md) — 管道、DAG、意图路由
- [基础语法](part1_basic.md) — Agent、Flow、Protocol 基础
