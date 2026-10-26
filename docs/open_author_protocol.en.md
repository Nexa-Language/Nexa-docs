---
title: "Author protocol and source synchronization"
capabilities: [open_author, open_revisions]
language_versions: ["3.0"]
---

# Author protocol and source synchronization

Author 3.0 transports newline-delimited JSON-RPC 2.0 over stdin/stdout. Each frame is limited to 2 Mi characters; oversized frames are drained before the next request. Initialize first to read the protocol version and `max_inflight`. Each server allows at most two concurrent author resolutions.

```sh
uv run nexa author --state .nexa/author.db --environment examples/open_programs/offline.json
```

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocol_version":"3.0","client":"editor"}}
```

Requests carry an integer/string/null `id`. Notifications omit it and have no response. Correlate replies by ID and recover events using the monotone cursor from `events/read`.

| Method | Key parameters / result |
| --- | --- |
| `program/check` | source, optional path → CheckReport, diagnostics, obligations |
| `revision/propose` | source, program_id, nullable expected_revision → draft revision |
| `goal/resolve` | program_id, expected_revision, goal, optional input_json/budget → activity_id |
| `activity/read` / `activity/cancel` | object_id → author activity and durable cancellation state |
| `author/answer` | program_id, expected_revision, request_id, answer → clarified child revision |
| `events/read` | program_id, optional after → durable events |
| `evidence/explain` | object_id, optional context → evidence and validity |

`goal/resolve` returns an author activity ID promptly; poll until terminal. Its result belongs to author resolution. CLI/ProgramSession builds and activates a source draft; SDK/`nexa open` manages runtime activities.

## Synchronize clarification back to source

`author/answer` requires the exact clarification ID and current draft revision. After answering, the client reads the real new IR, displays the target intent change as a diff, and marks source synchronization pending. Confirmation still requires the original source digest/document version before writing, checking again, and synchronizing with exact draft CAS.

Concurrent source edits preserve both the newer edit and pending draft. Declining synchronization or exiting also preserves the pending state. Block build/run from the old file until synchronization completes. The next build then uses the clarification the user actually approved.

## Errors and identity

Domain codes are in `error.data.code`, including `revision_conflict`, `model_unavailable`, `author_busy`, and `activity_missing`. JSON-RPC codes are `-32600` for envelopes, `-32602` for parameters, `-32601` for unknown methods, and `-32000` for domain failures. Provider errors expose a sanitized failure kind.

The local Author endpoint serves trusted human/Agent clients. Display diagnostics, author activity, active runtime revision, evidence validity, and pending patch authorization with separate identities. Read the packaged schema with `uv run nexa open schema author-protocol`.

---

[Source and validation](capability_inventory.md) · `open_author` / `open_revisions`
