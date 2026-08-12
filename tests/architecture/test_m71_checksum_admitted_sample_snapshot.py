"""Protect M71 checksum-admitted sample snapshot parsing."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import io
import re
import sys
import zipfile
from pathlib import Path
from typing import IO, BinaryIO, Protocol, cast

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
_CHECKSUM_ERROR = "sample bundle checksum does not match staged release"


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]
    _MAX_SAMPLE_ARCHIVE_BYTES: int

    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _snapshot_sample_archive(
        self,
        source: IO[bytes],
        snapshot: IO[bytes],
        *,
        expected_sha256: str | None,
    ) -> None: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m71_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m71_release_artifacts"))


def _bundle(path: Path, names: frozenset[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(names):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def test_snapshot_copies_exact_admitted_bytes_and_rewinds() -> None:
    module = _smoke()
    data = b"checksum-admitted sample archive"
    source = io.BytesIO(data)
    snapshot = io.BytesIO()
    source.seek(7)

    module._snapshot_sample_archive(
        source,
        snapshot,
        expected_sha256=_sha256(data),
    )

    assert source.tell() == 0
    assert snapshot.tell() == 0
    assert snapshot.read() == data


def test_snapshot_is_independent_after_source_change() -> None:
    module = _smoke()
    data = b"the exact bytes used by the parser"
    source = io.BytesIO(data)
    snapshot = io.BytesIO()
    module._snapshot_sample_archive(
        source,
        snapshot,
        expected_sha256=_sha256(data),
    )

    source.seek(0)
    source.write(b"changed and restored outside the owned snapshot")
    source.truncate()
    snapshot.seek(0)

    assert snapshot.read() == data


def test_snapshot_rejects_mismatch_content_silently_and_clears_target() -> None:
    module = _smoke()
    source = io.BytesIO(b"wrong bytes")
    snapshot = io.BytesIO(b"old snapshot")

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_CHECKSUM_ERROR)}$"):
        module._snapshot_sample_archive(
            source,
            snapshot,
            expected_sha256="0" * 64,
        )

    assert source.tell() == 0
    assert snapshot.getvalue() == b""


def test_snapshot_bounds_growing_source_and_clears_target() -> None:
    module = _smoke()

    class GrowingStream:
        position = 0
        bytes_read = 0

        def seek(self, offset: int) -> int:
            self.position = offset
            return offset

        def read(self, size: int = -1) -> bytes:
            assert size >= 0
            self.position += size
            self.bytes_read += size
            return b"x" * size

    source = GrowingStream()
    snapshot = io.BytesIO()
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_CHECKSUM_ERROR)}$"):
        module._snapshot_sample_archive(
            cast(BinaryIO, source),
            snapshot,
            expected_sha256="0" * 64,
        )

    assert source.bytes_read == module._MAX_SAMPLE_ARCHIVE_BYTES + 1
    assert source.position == 0
    assert snapshot.getvalue() == b""


def test_extraction_owns_distinct_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    expected_sha256 = _sha256(bundle.read_bytes())
    output = _empty_output(tmp_path)
    observed: list[tuple[IO[bytes], IO[bytes]]] = []
    parser_inputs: list[IO[bytes]] = []
    original_snapshot = module._snapshot_sample_archive
    original_zipfile = zipfile.ZipFile

    def recording_snapshot(
        source: IO[bytes],
        snapshot: IO[bytes],
        *,
        expected_sha256: str | None,
    ) -> None:
        observed.append((source, snapshot))
        original_snapshot(source, snapshot, expected_sha256=expected_sha256)

    def recording_zipfile(file: IO[bytes]) -> zipfile.ZipFile:
        parser_inputs.append(file)
        return original_zipfile(file)

    monkeypatch.setattr(module, "_snapshot_sample_archive", recording_snapshot)
    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    root = module._extract_bundle(
        bundle,
        output,
        version=_VERSION,
        expected_sha256=expected_sha256,
    )

    assert root == output / _PREFIX
    assert len(observed) == 1
    source, snapshot = observed[0]
    assert snapshot is not source
    assert parser_inputs == [snapshot]
    assert source.closed
    assert snapshot.closed


def test_extraction_failure_closes_source_and_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    output = _empty_output(tmp_path)
    observed: list[tuple[IO[bytes], IO[bytes]]] = []
    original_snapshot = module._snapshot_sample_archive

    def recording_snapshot(
        source: IO[bytes],
        snapshot: IO[bytes],
        *,
        expected_sha256: str | None,
    ) -> None:
        observed.append((source, snapshot))
        original_snapshot(source, snapshot, expected_sha256=expected_sha256)

    monkeypatch.setattr(module, "_snapshot_sample_archive", recording_snapshot)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_CHECKSUM_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256="0" * 64,
        )

    assert len(observed) == 1
    source, snapshot = observed[0]
    assert source.closed
    assert snapshot.closed
    assert list(output.iterdir()) == []


def test_current_producer_is_admitted_through_snapshot(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    output = _empty_output(tmp_path)

    assert module._extract_bundle(
        bundle,
        output,
        version=_VERSION,
        expected_sha256=_sha256(bundle.read_bytes()),
    ) == (output / _PREFIX)


def test_m71_source_parses_owned_snapshot_after_descriptor_admission() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]

    descriptor = extraction.index("os.fstat(bundle_stream.fileno())")
    spool = extraction.index("tempfile.SpooledTemporaryFile(")
    snapshot = extraction.index("_snapshot_sample_archive(")
    parser = extraction.index("zipfile.ZipFile(snapshot_stream)")
    member_read = extraction.index("archive.open(info)")
    publication = extraction.index("staged_root.replace(root)")

    assert descriptor < spool < snapshot < parser < member_read < publication
    assert "zipfile.ZipFile(bundle_stream)" not in extraction


def test_m71_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m71" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m71_docs_define_owned_snapshot_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0054-checksum-admitted-sample-snapshot.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m71" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 70
    for term in (
        "checksum-admitted snapshot",
        "spooled temporary file",
        "16 mib",
        "exact bytes",
        "before zip parsing",
        "content-silent",
        "no persistent copy",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
