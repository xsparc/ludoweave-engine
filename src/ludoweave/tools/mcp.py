"""Small local-only MCP stdio adapter over :mod:`ludoweave.agent`."""

from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TextIO, cast

from ludoweave.agent import AGENT_ERROR_PROTOCOL, AGENT_TOOLS, AgentCommandService
from ludoweave.core.errors import LudoWeaveError
from ludoweave.core.version import __version__

MCP_PROTOCOL_VERSION = "2025-11-25"
MCP_SERVER_NAME = "ludoweave"


@dataclass(frozen=True, slots=True)
class _ProtocolFailure(Exception):
    code: int
    message: str
    data: dict[str, object] | None = None


class McpServer:
    """Stateful MCP lifecycle and tools adapter with no network listener.

    The supported transport is newline-delimited UTF-8 JSON-RPC 2.0 over
    inherited stdin/stdout. Domain behavior remains entirely in the injected
    :class:`AgentCommandService`.
    """

    __slots__ = ("_initialized", "_ready", "_request_ids", "_service")

    def __init__(self, service: AgentCommandService) -> None:
        self._service = service
        self._initialized = False
        self._ready = False
        self._request_ids: set[str | int] = set()

    def close(self) -> None:
        self._service.close()

    def handle_line(self, line: str | bytes) -> str | None:
        """Handle one complete newline-delimited MCP message."""

        try:
            document = _decode_message(line, max_bytes=self._service.limits.max_request_bytes)
        except _ProtocolFailure as error:
            return _encode(_error_response(None, error))
        try:
            response = self._handle_message(document)
        except _ProtocolFailure as error:
            request_id = _response_id(document.get("id"))
            return _encode(_error_response(request_id, error))
        if response is None:
            return None
        return _encode(response)

    def _handle_message(self, document: dict[str, object]) -> dict[str, object] | None:
        if document.get("jsonrpc") != "2.0":
            raise _ProtocolFailure(-32600, "Invalid Request")
        method = document.get("method")
        if type(method) is not str:
            raise _ProtocolFailure(-32600, "Invalid Request")
        notification = "id" not in document
        if notification:
            self._handle_notification(method, document.get("params"))
            return None
        request_id = _request_id(document.get("id"))
        if request_id in self._request_ids:
            raise _ProtocolFailure(-32600, "Request ID was already used")
        self._request_ids.add(request_id)
        if method == "initialize":
            return self._initialize(request_id, document.get("params"))
        if method == "ping":
            return _result_response(request_id, {})
        if not self._ready:
            raise _ProtocolFailure(-32002, "Server is not initialized")
        if method == "tools/list":
            return self._list_tools(request_id, document.get("params"))
        if method == "tools/call":
            return self._call_tool(request_id, document.get("params"))
        raise _ProtocolFailure(-32601, "Method not found")

    def _initialize(self, request_id: str | int, params: object) -> dict[str, object]:
        if self._initialized:
            raise _ProtocolFailure(-32600, "Server is already initialized")
        values = _params(params)
        _require_fields(
            values,
            required={"capabilities", "clientInfo", "protocolVersion"},
            optional={"_meta"},
        )
        protocol_version = values["protocolVersion"]
        if type(protocol_version) is not str:
            raise _ProtocolFailure(-32602, "Invalid initialize parameters")
        if not isinstance(values["capabilities"], dict) or not isinstance(
            values["clientInfo"], dict
        ):
            raise _ProtocolFailure(-32602, "Invalid initialize parameters")
        self._initialized = True
        negotiated = (
            protocol_version if protocol_version == MCP_PROTOCOL_VERSION else MCP_PROTOCOL_VERSION
        )
        return _result_response(
            request_id,
            {
                "protocolVersion": negotiated,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": MCP_SERVER_NAME,
                    "title": "LudoWeave Engine",
                    "version": __version__,
                    "description": "Local typed tools for an agent-operable LudoWeave world.",
                },
                "instructions": (
                    "Read tools are always available. Mutations require the server process "
                    "to be started with explicit write capability."
                ),
            },
        )

    def _handle_notification(self, method: str, params: object) -> None:
        if method == "notifications/initialized":
            if not self._initialized or self._ready:
                return
            if params is not None and not isinstance(params, dict):
                return
            self._ready = True

    @staticmethod
    def _list_tools(request_id: str | int, params: object) -> dict[str, object]:
        values = _params(params)
        _require_fields(values, required=set(), optional={"_meta", "cursor"})
        if values.get("cursor") is not None:
            raise _ProtocolFailure(-32602, "Tool pagination cursor is invalid")
        return _result_response(
            request_id,
            {"tools": [tool.as_mcp_dict() for tool in AGENT_TOOLS]},
        )

    def _call_tool(self, request_id: str | int, params: object) -> dict[str, object]:
        values = _params(params)
        _require_fields(values, required={"name"}, optional={"_meta", "arguments"})
        name = values["name"]
        arguments = values.get("arguments", {})
        if type(name) is not str or not isinstance(arguments, dict):
            raise _ProtocolFailure(-32602, "Invalid tool call parameters")
        try:
            structured = self._service.call(name, cast(dict[str, object], arguments))
        except LudoWeaveError as error:
            structured_error: dict[str, object] = {
                "protocol": AGENT_ERROR_PROTOCOL,
                "error": error.as_dict(),
            }
            return _result_response(
                request_id,
                {
                    "content": [{"type": "text", "text": _encode(structured_error)}],
                    "structuredContent": structured_error,
                    "isError": True,
                },
            )
        return _result_response(
            request_id,
            {
                "content": [{"type": "text", "text": _encode(structured)}],
                "structuredContent": structured,
                "isError": False,
            },
        )


