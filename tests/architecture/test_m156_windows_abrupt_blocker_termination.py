"""Protect M156's test-only abrupt blocker-owner termination boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0138-probe-windows-child-owned-share-delete-handshake.md": (
        "e8f56099f2e7170dfe1f175487fa9c03dffc5ed2eb708eac4bd59522934520e0"
    ),
    "docs/security/cache-cleanup-windows-child-owned-share-delete-handshake.md": (
        "7a9bb84ec59c43d654e83aa9f82f9e6d730485061d09abac33cab56375989382"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m155_windows_child_owned_share_delete_handshake.py": (
        "d32b82337c9c1c16a267104f947a4af5c01269fb139df79f61ade9e0255adcf4"
    ),
    "tests/fixtures/windows_share_delete_blocker_child.py": (
        "be8da81a030f5de9490410e23d67147d777368f4b66e10cc580103add41b8f5d"
    ),
    "tests/integration/test_windows_cache_cleanup_child_owned_blocker_probe.py": (
        "c5feb520a1a6b95f8f819e743f82327f9bd59d42c93b4e5189660d418def75f7"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "f1774c37b8002dcd420b6aafe885c8289e2be44300e3d03f88cbcb03a43bc7a0",
    "scripts": "a21166a0d275e9583c39d280c8ca77c016da2048e510970c2601f5250ddefdbf",
    "src/ludoweave": "e6c951393b86b0673a25e0f6b1f4cf41224d3cb7807dd85c76aad482820cde36",
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


def test_m156_changes_no_runtime_example_script_dependency_ci_or_m155_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m156_probe_forces_one_bounded_owner_termination_transition() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_abrupt_blocker_termination_probe.py"
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
        'assert _read_ready(blocker) == "ready"',
        "blocker.kill()",
        "blocker.wait(timeout=_TIMEOUT_SECONDS)",
        "return_code != 0",
        'stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "_ERROR_SHARING_VIOLATION",
        "succeeded=False",
        "succeeded=True",
    ):
        assert required in probe
    assert probe.count("_attempt_native_child_rename(tmp_path)") == 2
    assert "_release_and_read_closed" not in probe
    assert "_RELEASE_TOKEN" not in probe
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m156_documents_narrow_abrupt_termination_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-abrupt-blocker-termination-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "abrupt blocker-owner termination",
        "no closed acknowledgement",
        "not crash recovery",
        "no hosted check is added",
    ):
        assert required in compact


def test_m156_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0139-probe-windows-abrupt-blocker-termination.md").read_text(
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
        assert "cache-cleanup-windows-abrupt-blocker-termination-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0139-probe-windows-abrupt-blocker-termination.md" in rfc_index
