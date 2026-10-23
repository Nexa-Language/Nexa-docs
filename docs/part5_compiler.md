---
title: "统一编译入口"
capabilities: [compilation]
---

# 统一编译入口

`compile_file` 与 `compile_source` 是 CLI、SDK 和嵌入式 API 共用的编译入口。inspect/validate 也使用同一模块加载器。

## 编译管线

`.nx` 与 include → 解析及来源位置 → 规范化 AST → Harness 诊断 → Python 生成物 → Python 语法检查。

```python
from src.compiler import compile_file

compilation = compile_file("hello.nx", harness_mode="warn")
print(compilation.sources)
print(compilation.python_code)
```

示例依赖[快速入门](quickstart.md)的 `hello.nx`。`Compilation` 包含 `python_code`、`ast`、`sources` 和 `diagnostics`；编译失败抛出 `CompilationError`。

## 模块与位置

include 先相对导入文件解析，再查包内标准库。同一规范路径只导入一次；循环依赖诊断显示路径链。Harness 嵌套节点与 include 文件保留自己的来源路径、行和列。

声明模块可以独立编译。生成物返回成功前会由 Python AST parser 检查语法。运行时错误仍通过执行状态和异常传播。

## 集成建议

编辑器以 JSON 诊断标记 Problems，调用方保持原始路径与 source span。实际工具行为和 provider 请求由运行时处理；编译不需要模型凭据。支持示例由主仓库 `examples/manifest.json` 登记并由 `tests/test_examples.py` 编译验证。

---

[来源与验证](capability_inventory.md) · `compilation`
