"""Protect M86 first local-header placement preflight."""

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
_EOCD_SIGNATURE = b"PK\x05\x06"
_CENTRAL_SIGNATURE = b"PK\x01\x02"
_PLACEMENT_ERROR = "sample bundle first local header placement is inconsistent"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_first_local_header(
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
    return cast(_SmokeModule, _load(_SMOKE, "m86_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m86_release_artifacts"))


def _write_bundle(path: Path, *, hidden_suffix: str = "") -> None:
    with zipfile.ZipFile(path, "w") as archive:
        info = zipfile.ZipInfo(f"{_PREFIX}/README.md{hidden_suffix}")
        info.orig_filename = info.filename
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, b"sample")


def _insert_leading_gap(path: Path, prefix: bytes) -> None:
    data = bytearray(path.read_bytes())
    central = data.index(_CENTRAL_SIGNATURE)
    end = data.rindex(_EOCD_SIGNATURE)
    header_offset = int.from_bytes(data[central + 42 : central + 46], "little")
    directory_offset = int.from_bytes(data[end + 16 : end + 20], "little")
    data[central + 42 : central + 46] = (header_offset + len(prefix)).to_bytes(4, "little")
    data[end + 16 : end + 20] = (directory_offset + len(prefix)).to_bytes(4, "little")
    path.write_bytes(prefix + data)


def _prepend_without_offset_updates(path: Path, prefix: bytes) -> None:
    path.write_bytes(prefix + path.read_bytes())


def _set_archive_entry_counts(path: Path, count: int) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    data[end + 8 : end + 10] = count.to_bytes(2, "little")
    data[end + 10 : end + 12] = count.to_bytes(2, "little")
    path.write_bytes(data)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize("prefix", (b"x", b"prefix-data"))
def test_cpython_reads_zero_adjustment_archive_with_leading_local_gap(
    tmp_path: Path,
    prefix: bytes,
) -> None:
    bundle = tmp_path / f"leading-gap-{len(prefix)}.zip"
    _write_bundle(bundle)
    _insert_leading_gap(bundle, prefix)

    data = bundle.read_bytes()
    end = data.rindex(_EOCD_SIGNATURE)
    directory_size = int.from_bytes(data[end + 12 : end + 16], "little")
    directory_offset = int.from_bytes(data[end + 16 : end + 20], "little")
    with zipfile.ZipFile(bundle) as archive:
        [info] = archive.infolist()
        assert info.header_offset == len(prefix)
        assert archive.read(info) == b"sample"
    assert end == directory_size + directory_offset


@pytest.mark.parametrize("prefix", (b"x", b"prefix-data"))
def test_leading_local_gap_fails_before_inventory_staging_or_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    prefix: bytes,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"rejected-gap-{len(prefix)}.zip"
    _write_bundle(bundle)
    _insert_leading_gap(bundle, prefix)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("local-header policy must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("local-header policy must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("local-header policy must fail before inventory")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PLACEMENT_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


def test_local_header_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "local-header-cleanup.zip"
    _write_bundle(bundle)
    _insert_leading_gap(bundle, b"prefix")
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PLACEMENT_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_m85_geometry_error_precedes_first_local_header_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "geometry-before-local-header.zip"
    _write_bundle(bundle)
    _prepend_without_offset_updates(bundle, b"prefix")

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle central directory placement is inconsistent$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_entry_count_error_precedes_first_local_header_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "counts-before-local-header.zip"
    _write_bundle(bundle)
    _insert_leading_gap(bundle, b"prefix")
    _set_archive_entry_counts(bundle, 0)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle archive entry counts are inconsistent$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_first_local_header_policy_precedes_nul_name_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "local-header-before-nul.zip"
    _write_bundle(bundle, hidden_suffix="\x00hidden")
    _insert_leading_gap(bundle, b"prefix")

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PLACEMENT_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_first_local_header_validator_accepts_zero_or_empty_inventory() -> None:
    module = _smoke()
    info = zipfile.ZipInfo("payload.txt")
    info.header_offset = 0

    module._validate_sample_first_local_header(infos=(info,))
    module._validate_sample_first_local_header(infos=())


def test_empty_archive_retains_exact_inventory_error_before_staging_or_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("empty inventory must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("empty inventory must fail before staging")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)

    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


@pytest.mark.parametrize("offset", (1, 11, 0xFFFFFFFF))
def test_first_local_header_validator_rejects_nonzero_earliest_offset(offset: int) -> None:
    module = _smoke()
    first = zipfile.ZipInfo("first.txt")
    first.header_offset = offset
    later = zipfile.ZipInfo("later.txt")
    later.header_offset = offset + 7

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_PLACEMENT_ERROR)}$"):
        module._validate_sample_first_local_header(infos=(later, first))


def test_current_producer_starts_earliest_local_header_at_zero(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert min(info.header_offset for info in infos) == 0


def test_m86_source_checks_first_header_after_m85_before_names() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    placement = extraction.index("_validate_sample_archive_placement(snapshot=snapshot_stream)")
    first_header = extraction.index("_validate_sample_first_local_header(infos=infos)")
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert placement < first_header < name < metadata
    helper = source[source.index("def _validate_sample_first_local_header") :]
    assert "info.header_offset" in helper
    assert "zipfile._" not in helper


def test_m86_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
    assert hashlib.sha256((_ROOT / ".github/workflows/ci.yml").read_bytes()).hexdigest() == (
        _CI_SHA256
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        _RELEASE_SHA256
    )
    assert hashlib.sha256(_STAGER.read_bytes()).hexdigest() == _STAGER_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == _PYPROJECT_SHA256
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m86" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m86_docs_define_first_header_rule_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0069-require-first-local-header-at-zero.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M86" in combined
    assert "first local header" in combined
    assert _PLACEMENT_ERROR in combined
    assert "no local-header parser" in combined
    assert "no inter-member layout validator" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
