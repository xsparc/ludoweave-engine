"""Direct Python, CLI, and MCP receipt equivalence and stdio acceptance."""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

from ludoweave.tools.agent_service import headless_agent_service
from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
from ludoweave.tools.mcp import MCP_PROTOCOL_VERSION, McpServer
from ludoweave.world import CommandActor, CommandEnvelope, CommandTransaction, canonical_dumps


def _project(root: Path) -> HeadlessProject:
    manifest = {
        "protocol": PROJECT_PROTOCOL,
        "world_id": "agent-conformance",
        "seed": "0000000000001079",
        "platform_profile": "cpython-agent-conformance-v1",
        "dependency_lock_hash": "sha256:" + "7" * 64,
    }
    (root / "ludoweave.project.json").write_bytes(canonical_dumps(manifest))
    return HeadlessProject.load(root)


def _transaction(project: HeadlessProject, actor: CommandActor) -> CommandTransaction:
    session = project.new_session()
    return CommandTransaction(
        (
            CommandEnvelope(
                command_id="conformance.spawn",
                transaction_id="conformance.transaction",
                actor=actor,
                operation="entity.spawn",
                arguments={"alias": "created", "components": []},
                expected_world_hash=session.state_hash,
            ),
        ),
        project.world_id,
    )


def _mcp_send(server: McpServer, document: object) -> dict[str, object]:
    response = server.handle_line(json.dumps(document, separators=(",", ":")))
    assert response is not None
    decoded = json.loads(response)
    assert isinstance(decoded, dict)
    return cast(dict[str, object], decoded)


def _mcp_ready(server: McpServer) -> None:
    initialized = _mcp_send(
        server,
        {
            "jsonrpc": "2.0",
            "id": "initialize",
            "method": "initialize",
            "params": {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "conformance", "version": "1"},
            },
        },
    )
    assert "result" in initialized
    assert server.handle_line('{"jsonrpc":"2.0","method":"notifications/initialized"}') is None


def test_direct_cli_and_mcp_apply_return_equivalent_receipts(tmp_path: Path) -> None:
    project = _project(tmp_path)
    actor = CommandActor("agent", "conformance")
    transaction = _transaction(project, actor)
    arguments = {"transaction": transaction.as_dict()}

    direct_service = headless_agent_service(
        project,
        project.new_session(),
        actor=actor,
        write=True,
    )
    direct = direct_service.call("transaction_apply", arguments)

    (tmp_path / "agent-request.json").write_bytes(canonical_dumps(arguments))
    cli = subprocess.run(
        (
            sys.executable,
            "-m",
            "ludoweave",
            "agent",
            str(tmp_path),
            "transaction_apply",
            "agent-request.json",
            "--write",
            "--actor-kind",
            actor.kind,
            "--actor-id",
            actor.id,
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    assert cli.returncode == 0, cli.stderr
    cli_result = json.loads(cli.stdout)

    mcp_service = headless_agent_service(
        project,
        project.new_session(),
        actor=actor,
        write=True,
    )
    server = McpServer(mcp_service)
    _mcp_ready(server)
    mcp = _mcp_send(
        server,
        {
            "jsonrpc": "2.0",
            "id": "apply",
            "method": "tools/call",
            "params": {"name": "transaction_apply", "arguments": arguments},
        },
    )
    mcp_result = cast(dict[str, object], mcp["result"])

    assert cli_result == direct
    assert mcp_result["structuredContent"] == direct
    assert json.loads(cast(list[dict[str, str]], mcp_result["content"])[0]["text"]) == direct
    direct_service.close()
    server.close()


def test_cli_agent_write_is_denied_without_explicit_flag(tmp_path: Path) -> None:
    project = _project(tmp_path)
    actor = CommandActor("agent", "conformance")
    arguments = {"transaction": _transaction(project, actor).as_dict()}
    (tmp_path / "agent-request.json").write_bytes(canonical_dumps(arguments))

    result = subprocess.run(
        (
            sys.executable,
            "-m",
            "ludoweave",
            "agent",
            str(tmp_path),
            "transaction_apply",
            "agent-request.json",
            "--actor-kind",
            actor.kind,
            "--actor-id",
            actor.id,
        ),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    error = json.loads(result.stderr)
    assert error["error"]["code"] == "agent.capability_denied"


def test_cli_mcp_subcommand_runs_local_stdio_lifecycle(tmp_path: Path) -> None:
    _project(tmp_path)
    messages = "\n".join(
        (
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": MCP_PROTOCOL_VERSION,
                        "capabilities": {},
                        "clientInfo": {"name": "cli-test", "version": "1"},
                    },
                }
            ),
            '{"jsonrpc":"2.0","method":"notifications/initialized"}',
            '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}',
            "",
        )
    )

    result = subprocess.run(
        (sys.executable, "-m", "ludoweave", "mcp", str(tmp_path)),
        input=messages,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    responses = [json.loads(line) for line in result.stdout.splitlines()]
    assert len(responses) == 2
    assert responses[0]["result"]["protocolVersion"] == MCP_PROTOCOL_VERSION
    assert len(responses[1]["result"]["tools"]) == 12
