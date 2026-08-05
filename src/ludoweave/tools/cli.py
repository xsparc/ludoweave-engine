"""Standard-library command-line adapters for deterministic headless workflows."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__
from ludoweave.agent import AGENT_TOOL_NAMES
from ludoweave.core.errors import LudoWeaveError
from ludoweave.plugins import (
    PluginDeterminism,
    PluginManifest,
    PluginManifestError,
    check_plugin_compatibility,
    current_plugin_context,
)
from ludoweave.samples import create_agent_world_builder
from ludoweave.tools.agent_service import headless_agent_service
from ludoweave.tools.doctor import run_doctor
from ludoweave.tools.headless_project import HeadlessProject
from ludoweave.tools.inspector import InspectorConfig, run_inspector
from ludoweave.tools.mcp import McpServer, run_stdio
from ludoweave.world import (
    CommandActor,
    CommandTransaction,
    ReceiptStatus,
    ReplayRecorder,
    TransactionService,
    canonical_dumps,
    canonical_loads,
    semantic_diff,
)
from ludoweave.world.canonical import JsonValue

_MAX_TRANSACTION_BYTES = 1_048_576
_MAX_SNAPSHOT_BYTES = 67_108_864
_MAX_REPLAY_BYTES = 134_217_728
_MAX_AGENT_REQUEST_BYTES = 1_048_576
_MAX_PLUGIN_MANIFEST_BYTES = 65_536
_MAX_PLUGIN_MANIFESTS = 64


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ludoweave",
        description="Deterministic, headless-first Python engine for agent-operable 2D worlds.",
    )
    parser.add_argument("--version", action="version", version=f"ludoweave {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("doctor", help="run structured local environment diagnostics")

    apply_parser = subparsers.add_parser(
        "apply",
        help="apply one typed transaction to an empty headless project",
    )
    apply_parser.add_argument("project", type=Path, help="project directory")
    apply_parser.add_argument("transaction", help="project-relative transaction JSON")
    apply_parser.add_argument("--state", help="project-relative input snapshot")
    apply_parser.add_argument("--snapshot-out", help="project-relative output snapshot")
    apply_parser.add_argument("--receipt-out", help="project-relative output receipt")
    apply_parser.add_argument("--replay-out", help="project-relative output replay")
    apply_parser.add_argument("--timeline-id", default="cli-timeline")

    snapshot_parser = subparsers.add_parser(
        "snapshot",
        help="materialize a canonical snapshot from a replay tick boundary",
    )
    snapshot_parser.add_argument("project", type=Path, help="project directory")
    snapshot_parser.add_argument("replay", help="project-relative replay document")
    snapshot_parser.add_argument("--tick", type=int, required=True)
    snapshot_parser.add_argument("--out", required=True, help="project-relative output snapshot")

    replay_parser = subparsers.add_parser(
        "replay",
        help="run a canonical replay through the typed transaction service",
    )
    replay_parser.add_argument("project", type=Path, help="project directory")
    replay_parser.add_argument("replay", help="project-relative replay document")
    replay_parser.add_argument("--verify-hashes", action="store_true")
    replay_parser.add_argument("--snapshot-out", help="project-relative final snapshot")

    diff_parser = subparsers.add_parser(
        "diff",
        help="compute a semantic diff between two canonical snapshots",
    )
    diff_parser.add_argument("project", type=Path, help="project directory")
    diff_parser.add_argument("before", help="project-relative base snapshot")
    diff_parser.add_argument("after", help="project-relative candidate snapshot")

    agent_parser = subparsers.add_parser(
        "agent",
        help="invoke one transport-independent typed agent tool",
    )
    agent_parser.add_argument("project", type=Path, help="data-only project directory")
    agent_parser.add_argument("tool", choices=AGENT_TOOL_NAMES)
    agent_parser.add_argument("request", help="project-relative canonical tool arguments")
    agent_parser.add_argument("--state", help="project-relative input snapshot")
    agent_parser.add_argument("--write", action="store_true", help="enable world mutations")
    agent_parser.add_argument("--actor-kind", default="agent")
    agent_parser.add_argument("--actor-id", default="local-cli")

    mcp_parser = subparsers.add_parser(
        "mcp",
        help="run the local-only MCP stdio adapter",
    )
    mcp_parser.add_argument("project", type=Path, nargs="?", help="data-only project directory")
    mcp_parser.add_argument("--sample", choices=("agent-world-builder",))
    mcp_parser.add_argument("--state", help="project-relative input snapshot")
    mcp_parser.add_argument("--write", action="store_true", help="enable world mutations")
    mcp_parser.add_argument("--actor-kind", default="agent")
    mcp_parser.add_argument("--actor-id", default="local-mcp")
    mcp_parser.add_argument(
        "--renderer",
        choices=("none", "wgpu"),
        default="none",
        help="optional built-in sample capture provider",
    )

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="stream semantic observations from an owned local MCP child",
    )
    inspect_parser.add_argument("project", type=Path, nargs="?", help="data-only project directory")
    inspect_parser.add_argument("--sample", choices=("agent-world-builder",))
    inspect_parser.add_argument("--state", help="project-relative input snapshot")
    inspect_parser.add_argument("--write", action="store_true", help="enable world mutations")
    inspect_parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="create the built-in sample through a receipted transaction",
    )
    inspect_parser.add_argument("--ticks", type=int, default=0)
    inspect_parser.add_argument("--query-limit", type=int, default=32)
    inspect_parser.add_argument("--actor-kind", default="inspector")
    inspect_parser.add_argument("--actor-id", default="local-inspector")

    plugin_parser = subparsers.add_parser(
        "plugin",
        help="validate explicit data-only plugin manifests",
    )
    plugin_subparsers = plugin_parser.add_subparsers(dest="plugin_command", required=True)
    plugin_check_parser = plugin_subparsers.add_parser(
        "check",
        help="check manifests against the current CPython and desktop platform",
    )
    plugin_check_parser.add_argument("manifests", type=Path, nargs="+")
    plugin_check_parser.add_argument(
        "--minimum-determinism",
        default=PluginDeterminism.D0.value,
        metavar="{d0,d1,d2}",
    )
    plugin_check_parser.add_argument(
        "--allow-native",
        action="store_true",
        help="allow manifests that declare native implementation code",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""

    parser = _build_parser()
    args = parser.parse_args(argv)
    command: object = getattr(args, "command", None)
    if command == "doctor":
        report, exit_code = run_doctor()
        _print_json(report)
        return exit_code
    try:
        if command == "apply":
            return _run_apply(args)
        if command == "snapshot":
            return _run_snapshot(args)
        if command == "replay":
            return _run_replay(args)
        if command == "diff":
            return _run_diff(args)
        if command == "agent":
            return _run_agent(args)
        if command == "mcp":
            return _run_mcp(args)
        if command == "inspect":
            return _run_inspect(args)
        if command == "plugin":
            return _run_plugin(args)
    except LudoWeaveError as error:
        _print_error(error)
        return 2
    parser.print_help()
    return 0


def _run_apply(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    state_name = _optional_text_argument(args, "state")
    if state_name is None:
        session = project.new_session()
    else:
        session = project.load_snapshot(
            project.read_relative(
                state_name,
                max_bytes=_MAX_SNAPSHOT_BYTES,
                role="state",
            )
        )
    transaction_name = _text_argument(args, "transaction")
    transaction = CommandTransaction.from_json(
        project.read_relative(
            transaction_name,
            max_bytes=_MAX_TRANSACTION_BYTES,
            role="transaction",
        )
    )
    recorder: ReplayRecorder | None = None
    if transaction.dry_run:
        receipt = TransactionService(session).apply(transaction)
    else:
        recorder = ReplayRecorder(
            session,
            project.snapshot_codec,
            timeline_id=_text_argument(args, "timeline_id"),
            project_schema=project.project_schema,
            dependency_lock_hash=project.dependency_lock_hash,
            platform_profile=project.platform_profile,
        )
        receipt = recorder.record(transaction)
    receipt_bytes = receipt.canonical_bytes()
    receipt_name = _optional_text_argument(args, "receipt_out")
    if receipt_name is not None:
        project.write_relative(receipt_name, receipt_bytes, role="receipt")
    if receipt.status is ReceiptStatus.COMMITTED:
        snapshot_name = _optional_text_argument(args, "snapshot_out")
        if snapshot_name is not None:
            project.write_relative(
                snapshot_name,
                project.snapshot_codec.encode(session),
                role="snapshot",
            )
        replay_name = _optional_text_argument(args, "replay_out")
        if replay_name is not None and recorder is not None:
            project.write_relative(
                replay_name,
                recorder.timeline().canonical_bytes(),
                role="replay",
            )
    _write_stdout(receipt_bytes)
    return 2 if receipt.status is ReceiptStatus.REJECTED else 0


def _run_snapshot(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    replay_bytes = project.read_relative(
        _text_argument(args, "replay"),
        max_bytes=_MAX_REPLAY_BYTES,
        role="replay",
    )
    result = project.replay_runner().replay_to_tick(
        replay_bytes,
        at_tick=_int_argument(args, "tick"),
        tick_executor=project.tick_executor,
    )
    snapshot = project.snapshot_codec.encode(result.session)
    project.write_relative(_text_argument(args, "out"), snapshot, role="snapshot")
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.snapshot/1",
                "tick": result.session.completed_ticks,
                "state_hash": result.session.state_hash,
            }
        )
    )
    return 0


def _run_replay(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    replay_bytes = project.read_relative(
        _text_argument(args, "replay"),
        max_bytes=_MAX_REPLAY_BYTES,
        role="replay",
    )
    verify_hashes = getattr(args, "verify_hashes", False)
    if type(verify_hashes) is not bool:
        raise _argument_error("verify_hashes")
    result = project.replay_runner().replay(
        replay_bytes,
        tick_executor=project.tick_executor,
        verify_hashes=verify_hashes,
    )
    snapshot_name = _optional_text_argument(args, "snapshot_out")
    if snapshot_name is not None:
        project.write_relative(
            snapshot_name,
            project.snapshot_codec.encode(result.session),
            role="snapshot",
        )
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.replay/1",
                "status": "verified" if verify_hashes else "completed",
                "batches": result.batches_applied,
                "checkpoints_verified": len(result.verified_checkpoints),
                "tick": result.session.completed_ticks,
                "state_hash": result.session.state_hash,
            }
        )
    )
    return 0


def _run_diff(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    before = project.load_snapshot(
        project.read_relative(
            _text_argument(args, "before"),
            max_bytes=_MAX_SNAPSHOT_BYTES,
            role="before_snapshot",
        )
    )
    after = project.load_snapshot(
        project.read_relative(
            _text_argument(args, "after"),
            max_bytes=_MAX_SNAPSHOT_BYTES,
            role="after_snapshot",
        )
    )
    changes = semantic_diff(before.authority_document(), after.authority_document())
    document: dict[str, JsonValue] = {
        "protocol": "ludoweave.cli.diff/1",
        "world_id": before.world_id,
        "pre_hash": before.state_hash,
        "post_hash": after.state_hash,
        "changes": changes.as_dict(),
    }
    _write_stdout(canonical_dumps(document))
    return 0


def _run_agent(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    session = _agent_session(project, _optional_text_argument(args, "state"))
    actor = CommandActor(
        _text_argument(args, "actor_kind"),
        _text_argument(args, "actor_id"),
    )
    write = _bool_argument(args, "write")
    request = canonical_loads(
        project.read_relative(
            _text_argument(args, "request"),
            max_bytes=_MAX_AGENT_REQUEST_BYTES,
            role="agent_request",
        )
    )
    if not isinstance(request, dict):
        raise _argument_error("request")
    service = headless_agent_service(
        project,
        session,
        actor=actor,
        write=write,
    )
    try:
        result = service.call(
            _text_argument(args, "tool"),
            cast(dict[str, object], request),
        )
    finally:
        service.close()
    _write_stdout(canonical_dumps(result))
    return 0


def _run_mcp(args: argparse.Namespace) -> int:
    actor = CommandActor(
        _text_argument(args, "actor_kind"),
        _text_argument(args, "actor_id"),
    )
    write = _bool_argument(args, "write")
    project_value: object = getattr(args, "project", None)
    sample = _optional_text_argument(args, "sample")
    renderer = _text_argument(args, "renderer")
    if sample is not None:
        if isinstance(project_value, Path):
            raise _argument_error("project_or_sample")
        device = None
        if renderer == "wgpu":
            from ludoweave.render.backends.wgpu import WgpuRenderDevice

            device = WgpuRenderDevice()
        builder = create_agent_world_builder(
            write=write,
            actor=actor,
            device=device,
        )
        return run_stdio(McpServer(builder.service))
    if not isinstance(project_value, Path):
        raise _argument_error("project_or_sample")
    if renderer != "none":
        raise _argument_error("renderer")
    project = HeadlessProject.load(project_value)
    session = _agent_session(project, _optional_text_argument(args, "state"))
    service = headless_agent_service(project, session, actor=actor, write=write)
    return run_stdio(McpServer(service))


def _run_inspect(args: argparse.Namespace) -> int:
    project_value: object = getattr(args, "project", None)
    project = project_value if isinstance(project_value, Path) else None
    config = InspectorConfig(
        actor=CommandActor(
            _text_argument(args, "actor_kind"),
            _text_argument(args, "actor_id"),
        ),
        project=project,
        sample=_optional_text_argument(args, "sample"),
        state=_optional_text_argument(args, "state"),
        write=_bool_argument(args, "write"),
        bootstrap=_bool_argument(args, "bootstrap"),
        ticks=_int_argument(args, "ticks"),
        query_limit=_int_argument(args, "query_limit"),
    )
    run_inspector(config, output=sys.stdout)
    return 0


def _run_plugin(args: argparse.Namespace) -> int:
    if _text_argument(args, "plugin_command") != "check":
        raise _argument_error("plugin_command")
    determinism_text = _text_argument(args, "minimum_determinism")
    try:
        minimum_determinism = PluginDeterminism(determinism_text)
    except ValueError as error:
        raise _argument_error("minimum_determinism") from error
    paths = _path_arguments(args, "manifests", maximum=_MAX_PLUGIN_MANIFESTS)
    manifests = tuple(PluginManifest.from_json(_read_plugin_manifest(path)) for path in paths)
    context = current_plugin_context(
        minimum_determinism=minimum_determinism,
        allow_native=_bool_argument(args, "allow_native"),
    )
    report = check_plugin_compatibility(manifests, context)
    _write_stdout(report.canonical_bytes())
    return 0 if report.compatible else 1


def _read_plugin_manifest(path: Path) -> bytes:
    try:
        with path.open("rb") as stream:
            document = stream.read(_MAX_PLUGIN_MANIFEST_BYTES + 1)
    except OSError as error:
        raise PluginManifestError(
            "plugin manifest file could not be read",
            code="plugins.manifest_read_failed",
            subsystem="plugins",
            phase="read",
            details={"cause_type": type(error).__name__},
        ) from error
    if len(document) > _MAX_PLUGIN_MANIFEST_BYTES:
        raise PluginManifestError(
            "plugin manifest file exceeds its byte limit",
            code="plugins.manifest_too_large",
            subsystem="plugins",
            phase="read",
            details={"limit": _MAX_PLUGIN_MANIFEST_BYTES},
        )
    return document


def _agent_session(project: HeadlessProject, state_name: str | None):
    if state_name is None:
        return project.new_session()
    return project.load_snapshot(
        project.read_relative(
            state_name,
            max_bytes=_MAX_SNAPSHOT_BYTES,
            role="state",
        )
    )


def _path_argument(args: argparse.Namespace, name: str) -> Path:
    value = getattr(args, name, None)
    if not isinstance(value, Path):
        raise _argument_error(name)
    return value


def _path_arguments(args: argparse.Namespace, name: str, *, maximum: int) -> tuple[Path, ...]:
    value = getattr(args, name, None)
    if not isinstance(value, list):
        raise _argument_error(name)
    items = cast(list[object], value)
    if not items or len(items) > maximum:
        raise _argument_error(name)
    if any(not isinstance(item, Path) for item in items):
        raise _argument_error(name)
    return tuple(cast(Path, item) for item in items)


def _text_argument(args: argparse.Namespace, name: str) -> str:
    value = getattr(args, name, None)
    if type(value) is not str:
        raise _argument_error(name)
    return value


def _optional_text_argument(args: argparse.Namespace, name: str) -> str | None:
    value = getattr(args, name, None)
    if value is not None and type(value) is not str:
        raise _argument_error(name)
    return value


def _int_argument(args: argparse.Namespace, name: str) -> int:
    value = getattr(args, name, None)
    if type(value) is not int:
        raise _argument_error(name)
    return value


def _bool_argument(args: argparse.Namespace, name: str) -> bool:
    value = getattr(args, name, None)
    if type(value) is not bool:
        raise _argument_error(name)
    return value


def _argument_error(field: str) -> LudoWeaveError:
    return LudoWeaveError(
        "CLI argument has an invalid type",
        code="tools.invalid_argument",
        subsystem="tools",
        phase="dispatch",
        details={"field": field},
    )


def _print_json(document: object) -> None:
    print(json.dumps(document, sort_keys=True, separators=(",", ":")))


def _print_error(error: LudoWeaveError) -> None:
    print(
        json.dumps(
            {"protocol": "ludoweave.cli.error/1", "error": error.as_dict()},
            sort_keys=True,
            separators=(",", ":"),
        ),
        file=sys.stderr,
    )


def _write_stdout(document: bytes) -> None:
    sys.stdout.buffer.write(document)
    sys.stdout.buffer.write(b"\n")
