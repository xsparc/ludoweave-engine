"""Protect M90 local-header signature preflight."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import tempfile
import zipfile
from io import BytesIO
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
_EOCD_SIGNATURE = b"PK\x05\x06"
_CENTRAL_SIGNATURE = b"PK\x01\x02"
_LOCAL_SIGNATURE = b"PK\x03\x04"
_SIGNATURE_ERROR = "sample bundle local header signature is inconsistent"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_local_header_signatures(
        self,
        *,
        snapshot: IO[bytes],
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
    return cast(_SmokeModule, _load(_SMOKE, "m90_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m90_release_artifacts"))


def _write_small_bundle(path: Path, *, members: int = 2) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index in range(members):
            archive.writestr(f"{_PREFIX}/member-{index}.txt", f"payload-{index}".encode())


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


def _directory_offset(data: bytes | bytearray) -> int:
    end = bytes(data).rindex(_EOCD_SIGNATURE)
    return int.from_bytes(data[end + 16 : end + 20], "little")


def _member_offset(data: bytes | bytearray, member: int) -> int:
    record, _ = _central_records(data)[member]
    return int.from_bytes(data[record + 42 : record + 46], "little")


def _set_member_offset(path: Path, member: int, offset: int) -> None:
    data = bytearray(path.read_bytes())
    record, _ = _central_records(data)[member]
    data[record + 42 : record + 46] = offset.to_bytes(4, "little")
    path.write_bytes(data)


def _shift_member_offset(path: Path, member: int = 1, delta: int = 1) -> None:
    data = path.read_bytes()
    _set_member_offset(path, member, _member_offset(data, member) + delta)


def _point_member_at_central_directory(path: Path, member: int = -1) -> None:
    data = path.read_bytes()
    _set_member_offset(path, member, _directory_offset(data))


def _set_archive_entry_counts(path: Path, count: int) -> None:
    data = bytearray(path.read_bytes())
    end = bytes(data).rindex(_EOCD_SIGNATURE)
    data[end + 8 : end + 10] = count.to_bytes(2, "little")
    data[end + 10 : end + 12] = count.to_bytes(2, "little")
    path.write_bytes(data)


def _shift_declared_directory_offset(path: Path, delta: int) -> None:
    data = bytearray(path.read_bytes())
    end = bytes(data).rindex(_EOCD_SIGNATURE)
    offset = int.from_bytes(data[end + 16 : end + 20], "little")
    data[end + 16 : end + 20] = (offset + delta).to_bytes(4, "little")
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


def test_cpython_exposes_shifted_offset_and_defers_signature_failure(tmp_path: Path) -> None:
    bundle = tmp_path / "signature.zip"
    _write_small_bundle(bundle)
    original_second = _member_offset(bundle.read_bytes(), 1)
    _shift_member_offset(bundle)
    data = bundle.read_bytes()

    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert [info.header_offset for info in infos] == [0, original_second + 1]
        assert data[infos[0].header_offset : infos[0].header_offset + 4] == _LOCAL_SIGNATURE
        assert data[infos[1].header_offset : infos[1].header_offset + 4] != _LOCAL_SIGNATURE
        assert archive.read(infos[0]) == b"payload-0"
        with pytest.raises(zipfile.BadZipFile):
            archive.read(infos[1])


def test_signature_error_precedes_inventory_staging_and_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "producer-signature.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    _shift_member_offset(bundle)
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("signature policy must fail before later processing")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_SIGNATURE_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )
    assert list(output.iterdir()) == []


def test_signature_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "signature-cleanup.zip"
    _write_small_bundle(bundle)
    _shift_member_offset(bundle)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_SIGNATURE_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_entry_count_error_precedes_signature_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "counts-before-signature.zip"
    _write_small_bundle(bundle)
    _shift_member_offset(bundle)
    _set_archive_entry_counts(bundle, 0)
    with pytest.raises(
        RuntimeError, match=r"^sample bundle archive entry counts are inconsistent$"
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_directory_placement_error_precedes_signature_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "placement-before-signature.zip"
    _write_small_bundle(bundle)
    _shift_member_offset(bundle)
    _shift_declared_directory_offset(bundle, -1)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle central directory placement is inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_first_header_error_precedes_signature_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "first-before-signature.zip"
    _write_small_bundle(bundle)
    _insert_leading_gap(bundle, b"prefix")
    _shift_member_offset(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle first local header placement is inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_distinct_offset_error_precedes_signature_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "distinct-before-signature.zip"
    _write_small_bundle(bundle)
    _set_member_offset(bundle, 1, 0)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header offsets are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_order_error_precedes_signature_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "order-before-signature.zip"
    _write_small_bundle(bundle)
    _shift_member_offset(bundle)
    _swap_first_two_central_records(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header offsets are out of order$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_bounds_error_precedes_signature_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "bounds-before-signature.zip"
    _write_small_bundle(bundle)
    _point_member_at_central_directory(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header offsets are out of bounds$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_signature_policy_precedes_nul_name_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "signature-before-name.zip"
    _write_small_bundle(bundle)
    _shift_member_offset(bundle)
    _nul_suffix_first_central_name(bundle)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_SIGNATURE_ERROR)}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_signature_validator_accepts_empty_and_valid_offsets_and_restores_position() -> None:
    module = _smoke()
    snapshot = BytesIO(_LOCAL_SIGNATURE + b"data" + _LOCAL_SIGNATURE)
    snapshot.seek(3)
    module._validate_sample_local_header_signatures(snapshot=snapshot, infos=())
    module._validate_sample_local_header_signatures(
        snapshot=snapshot,
        infos=(_info("one", 0), _info("two", 8)),
    )
    assert snapshot.tell() == 3


@pytest.mark.parametrize(
    ("payload", "offset"),
    ((b"BAD!", 0), (_LOCAL_SIGNATURE + b"BAD!", 4), (_LOCAL_SIGNATURE[:3], 0)),
)
def test_signature_validator_rejects_invalid_or_short_signatures(
    payload: bytes,
    offset: int,
) -> None:
    module = _smoke()
    snapshot = BytesIO(payload)
    snapshot.seek(len(payload))
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_SIGNATURE_ERROR)}$"):
        module._validate_sample_local_header_signatures(
            snapshot=snapshot,
            infos=(_info("member", offset),),
        )
    assert snapshot.tell() == len(payload)


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_offsets_point_to_local_header_signatures(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    assert all(
        data[info.header_offset : info.header_offset + 4] == _LOCAL_SIGNATURE for info in infos
    )


def test_m90_source_checks_signatures_after_m89_before_names() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    bounds = extraction.index("_validate_sample_local_header_bounds(")
    signatures = extraction.index("_validate_sample_local_header_signatures(")
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert bounds < signatures < name < metadata
    helper = source[source.index("def _validate_sample_local_header_signatures") :]
    assert "info.header_offset" in helper
    assert ".read(4)" in helper
    assert "zipfile._" not in helper


def test_m90_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m90" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m90_docs_define_signature_rule_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0073-require-local-header-signatures.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M90" in combined
    assert "four-byte local-header signature" in combined
    assert _SIGNATURE_ERROR in combined
    assert "signature classifier" in combined
    assert "no local-header field parser" in combined
    assert "no inter-member layout validator" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
