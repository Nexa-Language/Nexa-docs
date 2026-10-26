"""Behavior checks for the documentation gate, using intentionally broken fixtures."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from scripts.check_docs import check_inventory, check_provenance, check_site, digest, extract_examples, run_examples
from scripts.runtime_probe import execute_example


@pytest.fixture
def runtime_checkout(tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    (runtime / "VERSION").write_text("2.4.0\n")
    (runtime / "compiler.py").write_text("def compile_source(): pass\n")
    (runtime / "helper.py").write_text("VALUE = 1\n")
    subprocess.run(["git", "init", "-q", str(runtime)], check=True)
    subprocess.run(["git", "-C", str(runtime), "add", "."], check=True)
    subprocess.run(["git", "-C", str(runtime), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-qm", "Create fixture"], check=True)
    head, tree = subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD", "HEAD^{tree}"], text=True).splitlines()
    inventory = {"runtime": {"version": "2.4.0", "git_head": head, "source_tree": tree, "dirty": False},
                 "capabilities": [{"id": "compiler", "provenance": [{"path": "compiler.py", "symbol": "compile_source",
                                   "sha256": digest((runtime / "compiler.py").read_text())}]}]}
    return runtime, inventory


def test_runtime_checkout_matches_clean_pinned_baseline(runtime_checkout: tuple[Path, dict[str, Any]]) -> None:
    assert check_provenance(*runtime_checkout) == []


@pytest.mark.parametrize("change", ["tracked", "staged", "untracked"])
def test_runtime_checkout_rejects_changes_outside_provenance(runtime_checkout: tuple[Path, dict[str, Any]], change: str) -> None:
    runtime, inventory = runtime_checkout
    (runtime / ("extra.py" if change == "untracked" else "helper.py")).write_text("VALUE = 2\n")
    if change == "staged":
        subprocess.run(["git", "-C", str(runtime), "add", "helper.py"], check=True)
    assert any("worktree is dirty" in error for error in check_provenance(runtime, inventory))


def test_runtime_checkout_rejects_another_commit_with_the_same_version(runtime_checkout: tuple[Path, dict[str, Any]]) -> None:
    runtime, inventory = runtime_checkout
    (runtime / "helper.py").write_text("VALUE = 2\n")
    subprocess.run(["git", "-C", str(runtime), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-qam", "Change unlisted runtime behavior"], check=True)
    errors = check_provenance(runtime, inventory)
    assert any("commit differs" in error for error in errors)
    assert any("source tree differs" in error for error in errors)


def test_recorded_verification_commit_requires_the_exact_source_tree(runtime_checkout: tuple[Path, dict[str, Any]]) -> None:
    runtime, inventory = runtime_checkout
    subprocess.run(["git", "-C", str(runtime), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "--allow-empty", "-qm", "Equivalent reviewed checkout"], check=True)
    assert any("commit differs" in error for error in check_provenance(runtime, inventory))
    inventory["runtime"]["verification_checkout_head"] = subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD"], text=True).strip()
    assert check_provenance(runtime, inventory) == []
    inventory["runtime"]["source_tree"] = "0" * 40
    assert any("source tree differs" in error for error in check_provenance(runtime, inventory))


def test_dirty_inventory_cannot_define_a_release_baseline(runtime_checkout: tuple[Path, dict[str, Any]]) -> None:
    runtime, inventory = runtime_checkout
    inventory["runtime"]["dirty"] = True
    assert any("baseline must be clean" in error for error in check_provenance(runtime, inventory))


def test_runtime_checkout_requires_git_metadata(tmp_path: Path) -> None:
    (tmp_path / "VERSION").write_text("2.4.0\n")
    inventory = {"runtime": {"version": "2.4.0", "git_head": "0" * 40, "source_tree": "0" * 40, "dirty": False}, "capabilities": []}
    assert any("Git checkout" in error for error in check_provenance(tmp_path, inventory))


@pytest.fixture
def tool_scenario(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    from scripts import runtime_probe

    class Agent:
        def _get_client(self) -> Any:
            raise AssertionError("The probe must inject its fixture client")

    def run(source: str) -> SimpleNamespace:
        client = Agent()._get_client()
        messages = [] if source == "missing" else [{"role": "tool", "tool_call_id": "add-1", "content": source}]
        client.requests.extend([{"messages": []}, {"messages": messages}])
        return SimpleNamespace(success=True, result="5")

    modules = {"src.runtime.agent": SimpleNamespace(NexaAgent=Agent), "src.nexa_sdk": SimpleNamespace(run=run)}
    original = runtime_probe.importlib.import_module
    monkeypatch.setattr(runtime_probe.importlib, "import_module", lambda name: modules[name] if name in modules else original(name))
    return {"id": "add", "source": "5", "scenario": {"replies": [{"calls": [{"id": "add-1"}]}, "5"],
            "expected": "5", "model_calls": 2, "tool_results": {"add-1": "5"}}}


@pytest.mark.parametrize("tool_result", ["-999", "missing"])
def test_offline_tool_result_must_match_even_when_model_answer_is_correct(tool_scenario: dict[str, Any], tool_result: str) -> None:
    tool_scenario["source"] = tool_result
    with pytest.raises(AssertionError, match="tool results"):
        execute_example(tool_scenario)


def test_offline_tool_fixture_requires_explicit_result_expectations(tool_scenario: dict[str, Any]) -> None:
    del tool_scenario["scenario"]["tool_results"]
    with pytest.raises(AssertionError, match="tool results"):
        execute_example(tool_scenario)


def test_offline_tool_fixture_accepts_matching_real_result(tool_scenario: dict[str, Any]) -> None:
    assert execute_example(tool_scenario)["status"] == "passed"


def test_examples_capture_both_nexa_fence_names_and_real_line_numbers() -> None:
    blocks = extract_examples("intro\n\n```nexa\nflow main { result = 1; }\n```\n\n```nx\nagent A {}\n```\n")
    assert [(block.index, block.line, block.source) for block in blocks] == [(1, 4, "flow main { result = 1; }\n"), (2, 8, "agent A {}\n")]


def test_unregistered_example_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/guide.md").write_text("```nexa\nflow main { result = 1; }\n```\n")
    errors = check_inventory(tmp_path, {"pages": [], "examples": [], "capabilities": []})
    assert any("unregistered example: guide.md#1" in error for error in errors)


def test_changed_source_cannot_reuse_example_evidence(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/guide.md").write_text("```nexa\nflow main { result = 2; }\n```\n")
    entry = {"id": "one", "page": "guide.md", "block": 1, "status": "complete", "validation": "compile", "sha256": hashlib.sha256(b"old").hexdigest()}
    errors = check_inventory(tmp_path, {"pages": [], "examples": [entry], "capabilities": []})
    assert any("example changed: guide.md#1" in error for error in errors)


def test_partial_example_requires_specific_reason(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    source = "result = Worker.run(input);\n"
    (tmp_path / "docs/guide.md").write_text(f"```nexa\n{source}```\n")
    entry = {"id": "piece", "page": "guide.md", "block": 1, "status": "partial", "sha256": hashlib.sha256(source.encode()).hexdigest(), "reason": ""}
    errors = check_inventory(tmp_path, {"pages": [], "examples": [entry], "capabilities": []})
    assert any("reason required: guide.md#1" in error for error in errors)


def test_missing_translation_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/guide.md").write_text("# Guide\n")
    errors = check_inventory(tmp_path, {"pages": [{"path": "guide.md", "language": "zh", "capabilities": []}], "examples": [], "capabilities": []})
    assert any("missing translation: guide.en.md" in error for error in errors)


def test_page_capability_metadata_must_match_inventory(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/guide.md").write_text("---\ncapabilities: [runtime]\n---\n# Guide\n")
    inventory = {"pages": [{"path": "guide.md", "language": "zh", "capabilities": ["language"]}],
                 "examples": [], "capabilities": [{"id": "language"}]}
    assert any("metadata differs" in error for error in check_inventory(tmp_path, inventory))


def test_site_links_detect_missing_anchor_and_asset(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text('<a href="guide/#unknown">go</a><img src="missing.svg">')
    (tmp_path / "guide").mkdir()
    (tmp_path / "guide/index.html").write_text('<h1 id="known">Guide</h1><a href="../#top">back</a>')
    errors = check_site(tmp_path)
    assert any("unknown" in error and "anchor" in error for error in errors)
    assert any("missing.svg" in error and "target" in error for error in errors)


def test_site_links_accept_encoded_paths_and_external_links(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text('<a href="space%20name/#known">go</a><a href="https://example.com/no-network">external</a>')
    (tmp_path / "space name").mkdir()
    (tmp_path / "space name/index.html").write_text('<h1 id="known">Guide</h1>')
    assert check_site(tmp_path) == []


def test_asset_cannot_escape_site(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text('<img src="../../outside.png">')
    assert any("escapes site" in error for error in check_site(tmp_path))


def test_probe_isolates_credentials_and_blocks_io_before_runtime_import(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = Path(__file__).resolve().parents[1]
    fake_runtime = tmp_path / "runtime"
    package = fake_runtime / "src"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    sentinel = tmp_path / "secrets.nxs"
    sentinel.write_text("synthetic-fixture-only")
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-fixture-only")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "synthetic-fixture-only")
    monkeypatch.setenv("NEXA_DEBUG", "1")
    (package / "compiler.py").write_text(
        "import os, socket\nfrom pathlib import Path\nfrom types import SimpleNamespace\n"
        "assert 'OPENAI_API_KEY' not in os.environ\nassert 'ANTHROPIC_API_KEY' not in os.environ\nassert 'NEXA_DEBUG' not in os.environ\n"
        "assert Path.home().name == 'home'\nassert list(Path.home().iterdir()) == []\n"
        "try:\n    socket.create_connection(('127.0.0.1', 9))\nexcept RuntimeError as error:\n    assert 'forbid network' in str(error)\n"
        "else:\n    raise AssertionError('network guard missing during import')\n"
        f"try:\n    Path({str(sentinel)!r}).read_text()\nexcept RuntimeError as error:\n    assert 'forbid reading .nxs' in str(error)\n"
        "else:\n    raise AssertionError('credential guard missing during import')\n"
        "def compile_source(source):\n    return SimpleNamespace(diagnostics=SimpleNamespace(warnings=[]))\n"
    )
    report = run_examples(root, fake_runtime, Path(sys.executable), {"examples": []})
    assert report["network"] == "disabled"
    assert report["compiled"] == 0


def open_inventory(tmp_path: Path, *, validation: str = "nativecheck", claim: str = "check") -> dict[str, Any]:
    source = 'language "3.0"\nprogram Answer { goal answer() -> Int { intent "Return 42" implementation value 42 } }\n'
    (tmp_path / "docs").mkdir(exist_ok=True)
    pages = []
    examples = []
    for language, page in (("zh", "guide.md"), ("en", "guide.en.md")):
        (tmp_path / "docs" / page).write_text(f'---\ncapabilities: [open]\nlanguage_versions: ["3.0"]\n---\n```nexa\n{source}```\n')
        pages.append({"path": page, "language": language, "capabilities": ["open"], "language_versions": ["3.0"]})
        examples.append({"id": language, "page": page, "block": 1, "status": "complete", "validation": validation,
                         "language_version": "3.0", "claim": claim, "sha256": digest(source)})
    return {"pages": pages, "examples": examples, "capabilities": [{"id": "open"}]}


def test_nativecheck_accepts_only_contract_claims(tmp_path: Path) -> None:
    assert check_inventory(tmp_path, open_inventory(tmp_path)) == []


def test_nativecheck_cannot_claim_executed_output(tmp_path: Path) -> None:
    errors = check_inventory(tmp_path, open_inventory(tmp_path, claim="execute"))
    assert any("execution claim requires an actual scenario" in error for error in errors)


def test_open_program_cannot_use_legacy_compilation_evidence(tmp_path: Path) -> None:
    errors = check_inventory(tmp_path, open_inventory(tmp_path, validation="compile"))
    assert any("3.0 example requires nativecheck or oci" in error for error in errors)


def test_declared_version_must_match_registered_version(tmp_path: Path) -> None:
    inventory = open_inventory(tmp_path)
    inventory["examples"][0]["language_version"] = "2.4"
    assert any("language version differs" in error for error in check_inventory(tmp_path, inventory))


def test_oci_claim_requires_outputs_calls_and_locked_replay(tmp_path: Path) -> None:
    inventory = open_inventory(tmp_path, validation="oci", claim="execute")
    for item in inventory["examples"]:
        item["scenario"] = {"kind": "build-replay"}
    assert any("OCI scenario requires" in error for error in check_inventory(tmp_path, inventory))


def test_translations_have_matching_validation_and_scenarios(tmp_path: Path) -> None:
    inventory = open_inventory(tmp_path)
    inventory["examples"][0].update(validation="oci", claim="execute", scenario={"kind": "build-replay", "expected_outputs": {"answer": 42}, "model_calls": 0})
    assert any("translation example contract mismatch" in error for error in check_inventory(tmp_path, inventory))


def test_preserved_route_removal_is_rejected(tmp_path: Path) -> None:
    inventory = open_inventory(tmp_path)
    inventory["preserved_pages"] = ["old.md", "old.en.md"]
    assert any("preserved route missing: old.md" in error for error in check_inventory(tmp_path, inventory))


def test_page_versions_must_match_translation(tmp_path: Path) -> None:
    inventory = open_inventory(tmp_path)
    inventory["pages"][0]["language_versions"] = ["2.4"]
    assert any("translation version mismatch" in error for error in check_inventory(tmp_path, inventory))


def test_source_fingerprint_change_requires_review(runtime_checkout: tuple[Path, dict[str, Any]]) -> None:
    runtime, inventory = runtime_checkout
    (runtime / "compiler.py").write_text("def compile_source(): return 'changed'\n")
    assert any("provenance changed" in error for error in check_provenance(runtime, inventory))
