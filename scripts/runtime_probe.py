"""Compile docs with the selected runtime; execute fixtures with network disabled."""

from __future__ import annotations

import contextlib
import copy
import importlib
import io
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch


class FixtureClient:
    def __init__(self, responses: list[object]) -> None:
        self.responses = iter(responses)
        self.requests: list[dict[str, object]] = []
        self.chat = SimpleNamespace(completions=self)

    def create(self, **kwargs: object) -> object:
        self.requests.append(copy.deepcopy(kwargs))
        response = next(self.responses)
        calls = response.get("calls") if isinstance(response, dict) else None
        text = response.get("text", "") if isinstance(response, dict) else response
        completion_type = importlib.import_module("openai.types.chat").ChatCompletion
        return completion_type.model_validate({
            "id": "docs-fixture", "object": "chat.completion", "created": 1, "model": "docs-fixture",
            "choices": [{"index": 0, "finish_reason": "tool_calls" if calls else "stop",
                         "message": {"role": "assistant", "content": text, "tool_calls": calls}}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
        })


def install_guards() -> None:
    # Nexa creates configuration objects at import time, so guard before importing it.
    def guard(event: str, args: tuple[object, ...]) -> None:
        if event in {"socket.connect", "socket.bind", "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr", "socket.sendto"}:
            raise RuntimeError("Documentation checks forbid network access")
        if event == "open" and isinstance(args[0], (str, bytes)) and os.fsdecode(args[0]).endswith(".nxs"):
            raise RuntimeError("Documentation checks forbid reading .nxs credentials")

    sys.addaudithook(guard)


def last_message(request: dict[str, object]) -> object:
    messages = request.get("messages")
    if not isinstance(messages, list) or not messages or not isinstance(messages[-1], dict):
        raise AssertionError("Fixture expected a nonempty Chat message array")
    return messages[-1].get("content")


def verify_tool_results(example: dict[str, Any], requests: list[dict[str, object]]) -> None:
    scenario = example["scenario"]
    calls = {call["id"] for reply in scenario.get("replies", []) if isinstance(reply, dict) for call in reply.get("calls", [])}
    expected = scenario.get("tool_results", {})
    if not isinstance(expected, dict) or set(expected) != calls:
        raise AssertionError(f'{example["id"]}: expected tool results must cover every fixture call')
    observed: dict[str, object] = {}
    for request in requests:
        messages = request.get("messages", [])
        if not isinstance(messages, list):
            raise TypeError(f'{example["id"]}: cannot inspect tool results without a message array')
        for message in messages:
            if not isinstance(message, dict) or message.get("role") != "tool":
                continue
            call_id = message["tool_call_id"]
            content = message.get("content")
            if call_id in observed and observed[call_id] != content:
                raise AssertionError(f'{example["id"]}: tool results changed for {call_id}')
            observed[call_id] = content
    if observed != expected:
        raise AssertionError(f'{example["id"]}: expected tool results {expected!r}, got {observed!r}')


def execute_example(example: dict[str, Any]) -> dict[str, object]:
    scenario = example["scenario"]
    client = FixtureClient(scenario.get("replies", []))
    agent_type = importlib.import_module("src.runtime.agent").NexaAgent
    sdk = importlib.import_module("src.nexa_sdk")
    with patch.object(agent_type, "_get_client", lambda self: client):
        result = sdk.run(example["source"])
    if "error_contains" in scenario:
        if result.success or scenario["error_contains"] not in result.stderr:
            raise AssertionError(f'{example["id"]}: expected error {scenario["error_contains"]!r}, got {result.stderr!r}')
    else:
        if not result.success:
            raise AssertionError(f'{example["id"]}: {result.stderr}')
        output = result.result.model_dump() if hasattr(result.result, "model_dump") else result.result
        if output != scenario["expected"]:
            raise AssertionError(f'{example["id"]}: expected {scenario["expected"]!r}, got {output!r}')
    if "model_calls" in scenario and len(client.requests) != scenario["model_calls"]:
        raise AssertionError(f'{example["id"]}: unexpected model call count {len(client.requests)}')
    verify_tool_results(example, client.requests)
    if "user_messages" in scenario:
        messages = [last_message(request) for request in client.requests]
        if messages != scenario["user_messages"]:
            raise AssertionError(f'{example["id"]}: unexpected Actor mailbox order {messages!r}')
    return {"id": example["id"], "status": "passed", "model_calls": len(client.requests)}


def main() -> None:
    install_guards()
    runtime = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(runtime))
    examples = json.loads(Path(sys.argv[2]).read_text())
    compiler = importlib.import_module("src.compiler")
    results: list[dict[str, object]] = []
    warning_count = 0
    compiled = 0
    errors: list[str] = []
    with contextlib.redirect_stdout(io.StringIO()):
        for example in examples:
            try:
                compilation = compiler.compile_source(example["source"])
                compiled += 1
                warning_count += len(compilation.diagnostics.warnings)
                if example["validation"] == "offline":
                    results.append(execute_example(example))
            except Exception as error:  # noqa: BLE001 -- Every captured failure is reported and makes the gate fail.
                errors.append(f'{example["id"]}: {error}')
    print(json.dumps({"compiled": compiled, "offline_executed": len(results), "harness_warnings": warning_count,
                      "network": "disabled", "scenarios": results, "errors": errors}))


if __name__ == "__main__":
    main()
