"""Protect M76 enhanced-deflate sample-member preflight rejection."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import tempfile
import zipfile
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
_ENHANCED_ERROR = "sample bundle uses enhanced deflating"


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]
    _SAMPLE_ENHANCED_DEFLATE_FLAG: int

    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_compression_flags(
        self,
        *,
        flag_bits: int,
        compress_type: int,
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
    return cast(_SmokeModule, _load(_SMOKE, "m76_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m76_release_artifacts"))


def _bundle(path: Path, names: frozenset[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(names):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())


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


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m76_defines_method_scoped_enhanced_deflate_flag_and_error() -> None:
    module = _smoke()

    assert module._SAMPLE_ENHANCED_DEFLATE_FLAG == 0x0010
    module._validate_sample_compression_flags(
        flag_bits=0,
        compress_type=zipfile.ZIP_DEFLATED,
    )
    module._validate_sample_compression_flags(
        flag_bits=0x0010,
        compress_type=zipfile.ZIP_STORED,
    )
    module._validate_sample_compression_flags(
        flag_bits=0x0800,
        compress_type=zipfile.ZIP_DEFLATED,
    )
    for flag_bits in (0x0010, 0x0810):
        with pytest.raises(RuntimeError, match=rf"^{re.escape(_ENHANCED_ERROR)}$"):
            module._validate_sample_compression_flags(
                flag_bits=flag_bits,
                compress_type=zipfile.ZIP_DEFLATED,
            )


def test_cpython_reads_normal_deflate_with_enhanced_indicator(tmp_path: Path) -> None:
    bundle = tmp_path / "enhanced-deflate.zip"
    _bundle(bundle, frozenset(("README.md",)))
    _set_member_flags(bundle, member_index=0, flag_bits=0x0010)

    with zipfile.ZipFile(bundle) as archive:
        info = archive.infolist()[0]
        assert info.compress_type == zipfile.ZIP_DEFLATED
        assert info.flag_bits & 0x0010
        with archive.open(info) as source:
            assert source.read() == b"README.md"


def test_enhanced_deflate_fails_before_inventory_staging_or_member_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "enhanced-deflate.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    _set_member_flags(bundle, member_index=0, flag_bits=0x0010)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("enhanced deflating must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("enhanced deflating must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("enhanced deflating must fail before inventory validation")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ENHANCED_ERROR)}$") as caught:
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert _PREFIX not in str(caught.value)
    assert list(output.iterdir()) == []


def test_later_enhanced_deflate_preempts_earlier_member_metadata_error(
    tmp_path: Path,
) -> None:
    module = _smoke()
    bundle = tmp_path / "ordered-errors.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("/unsafe-first.txt", b"unsafe")
        archive.writestr(f"{_PREFIX}/enhanced-second.txt", b"enhanced")
    _set_member_flags(bundle, member_index=1, flag_bits=0x0010)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ENHANCED_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_enhanced_deflate_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "enhanced-deflate.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    _set_member_flags(bundle, member_index=0, flag_bits=0x0010)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: IO[bytes]) -> zipfile.ZipFile:
        archive = original_zipfile(file)
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ENHANCED_ERROR)}$"):
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


def test_encryption_precedes_enhanced_deflate_and_stored_bit_is_out_of_scope(
    tmp_path: Path,
) -> None:
    module = _smoke()
    encrypted = tmp_path / "encrypted-enhanced.zip"
    _bundle(encrypted, module._EXPECTED_SAMPLE_MEMBERS)
    _set_member_flags(encrypted, member_index=0, flag_bits=0x0011)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle contains an encrypted member$",
    ):
        module._extract_bundle(encrypted, _empty_output(tmp_path), version=_VERSION)

    stored = tmp_path / "stored-bit-four.zip"
    with zipfile.ZipFile(stored, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(module._EXPECTED_SAMPLE_MEMBERS):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())
    _set_member_flags(stored, member_index=0, flag_bits=0x0010)
    stored_output = tmp_path / "stored-output"
    stored_output.mkdir()
    extracted = module._extract_bundle(
        stored,
        stored_output,
        version=_VERSION,
        expected_sha256=_sha256(stored),
    )
    assert extracted.is_dir()


def test_current_producer_uses_no_enhanced_deflate_indicator(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        assert archive.infolist()
        assert all(
            info.flag_bits & module._SAMPLE_ENHANCED_DEFLATE_FLAG == 0
            for info in archive.infolist()
        )


def test_m76_source_preflights_exact_method_scoped_flag_without_allowlist() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    validation = source[
        source.index("def _validate_sample_compression_flags") : source.index(
            "def _portable_sample_member_parts"
        )
    ]

    assert "_SAMPLE_ENHANCED_DEFLATE_FLAG = 0x0010" in source
    assert "compress_type == zipfile.ZIP_DEFLATED" in validation
    assert "flag_bits & _SAMPLE_ENHANCED_DEFLATE_FLAG" in validation
    assert "flag_bits & ~" not in validation
    processing = extraction.index("_validate_sample_member_flags(flag_bits=info.flag_bits)")
    compression = extraction.index("_validate_sample_compression_flags(")
    metadata = extraction.index("total_bytes = 0")
    inventory = extraction.index("_validate_sample_inventory(observed_members)")
    staging = extraction.index("TemporaryDirectory(")
    member_read = extraction.index("archive.open(info)")
    assert processing < compression < metadata < inventory < staging < member_read


def test_m76_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m76" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m76_docs_define_enhanced_deflate_preflight_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0059-reject-enhanced-deflate-sample-members.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m76" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 75
    for term in (
        "enhanced deflating",
        "general-purpose bit 4",
        "compression method 8",
        "before member reads",
        "before staging",
        "content-silent",
        "no broad flag allowlist",
        "stored members",
        "central-directory",
        "local-header inconsistencies",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
