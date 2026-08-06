"""Installed M21 receipt-reader evidence and exact validator tests."""

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
_EXAMPLE = _ROOT / "examples" / "receipt_reader.py"
_VALIDATOR = _ROOT / "scripts" / "receipt_reader_evidence.py"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


def _validator() -> _Validate:
    spec = spec_from_file_location("receipt_reader_validator", _VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("receipt-reader evidence validator could not be loaded")
    module: ModuleType = module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(_Validate, module.validate_receipt_reader_evidence)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def test_installed_receipt_reader_evidence_is_repeatable_and_sanitized() -> None:
    first = _run()
    second = _run()

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["schema"] == "ludoweave.example.receipt-reader/1"
    assert document["receipt_protocol"] == "ludoweave.receipt/1"
    assert document["ludoweave_version"] == __version__
    baseline = cast(dict[str, object], document["baseline"])
    assert baseline["cross_version_proven"] is False
    assert baseline["evidence_level"] == "single-version-baseline"
    for forbidden in (
        "sha256:",
        "credential",
        "environment",
        "path",
        "timing",
        "token",
    ):
        assert forbidden not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "receipt_protocol", "ludoweave.receipt/2"),
        ("root", "schema", "ludoweave.example.receipt-reader/2"),
        ("baseline", "cross_version_proven", 0),
        ("failures", "oversized", "world.receipt.malformed"),
        ("limits", "max_outcomes", True),
        ("case", "wire_round_trip", False),
    ],
)
def test_exact_validator_rejects_value_and_type_drift(
    section: str, key: str, value: object
) -> None:
    document = cast(dict[str, object], json.loads(_run().stdout))
    tampered = deepcopy(document)
    if section == "root":
        tampered[key] = value
    elif section == "case":
        cases = cast(list[dict[str, object]], tampered["cases"])
        cases[0][key] = value
    else:
        cast(dict[str, object], tampered[section])[key] = value

    with pytest.raises(RuntimeError, match="installed receipt-reader evidence drifted"):
        _validator()(tampered, version=__version__)


def test_receipt_reader_example_rejects_arguments() -> None:
    result = _run("--fixture")

    assert result.returncode == 1
    assert "accepts no arguments" in result.stderr
