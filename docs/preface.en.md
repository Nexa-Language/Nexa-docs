---
title: Why Nexa
capabilities:
- open_language
- open_evidence
- open_revisions
language_versions:
- '3.0'
- '2.4'
---

# Why Nexa

Nexa 3.0 lets a program own goals, implementations, evidence, and revisions. Humans and models write the same `.nx` contract. The native compiler checks it, resolves implementations within a budget, and runs acceptance in OCI. Accepted results retain evidence; repository writes additionally require exact authorization.

Goals say what to achieve, frozen checks say how to decide, and persistent state records the current step. Source drafts and active runtime revisions are separate. Relevant dependency changes trigger validation; unknown external effects require reconciliation before recovery.

Start with a literal implementation in [Quickstart](quickstart.md), then learn model-assisted resolution through [open goals](open_programs.md). Existing Agent, tool, flow, Actor, and MCP applications retain the [2.4 compatibility path](quickstart_24.md). Migrate against the [source and state checklist](migration_30.md).
