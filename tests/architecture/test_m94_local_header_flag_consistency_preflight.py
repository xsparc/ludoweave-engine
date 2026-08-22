"""Protect M94 local-header flag-consistency preflight."""

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
_FIXED_LOCAL_HEADER_BYTES = 30
_LOCAL_FLAG_OFFSET = 6
_LOCAL_NAME_LENGTH_OFFSET = 26
_LOCAL_EXTRA_LENGTH_OFFSET = 28
_FLAG_ERROR = "sample bundle local header flags are inconsistent"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_local_header_flags(
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
    return cast(_SmokeModule, _load(_SMOKE, "m94_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m94_release_artifacts"))


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


def _change_local_flags(path: Path, *, member: int = -1, flags: int = 1) -> None:
    with zipfile.ZipFile(path) as archive:
        info = archive.infolist()[member]
        assert info.flag_bits != flags
        offset = info.header_offset
    data = bytearray(path.read_bytes())
    data[offset + _LOCAL_FLAG_OFFSET : offset + _LOCAL_FLAG_OFFSET + 2] = flags.to_bytes(
        2, "little"
    )
    path.write_bytes(data)


def _change_local_name(path: Path, *, member: int = -1) -> None:
    with zipfile.ZipFile(path) as archive:
        offset = archive.infolist()[member].header_offset
    data = bytearray(path.read_bytes())
    name_length = int.from_bytes(
        data[offset + _LOCAL_NAME_LENGTH_OFFSET : offset + _LOCAL_EXTRA_LENGTH_OFFSET],
        "little",
    )
    name_start = offset + _FIXED_LOCAL_HEADER_BYTES
    data[name_start + name_length - 1] ^= 1
    path.write_bytes(data)


def _set_member_offset(path: Path, member: int, offset: int) -> None:
    data = bytearray(path.read_bytes())
    record, _ = _central_records(data)[member]
    data[record + 42 : record + 46] = offset.to_bytes(4, "little")
    path.write_bytes(data)


def _point_member_near_directory(path: Path, *, member: int = -1) -> None:
    data = bytearray(path.read_bytes())
    directory_offset = _directory_offset(data)
    shifted_offset = directory_offset - len(_LOCAL_SIGNATURE)
    record, _ = _central_records(data)[member]
    data[record + 42 : record + 46] = shifted_offset.to_bytes(4, "little")
    data[shifted_offset:directory_offset] = _LOCAL_SIGNATURE
    path.write_bytes(data)


def _set_local_header_lengths(path: Path, *, member: int = -1) -> None:
    with zipfile.ZipFile(path) as archive:
        offset = archive.infolist()[member].header_offset
    data = bytearray(path.read_bytes())
    data[offset + _LOCAL_NAME_LENGTH_OFFSET : offset + _LOCAL_EXTRA_LENGTH_OFFSET] = (
        0xFFFF
    ).to_bytes(2, "little")
    path.write_bytes(data)


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


def _corrupt_local_signature(path: Path, member: int = -1) -> None:
    with zipfile.ZipFile(path) as archive:
        offset = archive.infolist()[member].header_offset
    data = bytearray(path.read_bytes())
    data[offset : offset + len(_LOCAL_SIGNATURE)] = b"BAD!"
    path.write_bytes(data)


def _nul_suffix_first_local_and_central_name(path: Path) -> None:
    data = bytearray(path.read_bytes())
    first, *_ = _central_records(data)
    name_size = int.from_bytes(data[first[0] + 28 : first[0] + 30], "little")
    data[first[0] + 46 + name_size - 1] = 0
    local_offset = int.from_bytes(data[first[0] + 42 : first[0] + 46], "little")
    data[local_offset + _FIXED_LOCAL_HEADER_BYTES + name_size - 1] = 0
    path.write_bytes(data)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _info(offset: int, *, flags: int = 0) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo("member.txt")
    info.header_offset = offset
    info.flag_bits = flags
    return info


def _snapshot_with_local_flags(*, header_offset: int, flags: int) -> BytesIO:
    data = bytearray(header_offset + _FIXED_LOCAL_HEADER_BYTES)
    data[header_offset : header_offset + 4] = _LOCAL_SIGNATURE
    data[header_offset + _LOCAL_FLAG_OFFSET : header_offset + _LOCAL_FLAG_OFFSET + 2] = (
        flags.to_bytes(2, "little")
    )
    return BytesIO(data)


def test_cpython_ignores_local_only_flag_mismatch_during_reads(tmp_path: Path) -> None:
    bundle = tmp_path / "flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)

    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
        assert [info.flag_bits for info in infos] == [0, 0]
        assert (
            int.from_bytes(
                data[
                    infos[1].header_offset + _LOCAL_FLAG_OFFSET : infos[1].header_offset
                    + _LOCAL_FLAG_OFFSET
                    + 2
                ],
                "little",
            )
            == 1
        )
        assert [archive.read(info) for info in infos] == [b"payload-0", b"payload-1"]


def test_flag_error_precedes_inventory_staging_and_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "producer-flags.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    _change_local_flags(bundle)
    output = _empty_output(tmp_path)

    def forbidden(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("local-flag policy must fail before later processing")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_FLAG_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )
    assert list(output.iterdir()) == []


def test_flag_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "flags-cleanup.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: object) -> zipfile.ZipFile:
        archive = original_zipfile(file)  # type: ignore[arg-type]
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_FLAG_ERROR)}$"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert len(archives) == 1
    assert archives[0].fp is None
    renamed = bundle.with_suffix(".closed")
    bundle.rename(renamed)
    renamed.rename(bundle)
    assert list(output.iterdir()) == []


