"""Protect M72 content-silent sample ZIP parser failures."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import traceback
import zipfile
from pathlib import Path
from typing import IO, Protocol, cast

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
_ZIP_ERROR = "sample bundle ZIP data is invalid"
_NAME_ERROR = "sample bundle local header names are inconsistent"


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

    def _snapshot_sample_archive(
        self,
        source: IO[bytes],
        snapshot: IO[bytes],
        *,
        expected_sha256: str | None,
    ) -> None: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m72_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m72_release_artifacts"))


def _bundle(path: Path, names: frozenset[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(names):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())


def _corrupt_first_local_name(path: Path) -> str:
    data = bytearray(path.read_bytes())
    assert data[:4] == b"PK\x03\x04"
    name_size = int.from_bytes(data[26:28], "little")
    name_start = 30
    name_end = name_start + name_size
    original = bytes(data[name_start:name_end])
    replacement = (b"private-member-detail-" + (b"x" * name_size))[:name_size]
    assert replacement != original and len(replacement) == name_size
    data[name_start:name_end] = replacement
    path.write_bytes(data)
    return replacement.decode("ascii")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def _assert_content_silent(error: RuntimeError, private_detail: str) -> None:
    assert str(error) == _ZIP_ERROR
    assert error.__suppress_context__
    context = error.__context__
    assert isinstance(context, (zipfile.BadZipFile, zipfile.LargeZipFile))
    assert private_detail in str(context)
    rendered = "".join(traceback.format_exception(error))
    assert private_detail not in rendered
    assert type(context).__name__ not in rendered


def _assert_name_preflight_is_content_silent(error: RuntimeError, private_detail: str) -> None:
    assert str(error) == _NAME_ERROR
    assert error.__context__ is None
    assert private_detail not in "".join(traceback.format_exception(error))


def test_invalid_zip_constructor_failure_is_stable_and_content_silent(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "invalid.zip"
    bundle.write_bytes(b"not a zip archive")
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP_ERROR)}$") as caught:
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    _assert_content_silent(caught.value, "File is not a zip file")
    assert list(output.iterdir()) == []


def test_local_name_preflight_precedes_member_read_and_cleans_stage(
    tmp_path: Path,
) -> None:
    module = _smoke()
    bundle = tmp_path / "local-name-mismatch.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    private_detail = _corrupt_first_local_name(bundle)
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_NAME_ERROR)}$") as caught:
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    _assert_name_preflight_is_content_silent(caught.value, private_detail)
    assert not (output / _PREFIX).exists()
    assert list(output.iterdir()) == []


def test_large_zip_failure_is_stable_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    output = _empty_output(tmp_path)
    private_detail = "private ZIP64 parser detail"

    def rejected_zipfile(*args: object, **kwargs: object) -> zipfile.ZipFile:
        del args, kwargs
        raise zipfile.LargeZipFile(private_detail)

    monkeypatch.setattr(zipfile, "ZipFile", rejected_zipfile)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP_ERROR)}$") as caught:
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    _assert_content_silent(caught.value, private_detail)
    assert list(output.iterdir()) == []


def test_parser_failure_closes_owned_source_and_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "invalid.zip"
    bundle.write_bytes(b"not a zip archive")
    output = _empty_output(tmp_path)
    observed: list[tuple[IO[bytes], IO[bytes]]] = []
    original_snapshot = module._snapshot_sample_archive

    def recording_snapshot(
        source: IO[bytes],
        snapshot: IO[bytes],
        *,
        expected_sha256: str | None,
    ) -> None:
        observed.append((source, snapshot))
        original_snapshot(source, snapshot, expected_sha256=expected_sha256)

    monkeypatch.setattr(module, "_snapshot_sample_archive", recording_snapshot)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_ZIP_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert len(observed) == 1
    source, snapshot = observed[0]
    assert source.closed
    assert snapshot.closed


def test_verifier_policy_error_remains_specific(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "wrong-inventory.zip"
    _bundle(bundle, frozenset(("README.md",)))
    output = _empty_output(tmp_path)

    with pytest.raises(
        RuntimeError,
        match=r"^sample bundle inventory is unexpected$",
    ) as caught:
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=_sha256(bundle),
        )

    assert not caught.value.__suppress_context__


def test_current_producer_remains_admitted(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)
    output = _empty_output(tmp_path)

    assert module._extract_bundle(
        bundle,
        output,
        version=_VERSION,
        expected_sha256=_sha256(bundle),
    ) == (output / _PREFIX)


def test_m72_source_normalizes_only_documented_zip_failures() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction = source[source.index("def _extract_bundle") :]

    catch_start = extraction.index("except (")
    catch = extraction[catch_start : extraction.index("):", catch_start)]
    assert "zipfile.BadZipFile" in catch
    assert "zipfile.LargeZipFile" in catch
    assert f'raise RuntimeError("{_ZIP_ERROR}") from None' in extraction
    assert extraction.index("def _extract_bundle") < extraction.index(
        "def _extract_checksum_admitted_bundle"
    )


def test_m72_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m72" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m72_docs_define_content_silent_zip_failure_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0055-content-silent-sample-zip-failures.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m72" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 71
    for term in (
        "badzipfile",
        "largezipfile",
        "archive-controlled",
        "stable error",
        "content-silent",
        "suppressed context",
        "owned cleanup",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
