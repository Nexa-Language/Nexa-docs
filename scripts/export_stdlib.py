"""Generate parameter references from the selected runtime's real tool registry."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Any

from scripts.runtime_probe import install_guards


def snapshot(runtime: Path) -> dict[str, list[dict[str, Any]]]:
    sys.path.insert(0, str(runtime.resolve()))
    module = importlib.import_module("src.runtime.stdlib")
    registry = module.get_stdlib_tools()
    return {namespace: [{"name": name, "parameters": registry[name].parameters, "description": registry[name].description,
                        "return_annotation": return_annotation(registry[name].handler)}
                        for name in names if name in registry] for namespace, names in module.STD_NAMESPACE_MAP.items()}


def return_annotation(handler: object) -> str:
    if not callable(handler):
        raise TypeError("Registered tool handler must be callable")
    annotation = inspect.signature(handler).return_annotation
    if annotation is inspect.Signature.empty:
        return "unspecified"
    return annotation if isinstance(annotation, str) else getattr(annotation, "__name__", str(annotation))


def reference(data: dict[str, list[dict[str, Any]]], language: str) -> str:
    english = language == "en"
    title = "Standard library API" if english else "标准库 API"
    introduction = (
        "This reference is generated from Nexa 3.0's retained 2.4 tool registry. Names below are exact registry identifiers. "
        "Expose a namespace with `uses std.fs`, or call supported DSL wrappers such as `std.fs.read(path)`. "
        "Required and optional parameters describe the JSON tool interface. Return types are the registered handler's annotations; `unspecified` means no annotation is declared. "
        "See the full [schema snapshot](stdlib-api.json) for property descriptions."
        if english else
        "本页从 Nexa 3.0 保留的 2.4 工具注册表生成。下列名称为准确的注册表标识符。用 `uses std.fs` 暴露 namespace，"
        "或调用受支持的 DSL 包装器，例如 `std.fs.read(path)`。必填与可选参数描述工具 JSON 接口；返回类型采用注册 handler 的注解，"
        "`unspecified` 表示该 handler 未声明返回注解。字段说明见完整的 [schema 快照](stdlib-api.json)。"
    )
    policy = (
        "## Execution and errors\n\nAgent-dispatched tools check exposure and approval before execution. Direct standard-library calls run as trusted program code. "
        "Filesystem mutation is disabled by default in the legacy standard-library layer; "
        "its `NEXA_ENABLE_DANGEROUS_TOOLS` and `NEXA_ALLOWED_WRITE_ROOTS` configuration is separate from Agent approval. Configure only reviewed, task-specific permissions. "
        "Regular handler failures may return an `Error:` string; uncertain transport failures propagate to preserve unknown-outcome recovery. "
        "Database handles and several collection results are JSON strings; explicitly decode them when local structured values are required. "
        "PostgreSQL and external services require their application dependencies. `std.ui` needs the `terminal` extra.\n"
        if english else
        "## 执行与错误\n\nAgent 发起的工具调用先检查暴露集与审批；直接标准库调用作为受信任程序代码执行。旧标准库层默认关闭文件系统修改；其 `NEXA_ENABLE_DANGEROUS_TOOLS` 与 "
        "`NEXA_ALLOWED_WRITE_ROOTS` 配置独立于 Agent 审批，应仅按已审核任务配置权限。普通 handler 失败可能返回 `Error:` 字符串；"
        "结果不确定的传输错误向上传播，保留未知结果恢复语义。数据库句柄与部分集合结果采用 JSON 字符串，需要本地结构化值时应显式解码。"
        "PostgreSQL 与外部服务需要应用依赖，`std.ui` 需要 `terminal` extra。\n"
    )
    compatibility = (
        '!!! note "2.4 compatibility in Nexa 3.0"\n    This API serves the 2.4 compatibility path. Open Programs use explicit capabilities and '
        '[controller-owned adapters](migration_30.md).\n'
        if english else
        '!!! note "Nexa 3.0 中的 2.4 兼容路径"\n    这些 API 服务于 2.4 兼容入口。Open Programs 使用显式 capabilities 与'
        '[控制器适配器](migration_30.md)。\n'
    )
    lines = [f'---\ntitle: "{title}"\ncapabilities: [stdlib, tools]\nlanguage_versions: ["2.4"]\n---\n\n{compatibility}\n# {title}\n\n{introduction}\n\n{policy}']
    for namespace, tools in data.items():
        lines += [f"\n## `{namespace}`\n", "| Registry name | Required parameters | Optional parameters | Return annotation |" if english else "| 注册表名称 | 必填参数 | 可选参数 | 返回注解 |", "| --- | --- | --- | --- |"]
        for tool in tools:
            schema = tool["parameters"]
            required = set(schema.get("required", []))
            groups = [[], []]
            for name, details in schema.get("properties", {}).items():
                value = f'`{name}: {details.get("type", "any")}`'
                if "enum" in details:
                    value += " (" + ", ".join(f"`{item}`" for item in details["enum"]) + ")"
                groups[0 if name in required else 1].append(value)
            returns = tool["return_annotation"].replace("|", "\\|")
            lines.append(f'| `{tool["name"]}` | {", ".join(groups[0]) or "—"} | {", ".join(groups[1]) or "—"} | `{returns}` |')
    lines += ["\n---\n", "[Source and validation](capability_inventory.md) · `stdlib` / `tools`\n" if english else "[来源与验证](capability_inventory.md) · `stdlib` / `tools`\n"]
    return "\n".join(lines)


def main() -> int:
    install_guards()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "docs"
    data = snapshot(args.runtime)
    outputs = {"stdlib-api.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
               "stdlib_reference.md": reference(data, "zh"), "stdlib_reference.en.md": reference(data, "en")}
    mismatches = []
    for name, content in outputs.items():
        path = root / name
        if args.check:
            if not path.exists() or path.read_text() != content:
                mismatches.append(name)
        else:
            path.write_text(content)
    if mismatches:
        print("Standard library reference drift: " + ", ".join(mismatches), file=sys.stderr)
    else:
        print(f"Standard library reference: {len(data)} namespaces, {sum(map(len, data.values()))} namespace tool entries")
    return bool(mismatches)


if __name__ == "__main__":
    sys.exit(main())
