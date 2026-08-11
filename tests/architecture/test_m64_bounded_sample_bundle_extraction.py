"""Protect M64 bounded, streaming sample-bundle extraction."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import io
import re
import sys
import zipfile
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, cast

import pytest

_ROOT = Path(__file__).parents[2]
_SMOKE = _ROOT / "scripts" / "smoke_release.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_VERSION = "0.1.0a1"
_PREFIX = f"ludoweave-samples-{_VERSION}"
_ONE_MIB = 1024 * 1024
_REQUIRED = frozenset(
    (
        "README.md",
        "agent_tool_recovery_rate_readiness.py",
        "agent_tool_conformance.py",
        "alpha_acceptance.py",
        "benchmark_regression_rate_readiness.py",
        "clockwork_arena.py",
        "command_receipt_stability_decision.py",
        "constrained_3d_decision.py",
        "cross_version_corpus_readiness.py",
        "external_contributor_rehearsal_readiness.py",
        "external_contributor_retention_readiness.py",
        "external_consumer_feedback_readiness.py",
        "external_sample_game_adoption_readiness.py",
        "installation_matrix_readiness.py",
        "operation_argument_compatibility.py",
        "receipt_reader.py",
        "receipt_semantic_compatibility.py",
        "render_device_conformance.py",
        "replay_divergence_rate_readiness.py",
        "response_review_latency_readiness.py",
        "rollback_readiness.py",
        "supported_release_channel_readiness.py",
        "third_party_conformance_adoption_readiness.py",
        "visual_editor_decision.py",
        "wasm_mod_security_decision.py",
        "world_store_conformance.py",
    )
)


class _SmokeModule(Protocol):
    _MAX_SAMPLE_MEMBERS: int
    _MAX_SAMPLE_MEMBER_BYTES: int
    _MAX_SAMPLE_TOTAL_BYTES: int
    _SAMPLE_COPY_BYTES: int
    _SAMPLE_COMPRESSION_METHODS: frozenset[int]

    def _extract_bundle(self, bundle: Path, output: Path, *, version: str) -> Path: ...


def _load() -> _SmokeModule:
    spec = importlib.util.spec_from_file_location("m64_smoke_release", _SMOKE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts = str(_ROOT / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts)
    return cast(_SmokeModule, module)


def _bundle(
    path: Path,
    members: Sequence[tuple[str, bytes]],
    *,
    compression: int = zipfile.ZIP_DEFLATED,
) -> None:
    with zipfile.ZipFile(path, "w", compression=compression) as archive:
        for name, payload in members:
            archive.writestr(f"{_PREFIX}/{name}", payload)


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def test_m64_pins_conservative_sample_expansion_limits() -> None:
    module = _load()
    supported_compression = frozenset((zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED))

    assert module._MAX_SAMPLE_MEMBERS == 256
    assert module._MAX_SAMPLE_MEMBER_BYTES == _ONE_MIB
    assert module._MAX_SAMPLE_TOTAL_BYTES == 8 * _ONE_MIB
    assert module._SAMPLE_COPY_BYTES == 64 * 1024
    assert supported_compression == module._SAMPLE_COMPRESSION_METHODS


def test_member_count_limit_fails_before_extraction(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "too-many.zip"
    _bundle(bundle, tuple((f"file-{index}.txt", b"") for index in range(257)))
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="sample bundle has too many members"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_member_size_limit_fails_before_extraction(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "oversized-member.zip"
    _bundle(bundle, (("oversized.bin", b"x" * (_ONE_MIB + 1)),))
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="sample bundle member is too large"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_total_size_limit_fails_before_extraction(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "oversized-total.zip"
    _bundle(bundle, tuple((f"file-{index}.bin", b"x" * _ONE_MIB) for index in range(9)))
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="sample bundle expands beyond the total limit"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


@pytest.mark.parametrize("compression", (zipfile.ZIP_BZIP2, zipfile.ZIP_LZMA))
def test_unbounded_read_codecs_fail_before_extraction(
    tmp_path: Path,
    compression: int,
) -> None:
    module = _load()
    bundle = tmp_path / "unsupported-codec.zip"
    _bundle(bundle, (("payload.bin", b"x"),), compression=compression)
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="unsupported compression method"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_stored_members_remain_admitted(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "stored.zip"
    _bundle(
        bundle,
        tuple((name, b"") for name in sorted(_REQUIRED)),
        compression=zipfile.ZIP_STORED,
    )
    output = _empty_output(tmp_path)

    assert module._extract_bundle(bundle, output, version=_VERSION) == (output / _PREFIX)


def test_valid_boundary_member_streams_without_zipfile_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load()
    bundle = tmp_path / "valid.zip"
    members = [(name, b"") for name in sorted(_REQUIRED)]
    members.append(("boundary.bin", b"x" * _ONE_MIB))
    _bundle(bundle, members)
    output = _empty_output(tmp_path)

    def forbidden_read(self: zipfile.ZipFile, name: object, pwd: bytes | None = None) -> bytes:
        del self, name, pwd
        raise AssertionError("whole-member ZipFile.read must not be used")

    monkeypatch.setattr(zipfile.ZipFile, "read", forbidden_read)
    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert (root / "boundary.bin").stat().st_size == _ONE_MIB


@pytest.mark.parametrize("streamed", (b"", b"xy"))
def test_streamed_size_must_match_preflight_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    streamed: bytes,
) -> None:
    module = _load()
    bundle = tmp_path / "size-changed.zip"
    _bundle(bundle, (("payload.bin", b"x"),))
    output = _empty_output(tmp_path)

    def mismatched_open(
        self: zipfile.ZipFile,
        info: zipfile.ZipInfo,
    ) -> io.BytesIO:
        del self, info
        return io.BytesIO(streamed)

    monkeypatch.setattr(zipfile.ZipFile, "open", mismatched_open)
    with pytest.raises(
        RuntimeError,
        match="sample bundle member size changed during extraction",
    ):
        module._extract_bundle(bundle, output, version=_VERSION)


def test_m64_source_preflights_then_streams_archive_members() -> None:
    source = _SMOKE.read_text(encoding="utf-8")

    assert "infos = tuple(archive.infolist())" in source
    assert source.index("infos = tuple(archive.infolist())") < source.index(
        "destination.parent.mkdir"
    )
    assert source.index("info.compress_type not in _SAMPLE_COMPRESSION_METHODS") < (
        source.index("destination.parent.mkdir")
    )
    assert "archive.open(info)" in source
    assert "source.read(_SAMPLE_COPY_BYTES)" in source
    assert "archive.read(info)" not in source


def test_m64_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "ci.yml").read_bytes()).hexdigest()
        == _CI_SHA256
    )
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "release.yml").read_bytes()).hexdigest()
        == _RELEASE_SHA256
    )
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m64" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m64_docs_define_bounded_streaming_extraction_and_nonclaim_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0047-bounded-sample-bundle-extraction.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m64" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 63
    for term in (
        "256 members",
        "1 mib",
        "8 mib",
        "64 kib",
        "stored and deflated",
        "bzip2",
        "lzma",
        "before extraction",
        "stream",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
