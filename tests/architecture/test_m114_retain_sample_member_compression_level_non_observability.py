"""Protect M114 sample-member compression-level non-observability."""

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
_DEFLATE_LEVELS = (0, 1, 6, 9)
_PROBE_PAYLOAD = (b"ludoweave-compression-level-probe\n" * 256) + bytes(range(256))


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
    return cast(_SmokeModule, _load(_SMOKE, "m114_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m114_release_artifacts"))


def _write_bundle(
    path: Path,
    *,
    names: frozenset[str],
    levels: tuple[int, ...],
    mode: int = _PRODUCER_MODE,
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for index, name in enumerate(sorted(names)):
            info = zipfile.ZipInfo(f"{_PREFIX}/{name}", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, name.encode(), compresslevel=levels[index % len(levels)])


def _write_probe(path: Path, *, level: int) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        info = zipfile.ZipInfo("probe.bin", date_time=_DATE_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, _PROBE_PAYLOAD, compresslevel=level)


def _assert_level_is_not_recovered(info: zipfile.ZipInfo) -> None:
    assert getattr(info, "compress_level", None) is None
    assert getattr(info, "_compresslevel", None) is None


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


@pytest.mark.parametrize("level", _DEFLATE_LEVELS)
def test_cpython_reopened_member_does_not_recover_exact_level(
    tmp_path: Path,
    level: int,
) -> None:
    bundle = tmp_path / f"level-{level}.zip"
    _write_probe(bundle, level=level)

    with zipfile.ZipFile(bundle) as archive:
        info = archive.infolist()[0]
        _assert_level_is_not_recovered(info)
        assert info.compress_type == zipfile.ZIP_DEFLATED
        assert info.extract_version == 20
        assert info.flag_bits == 0
        assert archive.read(info) == _PROBE_PAYLOAD


def test_distinct_requested_levels_can_produce_identical_archive_bytes(
    tmp_path: Path,
) -> None:
    level_six = tmp_path / "level-6.zip"
    level_nine = tmp_path / "level-9.zip"
    _write_probe(level_six, level=6)
    _write_probe(level_nine, level=9)

    assert level_six.read_bytes() == level_nine.read_bytes()


@pytest.mark.parametrize("level", _DEFLATE_LEVELS)
def test_complete_bundle_retains_compression_level_compatibility(
    tmp_path: Path,
    level: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"complete-level-{level}.zip"
    _write_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        levels=(level,),
    )

    output = _empty_output(tmp_path)
    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert sum(path.is_file() for path in root.rglob("*")) == 50


def test_complete_bundle_retains_mixed_compression_level_compatibility(
    tmp_path: Path,
) -> None:
    module = _smoke()
    bundle = tmp_path / "mixed-levels.zip"
    _write_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        levels=_DEFLATE_LEVELS,
    )
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert {info.flag_bits for info in infos} == {0}
        assert all(info.compress_type == zipfile.ZIP_DEFLATED for info in infos)
        assert all(getattr(info, "compress_level", None) is None for info in infos)

    output = _empty_output(tmp_path)
    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


def test_standard_writer_default_level_remains_admitted(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "default-level.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(module._EXPECTED_SAMPLE_MEMBERS):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert {info.compress_type for info in infos} == {zipfile.ZIP_DEFLATED}
        assert {info.flag_bits for info in infos} == {0}
        assert all(getattr(info, "compress_level", None) is None for info in infos)

    output = _empty_output(tmp_path)
    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


def test_level_compatibility_retains_inventory_error_precedence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = tmp_path / "wrong-inventory.zip"
    _write_bundle(
        bundle,
        names=frozenset(("README.md", "unexpected.txt")),
        levels=(0, 9),
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


def test_current_producer_level_is_writer_configuration_only(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    producer_source = _STAGER.read_text(encoding="utf-8")

    assert len(infos) == 50
    assert {info.compress_type for info in infos} == {zipfile.ZIP_DEFLATED}
    assert {info.flag_bits for info in infos} == {0}
    assert all(getattr(info, "compress_level", None) is None for info in infos)
    assert all(getattr(info, "_compresslevel", None) is None for info in infos)
    assert producer_source.count("compresslevel=9") == 1


def test_m114_adds_no_level_classifier_or_inference() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    assert "_validate_sample_compression_level" not in source
    assert "unsupported compression level" not in source
    assert "compress_level" not in source
    assert "_compresslevel" not in source


def test_m114_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m114" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m114_docs_define_level_non_observability_decision_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0097-retain-sample-member-compression-level-non-observability.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M114" in combined
    assert "retain sample-member compression-level non-observability" in combined
    assert "one compression-level non-observability decision" in combined
    assert "no exact level-9 verifier profile" in combined
    assert "no inferred compressor level" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
