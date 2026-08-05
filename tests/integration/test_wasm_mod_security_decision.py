"""M16 evidence is deterministic and keeps executable WASM mods deferred."""

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
_EXAMPLE = _ROOT / "examples" / "wasm_mod_security_decision.py"
_VALIDATOR = _ROOT / "scripts" / "wasm_mod_security_evidence.py"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self) -> dict[str, object]: ...


def _validator() -> _Validate:
    spec = spec_from_file_location("wasm_mod_security_evidence_validator", _VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("WASM-mod security evidence validator could not be loaded")
    module: ModuleType = module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(_Validate, module.validate_wasm_mod_security_evidence)


def _example_module() -> ModuleType:
    spec = spec_from_file_location("wasm_mod_security_decision_example", _EXAMPLE)
    if spec is None or spec.loader is None:
        raise RuntimeError("WASM-mod security example could not be loaded")
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


def test_wasm_mod_security_evidence_is_repeatable_and_deferred() -> None:
    first = _run()
    second = _run()

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["schema"] == "ludoweave.evaluation.wasm-mod-security/1"
    assert document["status"] == "deferred"
    assert document["decision"] == "retain-data-only-plugin-boundary"
    assert document["current_boundary_confirmed"] is True
    assert document["admission_ready"] is False
    assert document["ludoweave_version"] == __version__
    gates = cast(dict[str, object], document["gates"])
    assert all(value is False for value in gates.values())
    boundary = cast(dict[str, object], document["current_boundary"])
    assert boundary["distribution_requirements"] == [
        "glfw==2.10.2; extra == 'graphics'",
        "rendercanvas[glfw]==2.7.2; extra == 'graphics'",
        "wgpu==0.32.0; extra == 'graphics'",
    ]
    assert boundary["public_execution_surface_exported"] is False
    assert boundary["wasm_public_exports"] == []
    assert boundary["wasm_runtime_requirements"] == []
    assert boundary["plugin_all_preview"] is True
    assert set(cast(dict[str, object], boundary["plugin_stability"]).values()) == {"preview"}
    rejections = cast(dict[str, object], boundary["executable_manifest_fields_rejected"])
    assert set(rejections) == {"artifact", "entry_point", "host_imports", "module", "wasi", "wasm"}
    for forbidden in ("credential", "environment", "secret", "token"):
        assert forbidden not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "admission_ready", True),
        ("root", "current_boundary_confirmed", 1),
        ("boundary", "public_execution_surface_exported", True),
        ("boundary", "distribution_requirements", []),
        ("boundary", "plugin_all_preview", False),
        ("boundary", "wasm_runtime_requirements", ["wasmtime"]),
        ("boundary", "executable_manifest_fields_rejected", {}),
        ("gates", "world_mutation_command_receipt_mapping", True),
    ],
)
def test_exact_validator_rejects_security_decision_and_type_drift(
    section: str, key: str, value: object
) -> None:
    result = _run()
    document = cast(dict[str, object], json.loads(result.stdout))
    tampered = deepcopy(document)
    if section == "root":
        tampered[key] = value
    elif section == "boundary":
        cast(dict[str, object], tampered["current_boundary"])[key] = value
    else:
        cast(dict[str, object], tampered["gates"])[key] = value

    with pytest.raises(RuntimeError, match="WASM-mod installed security evidence drifted"):
        _validator()(tampered, version=__version__)


def test_wasm_mod_security_decision_rejects_arguments() -> None:
    result = _run("--execute")

    assert result.returncode == 1
    assert "accepts no arguments" in result.stderr


def test_evidence_rejects_an_unexpected_installed_requirement(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _example_module()

    def unexpected_requirements(_distribution: str) -> list[str]:
        return [
            "extism==1.0.0",
            "glfw==2.10.2; extra == 'graphics'",
            "rendercanvas[glfw]==2.7.2; extra == 'graphics'",
            "wgpu==0.32.0; extra == 'graphics'",
        ]

    monkeypatch.setattr(module.metadata, "requires", unexpected_requirements)

    with pytest.raises(AssertionError, match="inert plugin boundary"):
        cast(_Evaluate, module.evaluate)()


@pytest.mark.parametrize("requirements", [[""], ["; malformed"], [b"wasmtime==1"]])
def test_evidence_rejects_malformed_installed_requirements(
    monkeypatch: pytest.MonkeyPatch, requirements: list[object]
) -> None:
    module = _example_module()

    def malformed_requirements(_distribution: str) -> list[str]:
        return cast(list[str], requirements)

    monkeypatch.setattr(module.metadata, "requires", malformed_requirements)

    with pytest.raises(AssertionError, match="distribution requirement is malformed"):
        cast(_Evaluate, module.evaluate)()
