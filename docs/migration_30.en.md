---
title: "Migrate from 2.4 to 3.0"
capabilities: [open_migration, compilation, checkpoint]
language_versions: ["3.0", "2.4"]
---

# Migrate from 2.4 to 3.0

Nexa 3.0 accepts explicit `language "3.0"` Open Programs and existing 2.4 sources. A file without a language declaration retains the 2.4 path. `compile_source`/`compile_file` still return Python lowering; `compile_program` is version-aware. Existing pages and commands remain in the [compatibility quickstart](quickstart_24.md).

## Migrate source contracts

| 2.4 structure | 3.0 target |
| --- | --- |
| Pure function / computation | Typed goal, value or Python `solve(inputs)`, executed in OCI |
| Agent prompt | Intent, deterministic checks, separate review |
| Tool exposure / sandbox policy | Explicit capabilities and controller-owned adapters |
| `verify` / Protocol | Type boundary and frozen OutputCheck / RepositoryCheck |
| Sequential flow | Build/runtime goal DAG; results enter inputs.dependencies |
| Source edit during execution | Child revision → build → activation at a checkpoint |
| Approval before writing | PatchProposal / ApprovalGrant bound to exact baseline, policy, evidence |
| History reuse | Capsule with provenance, implementation conditions, and current validation |

The 3.0 maintenance subset supports Int/Float/String/Bool/Json/Unit and Patch/Repository/ChangeRequest. Arbitrary flow control, streaming callbacks, MCP sessions, dynamic tool imports, actors, distributed state, and framework integrations continue through 2.4 or require explicit adapters. Rust AVM retains its 2.4 subset. Source translation requires review of the task's acceptance contract; prompts and tool lists alone do not determine frozen checks.

## Archive legacy state

```sh
uv run nexa open migrate .nexa/runs.sqlite3 --target .nexa/open-archive.sqlite3
```

The destination must be a new path. SQLite opens the source with `mode=ro` in a read transaction, including committed WAL contents. Known RunState v1 rows become immutable LegacyRunArchive objects in a separate 3.0 database, preserving state and provenance. The report includes a logical snapshot digest, run IDs, object digests, and per-row errors. Unsupported schemas fail explicitly while preserving the source.

Archives are inert. They create no active Open Program, tool call, or new approval. `started` tool outcomes become `unknown_effects` with `resume_allowed=false`; reconcile them against the original tool/provider before starting new external work. Old approvals bind their original 2.4 calls; 3.0 patches require new exact grants.

Keep legacy checkpoints at their original paths and resume through `nexa agent ... --resume RUN_ID`. Migration of 3.0 runtime state executes a pure Candidate in OCI and validates the target JSON schema; failure preserves the previous runtime head. Track source revision CAS and active revision separately, as described in [revision and recovery](open_revisions.md).

## Upgrade clients and recover source synchronization

Keep the source, environment, state database, and `.nx.lock` when upgrading Code/extension. Existing Code `SourceSync` record formats and IDs remain compatible; a new separate write-intent supports filesystem recovery after process interruption. Also retain `.nexa-intent-<id>/` beside the source and use `/status` → `source_recovery` to find the exact paths. `original` retains the old inode, which an existing editor may still write to. Close the relevant editors and reconcile retained edits before archiving recovery directories. For an older interruption without a write-intent, follow `source_recovery_required` and manually restore the retained file. Source synchronization preserves LF/CRLF, comments, and valid parameters outside the replaced string.

Rebind through the client after changing an environment. Before execution, inspection, grants, apply, and related operations, Code checks the native semantic digest; formatting or key order changes with the same semantics are allowed. After semantic drift, restart Code, then rebuild and generate/review the relevant evidence. Extension Author binds a private snapshot and checks the original file contents before every actual RPC send, including queue dispatch. Changed contents or an unavailable file invalidate the old client; review configuration and explicitly start another Author operation. Automatic checks use a client without a provider. Inspect activity state for requests already sent, and use exact activity IDs for cancellation. See [Development toolchain](toolchain.md) for commands and recovery entry points.

---

[Source and validation](capability_inventory.md) · `open_migration` / `compilation` / `checkpoint`
