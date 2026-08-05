"""M13 offline rollback-readiness example and evidence validation."""

import importlib.util
import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "rollback_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "validate_rollback_readiness.py"


def _run_example(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def test_readiness_example_proves_local_branch_and_defers_networking() -> None:
    first = _run_example("--ticks", "24", "--branch-tick", "12")
    second = _run_example("--ticks", "24", "--branch-tick", "12")

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = json.loads(first.stdout)
    assert document["schema"] == "ludoweave.evaluation.rollback-readiness/1"
    assert document["status"] == "deferred"
    assert document["decision"] == "defer-network-rollback"
    assert document["transport_implemented"] is False
    assert document["proof"] == {
        "correction_changed_state": True,
        "correction_checkpoints_verified": True,
        "correction_repeatable": True,
        "input_rehydration_required": True,
        "lineage_verified": True,
        "parent_checkpoints_verified": True,
        "parent_repeatable": True,
    }
    assert document["gates"]["canonical_tick_inputs"] is False
    assert document["gates"]["versioned_network_snapshot_protocol"] is False
    assert document["work"] == {
        "branch_batches": 12,
        "branch_checkpoints": 13,
        "branch_tick": 12,
        "parent_batches": 24,
        "parent_checkpoints": 25,
        "ticks": 24,
    }
    assert document["hashes"]["corrected_final"] != document["hashes"]["parent_final"]


def test_written_evidence_passes_strict_validator(tmp_path: Path) -> None:
    artifact = tmp_path / "readiness.json"
    result = _run_example(
        "--ticks",
        "20",
        "--branch-tick",
        "8",
        "--output",
        str(artifact),
    )
    validation = subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert artifact.read_text(encoding="utf-8") == result.stdout
    assert validation.returncode == 0, validation.stderr
    assert validation.stdout == "rollback readiness evidence valid\n"


@pytest.mark.parametrize(
    "arguments",
    [
        ("--ticks", "1", "--branch-tick", "0"),
        ("--ticks", "601", "--branch-tick", "1"),
        ("--ticks", "10", "--branch-tick", "0"),
        ("--ticks", "10", "--branch-tick", "10"),
    ],
)
def test_readiness_example_rejects_unbounded_work(arguments: tuple[str, ...]) -> None:
    result = _run_example(*arguments)

    assert result.returncode == 2
    assert "error:" in result.stderr


def test_validator_rejects_false_admission_claim() -> None:
    validate = _validator()
    document = json.loads(_run_example("--ticks", "12", "--branch-tick", "6").stdout)
    document["transport_implemented"] = True

    with pytest.raises(ValueError, match="cannot claim a transport"):
        validate(document)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "ludoweave.evaluation.rollback-readiness/2"),
        ("status", "ok"),
        ("decision", "admit-network-rollback"),
        ("ludoweave_version", "0.1.0a2"),
        ("ludoweave_version", "C:\\private\\credential-token.txt"),
    ],
)
def test_validator_rejects_tampered_root_claim(field: str, value: object) -> None:
    validate = _validator()
    document = _evidence()
    document[field] = value

    with pytest.raises(ValueError):
        validate(document)


def test_validator_rejects_unknown_fields() -> None:
    validate = _validator()
    document = _evidence()
    document["peer"] = "remote"

    with pytest.raises(ValueError, match="incomplete or unknown"):
        validate(document)


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        ("proof", "lineage_verified", False),
        ("proof", "unexpected", True),
        ("gates", "canonical_tick_inputs", True),
        ("gates", "canonical_tick_inputs", 1),
        ("gates", "local_branch_lineage", 1),
        ("hashes", "parent_timeline", "sha256:xyz"),
        ("work", "parent_batches", 1),
        ("work", "branch_batches", True),
        ("work", "parent_checkpoints", 1),
        ("metrics", "parent_snapshot_bytes", 0),
        ("metrics", "parent_timeline_bytes", 64 * 1024 * 1024 + 1),
    ],
)
def test_validator_rejects_tampered_nested_claim(section: str, field: str, value: object) -> None:
    validate = _validator()
    document = _evidence()
    nested = cast(dict[str, object], document[section])
    nested[field] = value

    with pytest.raises(ValueError):
        validate(document)


