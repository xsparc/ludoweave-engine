"""Protect M153's test-only share-delete exclusion boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0135-probe-windows-cross-process-substitution.md": (
        "8bc4211201de0f7e5195bd95c9f01a204285bb63f1a3e06594a8715a28980651"
    ),
    "docs/security/cache-cleanup-windows-cross-process-substitution-probe.md": (
        "506c67d5036a87f10a2b425e33e896a408916d65597ecc2dc9dd49996961429b"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m152_windows_cross_process_substitution_probe.py": (
        "4221fa9c55552fb5e77544bd08231b3856080713f853d68f4056fb4e3c2bcf67"
    ),
    "tests/integration/test_windows_cache_cleanup_cross_process_probe.py": (
        "b0e98fe721fea539fdbf7a6f7567396ad04bdb3528d870a5f242a9b9b480d80e"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "f1774c37b8002dcd420b6aafe885c8289e2be44300e3d03f88cbcb03a43bc7a0",
    "scripts": "a21166a0d275e9583c39d280c8ca77c016da2048e510970c2601f5250ddefdbf",
    "src/ludoweave": "7aca7145f0f8184c23539f2fa1aa2d000939991873f0ecd660aa6cb8e56cad43",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for candidate in sorted(
        path.rglob("*"),
        key=lambda item: (tuple(part.casefold() for part in item.parts), item.parts),
    ):
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


def test_m153_changes_no_runtime_example_script_dependency_ci_or_m152_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m153_share_delete_boundary_is_test_only_and_not_installed() -> None:
    probe_path = _ROOT / "tests/integration/test_windows_cache_cleanup_share_delete_probe.py"
    probe = probe_path.read_text(encoding="utf-8")
    assert "import subprocess" in probe
    assert 'sys.platform != "win32"' in probe
    assert "pytest-owned" in probe

    metadata = (_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'packages = ["src/ludoweave"]' in metadata
    assert "test_windows_cache_cleanup_share_delete_probe" not in metadata
    for source in (_ROOT / "src/ludoweave").rglob("*.py"):
        content = source.read_text(encoding="utf-8")
        assert "import ctypes" not in content
        assert "from ctypes" not in content


def test_m153_probe_exercises_fixed_non_inheriting_share_delete_transition() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_share_delete_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "_filesystem_information",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE",
        '"ren live displaced"',
        "close_fds=True",
        "cwd=working_directory",
        "shell=False",
        "timeout=15.0",
        "blocked_return_code != 0",
        "not os.path.lexists(displaced_path)",
        "probe.release(blocker)",
        "probe.owned_count == 2",
        "probe.owned_count == 1",
        "_attempt_child_rename(tmp_path) == 0",
        "probe.owned_count == 0",
    ):
        assert required in probe
    assert probe.count("_attempt_child_rename(tmp_path)") == 2
    assert "time.sleep" not in probe


def test_m153_documents_narrow_share_delete_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-share-delete-exclusion-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "cross-process",
        "same child command",
        "not general cross-process exclusion",
        "missing admission evidence",
        "no hosted check is added",
    ):
        assert required in compact


def test_m153_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0136-probe-windows-share-delete-exclusion.md").read_text(
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
        assert "cache-cleanup-windows-share-delete-exclusion-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0136-probe-windows-share-delete-exclusion.md" in rfc_index
