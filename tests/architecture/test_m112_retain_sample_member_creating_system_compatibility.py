"""Protect M112 sample-member creating-system compatibility."""

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
_REPRESENTATIVE_SYSTEMS = (0, 3, 10, 19, 255)


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]

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
    return cast(_SmokeModule, _load(_SMOKE, "m112_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m112_release_artifacts"))


def _mode_for_system(create_system: int) -> int:
    return 0o600 if create_system == 0 else _PRODUCER_MODE


def _write_bundle(
    path: Path,
    *,
    names: frozenset[str],
    systems: tuple[int, ...],
    mode: int | None = None,
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for index, name in enumerate(sorted(names)):
            create_system = systems[index % len(systems)]
            info = zipfile.ZipInfo(f"{_PREFIX}/{name}", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = create_system
            info.external_attr = (mode or _mode_for_system(create_system)) << 16
            archive.writestr(info, name.encode(), compresslevel=9)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def test_cpython_exposes_creating_system_variants_and_reads_payload(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "creating-systems.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        for create_system in _REPRESENTATIVE_SYSTEMS:
            info = zipfile.ZipInfo(f"system-{create_system}.txt", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = create_system
            info.external_attr = _PRODUCER_MODE << 16
            archive.writestr(info, str(create_system).encode())
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert tuple(info.create_system for info in infos) == _REPRESENTATIVE_SYSTEMS
        assert {info.create_version for info in infos} == {20}
        assert tuple(archive.read(info).decode() for info in infos) == tuple(
            str(value) for value in _REPRESENTATIVE_SYSTEMS
        )


@pytest.mark.parametrize("create_system", _REPRESENTATIVE_SYSTEMS)
def test_complete_bundle_retains_creating_system_compatibility(
    tmp_path: Path,
    create_system: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"system-{create_system}.zip"
    _write_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        systems=(create_system,),
    )
    output = _empty_output(tmp_path)

    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert sum(path.is_file() for path in root.rglob("*")) == 50


def test_complete_bundle_retains_mixed_creating_system_compatibility(
    tmp_path: Path,
) -> None:
    module = _smoke()
    bundle = tmp_path / "mixed-creating-systems.zip"
    _write_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        systems=_REPRESENTATIVE_SYSTEMS,
    )
    output = _empty_output(tmp_path)

    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


def test_standard_writer_default_remains_admitted(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "default-creating-system.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(module._EXPECTED_SAMPLE_MEMBERS):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())
    expected_system = zipfile.ZipInfo("default.txt").create_system
    assert expected_system in (0, 3)
    with zipfile.ZipFile(bundle) as archive:
        assert {info.create_system for info in archive.infolist()} == {expected_system}

    assert module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize("create_system", (0, 3, 10))
def test_host_marker_does_not_bypass_established_file_type_policy(
    tmp_path: Path,
    create_system: int,
) -> None:
    bundle = tmp_path / f"symlink-system-{create_system}.zip"
    _write_bundle(
        bundle,
        names=frozenset(("README.md",)),
        systems=(create_system,),
        mode=stat.S_IFLNK | 0o777,
    )

    with pytest.raises(RuntimeError, match=r"^sample bundle must not contain symbolic links$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_creating_system_compatibility_retains_inventory_error_precedence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = tmp_path / "wrong-inventory.zip"
    _write_bundle(
        bundle,
        names=frozenset(("README.md",)),
        systems=(255,),
    )
    output = _empty_output(tmp_path)

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
    assert {(info.create_version, info.create_system) for info in infos} == {(20, 3)}
    assert {info.external_attr >> 16 for info in infos} == {_PRODUCER_MODE}


def test_m112_adds_no_creating_system_classifier_or_host_interpretation() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    assert "info.create_system" not in source
    assert "_validate_sample_creating_system_profile" not in source
    assert "sample bundle has an unsupported creating system" not in source
    assert source.count("info.external_attr") == 1
    assert "mode = info.external_attr >> 16" in source
    assert "file_type not in (0, stat.S_IFREG)" in source
    assert ".chmod(" not in source


def test_m112_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m112" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m112_docs_define_creating_system_compatibility_decision_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0095-retain-sample-member-creating-system-compatibility.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M112" in combined
    assert "retain sample-member creating-system compatibility" in combined
    assert "one host-marker compatibility decision" in combined
    assert "no creating-system allowlist" in combined
    assert "no host-specific external-attribute interpretation" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