def run_stdio(
    server: McpServer,
    *,
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> int:
    """Run a local MCP stdio session until the client closes stdin."""

    incoming = input_stream or sys.stdin
    outgoing = output_stream or sys.stdout
    try:
        for line in incoming:
            response = server.handle_line(line)
            if response is None:
                continue
            outgoing.write(response)
            outgoing.write("\n")
            outgoing.flush()
    finally:
        server.close()
    return 0


def _decode_message(line: str | bytes, *, max_bytes: int) -> dict[str, object]:
    try:
        if isinstance(line, bytes):
            raw = line
            text = raw.decode("utf-8")
        else:
            text = line
            raw = text.encode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError) as error:
        raise _ProtocolFailure(-32700, "Parse error") from error
    if len(raw) > max_bytes:
        raise _ProtocolFailure(-32600, "Request exceeds server limit")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as error:
        raise _ProtocolFailure(-32700, "Parse error") from error
    if not isinstance(value, dict):
        raise _ProtocolFailure(-32600, "Invalid Request")
    return cast(dict[str, object], value)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant {value!r}")


def _params(value: object) -> dict[str, object]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise _ProtocolFailure(-32602, "Invalid params")
    return cast(dict[str, object], value)


def _require_fields(
    value: Mapping[str, object],
    *,
    required: set[str],
    optional: set[str],
) -> None:
    actual = set(value)
    if required - actual or actual - required - optional:
        raise _ProtocolFailure(-32602, "Invalid params")


def _request_id(value: object) -> str | int:
    if type(value) not in (str, int):
        raise _ProtocolFailure(-32600, "Invalid Request")
    return cast(str | int, value)


def _response_id(value: object) -> str | int | None:
    return cast(str | int, value) if type(value) in (str, int) else None


def _result_response(request_id: str | int, result: object) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error_response(
    request_id: str | int | None,
    error: _ProtocolFailure,
) -> dict[str, object]:
    body: dict[str, object] = {"code": error.code, "message": error.message}
    if error.data is not None:
        body["data"] = error.data
    return {"jsonrpc": "2.0", "id": request_id, "error": body}


def _encode(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )
