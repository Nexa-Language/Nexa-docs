---
title: "Open Programs: goals and contracts"
capabilities: [open_language, open_execution]
language_versions: ["3.0"]
---

# Open Programs: goals and contracts

An Open Program owns goals, optional implementations, acceptance requirements, and dependencies. Humans and author Agents write the same `.nx` contract; the native frontend checks type boundaries, duplicate clauses, and dependencies.

## A complete open goal

```nexa
language "3.0"
program Sum {
    goal total() -> Int {
        intent "Sum every integer in inputs.get('values', []); return zero for an empty list."
        capabilities [sandbox.exec]
        ensure checks.sum
        review model("Handle all integers, including negatives, without hardcoded case outputs.")
        implementation open
    }
}
```

Save it as `sum.nx` and run `uv run nexa check sum.nx --json`. The report contains one open obligation, `total`. Execution requires `checks.sum` and an authorized model binding in the environment. This site's fixture provider executes the example with a `solve(inputs)` implementation that sums `values` and returns `0` for empty input. Frozen extra cases cover positive and negative integers, and a model review is recorded separately. Build uses one implementation request and one review request; locked replay uses zero requests.

## Contract fields

| Field | Meaning |
| --- | --- |
| `goal name(arg: Type) -> Type` | Parameters require types; results pass a type boundary before use |
| `intent` | Nonempty task intent; clarification creates a child revision |
| `implementation open` | Leaves a resolution obligation |
| `implementation value <JSON>` | Supplies an explicit JSON literal |
| `implementation python "..."` | Calls `solve(inputs)` inside OCI; requires `sandbox.exec` |
| `ensure checks.name` | Selects a fixed check with that environment name |
| `review model("criterion")` | Requests an independent structured boolean review |
| `depends [name]` | DAG dependency; results enter `inputs["dependencies"]` |
| `stage runtime` | Resolves in an activity; the default stage is build |

Boundary types are Int, Float, String, Bool, Unit, Json, Patch, Repository, and ChangeRequest. A build goal cannot depend on a runtime goal. Each `ensure`/`review` must be unique within its kind; the automatic name `typecheck` is reserved.

## A repository maintenance contract

The released `examples/open_programs/maintain.nx` declares a Repository parameter, a runtime goal from ChangeRequest to Patch, and an `on change_request` handler. The handler uses `resolve`, then `propose repo.apply(result) requires human.approval`. Candidate resolution, regression checks, authorization, and workspace application have separate records.

Named environment, sandbox, and acceptance declarations select reference bindings. Actual requirements come from goal clauses and environment configuration. Native `compile_program` dispatches explicit versions; existing `compile_source`/`compile_file` retain 2.4 Python lowering.

Continue with [environments](open_environments.md), [evidence](open_evidence.md), and [exact authorization](open_grants.md).

---

[Source and validation](capability_inventory.md) · `open_language` / `open_execution`
