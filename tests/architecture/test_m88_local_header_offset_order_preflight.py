"""Protect M88 parser-exposed local-header offset order."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import tempfile
import zipfile
from itertools import pairwise
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
_ORDER_ERROR = "sample bundle local header offsets are out of order"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_local_header_order(
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
    return cast(_SmokeModule, _load(_SMOKE, "m88_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m88_release_artifacts"))


def _write_small_bundle(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f"{_PREFIX}/first.txt", b"first")
        archive.writestr(f"{_PREFIX}/second.txt", b"second")


def _central_records(data: bytes | bytearray) -> list[tuple[int, int]]:
    end = bytes(data).rindex(_EOCD_SIGNATURE)
    cursor = int.from_bytes(data[end + 16 : end + 20], "little")
    records: list[tuple[int, int]] = []
    while cursor < end and bytes(data[cursor : cursor + 4]) == _CENTRAL_SIGNATURE:
        name_size = int.from_bytes(data[cursor + 28 : cursor + 30], "little")
        extra_size = int.from_bytes(data[cursor + 30 : cursor + 32], "little")
        comment_size = int.from_bytes(data[cursor + 32 : cursor + 34], "little")
        next_cursor = cursor + 46 + name_size + extra_size + comment_size
        records.append((cursor, next_cursor))
        cursor = next_cursor
    return records


def _swap_first_two_central_records(path: Path) -> None:
    data = path.read_bytes()
    first, second, *_ = _central_records(data)
    assert first[1] == second[0]
    path.write_bytes(
        data[: first[0]]
        + data[second[0] : second[1]]
        + data[first[0] : first[1]]
        + data[second[1] :]
    )


def _alias_second_local_header(path: Path) -> None:
    data = bytearray(path.read_bytes())
    first, second, *_ = _central_records(data)
    data[second[0] + 42 : second[0] + 46] = data[first[0] + 42 : first[0] + 46]
    path.write_bytes(data)


def _insert_leading_gap(path: Path, prefix: bytes) -> None:
    data = bytearray(path.read_bytes())
    end = bytes(data).rindex(_EOCD_SIGNATURE)
    for record, _ in _central_records(data):
        offset = int.from_bytes(data[record + 42 : record + 46], "little")
        data[record + 42 : record + 46] = (offset + len(prefix)).to_bytes(4, "little")
    directory_offset = int.from_bytes(data[end + 16 : end + 20], "little")
    data[end + 16 : end + 20] = (directory_offset + len(prefix)).to_bytes(4, "little")
    path.write_bytes(prefix + data)


def _set_archive_entry_counts(path: Path, count: int) -> None:
    data = bytearray(path.read_bytes())
    end = bytes(data).rindex(_EOCD_SIGNATURE)
    data[end + 8 : end + 10] = count.to_bytes(2, "little")
    data[end + 10 : end + 12] = count.to_bytes(2, "little")
    path.write_bytes(data)


def _nul_suffix_first_central_name(path: Path) -> None:
    data = bytearray(path.read_bytes())
    first, *_ = _central_records(data)
    name_size = int.from_bytes(data[first[0] + 28 : first[0] + 30], "little")
    data[first[0] + 46 + name_size - 1] = 0
    path.write_bytes(data)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _info(name: str, offset: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name)
    info.header_offset = offset
    return info


def test_cpython_exposes_central_order_and_reads_reordered_members(tmp_path: Path) -> None:
    bundle = tmp_path / "reordered.zip"
    _write_small_bundle(bundle)
    _swap_first_two_central_records(bundle)

    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert [info.filename.rsplit("/", 1)[-1] for info in infos] == [
            "second.txt",
            "first.txt",
        ]
        assert [info.header_offset for info in infos] == [72, 0]
        assert [archive.read(info) for info in infos] == [b"second", b"first"]


def test_reordered_offsets_fail_before_inventory_staging_or_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "reordered-producer.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    _swap_first_two_central_records(bundle)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("order policy must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("order policy must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("order policy must fail before inventory")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ORDER_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


def test_order_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "reordered-cleanup.zip"
    _write_small_bundle(bundle)
    _swap_first_two_central_records(bundle)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ORDER_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_entry_count_error_precedes_order_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "counts-before-order.zip"
    _write_small_bundle(bundle)
    _swap_first_two_central_records(bundle)
    _set_archive_entry_counts(bundle, 0)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle archive entry counts are inconsistent$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_first_header_error_precedes_order_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "first-header-before-order.zip"
    _write_small_bundle(bundle)
    _swap_first_two_central_records(bundle)
    _insert_leading_gap(bundle, b"prefix")

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle first local header placement is inconsistent$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_distinct_offset_error_precedes_order_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "distinct-before-order.zip"
    _write_small_bundle(bundle)
    _alias_second_local_header(bundle)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header offsets are inconsistent$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_order_policy_precedes_nul_name_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "order-before-name.zip"
    _write_small_bundle(bundle)
    _swap_first_two_central_records(bundle)
    _nul_suffix_first_central_name(bundle)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ORDER_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_order_validator_accepts_empty_single_and_strictly_increasing_offsets() -> None:
    module = _smoke()

    module._validate_sample_local_header_order(infos=())
    module._validate_sample_local_header_order(infos=(_info("one", 0),))
    module._validate_sample_local_header_order(
        infos=(_info("one", 0), _info("two", 17), _info("three", 101))
    )


@pytest.mark.parametrize("offsets", ((1, 0), (17, 0), (0, 0), (0, 11, 1)))
def test_order_validator_rejects_non_increasing_offsets(offsets: tuple[int, ...]) -> None:
    module = _smoke()
    infos = tuple(_info(str(index), offset) for index, offset in enumerate(offsets))

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ORDER_ERROR)}$"):
        module._validate_sample_local_header_order(infos=infos)


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass

    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_has_strictly_increasing_local_header_offsets(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        offsets = tuple(info.header_offset for info in archive.infolist())
    assert len(offsets) == 50
    assert all(left < right for left, right in pairwise(offsets))


def test_m88_source_checks_order_after_m87_before_names() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    distinct = extraction.index("_validate_sample_local_header_offsets(infos=infos)")
    order = extraction.index("_validate_sample_local_header_order(infos=infos)")
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert distinct < order < name < metadata
    helper = source[source.index("def _validate_sample_local_header_order") :]
    assert "info.header_offset" in helper
    assert "zipfile._" not in helper


def test_m88_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m88" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m88_docs_define_strict_order_rule_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0071-require-local-header-offset-order.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M88" in combined
    assert "strictly increasing local-header offsets" in combined
    assert _ORDER_ERROR in combined
    assert "no local-header parser" in combined
    assert "no inter-member layout validator" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
