"""Protect M115's fixed-environment sample-bundle reproducibility scope."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import sys
import zipfile
from pathlib import Path
from typing import Protocol, cast

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github/workflows/ci.yml"
_RELEASE = _ROOT / ".github/workflows/release.yml"
_SMOKE = _ROOT / "scripts/smoke_release.py"
_STAGER = _ROOT / "scripts/release_artifacts.py"
_REPRODUCIBILITY = _ROOT / "scripts/verify_distribution_reproducibility.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_SMOKE_SHA256 = "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be"
_STAGER_SHA256 = "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca"
_REPRODUCIBILITY_SHA256 = "51bada3fdeb4aaf3a5af81347917c44cc9c042dfde78bd8802e51fdecb6d4e45"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_VERSION = "0.1.0a1"


class _StagerModule(Protocol):
    def _write_sample_bundle(self, root: Path, output: Path, version: str) -> None: ...


def _load_stager() -> _StagerModule:
    spec = importlib.util.spec_from_file_location("m115_release_artifacts", _STAGER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return cast(_StagerModule, module)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_current_environment_repeats_identical_sample_bundle_bytes(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    stager = _load_stager()

    stager._write_sample_bundle(_ROOT, first, _VERSION)
    stager._write_sample_bundle(_ROOT, second, _VERSION)

    assert first.read_bytes() == second.read_bytes()
    assert _sha256(first) == _sha256(second)
    with zipfile.ZipFile(first) as archive:
        assert len(archive.infolist()) == 50
        assert archive.testzip() is None


def test_release_build_and_sample_staging_share_the_baseline_job() -> None:
    source = _RELEASE.read_text(encoding="utf-8")
    baseline = source.index("- name: Install uv and baseline CPython")
    build = source.index("- name: Build source and wheel distributions")
    stage = source.index("- name: Stage release inputs")
    smoke = source.index("- name: Smoke-test staged release")

    assert 'python-version: "3.12"' in source[baseline:build]
    assert baseline < build < stage < smoke


def test_ci_stages_samples_before_supported_runtime_compatibility_tests() -> None:
    source = _CI.read_text(encoding="utf-8")
    baseline = source.index("- name: Install uv and baseline CPython")
    build = source.index("- name: Build sdist and wheel")
    stage = source.index("- name: Stage release candidate")
    compatibility = source.index("- name: Run Ubuntu CPython 3.13 tests")

    assert 'python-version: "3.12"' in source[baseline:build]
    assert baseline < build < stage < compatibility


def test_distribution_reproducibility_contract_remains_wheel_and_sdist_only() -> None:
    source = _REPRODUCIBILITY.read_text(encoding="utf-8")

    assert 'name.endswith(".whl")' in source
    assert 'name.endswith(".tar.gz")' in source
    assert "len(files) != 2" in source
    assert "release_artifacts" not in source
    assert ".zip" not in source


def test_sample_producer_keeps_fixed_configuration_without_runtime_identity() -> None:
    source = _STAGER.read_text(encoding="utf-8")

    assert source.count("compresslevel=9") == 1
    assert "ZLIB_VERSION" not in source
    assert "ZLIBNG_VERSION" not in source
    assert "ZLIB_RUNTIME_VERSION" not in source
    assert "sys.version_info" not in source
    assert "sys.platform" not in source


def test_m115_changes_no_workflow_producer_verifier_dependency_or_package_boundary() -> None:
    assert _sha256(_CI) == _CI_SHA256
    assert _sha256(_RELEASE) == _RELEASE_SHA256
    assert _sha256(_SMOKE) == _SMOKE_SHA256
    assert _sha256(_STAGER) == _STAGER_SHA256
    assert _sha256(_REPRODUCIBILITY) == _REPRODUCIBILITY_SHA256
    assert _sha256(_ROOT / "pyproject.toml") == _PYPROJECT_SHA256
    assert _sha256(_ROOT / "uv.lock") == _LOCK_SHA256
    assert not any(
        "m115" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m115_docs_scope_sample_byte_reproducibility_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0098-scope-sample-bundle-byte-reproducibility.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M115" in combined
    assert "scope sample-bundle byte reproducibility to the release environment" in combined
    assert "one sample-bundle reproducibility-scope decision" in combined
    assert "no cross-runtime byte-identity claim" in combined
    assert "no compressor-identity manifest field" in combined
    assert "no workflow" in combined
    assert "not a general reproducible-build claim" in combined
    assert "not a real public release observation" in combined
