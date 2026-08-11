"""Protect M67 exact sample-bundle member inventory conformance."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import tempfile
import zipfile
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, cast

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
_EXPECTED = frozenset(
    (
        "README.md",
        "agent_tool_conformance.py",
        "agent_tool_recovery_rate_readiness.py",
        "agent_world_builder.py",
        "alpha_acceptance.py",
        "assets/agent_tool_recovery_rate.json",
        "assets/benchmark_regression_rate.json",
        "assets/clockwork_arena.scene.json",
        "assets/cross_version_receipt_corpus.json",
        "assets/external_contributor_rehearsal.json",
        "assets/external_contributor_retention.json",
        "assets/external_consumer_feedback.json",
        "assets/external_sample_game_adoption.json",
        "assets/installation_matrix.json",
        "assets/receipt_v1/committed.json",
        "assets/receipt_v1/dry_run.json",
        "assets/receipt_v1/manifest.json",
        "assets/receipt_v1/rejected.json",
        "assets/replay_divergence_rate.json",
        "assets/response_review_latency.json",
        "assets/supported_release_channel.json",
        "assets/third_party_conformance_adoption.json",
        "benchmark_regression_rate_readiness.py",
        "clockwork_arena.assets.json",
        "clockwork_arena.py",
        "command_receipt_stability_decision.py",
        "constrained_3d_decision.py",
        "cross_version_corpus_readiness.py",
        "example.plugin.json",
        "external_contributor_rehearsal_readiness.py",
        "external_contributor_retention_readiness.py",
        "external_consumer_feedback_readiness.py",
        "external_sample_game_adoption_readiness.py",
        "fixed_step_world.py",
        "hello_headless.py",
        "hello_sprite.py",
        "installation_matrix_readiness.py",
        "operation_argument_compatibility.py",
        "receipt_reader.py",
        "receipt_semantic_compatibility.py",
        "render_device_conformance.py",
        "replay_divergence_rate_readiness.py",
        "response_review_latency_readiness.py",
        "rich_2d_showcase.py",
        "rollback_readiness.py",
        "supported_release_channel_readiness.py",
        "third_party_conformance_adoption_readiness.py",
        "visual_editor_decision.py",
        "wasm_mod_security_decision.py",
        "world_store_conformance.py",
    )
)


class _SmokeModule(Protocol):
    _EXPECTED_SAMPLE_MEMBERS: frozenset[str]

    def _extract_bundle(self, bundle: Path, output: Path, *, version: str) -> Path: ...


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
    return cast(_SmokeModule, _load(_SMOKE, "m67_smoke_release"))


def _stager() -> _StagerModule:
    return cast(_StagerModule, _load(_STAGER, "m67_release_artifacts"))


def _bundle(path: Path, names: Sequence[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.writestr(f"{_PREFIX}/{name}", name.encode())


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


def test_m67_pins_exact_project_sample_inventory() -> None:
    module = _smoke()

    assert len(_EXPECTED) == 50
    assert module._EXPECTED_SAMPLE_MEMBERS == _EXPECTED


def test_sample_producer_emits_the_independently_expected_inventory(tmp_path: Path) -> None:
    bundle = tmp_path / "samples.zip"
    _stager()._write_sample_bundle(_ROOT, bundle, _VERSION)

    with zipfile.ZipFile(bundle) as archive:
        observed = {info.filename.removeprefix(f"{_PREFIX}/") for info in archive.infolist()}

    assert observed == _EXPECTED


@pytest.mark.parametrize(
    ("name", "members"),
    (
        (
            "unexpected-private-key.txt",
            tuple(sorted((*_EXPECTED, "unexpected-private-key.txt"))),
        ),
        (
            "assets/receipt_v1/manifest.json",
            tuple(sorted(_EXPECTED - {"assets/receipt_v1/manifest.json"})),
        ),
        (
            "unexpected-private-key.txt",
            tuple(
                sorted(
                    (
                        *(_EXPECTED - {"assets/receipt_v1/manifest.json"}),
                        "unexpected-private-key.txt",
                    )
                )
            ),
        ),
    ),
)
def test_inventory_mismatch_fails_content_silently_before_member_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    members: Sequence[str],
) -> None:
    module = _smoke()
    bundle = tmp_path / "unexpected-inventory.zip"
    _bundle(bundle, members)
    output = _empty_output(tmp_path)

    def forbidden_open(self: zipfile.ZipFile, member: object, *args: object) -> object:
        del self, member, args
        raise AssertionError("inventory mismatch must fail before archive member reads")

    def forbidden_staging(*args: object, **kwargs: object) -> object:
        del args, kwargs
        raise AssertionError("inventory mismatch must fail before staging")

    monkeypatch.setattr(zipfile.ZipFile, "open", forbidden_open)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden_staging)
    with pytest.raises(RuntimeError, match=r"^sample bundle inventory is unexpected$") as caught:
        module._extract_bundle(bundle, output, version=_VERSION)

    assert name not in str(caught.value)
    assert list(output.iterdir()) == []


def test_exact_inventory_extracts_independent_of_archive_order(tmp_path: Path) -> None:
    module = _smoke()
    bundle = tmp_path / "complete.zip"
    _bundle(bundle, tuple(reversed(sorted(_EXPECTED))))
    output = _empty_output(tmp_path)

    root = module._extract_bundle(bundle, output, version=_VERSION)
    observed = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}

    assert root == output / _PREFIX
    assert observed == _EXPECTED
    assert list(output.iterdir()) == [root]


def test_m67_source_checks_exact_inventory_before_staging_or_member_read() -> None:
    source = _SMOKE.read_text(encoding="utf-8")
    extraction_source = source[source.index("def _extract_bundle") :]

    assert "_EXPECTED_SAMPLE_MEMBERS" in source
    assert "observed_members" in source
    assert "sample bundle inventory is unexpected" in source
    inventory_check = extraction_source.index("_validate_sample_inventory(observed_members)")
    assert inventory_check < extraction_source.index("TemporaryDirectory(")
    assert inventory_check < extraction_source.index("archive.open(info)")


def test_m67_changes_no_workflow_producer_runtime_dependency_or_package_boundary() -> None:
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
        "m67" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m67_docs_define_exact_inventory_and_nonclaim_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0050-exact-sample-bundle-inventory.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m67" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 66
    for term in (
        "exact sample-bundle inventory",
        "50 regular files",
        "unexpected member",
        "missing member",
        "before extraction",
        "source-defined",
        "content-silent",
        "no workflow",
        "sample producer",
        "not a real public release observation",
    ):
        assert term in combined
