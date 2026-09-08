"""Protect M156's test-only abrupt blocker-owner termination boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "23f4cf86fdf46be2f56b38345f09bac61c7753ad15f05302874afb99d4a20394",
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
        "af55c36ef2c1c8ab2edd8d16a42aa65cbc3c09bbcbe6a480fbcfd3645d802801"
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
    "examples": "8e8d3a618b8bb14c439d4c0809db345fe471dc7c07f1765b03c4bb507f8fc98a",
    "scripts": "8833e1120f60e74f4b5024ef6a6049821a72afef44c0143bab3f7bbd9298e247",
    "src/ludoweave": "1e7f21b3d5bb0a8021f47f9bf1089873a59cb3e798b02933569d3eee3c9a35c1",
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
