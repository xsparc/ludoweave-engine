"""M20 installed evidence retains experimental command/receipt stability."""

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
_EXAMPLE = _ROOT / "examples" / "command_receipt_stability_decision.py"
_VALIDATOR = _ROOT / "scripts" / "command_receipt_stability_evidence.py"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self) -> dict[str, object]: ...


def _validator() -> _Validate:
    spec = spec_from_file_location("command_receipt_stability_validator", _VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("command/receipt evidence validator could not be loaded")
    module: ModuleType = module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(_Validate, module.validate_command_receipt_stability_evidence)


def _example_module() -> ModuleType:
    spec = spec_from_file_location("command_receipt_stability_example", _EXAMPLE)
    if spec is None or spec.loader is None:
        raise RuntimeError("command/receipt evidence example could not be loaded")
    module: ModuleType = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def test_installed_command_receipt_evidence_is_repeatable_and_deferred() -> None:
    first = _run()
    second = _run()

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["schema"] == "ludoweave.evaluation.command-receipt-stability/1"
    assert document["status"] == "deferred"
    assert document["decision"] == "retain-experimental-command-receipt"
    assert document["current_boundary_confirmed"] is True
    assert document["promotion_ready"] is False
    assert document["ludoweave_version"] == __version__
    gates = cast(dict[str, object], document["promotion_gates"])
    assert all(value is False for value in gates.values())
    boundary = cast(dict[str, object], document["current_boundary"])
    readers = cast(dict[str, object], boundary["public_readers"])
    assert readers == {
        "command_envelope": True,
        "command_transaction": True,
        "transaction_receipt": False,
    }
    assert boundary["agent_conformance_passed"] is True
    behavior = cast(dict[str, object], boundary["behavior"])
    assert behavior["dry_run_atomic"] is True
    assert behavior["commit_consistent"] is True
    assert behavior["stale_atomic"] is True
    assert behavior["failed_batch_atomic"] is True
    assert behavior["unsupported_hash_algorithm_atomic"] is True
    for forbidden in ("credential", "environment", "path", "secret", "timing", "token"):
        assert forbidden not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "promotion_ready", True),
        ("root", "current_boundary_confirmed", 1),
        ("boundary", "agent_conformance_passed", False),
        ("boundary", "public_readers", {}),
        ("behavior", "failed_batch_atomic", False),
        ("gates", "external_consumer_feedback", True),
    ],
)
def test_exact_validator_rejects_decision_and_type_drift(
    section: str, key: str, value: object
) -> None:
    document = cast(dict[str, object], json.loads(_run().stdout))
    tampered = deepcopy(document)
    if section == "root":
        tampered[key] = value
    elif section == "boundary":
        cast(dict[str, object], tampered["current_boundary"])[key] = value
    elif section == "behavior":
        boundary = cast(dict[str, object], tampered["current_boundary"])
        cast(dict[str, object], boundary["behavior"])[key] = value
    else:
        cast(dict[str, object], tampered["promotion_gates"])[key] = value

    with pytest.raises(RuntimeError, match="command/receipt installed stability evidence drifted"):
        _validator()(tampered, version=__version__)


def test_evidence_rejects_arguments() -> None:
    result = _run("--promote")

    assert result.returncode == 1
    assert "accepts no arguments" in result.stderr


def test_evidence_rejects_unrecorded_stability_promotion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _example_module()
    stability = cast(dict[str, str], module.world_stability)
    changed = dict(stability)
    changed["CommandEnvelope"] = "preview"
    monkeypatch.setattr(module, "world_stability", changed)

    with pytest.raises(AssertionError, match="command/receipt boundary"):
        cast(_Evaluate, module.evaluate)()
