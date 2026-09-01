"""M208 offline Windows independent-host evidence validation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ludoweave.world import canonical_dumps, canonical_loads
from tests.tools.validate_windows_cross_principal_evidence import (
    validate_evidence_file as validate_cross_principal_evidence_file,
)
from tests.tools.validate_windows_independent_host_evidence import (
    EvidenceValidationError,
    ValidationSummary,
    validate_evidence_files,
)

_ROOT = Path(__file__).parents[2]
_VALIDATOR = _ROOT / "tests/tools/validate_windows_independent_host_evidence.py"
_FIXTURE = _ROOT / "tests/fixtures/windows_cleanup_independent_host_evidence.json"
_CROSS_FIXTURE = _ROOT / "tests/fixtures/windows_cleanup_cross_principal_evidence.json"
_PROFILE_STATUSES = {"failed": 0, "not_run": 8, "passed": 0, "unsupported": 0}
_HOST_STATUSES = {"failed": 0, "not_run": 0, "passed": 0, "unsupported": 0}
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
_INTERRUPTIONS = (
    "forced_process_termination",
    "vm_power_cut",
    "physical_host_power_loss",
)


def _document() -> dict[str, object]:
    return cast(dict[str, object], canonical_loads(_FIXTURE.read_bytes()))


def _cross_document() -> dict[str, object]:
    return cast(dict[str, object], canonical_loads(_CROSS_FIXTURE.read_bytes()))


def _write(path: Path, document: object) -> Path:
    path.write_bytes(canonical_dumps(document))
    return path


def _run(evidence: Path, cross_evidence: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, "-B", str(_VALIDATOR), str(evidence), str(cross_evidence)),
        check=False,
        capture_output=True,
        text=True,
    )


def _complete_cross_document() -> dict[str, object]:
    document = _cross_document()
    document["source_commit"] = "git-sha1:" + "a" * 40
    document["executable_sha256"] = "sha256:" + "b" * 64
    for record_name in ("qualification", "controls"):
        record = cast(dict[str, object], document[record_name])
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
                "id": barrier,
                "release_orders": {
                    "authority_first": "passed",
                    "mutation_first": "passed",
                },
            }
            for barrier in _BARRIERS
        ]
    document["totals"] = {"event_count": 208, "lane_count": 13, "trial_count": 13}
    document["criterion_6_satisfied"] = True
    return document


def _interruptions(*, passed: bool) -> list[dict[str, object]]:
    status = "passed" if passed else "not_run"
    count = 1 if passed else 0
    return [
        {
            "id": interruption,
            "observation_count": count,
            "status": status,
            "trial_count": count,
        }
        for interruption in _INTERRUPTIONS
    ]


def _profile_result(profile_id: str, host_ordinal: int) -> dict[str, object]:
    capabilities = {
        "hard_links": True,
        "open_by_file_id": True,
        "persistent_acls": True,
        "profile_stable": True,
        "read_only_volume": False,
        "reparse_points": True,
        "same_volume": True,
    }
    outcomes = {
        "file_id_reuse_observed": False,
        "no_canonical_world_state_change": True,
        "no_credential_or_identity_disclosure": True,
        "no_leaked_handle": True,
        "no_live_participant_or_descendant": True,
        "no_out_of_root_mutation": True,
        "no_unauthorized_deletion_or_restoration": True,
        "refused_before_authority_or_mutation": profile_id != "local_fixed_ntfs",
        "stale_authorization_rejected": False,
    }
    locality = "local_fixed"
    filesystem_family = "ntfs"
    filesystem_version_class = "known_supported"
    file_id_scope = "host_volume_128"
    interruption_evidence = _interruptions(passed=profile_id == "local_fixed_ntfs")
    count = 3 if profile_id == "local_fixed_ntfs" else 1

    if profile_id == "refs_refusal":
        filesystem_family = "refs"
        filesystem_version_class = "known_unadmitted"
    elif profile_id == "smb_refusal":
        locality = "remote"
        filesystem_family = "smb"
        filesystem_version_class = "known_unadmitted"
    elif profile_id == "csvfs_refusal":
        locality = "clustered"
        filesystem_family = "csvfs"
        filesystem_version_class = "known_unadmitted"
    elif profile_id == "cross_volume_refusal":
        capabilities["same_volume"] = False
    elif profile_id == "unknown_filesystem_refusal":
        filesystem_family = "unknown"
        filesystem_version_class = "unknown"
        file_id_scope = "unknown"
    elif profile_id == "missing_capability_refusal":
        capabilities["hard_links"] = False
    elif profile_id == "file_id_reuse_aba":
        outcomes["file_id_reuse_observed"] = True
        outcomes["stale_authorization_rejected"] = True

    return {
        "capabilities": capabilities,
        "file_id_scope": file_id_scope,
        "filesystem_family": filesystem_family,
        "filesystem_version_class": filesystem_version_class,
        "host_ordinal": host_ordinal,
        "interruptions": interruption_evidence,
        "locality": locality,
        "observation_count": count,
        "outcomes": outcomes,
        "status": "passed",
        "trial_count": count,
    }


def _complete_document(cross_digest: str) -> dict[str, object]:
    document = _document()
    document["source_commit"] = "git-sha1:" + "a" * 40
    document["executable_sha256"] = "sha256:" + "b" * 64
    document["contract_sha256"] = "sha256:" + "c" * 64
    document["capability_profile_sha256"] = "sha256:" + "d" * 64
    document["fixture_recipe_sha256"] = "sha256:" + "e" * 64
    document["cross_principal_evidence_sha256"] = cross_digest
    document["hosts"] = [
        {
            "architecture_class": "x86_64",
            "independence": {
                "boot_instance_distinct": True,
                "observer_attested": True,
                "os_installation_distinct": True,
                "storage_instance_distinct": True,
            },
            "ordinal": ordinal,
            "persistence_class": "physical",
            "status": "passed",
            "windows_release_class": "windows_11",
        }
        for ordinal in (1, 2)
    ]
    total_count = 0
    profiles = cast(list[dict[str, object]], document["profiles"])
    for profile in profiles:
        profile_id = cast(str, profile["id"])
        results = [_profile_result(profile_id, ordinal) for ordinal in (1, 2)]
        profile["host_results"] = results
        profile["status"] = "passed"
        count = sum(cast(int, result["trial_count"]) for result in results)
        total_count += count
        profile["totals"] = {
            "host_result_count": 2,
            "observation_count": count,
            "trial_count": count,
        }
    document["totals"] = {
        "host_count": 2,
        "observation_count": total_count,
        "profile_count": 8,
        "profile_result_count": 16,
        "trial_count": total_count,
    }
    document["criterion_7_satisfied"] = True
    return document


def _complete_pair(tmp_path: Path) -> tuple[Path, Path, dict[str, object]]:
    cross_path = _write(tmp_path / "cross.json", _complete_cross_document())
    cross_digest = validate_cross_principal_evidence_file(cross_path).evidence_sha256
    document = _complete_document(cross_digest)
    return _write(tmp_path / "independent.json", document), cross_path, document


def test_reviewed_incomplete_fixture_is_valid_bound_and_not_admitted() -> None:
    summary = validate_evidence_files(_FIXTURE, _CROSS_FIXTURE)

    assert summary == ValidationSummary(
        criterion_6_satisfied=False,
        criterion_7_satisfied=False,
        cross_principal_evidence_sha256=(
            "sha256:b1e20ff9518c52dab5e8251597e5c8344bbca18f81b4ad008c4ac7f5b41cbc9b"
        ),
        evidence_sha256=("sha256:ac326e940e5bc3250b44f5d26dbf1d7592b56edb53c563d374301c9bea3461f8"),
        host_status_counts=_HOST_STATUSES,
        profile_status_counts=_PROFILE_STATUSES,
    )
    assert _FIXTURE.read_bytes()[-1:] != b"\n"


def test_cli_prints_one_canonical_path_free_summary() -> None:
    result = _run(_FIXTURE, _CROSS_FIXTURE)

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    decoded = canonical_loads(result.stdout.removesuffix("\n"))
    assert canonical_dumps(decoded).decode() + "\n" == result.stdout
    assert cast(dict[str, object], decoded)["status"] == "valid"
    assert str(_FIXTURE) not in result.stdout
    assert str(_CROSS_FIXTURE) not in result.stdout


def test_complete_bound_pair_can_satisfy_criteria_without_admission(tmp_path: Path) -> None:
    evidence, cross_evidence, _ = _complete_pair(tmp_path)

    summary = validate_evidence_files(evidence, cross_evidence)

    assert summary.criterion_6_satisfied is True
    assert summary.criterion_7_satisfied is True
    assert summary.windows_cleanup_admitted is False
    assert summary.host_status_counts["passed"] == 2
    assert summary.profile_status_counts["passed"] == 8


def test_independent_artifact_must_bind_the_computed_companion_digest(tmp_path: Path) -> None:
    evidence, cross_evidence, document = _complete_pair(tmp_path)
    document["cross_principal_evidence_sha256"] = "sha256:" + "f" * 64
    _write(evidence, document)

    with pytest.raises(EvidenceValidationError) as caught:
        validate_evidence_files(evidence, cross_evidence)

    assert caught.value.code == "binding.cross_principal"


def test_invalid_companion_is_normalized_without_private_details(tmp_path: Path) -> None:
    companion = tmp_path / "private-account-secret.json"
    companion.write_bytes(b"{}")

    result = _run(_FIXTURE, companion)

    assert result.returncode == 1
    assert result.stderr == ""
    assert str(companion) not in result.stdout
    assert "private-account-secret" not in result.stdout
    decoded = cast(dict[str, object], json.loads(result.stdout))
    error = cast(dict[str, object], decoded["error"])
    assert error["code"] == "companion.invalid"


@pytest.mark.parametrize(
    "location",
    ("document", "host", "profile", "host_result", "capabilities", "outcomes", "interruption"),
)
def test_unknown_fields_are_rejected(tmp_path: Path, location: str) -> None:
    evidence, cross_evidence, document = _complete_pair(tmp_path)
    profile = cast(list[dict[str, object]], document["profiles"])[0]
    result = cast(list[dict[str, object]], profile["host_results"])[0]
    targets = {
        "document": document,
        "host": cast(list[dict[str, object]], document["hosts"])[0],
        "profile": profile,
        "host_result": result,
        "capabilities": cast(dict[str, object], result["capabilities"]),
        "outcomes": cast(dict[str, object], result["outcomes"]),
        "interruption": cast(list[dict[str, object]], result["interruptions"])[0],
    }
    targets[location]["unknown"] = False

    with pytest.raises(EvidenceValidationError, match="missing or unknown fields"):
        validate_evidence_files(_write(evidence, document), cross_evidence)


def test_noncanonical_and_duplicate_json_are_rejected(tmp_path: Path) -> None:
    noncanonical = tmp_path / "noncanonical.json"
    noncanonical.write_bytes(_FIXTURE.read_bytes() + b"\n")
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"schema":null,"schema":null}', encoding="utf-8")

    with pytest.raises(EvidenceValidationError, match="exact canonical bytes"):
        validate_evidence_files(noncanonical, _CROSS_FIXTURE)
    with pytest.raises(EvidenceValidationError) as caught:
        validate_evidence_files(duplicate, _CROSS_FIXTURE)
    assert caught.value.code == "evidence.invalid_json"


def test_oversized_evidence_is_rejected_before_json_parsing(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 8_388_609)

    with pytest.raises(EvidenceValidationError) as caught:
        validate_evidence_files(oversized, _CROSS_FIXTURE)

    assert caught.value.code == "evidence.too_large"


def test_host_result_limit_is_enforced_before_unattempted_claims(tmp_path: Path) -> None:
    document = _document()
    document["hosts"] = [{} for _ in range(33)]

    with pytest.raises(EvidenceValidationError) as caught:
        validate_evidence_files(_write(tmp_path / "hosts.json", document), _CROSS_FIXTURE)

    assert caught.value.code == "limits.hosts"


def test_symbolic_link_evidence_is_rejected_when_supported(tmp_path: Path) -> None:
    link = tmp_path / "evidence-link.json"
    try:
        link.symlink_to(_FIXTURE)
    except OSError as error:
        pytest.skip(f"symbolic links unavailable: {type(error).__name__}")

    with pytest.raises(EvidenceValidationError) as caught:
        validate_evidence_files(link, _CROSS_FIXTURE)

    assert caught.value.code == "evidence.not_regular"


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("source_commit", None),
        ("source_commit", "git-sha1:ABC"),
        ("executable_sha256", "sha256:ABC"),
        ("contract_sha256", "git-sha1:" + "a" * 40),
        ("capability_profile_sha256", None),
        ("fixture_recipe_sha256", "sha256:" + "F" * 64),
    ),
)
def test_attempted_evidence_requires_exact_lowercase_identities(
    tmp_path: Path, field: str, value: object
) -> None:
    evidence, cross_evidence, document = _complete_pair(tmp_path)
    document[field] = value

    with pytest.raises(EvidenceValidationError, match="required digest identity"):
        validate_evidence_files(_write(evidence, document), cross_evidence)


def test_unattempted_evidence_must_omit_identities(tmp_path: Path) -> None:
    document = _document()
    document["contract_sha256"] = "sha256:" + "a" * 64

    with pytest.raises(EvidenceValidationError, match="must omit identities"):
        validate_evidence_files(_write(tmp_path / "identity.json", document), _CROSS_FIXTURE)


def test_profile_order_and_host_ordinals_are_exact(tmp_path: Path) -> None:
    evidence, cross_evidence, document = _complete_pair(tmp_path)
    profiles = cast(list[dict[str, object]], document["profiles"])
    profiles[0], profiles[1] = profiles[1], profiles[0]
    with pytest.raises(EvidenceValidationError, match="unexpected value"):
        validate_evidence_files(_write(evidence, document), cross_evidence)

    _, _, document = _complete_pair(tmp_path)
    cast(list[dict[str, object]], document["hosts"])[1]["ordinal"] = 3
    with pytest.raises(EvidenceValidationError, match="contiguous and canonical"):
        validate_evidence_files(_write(evidence, document), cross_evidence)


@pytest.mark.parametrize(
    "mutation",
    (
        "criterion",
        "admission",
        "single_host",
        "host_independence",
        "physical_persistence",
        "interruption",
        "refusal",
        "aba",
        "aba_scope",
        "filesystem",
        "total",
    ),
)
def test_complete_claims_are_derived_from_exact_observations(tmp_path: Path, mutation: str) -> None:
    evidence, cross_evidence, document = _complete_pair(tmp_path)
    profiles = cast(list[dict[str, object]], document["profiles"])
    local_results = cast(list[dict[str, object]], profiles[0]["host_results"])
    refs_results = cast(list[dict[str, object]], profiles[1]["host_results"])
    aba_results = cast(list[dict[str, object]], profiles[7]["host_results"])
    if mutation == "criterion":
        document["criterion_7_satisfied"] = False
    elif mutation == "admission":
        document["windows_cleanup_admitted"] = True
    elif mutation == "single_host":
        local_results.pop()
        profiles[0]["totals"] = {
            "host_result_count": 1,
            "observation_count": 3,
            "trial_count": 3,
        }
        profiles[0]["status"] = "unsupported"
        totals = cast(dict[str, object], document["totals"])
        totals["profile_result_count"] = 15
        totals["trial_count"] = 17
        totals["observation_count"] = 17
    elif mutation == "host_independence":
        host = cast(list[dict[str, object]], document["hosts"])[0]
        cast(dict[str, object], host["independence"])["observer_attested"] = False
    elif mutation == "physical_persistence":
        cast(list[dict[str, object]], document["hosts"])[0]["persistence_class"] = "persistent_vm"
    elif mutation == "interruption":
        interruption = cast(list[dict[str, object]], local_results[0]["interruptions"])[0]
        interruption["status"] = "failed"
    elif mutation == "refusal":
        cast(dict[str, object], refs_results[0]["outcomes"])[
            "refused_before_authority_or_mutation"
        ] = False
    elif mutation == "aba":
        cast(dict[str, object], aba_results[0]["outcomes"])["file_id_reuse_observed"] = False
    elif mutation == "aba_scope":
        aba_results[0]["file_id_scope"] = "unknown"
    elif mutation == "filesystem":
        refs_results[0]["filesystem_family"] = "ntfs"
    else:
        cast(dict[str, object], document["totals"])["observation_count"] = 19

    with pytest.raises(EvidenceValidationError):
        validate_evidence_files(_write(evidence, document), cross_evidence)


def test_non_file_and_missing_file_errors_are_path_free(tmp_path: Path) -> None:
    directory_result = _run(tmp_path, _CROSS_FIXTURE)
    missing = tmp_path / "private-machine-name.json"
    missing_result = _run(missing, _CROSS_FIXTURE)

    for result, code in (
        (directory_result, "evidence.not_regular"),
        (missing_result, "evidence.read_failed"),
    ):
        assert result.returncode == 1
        assert result.stderr == ""
        assert str(tmp_path) not in result.stdout
        assert "private-machine-name" not in result.stdout
        decoded = cast(dict[str, object], json.loads(result.stdout))
        error = cast(dict[str, object], decoded["error"])
        assert error["code"] == code
