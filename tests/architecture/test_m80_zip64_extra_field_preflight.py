"""Protect M80 ZIP64 extra-field rejection."""

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
_ZIP64_ID = 0x0001
_UNICODE_PATH_ID = 0x7075
_ZIP64_ERROR = "sample bundle uses a ZIP64 extra field"
_UNICODE_PATH_ERROR = "sample bundle uses a Unicode Path extra field"


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]
    _SAMPLE_ZIP64_EXTRA_FIELD: int

    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_inventory(self, observed_members: set[str]) -> None: ...

    def _validate_sample_zip64_extra_fields(self, *, extra: bytes) -> None: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m80_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m80_release_artifacts"))


def _write_member(
    archive: zipfile.ZipFile,
    *,
    name: str,
    payload: bytes,
    extra: bytes = b"",
    hidden_suffix: str = "",
) -> None:
    info = zipfile.ZipInfo("placeholder")
    info.filename = f"{name}{hidden_suffix}"
    info.orig_filename = info.filename
    info.extra = extra
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, payload)


def _unicode_path_extra(*, legacy_name: str, replacement_name: str) -> bytes:
    legacy_bytes = legacy_name.encode("cp437")
    data = struct.pack("<BL", 1, zlib.crc32(legacy_bytes)) + replacement_name.encode("utf-8")
    return struct.pack("<HH", _UNICODE_PATH_ID, len(data)) + data


def _inject_zip64_extra(data: bytes, *, member_index: int) -> bytes:
    patched = bytearray(data)
    central = -1
    for _ in range(member_index + 1):
        central = patched.index(b"PK\x01\x02", central + 1)
    compressed_size = int.from_bytes(patched[central + 20 : central + 24], "little")
    file_size = int.from_bytes(patched[central + 24 : central + 28], "little")
    header_offset = int.from_bytes(patched[central + 42 : central + 46], "little")
    name_size = int.from_bytes(patched[central + 28 : central + 30], "little")
    extra_size = int.from_bytes(patched[central + 30 : central + 32], "little")
    zip64 = struct.pack(
        "<HHQQQ",
        _ZIP64_ID,
        24,
        file_size,
        compressed_size,
        header_offset,
    )
    insert_at = central + 46 + name_size + extra_size
    patched[central + 20 : central + 24] = b"\xff" * 4
    patched[central + 24 : central + 28] = b"\xff" * 4
    patched[central + 42 : central + 46] = b"\xff" * 4
    patched[central + 30 : central + 32] = (extra_size + len(zip64)).to_bytes(2, "little")
    patched[insert_at:insert_at] = zip64
    eocd = patched.rindex(b"PK\x05\x06")
    directory_size = int.from_bytes(patched[eocd + 12 : eocd + 16], "little")
    patched[eocd + 12 : eocd + 16] = (directory_size + len(zip64)).to_bytes(4, "little")
    return bytes(patched)


def _inject_zip64_extra_file(path: Path, *, member_index: int) -> None:
    path.write_bytes(_inject_zip64_extra(path.read_bytes(), member_index=member_index))


