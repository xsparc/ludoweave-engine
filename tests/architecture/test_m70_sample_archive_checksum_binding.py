"""Protect M70 same-descriptor sample-archive checksum binding."""

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
_CHECKSUM_ERROR = "sample bundle checksum does not match staged release"


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
    return cast(_SmokeModule, _load(_SMOKE, "m70_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m70_release_artifacts"))


def _bundle(path: Path, names: frozenset[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(names):
            archive.writestr(f"{_PREFIX}/{name}", name.encode())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def test_changed_archive_fails_before_zip_parser_or_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _smoke()
    bundle = tmp_path / "changed.zip"
    _bundle(bundle, module._EXPECTED_SAMPLE_MEMBERS)
    expected_sha256 = _sha256(bundle)
    bundle.write_bytes(bundle.read_bytes() + b"changed after release checks")
    output = _empty_output(tmp_path)

    def forbidden_zipfile(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("a checksum mismatch must fail before ZIP parsing")

    def forbidden_staging(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise AssertionError("a checksum mismatch must fail before staging")

    monkeypatch.setattr(zipfile, "ZipFile", forbidden_zipfile)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)

    with pytest.raises(RuntimeError, match=rf"^{re.escape(_CHECKSUM_ERROR)}$"):
        module._extract_bundle(
            bundle,
            output,
            version=_VERSION,
            expected_sha256=expected_sha256,
        )

    assert list(output.iterdir()) == []


def test_current_producer_is_admitted_by_its_exact_digest(tmp_path: Path) -> None:
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


def test_m70_source_binds_release_digest_before_parser_and_publication() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    main_source = source[source.index("def main") : source.index("def _extract_bundle")]
    extraction_source = source[source.index("def _extract_bundle") :]

    assert "expected_sha256=checksums[bundle.name]" in main_source
    descriptor = extraction_source.index("os.fstat(bundle_stream.fileno())")
    checksum_binding = extraction_source.index("_snapshot_sample_archive(")
    parser = extraction_source.index("zipfile.ZipFile(snapshot_stream)")
    member_read = extraction_source.index("archive.open(info)")
    publication = extraction_source.index("staged_root.replace(root)")

    assert descriptor < checksum_binding < parser < member_read < publication


def test_m70_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m70" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m70_docs_define_checksum_binding_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0053-bind-sample-archive-checksum.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m70" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 69
    for term in (
        "sha256sums",
        "same opened handle",
        "before zip parsing",
        "before publication",
        "content-silent",
        "no immutable-input guarantee",
        "no workflow",
        "sample producer",
        "not a general archive sandbox",
        "not a real public release observation",
    ):
        assert term in combined
