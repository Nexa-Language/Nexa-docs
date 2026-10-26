"""Reject execution reports whose result or evidence differs from the documented claim."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from scripts import runtime_probe


def artifact(output: str = "42", *, passed: bool = True, status: str = "accepted") -> SimpleNamespace:
    evidence = SimpleNamespace(passed=passed, requirement="typecheck", digest="evidence")
    result = SimpleNamespace(goal_name="answer", output_json=output, status=status, evidence=[evidence])
    return SimpleNamespace(results=[result])


def test_open_artifact_requires_actual_output() -> None:
    with pytest.raises(AssertionError, match="outputs"):
        runtime_probe.verify_open_artifact(artifact("41"), {"answer": 42})


def test_open_artifact_requires_accepted_result() -> None:
    with pytest.raises(AssertionError, match="accepted"):
        runtime_probe.verify_open_artifact(artifact(status="blocked"), {"answer": 42})


def test_open_artifact_requires_passing_evidence() -> None:
    with pytest.raises(AssertionError, match="evidence"):
        runtime_probe.verify_open_artifact(artifact(passed=False), {"answer": 42})


def test_open_artifact_preserves_observed_values() -> None:
    result = runtime_probe.verify_open_artifact(artifact(), {"answer": 42})
    assert result == {"outputs": {"answer": 42}, "evidence": {"answer": [{"requirement": "typecheck", "digest": "evidence"}]}}
