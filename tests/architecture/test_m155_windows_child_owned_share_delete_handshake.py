"""Protect M155's test-only child-owned share-delete handshake boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0137-probe-windows-native-sharing-violation.md": (
        "bedf07936a75cc8fecb986ad4e451726b569e646677fd2bfd7ca12cd49e9cb46"
    ),
    "docs/security/cache-cleanup-windows-native-sharing-violation-probe.md": (
        "af9700312b13a12cdb24ab848fa986cb8f6fa25750257a91f406e3bf10af2122"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m154_windows_native_sharing_violation_probe.py": (
        "2c49c40ad145b1e2d5d1afa15aea12522017c89f3ddc757aee11a16840b9fbfa"
    ),
    "tests/fixtures/windows_share_delete_rename_child.py": (
        "aeee1be252fd3255e3769e6b75ba70d96ffebaa1cec8ef9aefb500b92160a057"
    ),
    "tests/integration/test_windows_cache_cleanup_native_error_probe.py": (
        "8fd0b1ad78900f5fdd42dc7b4fd92c3bf0595b0c172336a79905b3aac424d55e"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
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


def test_m155_changes_no_runtime_example_script_dependency_ci_or_m154_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m155_blocker_child_is_fixed_owned_bounded_and_not_installed() -> None:
    child_path = _ROOT / "tests/fixtures/windows_share_delete_blocker_child.py"
    child = child_path.read_text(encoding="utf-8")
    for required in (
        '"CreateFileW"',
        '"CloseHandle"',
        '"live"',
        "_FILE_LIST_DIRECTORY | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE",
        "sys.stdin.buffer.read(1)",
        '_emit("ready")',
        '_emit("closed")',
        "finally:",
        '"ludoweave.test.windows-share-delete-blocker/1"',
    ):
        assert required in child
    for forbidden in (
        "_FILE_SHARE_DELETE",
        "sys.argv",
        "input(",
        "os.environ",
        "subprocess",
        "eval(",
        "exec(",
        "time.sleep",
    ):
        assert forbidden not in child

    metadata = (_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'packages = ["src/ludoweave"]' in metadata
    assert "windows_share_delete_blocker_child" not in metadata


def test_m155_probe_exercises_explicit_child_owned_release_transition() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_child_owned_blocker_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "_filesystem_information",
        "_ShareDeleteProbe",
        'filesystem_name.casefold() != "ntfs"',
        "filesystem_probe.owned_count == 0",
        '(sys.executable, "-I", "-B", str(_CHILD))',
        "close_fds=True",
        "cwd=tmp_path",
        "shell=False",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "queue.Queue",
        "threading.Thread",
        "timeout=_TIMEOUT_SECONDS",
        "process.kill()",
        "process.wait(timeout=_TIMEOUT_SECONDS)",
        "stdin.write(_RELEASE_TOKEN)",
        'assert _read_ready(blocker) == "ready"',
        'assert _release_and_read_closed(blocker) == "closed"',
        "_ERROR_SHARING_VIOLATION",
        "succeeded=False",
        "succeeded=True",
    ):
        assert required in probe
    assert probe.count("_attempt_native_child_rename(tmp_path)") == 2
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m155_documents_narrow_child_owned_handshake_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-child-owned-share-delete-handshake.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "child-owned blocker",
        "fixed one-byte release token",
        "not a concurrent race",
        "metadata-only prototype",
        "no hosted check is added",
    ):
        assert required in compact


def test_m155_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0138-probe-windows-child-owned-share-delete-handshake.md").read_text(
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
        assert "cache-cleanup-windows-child-owned-share-delete-handshake" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0138-probe-windows-child-owned-share-delete-handshake.md" in rfc_index
