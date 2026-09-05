"""Protect M151's test-only retained-parent substitution boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0133-probe-windows-junction-refusal.md": (
        "c8c560d5148d6ade095d39d7e9ced06c60330de9e43f7b7c2b0c6df18d94505d"
    ),
    "docs/security/cache-cleanup-windows-junction-probe.md": (
        "5f55e5243466a474c3a43c951dbbf6a725b9f2e04176d7b35a2c895efaf0ace2"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m150_windows_junction_refusal_probe.py": (
        "528443ddf6151b7c8beb0524f114252199bbb1cc41c47c108c3dba5b33cc9275"
    ),
    "tests/integration/test_windows_cache_cleanup_junction_probe.py": (
        "78d08aa892efa5e8c251615a65fc071adb1452661e944e8b19d4b6b667c5f8e9"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for candidate in sorted(path.rglob("*")):
        if (
            candidate.is_file()
            and "__pycache__" not in candidate.parts
            and candidate.suffix != ".pyc"
        ):
            digest.update(candidate.relative_to(path).as_posix().encode())
            digest.update(b"\0")
            digest.update(candidate.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def test_m151_changes_no_runtime_script_dependency_ci_or_m150_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m151_native_boundary_is_test_only_and_not_installed() -> None:
    probe_path = _ROOT / "tests/integration/test_windows_cache_cleanup_retained_parent_probe.py"
    probe = probe_path.read_text(encoding="utf-8")
    assert "import subprocess" in probe
    assert 'sys.platform != "win32"' in probe
    assert "pytest-owned" in probe

    metadata = (_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'packages = ["src/ludoweave"]' in metadata
    for source in (_ROOT / "src/ludoweave").rglob("*.py"):
        content = source.read_text(encoding="utf-8")
        assert "import ctypes" not in content
        assert "from ctypes" not in content


def test_m151_probe_exercises_retained_parent_substitution_safety() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_retained_parent_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "_filesystem_information",
        "FILE_SUPPORTS_REPARSE_POINTS",
        "os.rename(live_path, displaced_path)",
        '["cmd.exe", "/d", "/c", "mklink", "/j", "live", "target"]',
        "retained_parent_identity",
        'probe.open_directory(root, "live")',
        "_UnsafeComponent",
        "through_retained_parent",
        "through_displaced_name",
        "through_target",
        "probe.owned_count == 7",
        "probe.owned_count == 0",
        "os.rmdir(junction_path)",
    ):
        assert required in probe


def test_m151_documents_narrow_current_host_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-retained-parent-substitution-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "retained parent",
        "namespace substitution",
        "same-process",
        "missing admission evidence",
        "no hosted check is added",
    ):
        assert required in compact


def test_m151_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0134-probe-windows-retained-parent-substitution.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "windows is not admitted" in " ".join(rfc.casefold().split())
    for path in (
        "README.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        content = (_ROOT / path).read_text(encoding="utf-8")
        assert "cache-cleanup-windows-retained-parent-substitution-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0134-probe-windows-retained-parent-substitution.md" in rfc_index
