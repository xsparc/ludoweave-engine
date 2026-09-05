"""M210 offline Windows independent-host collection-plan validation."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ludoweave.world import canonical_dumps, canonical_loads
from tests.tools.validate_windows_independent_host_collection_plan import (
    CollectionPlanValidationError,
    ValidationSummary,
    validate_collection_plan_file,
)

_ROOT = Path(__file__).parents[2]
_VALIDATOR = _ROOT / "tests/tools/validate_windows_independent_host_collection_plan.py"
_FIXTURE = _ROOT / "tests/fixtures/windows_cleanup_independent_host_collection_plan.json"


def _document() -> dict[str, object]:
    return cast(dict[str, object], canonical_loads(_FIXTURE.read_bytes()))


def _write(path: Path, document: object) -> Path:
    path.write_bytes(canonical_dumps(document) + b"\n")
    return path


def _run(plan: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, "-B", str(_VALIDATOR), str(plan)),
        check=False,
        capture_output=True,
        text=True,
    )


def _complete_document() -> dict[str, object]:
    document = _document()
    document["source_commit"] = "git-sha1:" + "a" * 40
    for field, character in (
        ("executable_sha256", "b"),
        ("independent_host_contract_sha256", "c"),
        ("collection_authority_policy_sha256", "d"),
        ("cross_principal_evidence_sha256", "e"),
        ("fixture_recipe_sha256", "f"),
        ("capability_profile_sha256", "1"),
    ):
        document[field] = "sha256:" + character * 64
    document["hosts"] = [
        {
            "architecture_class": "x86_64",
            "ordinal": ordinal,
            "persistence_class": "physical",
            "status": "not_run",
            "windows_release_class": "windows_11",
        }
        for ordinal in (1, 2)
    ]
    requirements = cast(dict[str, object], document["requirements"])
    for field in requirements:
        requirements[field] = True
    totals = cast(dict[str, object], document["totals"])
    totals["host_count"] = 2
    totals["planned_binding_count"] = 384
    document["plan_complete"] = True
    return document


def test_reviewed_fixture_is_valid_incomplete_and_non_authorizing() -> None:
    encoded = _FIXTURE.read_bytes()
    summary = validate_collection_plan_file(_FIXTURE)

    assert summary == ValidationSummary(
        collection_status="not_run",
        plan_complete=False,
        plan_sha256=f"sha256:{hashlib.sha256(encoded).hexdigest()}",
        host_count=0,
        planned_binding_count=0,
    )
    assert canonical_dumps(canonical_loads(encoded)) + b"\n" == encoded


def test_cli_prints_one_canonical_path_free_summary() -> None:
    result = _run(_FIXTURE)

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    decoded = canonical_loads(result.stdout.removesuffix("\n"))
    assert canonical_dumps(decoded).decode() + "\n" == result.stdout
    assert cast(dict[str, object], decoded)["status"] == "valid"
    assert str(_FIXTURE) not in result.stdout


def test_complete_plan_derives_bounded_cross_product_without_authority(tmp_path: Path) -> None:
    plan = _write(tmp_path / "plan.json", _complete_document())

    summary = validate_collection_plan_file(plan)

    assert summary.plan_complete is True
    assert summary.host_count == 2
    assert summary.planned_binding_count == 384
    assert summary.authority_issued is False
    assert summary.criterion_6_satisfied is False
    assert summary.criterion_7_satisfied is False
    assert summary.windows_cleanup_admitted is False


@pytest.mark.parametrize(
    ("field", "code"),
    (
        ("authority_issued", "claim.authority"),
        ("criterion_6_satisfied", "claim.criterion_6"),
        ("criterion_7_satisfied", "claim.criterion_7"),
        ("windows_cleanup_admitted", "claim.windows_cleanup"),
    ),
)
def test_authority_and_admission_claims_always_refuse(
    tmp_path: Path, field: str, code: str
) -> None:
    document = _document()
    document[field] = True
    plan = _write(tmp_path / "plan.json", document)

    with pytest.raises(CollectionPlanValidationError) as raised:
        validate_collection_plan_file(plan)

    assert raised.value.code == code


def test_false_plan_complete_claim_refuses(tmp_path: Path) -> None:
    document = _document()
    document["plan_complete"] = True
    plan = _write(tmp_path / "plan.json", document)

    with pytest.raises(CollectionPlanValidationError) as raised:
        validate_collection_plan_file(plan)

    assert raised.value.code == "claim.plan_complete"


@pytest.mark.parametrize(
    "mutation",
    (
        "unknown_field",
        "wrong_profile_order",
        "wrong_barrier_order",
        "wrong_operation",
        "wrong_total",
        "host_identifier",
        "noncontiguous_host",
    ),
)
def test_schema_matrix_identity_and_totals_refuse(tmp_path: Path, mutation: str) -> None:
    document = _complete_document()
    if mutation == "unknown_field":
        document["command"] = "arbitrary"
    elif mutation == "wrong_profile_order":
        profiles = cast(list[object], document["profiles"])
        profiles[0], profiles[1] = profiles[1], profiles[0]
    elif mutation == "wrong_barrier_order":
        barriers = cast(list[object], document["barriers"])
        barriers[0], barriers[1] = barriers[1], barriers[0]
    elif mutation == "wrong_operation":
        operations = cast(list[object], document["operations"])
        operations[-1] = "run_shell"
    elif mutation == "wrong_total":
        cast(dict[str, object], document["totals"])["planned_binding_count"] = 383
    elif mutation == "host_identifier":
        hosts = cast(list[dict[str, object]], document["hosts"])
        hosts[0]["hostname"] = "forbidden"
    else:
        hosts = cast(list[dict[str, object]], document["hosts"])
        hosts[1]["ordinal"] = 3
    plan = _write(tmp_path / "plan.json", document)

    with pytest.raises(CollectionPlanValidationError):
        validate_collection_plan_file(plan)


def test_noncanonical_json_refuses(tmp_path: Path) -> None:
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps(_document(), indent=2) + "\n", encoding="utf-8")

    with pytest.raises(CollectionPlanValidationError) as raised:
        validate_collection_plan_file(plan)

    assert raised.value.code == "plan.noncanonical"


def test_symlink_refuses_when_supported(tmp_path: Path) -> None:
    target = _write(tmp_path / "target.json", _document())
    link = tmp_path / "link.json"
    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("symbolic links are unavailable for this test account")

    with pytest.raises(CollectionPlanValidationError) as raised:
        validate_collection_plan_file(link)

    assert raised.value.code == "plan.not_regular"


def test_oversized_file_refuses_without_echoing_content(tmp_path: Path) -> None:
    plan = tmp_path / "plan.json"
    plan.write_bytes(b"x" * 1_048_577)

    with pytest.raises(CollectionPlanValidationError) as raised:
        validate_collection_plan_file(plan)

    assert raised.value.code == "plan.too_large"
    assert "x" * 32 not in raised.value.message


def test_invalid_cli_result_is_canonical_and_path_free(tmp_path: Path) -> None:
    plan = tmp_path / "private-host-name.json"
    plan.write_bytes(b"not-json")

    result = _run(plan)

    assert result.returncode == 1
    assert result.stderr == ""
    decoded = cast(dict[str, object], canonical_loads(result.stdout.removesuffix("\n")))
    assert canonical_dumps(decoded).decode() + "\n" == result.stdout
    assert decoded["status"] == "invalid"
    assert str(plan) not in result.stdout
    assert plan.name not in result.stdout


def test_validation_is_read_only(tmp_path: Path) -> None:
    plan = _write(tmp_path / "plan.json", _complete_document())
    before = plan.read_bytes()

    validate_collection_plan_file(plan)

    assert plan.read_bytes() == before
