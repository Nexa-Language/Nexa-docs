---
title: "Development toolchain"
capabilities: [ecosystem, cli, conversations]
---

# Development toolchain

Three developer entry points share Nexa's contracts: the CLI executes programs, Nexa Code performs coding tasks, and VS Code supplies editing and diagnostics. Current 2.4 integrations target a local development checkout.

## CLI

Follow [Quickstart](quickstart.md) for Python 3.10+, uv, and local Nexa. `validate --json`, `inspect --format json`, and `agent` provide diagnostics, structure, and durable execution respectively.

## Nexa Code

The [Nexa-Code repository](https://github.com/Nexa-Language/Nexa-Code) provides the Ink/React terminal assistant. Use that checkout's README to link the development runtime, then validate reads, writes, approvals, cancellation, and recovery in a separate workspace. Its runtime entries are `execute`, `continue_run`, and checkpoints; see [Conversations](runtime_conversations.md).

## VS Code

The [Nexa-extension repository](https://github.com/Nexa-Language/Nexa-extension) maintains editor integration. Development and packaging require Node.js 22+ and pnpm; the VS Code API baseline is 1.96. Install the local VSIX and configure the verified Nexa CLI path using the extension README.

Structured `inspect` declarations include `source: {file, line, column, end_line, end_column}`. Positions are 1-based and ends are exclusive. Included declarations retain their original file. Editors display diagnostics when source spans are unavailable.

## Release status

Installation currently uses explicit local paths. Public CLI, Nexa Code, and VSIX releases need independent versioning, packaging, and release acceptance. A public 2.4 release reference is still pending.

---

[Source and validation](capability_inventory.md) · `ecosystem` / `cli` / `conversations`