def test_validator_rejects_equal_parent_and_corrected_hashes() -> None:
    validate = _validator()
    document = _evidence()
    hashes = cast(dict[str, object], document["hashes"])
    hashes["corrected_final"] = hashes["parent_final"]

    with pytest.raises(ValueError, match="must differ"):
        validate(document)


def test_validator_rejects_oversized_file_before_json_decode(tmp_path: Path) -> None:
    artifact = tmp_path / "oversized.json"
    artifact.write_bytes(b"{" + b" " * (64 * 1024))

    result = subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "artifact size is outside the accepted bound" in result.stderr
    assert "JSONDecodeError" not in result.stderr


def test_validator_rejects_non_regular_path_before_open(tmp_path: Path) -> None:
    result = subprocess.run(
        (sys.executable, str(_VALIDATOR), str(tmp_path)),
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 1
    assert "artifact must be a regular file" in result.stderr


@pytest.mark.parametrize("nested", [False, True])
def test_validator_rejects_duplicate_json_keys(tmp_path: Path, nested: bool) -> None:
    artifact = tmp_path / "duplicate.json"
    encoded = _run_example("--ticks", "12", "--branch-tick", "6").stdout.strip()
    if nested:
        encoded = encoded.replace(
            '"proof":{',
            '"proof":{"lineage_verified":false,',
            1,
        )
    else:
        encoded = '{"schema":"evil-duplicate",' + encoded[1:]
    artifact.write_text(encoded, encoding="utf-8")

    result = subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "duplicate object key" in result.stderr


def test_validator_rejects_non_finite_json_number(tmp_path: Path) -> None:
    artifact = tmp_path / "nonfinite.json"
    encoded = _run_example("--ticks", "12", "--branch-tick", "6").stdout.replace(
        '"parent_snapshot_bytes":2793',
        '"parent_snapshot_bytes":NaN',
        1,
    )
    artifact.write_text(encoded, encoding="utf-8")

    result = subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "non-finite number" in result.stderr


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "ludoweave.evaluation.rollback-readiness/1"),
        ("status", "deferred"),
        ("decision", "defer-network-rollback"),
        ("ludoweave_version", "0.1.0a1"),
    ],
)
def test_direct_validator_rejects_string_subclass_claim(field: str, value: str) -> None:
    class _Text(str):
        pass

    validate = _validator()
    document = _evidence()
    document[field] = _Text(value)

    with pytest.raises(ValueError):
        validate(document)


@pytest.mark.parametrize(
    ("ticks", "branch_tick"),
    [
        (True, 1),
        (2, False),
        (-1, 1),
        (601, 1),
        (10, 0),
        (10, 10),
    ],
)
def test_direct_evaluator_rejects_unbounded_work(ticks: object, branch_tick: object) -> None:
    evaluate = _evaluator()

    with pytest.raises((TypeError, ValueError)):
        evaluate(ticks=ticks, branch_tick=branch_tick)


def _validator() -> Callable[[object], None]:
    spec = importlib.util.spec_from_file_location("rollback_readiness_validator", _VALIDATOR)
    if spec is None or spec.loader is None:
        raise AssertionError("validator module could not be loaded")
    module = ModuleType(spec.name)
    spec.loader.exec_module(module)
    return cast(Callable[[object], None], module.validate)


def _evaluator() -> Callable[..., dict[str, object]]:
    spec = importlib.util.spec_from_file_location("rollback_readiness_example", _EXAMPLE)
    if spec is None or spec.loader is None:
        raise AssertionError("readiness example module could not be loaded")
    module = ModuleType(spec.name)
    spec.loader.exec_module(module)
    return cast(Callable[..., dict[str, object]], module.evaluate)


def _evidence() -> dict[str, object]:
    result = _run_example("--ticks", "12", "--branch-tick", "6")
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))
