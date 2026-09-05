"""Protect M152's test-only cross-process substitution boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0134-probe-windows-retained-parent-substitution.md": (
        "68269b9e3fe48750248954ddeb17aecc35f50ff5d8abf8b69e8d08c4f575a5cb"
    ),
    "docs/security/cache-cleanup-windows-retained-parent-substitution-probe.md": (
        "9045dca9969120376651e941a946a224ba062783652fc99a5e2d1f245124d21f"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m151_windows_retained_parent_substitution_probe.py": (
        "4f5cffc1e866fe2fcbfb2bbe53195eaa6fcc739279507d49b97c143369d7d8f6"
    ),
    "tests/integration/test_windows_cache_cleanup_retained_parent_probe.py": (
        "6698b0382f1cf71d4c29e74a2e84bbd1e695f41b896e0be0feb9d10924e18b46"
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
