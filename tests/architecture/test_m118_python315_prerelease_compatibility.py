"""Protect M118 prerelease evidence without promoting Python 3.15 support."""

from __future__ import annotations

import hashlib
import tomllib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github/workflows/ci.yml"
_RELEASE = _ROOT / ".github/workflows/release.yml"
_PYPROJECT = _ROOT / "pyproject.toml"
_LOCK = _ROOT / "uv.lock"
_DOCTOR = _ROOT / "src/ludoweave/tools/doctor.py"
_CLI = _ROOT / "src/ludoweave/tools/cli.py"
_WHEEL_SMOKE = _ROOT / "scripts/smoke_wheel.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_DOCTOR_SHA256 = "9a27c9e2d1fd26f65f0b3c5fbca5869dcf76fa9652c48a4a8808d427b1b6f7e6"
_CLI_SHA256 = "dae6839dcd1553d8f904a634c800190d68abc4ebdc06959f35541262c9ee60f4"
_WHEEL_SMOKE_SHA256 = "2727640d8696c9ff67c3f2a7a23af06b89a98d9edc40400696e4a9ed34ce464c"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_python315_remains_outside_supported_metadata() -> None:
    document = tomllib.loads(_PYPROJECT.read_text(encoding="utf-8"))
    project = document["project"]

    assert project["requires-python"] == ">=3.12,<3.15"
    assert project["dependencies"] == []
    assert "Programming Language :: Python :: 3.15" not in project["classifiers"]
    assert "Development Status :: 3 - Alpha" in project["classifiers"]


def test_doctor_retains_the_exact_supported_cpython_boundary() -> None:
    source = _DOCTOR.read_text(encoding="utf-8")

    assert 'sys.implementation.name == "cpython"' in source
    assert "(3, 12) <= version_info[:2] < (" in source
    assert "        15," in source
    assert 'status="ok" if python_supported else "error"' in source


def test_m118_changes_no_workflow_runtime_metadata_or_wheel_smoke_boundary() -> None:
    assert _sha256(_CI) == _CI_SHA256
    assert _sha256(_RELEASE) == _RELEASE_SHA256
    assert _sha256(_PYPROJECT) == _PYPROJECT_SHA256
    assert _sha256(_LOCK) == _LOCK_SHA256
    assert _sha256(_DOCTOR) == _DOCTOR_SHA256
    assert _sha256(_CLI) == _CLI_SHA256
    assert _sha256(_WHEEL_SMOKE) == _WHEEL_SMOKE_SHA256
    assert not any(
        "m118" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m118_docs_bound_python315_prerelease_compatibility() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/runtime-contract.md",
        _ROOT / "docs/rfcs/0101-retain-python315-prerelease-outside-support.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M118" in combined
    assert "retain python 3.15 outside the supported range" in folded
    assert "one exact windows cpython 3.15.0b1" in folded
    assert "explicit metadata override" in folded
    assert "doctor correctly rejected" in folded
    assert "unsupported prerelease compatibility observation" in folded
    assert "no support promise" in folded
    assert "no workflow" in folded
    assert "not a real public release observation" in folded
    assert "https://peps.python.org/pep-0790/" in combined
    assert "https://docs.python.org/3.15/contents.html" in combined
    assert "https://docs.astral.sh/uv/reference/policies/python/" in combined
