"""Protect M150's test-only Windows junction-refusal boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0132-probe-windows-cache-cleanup-capability.md": (
        "6b7297550d04747815706808b0050b801e114aac20397bf680fabb40ccafabdd"
    ),
    "docs/security/cache-cleanup-windows-capability-probe.md": (
        "80fdea9295c1105957a911d59b92adc0b428af9f01b3e63080a736715d78d9ec"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m149_windows_cache_cleanup_capability_probe.py": (
        "bd98a8a07b3aa07847283b7fb3da2cbd1eedbe6c1351acd62bf9ee0fdb8ad99a"
    ),
    "tests/integration/test_windows_cache_cleanup_capability_probe.py": (
        "151c2e0a102c622fdb66d4d78ee803564b26081a0da34b76341e86596e11d973"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "scripts": "a71ced2308ffe412518ab7e35867185fdf260fe0f92d567c166964bfb0fb6787",
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


def test_m150_changes_no_runtime_script_dependency_ci_or_m149_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m150_native_boundary_is_test_only_and_not_installed() -> None:
    probe_path = _ROOT / "tests/integration/test_windows_cache_cleanup_junction_probe.py"
    probe = probe_path.read_text(encoding="utf-8")
    assert "import ctypes" in probe
    assert 'sys.platform != "win32"' in probe
    assert "pytest-owned" in probe

    metadata = (_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'packages = ["src/ludoweave"]' in metadata
    for source in (_ROOT / "src/ludoweave").rglob("*.py"):
        content = source.read_text(encoding="utf-8")
        assert "import ctypes" not in content
        assert "from ctypes" not in content


def test_m150_probe_exercises_junction_refusal_and_bounded_cleanup() -> None:
    probe = (_ROOT / "tests/integration/test_windows_cache_cleanup_junction_probe.py").read_text(
        encoding="utf-8"
    )
    for required in (
        "GetVolumeInformationByHandleW",
        "FILE_SUPPORTS_REPARSE_POINTS",
        '"mklink", "/j"',
        "os.path.isjunction",
        "_UnsafeComponent",
        "os.path.lexists",
        "os.rmdir",
        "marker_path.read_bytes",
    ):
        assert required in probe


def test_m150_documents_incomplete_current_host_evidence() -> None:
    decision = (_ROOT / "docs/security/cache-cleanup-windows-junction-probe.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "directory junction",
        "getvolumeinformationbyhandlew",
        "ntfs",
        "missing admission evidence",
        "no hosted check is added",
    ):
        assert required in compact


def test_m150_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0133-probe-windows-junction-refusal.md").read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "windows is not admitted" in " ".join(rfc.casefold().split())
    for path in (
        "docs/readme-history.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        content = (_ROOT / path).read_text(encoding="utf-8")
        assert "cache-cleanup-windows-junction-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0133-probe-windows-junction-refusal.md" in rfc_index
