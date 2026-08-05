"""Live semantic inspector CLI acceptance over an owned stdio child."""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

from ludoweave.tools.headless_project import PROJECT_PROTOCOL
from ludoweave.tools.inspector import INSPECTOR_EVENT_PROTOCOL
from ludoweave.world import canonical_dumps


def _inspect(*arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, "-I", "-m", "ludoweave", "inspect", *arguments),
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
        cwd=cwd,
    )


def _events(result: subprocess.CompletedProcess[str]) -> list[dict[str, object]]:
    return [cast(dict[str, object], json.loads(line)) for line in result.stdout.splitlines()]


def _object(document: dict[str, object], field: str) -> dict[str, object]:
    value = document[field]
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def test_read_only_inspector_emits_one_bounded_semantic_observation() -> None:
    result = _inspect("--sample", "agent-world-builder")

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    events = _events(result)
    assert len(events) == 1
    event = events[0]
    assert event["protocol"] == INSPECTOR_EVENT_PROTOCOL
    assert event["sequence"] == 0
    assert event["event"] == "observation"
    assert event["cause"] == "initial"
    assert event["transition"] is None
    assert event["diff"] is None
    world = _object(event, "world")
    query = _object(event, "query")
    telemetry = _object(event, "telemetry")
    assert world["completed_ticks"] == 0
    assert world["entity_count"] == 0
    assert query["entities"] == []
    assert telemetry["state_hash"] == query["state_hash"] == world["state_hash"]
    assert "snapshot" not in event


def test_read_only_inspector_accepts_a_data_only_project_target(tmp_path: Path) -> None:
    (tmp_path / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "inspector-project",
                "seed": "0000000000000001",
                "platform_profile": "cpython-inspector-test-v1",
                "dependency_lock_hash": "sha256:" + "1" * 64,
            }
        )
    )

    result = _inspect(str(tmp_path))

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    events = _events(result)
    assert len(events) == 1
    assert _object(events[0], "world")["world_id"] == "inspector-project"


def test_dash_prefixed_project_name_cannot_become_a_child_option(tmp_path: Path) -> None:
    project = tmp_path / "--sample=agent-world-builder"
    project.mkdir()
    (project / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "dash-project",
                "seed": "0000000000000002",
                "platform_profile": "cpython-inspector-test-v1",
                "dependency_lock_hash": "sha256:" + "2" * 64,
            }
        )
    )

    result = _inspect("--", project.name, cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    events = _events(result)
    assert len(events) == 1
    assert _object(events[0], "world")["world_id"] == "dash-project"


def test_write_inspector_bootstraps_and_ticks_with_receipts_and_hash_chain() -> None:
    result = _inspect(
        "--sample",
        "agent-world-builder",
        "--write",
        "--bootstrap",
        "--ticks",
        "2",
        "--query-limit",
        "16",
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    events = _events(result)
    assert [event["sequence"] for event in events] == [0, 1, 2, 3]
    assert [event["cause"] for event in events] == ["initial", "bootstrap", "tick", "tick"]

    bootstrap = events[1]
    bootstrap_world = _object(bootstrap, "world")
    bootstrap_query = _object(bootstrap, "query")
    bootstrap_transition = _object(bootstrap, "transition")
    bootstrap_receipt = _object(bootstrap_transition, "receipt")
    bootstrap_diff = _object(bootstrap, "diff")
    bootstrap_changes = _object(bootstrap_diff, "changes")
    assert bootstrap_world["entity_count"] == 6
    assert bootstrap_query["matched"] == bootstrap_query["returned"] == 6
    assert bootstrap_receipt["status"] == "committed"
    assert bootstrap_changes["created_entities"] == ["0:0", "1:0", "2:0", "3:0", "4:0", "5:0"]

    previous_hash = _object(events[0], "world")["state_hash"]
    for expected_ticks, event in enumerate(events[1:]):
        world = _object(event, "world")
        transition = _object(event, "transition")
        diff = _object(event, "diff")
        assert diff["pre_hash"] == previous_hash
        assert diff["post_hash"] == world["state_hash"]
        if event["cause"] == "tick":
            assert transition["status"] == "committed"
            assert transition["completed"] == 1
            assert world["completed_ticks"] == expected_ticks
            receipts = transition["receipts"]
            assert isinstance(receipts, list)
            receipt_values = cast(list[object], receipts)
            assert len(receipt_values) == 1
            receipt = cast(dict[str, object], receipt_values[0])
            assert receipt["status"] == "committed"
            assert receipt["pre_hash"] == diff["pre_hash"]
            assert receipt["post_hash"] == diff["post_hash"]
        previous_hash = world["state_hash"]


def test_inspector_mutation_requires_explicit_write_capability() -> None:
    for mutation in (("--bootstrap",), ("--ticks", "1")):
        result = _inspect("--sample", "agent-world-builder", *mutation)

        assert result.returncode == 2
        assert result.stdout == ""
        error = cast(dict[str, object], json.loads(result.stderr))
        details = _object(_object(error, "error"), "details")
        assert _object(error, "error")["code"] == "tools.inspector_invalid_config"
        assert details["field"] in {"bootstrap", "write"}


def test_inspector_rejects_unbounded_numeric_options_before_launch() -> None:
    for option in (("--ticks", "601"), ("--query-limit", "0")):
        result = _inspect("--sample", "agent-world-builder", "--write", *option)

        assert result.returncode == 2
        assert result.stdout == ""
        error = _object(cast(dict[str, object], json.loads(result.stderr)), "error")
        assert error["code"] == "tools.inspector_invalid_config"


def test_inspector_reports_early_child_failure_without_disclosing_target_path(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "private-project-name"

    result = _inspect(str(missing))

    assert result.returncode == 2
    assert result.stdout == ""
    error = _object(cast(dict[str, object], json.loads(result.stderr)), "error")
    assert error["code"] == "tools.inspector_transport_failure"
    assert str(missing) not in result.stderr
