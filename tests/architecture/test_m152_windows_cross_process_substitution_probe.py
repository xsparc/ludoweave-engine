"""Protect M152's test-only cross-process substitution boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0134-probe-windows-retained-parent-substitution.md": (
        "68269b9e3fe48750248954ddeb17aecc35f50ff5d8abf8b69e8d08c4f575a5cb"
    ),
    "docs/security/cache-cleanup-windows-retained-parent-substitution-probe.md": (
        "9045dca9969120376651e941a946a224ba062783652fc99a5e2d1f245124d21f"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m151_windows_retained_parent_substitution_probe.py": (
        "9e1102c85516a5386c837934cf2ef42ecc122d4eba41e366460e0ab6ba61f4d9"
    ),
    "tests/integration/test_windows_cache_cleanup_retained_parent_probe.py": (
        "6698b0382f1cf71d4c29e74a2e84bbd1e695f41b896e0be0feb9d10924e18b46"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "scripts": "a21166a0d275e9583c39d280c8ca77c016da2048e510970c2601f5250ddefdbf",
    "src/ludoweave": "7aca7145f0f8184c23539f2fa1aa2d000939991873f0ecd660aa6cb8e56cad43",
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


def test_m152_changes_no_runtime_script_dependency_ci_or_m151_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m152_process_boundary_is_test_only_and_not_installed() -> None:
    probe_path = _ROOT / "tests/integration/test_windows_cache_cleanup_cross_process_probe.py"
    probe = probe_path.read_text(encoding="utf-8")
    assert "import subprocess" in probe
    assert 'sys.platform != "win32"' in probe
    assert "pytest-owned" in probe

    metadata = (_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'packages = ["src/ludoweave"]' in metadata
    assert "test_windows_cache_cleanup_cross_process_probe" not in metadata


def test_m152_probe_exercises_fixed_non_inheriting_child_substitution() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_cross_process_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "_filesystem_information",
        "FILE_SUPPORTS_REPARSE_POINTS",
        '"ren live displaced && mklink /j live target"',
        "close_fds=True",
        "cwd=working_directory",
        "shell=False",
        "timeout=15.0",
        "retained_parent_identity",
        'probe.open_directory(root, "live")',
        "_UnsafeComponent",
        "through_retained_parent",
        "through_displaced_name",
        "through_target",
        "probe.owned_count == 7",
        "probe.owned_count == 0",
        "os.path.isjunction(junction_path)",
        "os.rmdir(junction_path)",
    ):
        assert required in probe
    assert "time.sleep" not in probe


def test_m152_documents_narrow_cross_process_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-cross-process-substitution-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "cross-process",
        "non-inherited",
        "not claim simultaneous execution",
        "missing admission evidence",
        "no hosted check is added",
    ):
        assert required in compact


def test_m152_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0135-probe-windows-cross-process-substitution.md").read_text(
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
        assert "cache-cleanup-windows-cross-process-substitution-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0135-probe-windows-cross-process-substitution.md" in rfc_index
