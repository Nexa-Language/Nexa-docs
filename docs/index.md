---
title: 概览
hide: [toc]
capabilities: [language, execution, compilation]
---

<div class="nx-home" markdown="1">
<div class="nx-hero" markdown="1">
<div class="nx-intro" markdown="1">
<span class="nx-eyebrow">NEXA / LANGUAGE &amp; RUNTIME</span>

# 从意图，<br>到执行。

用同一种语言定义 Agent、工具与执行流程。从一个完整程序开始，逐步掌握可检查、可恢复的运行时。
{.nx-lead}

[开始使用 →](quickstart.md){.nx-button .nx-primary}
[浏览语言参考](reference.md){.nx-button .nx-secondary}

<span class="nx-version">Nexa 2.4.0 · 可检查、可恢复的执行</span>
</div>
<div class="nx-source" markdown="1">
<span class="nx-file">hello.nx <span>01 / SOURCE</span></span>

```nexa
agent Analyst {
    prompt: "Work from evidence."
    timeout: 120
}

flow main {
    result = Analyst.run("Explain.");
    verify result satisfies string;
}
```

<span class="nx-caption">.nx → compile → run → inspect</span>
</div>
</div>

<div class="nx-section-heading" markdown="1">
<span class="nx-eyebrow">THE DEVELOPMENT PATH</span>

## 写下程序，也掌握它的运行。
</div>
<div class="nx-steps" markdown="1">
<div markdown="1">
<span class="nx-step">01 / DEFINE</span>

### 写下目标与工具

在源码中保留任务指令、工具暴露集和控制流。

[编写第一个程序 →](quickstart.md)
</div>
<div markdown="1">
<span class="nx-step">02 / EXECUTE</span>

### 运行并控制过程

选择模型协议，设置运行预算，确认需要审批的操作。

[理解执行状态 →](runtime_execution.md)
</div>
<div markdown="1">
<span class="nx-step">03 / INSPECT</span>

### 查看状态与结果

查看状态与用量，保存 checkpoint，核实结果不确定的操作。

[恢复任务 →](runtime_checkpoints.md)
</div>
</div>

<div class="nx-next" markdown="1">
<div markdown="1">
<span class="nx-eyebrow">UPGRADING TO 2.4</span>

### 迁移到明确的执行契约。

核对编译、审批、连续对话和 Rust 支持范围的变化。
</div>
[阅读迁移指南 →](migration_24.md){.nx-button .nx-secondary}
</div>

<div class="nx-ecosystem" markdown="1">
## 从语言到工具。

[**Nexa Code** · 在终端执行编程任务 ↗](toolchain.md)

[**VS Code** · 编写与检查 Nexa 源码 ↗](toolchain.md)

[**可验证示例** · 从完整程序继续学习 →](examples.md)
</div>
</div>
