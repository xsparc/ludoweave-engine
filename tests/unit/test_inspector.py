# pyright: reportPrivateUsage=false
"""Inspector composition-value and protocol validation."""

import sys
from io import StringIO
from pathlib import Path

import pytest

from ludoweave.core.errors import LudoWeaveError
from ludoweave.tools.inspector import (
    InspectorConfig,
    _child_command,
    _decode_object,
    _json_object,
    _ObservationState,
    _read_response_line,
    _require_committed_transition,
)
from ludoweave.world import CommandActor
from ludoweave.world.canonical import JsonValue

_ACTOR = CommandActor("test", "inspector")


def test_inspector_config_accepts_one_read_only_local_target() -> None:
    sample = InspectorConfig(actor=_ACTOR, sample="agent-world-builder")
    project = InspectorConfig(actor=_ACTOR, project=Path("project"), state="world.lws")

    assert sample.write is False
    assert sample.ticks == 0
    assert project.state == "world.lws"


@pytest.mark.parametrize(
    ("values", "field"),
    [
        ({}, "project_or_sample"),
        ({"project": Path("project"), "sample": "agent-world-builder"}, "project_or_sample"),
        ({"project": "project"}, "project"),
        ({"sample": "unknown"}, "sample"),
        ({"sample": "agent-world-builder", "state": "world.lws"}, "state"),
        ({"sample": "agent-world-builder", "bootstrap": True}, "bootstrap"),
        ({"project": Path("project"), "write": True, "bootstrap": True}, "bootstrap"),
        ({"sample": "agent-world-builder", "ticks": 1}, "write"),
        ({"sample": "agent-world-builder", "write": True, "ticks": -1}, "ticks"),
        ({"sample": "agent-world-builder", "write": True, "ticks": 601}, "ticks"),
        ({"sample": "agent-world-builder", "query_limit": 0}, "query_limit"),
        ({"sample": "agent-world-builder", "query_limit": 1_001}, "query_limit"),
    ],
)
def test_inspector_config_rejects_ambiguous_or_unbounded_sessions(
    values: dict[str, object], field: str
) -> None:
    with pytest.raises(LudoWeaveError) as captured:
        InspectorConfig(actor=_ACTOR, **values)  # type: ignore[arg-type]

    assert captured.value.code == "tools.inspector_invalid_config"
    assert dict(captured.value.details) == {"field": field}


def test_inspector_child_command_is_fixed_to_current_ludoweave_module() -> None:
    config = InspectorConfig(
        actor=_ACTOR,
        project=Path("project with spaces"),
        state="state.lws",
        write=True,
    )

    assert _child_command(config) == (
        sys.executable,
        "-I",
        "-m",
        "ludoweave",
        "mcp",
        "--state=state.lws",
        "--write",
        "--actor-kind=test",
        "--actor-id=inspector",
        "--",
        "project with spaces",
    )


@pytest.mark.parametrize(
    "document",
    [
        "[]\n",
        '{"jsonrpc":"2.0","id":1,"id":2}\n',
        '{"jsonrpc":"2.0","result":NaN}\n',
    ],
)
def test_inspector_rejects_malformed_child_documents(document: str) -> None:
    with pytest.raises(LudoWeaveError) as captured:
        _decode_object(document, operation="test")

    assert captured.value.code == "tools.inspector_protocol_failure"


def test_inspector_rejects_child_values_outside_canonical_integer_domain() -> None:
    decoded = _decode_object('{"result":9223372036854775808}\n', operation="test")

    with pytest.raises(LudoWeaveError) as captured:
        _json_object(decoded, operation="test")

    assert captured.value.code == "tools.inspector_protocol_failure"


def test_inspector_rejects_tick_result_without_one_valid_receipt() -> None:
    previous_hash = "sha256:" + "1" * 64
    transition: dict[str, JsonValue] = {
        "status": "committed",
        "completed": 1,
        "completed_ticks": 5,
        "state_hash": "sha256:" + "2" * 64,
        "receipts": [],
    }

    with pytest.raises(LudoWeaveError) as captured:
        _require_committed_transition(
            transition,
            cause="tick",
            previous=_ObservationState("snapshot", previous_hash, 4),
        )

    assert captured.value.code == "tools.inspector_protocol_failure"
    assert dict(captured.value.details)["field"] == "receipts"


class _FailingStream(StringIO):
    def __init__(self, error: Exception) -> None:
        super().__init__()
        self._error = error

    def readline(self, size: int = -1, /) -> str:
        del size
        raise self._error


@pytest.mark.parametrize(
    ("error", "code"),
    [
        (OSError("failed read"), "tools.inspector_transport_failure"),
        (ValueError("closed stream"), "tools.inspector_transport_failure"),
        (
            UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte"),
            "tools.inspector_protocol_failure",
        ),
    ],
)
def test_inspector_translates_child_stream_failures(error: Exception, code: str) -> None:
    with pytest.raises(LudoWeaveError) as captured:
        _read_response_line(_FailingStream(error), operation="test")

    assert captured.value.code == code
