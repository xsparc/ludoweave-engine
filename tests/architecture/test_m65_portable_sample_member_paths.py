"""Protect M65 portable, collision-free sample-bundle member paths."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import importlib.util
import re
import stat
import sys
import warnings
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
    _MAX_SAMPLE_PATH_CHARS: int

    def _extract_bundle(self, bundle: Path, output: Path, *, version: str) -> Path: ...

    def _portable_sample_member_parts(
        self,
        info: zipfile.ZipInfo,
        *,
        expected_root: str,
    ) -> tuple[str, ...]: ...


def _allow_scoped_inventory(members: set[str]) -> None:
    del members


def _load() -> _SmokeModule:
    spec = importlib.util.spec_from_file_location("m65_smoke_release", _SMOKE)
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


def _empty_output(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    return output


@pytest.mark.parametrize(
    "name",
    (
        "nested/CON.txt",
        "nested/com9.json",
        "nested/release.",
        "nested/naive-\N{LATIN SMALL LETTER I WITH DIAERESIS}.txt",
        "nested//file.txt",
        "nested/./file.txt",
        "a" * 256,
        f"{'a' * 130}/{'b' * 130}",
    ),
)
def test_nonportable_member_path_fails_before_extraction(
    tmp_path: Path,
    name: str,
) -> None:
    module = _load()
    bundle = tmp_path / "nonportable.zip"
    _bundle(bundle, ((name, b"x"),))
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="non-portable member path"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


@pytest.mark.parametrize(
    "names",
    (
        ("README.md", "README.md"),
        ("assets/value.json", "ASSETS/VALUE.JSON"),
        ("Assets/one.json", "assets/two.json"),
    ),
)
def test_duplicate_or_case_ambiguous_paths_fail_before_extraction(
    tmp_path: Path,
    names: tuple[str, str],
) -> None:
    module = _load()
    bundle = tmp_path / "collision.zip"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        _bundle(bundle, tuple((name, b"x") for name in names))
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="member paths collide"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


@pytest.mark.parametrize(
    "names",
    (
        ("assets", "assets/value.json"),
        ("ASSETS/value.json", "assets"),
    ),
)
def test_file_directory_prefix_collision_fails_before_extraction(
    tmp_path: Path,
    names: tuple[str, str],
) -> None:
    module = _load()
    bundle = tmp_path / "prefix-collision.zip"
    _bundle(bundle, tuple((name, b"x") for name in names))
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="member paths collide"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_explicit_directory_member_fails_before_extraction(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "directory-entry.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f"{_PREFIX}/assets/", b"")
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="non-portable member path"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


@pytest.mark.parametrize(
    "file_type",
    (
        stat.S_IFIFO,
        stat.S_IFCHR,
        stat.S_IFBLK,
        stat.S_IFSOCK,
    ),
)
def test_nonregular_member_mode_fails_before_extraction(
    tmp_path: Path,
    file_type: int,
) -> None:
    module = _load()
    bundle = tmp_path / "nonregular-entry.zip"
    info = zipfile.ZipInfo(f"{_PREFIX}/payload.bin")
    info.external_attr = (file_type | 0o644) << 16
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr(info, b"payload")
    output = _empty_output(tmp_path)

    with pytest.raises(RuntimeError, match="non-regular member"):
        module._extract_bundle(bundle, output, version=_VERSION)

    assert list(output.iterdir()) == []


def test_existing_portable_nested_sample_shape_remains_valid(tmp_path: Path) -> None:
    module = _load()
    bundle = tmp_path / "portable.zip"
    members = [(name, b"") for name in sorted(_REQUIRED)]
    members.extend(
        (
            ("assets/receipt_v1/valid.json", b"{}"),
            ("assets/receipt_v1/valid.bin", b"payload"),
        )
    )
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in members:
            if name == "assets/receipt_v1/valid.bin":
                info = zipfile.ZipInfo(f"{_PREFIX}/{name}")
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED)
            else:
                archive.writestr(f"{_PREFIX}/{name}", payload)
    output = _empty_output(tmp_path)

    root = module._extract_bundle(bundle, output, version=_VERSION)

    assert root == output / _PREFIX
    assert (root / "assets" / "receipt_v1" / "valid.json").read_bytes() == b"{}"
    assert (root / "assets" / "receipt_v1" / "valid.bin").read_bytes() == b"payload"


def test_exact_255_ascii_character_relative_path_is_admitted() -> None:
    module = _load()
    name = "a" * 255
    info = zipfile.ZipInfo(f"{_PREFIX}/{name}")

    assert module._portable_sample_member_parts(info, expected_root=_PREFIX) == (name,)


def test_m65_source_preflights_portable_identity_before_writes() -> None:
    module = _load()
    source = _SMOKE.read_text(encoding="utf-8")

    assert module._MAX_SAMPLE_PATH_CHARS == 255
    assert "_portable_sample_member_parts" in source
    assert "casefold()" in source
    assert "member paths collide" in source
    assert source.index("_portable_sample_member_parts") < source.index("destination.parent.mkdir")


def test_m65_changes_no_workflow_stager_runtime_dependency_or_package_boundary() -> None:
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
        "m65" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m65_docs_define_portable_member_identity_and_nonclaim_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0048-portable-sample-member-paths.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m65" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 64
    for term in (
        "portable sample member path",
        "255 ascii",
        "windows device",
        "case-insensitive",
        "prefix collision",
        "non-regular",
        "before extraction",
        "no unicode normalization",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
