"""Distribution reproducibility verification is strict and fail closed."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "verify_distribution_reproducibility.py"
_WHEEL = "ludoweave-0.1.0a1-py3-none-any.whl"
_SDIST = "ludoweave-0.1.0a1.tar.gz"


def _dist(root: Path, *, wheel: bytes = b"wheel", sdist: bytes = b"sdist") -> Path:
    root.mkdir()
    (root / ".gitignore").write_text("*\n", encoding="utf-8")
    (root / _WHEEL).write_bytes(wheel)
    (root / _SDIST).write_bytes(sdist)
    return root


def _run(first: Path, second: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(_SCRIPT), str(first), str(second)],
        cwd=_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_equal_independent_builds_emit_stable_artifact_identities(tmp_path: Path) -> None:
    result = _run(_dist(tmp_path / "first"), _dist(tmp_path / "second"))

    assert result.returncode == 0, result.stderr
    document = json.loads(result.stdout)
    assert document["protocol"] == "ludoweave.distribution-reproducibility/1"
    assert document["status"] == "pass"
    assert [artifact["name"] for artifact in document["artifacts"]] == [_WHEEL, _SDIST]
    assert all(len(artifact["sha256"]) == 64 for artifact in document["artifacts"])


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        ("wheel-bytes", "distribution.bytes_mismatch"),
        ("sdist-bytes", "distribution.bytes_mismatch"),
        ("missing", "distribution.invalid_artifact_set"),
        ("extra", "distribution.invalid_artifact_set"),
        ("directory", "distribution.invalid_entry"),
    ],
)
def test_mismatch_and_ambiguous_entries_fail_closed(
    tmp_path: Path, mutation: str, code: str
) -> None:
    first = _dist(tmp_path / "first")
    second = _dist(tmp_path / "second")
    if mutation == "wheel-bytes":
        (second / _WHEEL).write_bytes(b"changed-wheel")
    elif mutation == "sdist-bytes":
        (second / _SDIST).write_bytes(b"changed-sdist")
    elif mutation == "missing":
        (second / _SDIST).unlink()
    elif mutation == "extra":
        (second / "unexpected.txt").write_text("unexpected", encoding="utf-8")
    else:
        (second / "nested").mkdir()

    result = _run(first, second)

    assert result.returncode == 1
    assert result.stdout == ""
    document = json.loads(result.stderr)
    assert document["status"] == "fail"
    assert document["code"] == code


def test_same_or_missing_directory_cannot_claim_independent_builds(tmp_path: Path) -> None:
    first = _dist(tmp_path / "first")

    same = _run(first, first)
    assert same.returncode == 1
    assert json.loads(same.stderr)["code"] == "distribution.same_directory"

    missing = _run(first, tmp_path / "missing")
    assert missing.returncode == 1
    assert json.loads(missing.stderr)["code"] == "distribution.invalid_directory"


def test_distinct_valid_versions_fail_name_comparison(tmp_path: Path) -> None:
    first = _dist(tmp_path / "first")
    second = _dist(tmp_path / "second")
    (second / _WHEEL).rename(second / "ludoweave-0.1.0a2-py3-none-any.whl")
    (second / _SDIST).rename(second / "ludoweave-0.1.0a2.tar.gz")

    result = _run(first, second)
    assert result.returncode == 1
    assert json.loads(result.stderr)["code"] == "distribution.name_mismatch"


def test_symlinked_artifact_fails_closed_when_platform_supports_it(tmp_path: Path) -> None:
    first = _dist(tmp_path / "first")
    second = _dist(tmp_path / "second")
    (second / _WHEEL).unlink()
    try:
        (second / _WHEEL).symlink_to(first / _WHEEL)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")

    result = _run(first, second)
    assert result.returncode == 1
    assert json.loads(result.stderr)["code"] == "distribution.invalid_entry"


def test_symlink_cycle_is_a_structured_directory_failure_when_supported(tmp_path: Path) -> None:
    first = tmp_path / "cycle-first"
    second = tmp_path / "cycle-second"
    valid = _dist(tmp_path / "valid")
    try:
        first.symlink_to(second, target_is_directory=True)
        second.symlink_to(first, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")

    result = _run(first, valid)
    assert result.returncode == 1
    assert result.stdout == ""
    assert json.loads(result.stderr)["code"] == "distribution.invalid_directory"


@pytest.mark.parametrize(
    ("wheel", "sdist"),
    [
        ("ludoweave-0.1.0a1-cp312-cp312-win_amd64.whl", _SDIST),
        (_WHEEL, "other-0.1.0a1.tar.gz"),
        ("ludoweave--py3-none-any.whl", "ludoweave-.tar.gz"),
    ],
)
def test_nonportable_or_inconsistent_artifact_names_fail(
    tmp_path: Path, wheel: str, sdist: str
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    for root in (first, second):
        root.mkdir()
        (root / wheel).write_bytes(b"wheel")
        (root / sdist).write_bytes(b"sdist")

    result = _run(first, second)
    assert result.returncode == 1
    assert json.loads(result.stderr)["code"] == "distribution.invalid_artifact_name"
