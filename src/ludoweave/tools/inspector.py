"""Headless semantic inspector over an owned local MCP child process."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO, cast

from ludoweave.core.errors import ErrorValue, LudoWeaveError
from ludoweave.core.version import __version__
from ludoweave.samples import builder_create_transaction
from ludoweave.tools.mcp import MCP_PROTOCOL_VERSION
from ludoweave.world import CommandActor
from ludoweave.world.canonical import JsonLimits, JsonValue, validate_json_value

INSPECTOR_EVENT_PROTOCOL = "ludoweave.inspector.event/1"

_MAX_REQUEST_BYTES = 1_048_576
_MAX_RESPONSE_BYTES = 16_777_216
_MAX_TICKS = 600
_MAX_QUERY_LIMIT = 1_000
_CLOSE_TIMEOUT_SECONDS = 5.0
_REQUIRED_TOOLS = frozenset(
    {
        "telemetry_get",
        "transaction_apply",
        "world_describe",
        "world_diff",
        "world_query",
        "world_snapshot",
        "world_tick",
    }
)
_JSON_LIMITS = JsonLimits(
    max_bytes=_MAX_RESPONSE_BYTES,
    max_depth=64,
    max_nodes=250_000,
    max_collection_items=100_000,
    max_string_bytes=_MAX_RESPONSE_BYTES,
)


@dataclass(frozen=True, slots=True)
class InspectorConfig:
    """Validated composition values for one local inspector session."""

    actor: CommandActor
    project: Path | None = None
    sample: str | None = None
    state: str | None = None
    write: bool = False
    bootstrap: bool = False
    ticks: int = 0
    query_limit: int = 32

    def __post_init__(self) -> None:
        if type(self.actor) is not CommandActor:
            raise _config_error("actor")
        if (self.project is None) == (self.sample is None):
            raise _config_error("project_or_sample")
        _require_project(self.project)
        if self.sample is not None and self.sample != "agent-world-builder":
            raise _config_error("sample")
        if self.state is not None and (type(self.state) is not str or not self.state):
            raise _config_error("state")
        if self.state is not None and self.project is None:
            raise _config_error("state")
        if type(self.write) is not bool or type(self.bootstrap) is not bool:
            raise _config_error("capabilities")
        if self.bootstrap and (not self.write or self.sample != "agent-world-builder"):
            raise _config_error("bootstrap")
        if type(self.ticks) is not int or not 0 <= self.ticks <= _MAX_TICKS:
            raise _config_error("ticks")
        if self.ticks and not self.write:
            raise _config_error("write")
        if type(self.query_limit) is not int or not 1 <= self.query_limit <= _MAX_QUERY_LIMIT:
            raise _config_error("query_limit")


@dataclass(frozen=True, slots=True)
class _ObservationState:
    snapshot: str
    state_hash: str
    completed_ticks: int


class _McpChild:
    __slots__ = ("_closed", "_next_id", "_process", "_stderr", "_stdin", "_stdout")

    def __init__(self, config: InspectorConfig) -> None:
        try:
            process = subprocess.Popen(
                _child_command(config),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="strict",
                bufsize=1,
                shell=False,
            )
        except OSError as error:
            raise _transport_error("spawn", error_type=type(error).__name__) from error
        if process.stdin is None or process.stdout is None or process.stderr is None:
            process.kill()
            process.wait()
            raise _transport_error("spawn", error_type="MissingPipe")
        self._process: subprocess.Popen[str] = process
        self._stdin = cast(TextIO, process.stdin)
        self._stdout = cast(TextIO, process.stdout)
        self._stderr = cast(TextIO, process.stderr)
        self._closed = False
        self._next_id = 1

    def initialize(self) -> None:
        result = self._request(
            "initialize",
            {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "ludoweave-inspector", "version": __version__},
            },
        )
        if result.get("protocolVersion") != MCP_PROTOCOL_VERSION:
            raise _protocol_error("initialize", "protocol_version")
        self._notify("notifications/initialized", {})
        tools = self._request("tools/list", {})
        tool_values_value: object = tools.get("tools")
        if not isinstance(tool_values_value, list):
            raise _protocol_error("tools/list", "tools")
        tool_values = cast(list[object], tool_values_value)
        names: set[str] = set()
        for value in tool_values:
            if not isinstance(value, dict):
                raise _protocol_error("tools/list", "tool")
            tool = cast(dict[object, object], value)
            name_value = tool.get("name")
            if type(name_value) is not str:
                raise _protocol_error("tools/list", "tool")
            names.add(name_value)
        if not _REQUIRED_TOOLS.issubset(names):
            raise _protocol_error("tools/list", "required_tools")

    def call_tool(
        self, name: str, arguments: Mapping[str, JsonValue] | None = None
    ) -> dict[str, JsonValue]:
        result = self._request(
            "tools/call",
            {"name": name, "arguments": dict(arguments or {})},
        )
        is_error = result.get("isError")
        structured = result.get("structuredContent")
        if type(is_error) is not bool:
            raise _protocol_error(name, "tool_result")
        checked = _json_object(structured, operation=name)
        if is_error:
            remote_code = "unknown"
            error_value = checked.get("error")
            if isinstance(error_value, dict) and type(error_value.get("code")) is str:
                remote_code = cast(str, error_value["code"])
            raise LudoWeaveError(
                "inspector target rejected a typed tool call",
                code="tools.inspector_tool_failure",
                subsystem="tools",
                phase="inspect",
                details={"tool": name, "remote_code": remote_code},
            )
        return checked

    def close(self, *, suppress_failure: bool) -> None:
        if self._closed:
            return
        self._closed = True
        close_error: BaseException | None = None
        try:
            self._stdin.close()
        except BaseException as error:
            close_error = error
        timed_out = False
        return_code: int | None = None
        try:
            return_code = self._process.wait(timeout=_CLOSE_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                self._process.kill()
                return_code = self._process.wait(timeout=_CLOSE_TIMEOUT_SECONDS)
            except BaseException as error:
                close_error = close_error or error
        except BaseException as error:
            close_error = close_error or error
        finally:
            for pipe in (self._stdout, self._stderr):
                try:
                    pipe.close()
                except BaseException as error:
                    close_error = close_error or error
        if suppress_failure:
            return
        if close_error is not None:
            if isinstance(close_error, Exception):
                raise _transport_error(
                    "close", error_type=type(close_error).__name__
                ) from close_error
            raise close_error
        if timed_out:
            raise _transport_error("close", error_type="TimeoutExpired")
        if return_code != 0:
            raise _transport_error("close", exit_code=return_code)

    def _notify(self, method: str, params: Mapping[str, object]) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": dict(params)})

    def _request(self, method: str, params: Mapping[str, object]) -> dict[str, JsonValue]:
        request_id = self._next_id
        self._next_id += 1
        self._write(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": dict(params),
            }
        )
        line = _read_response_line(self._stdout, operation=method)
        if not line:
            raise _transport_error("read", exit_code=self._process.poll())
        if len(line.encode("utf-8")) > _MAX_RESPONSE_BYTES or not line.endswith("\n"):
            raise _protocol_error(method, "response_size")
        response = _json_object(_decode_object(line, operation=method), operation=method)
        if response.get("jsonrpc") != "2.0" or response.get("id") != request_id:
            raise _protocol_error(method, "response_identity")
        if "error" in response:
            error_value = response["error"]
            remote_code = "unknown"
            if isinstance(error_value, dict) and type(error_value.get("code")) in (str, int):
                remote_code = str(error_value["code"])
            raise LudoWeaveError(
                "inspector target returned a protocol error",
                code="tools.inspector_protocol_failure",
                subsystem="tools",
                phase="protocol",
                details={"operation": method, "remote_code": remote_code},
            )
        result = response.get("result")
        return _json_object(result, operation=method)

    def _write(self, document: Mapping[str, object]) -> None:
        line = _encode(document)
        if len(line.encode("utf-8")) > _MAX_REQUEST_BYTES:
            raise _protocol_error("write", "request_size")
        try:
            self._stdin.write(line)
            self._stdin.write("\n")
            self._stdin.flush()
        except (OSError, UnicodeError) as error:
            raise _transport_error("write", error_type=type(error).__name__) from error


def run_inspector(config: InspectorConfig, *, output: TextIO) -> None:
    """Run one bounded inspector session and emit newline-delimited events."""

    child = _McpChild(config)
    failed = False
    try:
        child.initialize()
        sequence = 0
        state = _observe(
            child,
            config=config,
            output=output,
            sequence=sequence,
            cause="initial",
            previous=None,
            transition=None,
        )
        if config.bootstrap:
            transition = child.call_tool(
                "transaction_apply",
                {
                    "transaction": builder_create_transaction(
                        config.actor,
                        expected_world_hash=state.state_hash,
                        transaction_id="inspector.bootstrap",
                    ).as_dict()
                },
            )
            _require_committed_transition(transition, cause="bootstrap", previous=state)
            sequence += 1
            state = _observe(
                child,
                config=config,
                output=output,
                sequence=sequence,
                cause="bootstrap",
                previous=state,
                transition=transition,
            )
        for index in range(config.ticks):
            transition = child.call_tool(
                "world_tick",
                {
                    "count": 1,
                    "expected_world_hash": state.state_hash,
                    "request_id": f"inspector.tick-{index}",
                },
            )
            _require_committed_transition(transition, cause="tick", previous=state)
            sequence += 1
            state = _observe(
                child,
                config=config,
                output=output,
                sequence=sequence,
                cause="tick",
                previous=state,
                transition=transition,
            )
    except BaseException:
        failed = True
        raise
    finally:
        child.close(suppress_failure=failed)


def _observe(
    child: _McpChild,
    *,
    config: InspectorConfig,
    output: TextIO,
    sequence: int,
    cause: str,
    previous: _ObservationState | None,
    transition: dict[str, JsonValue] | None,
) -> _ObservationState:
    snapshot_document = child.call_tool("world_snapshot")
    world = child.call_tool("world_describe")
    query = child.call_tool("world_query", {"limit": config.query_limit})
    telemetry = child.call_tool("telemetry_get")
    snapshot = _required_text(snapshot_document, "snapshot", operation="world_snapshot")
    state_hash = _required_text(snapshot_document, "state_hash", operation="world_snapshot")
    completed_ticks = _required_int(
        snapshot_document, "completed_ticks", operation="world_snapshot"
    )
    _require_observation_identity(world, state_hash=state_hash, ticks=completed_ticks)
    _require_hash(query, state_hash=state_hash, operation="world_query")
    _require_observation_identity(telemetry, state_hash=state_hash, ticks=completed_ticks)

    diff: dict[str, JsonValue] | None = None
    if previous is not None:
        diff = child.call_tool("world_diff", {"before_snapshot": previous.snapshot})
        if (
            _required_text(diff, "pre_hash", operation="world_diff") != previous.state_hash
            or _required_text(diff, "post_hash", operation="world_diff") != state_hash
        ):
            raise _protocol_error("world_diff", "hash_chain")
        _require_transition_post_state(
            transition,
            cause=cause,
            state_hash=state_hash,
            completed_ticks=completed_ticks,
        )

    event: dict[str, JsonValue] = {
        "protocol": INSPECTOR_EVENT_PROTOCOL,
        "sequence": sequence,
        "event": "observation",
        "cause": cause,
        "world": world,
        "query": query,
        "telemetry": telemetry,
        "transition": transition,
        "diff": diff,
    }
    line = _encode(event)
    if len(line.encode("utf-8")) > _MAX_RESPONSE_BYTES:
        raise _protocol_error("observation", "event_size")
    output.write(line)
    output.write("\n")
    output.flush()
    return _ObservationState(snapshot, state_hash, completed_ticks)


def _require_committed_transition(
    transition: Mapping[str, JsonValue], *, cause: str, previous: _ObservationState
) -> None:
    if cause == "bootstrap":
        receipt = transition.get("receipt")
        if not isinstance(receipt, dict):
            raise _protocol_error("transaction_apply", "receipt")
        checked = _json_object(receipt, operation="transaction_apply")
        if (
            checked.get("status") != "committed"
            or checked.get("pre_hash") != previous.state_hash
            or checked.get("completed_ticks_before") != previous.completed_ticks
            or checked.get("completed_ticks_after") != previous.completed_ticks
        ):
            raise _protocol_error("transaction_apply", "receipt_status")
        return
    if (
        transition.get("status") != "committed"
        or transition.get("completed") != 1
        or transition.get("completed_ticks") != previous.completed_ticks + 1
        or transition.get("state_hash") == previous.state_hash
    ):
        raise _protocol_error("world_tick", "receipt_status")
    receipts = transition.get("receipts")
    if not isinstance(receipts, list) or len(receipts) != 1:
        raise _protocol_error("world_tick", "receipts")
    receipt = _json_object(receipts[0], operation="world_tick")
    if (
        receipt.get("status") != "committed"
        or receipt.get("pre_hash") != previous.state_hash
        or receipt.get("post_hash") != transition.get("state_hash")
        or receipt.get("completed_ticks_before") != previous.completed_ticks
        or receipt.get("completed_ticks_after") != previous.completed_ticks + 1
    ):
        raise _protocol_error("world_tick", "receipt_status")


def _require_transition_post_state(
    transition: Mapping[str, JsonValue] | None,
    *,
    cause: str,
    state_hash: str,
    completed_ticks: int,
) -> None:
    if transition is None:
        raise _protocol_error(cause, "transition")
    if cause == "bootstrap":
        receipt = transition.get("receipt")
        if not isinstance(receipt, dict) or receipt.get("post_hash") != state_hash:
            raise _protocol_error("transaction_apply", "post_hash")
        return
    if (
        transition.get("state_hash") != state_hash
        or transition.get("completed_ticks") != completed_ticks
    ):
        raise _protocol_error("world_tick", "post_hash")


def _require_observation_identity(
    document: Mapping[str, JsonValue], *, state_hash: str, ticks: int
) -> None:
    if document.get("state_hash") != state_hash or document.get("completed_ticks") != ticks:
        raise _protocol_error("observation", "state_identity")


def _require_hash(document: Mapping[str, JsonValue], *, state_hash: str, operation: str) -> None:
    if document.get("state_hash") != state_hash:
        raise _protocol_error(operation, "state_hash")


def _required_text(document: Mapping[str, JsonValue], field: str, *, operation: str) -> str:
    value = document.get(field)
    if type(value) is not str:
        raise _protocol_error(operation, field)
    return value


def _required_int(document: Mapping[str, JsonValue], field: str, *, operation: str) -> int:
    value = document.get(field)
    if type(value) is not int:
        raise _protocol_error(operation, field)
    return value


def _child_command(config: InspectorConfig) -> tuple[str, ...]:
    command = [sys.executable, "-I", "-m", "ludoweave", "mcp"]
    if config.sample is not None:
        command.append(f"--sample={config.sample}")
    if config.state is not None:
        command.append(f"--state={config.state}")
    if config.write:
        command.append("--write")
    command.extend(
        (
            f"--actor-kind={config.actor.kind}",
            f"--actor-id={config.actor.id}",
        )
    )
    if config.project is not None:
        command.extend(("--", str(config.project)))
    return tuple(command)


def _read_response_line(stream: TextIO, *, operation: str) -> str:
    try:
        return stream.readline(_MAX_RESPONSE_BYTES + 1)
    except UnicodeError as error:
        raise _protocol_error(operation, "encoding") from error
    except (OSError, ValueError) as error:
        raise _transport_error("read", error_type=type(error).__name__) from error


def _decode_object(line: str, *, operation: str) -> dict[str, object]:
    try:
        value = json.loads(
            line,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, UnicodeError, ValueError) as error:
        raise _protocol_error(operation, "json") from error
    if not isinstance(value, dict):
        raise _protocol_error(operation, "document")
    return cast(dict[str, object], value)


def _json_object(value: object, *, operation: str) -> dict[str, JsonValue]:
    try:
        checked = validate_json_value(value, limits=_JSON_LIMITS)
    except LudoWeaveError as error:
        raise _protocol_error(operation, "json_value") from error
    if not isinstance(checked, dict):
        raise _protocol_error(operation, "json_object")
    return checked


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant {value!r}")


def _encode(value: Mapping[str, object]) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _config_error(field: str) -> LudoWeaveError:
    return LudoWeaveError(
        "inspector configuration is invalid",
        code="tools.inspector_invalid_config",
        subsystem="tools",
        phase="configure",
        details={"field": field},
    )


def _require_project(value: object) -> None:
    if value is not None and not isinstance(value, Path):
        raise _config_error("project")


def _protocol_error(operation: str, field: str) -> LudoWeaveError:
    return LudoWeaveError(
        "inspector received an invalid local protocol document",
        code="tools.inspector_protocol_failure",
        subsystem="tools",
        phase="protocol",
        details={"operation": operation, "field": field},
    )


def _transport_error(
    operation: str, *, error_type: str | None = None, exit_code: int | None = None
) -> LudoWeaveError:
    details: dict[str, ErrorValue] = {"operation": operation}
    if error_type is not None:
        details["error_type"] = error_type
    if exit_code is not None:
        details["exit_code"] = exit_code
    return LudoWeaveError(
        "local inspector child transport failed",
        code="tools.inspector_transport_failure",
        subsystem="tools",
        phase="transport",
        details=details,
    )
