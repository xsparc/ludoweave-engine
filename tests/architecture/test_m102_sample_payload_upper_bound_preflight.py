"""Protect M102 compressed-payload upper-bound preflight."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
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
_DATE_TIME = (2026, 8, 25, 0, 0, 0)
_EOCD_SIGNATURE = b"PK\x05\x06"
_CENTRAL_SIGNATURE = b"PK\x01\x02"
_FIXED_LOCAL_HEADER_BYTES = 30
_LOCAL_COMPRESSED_SIZE_OFFSET = 18
_LOCAL_UNCOMPRESSED_SIZE_OFFSET = 22
_LOCAL_LENGTH_FIELDS_OFFSET = 26
_CENTRAL_COMPRESSED_SIZE_OFFSET = 20
_FIELD_BYTES = 4
_PAYLOAD_ERROR = "sample bundle member payloads are out of bounds"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_payload_bounds(
        self,
        *,
        snapshot: IO[bytes],
        infos: tuple[zipfile.ZipInfo, ...],
    ) -> None: ...

    def _validate_sample_inventory(self, observed_members: set[str]) -> None: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m102_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m102_release_artifacts"))


def _write_small_bundle(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index in range(2):
            info = zipfile.ZipInfo(f"{_PREFIX}/member-{index}.txt", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, f"payload-{index}".encode())


def _central_records(data: bytes | bytearray) -> list[tuple[int, int]]:
    end = bytes(data).rindex(_EOCD_SIGNATURE)
    cursor = int.from_bytes(data[end + 16 : end + 20], "little")
    records: list[tuple[int, int]] = []
    while cursor < end and bytes(data[cursor : cursor + 4]) == _CENTRAL_SIGNATURE:
        name_size = int.from_bytes(data[cursor + 28 : cursor + 30], "little")
        extra_size = int.from_bytes(data[cursor + 30 : cursor + 32], "little")
        comment_size = int.from_bytes(data[cursor + 32 : cursor + 34], "little")
        next_cursor = cursor + 46 + name_size + extra_size + comment_size
        records.append((cursor, next_cursor))
        cursor = next_cursor
    return records


def _change_both_compressed_sizes(path: Path, *, member: int, delta: int) -> None:
    with zipfile.ZipFile(path) as archive:
        info = archive.infolist()[member]
        value = info.compress_size + delta
        local_offset = info.header_offset + _LOCAL_COMPRESSED_SIZE_OFFSET
    data = bytearray(path.read_bytes())
    central_offset = _central_records(data)[member][0] + _CENTRAL_COMPRESSED_SIZE_OFFSET
    encoded = value.to_bytes(_FIELD_BYTES, "little")
    data[local_offset : local_offset + _FIELD_BYTES] = encoded
    data[central_offset : central_offset + _FIELD_BYTES] = encoded
    path.write_bytes(data)


def _change_local_uncompressed_size(path: Path, *, member: int = 0) -> None:
    with zipfile.ZipFile(path) as archive:
        start = archive.infolist()[member].header_offset + _LOCAL_UNCOMPRESSED_SIZE_OFFSET
    data = bytearray(path.read_bytes())
    value = int.from_bytes(data[start : start + _FIELD_BYTES], "little") + 1
    data[start : start + _FIELD_BYTES] = value.to_bytes(_FIELD_BYTES, "little")
    path.write_bytes(data)


def _nul_suffix_first_local_and_central_name(path: Path) -> None:
    data = bytearray(path.read_bytes())
    first, *_ = _central_records(data)
    name_size = int.from_bytes(data[first[0] + 28 : first[0] + 30], "little")
    data[first[0] + 46 + name_size - 1] = 0
    local_offset = int.from_bytes(data[first[0] + 42 : first[0] + 46], "little")
    data[local_offset + _FIXED_LOCAL_HEADER_BYTES + name_size - 1] = 0
    path.write_bytes(data)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _archive_state(path: Path) -> tuple[BytesIO, tuple[zipfile.ZipInfo, ...]]:
    data = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        infos = tuple(archive.infolist())
    return BytesIO(data), infos


def _payload_end(data: bytes, info: zipfile.ZipInfo) -> int:
    start = info.header_offset + _LOCAL_LENGTH_FIELDS_OFFSET
    name_length = int.from_bytes(data[start : start + 2], "little")
    extra_length = int.from_bytes(data[start + 2 : start + 4], "little")
    return (
        info.header_offset
        + _FIXED_LOCAL_HEADER_BYTES
        + name_length
        + extra_length
        + info.compress_size
    )


def test_cpython_delays_matching_compressed_size_overlap_until_member_read(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "overlap.zip"
    _write_small_bundle(bundle)
    _change_both_compressed_sizes(bundle, member=0, delta=1)
    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert [info.compress_size for info in infos] == [12, 11]
        assert _payload_end(data, infos[0]) == infos[1].header_offset + 1
        with pytest.raises(zipfile.BadZipFile):
            archive.read(infos[0])
        assert archive.read(infos[1]) == b"payload-1"


def test_payload_bound_error_precedes_inventory_staging_and_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "producer-overlap.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    _change_both_compressed_sizes(bundle, member=0, delta=1)
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("payload bound must fail before later processing")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PAYLOAD_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )
    assert list(output.iterdir()) == []


def test_payload_bound_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "overlap-cleanup.zip"
    _write_small_bundle(bundle)
    _change_both_compressed_sizes(bundle, member=0, delta=1)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PAYLOAD_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)
    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_m101_uncompressed_size_error_precedes_payload_bound(tmp_path: Path) -> None:
    bundle = tmp_path / "uncompressed-before-payload.zip"
    _write_small_bundle(bundle)
    _change_both_compressed_sizes(bundle, member=0, delta=1)
    _change_local_uncompressed_size(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header uncompressed sizes are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_payload_bound_precedes_nul_name_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "payload-before-nul.zip"
    _write_small_bundle(bundle)
    _change_both_compressed_sizes(bundle, member=0, delta=1)
    _nul_suffix_first_local_and_central_name(bundle)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PAYLOAD_ERROR)}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize("member", (0, -1))
def test_payload_bound_validator_rejects_next_header_or_directory_overlap(
    tmp_path: Path,
    member: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"overlap-{member}.zip"
    _write_small_bundle(bundle)
    _change_both_compressed_sizes(bundle, member=member, delta=1)
    snapshot, infos = _archive_state(bundle)
    snapshot.seek(5)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PAYLOAD_ERROR)}$"):
        module._validate_sample_payload_bounds(snapshot=snapshot, infos=infos)
    assert snapshot.tell() == 5


def test_payload_bound_validator_accepts_exact_bounds_empty_and_gap(
    tmp_path: Path,
) -> None:
    module = _smoke()
    exact = tmp_path / "exact.zip"
    _write_small_bundle(exact)
    snapshot, infos = _archive_state(exact)
    snapshot.seek(3)
    module._validate_sample_payload_bounds(snapshot=snapshot, infos=())
    module._validate_sample_payload_bounds(snapshot=snapshot, infos=infos)
    assert snapshot.tell() == 3

    gap = tmp_path / "gap.zip"
    _write_small_bundle(gap)
    _change_both_compressed_sizes(gap, member=0, delta=-1)
    gap_snapshot, gap_infos = _archive_state(gap)
    gap_snapshot.seek(7)
    module._validate_sample_payload_bounds(snapshot=gap_snapshot, infos=gap_infos)
    assert gap_snapshot.tell() == 7


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_payloads_end_at_the_next_header_or_directory(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    directory_offset = int.from_bytes(
        data[data.rindex(_EOCD_SIGNATURE) + 16 : data.rindex(_EOCD_SIGNATURE) + 20],
        "little",
    )
    limits = (*(info.header_offset for info in infos[1:]), directory_offset)
    assert len(infos) == 50
    assert all(_payload_end(data, info) == limit for info, limit in zip(infos, limits, strict=True))


def test_m102_source_checks_payload_bounds_after_m101_before_decoded_name_policy() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    local_compressed_size = extraction.index("_validate_sample_local_header_compressed_sizes(")
    local_uncompressed_size = extraction.index("_validate_sample_local_header_uncompressed_sizes(")
    payload_bounds = extraction.index("_validate_sample_payload_bounds(")
    decoded_name = extraction.index(
        "_validate_sample_member_name(original_name=info.orig_filename)"
    )
    metadata = extraction.index("total_bytes = 0")
    assert (
        local_compressed_size < local_uncompressed_size < payload_bounds < decoded_name < metadata
    )
    helper = source[source.index("def _validate_sample_payload_bounds") :]
    assert "info.header_offset" in helper
    assert "info.compress_size" in helper
    assert "_read_final_sample_eocd" in helper
    assert "archive.read" not in helper
    assert "zipfile._" not in helper


def test_m102_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m102" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m102_docs_define_payload_bound_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0085-bound-sample-member-payloads.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M102" in combined
    assert "compressed-payload upper-bound preflight" in combined
    assert _PAYLOAD_ERROR in combined
    assert "one compressed-payload upper-bound classifier" in combined
    assert "no decompression or recompression" in combined
    assert "no exact-contiguity requirement" in combined
    assert "no gap or adjacency ban" in combined
    assert "no payload-integrity certification" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
