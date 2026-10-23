---
title: Overview
hide: [toc]
capabilities: [language, execution, compilation]
---

<div class="nx-home" markdown="1">
<div class="nx-hero" markdown="1">
<div class="nx-intro" markdown="1">
<span class="nx-eyebrow">NEXA / LANGUAGE &amp; RUNTIME</span>

# Agents, written<br>in Nexa.

Define the tools. Shape the context. Control the run. Start with a complete program, then build an Agent you can inspect and resume.
{.nx-lead}

[Start building →](quickstart.md){.nx-button .nx-primary}
[Explore the language](reference.md){.nx-button .nx-secondary}

<span class="nx-version">NEXA 2.4.0 · INSPECTABLE, RECOVERABLE EXECUTION</span>
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

## From a program to a running system.
</div>
<div class="nx-steps" markdown="1">
<div markdown="1">
<span class="nx-step">01 / DEFINE</span>

### Write the goal and tools

Keep instructions, tool exposure, and control flow together in source.

[Write your first program →](quickstart.md)
</div>
<div markdown="1">
<span class="nx-step">02 / EXECUTE</span>

### Make the run explicit

Choose a protocol, set budgets, and review tools requiring approval.

[Understand execution →](runtime_execution.md)
</div>
<div markdown="1">
<span class="nx-step">03 / INSPECT</span>

### Keep the outcome visible

Read status and usage. Preserve checkpoints and settle unknown results.

[Recover a task →](runtime_checkpoints.md)
</div>
</div>

<div class="nx-next" markdown="1">
<div markdown="1">
<span class="nx-eyebrow">UPGRADING TO 2.4</span>

### Execution contracts, made concrete.

Review compilation, approval, conversation turns, and the Rust support boundary.
</div>
[Read the migration guide →](migration_24.md){.nx-button .nx-secondary}
</div>

<div class="nx-ecosystem" markdown="1">
## A connected toolchain.

[**Nexa Code** · Coding tasks in the terminal ↗](toolchain.md)

[**VS Code** · Edit and inspect Nexa source ↗](toolchain.md)

[**Examples** · Complete programs with evidence →](examples.md)
</div>
</div>
