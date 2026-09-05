"""Protect M110 sample-member timestamp compatibility."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
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
_PRODUCER_TIME = (1980, 1, 1, 0, 0, 0)
_ALTERNATE_TIMES = (
    (1980, 1, 1, 0, 0, 2),
    (1980, 1, 2, 0, 0, 0),
    (1981, 1, 1, 0, 0, 0),
    (2026, 8, 25, 12, 34, 56),
    (2107, 12, 31, 23, 59, 58),
)


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]

    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
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
    return cast(_SmokeModule, _load(_SMOKE, "m110_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m110_release_artifacts"))


def _write_complete_bundle(
    path: Path,
    *,
    names: frozenset[str],
    date_times: tuple[tuple[int, int, int, int, int, int], ...],
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for index, name in enumerate(sorted(names)):
            date_time = date_times[index % len(date_times)]
            info = zipfile.ZipInfo(f"{_PREFIX}/{name}", date_time=date_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, name.encode(), compresslevel=9)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cpython_exposes_alternate_timestamp_and_reads_payload(tmp_path: Path) -> None:
    bundle = tmp_path / "alternate-timestamp.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        info = zipfile.ZipInfo("member.txt", date_time=_ALTERNATE_TIMES[3])
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, b"payload")
    with zipfile.ZipFile(bundle) as archive:
        observed = archive.infolist()[0]
        assert observed.date_time == _ALTERNATE_TIMES[3]
        assert archive.read(observed) == b"payload"


@pytest.mark.parametrize("date_time", _ALTERNATE_TIMES)
def test_complete_bundle_retains_alternate_timestamp_compatibility(
    tmp_path: Path,
    date_time: tuple[int, int, int, int, int, int],
) -> None:
    module = _smoke()
    bundle = tmp_path / f"timestamp-{'-'.join(str(value) for value in date_time)}.zip"
    _write_complete_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        date_times=(date_time,),
    )
    output = _empty_output(tmp_path)

    root = module._extract_bundle(
        bundle,
        output,
        version=_VERSION,
        expected_sha256=_sha256(bundle),
    )

    assert root == output / _PREFIX
    assert sum(path.is_file() for path in root.rglob("*")) == 50


def test_complete_bundle_retains_mixed_timestamp_compatibility(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "mixed-timestamps.zip"
    _write_complete_bundle(
        bundle,
        names=module._EXPECTED_SAMPLE_MEMBERS,
        date_times=(_PRODUCER_TIME, *_ALTERNATE_TIMES),
    )
    output = _empty_output(tmp_path)

    assert module._extract_bundle(bundle, output, version=_VERSION) == output / _PREFIX


def test_alternate_timestamp_retains_inventory_error_precedence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "wrong-inventory.zip"
    _write_complete_bundle(
        bundle,
        names=frozenset(("README.md",)),
        date_times=(_ALTERNATE_TIMES[3],),
    )
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("inventory mismatch must fail before staging or reads")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        module._extract_bundle(bundle, output, version=_VERSION)
    assert list(output.iterdir()) == []


def test_current_producer_remains_fixed_and_reproducible(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert {info.date_time for info in infos} == {_PRODUCER_TIME}


def test_m110_retains_m98_consistency_without_exact_timestamp_classifier() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    local_timestamp = extraction.index("_validate_sample_local_header_timestamps(")
    internal_profile = extraction.index("_validate_sample_internal_attribute_profile(")
    inventory = extraction.index("_validate_sample_inventory(observed_members)")
    assert local_timestamp < internal_profile < inventory
    assert "_validate_sample_timestamp_profile" not in source
    assert "sample bundle has an unsupported timestamp profile" not in source
    assert source.count("info.date_time") == 1
    assert "sample bundle local header timestamps are inconsistent" in source


def test_m110_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m110" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m110_docs_define_timestamp_compatibility_decision_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0093-retain-sample-member-timestamp-compatibility.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M110" in combined
    assert "retain sample-member timestamp compatibility" in combined
    assert "one central-timestamp compatibility decision" in combined
    assert "22 established architecture regressions" in combined
    assert "no timezone or UTC conversion" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
