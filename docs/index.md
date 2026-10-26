---
title: 概览
hide: [toc]
capabilities: [open_language, open_execution, open_evidence]
language_versions: ["3.0"]
---

<div class="nx-home" markdown="1">
<div class="nx-hero" markdown="1">
<div class="nx-intro" markdown="1">
<span class="nx-eyebrow">NEXA / OPEN PROGRAMS</span>

# 目标可写，<br>结果有据。

写下目标与验收合同，在隔离运行时中构建实现，核对证据，再让程序持续修订。
{.nx-lead}

[开始使用 →](quickstart.md){.nx-button .nx-primary}
[了解 Open Programs](open_programs.md){.nx-button .nx-secondary}

<span class="nx-version">Nexa 3.0.0 · 目标 · 证据 · 修订</span>
</div>
<div class="nx-source" markdown="1">
<span class="nx-file">answer.nx <span>01 / SOURCE</span></span>

```nexa
language "3.0"
program Answer {
    goal answer() -> Int {
        intent "Return 42"
        implementation value 42
    }
}
```

<span class="nx-caption">.nx → check → build → evidence → replay</span>
</div>
</div>

<div class="nx-section-heading" markdown="1">
<span class="nx-eyebrow">THE DEVELOPMENT PATH</span>

## 写下目标，也保留完成的依据。
</div>
<div class="nx-steps" markdown="1">
<div markdown="1">
<span class="nx-step">01 / DEFINE</span>

### 定义目标合同

在源码中保留类型、意图、能力与冻结检查。

[编写第一个程序 →](quickstart.md)
</div>
<div markdown="1">
<span class="nx-step">02 / EXECUTE</span>

### 构建并检查证据

在预算内求解，在 OCI 中执行候选，逐项核对验收记录。

[理解验收证据 →](open_evidence.md)
</div>
<div markdown="1">
<span class="nx-step">03 / INSPECT</span>

### 修订并恢复任务

分别跟踪草稿与活动版本，取消准确活动，核对未知副作用。

[恢复任务 →](open_revisions.md)
</div>
</div>

<div class="nx-next" markdown="1">
<div markdown="1">
<span class="nx-eyebrow">FROM 2.4 TO 3.0</span>

### 保留已有路径，逐步迁移合同。

已有 2.4 源码继续走兼容入口；源码合同与历史状态分别迁移。
</div>
[阅读迁移指南 →](migration_30.md){.nx-button .nx-secondary}
</div>

<div class="nx-ecosystem" markdown="1">
## 从语言到工具。

[**Nexa Code** · 在终端执行编程任务 ↗](toolchain.md)

[**VS Code** · 编写与检查 Nexa 源码 ↗](toolchain.md)

[**可验证示例** · 从完整程序继续学习 →](examples.md)
</div>
</div>
