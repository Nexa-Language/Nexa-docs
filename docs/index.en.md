---
title: Overview
hide: [toc]
capabilities: [open_language, open_execution, open_evidence]
language_versions: ["3.0"]
---

<div class="nx-home" markdown="1">
<div class="nx-hero" markdown="1">
<div class="nx-intro" markdown="1">
<span class="nx-eyebrow">NEXA / OPEN PROGRAMS</span>

# Goals, grounded<br>in evidence.

Write a goal and its acceptance contract. Build implementations in an isolated runtime, inspect their evidence, and carry revisions forward.
{.nx-lead}

[Start building →](quickstart.md){.nx-button .nx-primary}
[Explore Open Programs](open_programs.md){.nx-button .nx-secondary}

<span class="nx-version">NEXA 3.0.0 · GOALS · EVIDENCE · REVISIONS</span>
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

## Write the goal. Keep the evidence.
</div>
<div class="nx-steps" markdown="1">
<div markdown="1">
<span class="nx-step">01 / DEFINE</span>

### Define the contract

Keep types, intent, capabilities, and frozen checks together in source.

[Write your first program →](quickstart.md)
</div>
<div markdown="1">
<span class="nx-step">02 / EXECUTE</span>

### Build with evidence

Resolve within a budget. Execute candidates in OCI and inspect each acceptance record.

[Understand acceptance →](open_evidence.md)
</div>
<div markdown="1">
<span class="nx-step">03 / INSPECT</span>

### Revise and recover

Track draft and active revisions. Cancel exact activities and reconcile unknown effects.

[Recover a task →](open_revisions.md)
</div>
</div>

<div class="nx-next" markdown="1">
<div markdown="1">
<span class="nx-eyebrow">FROM 2.4 TO 3.0</span>

### Keep your working path. Add Open Programs.

Existing 2.4 sources keep their compatibility path. Migrate source contracts and archive state explicitly.
</div>
[Read the migration guide →](migration_30.md){.nx-button .nx-secondary}
</div>

<div class="nx-ecosystem" markdown="1">
## A connected toolchain.

[**Nexa Code** · Coding tasks in the terminal ↗](toolchain.md)

[**VS Code** · Edit and inspect Nexa source ↗](toolchain.md)

[**Examples** · Complete programs with evidence →](examples.md)
</div>
</div>
