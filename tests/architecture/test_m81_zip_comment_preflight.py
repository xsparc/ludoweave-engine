"""Protect M81 ZIP archive/member-comment rejection."""

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
_UNICODE_PATH_ID = 0x7075
_ZIP64_ID = 0x0001
_ARCHIVE_ERROR = "sample bundle uses an archive comment"
_MEMBER_ERROR = "sample bundle uses a member comment"
_UNICODE_PATH_ERROR = "sample bundle uses a Unicode Path extra field"
_ZIP64_ERROR = "sample bundle uses a ZIP64 extra field"


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

    def _validate_sample_archive_comment(self, *, comment: bytes) -> None: ...

    def _validate_sample_inventory(self, observed_members: set[str]) -> None: ...

    def _validate_sample_member_comment(self, *, comment: bytes) -> None: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m81_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m81_release_artifacts"))


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


def _write_commented_bundle(path: Path, *, kind: str) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        _write_member(
            archive,
            name=f"{_PREFIX}/README.md",
            payload=b"sample",
            comment=b"member metadata" if kind == "member" else b"",
        )
        if kind == "archive":
            archive.comment = b"archive metadata"


def _unicode_path_extra(*, legacy_name: str, replacement_name: str) -> bytes:
    legacy_bytes = legacy_name.encode("cp437")
    data = struct.pack("<BL", 1, zlib.crc32(legacy_bytes)) + replacement_name.encode("utf-8")
    return struct.pack("<HH", _UNICODE_PATH_ID, len(data)) + data


def _inject_zip64_extra(data: bytes, *, member_index: int = 0) -> bytes:
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


def _set_member_flags(path: Path, *, flag_bits: int) -> None:
    data = bytearray(path.read_bytes())
    for signature, flag_offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
        header = data.index(signature)
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


def test_cpython_preserves_comments_while_reading_member_payload() -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        _write_member(
            archive,
            name="sample.txt",
            payload=b"payload",
            comment=b"member-comment",
        )
        archive.comment = b"archive-comment"

    stream.seek(0)
    with zipfile.ZipFile(stream) as archive:
        [info] = archive.infolist()
        assert archive.comment == b"archive-comment"
        assert info.comment == b"member-comment"
        assert info.extra == b""
        assert archive.read(info) == b"payload"


@pytest.mark.parametrize(
    ("kind", "expected_error"),
    (("archive", _ARCHIVE_ERROR), ("member", _MEMBER_ERROR)),
)
def test_comment_fails_before_inventory_staging_or_member_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    kind: str,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"{kind}-comment.zip"
    _write_commented_bundle(bundle, kind=kind)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("comments must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("comments must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("comments must fail before inventory")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


@pytest.mark.parametrize(
    ("kind", "expected_error"),
    (("archive", _ARCHIVE_ERROR), ("member", _MEMBER_ERROR)),
)
def test_comment_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    kind: str,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"{kind}-comment.zip"
    _write_commented_bundle(bundle, kind=kind)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: IO[bytes]) -> zipfile.ZipFile:
        archive = original_zipfile(file)
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
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
@pytest.mark.parametrize("kind", ("archive", "member"))
def test_established_flag_errors_precede_comments(
    tmp_path: Path,
    flag_bits: int,
    expected_error: str,
    kind: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"{kind}-precedence-{flag_bits}.zip"
    _write_commented_bundle(bundle, kind=kind)
    _set_member_flags(bundle, flag_bits=flag_bits)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize("kind", ("archive", "member"))
@pytest.mark.parametrize("established", ("unicode", "zip64"))
def test_established_extra_field_errors_precede_comments(
    tmp_path: Path,
    kind: str,
    established: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"{established}-before-{kind}.zip"
    legacy_name = f"{_PREFIX}/legacy.txt"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(
            archive,
            name=legacy_name,
            payload=b"combined",
            comment=b"member-comment" if kind == "member" else b"",
            extra=(
                _unicode_path_extra(
                    legacy_name=legacy_name,
                    replacement_name=f"{_PREFIX}/README.md",
                )
                if established == "unicode"
                else b""
            ),
        )
        if kind == "archive":
            archive.comment = b"archive-comment"
    if established == "zip64":
        bundle.write_bytes(_inject_zip64_extra(bundle.read_bytes()))

    expected = _UNICODE_PATH_ERROR if established == "unicode" else _ZIP64_ERROR
    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_archive_comment_precedes_member_comment(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "both-comments.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(
            archive,
            name=f"{_PREFIX}/README.md",
            payload=b"sample",
            comment=b"member-comment",
        )
        archive.comment = b"archive-comment"

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ARCHIVE_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize(
    ("kind", "expected_error"),
    (("archive", _ARCHIVE_ERROR), ("member", _MEMBER_ERROR)),
)
def test_comments_precede_nul_name_policy(
    tmp_path: Path,
    kind: str,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"{kind}-before-nul.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(
            archive,
            name=f"{_PREFIX}/README.md",
            hidden_suffix="\x00hidden",
            payload=b"sample",
            comment=b"member-comment" if kind == "member" else b"",
        )
        if kind == "archive":
            archive.comment = b"archive-comment"

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize(
    ("validator_name", "expected_error"),
    (
        ("_validate_sample_archive_comment", _ARCHIVE_ERROR),
        ("_validate_sample_member_comment", _MEMBER_ERROR),
    ),
)
def test_comment_validators_accept_only_empty_bytes(
    validator_name: str,
    expected_error: str,
) -> None:
    validator = getattr(_smoke(), validator_name)

    validator(comment=b"")
    for comment in (b"comment", b"\x00", b"PK\x05\x06"):
        with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
            validator(comment=comment)


def test_current_producer_emits_no_archive_or_member_comments(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        assert len(archive.infolist()) == 50
        assert archive.comment == b""
        assert all(info.comment == b"" for info in archive.infolist())


def test_m81_source_uses_separate_archive_and_member_comment_passes() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]

    processing = extraction.index("_validate_sample_member_flags(flag_bits=info.flag_bits)")
    descriptor = extraction.index("_validate_sample_descriptor_flags(flag_bits=info.flag_bits)")
    unicode = extraction.index("_validate_sample_extra_fields(extra=info.extra)")
    zip64 = extraction.index("_validate_sample_zip64_extra_fields(extra=info.extra)")
    archive_comment = extraction.index("_validate_sample_archive_comment(comment=archive.comment)")
    member_pass = extraction.index("for info in infos:", archive_comment)
    member_comment = extraction.index("_validate_sample_member_comment(comment=info.comment)")
    name_pass = extraction.index("for info in infos:", member_pass + 1)
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert (
        processing
        < descriptor
        < unicode
        < zip64
        < archive_comment
        < member_pass
        < member_comment
        < name_pass
        < name
        < metadata
    )


def test_m81_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m81" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m81_docs_define_comment_preflight_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0064-reject-zip-comments.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m81" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 80
    for term in (
        "archive comment",
        "member comment",
        "parser-exposed",
        "before member reads",
        "before staging",
        "content-silent",
        "no raw zip parser",
        "no general comment scanner",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
