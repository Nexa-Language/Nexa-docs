---
title: "Revisions, cancellation, and recovery"
capabilities: [open_revisions, open_author]
language_versions: ["3.0"]
---

# Revisions, cancellation, and recovery

Source drafts, active runtime revisions, author activities, and runtime activities have different identities. An edit becomes a draft, is built and admitted, then switches the runtime head. Existing activities keep their original source and artifact; new activities use the activated version.

## CAS revisions and activities

```sh
uv run nexa open revise program.nx --environment environment.json --state .nexa/program.db --program-id demo --expected-revision CURRENT_REVISION
uv run nexa open status demo --state .nexa/program.db
uv run nexa open cancel ACTIVITY_ID --environment environment.json --state .nexa/program.db
```

Read `CURRENT_REVISION` from the current draft and `ACTIVITY_ID` from the activity the user selected. On `revision_conflict`, refresh the real revision and show the conflict while preserving concurrent edits. `open status` returns RuntimeHead; ProgramSession/ProgramStore supplies full runtime activities and history. Author `activity/read` returns author activities.

Activities bind their revision and artifact digest. To recover a cross-process view, read durable program events, load RuntimeActivity objects referenced by those events, and refresh each by its original activity ID. List parallel activities individually; cancel only the selected ID.

## Controller recovery

```sh
uv run nexa open resume demo --environment environment.json --state .nexa/program.db
```

A live operation owner holds a kernel lock, so recovery returns `operation_busy`. Interrupted activities remain in history; clients explicitly start new activities after recovery. SQLite commits revisions, objects, and events in one transaction. Unknown schemas, unrelated databases, and objects with invalid content digests are rejected.

External effects use a `prepared` / `started` / `completed` journal. Idempotent adapters reuse the original operation key. Unknown non-idempotent outcomes require recorded reconciliation through `EffectJournal.reconcile`. New activities, activation, and patch application stay blocked until reconciliation finishes.

State schema migration executes a pure Candidate inside OCI and validates returned JSON against the target schema. Failure preserves the previous runtime head. Recover exact patch writes through the [patch journal](open_grants.md); recover legacy 2.4 checkpoints through the [compatibility workflow](runtime_checkpoints.md).

---

[Source and validation](capability_inventory.md) · `open_revisions` / `open_author`
