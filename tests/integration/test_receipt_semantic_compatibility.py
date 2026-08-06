"""M23 installed receipt semantic-diff and diagnostic compatibility evidence."""

import json
import subprocess
import sys
from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

from ludoweave import __version__

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "receipt_semantic_compatibility.py"
_VALIDATOR = _ROOT / "scripts" / "receipt_semantic_evidence.py"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


def _validator() -> _Validate:
    spec = spec_from_file_location("receipt_semantic_validator", _VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("receipt-semantic evidence validator could not be loaded")
    module: ModuleType = module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(_Validate, module.validate_receipt_semantic_evidence)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def test_installed_receipt_semantic_evidence_is_repeatable_and_sanitized() -> None:
    first = _run()
    second = _run()

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is True
    assert document["cross_version_proven"] is False
    assert document["status"] == "pass"
    cases = cast(list[dict[str, object]], document["diagnostic_cases"])
    assert len(cases) == 6
    assert all(item["status"] == "rejected" for item in cases)
    contract = cast(dict[str, object], document["semantic_diff_contract"])
    assert contract["dry_run_matches_commit"] is True
    diagnostic = cast(dict[str, object], document["diagnostic_contract"])
    assert diagnostic["unknown_code_additive"] is True
    assert diagnostic["metadata_flexible"] is True
    for forbidden in (
        "credential",
        "environment",
        "expected_hash",
        "path",
        "secret",
        "timing",
        "token",
    ):
        assert forbidden not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 1),
        ("root", "cross_version_proven", True),
        ("policy", "new_diagnostic_code", "breaking"),
        ("diagnostic", "unknown_code_additive", False),
        ("semantic", "dry_run_matches_commit", False),
        ("fail_closed", "unknown_diff_field", "accepted"),
        ("case", "status", "committed"),
    ],
)
def test_exact_validator_rejects_policy_behavior_and_type_drift(
    section: str, key: str, value: object
) -> None:
    document = cast(dict[str, object], json.loads(_run().stdout))
    tampered = deepcopy(document)
    if section == "root":
        tampered[key] = value
    elif section == "policy":
        cast(dict[str, object], tampered["policy"])[key] = value
    elif section == "diagnostic":
        cast(dict[str, object], tampered["diagnostic_contract"])[key] = value
    elif section == "semantic":
        cast(dict[str, object], tampered["semantic_diff_contract"])[key] = value
    elif section == "fail_closed":
        cast(dict[str, object], tampered["reader_fail_closed"])[key] = value
    else:
        cast(list[dict[str, object]], tampered["diagnostic_cases"])[0][key] = value

    with pytest.raises(RuntimeError, match="receipt semantic installed compatibility"):
        _validator()(tampered, version=__version__)


def test_receipt_semantic_evidence_rejects_arguments() -> None:
    result = _run("--reinterpret-v1")

    assert result.returncode == 1
    assert "accepts no arguments" in result.stderr
