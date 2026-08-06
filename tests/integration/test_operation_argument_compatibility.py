"""M22 installed operation-argument compatibility evidence."""

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
_EXAMPLE = _ROOT / "examples" / "operation_argument_compatibility.py"
_VALIDATOR = _ROOT / "scripts" / "operation_argument_evidence.py"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


def _validator() -> _Validate:
    spec = spec_from_file_location("operation_argument_validator", _VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("operation-argument evidence validator could not be loaded")
    module: ModuleType = module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(_Validate, module.validate_operation_argument_evidence)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def test_installed_operation_argument_evidence_is_repeatable_and_sanitized() -> None:
    first = _run()
    second = _run()

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is True
    assert document["cross_version_proven"] is False
    contracts = cast(list[dict[str, object]], document["contracts"])
    assert len(contracts) == 7
    assert all(contract["valid_status"] == "committed" for contract in contracts)
    assert all(contract["missing_required_status"] == "rejected" for contract in contracts)
    assert all(contract["unexpected_field_status"] == "rejected" for contract in contracts)
    for forbidden in ("credential", "environment", "message", "path", "secret", "timing", "token"):
        assert forbidden not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 1),
        ("root", "cross_version_proven", True),
        ("policy", "same_identity_change", "allowed"),
        ("contract", "valid_status", "rejected"),
        ("contract", "required", ["entity"]),
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
    else:
        cast(list[dict[str, object]], tampered["contracts"])[0][key] = value

    with pytest.raises(RuntimeError, match="operation-argument installed compatibility"):
        _validator()(tampered, version=__version__)


def test_operation_argument_evidence_rejects_arguments() -> None:
    result = _run("--change-policy")

    assert result.returncode == 1
    assert "accepts no arguments" in result.stderr
