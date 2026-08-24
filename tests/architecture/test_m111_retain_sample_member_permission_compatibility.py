"""Protect M111 sample-member permission compatibility."""

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
_ADMITTED_MODES = (
    0o400,
    0o600,
    0o777,
    stat.S_IFREG | 0o400,
    stat.S_IFREG | 0o600,
    stat.S_IFREG | 0o755,
)


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
    return cast(_SmokeModule, _load(_SMOKE, "m111_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m111_release_artifacts"))


def _write_bundle(
    path: Path,
    *,
    names: frozenset[str],
    modes: tuple[int, ...],
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for index, name in enumerate(sorted(names)):
            mode = modes[index % len(modes)]
            info = zipfile.ZipInfo(f"{_PREFIX}/{name}", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, name.encode(), compresslevel=9)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def test_cpython_exposes_permission_variants_and_reads_payload(tmp_path: Path) -> None:
    bundle = tmp_path / "permissions.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        for mode in _ADMITTED_MODES:
            info = zipfile.ZipInfo(f"mode-{mode:o}.txt", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, f"{mode:o}".encode())
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert tuple(info.external_attr >> 16 for info in infos) == _ADMITTED_MODES
        assert tuple(archive.read(info).decode() for info in infos) == tuple(
            f"{mode:o}" for mode in _ADMITTED_MODES
        )


@pytest.mark.parametrize("mode", _ADMITTED_MODES)
def test_complete_bundle_retains_permission_compatibility(
    tmp_path: Path,
    mode: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"mode-{mode:o}.zip"
    _write_bundle(bundle, names=module._EXPECTED_SAMPLE_MEMBERS, modes=(mode,))
    output = _empty_output(tmp_path)

    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert sum(path.is_file() for path in root.rglob("*")) == 50


def test_complete_bundle_retains_mixed_permission_compatibility(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "mixed-permissions.zip"
    _write_bundle(bundle, names=module._EXPECTED_SAMPLE_MEMBERS, modes=_ADMITTED_MODES)
    output = _empty_output(tmp_path)

    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


def test_standard_writer_defaults_remain_admitted(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "default-permissions.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(module._EXPECTED_SAMPLE_MEMBERS):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())
    output = _empty_output(tmp_path)

    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


@pytest.mark.parametrize(
    ("mode", "expected_error"),
    (
        (stat.S_IFLNK | 0o777, "sample bundle must not contain symbolic links"),
        (stat.S_IFDIR | 0o755, "sample bundle contains a non-regular member"),
    ),
)
def test_established_file_type_rejections_remain_exact(
    tmp_path: Path,
    mode: int,
    expected_error: str,
) -> None:
    bundle = tmp_path / f"rejected-mode-{mode:o}.zip"
    _write_bundle(bundle, names=frozenset(("README.md",)), modes=(mode,))

    with pytest.raises(RuntimeError, match=rf"^{expected_error}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_permission_variants_retain_inventory_error_precedence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = tmp_path / "wrong-inventory.zip"
    _write_bundle(
        bundle,
        names=frozenset(("README.md",)),
        modes=(stat.S_IFREG | 0o400,),
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
    assert {info.create_system for info in infos} == {3}
    assert {info.external_attr >> 16 for info in infos} == {_PRODUCER_MODE}


def test_m111_retains_m65_file_type_policy_without_permission_classifier() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    file_type = extraction.index("mode = info.external_attr >> 16")
    inventory = extraction.index("_validate_sample_inventory(observed_members)")
    assert file_type < inventory
    assert source.count("info.external_attr") == 1
    assert "stat.S_ISLNK(mode)" in source
    assert "file_type not in (0, stat.S_IFREG)" in source
    assert "_validate_sample_permission_profile" not in source
    assert "sample bundle has unsupported permissions" not in source
    assert ".chmod(" not in source


def test_m111_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m111" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m111_docs_define_permission_compatibility_decision_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0094-retain-sample-member-permission-compatibility.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M111" in combined
    assert "retain sample-member permission compatibility" in combined
    assert "one permission-bit compatibility decision" in combined
    assert "no permission restoration" in combined
    assert "no exact external-attribute profile" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
