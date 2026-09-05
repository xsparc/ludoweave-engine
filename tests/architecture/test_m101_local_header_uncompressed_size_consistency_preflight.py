"""Protect M101 local-header uncompressed-size consistency preflight."""

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
_DATE_TIME = (2026, 8, 24, 0, 0, 0)
_EOCD_SIGNATURE = b"PK\x05\x06"
_CENTRAL_SIGNATURE = b"PK\x01\x02"
_FIXED_LOCAL_HEADER_BYTES = 30
_LOCAL_COMPRESSED_SIZE_OFFSET = 18
_LOCAL_UNCOMPRESSED_SIZE_OFFSET = 22
_LOCAL_FIELD_BYTES = 4
_UNCOMPRESSED_SIZE_ERROR = "sample bundle local header uncompressed sizes are inconsistent"
_REFERENCE_UNCOMPRESSED_SIZE = 0x11223344


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_local_header_uncompressed_sizes(
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
    return cast(_SmokeModule, _load(_SMOKE, "m101_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m101_release_artifacts"))


def _size_bytes(size: int) -> bytes:
    return size.to_bytes(_LOCAL_FIELD_BYTES, "little")


def _write_small_bundle(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index in range(2):
            info = zipfile.ZipInfo(f"{_PREFIX}/member-{index}.txt", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, f"payload-{index}".encode())


def _change_local_size(path: Path, *, offset: int, member: int = -1) -> None:
    with zipfile.ZipFile(path) as archive:
        info = archive.infolist()[member]
        start = info.header_offset + offset
    data = bytearray(path.read_bytes())
    value = int.from_bytes(data[start : start + _LOCAL_FIELD_BYTES], "little")
    data[start : start + _LOCAL_FIELD_BYTES] = (value + 1).to_bytes(
        _LOCAL_FIELD_BYTES,
        "little",
    )
    path.write_bytes(data)


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


def _info(offset: int, *, size: int = _REFERENCE_UNCOMPRESSED_SIZE) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo("member.txt", date_time=_DATE_TIME)
    info.header_offset = offset
    info.file_size = size
    return info


def _snapshot(*, header_offset: int, size: bytes) -> BytesIO:
    assert len(size) == _LOCAL_FIELD_BYTES
    data = bytearray(header_offset + _FIXED_LOCAL_HEADER_BYTES)
    start = header_offset + _LOCAL_UNCOMPRESSED_SIZE_OFFSET
    data[start : start + _LOCAL_FIELD_BYTES] = size
    return BytesIO(data)


def test_cpython_ignores_local_only_uncompressed_size_mismatch_during_reads(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "uncompressed-sizes.zip"
    _write_small_bundle(bundle)
    _change_local_size(bundle, offset=_LOCAL_UNCOMPRESSED_SIZE_OFFSET)

    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        central_sizes = [info.file_size for info in infos]
        assert central_sizes == [9, 9]
        assert [
            data[
                info.header_offset + _LOCAL_UNCOMPRESSED_SIZE_OFFSET : info.header_offset
                + _LOCAL_UNCOMPRESSED_SIZE_OFFSET
                + _LOCAL_FIELD_BYTES
            ]
            for info in infos
        ] == [_size_bytes(9), _size_bytes(10)]
        assert [archive.read(info) for info in infos] == [b"payload-0", b"payload-1"]


def test_uncompressed_size_error_precedes_inventory_staging_and_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "producer-uncompressed-sizes.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    _change_local_size(bundle, offset=_LOCAL_UNCOMPRESSED_SIZE_OFFSET)
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("local-uncompressed-size policy must fail before later processing")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_UNCOMPRESSED_SIZE_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )
    assert list(output.iterdir()) == []


def test_uncompressed_size_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "uncompressed-sizes-cleanup.zip"
    _write_small_bundle(bundle)
    _change_local_size(bundle, offset=_LOCAL_UNCOMPRESSED_SIZE_OFFSET)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_UNCOMPRESSED_SIZE_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)
    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_m100_compressed_size_error_precedes_uncompressed_size_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "compressed-before-uncompressed.zip"
    _write_small_bundle(bundle)
    _change_local_size(bundle, offset=_LOCAL_COMPRESSED_SIZE_OFFSET)
    _change_local_size(bundle, offset=_LOCAL_UNCOMPRESSED_SIZE_OFFSET)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header compressed sizes are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_uncompressed_size_policy_precedes_nul_name_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "uncompressed-before-nul.zip"
    _write_small_bundle(bundle)
    _change_local_size(bundle, offset=_LOCAL_UNCOMPRESSED_SIZE_OFFSET, member=0)
    _nul_suffix_first_local_and_central_name(bundle)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_UNCOMPRESSED_SIZE_ERROR)}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_uncompressed_size_validator_accepts_empty_equal_values_and_restores_position() -> None:
    module = _smoke()
    snapshot = _snapshot(header_offset=10, size=_size_bytes(_REFERENCE_UNCOMPRESSED_SIZE))
    snapshot.seek(3)
    module._validate_sample_local_header_uncompressed_sizes(snapshot=snapshot, infos=())
    module._validate_sample_local_header_uncompressed_sizes(snapshot=snapshot, infos=(_info(10),))
    assert snapshot.tell() == 3


