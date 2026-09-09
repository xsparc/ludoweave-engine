"""Protect M159's test-only Windows broken-control-pipe boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
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
        "171d2534ec25604722c92c30a7fafd7157186fa2b811e182cc8624cfce5056df"
    ),
    "tests/integration/test_windows_cache_cleanup_invalid_control_token_probe.py": (
        "1ae6b76d1b9adcf31257e2c973f6141947f045dd325f44c6719956a0e604d60c"
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
        "docs/readme-history.md",
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
