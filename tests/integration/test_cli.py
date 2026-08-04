"""CLI version and doctor smoke tests."""

import json
import subprocess
import sys
from dataclasses import replace
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path
from typing import cast

import ludoweave
from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
from ludoweave.world import (
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    TransactionService,
    canonical_dumps,
)


def _run_module(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ludoweave", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def test_python_version_matches_distribution_metadata() -> None:
    assert ludoweave.__version__ == version("ludoweave") == "0.1.0.dev0"
    assert set(ludoweave.__all__) == {"Engine", "EngineConfig", "LifecycleState", "__version__"}


def test_module_version_smoke() -> None:
    result = _run_module("--version")
    assert result.returncode == 0
    assert result.stdout.strip() == "ludoweave 0.1.0.dev0"
    assert result.stderr == ""


def test_doctor_emits_structured_success() -> None:
    result = _run_module("doctor")
    assert result.returncode == 0
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["schema"] == "ludoweave.doctor/1"
    assert report["status"] == "ok"
    assert report["ludoweave_version"] == "0.1.0.dev0"
    assert isinstance(report["checks"], list)
    assert result.stderr == ""


def _headless_project(root: Path) -> HeadlessProject:
    manifest = {
        "protocol": PROJECT_PROTOCOL,
        "world_id": "cli-world",
        "seed": "000000000000002a",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'cli-lock').hexdigest()}",
    }
    (root / "ludoweave.project.json").write_bytes(canonical_dumps(manifest))
    return HeadlessProject.load(root)


def _cli_transaction(session_hash: str | None = None) -> CommandTransaction:
    actor = CommandActor("test", "cli-suite")
    return CommandTransaction(
        (
            CommandEnvelope(
                "cli-command-spawn",
                "cli-transaction",
                actor,
                "entity.spawn",
                {"alias": "subject", "components": []},
                expected_world_hash=session_hash,
            ),
            CommandEnvelope(
                "cli-command-tick",
                "cli-transaction",
                actor,
                "world.tick",
                {"count": 1},
                expected_world_hash=session_hash,
            ),
        ),
        "cli-world",
    )


def test_cli_full_headless_apply_snapshot_replay_and_diff_workflow(
    tmp_path: Path,
) -> None:
    project = _headless_project(tmp_path)
    baseline_session = project.new_session()
    baseline = project.snapshot_codec.encode(baseline_session)
    (tmp_path / "baseline.lws").write_bytes(baseline)
    transaction = _cli_transaction()
    (tmp_path / "transaction.json").write_bytes(transaction.canonical_bytes())

    direct_session = project.new_session()
    direct_receipt = TransactionService(direct_session).apply(transaction)
    apply_result = _run_module(
        "apply",
        str(tmp_path),
        "transaction.json",
        "--snapshot-out",
        "after.lws",
        "--receipt-out",
        "receipt.json",
        "--replay-out",
        "run.lwr",
        "--timeline-id",
        "cli-acceptance",
    )

    assert apply_result.returncode == 0
    assert apply_result.stderr == ""
    assert json.loads(apply_result.stdout) == direct_receipt.as_dict()
    assert apply_result.stdout.encode() == direct_receipt.canonical_bytes() + b"\n"
    assert json.loads((tmp_path / "receipt.json").read_bytes()) == direct_receipt.as_dict()
    assert (tmp_path / "receipt.json").read_bytes() == direct_receipt.canonical_bytes()

    replay_result = _run_module(
        "replay",
        str(tmp_path),
        "run.lwr",
        "--verify-hashes",
        "--snapshot-out",
        "replayed.lws",
    )
    replay_report = cast(dict[str, object], json.loads(replay_result.stdout))
    assert replay_result.returncode == 0
    assert replay_result.stderr == ""
    assert replay_report == {
        "protocol": "ludoweave.cli.replay/1",
        "status": "verified",
        "batches": 1,
        "checkpoints_verified": 2,
        "tick": 1,
        "state_hash": direct_receipt.post_hash,
    }

    snapshot_result = _run_module(
        "snapshot",
        str(tmp_path),
        "run.lwr",
        "--tick",
        "1",
        "--out",
        "tick-1.lws",
    )
    snapshot_report = cast(dict[str, object], json.loads(snapshot_result.stdout))
    assert snapshot_result.returncode == 0
    assert snapshot_result.stderr == ""
    assert snapshot_report == {
        "protocol": "ludoweave.cli.snapshot/1",
        "tick": 1,
        "state_hash": direct_receipt.post_hash,
    }

    assert (tmp_path / "after.lws").read_bytes() == (tmp_path / "replayed.lws").read_bytes()
    assert (tmp_path / "after.lws").read_bytes() == (tmp_path / "tick-1.lws").read_bytes()

    diff_result = _run_module(
        "diff",
        str(tmp_path),
        "baseline.lws",
        "after.lws",
    )
    diff = cast(dict[str, object], json.loads(diff_result.stdout))
    assert diff_result.returncode == 0
    assert diff_result.stderr == ""
    assert diff["protocol"] == "ludoweave.cli.diff/1"
    assert diff["pre_hash"] != diff["post_hash"] == direct_receipt.post_hash
    changes = cast(dict[str, object], diff["changes"])
    assert changes["created_entities"] == ["0:0"]
    assert changes["completed_ticks_before"] == 0
    assert changes["completed_ticks_after"] == 1


