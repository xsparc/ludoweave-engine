"""Protect M87 distinct parser-exposed local-header offsets."""

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
_OFFSET_ERROR = "sample bundle local header offsets are inconsistent"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_local_header_offsets(
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
    return cast(_SmokeModule, _load(_SMOKE, "m87_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m87_release_artifacts"))


def _write_small_bundle(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f"{_PREFIX}/first.txt", b"first")
        archive.writestr(f"{_PREFIX}/second.txt", b"second")


def _central_records(data: bytearray) -> list[int]:
    end = data.rindex(_EOCD_SIGNATURE)
    cursor = int.from_bytes(data[end + 16 : end + 20], "little")
    records: list[int] = []
    while cursor < end and bytes(data[cursor : cursor + 4]) == _CENTRAL_SIGNATURE:
        records.append(cursor)
        name_size = int.from_bytes(data[cursor + 28 : cursor + 30], "little")
        extra_size = int.from_bytes(data[cursor + 30 : cursor + 32], "little")
        comment_size = int.from_bytes(data[cursor + 32 : cursor + 34], "little")
        cursor += 46 + name_size + extra_size + comment_size
    return records


def _alias_second_local_header(path: Path) -> None:
    data = bytearray(path.read_bytes())
    first, second, *_ = _central_records(data)
    data[second + 42 : second + 46] = data[first + 42 : first + 46]
    path.write_bytes(data)


def _insert_leading_gap(path: Path, prefix: bytes) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    records = _central_records(data)
    for record in records:
        offset = int.from_bytes(data[record + 42 : record + 46], "little")
        data[record + 42 : record + 46] = (offset + len(prefix)).to_bytes(4, "little")
    directory_offset = int.from_bytes(data[end + 16 : end + 20], "little")
    data[end + 16 : end + 20] = (directory_offset + len(prefix)).to_bytes(4, "little")
    path.write_bytes(prefix + data)


def _set_archive_entry_counts(path: Path, count: int) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    data[end + 8 : end + 10] = count.to_bytes(2, "little")
    data[end + 10 : end + 12] = count.to_bytes(2, "little")
    path.write_bytes(data)


def _nul_suffix_second_central_name(path: Path) -> None:
    data = bytearray(path.read_bytes())
    _, second, *_ = _central_records(data)
    name_size = int.from_bytes(data[second + 28 : second + 30], "little")
    data[second + 46 + name_size - 1] = 0
    path.write_bytes(data)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.filterwarnings("ignore:Overlapped entries.*:UserWarning")
def test_cpython_exposes_duplicate_offsets_and_defers_failure_to_member_open(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "duplicate-offsets.zip"
    _write_small_bundle(bundle)
    _alias_second_local_header(bundle)

    with zipfile.ZipFile(bundle) as archive:
        first, second = archive.infolist()
        assert [first.header_offset, second.header_offset] == [0, 0]
        assert archive.read(first) == b"first"
        with pytest.raises(zipfile.BadZipFile, match=r"^File name in directory"):
            archive.read(second)


def test_duplicate_offsets_fail_before_inventory_staging_or_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "aliased-producer.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    _alias_second_local_header(bundle)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("offset policy must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("offset policy must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("offset policy must fail before inventory")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_OFFSET_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


def test_duplicate_offset_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "duplicate-cleanup.zip"
    _write_small_bundle(bundle)
    _alias_second_local_header(bundle)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_OFFSET_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_entry_count_error_precedes_distinct_offset_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "counts-before-offsets.zip"
    _write_small_bundle(bundle)
    _alias_second_local_header(bundle)
    _set_archive_entry_counts(bundle, 0)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle archive entry counts are inconsistent$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_m86_first_header_error_precedes_distinct_offset_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "first-header-before-distinct.zip"
    _write_small_bundle(bundle)
    _alias_second_local_header(bundle)
    _insert_leading_gap(bundle, b"prefix")

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle first local header placement is inconsistent$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_distinct_offset_policy_precedes_nul_name_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "offsets-before-name.zip"
    _write_small_bundle(bundle)
    _alias_second_local_header(bundle)
    _nul_suffix_second_central_name(bundle)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_OFFSET_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_distinct_offset_validator_accepts_empty_single_and_unique_offsets() -> None:
    module = _smoke()
    first = zipfile.ZipInfo("first.txt")
    first.header_offset = 0
    second = zipfile.ZipInfo("second.txt")
    second.header_offset = 17

    module._validate_sample_local_header_offsets(infos=())
    module._validate_sample_local_header_offsets(infos=(first,))
    module._validate_sample_local_header_offsets(infos=(second, first))


@pytest.mark.parametrize("offset", (0, 1, 11, 0xFFFFFFFF))
def test_distinct_offset_validator_rejects_duplicate_offsets(offset: int) -> None:
    module = _smoke()
    first = zipfile.ZipInfo("first.txt")
    first.header_offset = offset
    second = zipfile.ZipInfo("second.txt")
    second.header_offset = offset

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_OFFSET_ERROR)}$"):
        module._validate_sample_local_header_offsets(infos=(first, second))


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass

    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_has_50_distinct_local_header_offsets(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert len({info.header_offset for info in infos}) == len(infos)


def test_m87_source_checks_distinct_offsets_after_m86_before_names() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    first_header = extraction.index("_validate_sample_first_local_header(infos=infos)")
    distinct = extraction.index("_validate_sample_local_header_offsets(infos=infos)")
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert first_header < distinct < name < metadata
    helper = source[source.index("def _validate_sample_local_header_offsets") :]
    assert "info.header_offset" in helper
    assert "zipfile._" not in helper


def test_m87_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m87" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m87_docs_define_distinct_offset_rule_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0070-require-distinct-local-header-offsets.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M87" in combined
    assert "distinct local-header offsets" in combined
    assert _OFFSET_ERROR in combined
    assert "no local-header parser" in combined
    assert "no inter-member layout validator" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
