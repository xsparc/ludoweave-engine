"""Protect M151's test-only retained-parent substitution boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0133-probe-windows-junction-refusal.md": (
        "c8c560d5148d6ade095d39d7e9ced06c60330de9e43f7b7c2b0c6df18d94505d"
    ),
    "docs/security/cache-cleanup-windows-junction-probe.md": (
        "5f55e5243466a474c3a43c951dbbf6a725b9f2e04176d7b35a2c895efaf0ace2"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m150_windows_junction_refusal_probe.py": (
        "3355b13dc892eeca5a2e43fde04cbb68e4aca2783e436541b42034637a7d58bc"
    ),
    "tests/integration/test_windows_cache_cleanup_junction_probe.py": (
        "78d08aa892efa5e8c251615a65fc071adb1452661e944e8b19d4b6b667c5f8e9"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "scripts": "a21166a0d275e9583c39d280c8ca77c016da2048e510970c2601f5250ddefdbf",
    "src/ludoweave": "e6c951393b86b0673a25e0f6b1f4cf41224d3cb7807dd85c76aad482820cde36",
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