def test_cli_rejects_paths_outside_the_project_without_disclosure(tmp_path: Path) -> None:
    project = _headless_project(tmp_path)
    transaction = _cli_transaction(project.new_session().state_hash)
    outside = tmp_path.parent / "outside-transaction.json"
    outside.write_bytes(transaction.canonical_bytes())

    result = _run_module("apply", str(tmp_path), "..\\outside-transaction.json")

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], json.loads(result.stderr))
    diagnostic = cast(dict[str, object], error["error"])
    assert error["protocol"] == "ludoweave.cli.error/1"
    assert diagnostic["code"] == "tools.unsafe_path"
    assert str(tmp_path) not in result.stderr
    assert str(outside) not in result.stderr


def test_cli_dry_run_matches_direct_receipt_without_writing_state(tmp_path: Path) -> None:
    project = _headless_project(tmp_path)
    transaction = replace(_cli_transaction(), dry_run=True)
    (tmp_path / "dry-run.json").write_bytes(transaction.canonical_bytes())
    direct = TransactionService(project.new_session()).apply(transaction)

    result = _run_module(
        "apply",
        str(tmp_path),
        "dry-run.json",
        "--snapshot-out",
        "must-not-exist.lws",
        "--replay-out",
        "must-not-exist.lwr",
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert json.loads(result.stdout) == direct.as_dict()
    assert result.stdout.encode() == direct.canonical_bytes() + b"\n"
    assert direct.status.value == "dry_run"
    assert not (tmp_path / "must-not-exist.lws").exists()
    assert not (tmp_path / "must-not-exist.lwr").exists()


def test_cli_stale_precondition_matches_direct_rejected_receipt(tmp_path: Path) -> None:
    project = _headless_project(tmp_path)
    transaction = _cli_transaction("sha256:" + "0" * 64)
    (tmp_path / "stale.json").write_bytes(transaction.canonical_bytes())
    direct = TransactionService(project.new_session()).apply(transaction)

    result = _run_module(
        "apply",
        str(tmp_path),
        "stale.json",
        "--receipt-out",
        "stale-receipt.json",
        "--snapshot-out",
        "must-not-exist.lws",
    )

    assert result.returncode == 2
    assert result.stderr == ""
    assert json.loads(result.stdout) == direct.as_dict()
    assert result.stdout.encode() == direct.canonical_bytes() + b"\n"
    assert json.loads((tmp_path / "stale-receipt.json").read_bytes()) == direct.as_dict()
    assert (tmp_path / "stale-receipt.json").read_bytes() == direct.canonical_bytes()
    assert direct.status.value == "rejected"
    assert not (tmp_path / "must-not-exist.lws").exists()
