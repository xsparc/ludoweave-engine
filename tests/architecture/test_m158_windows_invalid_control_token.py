"""Protect M158's test-only Windows invalid-control-token boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "67fc471f84d7dde8b239bd9e92235a34f780cc3d3370b0dbf451e6a922a027f1",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0140-probe-windows-control-pipe-eof.md": (
        "a6c68a90d1b0fefb28dbed14bb45a8f553c6d8ba3118db1df0713d54aeaebc8a"
    ),
    "docs/security/cache-cleanup-windows-control-pipe-eof-probe.md": (
        "6f5736aba485a99904a29459730af349ba0b969f91d099b09341a23a7aeaea1d"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m157_windows_control_pipe_eof.py": (
        "997c4bf52a6fb49dc2e0d94e8ffe31df9dcfe4ca20321e63fc5e9b0c3cc68bef"
    ),
    "tests/integration/test_windows_cache_cleanup_control_pipe_eof_probe.py": (
        "cd4ae117e85badede79436d02d30ad9d8f619c3174ab817a0467aab6377398f7"
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


def test_m158_changes_no_runtime_example_script_dependency_ci_or_m157_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m158_probe_writes_one_fixed_invalid_token_before_bounded_wait() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_invalid_control_token_probe.py"
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
        '"?"',
        "stdin.write(_INVALID_CONTROL_TOKEN)",
        "stdin.flush()",
        "stdin.close()",
        "assert stdin.closed",
        "blocker.wait(timeout=_TIMEOUT_SECONDS)",
        "return_code == _INVALID_CONTROL_EXIT_CODE",
        'stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "_ERROR_SHARING_VIOLATION",
        "succeeded=False",
        "succeeded=True",
    ):
        assert required in probe
    assert probe.count("stdin.write(_INVALID_CONTROL_TOKEN)") == 1
    assert probe.count("_attempt_native_child_rename(tmp_path)") == 2
    assert "_release_and_read_closed" not in probe
    assert "_RELEASE_TOKEN" not in probe
    assert "communicate(" not in probe
    assert "blocker.kill()" not in probe
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m158_documents_narrow_invalid_control_token_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-invalid-control-token-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "fixed invalid control token",
        "no closed acknowledgement",
        "not arbitrary malformed input",
        "no hosted check is added",
    ):
        assert required in compact


def test_m158_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0141-probe-windows-invalid-control-token.md").read_text(
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
        assert "cache-cleanup-windows-invalid-control-token-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0141-probe-windows-invalid-control-token.md" in rfc_index
