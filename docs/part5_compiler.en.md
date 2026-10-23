---
title: "The unified compiler"
capabilities: [compilation]
---

# The unified compiler

`compile_file` and `compile_source` are shared by the CLI, SDK, and embedded API. Inspect and validate use the same module loader.

## Compilation pipeline

`.nx` and includes → parse with source locations → normalize AST → Harness diagnostics → generate Python → check Python syntax.

```python
from src.compiler import compile_file

compilation = compile_file("hello.nx", harness_mode="warn")
print(compilation.sources)
print(compilation.python_code)
```

This example uses `hello.nx` from [Quickstart](quickstart.md). `Compilation` contains `python_code`, `ast`, `sources`, and `diagnostics`. Failures raise `CompilationError`.

## Modules and locations

Includes resolve relative to the importing file, then search the packaged standard library. Each canonical path is imported once. Cycle diagnostics show the path chain. Nested Harness nodes and included files retain their own source path, line, and column.

Declaration-only modules compile independently. Generated output passes Python AST syntax validation before compilation succeeds. Execution failures propagate through runtime state and exceptions.

## Integration guidance

Editors can map JSON diagnostics to Problems, preserving original paths and source spans. Runtime code handles tools and provider requests; compilation needs no model credentials. The main repository registers supported examples in `examples/manifest.json` and compiles them through `tests/test_examples.py`.

---

[Source and validation](capability_inventory.md) · `compilation`
