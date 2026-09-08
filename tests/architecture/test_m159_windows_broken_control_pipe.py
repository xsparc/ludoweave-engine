"""Protect M159's test-only Windows broken-control-pipe boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "67fc471f84d7dde8b239bd9e92235a34f780cc3d3370b0dbf451e6a922a027f1",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0141-probe-windows-invalid-control-token.md": (
        "812d8ba3ab32a20f02ce8a3e44e2df352b31dec7b943fdb969e8ccc3cb086b21"
    ),
    "docs/security/cache-cleanup-windows-invalid-control-token-probe.md": (
        "aa91ceec20285d562ec1e479a67c07e778f027aaadd536692bddb803d2dbee45"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m158_windows_invalid_control_token.py": (
        "6b144d1710ecf4a83c2b109e0671d6e4fb310e76a39ae2d3fe9a7528ea3f2a3d"
    ),
    "tests/integration/test_windows_cache_cleanup_invalid_control_token_probe.py": (
        "1ae6b76d1b9adcf31257e2c973f6141947f045dd325f44c6719956a0e604d60c"
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


def test_m159_changes_no_runtime_example_script_dependency_ci_or_m158_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m159_probe_writes_only_after_bounded_blocker_termination() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_broken_control_pipe_probe.py"
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
        '"WriteFile"',
        "msvcrt.get_osfhandle(stream.fileno())",
        "ctypes.set_last_error(0)",
        "error_code=0 if succeeded else ctypes.get_last_error()",
        "_ERROR_NO_DATA",
        "bytes_written=0",
        "_attempt_native_pipe_write(cast(BinaryIO, stdin))",
        "stdin.close()",
        "assert stdin.closed",
        'stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "_ERROR_SHARING_VIOLATION",
        "succeeded=False",
        "succeeded=True",
    ):
        assert required in probe
    assert probe.count("blocker.kill()") == 1
    assert probe.count("_attempt_native_pipe_write(cast(BinaryIO, stdin))") == 1
    wait_index = probe.index("blocker.wait(timeout=_TIMEOUT_SECONDS)")
    stdout_eof_index = probe.index('stdout.read(_MAX_LINE_BYTES + 1) == b""')
    stderr_eof_index = probe.index('stderr.read(_MAX_LINE_BYTES + 1) == b""')
    write_index = probe.index("_attempt_native_pipe_write(cast(BinaryIO, stdin))")
    close_index = probe.index("stdin.close()")
    assert wait_index < stdout_eof_index < write_index < close_index
    assert wait_index < stderr_eof_index < write_index
    assert probe.count("_attempt_native_child_rename(tmp_path)") == 2
    assert "_release_and_read_closed" not in probe
    assert "communicate(" not in probe
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m159_documents_narrow_broken_control_pipe_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-broken-control-pipe-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "fixed late release byte",
        "error 232",
        "not a recovery contract",
        "no hosted check is added",
    ):
        assert required in compact


def test_m159_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0142-probe-windows-broken-control-pipe.md").read_text(
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
        assert "cache-cleanup-windows-broken-control-pipe-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0142-probe-windows-broken-control-pipe.md" in rfc_index
