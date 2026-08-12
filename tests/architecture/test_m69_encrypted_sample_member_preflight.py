"""Protect M69 encrypted sample-member preflight rejection."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import tempfile
import zipfile
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


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]
    _SAMPLE_ENCRYPTION_FLAGS: int

    def _extract_bundle(self, bundle: Path, output: Path, *, version: str) -> Path: ...

    def _validate_sample_member_flags(self, *, flag_bits: int) -> None: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m69_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m69_release_artifacts"))


def _bundle(path: Path, names: frozenset[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(names):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())


def _set_first_member_flags(path: Path, flag_bits: int) -> None:
    data = bytearray(path.read_bytes())
    for signature, flag_offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
        header = data.index(signature)
        offset = header + flag_offset
        current = int.from_bytes(data[offset : offset + 2], "little")
        data[offset : offset + 2] = (current | flag_bits).to_bytes(2, "little")
    path.write_bytes(data)


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def test_m69_defines_all_zip_encryption_indicator_bits() -> None:
    module = _smoke()

    assert module._SAMPLE_ENCRYPTION_FLAGS == 0x2041
    module._validate_sample_member_flags(flag_bits=0)
    module._validate_sample_member_flags(flag_bits=0x0800)
    for flag_bits in (0x0001, 0x0040, 0x2000, 0x2041):
        with pytest.raises(
            RuntimeError,
            match=r"^sample bundle contains an encrypted member$",
        ):
            module._validate_sample_member_flags(flag_bits=flag_bits)


@pytest.mark.parametrize("flag_bits", (0x0001, 0x0040, 0x2000))
def test_encryption_indicator_fails_content_silently_before_read_or_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    flag_bits: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / "encrypted.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    _set_first_member_flags(bundle, flag_bits)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("encrypted members must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("encrypted members must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("encrypted members must fail before inventory validation")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle contains an encrypted member$",
    ) as caught:
        module._extract_bundle(bundle, output, version=_VERSION)

    assert all(name not in str(caught.value) for name in module._EXPECTED_SAMPLE_MEMBERS)
    assert list(output.iterdir()) == []


def test_current_producer_uses_no_encryption_indicators(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        assert archive.infolist()
        assert all(
            info.flag_bits & module._SAMPLE_ENCRYPTION_FLAGS == 0 for info in archive.infolist()
        )


def test_m69_source_preflights_encryption_before_inventory_staging_or_read() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction_source = source[source.index("def _extract_bundle") :]

    encryption = extraction_source.index("_validate_sample_member_flags(flag_bits=info.flag_bits)")
    inventory = extraction_source.index("_validate_sample_inventory(observed_members)")
    staging = extraction_source.index("TemporaryDirectory(")
    member_read = extraction_source.index("archive.open(info)")

    assert encryption < inventory < staging < member_read


def test_m69_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m69" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m69_docs_define_encryption_preflight_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0052-reject-encrypted-sample-members.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m69" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 68
    for term in (
        "general-purpose bit flags",
        "traditional encryption",
        "strong encryption",
        "masked header values",
        "before member reads",
        "before staging",
        "content-silent",
        "no password",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
