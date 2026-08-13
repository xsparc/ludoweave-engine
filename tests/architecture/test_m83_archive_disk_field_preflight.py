"""Protect M83 conventional archive disk-field preflight."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import io
import re
import struct
import sys
import tempfile
import zipfile
import zlib
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
_EOCD_SIGNATURE = b"PK\x05\x06"
_UNICODE_PATH_ID = 0x7075
_ZIP64_ID = 0x0001
_DISK_ERROR = "sample bundle uses unsupported archive disk fields"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_archive_disk_fields(self, *, snapshot: IO[bytes]) -> None: ...

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
    return cast(_SmokeModule, _load(_SMOKE, "m83_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m83_release_artifacts"))


def _write_member(
    archive: zipfile.ZipFile,
    *,
    name: str,
    payload: bytes,
    comment: bytes = b"",
    extra: bytes = b"",
    hidden_suffix: str = "",
) -> None:
    info = zipfile.ZipInfo("placeholder")
    info.filename = f"{name}{hidden_suffix}"
    info.orig_filename = info.filename
    info.comment = comment
    info.extra = extra
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, payload)


def _write_bundle(
    path: Path,
    *,
    hidden_suffix: str = "",
    member_comment: bytes = b"",
    extra: bytes = b"",
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        _write_member(
            archive,
            name=f"{_PREFIX}/README.md",
            hidden_suffix=hidden_suffix,
            payload=b"sample",
            comment=member_comment,
            extra=extra,
        )


def _set_archive_disk_fields(path: Path, *, disk: int, central_disk: int) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    data[end + 4 : end + 6] = disk.to_bytes(2, "little")
    data[end + 6 : end + 8] = central_disk.to_bytes(2, "little")
    path.write_bytes(data)


def _set_member_volume(path: Path, *, volume: int) -> None:
    data = bytearray(path.read_bytes())
    central = data.index(b"PK\x01\x02")
    data[central + 34 : central + 36] = volume.to_bytes(2, "little")
    path.write_bytes(data)


def _set_member_flags(path: Path, *, flag_bits: int) -> None:
    data = bytearray(path.read_bytes())
    for signature, flag_offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
        header = data.index(signature)
        offset = header + flag_offset
        current = int.from_bytes(data[offset : offset + 2], "little")
        data[offset : offset + 2] = (current | flag_bits).to_bytes(2, "little")
    path.write_bytes(data)


def _unicode_path_extra(*, legacy_name: str, replacement_name: str) -> bytes:
    legacy_bytes = legacy_name.encode("cp437")
    data = struct.pack("<BL", 1, zlib.crc32(legacy_bytes)) + replacement_name.encode("utf-8")
    return struct.pack("<HH", _UNICODE_PATH_ID, len(data)) + data


def _zip64_extra() -> bytes:
    data = struct.pack("<QQQ", 6, 8, 0)
    return struct.pack("<HH", _ZIP64_ID, len(data)) + data


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    ("disk", "central_disk"),
    ((0, 0), (1, 0), (0, 1), (1, 1), (0xFFFF, 0xFFFF)),
)
def test_cpython_ignores_conventional_disk_fields_while_reading_payload(
    tmp_path: Path,
    disk: int,
    central_disk: int,
) -> None:
    bundle = tmp_path / f"accepted-{disk}-{central_disk}.zip"
    _write_bundle(bundle)
    _set_archive_disk_fields(bundle, disk=disk, central_disk=central_disk)

    with zipfile.ZipFile(bundle) as archive:
        [info] = archive.infolist()
        assert archive.comment == b""
        assert info.volume == 0
        assert info.extra == b""
        assert info.flag_bits == 0
        assert archive.read(info) == b"sample"


@pytest.mark.parametrize(
    ("disk", "central_disk"),
    ((1, 0), (0, 1), (1, 1), (2, 7), (0xFFFF, 0xFFFF)),
)
def test_nonzero_archive_disk_field_fails_before_inventory_staging_or_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    disk: int,
    central_disk: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"disk-{disk}-{central_disk}.zip"
    _write_bundle(bundle)
    _set_archive_disk_fields(bundle, disk=disk, central_disk=central_disk)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("archive disk policy must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("archive disk policy must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("archive disk policy must fail before inventory")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_DISK_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


def test_archive_disk_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "disk-cleanup.zip"
    _write_bundle(bundle)
    _set_archive_disk_fields(bundle, disk=1, central_disk=0)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: IO[bytes]) -> zipfile.ZipFile:
        archive = original_zipfile(file)
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_DISK_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


@pytest.mark.parametrize(
    ("flag_bits", "expected_error"),
    (
        (0x0001, "sample bundle contains an encrypted member"),
        (0x0020, "sample bundle uses compressed patched data"),
        (0x0010, "sample bundle uses enhanced deflating"),
        (0x0008, "sample bundle uses a data descriptor"),
    ),
)
def test_established_flag_errors_precede_archive_disk_fields(
    tmp_path: Path,
    flag_bits: int,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"flag-before-disk-{flag_bits}.zip"
    _write_bundle(bundle)
    _set_member_flags(bundle, flag_bits=flag_bits)
    _set_archive_disk_fields(bundle, disk=1, central_disk=0)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize("established", ("unicode", "zip64"))
def test_established_extra_field_errors_precede_archive_disk_fields(
    tmp_path: Path,
    established: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"{established}-before-disk.zip"
    legacy_name = f"{_PREFIX}/legacy.txt"
    extra = (
        _unicode_path_extra(
            legacy_name=legacy_name,
            replacement_name=f"{_PREFIX}/README.md",
        )
        if established == "unicode"
        else _zip64_extra()
    )
    _write_bundle(bundle, extra=extra)
    _set_archive_disk_fields(bundle, disk=1, central_disk=0)

    expected = (
        "sample bundle uses a Unicode Path extra field"
        if established == "unicode"
        else "sample bundle uses a ZIP64 extra field"
    )
    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize(
    ("kind", "expected_error"),
    (
        ("archive", "sample bundle uses an archive comment"),
        ("member", "sample bundle uses a member comment"),
    ),
)
def test_established_comment_errors_precede_archive_disk_fields(
    tmp_path: Path,
    kind: str,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"{kind}-comment-before-disk.zip"
    _write_bundle(bundle, member_comment=b"metadata" if kind == "member" else b"")
    if kind == "archive":
        with zipfile.ZipFile(bundle, "a") as archive:
            archive.comment = b"metadata"
    _set_archive_disk_fields(bundle, disk=1, central_disk=0)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_member_volume_error_precedes_archive_disk_fields(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "member-volume-before-archive-disk.zip"
    _write_bundle(bundle)
    _set_member_volume(bundle, volume=1)
    _set_archive_disk_fields(bundle, disk=1, central_disk=0)

    with pytest.raises(RuntimeError, match=r"^sample bundle uses a split-volume member$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_archive_disk_fields_precede_nul_name_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "archive-disk-before-nul.zip"
    _write_bundle(bundle, hidden_suffix="\x00hidden")
    _set_archive_disk_fields(bundle, disk=1, central_disk=0)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_DISK_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_archive_disk_validator_accepts_zero_fields_and_restores_position() -> None:
    module = _smoke()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("payload.txt", b"payload")
    stream.seek(3)

    module._validate_sample_archive_disk_fields(snapshot=stream)

    assert stream.tell() == 3


@pytest.mark.parametrize(
    ("disk", "central_disk"),
    ((1, 0), (0, 1), (1, 1), (2, 7), (0xFFFF, 0xFFFF)),
)
def test_archive_disk_validator_rejects_nonzero_and_restores_position(
    tmp_path: Path,
    disk: int,
    central_disk: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"validator-{disk}-{central_disk}.zip"
    _write_bundle(bundle)
    _set_archive_disk_fields(bundle, disk=disk, central_disk=central_disk)
    with bundle.open("rb") as stream:
        stream.seek(3)
        with pytest.raises(RuntimeError, match=rf"^{re.escape(_DISK_ERROR)}$"):
            module._validate_sample_archive_disk_fields(snapshot=stream)
        assert stream.tell() == 3


@pytest.mark.parametrize("mutation", ("signature", "comment-length", "trailing"))
def test_structurally_unusable_final_record_keeps_stable_zip_error(
    tmp_path: Path,
    mutation: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"structural-{mutation}.zip"
    _write_bundle(bundle)
    data = bytearray(bundle.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    if mutation == "signature":
        data[end : end + 4] = b"NOPE"
    elif mutation == "comment-length":
        data[end + 20 : end + 22] = (1).to_bytes(2, "little")
    else:
        data.extend(b"trailing")
    bundle.write_bytes(data)

    with pytest.raises(RuntimeError, match=r"^sample bundle ZIP data is invalid$"):
        module._extract_bundle(
            bundle,
            _empty_output(tmp_path),
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )


def test_current_producer_emits_base_archive_disk_fields(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    data = bundle.read_bytes()
    end = data.rindex(_EOCD_SIGNATURE)
    assert end == len(data) - 22
    assert data[end + 4 : end + 8] == b"\x00\x00\x00\x00"


def test_m83_source_checks_final_eocd_after_member_volume_before_names() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]

    processing = extraction.index("_validate_sample_member_flags(flag_bits=info.flag_bits)")
    descriptor = extraction.index("_validate_sample_descriptor_flags(flag_bits=info.flag_bits)")
    unicode = extraction.index("_validate_sample_extra_fields(extra=info.extra)")
    zip64 = extraction.index("_validate_sample_zip64_extra_fields(extra=info.extra)")
    archive_comment = extraction.index("_validate_sample_archive_comment(comment=archive.comment)")
    member_comment = extraction.index("_validate_sample_member_comment(comment=info.comment)")
    member_volume = extraction.index("_validate_sample_member_volume(volume=info.volume)")
    archive_disk = extraction.index(
        "_validate_sample_archive_disk_fields(snapshot=snapshot_stream)"
    )
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert (
        processing
        < descriptor
        < unicode
        < zip64
        < archive_comment
        < member_comment
        < member_volume
        < archive_disk
        < name
        < metadata
    )
    helper = source[source.index("def _validate_sample_archive_disk_fields") :]
    assert "snapshot.seek(-_SAMPLE_EOCD_BYTES, os.SEEK_END)" in helper
    assert "zipfile._" not in helper


def test_m83_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m83" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m83_docs_define_archive_disk_preflight_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0066-reject-unsupported-archive-disk-fields.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M83" in combined
    assert "end-of-central-directory" in combined
    assert _DISK_ERROR in combined
    assert "no ZIP64 end-record parser" in combined
    assert "no multi-volume assembler" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
