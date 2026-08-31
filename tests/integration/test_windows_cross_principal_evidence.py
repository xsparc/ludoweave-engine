"""M206 offline Windows cross-principal evidence validation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ludoweave.world import canonical_dumps, canonical_loads
from tests.tools.validate_windows_cross_principal_evidence import (
    EvidenceValidationError,
    ValidationSummary,
    validate_evidence_file,
)

_ROOT = Path(__file__).parents[2]
_VALIDATOR = _ROOT / "tests/tools/validate_windows_cross_principal_evidence.py"
_FIXTURE = _ROOT / "tests/fixtures/windows_cleanup_cross_principal_evidence.json"
_LANE_STATUSES = {"failed": 0, "not_run": 13, "passed": 0, "unsupported": 0}
_BARRIERS = (
    "before_authority_admission",
    "after_authority_before_intent",
    "after_intent_before_pending",
    "after_quarantine_pending_before_quarantine",
    "after_quarantine_before_quarantined",
    "after_delete_pending_before_deletion",
    "after_deletion_before_deleted",
    "during_recovery_reconciliation",
)


def _document() -> dict[str, object]:
    return cast(dict[str, object], canonical_loads(_FIXTURE.read_bytes()))


def _write(path: Path, document: object) -> Path:
    path.write_bytes(canonical_dumps(document))
    return path


def _run(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, "-B", str(_VALIDATOR), str(path)),
        check=False,
        capture_output=True,
        text=True,
    )


def _complete_document() -> dict[str, object]:
    document = _document()
    document["source_commit"] = "git-sha1:" + "a" * 40
    document["executable_sha256"] = "sha256:" + "b" * 64
    qualification = cast(dict[str, object], document["qualification"])
    controls = cast(dict[str, object], document["controls"])
    for record in (qualification, controls):
        for field in record:
            record[field] = True

    lanes = cast(list[dict[str, object]], document["lanes"])
    for lane in lanes:
        lane["status"] = "passed"
        lane["trial_count"] = 1
        lane["event_count"] = 16
        outcomes = cast(dict[str, object], lane["outcomes"])
        for field in outcomes:
            outcomes[field] = True
        lane["barriers"] = [
            {
                "applicable": True,
                "id": barrier_id,
                "release_orders": {
                    "authority_first": "passed",
                    "mutation_first": "passed",
                },
            }
            for barrier_id in _BARRIERS
        ]
    document["totals"] = {"event_count": 208, "lane_count": 13, "trial_count": 13}
    document["criterion_6_satisfied"] = True
    return document


def test_reviewed_incomplete_fixture_is_valid_and_not_admitted() -> None:
    summary = validate_evidence_file(_FIXTURE)

    assert summary == ValidationSummary(
        criterion_6_satisfied=False,
        evidence_sha256=("sha256:b1e20ff9518c52dab5e8251597e5c8344bbca18f81b4ad008c4ac7f5b41cbc9b"),
        lane_status_counts=_LANE_STATUSES,
    )
    assert summary.windows_cleanup_admitted is False


def test_cli_prints_one_canonical_path_free_summary() -> None:
    result = _run(_FIXTURE)

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    decoded = canonical_loads(result.stdout.removesuffix("\n"))
    assert canonical_dumps(decoded).decode() + "\n" == result.stdout
    assert cast(dict[str, object], decoded)["status"] == "valid"
    assert str(_FIXTURE) not in result.stdout


def test_complete_all_passed_evidence_can_satisfy_criterion_6_without_admission(
    tmp_path: Path,
) -> None:
    evidence = _write(tmp_path / "complete.json", _complete_document())

    summary = validate_evidence_file(evidence)

    assert summary.criterion_6_satisfied is True
    assert summary.windows_cleanup_admitted is False
    assert summary.lane_status_counts == {
        "failed": 0,
        "not_run": 0,
        "passed": 13,
        "unsupported": 0,
    }


@pytest.mark.parametrize(
    "location",
    ("document", "qualification", "lane", "outcomes"),
)
def test_unknown_fields_are_rejected(tmp_path: Path, location: str) -> None:
    document = _document()
    lanes = cast(list[dict[str, object]], document["lanes"])
    targets = {
        "document": document,
        "qualification": cast(dict[str, object], document["qualification"]),
        "lane": lanes[0],
        "outcomes": cast(dict[str, object], lanes[0]["outcomes"]),
    }
    targets[location]["unknown"] = False

    with pytest.raises(EvidenceValidationError, match="missing or unknown fields"):
        validate_evidence_file(_write(tmp_path / "unknown.json", document))


def test_noncanonical_bytes_are_rejected(tmp_path: Path) -> None:
    evidence = tmp_path / "noncanonical.json"
    evidence.write_bytes(_FIXTURE.read_bytes() + b"\n")

    with pytest.raises(EvidenceValidationError, match="exact canonical bytes"):
        validate_evidence_file(evidence)


def test_duplicate_fields_are_rejected(tmp_path: Path) -> None:
    evidence = tmp_path / "duplicate.json"
    evidence.write_text('{"schema":null,"schema":null}', encoding="utf-8")

    with pytest.raises(EvidenceValidationError) as caught:
        validate_evidence_file(evidence)

    assert caught.value.code == "evidence.invalid_json"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_commit", None),
        ("source_commit", "git-sha1:ABC"),
        ("source_commit", "sha256:" + "a" * 40),
        ("executable_sha256", None),
        ("executable_sha256", "sha256:ABC"),
        ("executable_sha256", "git-sha1:" + "b" * 64),
    ],
)
def test_attempted_evidence_requires_exact_lowercase_identities(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _complete_document()
    document[field] = value

    with pytest.raises(EvidenceValidationError, match="required digest identity"):
        validate_evidence_file(_write(tmp_path / "identity.json", document))


def test_unattempted_evidence_must_omit_identities(tmp_path: Path) -> None:
    document = _document()
    document["source_commit"] = "git-sha1:" + "a" * 40

    with pytest.raises(EvidenceValidationError, match="must omit identities"):
        validate_evidence_file(_write(tmp_path / "identity.json", document))


@pytest.mark.parametrize(
    ("lane_status", "order_status"),
    (("failed", "failed"), ("unsupported", "unsupported")),
)
def test_negative_attempted_evidence_is_valid_but_cannot_satisfy_criterion_6(
    tmp_path: Path, lane_status: str, order_status: str
) -> None:
    document = _document()
    document["source_commit"] = "git-sha1:" + "a" * 40
    document["executable_sha256"] = "sha256:" + "b" * 64
    lane = cast(list[dict[str, object]], document["lanes"])[0]
    lane["status"] = lane_status
    lane["trial_count"] = 1
    lane["event_count"] = 1
    lane["barriers"] = [
        {
            "applicable": True,
            "id": _BARRIERS[0],
            "release_orders": {
                "authority_first": order_status,
                "mutation_first": "not_run",
            },
        }
    ]
    document["totals"] = {"event_count": 1, "lane_count": 13, "trial_count": 1}

    summary = validate_evidence_file(_write(tmp_path / "negative.json", document))

    assert summary.criterion_6_satisfied is False
    assert summary.windows_cleanup_admitted is False
    assert summary.lane_status_counts[lane_status] == 1
    assert summary.lane_status_counts["not_run"] == 12


def test_lane_order_is_exact(tmp_path: Path) -> None:
    document = _document()
    lanes = cast(list[dict[str, object]], document["lanes"])
    lanes[0], lanes[1] = lanes[1], lanes[0]

    with pytest.raises(EvidenceValidationError, match="unexpected value"):
        validate_evidence_file(_write(tmp_path / "lane-order.json", document))


@pytest.mark.parametrize(
    "mutation",
    ("criterion", "admission", "trial", "barriers", "applicable", "outcome"),
)
def test_complete_evidence_claims_and_observations_are_cross_checked(
    tmp_path: Path, mutation: str
) -> None:
    document = _complete_document()
    lane = cast(list[dict[str, object]], document["lanes"])[0]
    if mutation == "criterion":
        document["criterion_6_satisfied"] = False
    elif mutation == "admission":
        document["windows_cleanup_admitted"] = True
    elif mutation == "trial":
        lane["trial_count"] = 0
    elif mutation == "barriers":
        lane["barriers"] = []
    elif mutation == "applicable":
        cast(list[dict[str, object]], lane["barriers"])[0]["applicable"] = False
    else:
        cast(dict[str, object], lane["outcomes"])["no_leaked_handle"] = False

    with pytest.raises(EvidenceValidationError):
        validate_evidence_file(_write(tmp_path / "claim.json", document))


def test_totals_are_cross_checked(tmp_path: Path) -> None:
    document = _complete_document()
    cast(dict[str, object], document["totals"])["event_count"] = 207

    with pytest.raises(EvidenceValidationError, match="unexpected value"):
        validate_evidence_file(_write(tmp_path / "totals.json", document))


def test_non_file_is_rejected_without_echoing_its_location(tmp_path: Path) -> None:
    result = _run(tmp_path)

    assert result.returncode == 1
    assert result.stderr == ""
    output = cast(dict[str, object], json.loads(result.stdout))
    assert output["status"] == "invalid"
    assert str(tmp_path) not in result.stdout
    assert cast(dict[str, object], output["error"])["code"] == "evidence.not_regular"


def test_missing_file_error_is_path_free(tmp_path: Path) -> None:
    missing = tmp_path / "private-account-secret.json"

    result = _run(missing)

    assert result.returncode == 1
    assert str(missing) not in result.stdout
    assert "private-account-secret" not in result.stdout
    output = cast(dict[str, object], json.loads(result.stdout))
    assert cast(dict[str, object], output["error"])["code"] == "evidence.read_failed"
