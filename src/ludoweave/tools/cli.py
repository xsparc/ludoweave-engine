"""Standard-library command-line adapters for deterministic headless workflows."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from ludoweave import __version__
from ludoweave.core.errors import LudoWeaveError
from ludoweave.tools.doctor import run_doctor
from ludoweave.tools.headless_project import HeadlessProject
from ludoweave.world import (
    CommandTransaction,
    ReceiptStatus,
    ReplayRecorder,
    TransactionService,
    canonical_dumps,
    semantic_diff,
)
from ludoweave.world.canonical import JsonValue

_MAX_TRANSACTION_BYTES = 1_048_576
_MAX_SNAPSHOT_BYTES = 67_108_864
_MAX_REPLAY_BYTES = 134_217_728


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


def _path_argument(args: argparse.Namespace, name: str) -> Path:
    value = getattr(args, name, None)
    if not isinstance(value, Path):
        raise _argument_error(name)
    return value


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
