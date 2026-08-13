"""Protect M84 conventional archive entry-count preflight."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import io
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
_EOCD_SIGNATURE = b"PK\x05\x06"
_COUNT_ERROR = "sample bundle archive entry counts are inconsistent"


class _SmokeModule(Protocol):
    def _extract_bundle(
        self,
        bundle: Path,
        output: Path,
        *,
        version: str,
        expected_sha256: str | None = None,
    ) -> Path: ...

    def _validate_sample_archive_entry_counts(
        self,
        *,
        snapshot: IO[bytes],
        parsed_entries: int,
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
    return cast(_SmokeModule, _load(_SMOKE, "m84_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m84_release_artifacts"))


def _write_member(
    archive: zipfile.ZipFile,
    *,
    name: str,
    payload: bytes,
    hidden_suffix: str = "",
) -> None:
    info = zipfile.ZipInfo("placeholder")
    info.filename = f"{name}{hidden_suffix}"
    info.orig_filename = info.filename
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, payload)


def _write_bundle(path: Path, *, hidden_suffix: str = "", members: int = 1) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for index in range(members):
            name = "README.md" if index == 0 else f"member-{index}.txt"
            _write_member(
                archive,
                name=f"{_PREFIX}/{name}",
                hidden_suffix=hidden_suffix if index == 0 else "",
                payload=f"sample-{index}".encode(),
            )


def _set_archive_entry_counts(
    path: Path,
    *,
    entries_on_disk: int,
    total_entries: int,
) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    data[end + 8 : end + 10] = entries_on_disk.to_bytes(2, "little")
    data[end + 10 : end + 12] = total_entries.to_bytes(2, "little")
    path.write_bytes(data)


def _set_archive_disk_fields(path: Path, *, disk: int, central_disk: int) -> None:
    data = bytearray(path.read_bytes())
    end = data.rindex(_EOCD_SIGNATURE)
    data[end + 4 : end + 6] = disk.to_bytes(2, "little")
    data[end + 6 : end + 8] = central_disk.to_bytes(2, "little")
    path.write_bytes(data)


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    ("entries_on_disk", "total_entries"),
    ((1, 1), (0, 1), (1, 0), (0, 0), (2, 2), (0xFFFF, 0xFFFF)),
)
def test_cpython_ignores_conventional_entry_counts_while_reading_payload(
    tmp_path: Path,
    entries_on_disk: int,
    total_entries: int,
) -> None:
    bundle = tmp_path / f"accepted-{entries_on_disk}-{total_entries}.zip"
    _write_bundle(bundle)
    _set_archive_entry_counts(
        bundle,
        entries_on_disk=entries_on_disk,
        total_entries=total_entries,
    )

    with zipfile.ZipFile(bundle) as archive:
        [info] = archive.infolist()
        assert info.volume == 0
        assert info.extra == b""
        assert info.flag_bits == 0
        assert archive.read(info) == b"sample-0"


@pytest.mark.parametrize(
    ("members", "entries_on_disk", "total_entries"),
    (
        (1, 0, 1),
        (1, 1, 0),
        (1, 0, 0),
        (1, 2, 2),
        (1, 0xFFFF, 0xFFFF),
        (2, 1, 1),
    ),
)
def test_inconsistent_counts_fail_before_inventory_staging_or_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    members: int,
    entries_on_disk: int,
    total_entries: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"counts-{members}-{entries_on_disk}-{total_entries}.zip"
    _write_bundle(bundle, members=members)
    _set_archive_entry_counts(
        bundle,
        entries_on_disk=entries_on_disk,
        total_entries=total_entries,
    )
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("entry-count policy must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("entry-count policy must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("entry-count policy must fail before inventory")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_COUNT_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert list(output.iterdir()) == []


def test_entry_count_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "count-cleanup.zip"
    _write_bundle(bundle)
    _set_archive_entry_counts(bundle, entries_on_disk=0, total_entries=0)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: IO[bytes]) -> zipfile.ZipFile:
        archive = original_zipfile(file)
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_COUNT_ERROR)}$"):
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


def test_archive_disk_error_precedes_entry_counts(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "disk-before-count.zip"
    _write_bundle(bundle)
    _set_archive_disk_fields(bundle, disk=1, central_disk=0)
    _set_archive_entry_counts(bundle, entries_on_disk=0, total_entries=0)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle uses unsupported archive disk fields$",
    ):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_entry_counts_precede_nul_name_policy(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "count-before-nul.zip"
    _write_bundle(bundle, hidden_suffix="\x00hidden")
    _set_archive_entry_counts(bundle, entries_on_disk=0, total_entries=0)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_COUNT_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_entry_count_validator_accepts_exact_counts_and_restores_position() -> None:
    module = _smoke()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("payload.txt", b"payload")
    stream.seek(3)

    module._validate_sample_archive_entry_counts(snapshot=stream, parsed_entries=1)

    assert stream.tell() == 3


@pytest.mark.parametrize("mutation", ("signature", "comment", "trailing"))
def test_entry_count_validator_normalizes_unusable_record_and_restores_position(
    mutation: str,
) -> None:
    module = _smoke()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("payload.txt", b"payload")
    data = bytearray(stream.getvalue())
    end = data.rindex(_EOCD_SIGNATURE)
    if mutation == "signature":
        data[end : end + 4] = b"BAD!"
    elif mutation == "comment":
        data[end + 20 : end + 22] = b"\x01\x00"
    else:
        data.extend(b"x")
    stream = io.BytesIO(data)
    stream.seek(3)

    with pytest.raises(
        zipfile.BadZipFile,
        match=r"^invalid final end-of-central-directory record$",
    ):
        module._validate_sample_archive_entry_counts(
            snapshot=stream,
            parsed_entries=1,
        )

    assert stream.tell() == 3


@pytest.mark.parametrize(
    ("parsed_entries", "entries_on_disk", "total_entries"),
    ((1, 0, 1), (1, 1, 0), (1, 2, 2), (2, 1, 1), (1, 0xFFFF, 0xFFFF)),
)
def test_entry_count_validator_rejects_mismatch_and_restores_position(
    tmp_path: Path,
    parsed_entries: int,
    entries_on_disk: int,
    total_entries: int,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"validator-{parsed_entries}-{entries_on_disk}-{total_entries}.zip"
    _write_bundle(bundle)
    _set_archive_entry_counts(
        bundle,
        entries_on_disk=entries_on_disk,
        total_entries=total_entries,
    )
    with bundle.open("rb") as stream:
        stream.seek(3)
        with pytest.raises(RuntimeError, match=rf"^{re.escape(_COUNT_ERROR)}$"):
            module._validate_sample_archive_entry_counts(
                snapshot=stream,
                parsed_entries=parsed_entries,
            )
        assert stream.tell() == 3


def test_current_producer_entry_counts_match_parser_inventory(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    data = bundle.read_bytes()
    end = data.rindex(_EOCD_SIGNATURE)
    with zipfile.ZipFile(bundle) as archive:
        parsed_entries = len(archive.infolist())
    assert parsed_entries == 50
    assert int.from_bytes(data[end + 8 : end + 10], "little") == parsed_entries
    assert int.from_bytes(data[end + 10 : end + 12], "little") == parsed_entries


def test_m84_source_checks_counts_after_disk_before_names() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]

    member_volume = extraction.index("_validate_sample_member_volume(volume=info.volume)")
    archive_disk = extraction.index(
        "_validate_sample_archive_disk_fields(snapshot=snapshot_stream)"
    )
    archive_counts = extraction.index(
        "_validate_sample_archive_entry_counts(\n"
        "            snapshot=snapshot_stream,\n"
        "            parsed_entries=len(infos),\n"
        "        )"
    )
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    assert member_volume < archive_disk < archive_counts < name < metadata
    helper = source[source.index("def _validate_sample_archive_entry_counts") :]
    assert "snapshot.seek(-_SAMPLE_EOCD_BYTES, os.SEEK_END)" in helper
    assert "zipfile._" not in helper


def test_m84_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m84" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m84_docs_define_entry_count_preflight_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0067-require-consistent-archive-entry-counts.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "M84" in combined
    assert "end-of-central-directory" in combined
    assert _COUNT_ERROR in combined
    assert "no ZIP64 end-record parser" in combined
    assert "no multi-volume assembler" in combined
    assert "not a general archive sandbox" in combined
    assert "not a real public release observation" in combined
