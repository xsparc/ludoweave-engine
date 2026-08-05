"""MCP 2025-11-25 lifecycle and thin-adapter conformance."""

import json
from io import StringIO
from typing import cast

from ludoweave.agent import AGENT_TOOL_NAMES
from ludoweave.samples import builder_create_transaction, create_agent_world_builder
from ludoweave.tools.mcp import MCP_PROTOCOL_VERSION, McpServer, run_stdio


def _send(server: McpServer, document: object) -> dict[str, object]:
    response = server.handle_line(json.dumps(document, separators=(",", ":")))
    assert response is not None
    decoded = json.loads(response)
    assert isinstance(decoded, dict)
    return cast(dict[str, object], decoded)


def _ready(server: McpServer) -> None:
    initialized = _send(
        server,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1"},
            },
        },
    )
    result = cast(dict[str, object], initialized["result"])
    assert result["protocolVersion"] == MCP_PROTOCOL_VERSION
    assert result["capabilities"] == {"tools": {"listChanged": False}}
    assert server.handle_line('{"jsonrpc":"2.0","method":"notifications/initialized"}') is None


def test_mcp_requires_lifecycle_and_lists_exact_typed_surface() -> None:
    builder = create_agent_world_builder()
    server = McpServer(builder.service)

    early = _send(
        server,
        {"jsonrpc": "2.0", "id": "early", "method": "tools/list", "params": {}},
    )
    assert cast(dict[str, object], early["error"])["code"] == -32002

    _ready(server)
    listed = _send(
        server,
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    )
    result = cast(dict[str, object], listed["result"])
    tools = cast(list[object], result["tools"])
    assert tuple(cast(dict[str, object], tool)["name"] for tool in tools) == AGENT_TOOL_NAMES
    assert all(
        cast(dict[str, object], tool)["inputSchema"]
        and cast(dict[str, object], tool)["outputSchema"]
        and cast(dict[str, object], tool)["annotations"]
        for tool in tools
    )
    server.close()


def test_mcp_read_tool_returns_equivalent_structured_and_text_content() -> None:
    builder = create_agent_world_builder()
    server = McpServer(builder.service)
    _ready(server)

    response = _send(
        server,
        {
            "jsonrpc": "2.0",
            "id": "describe",
            "method": "tools/call",
            "params": {"name": "world_describe", "arguments": {}},
        },
    )

    result = cast(dict[str, object], response["result"])
    assert result["isError"] is False
    structured = cast(dict[str, object], result["structuredContent"])
    content = cast(list[object], result["content"])
    text = cast(dict[str, object], content[0])["text"]
    assert isinstance(text, str)
    assert json.loads(text) == structured
    assert structured["state_hash"] == builder.service.session.state_hash
    server.close()


def test_mcp_capability_failure_is_a_tool_result_not_protocol_error() -> None:
    builder = create_agent_world_builder()
    transaction = builder_create_transaction(
        builder.service.actor,
        expected_world_hash=builder.service.session.state_hash,
    )
    server = McpServer(builder.service)
    _ready(server)

    response = _send(
        server,
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "transaction_apply",
                "arguments": {"transaction": transaction.as_dict()},
            },
        },
    )

    result = cast(dict[str, object], response["result"])
    assert result["isError"] is True
    structured = cast(dict[str, object], result["structuredContent"])
    error = cast(dict[str, object], structured["error"])
    assert error["code"] == "agent.capability_denied"
    assert builder.service.call("world_describe")["entity_count"] == 0
    server.close()


def test_mcp_write_tool_returns_the_exact_service_receipt() -> None:
    direct = create_agent_world_builder(write=True)
    direct_transaction = builder_create_transaction(
        direct.service.actor,
        expected_world_hash=direct.service.session.state_hash,
    )
    direct_result = direct.service.call(
        "transaction_apply", {"transaction": direct_transaction.as_dict()}
    )

    adapted = create_agent_world_builder(write=True)
    adapted_transaction = builder_create_transaction(
        adapted.service.actor,
        expected_world_hash=adapted.service.session.state_hash,
    )
    server = McpServer(adapted.service)
    _ready(server)
    response = _send(
        server,
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "transaction_apply",
                "arguments": {"transaction": adapted_transaction.as_dict()},
            },
        },
    )

    result = cast(dict[str, object], response["result"])
    assert result["structuredContent"] == direct_result
    assert adapted.service.session.state_hash == direct.service.session.state_hash
    direct.close()
    server.close()


def test_mcp_rejects_batch_duplicate_keys_duplicate_ids_and_invalid_params() -> None:
    builder = create_agent_world_builder()
    server = McpServer(builder.service)

    batch = server.handle_line("[]")
    assert batch is not None
    assert json.loads(batch)["error"]["code"] == -32600
    duplicate_key = server.handle_line('{"jsonrpc":"2.0","id":1,"id":2,"method":"ping"}')
    assert duplicate_key is not None
    assert json.loads(duplicate_key)["error"]["code"] == -32700

    _ready(server)
    first = _send(server, {"jsonrpc": "2.0", "id": 7, "method": "ping"})
    assert first["result"] == {}
    duplicate_id = _send(server, {"jsonrpc": "2.0", "id": 7, "method": "ping"})
    assert cast(dict[str, object], duplicate_id["error"])["code"] == -32600
    invalid = _send(
        server,
        {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {"name": "world_describe", "arguments": []},
        },
    )
    assert cast(dict[str, object], invalid["error"])["code"] == -32602
    server.close()


def test_stdio_runner_emits_only_json_rpc_and_closes_service() -> None:
    builder = create_agent_world_builder()
    incoming = StringIO(
        "\n".join(
            (
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": MCP_PROTOCOL_VERSION,
                            "capabilities": {},
                            "clientInfo": {"name": "test", "version": "1"},
                        },
                    }
                ),
                '{"jsonrpc":"2.0","method":"notifications/initialized"}',
                '{"jsonrpc":"2.0","id":2,"method":"ping"}',
                "",
            )
        )
    )
    outgoing = StringIO()

    assert run_stdio(McpServer(builder.service), input_stream=incoming, output_stream=outgoing) == 0

    lines = outgoing.getvalue().splitlines()
    assert len(lines) == 2
    assert all(json.loads(line)["jsonrpc"] == "2.0" for line in lines)
    assert json.loads(lines[1])["result"] == {}
