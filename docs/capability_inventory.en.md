---
title: "Capability and example evidence"
capabilities: [compilation, verification]
---

# Capability and example evidence

This site is verified against the [Nexa v2.4.0 source](https://github.com/Nexa-Language/Nexa/commit/c2162637236e4a73feea410c4183672411666521). Machine-readable [inventory.json](inventory.json) records the version, Git baseline, workspace status, and exact source/test symbols and SHA-256 fingerprints for each capability. The published tag `v2.4.0` has been checked against this commit; installation uses that release source.

## Three record types

| Record | Fields and purpose |
| --- | --- |
| Page | Path, language, capability IDs; Chinese/English pairs must match |
| Capability | Current/planned status, precise claim, source/test path and symbol, content hash |
| Example | Page, block index, code hash, complete/partial/historical status, compilation or offline mode |

Complete Nexa blocks compile through local `src.compiler.compile_source`. Representative programs execute in temporary workspaces with networking disabled and fixed model-boundary fixtures. SDK, tools, flows, and output validation use real implementations.

## Update policy

Register new blocks. Recompile changed code and refresh its hash. Fragments and historical drafts need individual visible explanations of missing dependencies or failure. When provenance changes, review affected claims before explicitly refreshing evidence.

Strict builds check Markdown and navigation. HTML checks cover internal targets, fragments, images, styles, and scripts. Language checks require a Chinese/English pair for every page. Generated standard-library schemas live in [stdlib-api.json](stdlib-api.json) and are compared with the actual registry.

Local and CI commands are in the [Nexa-docs README](https://github.com/Nexa-Language/Nexa-docs). External URL availability, real-model quality, and publication results require separate validation.

---

[Source and validation](capability_inventory.md) · `compilation` / `verification`
