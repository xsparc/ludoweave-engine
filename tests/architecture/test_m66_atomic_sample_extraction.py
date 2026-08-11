"""Protect M66 staged publication and failed sample-extraction cleanup."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import io
import os
import re
import sys
import zipfile
from collections.abc import Sequence
from pathlib import Path
from types import TracebackType
from typing import IO, Protocol, cast

import pytest

_ROOT = Path(__file__).parents[2]
_SMOKE = _ROOT / "scripts" / "smoke_release.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_STAGER_SHA256 = "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca"
_VERSION = "0.1.0a1"
_PREFIX = f"ludoweave-samples-{_VERSION}"
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
    def _extract_bundle(self, bundle: Path, output: Path, *, version: str) -> Path: ...


def _allow_scoped_inventory(members: set[str]) -> None:
    del members


def _load() -> _SmokeModule:
    spec = importlib.util.spec_from_file_location("m66_smoke_release", _SMOKE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts = str(_ROOT / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts)
    module.__dict__["_validate_sample_inventory"] = _allow_scoped_inventory
    return cast(_SmokeModule, module)


def _bundle(path: Path, members: Sequence[tuple[str, bytes]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in members:
            archive.writestr(f"{_PREFIX}/{name}", payload)


def _complete_bundle(path: Path) -> None:
    _bundle(path, tuple((name, name.encode()) for name in sorted(_REQUIRED)))


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def test_stream_size_failure_removes_partial_staging_tree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load()
    bundle = tmp_path / "size-changed.zip"
    _bundle(bundle, (("payload.bin", b"x"),))
    output = _empty_output(tmp_path)

    def empty_stream(self: zipfile.ZipFile, info: zipfile.ZipInfo) -> io.BytesIO:
        del self, info
        return io.BytesIO()

    monkeypatch.setattr(zipfile.ZipFile, "open", empty_stream)
    with pytest.raises(
        RuntimeError,
        match="sample bundle member size changed during extraction",
    ):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_midstream_io_failure_removes_partial_staging_tree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load()
    bundle = tmp_path / "read-failed.zip"
    _bundle(bundle, (("payload.bin", b"xy"),))
    output = _empty_output(tmp_path)

    class FailingStream:
        def __init__(self) -> None:
            self._first = True

        def __enter__(self) -> FailingStream:
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
        ) -> None:
            del exc_type, exc_value, traceback

        def read(self, size: int = -1) -> bytes:
            del size
            if self._first:
                self._first = False
                return b"x"
            raise OSError("simulated archive read failure")

    def failed_stream(self: zipfile.ZipFile, info: zipfile.ZipInfo) -> FailingStream:
        del self, info
        return FailingStream()

    monkeypatch.setattr(zipfile.ZipFile, "open", failed_stream)
    with pytest.raises(OSError, match="simulated archive read failure"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_incomplete_bundle_removes_staged_members(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "incomplete.zip"
    _bundle(bundle, (("payload.bin", b"payload"),))
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="sample bundle is incomplete"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


@pytest.mark.parametrize("kind", ("directory", "file"))
def test_existing_final_root_fails_before_archive_reads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    kind: str,
) -> None:
    module = _load()
    bundle = tmp_path / "complete.zip"
    _complete_bundle(bundle)
    output = _empty_output(tmp_path)
    root = output / _PREFIX
    if kind == "directory":
        root.mkdir()
        sentinel = root / "sentinel.txt"
        sentinel.write_text("preserve", encoding="utf-8")
    else:
        root.write_text("preserve", encoding="utf-8")

    def forbidden_open(self: zipfile.ZipFile, info: zipfile.ZipInfo) -> io.BytesIO:
        del self, info
        raise AssertionError("archive content must not be opened after a root collision")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    with pytest.raises(RuntimeError, match="sample bundle output already exists"):
        module._extract_bundle(bundle, output, version=_VERSION)

    if kind == "directory":
        assert root.is_dir()
        assert (root / "sentinel.txt").read_text(encoding="utf-8") == "preserve"
    else:
        assert root.read_text(encoding="utf-8") == "preserve"


def test_dangling_final_root_link_is_an_existing_collision(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "complete.zip"
    _complete_bundle(bundle)
    output = _empty_output(tmp_path)
    root = output / _PREFIX
    try:
        root.symlink_to(tmp_path / "missing", target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symbolic-link creation unavailable: {error}")

    assert os.path.lexists(root)
    with pytest.raises(RuntimeError, match="sample bundle output already exists"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert root.is_symlink()
    assert os.path.lexists(root)


def test_missing_output_parent_is_not_created(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "complete.zip"
    _complete_bundle(bundle)
    output = tmp_path / "missing-output"

    with pytest.raises(RuntimeError, match="sample bundle output directory is unavailable"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert not output.exists()


def test_link_like_output_parent_is_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load()
    bundle = tmp_path / "complete.zip"
    _complete_bundle(bundle)
    output = _empty_output(tmp_path)
    original_is_junction = Path.is_junction

    def simulated_junction(self: Path) -> bool:
        return self == output or original_is_junction(self)

    monkeypatch.setattr(Path, "is_junction", simulated_junction)
    with pytest.raises(RuntimeError, match="sample bundle output directory is unavailable"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_publish_failure_removes_staging_and_preserves_cause(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load()
    bundle = tmp_path / "complete.zip"
    _complete_bundle(bundle)
    output = _empty_output(tmp_path)
    root = output / _PREFIX
    original_replace = Path.replace

    def failed_replace(self: Path, target: Path) -> Path:
        if target == root:
            raise OSError("simulated publish failure")
        return original_replace(self, target)

    monkeypatch.setattr(Path, "replace", failed_replace)
    with pytest.raises(OSError, match="simulated publish failure"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert not os.path.lexists(root)
    assert list(output.iterdir()) == []


def test_late_final_root_collision_is_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load()
    bundle = tmp_path / "complete.zip"
    _complete_bundle(bundle)
    output = _empty_output(tmp_path)
    root = output / _PREFIX
    original_open = zipfile.ZipFile.open
    collision_created = False

    def colliding_open(self: zipfile.ZipFile, info: zipfile.ZipInfo) -> IO[bytes]:
        nonlocal collision_created
        if not collision_created:
            root.mkdir()
            (root / "sentinel.txt").write_text("preserve", encoding="utf-8")
            collision_created = True
        return original_open(self, info)

    monkeypatch.setattr(zipfile.ZipFile, "open", colliding_open)
    with pytest.raises(RuntimeError, match="sample bundle output already exists"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert (root / "sentinel.txt").read_text(encoding="utf-8") == "preserve"
    assert list(output.iterdir()) == [root]


def test_complete_bundle_publishes_only_final_root(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "complete.zip"
    _complete_bundle(bundle)
    output = _empty_output(tmp_path)

    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert {path.name for path in root.iterdir()} == _REQUIRED
    assert list(output.iterdir()) == [root]


def test_m66_source_stages_validates_then_renames() -> None:
    source = _SMOKE.read_text(encoding="utf-8")

    assert "os.path.lexists(root)" in source
    assert "output.is_junction()" in source
    assert "TemporaryDirectory(" in source
    assert "dir=output" in source
    assert "staged_root" in source
    assert source.index("sample bundle is incomplete") < source.index("staged_root.replace(root)")
    assert "destination = staged_root.joinpath(*parts[1:])" in source


def test_m66_changes_no_workflow_stager_runtime_dependency_or_package_boundary() -> None:
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "ci.yml").read_bytes()).hexdigest()
        == _CI_SHA256
    )
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "release.yml").read_bytes()).hexdigest()
        == _RELEASE_SHA256
    )
    assert hashlib.sha256(
        (_ROOT / "scripts" / "release_artifacts.py").read_bytes()
    ).hexdigest() == (_STAGER_SHA256)
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m66" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m66_docs_define_staged_publication_and_nonclaim_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0049-atomic-sample-extraction.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m66" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 65
    for term in (
        "same-filesystem",
        "temporary staging directory",
        "final sample root",
        "single rename",
        "incomplete",
        "partial",
        "cleanup",
        "already exists",
        "no workflow",
        "not crash-durable",
        "race isolation",
        "not a real public release observation",
    ):
        assert term in combined
