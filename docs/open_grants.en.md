---
title: "Exact patch authorization and application"
capabilities: [open_grants, open_evidence, open_revisions]
language_versions: ["3.0"]
---

# Exact patch authorization and application

Maintenance produces a PatchProposal with an exact diff, workspace baseline, policy, and evidence. After review, the user issues an ApprovalGrant and applies with that exact grant ID. Models, legacy 2.4 tool approvals, and old bypass settings cannot issue this authorization.

## From proposal to application

Create a temporary demonstration repository containing `calc.py`, where `add(a, b)` incorrectly returns subtraction. The released environment's frozen checks expect `5` and `-5`. The explicit operation below calls your configured model and executes candidates and regression checks inside OCI.

```sh
uv run nexa run examples/open_programs/maintain.nx --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db --program-id demo --repository /absolute/path/to/repository --include calc.py --request 'Fix calc.add to return the mathematical sum.' --json
uv run nexa open evidence PROPOSAL_ID --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db
uv run nexa open approve PROPOSAL_ID --actor local-operator --state .nexa/maintain.db
uv run nexa open apply PROPOSAL_ID --grant GRANT_ID --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db
```

Read the actual diff and each evidence record, then use the returned proposal/grant IDs exactly. A grant binds the proposal, path scope, baseline, policy, evidence, task, and expiry. Every apply revalidates them. `--actor` records the operator represented by a trusted local client; the local database is the trust boundary. Candidates cannot access it. External services provide multi-user authentication separately.

## Concurrent edits and interruption

Application checks baselines before and after writing. It first atomically moves each old file into a sibling `.nexa-preserved-*/original`, verifies its content, and exclusively creates the replacement. Deletion preserves the original too. The write-ahead journal's `preserved` field records the recovery path, and source snapshots exclude these internal directories.

On `workspace_conflict`, preserve and inspect user content, then propose again against the current workspace. After interruption:

```sh
uv run nexa open recover PROPOSAL_ID --state .nexa/maintain.db
uv run nexa open apply PROPOSAL_ID --grant GRANT_ID --environment examples/open_programs/maintain-aliyun.json --state .nexa/maintain.db --resume
```

Inspect recovery before resuming. Recovery recognizes completed writes and can restore a baseline interrupted after moving its original file. Successful application retains the original inode. Editor writes through an old file descriptor land in the recovery file, and later recovery reports differences. Users archive or clean recovery directories after review. Cross-file writes use a journal and storage proportional to changed content. Filename switches have a brief gap, so coordinate editors and builders during application.

---

[Source and validation](capability_inventory.md) · `open_grants` / `open_evidence` / `open_revisions`
