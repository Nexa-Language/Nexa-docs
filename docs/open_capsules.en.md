---
title: "Capsules: reuse with conditions"
capabilities: [open_capsules, open_evidence]
language_versions: ["3.0"]
---

# Capsules: reuse with conditions

A capsule preserves an implementation, provenance, license, contract conditions, capabilities, dependencies, and evidence. A receiving task selects it explicitly; the runtime matches and admits it again. New inputs create new verification obligations.

```sh
uv run nexa open capsule export repair.capsule.json --activity ACTIVITY_ID --source local-repository --creator local-operator --license MIT --state .nexa/maintain.db
uv run nexa open capsule import repair.capsule.json --state .nexa/second.db
```

Use `ACTIVITY_ID` from the actual completed activity. Import returns a capsule ID. Add `--capsule CAPSULE_ID` to a new `nexa run` command to select it. Explicit source implementations take precedence and require an exactly matching capsule implementation. Open implementations may select another compatible candidate.

## Reuse decisions

File hashes verify integrity; the local trusted evidence registry decides which results can be reused. Contracts, capabilities, original provenance, and dependency conditions all participate in matching. A new task retains the original implementation conditions; removing conditions from an import breaks matching or integrity.

Candidate reuse can avoid generation requests. The current task still checks inputs and evidence against policy. Mutable model aliases require review in another task, and human authorization does not transfer with a capsule. An accepted reused artifact still requires an exact grant for the current write proposal.

Locked artifact replay preserves a lock and object database. Cross-task capsule reuse preserves provenance and verifiable conditions. Inspect each path's results and evidence through [acceptance](open_evidence.md).

---

[Source and validation](capability_inventory.md) · `open_capsules` / `open_evidence`