def _full_bundle_with_zip64(
    path: Path,
    names: frozenset[str],
    *,
    target_index: int = 0,
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for name in sorted(names):
            full_name = f"{_PREFIX}/{name}"
            _write_member(archive, name=full_name, payload=full_name.encode())
    _inject_zip64_extra_file(path, member_index=target_index)


def _set_member_flags(path: Path, *, member_index: int, flag_bits: int) -> None:
    data = bytearray(path.read_bytes())
    for signature, flag_offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
        header = -1
        for _ in range(member_index + 1):
            header = data.index(signature, header + 1)
        offset = header + flag_offset
        current = int.from_bytes(data[offset : offset + 2], "little")
        data[offset : offset + 2] = (current | flag_bits).to_bytes(2, "little")
    path.write_bytes(data)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cpython_applies_and_reads_a_genuine_zip64_extra_field() -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("sample.txt", b"zip64 payload")

    with zipfile.ZipFile(
        io.BytesIO(_inject_zip64_extra(stream.getvalue(), member_index=0))
    ) as archive:
        info = archive.infolist()[0]
        assert info.file_size == len(b"zip64 payload")
        assert info.compress_size < 0xFFFF_FFFF
        assert info.header_offset == 0
        assert info.extra[:2] == _ZIP64_ID.to_bytes(2, "little")
        assert archive.read(info) == b"zip64 payload"


def test_zip64_fails_before_inventory_staging_or_member_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "zip64.zip"
    _full_bundle_with_zip64(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("ZIP64 fields must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("ZIP64 fields must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("ZIP64 fields must fail before inventory")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP64_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


def test_later_zip64_preempts_earlier_member_metadata_error(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "ordered-errors.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(archive, name="/unsafe-first.txt", payload=b"unsafe")
        _write_member(archive, name=f"{_PREFIX}/README.md", payload=b"zip64")
    _inject_zip64_extra_file(bundle, member_index=1)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP64_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_zip64_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "zip64.zip"
    _full_bundle_with_zip64(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: IO[bytes]) -> zipfile.ZipFile:
        archive = original_zipfile(file)
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP64_ERROR)}$"):
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
def test_established_flag_errors_precede_zip64_on_same_member(
    tmp_path: Path,
    flag_bits: int,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"same-member-precedence-{flag_bits}.zip"
    _full_bundle_with_zip64(bundle, frozenset(("README.md",)))
    _set_member_flags(bundle, member_index=0, flag_bits=flag_bits)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize(
    ("flag_bits", "expected_error"),
    (
        (0x0001, "sample bundle contains an encrypted member"),
        (0x0020, "sample bundle uses compressed patched data"),
        (0x0010, "sample bundle uses enhanced deflating"),
        (0x0008, "sample bundle uses a data descriptor"),
    ),
)
def test_later_established_flag_error_precedes_earlier_zip64(
    tmp_path: Path,
    flag_bits: int,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"archive-precedence-{flag_bits}.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(archive, name=f"{_PREFIX}/README.md", payload=b"zip64")
        _write_member(archive, name=f"{_PREFIX}/pyproject.toml", payload=b"flagged")
    _inject_zip64_extra_file(bundle, member_index=0)
    _set_member_flags(bundle, member_index=1, flag_bits=flag_bits)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_unicode_path_precedes_zip64_on_same_member(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "unicode-and-zip64.zip"
    legacy_name = f"{_PREFIX}/legacy.txt"
    replacement_name = f"{_PREFIX}/README.md"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(
            archive,
            name=legacy_name,
            payload=b"combined",
            extra=_unicode_path_extra(
                legacy_name=legacy_name,
                replacement_name=replacement_name,
            ),
        )
    _inject_zip64_extra_file(bundle, member_index=0)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_UNICODE_PATH_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_later_unicode_path_precedes_earlier_zip64(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "unicode-after-zip64.zip"
    legacy_name = f"{_PREFIX}/legacy.txt"
    replacement_name = f"{_PREFIX}/pyproject.toml"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(archive, name=f"{_PREFIX}/README.md", payload=b"zip64")
        _write_member(
            archive,
            name=legacy_name,
            payload=b"unicode",
            extra=_unicode_path_extra(
                legacy_name=legacy_name,
                replacement_name=replacement_name,
            ),
        )
    _inject_zip64_extra_file(bundle, member_index=0)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_UNICODE_PATH_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_zip64_policy_precedes_nul_name_policy_across_members(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "zip64-before-nul.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(
            archive,
            name=f"{_PREFIX}/README.md",
            payload=b"hidden",
            hidden_suffix="\x00hidden",
        )
        _write_member(archive, name=f"{_PREFIX}/pyproject.toml", payload=b"zip64")
    _inject_zip64_extra_file(bundle, member_index=1)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP64_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_exact_zip64_validator_ignores_unrelated_and_trailing_fields() -> None:
    module = _smoke()
    unrelated = struct.pack("<HH", 0xCAFE, 4) + b"zip\x01"
    zip64 = struct.pack("<HH", _ZIP64_ID, 0)

    assert module._SAMPLE_ZIP64_EXTRA_FIELD == _ZIP64_ID
    for extra in (b"", b"\x01\x00\x00", unrelated):
        module._validate_sample_zip64_extra_fields(extra=extra)
    for extra in (zip64, unrelated + zip64):
        with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP64_ERROR)}$"):
            module._validate_sample_zip64_extra_fields(extra=extra)


def test_current_producer_emits_no_extra_fields(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        assert len(archive.infolist()) == 50
        assert all(not info.extra for info in archive.infolist())


def test_m80_source_uses_a_separate_exact_zip64_pass() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    validation = source[
        source.index("def _validate_sample_zip64_extra_fields") : source.index(
            "def _validate_sample_extra_fields"
        )
    ]

    assert "field_id == _SAMPLE_ZIP64_EXTRA_FIELD" in validation
    assert 'extra != b""' not in validation
    established_pass = extraction.index("for info in infos:")
    processing = extraction.index("_validate_sample_member_flags(flag_bits=info.flag_bits)")
    descriptor_pass = extraction.index("for info in infos:", established_pass + 1)
    descriptor = extraction.index("_validate_sample_descriptor_flags(flag_bits=info.flag_bits)")
    unicode_pass = extraction.index("for info in infos:", descriptor_pass + 1)
    unicode = extraction.index("_validate_sample_extra_fields(extra=info.extra)")
    zip64_pass = extraction.index("for info in infos:", unicode_pass + 1)
    zip64 = extraction.index("_validate_sample_zip64_extra_fields(extra=info.extra)")
    name_pass = extraction.index("for info in infos:", zip64_pass + 1)
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert (
        established_pass
        < processing
        < descriptor_pass
        < descriptor
        < unicode_pass
        < unicode
        < zip64_pass
        < zip64
        < name_pass
        < name
        < metadata
    )


def test_m80_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m80" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m80_docs_define_zip64_preflight_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0063-reject-zip64-extra-fields.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m80" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 79
    for term in (
        "zip64",
        "0x0001",
        "before member reads",
        "before staging",
        "content-silent",
        "exact extra-field id",
        "bounded extra-field walk",
        "no broad extra-field ban",
        "no raw zip64 parser",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
