"""Protect M109 zero sample-member internal-attribute profile preflight."""

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
_DATE_TIME = (2026, 8, 25, 0, 0, 0)
_UNINTERPRETED_EXTRA = bytes((0xFE, 0xCA, 2, 0, 111, 107))
_PROFILE_ERROR = "sample bundle has unsupported internal attributes"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_internal_attribute_profile(
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
    return cast(_SmokeModule, _load(_SMOKE, "m109_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m109_release_artifacts"))


def _write_small_bundle(
    path: Path,
    *,
    internal_attr: int,
    create_version: int = 20,
    extract_version: int = 20,
    reserved: int = 0,
    extra: bytes = b"",
    name: str = "member.txt",
    compression: int = zipfile.ZIP_DEFLATED,
) -> None:
    with zipfile.ZipFile(path, "w", compression=compression) as archive:
        info = zipfile.ZipInfo(f"{_PREFIX}/{name}", date_time=_DATE_TIME)
        info.compress_type = compression
        info.create_system = 3
        info.create_version = create_version
        info.extract_version = extract_version
        info.reserved = reserved
        info.internal_attr = internal_attr
        info.external_attr = 0o100644 << 16
        info.extra = extra
        archive.writestr(info, b"payload")


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cpython_admits_text_marker_and_reads_payload(tmp_path: Path) -> None:
    bundle = tmp_path / "text-marker.zip"
    _write_small_bundle(bundle, internal_attr=1)
    with zipfile.ZipFile(bundle) as archive:
        info = archive.infolist()[0]
        assert info.internal_attr == 1
        assert archive.read(info) == b"payload"


def test_internal_attribute_profile_precedes_inventory_staging_and_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "unsupported-internal-attribute.zip"
    _write_small_bundle(bundle, internal_attr=1)
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("internal-attribute profile must fail before later processing")

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


def test_internal_attribute_profile_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "unsupported-internal-attribute-cleanup.zip"
    _write_small_bundle(bundle, internal_attr=1)
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
    ("kwargs", "expected_error"),
    (
        (
            {"extra": _UNINTERPRETED_EXTRA},
            "sample bundle contains an unsupported extra field",
        ),
        (
            {"reserved": 1},
            "sample bundle has a nonzero extraction-version reserved byte",
        ),
        (
            {"extract_version": 21},
            "sample bundle has an unsupported extraction version",
        ),
        (
            {"create_version": 21},
            "sample bundle has an unsupported creation version",
        ),
    ),
)
def test_established_profiles_precede_internal_attribute_profile(
    tmp_path: Path,
    kwargs: dict[str, int | bytes],
    expected_error: str,
) -> None:
    bundle = tmp_path / "ordered-profile-errors.zip"
    _write_small_bundle(bundle, internal_attr=1, **kwargs)  # type: ignore[arg-type]
    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
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
def test_member_metadata_errors_precede_internal_attribute_profile(
    tmp_path: Path,
    name: str,
    compression: int,
    expected_error: str,
) -> None:
    bundle = tmp_path / "metadata-internal-attribute.zip"
    _write_small_bundle(
        bundle,
        internal_attr=1,
        name=name,
        compression=compression,
    )
    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


@pytest.mark.parametrize("internal_attr", (1, 2, 3, 0x8000, 0xFFFF))
def test_internal_attribute_profile_rejects_every_nonproducer_value(
    tmp_path: Path,
    internal_attr: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"internal-attribute-{internal_attr}.zip"
    _write_small_bundle(bundle, internal_attr=internal_attr)
    with (
        zipfile.ZipFile(bundle) as archive,
        pytest.raises(RuntimeError, match=rf"^{re.escape(_PROFILE_ERROR)}$"),
    ):
        module._validate_sample_internal_attribute_profile(infos=tuple(archive.infolist()))


def test_internal_attribute_profile_accepts_zero_and_empty(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "internal-attribute-zero.zip"
    _write_small_bundle(bundle, internal_attr=0)
    with zipfile.ZipFile(bundle) as archive:
        module._validate_sample_internal_attribute_profile(infos=tuple(archive.infolist()))
    module._validate_sample_internal_attribute_profile(infos=())


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_emits_zero_internal_attributes(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert {info.internal_attr for info in infos} == {0}


def test_m109_source_checks_internal_attributes_after_m108_before_inventory() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    flag_profile = extraction.index("_validate_sample_general_purpose_flag_profile(")
    reserved_profile = extraction.index(
        "_validate_sample_extraction_version_reserved_byte_profile("
    )
    extraction_profile = extraction.index("_validate_sample_extraction_version_profile(")
    creation_profile = extraction.index("_validate_sample_creation_version_profile(")
    internal_profile = extraction.index("_validate_sample_internal_attribute_profile(")
    inventory = extraction.index("_validate_sample_inventory(observed_members)")
    assert (
        flag_profile
        < reserved_profile
        < extraction_profile
        < creation_profile
        < internal_profile
        < inventory
    )
    helper = source[source.index("def _validate_sample_internal_attribute_profile") :]
    assert "info.internal_attr" in helper
    assert "info.external_attr" not in helper
    assert "info.create_system" not in helper
    assert "archive.read" not in helper
    assert "zipfile._" not in helper


def test_m109_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m109" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m109_docs_define_zero_internal_attribute_profile_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0092-require-zero-sample-member-internal-attributes.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M109" in combined
    assert "zero sample-member internal-attribute profile preflight" in combined
    assert _PROFILE_ERROR in combined
    assert "one central-internal-attribute exact-profile classifier" in combined
    assert "no text/binary content interpretation" in combined
    assert "no payload-content read" in combined
    assert "no workflow" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
