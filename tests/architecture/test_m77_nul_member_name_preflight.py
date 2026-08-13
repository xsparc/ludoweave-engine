"""Protect M77 NUL-suffixed sample-member name rejection."""

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
_NUL_ERROR = "sample bundle member name contains a NUL byte"


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

    def _validate_sample_member_name(self, *, original_name: str) -> None: ...

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
    return cast(_SmokeModule, _load(_SMOKE, "m77_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m77_release_artifacts"))


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


def _bundle_with_hidden_suffix(
    path: Path,
    names: frozenset[str],
    *,
    target_index: int = 0,
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for index, name in enumerate(sorted(names)):
            _write_member(
                archive,
                name=f"{_PREFIX}/{name}",
                payload=name.encode(),
                hidden_suffix="\x00hidden" if index == target_index else "",
            )


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


def _empty_output(tmp_path: Path, name: str = "output") -> Path:
    output = tmp_path / name
    output.mkdir()
    return output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cpython_exposes_original_nul_suffix_while_reading_payload(tmp_path: Path) -> None:
    bundle = tmp_path / "nul-suffix.zip"
    expected_name = f"{_PREFIX}/README.md"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(
            archive,
            name=expected_name,
            payload=b"payload",
            hidden_suffix="\x00hidden",
        )

    with zipfile.ZipFile(bundle) as archive:
        info = archive.infolist()[0]
        assert info.orig_filename == f"{expected_name}\x00hidden"
        assert info.filename == expected_name
        assert archive.read(info) == b"payload"


def test_nul_suffix_fails_before_inventory_staging_or_member_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "nul-suffix.zip"
    _bundle_with_hidden_suffix(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    output = _empty_output(tmp_path)

    def forbidden_open(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("NUL-suffixed names must fail before member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("NUL-suffixed names must fail before staging")

    def forbidden_inventory(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("NUL-suffixed names must fail before inventory validation")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    monkeypatch.setattr(module, "_validate_sample_inventory", forbidden_inventory)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_NUL_ERROR)}$") as caught:
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert _PREFIX not in str(caught.value)
    assert list(output.iterdir()) == []


def test_later_nul_suffix_preempts_earlier_member_metadata_error(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "ordered-errors.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        _write_member(archive, name="/unsafe-first.txt", payload=b"unsafe")
        _write_member(
            archive,
            name=f"{_PREFIX}/README.md",
            payload=b"hidden",
            hidden_suffix="\x00hidden",
        )

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_NUL_ERROR)}$"):
        module._extract_bundle(bundle, _empty_output(tmp_path), version=_VERSION)


def test_nul_name_preflight_closes_owned_archive_and_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "nul-suffix.zip"
    _bundle_with_hidden_suffix(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    output = _empty_output(tmp_path)
    original_zipfile = zipfile.ZipFile
    archives: list[zipfile.ZipFile] = []

    def recording_zipfile(file: IO[bytes]) -> zipfile.ZipFile:
        archive = original_zipfile(file)
        archives.append(archive)
        return archive

    monkeypatch.setattr(zipfile, "ZipFile", recording_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_NUL_ERROR)}$"):
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
    ),
)
def test_existing_flag_errors_precede_nul_name_policy(
    tmp_path: Path,
    flag_bits: int,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"precedence-{flag_bits}.zip"
    _bundle_with_hidden_suffix(bundle, frozenset(("README.md",)))
    _set_member_flags(bundle, member_index=0, flag_bits=flag_bits)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(
            bundle,
            _empty_output(tmp_path, f"output-{flag_bits}"),
            version=_VERSION,
        )


@pytest.mark.parametrize(
    ("flag_bits", "expected_error"),
    (
        (0x0001, "sample bundle contains an encrypted member"),
        (0x0020, "sample bundle uses compressed patched data"),
        (0x0010, "sample bundle uses enhanced deflating"),
    ),
)
def test_later_member_flag_errors_precede_earlier_nul_name_policy(
    tmp_path: Path,
    flag_bits: int,
    expected_error: str,
) -> None:
    module = _smoke()
    bundle = tmp_path / f"archive-wide-precedence-{flag_bits}.zip"
    _bundle_with_hidden_suffix(
        bundle,
        frozenset(("README.md", "pyproject.toml")),
        target_index=0,
    )
    _set_member_flags(bundle, member_index=1, flag_bits=flag_bits)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(expected_error)}$"):
        module._extract_bundle(
            bundle,
            _empty_output(tmp_path, f"archive-wide-output-{flag_bits}"),
            version=_VERSION,
        )


def test_exact_nul_validator_does_not_reject_other_name_differences() -> None:
    module = _smoke()

    module._validate_sample_member_name(original_name="README.md")
    module._validate_sample_member_name(original_name="different-normalized-name")
    with pytest.raises(RuntimeError, match=rf"^{re.escape(_NUL_ERROR)}$"):
        module._validate_sample_member_name(original_name="README.md\x00hidden")


def test_current_producer_uses_no_nul_suffixed_member_name(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"

    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        assert archive.infolist()
        assert all("\x00" not in info.orig_filename for info in archive.infolist())


def test_m77_source_preflights_exact_nul_without_general_name_comparison() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]
    validation = source[
        source.index("def _validate_sample_member_name") : source.index(
            "def _portable_sample_member_parts"
        )
    ]

    assert '"\\x00" in original_name' in validation
    assert "original_name !=" not in validation
    flag_pass = extraction.index("for info in infos:")
    processing = extraction.index("_validate_sample_member_flags(flag_bits=info.flag_bits)")
    compression = extraction.index("_validate_sample_compression_flags(")
    name_pass = extraction.index("for info in infos:", flag_pass + 1)
    name = extraction.index("_validate_sample_member_name(original_name=info.orig_filename)")
    metadata = extraction.index("total_bytes = 0")
    inventory = extraction.index("_validate_sample_inventory(observed_members)")
    staging = extraction.index("TemporaryDirectory(")
    member_read = extraction.index("archive.open(info)")
    assert (
        flag_pass
        < processing
        < compression
        < name_pass
        < name
        < metadata
        < inventory
        < staging
        < member_read
    )


def test_m77_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m77" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m77_docs_define_nul_name_preflight_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0060-reject-nul-suffixed-sample-member-names.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m77" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 76
    for term in (
        "nul byte",
        "orig_filename",
        "before member reads",
        "before staging",
        "content-silent",
        "exact nul check",
        "no general normalized-name comparison",
        "no raw parser",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
