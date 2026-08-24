"""Protect M113 sample-member compression-method compatibility."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import stat
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import NoReturn, Protocol, cast

import pytest

_ROOT = Path(__file__).parents[2]
_SMOKE = _ROOT / "scripts" / "smoke_release.py"
_STAGER = _ROOT / "scripts" / "release_artifacts.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_SMOKE_SHA256 = "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be"
_STAGER_SHA256 = "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_VERSION = "0.1.0a1"
_PREFIX = f"ludoweave-samples-{_VERSION}"
_DATE_TIME = (1980, 1, 1, 0, 0, 0)
_PRODUCER_MODE = stat.S_IFREG | 0o644
_ADMITTED_METHODS = (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]
    _SAMPLE_COMPRESSION_METHODS: frozenset[int]

    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
    ) -> Path: ...


class _StagerModule(Protocol):
    def _write_sample_bundle(self, root: Path, output: Path, version: str) -> None: ...


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


def _smoke() -> _SmokeModule:
    return cast(_SmokeModule, _load(_SMOKE, "m113_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m113_release_artifacts"))


def _write_bundle(
    path: Path,
    *,
    names: frozenset[str],
    methods: tuple[int, ...],
    mode: int = _PRODUCER_MODE,
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for index, name in enumerate(sorted(names)):
            method = methods[index % len(methods)]
            info = zipfile.ZipInfo(f"{_PREFIX}/{name}", date_time=_DATE_TIME)
            info.compress_type = method
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(
                info,
                name.encode(),
                compresslevel=9 if method == zipfile.ZIP_DEFLATED else None,
            )


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def test_cpython_exposes_admitted_methods_and_reads_payload(tmp_path: Path) -> None:
    bundle = tmp_path / "compression-methods.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        for method in _ADMITTED_METHODS:
            info = zipfile.ZipInfo(f"method-{method}.txt", date_time=_DATE_TIME)
            info.compress_type = method
            archive.writestr(
                info,
                str(method).encode(),
                compresslevel=9 if method == zipfile.ZIP_DEFLATED else None,
            )
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert tuple(info.compress_type for info in infos) == _ADMITTED_METHODS
        assert {info.create_version for info in infos} == {20}
        assert {info.extract_version for info in infos} == {20}
        assert tuple(archive.read(info).decode() for info in infos) == tuple(
            str(method) for method in _ADMITTED_METHODS
        )


@pytest.mark.parametrize("method", _ADMITTED_METHODS)
def test_complete_bundle_retains_compression_method_compatibility(
    tmp_path: Path,
    method: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"method-{method}.zip"
    _write_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        methods=(method,),
    )
    output = _empty_output(tmp_path)

    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert sum(path.is_file() for path in root.rglob("*")) == 50


def test_complete_bundle_retains_mixed_compression_method_compatibility(
    tmp_path: Path,
) -> None:
    module = _smoke()
    bundle = tmp_path / "mixed-compression-methods.zip"
    _write_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        methods=_ADMITTED_METHODS,
    )
    output = _empty_output(tmp_path)

    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


def test_standard_writer_default_stored_method_remains_admitted(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "default-stored.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        for name in sorted(module._EXPECTED_SAMPLE_MEMBERS):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())
    with zipfile.ZipFile(bundle) as archive:
        assert {info.compress_type for info in archive.infolist()} == {zipfile.ZIP_STORED}

    output = _empty_output(tmp_path)
    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


@pytest.mark.parametrize("method", _ADMITTED_METHODS)
def test_admitted_method_does_not_bypass_established_file_type_policy(
    tmp_path: Path,
    method: int,
) -> None:
    bundle = tmp_path / f"symlink-method-{method}.zip"
    _write_bundle(
        bundle,
        names=frozenset(("README.md",)),
        methods=(method,),
        mode=stat.S_IFLNK | 0o777,
    )

    with pytest.raises(RuntimeError, match=r"^sample bundle must not contain symbolic links$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize("method", (zipfile.ZIP_BZIP2, zipfile.ZIP_LZMA))
def test_other_supported_cpython_methods_remain_outside_sample_profile(
    tmp_path: Path,
    method: int,
) -> None:
    bundle = tmp_path / f"unsupported-method-{method}.zip"
    _write_bundle(
        bundle,
        names=frozenset(("README.md",)),
        methods=(method,),
    )

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle uses an unsupported compression method$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_compression_method_compatibility_retains_inventory_error_precedence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = tmp_path / "wrong-inventory.zip"
    _write_bundle(
        bundle,
        names=frozenset(("README.md", "unexpected.txt")),
        methods=_ADMITTED_METHODS,
    )
    output = _empty_output(tmp_path)
    with zipfile.ZipFile(bundle) as archive:
        assert {info.compress_type for info in archive.infolist()} == set(_ADMITTED_METHODS)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("inventory mismatch must fail before staging or reads")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, output, version=_VERSION)
    assert list(output.iterdir()) == []


def test_current_producer_remains_fixed_and_reproducible(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert {info.compress_type for info in infos} == {zipfile.ZIP_DEFLATED}
    assert {(info.create_version, info.extract_version) for info in infos} == {(20, 20)}
    assert {info.flag_bits for info in infos} == {0}


def test_m113_adds_no_exact_deflate_only_profile_or_new_decompressor() -> None:
    module = _smoke()
    source = _SMOKE.read_text(encoding="utf-8")
    assert frozenset(_ADMITTED_METHODS) == module._SAMPLE_COMPRESSION_METHODS
    assert "_validate_sample_compression_method_profile" not in source
    assert "sample bundle must use deflate" not in source
    assert source.count("info.compress_type not in _SAMPLE_COMPRESSION_METHODS") == 1
    assert "zipfile.ZIP_BZIP2" not in source
    assert "zipfile.ZIP_LZMA" not in source
    assert "zipfile.ZIP_ZSTANDARD" not in source


def test_m113_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
    assert hashlib.sha256(_SMOKE.read_bytes()).hexdigest() == _SMOKE_SHA256
    assert (
        hashlib.sha256((_ROOT / ".github/workflows/ci.yml").read_bytes()).hexdigest() == _CI_SHA256
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        _RELEASE_SHA256
    )
    assert hashlib.sha256(_STAGER.read_bytes()).hexdigest() == _STAGER_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == _PYPROJECT_SHA256
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m113" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m113_docs_define_compression_method_compatibility_decision_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0096-retain-sample-member-compression-method-compatibility.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M113" in combined
    assert "retain sample-member compression-method compatibility" in combined
    assert "one compression-method compatibility decision" in combined
    assert "no exact deflate-only profile" in combined
    assert "no new decompressor" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