@pytest.mark.parametrize(
    "size",
    (b"\x45\x33\x22\x11", b"\x44\x32\x22\x11", b"\x44\x33\x23\x11", b"\x44\x33\x22\x10"),
)
def test_uncompressed_size_validator_rejects_any_local_central_mismatch(size: bytes) -> None:
    module = _smoke()
    snapshot = _snapshot(header_offset=10, size=size)
    snapshot.seek(5)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_UNCOMPRESSED_SIZE_ERROR)}$"):
        module._validate_sample_local_header_uncompressed_sizes(
            snapshot=snapshot,
            infos=(_info(10),),
        )
    assert snapshot.tell() == 5


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_local_uncompressed_sizes_match_central_sizes(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    for info in infos:
        start = info.header_offset + _LOCAL_UNCOMPRESSED_SIZE_OFFSET
        assert data[start : start + _LOCAL_FIELD_BYTES] == _size_bytes(info.file_size)


def test_m101_source_checks_uncompressed_size_after_m100_before_decoded_name_policy() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    local_crc = extraction.index("_validate_sample_local_header_crcs(")
    local_compressed_size = extraction.index("_validate_sample_local_header_compressed_sizes(")
    local_uncompressed_size = extraction.index("_validate_sample_local_header_uncompressed_sizes(")
    decoded_name = extraction.index(
        "_validate_sample_member_name(original_name=info.orig_filename)"
    )
    metadata = extraction.index("total_bytes = 0")
    assert local_crc < local_compressed_size < local_uncompressed_size < decoded_name < metadata
    helper = source[source.index("def _validate_sample_local_header_uncompressed_sizes") :]
    assert "info.header_offset" in helper
    assert "info.file_size" in helper
    assert 'to_bytes(4, "little")' in helper
    assert "zipfile._" not in helper


def test_m101_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m101" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m101_docs_define_uncompressed_size_rule_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0084-require-consistent-local-header-uncompressed-sizes.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M101" in combined
    assert "local-header uncompressed-size consistency" in combined
    assert _UNCOMPRESSED_SIZE_ERROR in combined
    assert "one four-byte local-uncompressed-size consistency classifier" in combined
    assert "no decompression or recompression" in combined
    assert "no compression-ratio policy" in combined
    assert "no payload or next-header bound" in combined
    assert "no inter-member layout validator" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    current = re.search(
        r"> Current validation: M0 through M(?P<milestone>\d+) are hosted-validated",
        readme,
    )
    project = re.search(
        r"> Project status: community-alpha release candidate \(`0\.1\.0a1`\)\. "
        r"M0 through M(?P<milestone>\d+) are hosted-validated",
        readme,
    )
    assert current is not None and project is not None
    assert current.group("milestone") == project.group("milestone")
    assert int(current.group("milestone")) >= 99
