"""Protect M116 sample-bundle semantic portability apart from byte identity."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import sys
import zipfile
import zlib
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


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts = str(_ROOT / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts)
    return module


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m116_release_artifacts"))


def _smoke() -> _SmokeModule:
    return cast(_SmokeModule, _load(_SMOKE, "m116_smoke_release"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _recompress(source: Path, output: Path, *, level: int) -> None:
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(output, "w") as rewritten:
        for existing in original.infolist():
            info = zipfile.ZipInfo(existing.filename, date_time=existing.date_time)
            info.compress_type = existing.compress_type
            info.create_system = existing.create_system
            info.external_attr = existing.external_attr
            rewritten.writestr(info, original.read(existing), compresslevel=level)


def _tree(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_distinct_deflate_bytes_extract_to_the_same_sample_tree(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.zip"
    alternate = tmp_path / "alternate.zip"
    _stager()._write_sample_bundle(_ROOT, baseline, _VERSION)
    _recompress(baseline, alternate, level=1)

    assert baseline.read_bytes() != alternate.read_bytes()
    assert _sha256(baseline) != _sha256(alternate)
    with zipfile.ZipFile(alternate) as archive:
        assert {info.compress_type for info in archive.infolist()} == {zipfile.ZIP_DEFLATED}
        assert archive.testzip() is None

    baseline_output = tmp_path / "baseline-output"
    alternate_output = tmp_path / "alternate-output"
    baseline_output.mkdir()
    alternate_output.mkdir()
    baseline_root = _smoke()._extract_bundle(baseline, baseline_output, version=_VERSION)
    alternate_root = _smoke()._extract_bundle(alternate, alternate_output, version=_VERSION)

    assert len(_tree(baseline_root)) == 50
    assert _tree(baseline_root) == _tree(alternate_root)


def test_deflate_method_and_runtime_decoder_are_available() -> None:
    assert zipfile.ZIP_DEFLATED == 8
    assert zlib.ZLIB_VERSION
    assert zlib.ZLIB_RUNTIME_VERSION


def test_release_smoke_has_no_fixed_sample_digest_or_compressor_identity() -> None:
    source = _SMOKE.read_text(encoding="utf-8")

    assert "52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3" not in source
    assert "d592e99c8c3a65ae63f0cf89ed7eff6094365ca98ba58d08c2099fac4316834b" not in source
    assert "ZLIB_VERSION" not in source
    assert "ZLIBNG_VERSION" not in source
    assert "ZLIB_RUNTIME_VERSION" not in source


def test_fixed_producer_remains_deflated_without_runtime_branching() -> None:
    source = _STAGER.read_text(encoding="utf-8")

    assert source.count("info.compress_type = zipfile.ZIP_DEFLATED") == 1
    assert source.count("compresslevel=9") == 1
    assert "sys.version_info" not in source
    assert "sys.platform" not in source


def test_m116_changes_no_workflow_producer_verifier_dependency_or_package_boundary() -> None:
    assert _sha256(_CI) == _CI_SHA256
    assert _sha256(_RELEASE) == _RELEASE_SHA256
    assert _sha256(_SMOKE) == _SMOKE_SHA256
    assert _sha256(_STAGER) == _STAGER_SHA256
    assert _sha256(_REPRODUCIBILITY) == _REPRODUCIBILITY_SHA256
    assert _sha256(_ROOT / "pyproject.toml") == _PYPROJECT_SHA256
    assert _sha256(_ROOT / "uv.lock") == _LOCK_SHA256
    assert not any(
        "m116" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m116_docs_separate_semantic_portability_from_byte_identity() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0099-separate-sample-semantic-portability.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M116" in combined
    assert "separate sample-bundle semantic portability from byte identity" in combined
    assert "one sample-bundle semantic-portability decision" in combined
    assert "cross-runtime producer-consumer compatibility" in combined
    assert "no cross-runtime byte-identity claim" in combined
    assert "no alternate compression method" in combined
    assert "no workflow" in combined
    assert "not a general ZIP interoperability claim" in combined
    assert "not a real public release observation" in combined
