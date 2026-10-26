---
title: "Evidence and acceptance"
capabilities: [open_evidence]
language_versions: ["3.0"]
---

# Evidence and acceptance

Each result has both an acceptance status and evidence validity. Policy requirements are frozen. Evidence binds the candidate, policy, checker, dependencies, task, issue time, and optional expiry.

| Record | Execution and decision |
| --- | --- |
| `typecheck` | Whether OCI output matches the return type; an automatic requirement in every policy |
| OutputCheck | Executes candidates on frozen JSON inputs and compares against host-held expectations |
| RepositoryCheck | Applies a typed Patch in fresh OCI, then checks fixed command exit codes and output |
| model_review | A separate model request returns a structured boolean and detail |
| ApprovalGrant | Independent user authorization to write the exact proposal |

A passing check covers its input and requirement. When a candidate changes repository tests, the controller's acceptance oracle still uses its original configuration. Model reviews and deterministic checks have separate accounting and records; interfaces should show both results and evidence state.

## Validity and updates

Revoked, expired, future-dated, dependency-incomplete evidence, or evidence bound to a different candidate/policy/input, becomes invalid. A newer failure in the same candidate, policy, and dependency context prevents an older success from satisfying the requirement. Different inputs retain their own contexts. Mutable model aliases require review in a new task; human decisions are task-bound.

Artifact admission, locked replay, patch authorization, and application revalidate through the runtime. Objects serialize source spans but exclude them from semantic digests. Source content has a separate hash; clients retain both identities.

```sh
uv run nexa open evidence PROPOSAL_ID --environment environment.json --state .nexa/program.db
```

Use the `PROPOSAL_ID` returned by the real run. Author `evidence/explain` instead accepts an evidence object ID and optional context. Preserve requirement names, failure details, object digests, and context when diagnosing a failure. Natural-language completion becomes a usable result through formal policy admission.

---

[Source and validation](capability_inventory.md) · `open_evidence`
