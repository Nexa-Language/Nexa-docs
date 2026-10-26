"""Validate registered examples, bilingual coverage, provenance, and built links."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml


@dataclass(frozen=True)
class CodeBlock:
    index: int
    line: int
    source: str


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def extract_examples(markdown: str) -> list[CodeBlock]:
    blocks: list[CodeBlock] = []
    for match in re.finditer(r"^(`{3,}|~{3,})(?:nexa|nx)[^\n]*\n(.*?)^\1\s*$", markdown, re.MULTILINE | re.DOTALL):
        blocks.append(CodeBlock(len(blocks) + 1, markdown[:match.start(2)].count("\n") + 1, match[2]))
    return blocks


def read_examples(root: Path) -> dict[tuple[str, int], CodeBlock]:
    return {(str(page.relative_to(root / "docs")), block.index): block
            for page in sorted((root / "docs").rglob("*.md")) for block in extract_examples(page.read_text())}


def check_pages(root: Path, inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    actual = {str(path.relative_to(root / "docs")) for path in (root / "docs").rglob("*.md")}
    pages = {page["path"]: page for page in inventory["pages"]}
    capabilities = {entry["id"] for entry in inventory["capabilities"]}
    for path in sorted(actual - pages.keys()):
        errors.append(f"unregistered page: {path}")
    errors.extend(f"preserved route missing: {path}" for path in inventory.get("preserved_pages", []) if path not in actual)
    for path, page in pages.items():
        if path not in actual:
            errors.append(f"missing page: {path}")
        else:
            markdown = (root / "docs" / path).read_text()
            metadata = yaml.safe_load(markdown.split("---", 2)[1]) if markdown.startswith("---\n") else {}
            if not isinstance(metadata, dict) or metadata.get("capabilities") != page["capabilities"]:
                errors.append(f"page capability metadata differs from inventory: {path}")
            if not isinstance(metadata, dict) or metadata.get("language_versions") != page.get("language_versions"):
                errors.append(f"page version metadata differs from inventory: {path}")
        translated = path.removesuffix(".en.md") + ".md" if path.endswith(".en.md") else path.removesuffix(".md") + ".en.md"
        if translated not in actual:
            errors.append(f"missing translation: {translated}")
        elif translated in pages and page["capabilities"] != pages[translated]["capabilities"]:
            errors.append(f"translation capability mismatch: {path}")
        if translated in pages and page.get("language_versions") != pages[translated].get("language_versions"):
            errors.append(f"translation version mismatch: {path}")
        expected_language = "en" if path.endswith(".en.md") else "zh"
        if page["language"] != expected_language:
            errors.append(f"incorrect language: {path}")
        if not page["capabilities"] or not set(page["capabilities"]).issubset(capabilities):
            errors.append(f"missing/unknown capability provenance: {path}")
    return errors


def check_example_contract(item: dict[str, Any], source: str, label: str) -> list[str]:
    errors: list[str] = []
    declaration = re.match(r'\s*(?://[^\n]*\n\s*)*language\s+"([^"]+)"', source)
    version = declaration[1] if declaration else "2.4"
    if item.get("language_version") != version:
        errors.append(f"language version differs from source: {label}")
    validation = item.get("validation")
    allowed = {"2.4": {"compile", "offline"}, "3.0": {"nativecheck", "oci"}}
    if validation not in allowed.get(version, set()):
        errors.append(f"{version} example requires {'nativecheck or oci' if version == '3.0' else 'compile or offline'}: {label}")
    claim = item.get("claim")
    if claim not in {"check", "execute"}:
        errors.append(f"example needs an explicit check/execute claim: {label}")
    if claim == "execute" and validation not in {"offline", "oci"}:
        errors.append(f"execution claim requires an actual scenario: {label}")
    if validation in {"offline", "oci"} and (claim != "execute" or not isinstance(item.get("scenario"), dict)):
        errors.append(f"{validation} scenario required with execute claim: {label}")
    if validation == "oci":
        scenario = item.get("scenario", {})
        if (scenario.get("kind") != "build-replay" or not isinstance(scenario.get("expected_outputs"), dict)
                or not scenario.get("expected_outputs") or type(scenario.get("model_calls")) is not int or scenario["model_calls"] < 0):
            errors.append(f"OCI scenario requires build-replay, nonempty expected_outputs and model_calls: {label}")
    return errors


def check_example_translations(registered: dict[tuple[str, int], dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for (page, block), item in registered.items():
        translated = page.removesuffix(".en.md") + ".md" if page.endswith(".en.md") else page.removesuffix(".md") + ".en.md"
        other = registered.get((translated, block))
        fields = ("language_version", "validation", "claim", "status", "scenario")
        if other is None or any(item.get(field) != other.get(field) for field in fields):
            errors.append(f"translation example contract mismatch: {page}#{block}")
    return errors


def check_inventory(root: Path, inventory: dict[str, Any]) -> list[str]:
    errors = check_pages(root, inventory)
    actual = read_examples(root)
    registered = {(item["page"], item["block"]): item for item in inventory["examples"]}
    for key in sorted(actual.keys() - registered.keys()):
        errors.append(f"unregistered example: {key[0]}#{key[1]}")
    for key, item in registered.items():
        label = f"{key[0]}#{key[1]}"
        if key not in actual:
            errors.append(f"missing example: {label}")
            continue
        if digest(actual[key].source) != item["sha256"]:
            errors.append(f"example changed: {label}; review and update its evidence")
        if item["status"] == "complete":
            errors.extend(check_example_contract(item, actual[key].source, label))
        elif item["status"] in {"partial", "historical"}:
            if not item.get("reason") or len(item["reason"].strip()) < 20:
                errors.append(f"specific reason required: {label}")
            if item.get("reason", "") not in (root / "docs" / key[0]).read_text():
                errors.append(f"example reason must also be visible on page: {label}")
        else:
            errors.append(f"invalid example status: {label}")
    errors.extend(check_example_translations(registered))
    for field, entries in (("example id", [item["id"] for item in inventory["examples"]]),
                           ("example location", [f'{item["page"]}#{item["block"]}' for item in inventory["examples"]]),
                           ("page", [item["path"] for item in inventory["pages"]])):
        errors.extend(f"duplicate {field}: {key}" for key, count in Counter(entries).items() if count > 1)
    return errors


def check_runtime_checkout(runtime: Path, baseline: dict[str, Any]) -> list[str]:
    try:
        head, tree = subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD", "HEAD^{tree}"],
                                             text=True, stderr=subprocess.DEVNULL).splitlines()
        dirty = bool(subprocess.check_output(["git", "-C", str(runtime), "status", "--porcelain", "--untracked-files=all"],
                                             text=True, stderr=subprocess.DEVNULL).strip())
    except (OSError, subprocess.CalledProcessError, ValueError):
        return ["runtime is not a readable Git checkout"]
    errors: list[str] = []
    if baseline.get("dirty") is not False:
        errors.append("runtime documentation baseline must be clean; review and refresh after committing")
    if head not in {baseline["git_head"], baseline.get("verification_checkout_head")}:
        errors.append("runtime commit differs from the pinned or explicitly recorded verification checkout")
    if tree != baseline.get("source_tree"):
        errors.append("runtime source tree differs from the documentation baseline")
    if dirty:
        errors.append("runtime worktree is dirty; commit or isolate changes before validating the pinned baseline")
    return errors


def check_provenance(runtime: Path, inventory: dict[str, Any]) -> list[str]:
    errors = check_runtime_checkout(runtime, inventory["runtime"])
    if (runtime / "VERSION").read_text().strip() != inventory["runtime"]["version"]:
        errors.append("runtime version differs from the documentation baseline")
    for capability in inventory["capabilities"]:
        if not capability.get("provenance"):
            errors.append(f'no provenance: {capability["id"]}')
        for source in capability["provenance"]:
            path = (runtime / source["path"]).resolve()
            if not path.is_relative_to(runtime.resolve()) or not path.is_file():
                errors.append(f'missing provenance source: {source["path"]}')
                continue
            text = path.read_text()
            if digest(text) != source["sha256"]:
                errors.append(f'provenance changed: {capability["id"]}: {source["path"]}; re-audit claims before refreshing')
            if source.get("symbol") and source["symbol"] not in text:
                errors.append(f'provenance symbol missing: {source["path"]}: {source["symbol"]}')
    return errors


def nav_paths(value: object) -> set[str]:
    if isinstance(value, str):
        return {value} if value.endswith(".md") else set()
    if isinstance(value, list):
        return set().union(*(nav_paths(item) for item in value))
    if isinstance(value, dict):
        return set().union(*(nav_paths(item) for item in value.values()))
    return set()


def check_navigation(root: Path, inventory: dict[str, Any]) -> list[str]:
    config = yaml.safe_load((root / "mkdocs.yml").read_text())
    paths = nav_paths(config["nav"])
    actual = {page["path"] for page in inventory["pages"] if page["language"] == "zh"}
    errors = [f"navigation page missing: {path}" for path in sorted(paths - actual)]
    errors.extend(f"page absent from navigation: {path}" for path in sorted(actual - paths))
    for kind in ("extra_css", "extra_javascript"):
        errors.extend(f"missing configured asset: {path}" for path in config.get(kind, []) if not (root / "docs" / path).is_file())
    for path in (root / "docs").rglob("*.css"):
        for target in re.findall(r"url\(['\"]?([^'\")]+)", path.read_text()):
            if not urlsplit(target).scheme and not (path.parent / target).is_file():
                errors.append(f"missing CSS asset: {path.relative_to(root)} -> {target}")
    return errors


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = {"top"}
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value is None:
                continue
            if key in {"id", "name"}:
                self.ids.add(value)
            if key in {"href", "src"} and value:
                self.targets.append(value)


def check_site(site: Path) -> list[str]:
    site = site.resolve()
    pages: dict[Path, Links] = {}
    errors: list[str] = []
    for path in site.rglob("*.html"):
        links = Links()
        links.feed(path.read_text())
        pages[path] = links
    if not pages:
        return [f"no built pages found: {site}"]
    for page, links in pages.items():
        for target in links.targets:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            resolved = ((site / path.lstrip("/")) if path.startswith("/") else (page.parent / path) if path else page).resolve()
            if not resolved.is_relative_to(site):
                errors.append(f"link escapes site: {page.relative_to(site)} -> {target}")
                continue
            if resolved.is_dir():
                resolved /= "index.html"
            if not resolved.is_file():
                errors.append(f"missing link target: {page.relative_to(site)} -> {target}")
            elif url.fragment and resolved in pages and unquote(url.fragment) not in pages[resolved].ids:
                errors.append(f"missing link anchor: {page.relative_to(site)} -> {target}")
    return sorted(set(errors))


def probe_environment(directory: Path) -> dict[str, str]:
    home = directory / "home"
    temporary = directory / "tmp"
    home.mkdir()
    temporary.mkdir()
    return {"HOME": str(home), "TMPDIR": str(temporary), "PATH": os.defpath, "LANG": "C.UTF-8",
            "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1", "NEXA_QUIET": "1"}


def run_examples(root: Path, runtime: Path, python: Path, inventory: dict[str, Any], *, oci: bool = False) -> dict[str, object]:
    actual = read_examples(root)
    examples = [{**item, "source": actual[(item["page"], item["block"])].source}
                for item in inventory["examples"] if item["status"] == "complete"]
    with tempfile.TemporaryDirectory(prefix="nexa-docs-check-") as temporary:
        manifest = Path(temporary) / "examples.json"
        manifest.write_text(json.dumps(examples))
        environment = probe_environment(Path(temporary))
        command = [str(python), str(root / "scripts/runtime_probe.py"), str(runtime), str(manifest)]
        if oci:
            docker = shutil.which("docker")
            if not docker:
                raise RuntimeError("OCI validation requires Docker")
            endpoint = subprocess.check_output([docker, "context", "inspect", "--format", "{{.Endpoints.docker.Host}}"], text=True).strip()
            if not endpoint.startswith("unix://"):
                raise RuntimeError("Documentation OCI validation requires a local Unix Docker endpoint")
            environment["DOCKER_HOST"] = endpoint
            command.extend(["--oci", docker])
        result = subprocess.run(command, cwd=temporary, env=environment, capture_output=True, text=True, timeout=600 if oci else 180, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def check_stdlib(root: Path, runtime: Path, python: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="nexa-docs-stdlib-") as temporary:
        environment = {**probe_environment(Path(temporary)), "PYTHONPATH": str(root)}
        result = subprocess.run([str(python), "-m", "scripts.export_stdlib", "--runtime", str(runtime), "--check"],
                                cwd=temporary, env=environment, capture_output=True, text=True, timeout=60, check=False)
    return [result.stderr or result.stdout] if result.returncode else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, help="Explicit clean pinned Nexa 3.0 checkout")
    parser.add_argument("--runtime-python", type=Path, help="Interpreter with Nexa dependencies; defaults to runtime/.venv/bin/python")
    parser.add_argument("--site", type=Path, help="Check built HTML links and fragments")
    parser.add_argument("--oci", action="store_true", help="Execute registered 3.0 scenarios and locked replay in real OCI")
    parser.add_argument("--report", type=Path, default=Path(".reports/docs-check.json"))
    args = parser.parse_args()
    if args.oci and not args.runtime:
        parser.error("--oci requires --runtime")
    root = Path(__file__).resolve().parents[1]
    inventory = json.loads((root / "docs/inventory.json").read_text())
    errors = check_inventory(root, inventory) + check_navigation(root, inventory)
    report: dict[str, object] = {"pages": len(inventory["pages"]), "registered_examples": len(inventory["examples"]), "runtime_validation": "not_requested"}
    if args.site:
        errors.extend(check_site(args.site))
    if args.runtime:
        runtime = args.runtime.resolve()
        errors.extend(check_provenance(runtime, inventory))
        if not errors:
            # Resolving a venv's interpreter symlink would discard its installed packages.
            python = (args.runtime_python or runtime / ".venv/bin/python").absolute()
            try:
                runtime_report = run_examples(root, runtime, python, inventory, oci=args.oci)
                report["runtime_validation"] = runtime_report
                runtime_errors = runtime_report.get("errors")
                if not isinstance(runtime_errors, list):
                    raise TypeError("Invalid probe report: expected an errors array")
                errors.extend(str(error) for error in runtime_errors)
                errors.extend(check_stdlib(root, runtime, python))
            except (OSError, RuntimeError, TypeError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
                errors.append(f"runtime check failed: {error}")
    report.update({"status": "failed" if errors else "passed", "errors": errors})
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
