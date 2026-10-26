---
title: Capability and example evidence
capabilities:
- compilation
- verification
- open_language
- open_execution
- open_evidence
language_versions:
- '3.0'
- '2.4'
---

# Capability and example evidence

This site pins released [Nexa v3.0.0 source](https://github.com/Nexa-Language/Nexa/commit/274379606e53c90d2d25774f6bb8984c777d0759): commit `274379606e53c90d2d25774f6bb8984c777d0759`, Git tree `b090cc6503ea70318667031925480e36c352a913`. Machine-readable [inventory.json](inventory.json) stores source/test symbols, whole-file SHA-256 fingerprints, runtime version, and review records.

## Verify language and claims

The inventory contains **104 pages, 52 Chinese/English pairs, and 68 complete Nexa examples**. All 84 previous page paths are preserved. The 62 legacy examples compile through the 3.0 compatibility runtime, with 40 checking actual offline behavior. Six 3.0 blocks pass native contract checking; four register OCI builds and locked replay (two in each language).

| Mode | Language and actual check |
| --- | --- |
| `compile` | 2.4: actual `compile_source`, Python lowering and syntax validation |
| `offline` | 2.4: compile and execute SDK/tools/flows; compare outputs, errors, request counts, or mailbox order |
| `nativecheck` | 3.0: native `compile_program` and CheckReport validation, no model requests or subprocesses |
| `oci` | 3.0: nativecheck, actual pinned-image execution, outputs and evidence, then zero-request locked replay |

Every complete example declares `language_version`, a check/execute `claim`, and its validation mode. Execution claims require an actual scenario. A 3.0 execution scenario specifies expected_outputs, model_calls, and build-replay. Translations share language versions, validation modes, and scenarios. Offline-only runs list `oci_deferred` accurately; explicit OCI verification records real execution.

## Provenance and isolation

Verification requires a clean checkout, exact commit, full Git tree, file hashes, and symbols. Staged, unstaged, and non-ignored new files fail the gate. This upgrade re-audits changed compiler, CLI, provider, manifest, example tests, README, and dependency configuration. Retained 2.4 semantics execute against the 3.0 package.

Subprocesses have temporary HOME/TMPDIR and a minimal environment without inherited provider credentials. Python networking and `.nxs` reads are blocked before runtime import. Fixtures supply fixed model replies; execution and acceptance use the actual runtime. OCI uses a local Docker Unix socket and pinned digest, with candidate network=none. Reports include artifact digests, outputs, and each evidence digest.

Review changed source, explanations, and expectations before refreshing fingerprints. Partial/historical blocks need visible, specific reasons. Strict MkDocs builds and HTML link/anchor/asset checks cover both languages. [stdlib-api.json](stdlib-api.json) is compared against the actual compatibility registry. See the [README](https://github.com/Nexa-Language/Nexa-docs) for commands and CI gates.
