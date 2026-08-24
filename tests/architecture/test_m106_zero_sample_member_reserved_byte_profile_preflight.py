"""Protect M106 zero extraction-version reserved-byte profile preflight."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import struct
import sys
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
from typing import NoReturn, Protocol, cast

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
_FIXED_CENTRAL_HEADER_BYTES = 46
_UNINTERPRETED_EXTRA = struct.pack("<HH2s", 0xCAFE, 2, b"ok")
_UNUSED_FLAG = 1 << 7
_PROFILE_ERROR = "sample bundle has a nonzero extraction-version reserved byte"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_extraction_version_reserved_byte_profile(
        self,
        *,
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
    return cast(_SmokeModule, _load(_SMOKE, "m106_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m106_release_artifacts"))


def _write_small_bundle(path: Path, *, extra: bytes = b"") -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index in range(2):
            info = zipfile.ZipInfo(f"{_PREFIX}/member-{index}.txt", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            info.extra = extra
            archive.writestr(info, f"payload-{index}".encode())


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _set_member_reserved_byte(
    path: Path,
    *,
    member: int,
    reserved: int,
    change_local: bool = True,
    change_central: bool = True,
) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    directory_offset = int.from_bytes(data[end + 16 : end + 20], "little")
    with zipfile.ZipFile(BytesIO(data)) as archive:
        infos = tuple(archive.infolist())
    if change_local:
        data[infos[member].header_offset + 5] = reserved

    cursor = directory_offset
    for index in range(len(infos)):
        assert data[cursor : cursor + 4] == _CENTRAL_SIGNATURE
        if index == member and change_central:
            data[cursor + 7] = reserved
            break
        name_size = int.from_bytes(data[cursor + 28 : cursor + 30], "little")
        extra_size = int.from_bytes(data[cursor + 30 : cursor + 32], "little")
        comment_size = int.from_bytes(data[cursor + 32 : cursor + 34], "little")
        cursor += _FIXED_CENTRAL_HEADER_BYTES + name_size + extra_size + comment_size
    path.write_bytes(data)


def _set_member_flags(path: Path, *, member: int, flags: int) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    directory_offset = int.from_bytes(data[end + 16 : end + 20], "little")
    with zipfile.ZipFile(BytesIO(data)) as archive:
        infos = tuple(archive.infolist())
    local = infos[member].header_offset + 6
    data[local : local + 2] = flags.to_bytes(2, "little")

    cursor = directory_offset
    for index in range(len(infos)):
        assert data[cursor : cursor + 4] == _CENTRAL_SIGNATURE
        if index == member:
            data[cursor + 8 : cursor + 10] = flags.to_bytes(2, "little")
            break
        name_size = int.from_bytes(data[cursor + 28 : cursor + 30], "little")
        extra_size = int.from_bytes(data[cursor + 30 : cursor + 32], "little")
        comment_size = int.from_bytes(data[cursor + 32 : cursor + 34], "little")
        cursor += _FIXED_CENTRAL_HEADER_BYTES + name_size + extra_size + comment_size
    path.write_bytes(data)


def _insert_payload_gap(path: Path, *, member: int) -> None:
    data = path.read_bytes()
    end = data.rindex(_EOCD_SIGNATURE)
    directory_offset = int.from_bytes(data[end + 16 : end + 20], "little")
    with zipfile.ZipFile(BytesIO(data)) as archive:
        infos = tuple(archive.infolist())
    insertion = infos[member + 1].header_offset

    changed = bytearray(data[:insertion] + b"\x00" + data[insertion:])
    changed_end = end + 1
    changed_directory = directory_offset + 1
    changed[changed_end + 16 : changed_end + 20] = changed_directory.to_bytes(4, "little")
    cursor = changed_directory
    while bytes(changed[cursor : cursor + 4]) == _CENTRAL_SIGNATURE:
        local_offset = int.from_bytes(changed[cursor + 42 : cursor + 46], "little")
        if local_offset >= insertion:
            changed[cursor + 42 : cursor + 46] = (local_offset + 1).to_bytes(4, "little")
        name_size = int.from_bytes(changed[cursor + 28 : cursor + 30], "little")
        extra_size = int.from_bytes(changed[cursor + 30 : cursor + 32], "little")
        comment_size = int.from_bytes(changed[cursor + 32 : cursor + 34], "little")
        cursor += _FIXED_CENTRAL_HEADER_BYTES + name_size + extra_size + comment_size
    path.write_bytes(changed)


def test_cpython_admits_matching_nonzero_reserved_byte_and_reads_payloads(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "nonzero-reserved-cpython.zip"
    _write_small_bundle(bundle)
    _set_member_reserved_byte(bundle, member=0, reserved=1)
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert [(info.extract_version, info.reserved) for info in infos] == [
            (20, 1),
            (20, 0),
        ]
        assert [archive.read(info) for info in infos] == [b"payload-0", b"payload-1"]


def test_reserved_byte_profile_error_precedes_inventory_staging_and_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "nonzero-reserved.zip"
    _write_small_bundle(bundle)
    _set_member_reserved_byte(bundle, member=0, reserved=1)
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("reserved-byte profile must fail before later processing")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PROFILE_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )
    assert list(output.iterdir()) == []


def test_reserved_byte_profile_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "nonzero-reserved-cleanup.zip"
    _write_small_bundle(bundle)
    _set_member_reserved_byte(bundle, member=0, reserved=1)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PROFILE_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)
    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_local_reserved_byte_mismatch_precedes_zero_profile(tmp_path: Path) -> None:
    bundle = tmp_path / "local-reserved-mismatch.zip"
    _write_small_bundle(bundle)
    _set_member_reserved_byte(
        bundle,
        member=0,
        reserved=1,
        change_central=False,
    )
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header extraction versions are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_contiguity_error_precedes_zero_reserved_byte_profile(tmp_path: Path) -> None:
    bundle = tmp_path / "gap-and-reserved.zip"
    _write_small_bundle(bundle)
    _set_member_reserved_byte(bundle, member=0, reserved=1)
    _insert_payload_gap(bundle, member=0)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle member payloads are not contiguous$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_extra_profile_error_precedes_zero_reserved_byte_profile(tmp_path: Path) -> None:
    bundle = tmp_path / "extra-and-reserved.zip"
    _write_small_bundle(bundle, extra=_UNINTERPRETED_EXTRA)
    _set_member_reserved_byte(bundle, member=0, reserved=1)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle contains an unsupported extra field$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_zero_flag_profile_error_precedes_zero_reserved_byte_profile(tmp_path: Path) -> None:
    bundle = tmp_path / "flags-and-reserved.zip"
    _write_small_bundle(bundle)
    _set_member_flags(bundle, member=0, flags=_UNUSED_FLAG)
    _set_member_reserved_byte(bundle, member=0, reserved=1)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle contains unsupported general-purpose flags$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize(
    ("name", "compression", "expected_error"),
    (
        ("member.txt", zipfile.ZIP_LZMA, "sample bundle uses an unsupported compression method"),
        (
            "na\N{LATIN SMALL LETTER I WITH DIAERESIS}ve.txt",
            zipfile.ZIP_DEFLATED,
            "sample bundle contains a non-portable member path",
        ),
    ),
)
def test_established_member_metadata_errors_precede_zero_reserved_byte_profile(
    tmp_path: Path,
    name: str,
    compression: int,
    expected_error: str,
) -> None:
    bundle = tmp_path / "metadata-reserved.zip"
    with zipfile.ZipFile(bundle, "w", compression=compression) as archive:
        archive.writestr(f"{_PREFIX}/{name}", b"payload")
    _set_member_reserved_byte(bundle, member=0, reserved=1)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_reserved_byte_profile_validator_accepts_zero_and_rejects_nonzero(
    tmp_path: Path,
) -> None:
    module = _smoke()
    zero_bundle = tmp_path / "zero-reserved.zip"
    nonzero_bundle = tmp_path / "nonzero-reserved.zip"
    _write_small_bundle(zero_bundle)
    _write_small_bundle(nonzero_bundle)
    _set_member_reserved_byte(nonzero_bundle, member=0, reserved=1)
    with zipfile.ZipFile(zero_bundle) as archive:
        module._validate_sample_extraction_version_reserved_byte_profile(
            infos=tuple(archive.infolist())
        )
    module._validate_sample_extraction_version_reserved_byte_profile(infos=())
    with (
        zipfile.ZipFile(nonzero_bundle) as archive,
        pytest.raises(RuntimeError, match=rf"^{re.escape(_PROFILE_ERROR)}$"),
    ):
        module._validate_sample_extraction_version_reserved_byte_profile(
            infos=tuple(archive.infolist())
        )


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_emits_exactly_zero_reserved_bytes(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert all(info.reserved == 0 for info in infos)


def test_m106_source_checks_reserved_profile_after_flags_before_inventory() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    extra_profile = extraction.index("_validate_sample_extra_field_profile(")
    decoded_name = extraction.index(
        "_validate_sample_member_name(original_name=info.orig_filename)"
    )
    metadata = extraction.index("total_bytes = 0")
    flag_profile = extraction.index("_validate_sample_general_purpose_flag_profile(")
    reserved_profile = extraction.index(
        "_validate_sample_extraction_version_reserved_byte_profile("
    )
    inventory = extraction.index("_validate_sample_inventory(observed_members)")
    assert extra_profile < decoded_name < metadata < flag_profile < reserved_profile < inventory
    helper = source[source.index("def _validate_sample_extraction_version_reserved_byte_profile") :]
    assert "info.reserved" in helper
    assert "archive.read" not in helper
    assert "zipfile._" not in helper


def test_m106_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m106" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m106_docs_define_zero_reserved_byte_profile_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0089-require-zero-sample-member-extraction-version-reserved-bytes.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M106" in combined
    assert "zero sample-member extraction-version reserved-byte profile preflight" in combined
    assert _PROFILE_ERROR in combined
    assert "one central-reserved zero-profile classifier" in combined
    assert "no extraction-version semantics parser" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