def test_entry_count_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "counts-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _set_archive_entry_counts(bundle, 0)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle archive entry counts are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_directory_placement_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "placement-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _shift_declared_directory_offset(bundle, -1)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle central directory placement is inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_first_header_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "first-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _insert_leading_gap(bundle, b"prefix")
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle first local header placement is inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_distinct_offset_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "distinct-before-flags.zip"
    _write_small_bundle(bundle, members=3)
    _change_local_flags(bundle)
    with zipfile.ZipFile(bundle) as archive:
        final_offset = archive.infolist()[-1].header_offset
    _set_member_offset(bundle, 1, final_offset)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header offsets are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_order_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "order-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _swap_first_two_central_records(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header offsets are out of order$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_offset_bounds_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "bounds-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _set_member_offset(bundle, 1, _directory_offset(bundle.read_bytes()))
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header offsets are out of bounds$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_signature_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "signature-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _corrupt_local_signature(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header signature is inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_prefix_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "prefix-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _point_member_near_directory(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header prefixes are out of bounds$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_envelope_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "envelope-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _set_local_header_lengths(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header envelopes are out of bounds$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_name_error_precedes_flag_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "names-before-flags.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle)
    _change_local_name(bundle)
    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle local header names are inconsistent$",
    ):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_flag_policy_precedes_nul_name_policy(tmp_path: Path) -> None:
    bundle = tmp_path / "flags-before-nul.zip"
    _write_small_bundle(bundle)
    _change_local_flags(bundle, member=0)
    _nul_suffix_first_local_and_central_name(bundle)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_FLAG_ERROR)}$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_flag_validator_accepts_empty_and_equal_flags_and_restores_position() -> None:
    module = _smoke()
    snapshot = _snapshot_with_local_flags(header_offset=10, flags=0x0802)
    snapshot.seek(3)
    module._validate_sample_local_header_flags(snapshot=snapshot, infos=())
    module._validate_sample_local_header_flags(
        snapshot=snapshot,
        infos=(_info(10, flags=0x0802),),
    )
    assert snapshot.tell() == 3


@pytest.mark.parametrize("local_flags", (1, 8, 0x0800, 0xFFFF))
def test_flag_validator_rejects_any_local_central_mismatch(local_flags: int) -> None:
    module = _smoke()
    snapshot = _snapshot_with_local_flags(header_offset=10, flags=local_flags)
    snapshot.seek(5)
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_FLAG_ERROR)}$"):
        module._validate_sample_local_header_flags(
            snapshot=snapshot,
            infos=(_info(10),),
        )
    assert snapshot.tell() == 5


def test_empty_archive_retains_exact_inventory_error(tmp_path: Path) -> None:
    bundle = tmp_path / "empty.zip"
    with zipfile.ZipFile(bundle, "w"):
        pass
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$"):
        _smoke()._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_current_producer_local_flags_match_central_flags(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    data = bundle.read_bytes()
    with zipfile.ZipFile(bundle) as archive:
        infos = tuple(archive.infolist())
    assert len(infos) == 50
    for info in infos:
        local_flags = int.from_bytes(
            data[
                info.header_offset + _LOCAL_FLAG_OFFSET : info.header_offset
                + _LOCAL_FLAG_OFFSET
                + 2
            ],
            "little",
        )
        assert local_flags == info.flag_bits


def test_m94_source_checks_local_flags_after_m93_before_decoded_name_policy() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    local_names = extraction.index("_validate_sample_local_header_names(")
    local_flags = extraction.index("_validate_sample_local_header_flags(")
    decoded_name = extraction.index(
        "_validate_sample_member_name(original_name=info.orig_filename)"
    )
    metadata = extraction.index("total_bytes = 0")
    assert local_names < local_flags < decoded_name < metadata
    helper = source[source.index("def _validate_sample_local_header_flags") :]
    assert "info.header_offset" in helper
    assert "info.flag_bits" in helper
    assert "int.from_bytes" in helper
    assert "zipfile._" not in helper


def test_m94_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m94" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src/ludoweave").rglob("*.py")
    )


def test_m94_docs_define_flag_rule_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/release-process.md",
        _ROOT / "docs/rfcs/0077-require-consistent-local-header-flags.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M94" in combined
    assert "local-header flag consistency" in combined
    assert _FLAG_ERROR in combined
    assert "one two-byte local-flag consistency classifier" in combined
    assert "no local compression-method comparison" in combined
    assert "no extra-field comparison" in combined
    assert "no inter-member layout validator" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    current = re.search(
        r"> Current validation: M0 through M(?P<milestone>\d+) are hosted-validated",
        readme,
    )
    project = re.search(
        r"> Project status: community-alpha release candidate \(`0\.1\.0a1`\)\. "
        r"M0 through M(?P<milestone>\d+) are hosted-validated",
        readme,
    )
    assert current is not None and project is not None
    assert current.group("milestone") == project.group("milestone")
    assert int(current.group("milestone")) >= 93
