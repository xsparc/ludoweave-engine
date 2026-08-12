"""Protect M68 bounded sample-archive container admission."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import stat
import sys
import tempfile
import zipfile
from collections.abc import Sequence
from pathlib import Path
from types import SimpleNamespace
from typing import IO, NoReturn, Protocol, cast

import pytest

_ROOT = Path(__file__).parents[2]
_SMOKE = _ROOT / "scripts" / "smoke_release.py"
_STAGER = _ROOT / "scripts" / "release_artifacts.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_STAGER_SHA256 = "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_VERSION = "0.1.0a1"
_PREFIX = f"ludoweave-samples-{_VERSION}"


class _SmokeModule(Protocol):
    _MAX_SAMPLE_ARCHIVE_BYTES: int
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]

    def _extract_bundle(self, bundle: Path, output: Path, *, version: str) -> Path: ...

    def _validate_sample_archive_source(self, *, mode: int, size: int) -> None: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m68_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m68_release_artifacts"))


def _bundle(path: Path, names: Sequence[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.writestr(f"{_PREFIX}/{name}", name.encode())


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def _fake_stat(*, mode: int, size: int) -> os.stat_result:
    return cast(os.stat_result, SimpleNamespace(st_mode=mode, st_size=size))


def test_m68_defines_regular_file_and_sixteen_mib_archive_boundary() -> None:
    module = _smoke()

    assert module._MAX_SAMPLE_ARCHIVE_BYTES == 16 * 1024 * 1024
    module._validate_sample_archive_source(
        mode=stat.S_IFREG,
        size=module._MAX_SAMPLE_ARCHIVE_BYTES,
    )
    with pytest.raises(RuntimeError, match=r"^sample bundle archive is too large$"):
        module._validate_sample_archive_source(
            mode=stat.S_IFREG,
            size=module._MAX_SAMPLE_ARCHIVE_BYTES + 1,
        )
    with pytest.raises(RuntimeError, match=r"^sample bundle is not a regular file$"):
        module._validate_sample_archive_source(mode=stat.S_IFIFO, size=1)


@pytest.mark.parametrize(
    ("metadata", "message"),
    (
        (
            _fake_stat(mode=stat.S_IFREG, size=(16 * 1024 * 1024) + 1),
            "sample bundle archive is too large",
        ),
        (
            _fake_stat(mode=stat.S_IFIFO, size=1),
            "sample bundle is not a regular file",
        ),
    ),
)
def test_invalid_container_fails_before_zip_parser_or_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    metadata: os.stat_result,
    message: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / "unadmitted.zip"
    bundle.write_bytes(b"not parsed")
    output = _empty_output(tmp_path)

    def controlled_fstat(file_descriptor: int) -> os.stat_result:
        del file_descriptor
        return metadata

    def forbidden_zipfile(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("an unadmitted container must not reach the ZIP parser")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("an unadmitted container must not create staging output")

    monkeypatch.setattr(os, "fstat", controlled_fstat)
    monkeypatch.setattr(zipfile, "ZipFile", forbidden_zipfile)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(message)}$") as caught:
        module._extract_bundle(bundle, output, version=_VERSION)

    assert str(bundle) not in str(caught.value)
    assert list(output.iterdir()) == []


def test_obvious_nonregular_container_fails_before_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "directory.zip"
    bundle.mkdir()
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("an obvious non-regular source must not be opened")

    monkeypatch.setattr(Path, "open", forbidden_open)

    with pytest.raises(RuntimeError, match=r"^sample bundle is not a regular file$") as caught:
        module._extract_bundle(bundle, output, version=_VERSION)

    assert str(bundle) not in str(caught.value)
    assert list(output.iterdir()) == []


def test_valid_archive_is_parsed_from_the_admitted_open_handle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "valid.zip"
    _bundle(bundle, tuple(sorted(module._EXPECTED_SAMPLE_MEMBERS)))
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    observed: list[str | os.PathLike[str] | IO[bytes]] = []

    def recording_zipfile(
        file: str | os.PathLike[str] | IO[bytes],
    ) -> zipfile.ZipFile:
        observed.append(file)
        return original_zipfile(file)

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert len(observed) == 1
    assert not isinstance(observed[0], (str, os.PathLike))
    admitted_handle = observed[0]
    assert admitted_handle.closed


def test_current_producer_stays_well_below_archive_limit(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    assert 0 < bundle.stat().st_size < module._MAX_SAMPLE_ARCHIVE_BYTES
    assert bundle.stat().st_size * 100 < module._MAX_SAMPLE_ARCHIVE_BYTES


def test_m68_source_validates_same_open_handle_before_zipfile_construction() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction_source = source[source.index("def _extract_bundle") :]

    path_stat = extraction_source.index("bundle.stat()")
    path_admission = extraction_source.index("_validate_sample_archive_source(", path_stat)
    open_handle = extraction_source.index('bundle.open("rb")')
    descriptor_stat = extraction_source.index("os.fstat(bundle_stream.fileno())")
    descriptor_admission = extraction_source.index(
        "_validate_sample_archive_source(", descriptor_stat
    )
    parser = extraction_source.index("zipfile.ZipFile(bundle_stream)")
    inventory = extraction_source.index("_validate_sample_inventory(observed_members)")

    assert (
        path_stat
        < path_admission
        < open_handle
        < descriptor_stat
        < descriptor_admission
        < parser
        < inventory
    )


def test_m68_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "ci.yml").read_bytes()).hexdigest()
        == _CI_SHA256
    )
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "release.yml").read_bytes()).hexdigest()
        == _RELEASE_SHA256
    )
    assert hashlib.sha256(_STAGER.read_bytes()).hexdigest() == _STAGER_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m68" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m68_docs_define_preparser_input_boundary_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0051-bounded-sample-archive-container.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m68" in document for document in documents)

    for term in (
        "16 mib",
        "regular file",
        "before",
        "zipfile",
        "same opened handle",
        "content-silent",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
