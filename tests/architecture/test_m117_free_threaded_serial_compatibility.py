"""Protect M117 free-threaded serial evidence without a support promotion."""

from __future__ import annotations

import hashlib
import tomllib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github/workflows/ci.yml"
_RELEASE = _ROOT / ".github/workflows/release.yml"
_PYPROJECT = _ROOT / "pyproject.toml"
_LOCK = _ROOT / "uv.lock"
_LIFECYCLE = _ROOT / "src/ludoweave/app/lifecycle.py"
_WHEEL_SMOKE = _ROOT / "scripts/smoke_wheel.py"
_CI_SHA256 = "67fc471f84d7dde8b239bd9e92235a34f780cc3d3370b0dbf451e6a922a027f1"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_PYPROJECT_SHA256 = "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d"
_LOCK_SHA256 = "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18"
_LIFECYCLE_SHA256 = "4c39689e680359db58eeb7275a5746661c2aeb05009235bddabf0d17ff85b55e"
_WHEEL_SMOKE_SHA256 = "2727640d8696c9ff67c3f2a7a23af06b89a98d9edc40400696e4a9ed34ce464c"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_standard_cpython_package_baseline_remains_exact() -> None:
    document = tomllib.loads(_PYPROJECT.read_text(encoding="utf-8"))
    project = document["project"]

    assert project["requires-python"] == ">=3.12,<3.15"
    assert project["dependencies"] == []
    assert "Programming Language :: Python :: Implementation :: CPython" in project["classifiers"]
    assert "freethread" not in _PYPROJECT.read_text(encoding="utf-8").casefold()


def test_engine_owner_thread_contract_remains_exact() -> None:
    source = _LIFECYCLE.read_text(encoding="utf-8")

    assert source.count("self._assert_owner_thread()") == 4
    assert "self._owner_thread = get_ident()" in source
    assert 'code="engine.wrong_thread"' in source
    assert "Py_GIL_DISABLED" not in source
    assert "_is_gil_enabled" not in source


def test_m117_changes_no_workflow_runtime_metadata_or_wheel_smoke_boundary() -> None:
    assert _sha256(_CI) == _CI_SHA256
    assert _sha256(_RELEASE) == _RELEASE_SHA256
    assert _sha256(_PYPROJECT) == _PYPROJECT_SHA256
    assert _sha256(_LOCK) == _LOCK_SHA256
    assert _sha256(_LIFECYCLE) == _LIFECYCLE_SHA256
    assert _sha256(_WHEEL_SMOKE) == _WHEEL_SMOKE_SHA256
    assert not any(
        "m117" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m117_docs_bound_free_threaded_serial_compatibility() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/runtime-contract.md",
        _ROOT / "docs/rfcs/0100-retain-standard-cpython-baseline.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M117" in combined
    assert "retain standard gil cpython as the supported baseline" in folded
    assert "one free-threaded serial-compatibility decision" in folded
    assert "installed-wheel serial compatibility" in folded
    assert "no concurrent-safety claim" in folded
    assert "no graphics" in folded
    assert "no workflow" in folded
    assert "not a support promise" in folded
    assert "not a real public release observation" in folded
    assert "https://peps.python.org/pep-0779/" in combined
    assert "https://docs.python.org/3/howto/free-threading-python.html" in combined
    assert "https://docs.astral.sh/uv/concepts/python-versions/" in combined
