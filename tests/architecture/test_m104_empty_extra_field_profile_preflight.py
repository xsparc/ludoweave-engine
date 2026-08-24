"""Protect M104 empty sample-member extra-field profile preflight."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import binascii
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
_UNINTERPRETED_EXTRA = struct.pack("<HH2s", 0xCAFE, 2, b"ok")
_EOCD_SIGNATURE = b"PK\x05\x06"
_CENTRAL_SIGNATURE = b"PK\x01\x02"
_FIXED_LOCAL_HEADER_BYTES = 30
_FIXED_CENTRAL_HEADER_BYTES = 46
_PROFILE_ERROR = "sample bundle contains an unsupported extra field"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_extra_field_profile(
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
    return cast(_SmokeModule, _load(_SMOKE, "m104_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m104_release_artifacts"))


def _write_small_bundle(path: Path, *, extra: bytes = _UNINTERPRETED_EXTRA) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index in range(2):
            info = zipfile.ZipInfo(f"{_PREFIX}/member-{index}.txt", date_time=_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            info.extra = extra
            archive.writestr(info, f"payload-{index}".encode())


def _unicode_path_extra(*, legacy_name: str, replacement_name: str) -> bytes:
    legacy_crc = binascii.crc32(legacy_name.encode()) & 0xFFFFFFFF
    payload = b"\x01" + legacy_crc.to_bytes(4, "little") + replacement_name.encode()
    return struct.pack("<HH", 0x7075, len(payload)) + payload


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _local_extra(data: bytes | bytearray, info: zipfile.ZipInfo) -> bytes:
    lengths = info.header_offset + 26
    name_length = int.from_bytes(data[lengths : lengths + 2], "little")
    extra_length = int.from_bytes(data[lengths + 2 : lengths + 4], "little")
    start = info.header_offset + _FIXED_LOCAL_HEADER_BYTES + name_length
    return bytes(data[start : start + extra_length])


def _change_local_extra_payload(path: Path, *, member: int) -> None:
    data = bytearray(path.read_bytes())
    with zipfile.ZipFile(BytesIO(data)) as archive:
        info = archive.infolist()[member]
    local = _local_extra(data, info)
    assert local == _UNINTERPRETED_EXTRA
    start = info.header_offset + _FIXED_LOCAL_HEADER_BYTES + len(info.orig_filename.encode())
    data[start + len(local) - 1] ^= 0x01
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


def test_cpython_admits_equal_uninterpreted_extra_fields_and_reads_payloads(tmp_path: Path) -> None:
    bundle = tmp_path / "uninterpreted-extra.zip"
    _write_small_bundle(bundle)
    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert all(info.extra == _UNINTERPRETED_EXTRA for info in infos)
        assert all(_local_extra(data, info) == _UNINTERPRETED_EXTRA for info in infos)
        assert [archive.read(info) for info in infos] == [b"payload-0", b"payload-1"]


def test_extra_profile_error_precedes_inventory_staging_and_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "unsupported-extra.zip"
    _write_small_bundle(bundle)
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("extra-field profile must fail before later processing")

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


def test_extra_profile_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "unsupported-extra-cleanup.zip"
    _write_small_bundle(bundle)
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


@pytest.mark.parametrize(
    ("extra", "expected_error"),
    (
        (
            _unicode_path_extra(
                legacy_name=f"{_PREFIX}/legacy.txt",
                replacement_name=f"{_PREFIX}/replacement.txt",
            ),
            "sample bundle uses a Unicode Path extra field",
        ),
        (struct.pack("<HH", 0x0001, 0), "sample bundle uses a ZIP64 extra field"),
    ),
)
def test_established_extra_field_errors_precede_empty_profile(
    tmp_path: Path,
    extra: bytes,
    expected_error: str,
) -> None:
    bundle = tmp_path / "established-extra.zip"
    _write_small_bundle(bundle, extra=extra)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_local_extra_mismatch_precedes_empty_profile(tmp_path: Path) -> None:
    bundle = tmp_path / "local-extra-mismatch.zip"
    _write_small_bundle(bundle)
    _change_local_extra_payload(bundle, member=1)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header extra fields are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_contiguity_error_precedes_empty_profile(tmp_path: Path) -> None:
    bundle = tmp_path / "gap-and-extra.zip"
    _write_small_bundle(bundle)
    _insert_payload_gap(bundle, member=0)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle member payloads are not contiguous$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_extra_profile_validator_accepts_empty_and_rejects_nonempty(tmp_path: Path) -> None:
    module = _smoke()
    empty_bundle = tmp_path / "empty-extra.zip"
    uninterpreted_bundle = tmp_path / "uninterpreted-extra.zip"
    _write_small_bundle(empty_bundle, extra=b"")
    _write_small_bundle(uninterpreted_bundle)
    with zipfile.ZipFile(empty_bundle) as archive:
        module._validate_sample_extra_field_profile(infos=tuple(archive.infolist()))
    module._validate_sample_extra_field_profile(infos=())
    with (
        zipfile.ZipFile(uninterpreted_bundle) as archive,
        pytest.raises(RuntimeError, match=rf"^{re.escape(_PROFILE_ERROR)}$"),
    ):
        module._validate_sample_extra_field_profile(infos=tuple(archive.infolist()))


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_emits_exactly_empty_extra_fields(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert all(info.extra == b"" for info in infos)


def test_m104_source_checks_empty_profile_after_m103_before_decoded_names() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    contiguity = extraction.index("_validate_sample_payload_contiguity(")
    profile = extraction.index("_validate_sample_extra_field_profile(")
    decoded_name = extraction.index(
        "_validate_sample_member_name(original_name=info.orig_filename)"
    )
    metadata = extraction.index("total_bytes = 0")
    assert contiguity < profile < decoded_name < metadata
    helper = source[source.index("def _validate_sample_extra_field_profile") :]
    assert "info.extra" in helper
    assert "archive.read" not in helper
    assert "zipfile._" not in helper


def test_m104_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m104" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m104_docs_define_empty_extra_field_profile_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0087-require-empty-sample-member-extra-fields.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())
    assert "M104" in combined
    assert "empty sample-member extra-field profile preflight" in combined
    assert _PROFILE_ERROR in combined
    assert "one central-extra emptiness classifier" in combined
    assert "no extra-field semantics parser" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
