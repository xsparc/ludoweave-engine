"""Protect M157's test-only Windows blocker control-pipe EOF boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0139-probe-windows-abrupt-blocker-termination.md": (
        "d8be0cf3b551d898b7a15b59aeca13eb1e4f7368e018ad3b9ce2bb6dff5b00c7"
    ),
    "docs/security/cache-cleanup-windows-abrupt-blocker-termination-probe.md": (
        "324cdc4deca3e95f97d0dbc3dc3ce34a9047e693e386dfe66e59f52e29c72420"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m156_windows_abrupt_blocker_termination.py": (
        "c27e94cc2965d5b65fe64feec9cb2a636befa08c3e8551c080f5e10136f00c73"
    ),
    "tests/integration/test_windows_cache_cleanup_abrupt_blocker_termination_probe.py": (
        "2c32cd507db78552d6372cc31588e44408fa1bd9b7bf2615c85a5ec5b72a1b0c"
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


def test_m157_changes_no_runtime_example_script_dependency_ci_or_m156_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m157_probe_closes_only_the_control_writer_before_bounded_wait() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_control_pipe_eof_probe.py"
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
        "stdin.close()",
        "assert stdin.closed",
        "blocker.wait(timeout=_TIMEOUT_SECONDS)",
        "return_code == _CONTROL_EOF_EXIT_CODE",
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
    assert "stdin.write" not in probe
    assert "blocker.kill()" not in probe
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m157_documents_narrow_control_pipe_eof_evidence() -> None:
    decision = (_ROOT / "docs/security/cache-cleanup-windows-control-pipe-eof-probe.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "control-pipe eof",
        "no closed acknowledgement",
        "not arbitrary pipe failure",
        "no hosted check is added",
    ):
        assert required in compact


def test_m157_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0140-probe-windows-control-pipe-eof.md").read_text(encoding="utf-8")
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
        assert "cache-cleanup-windows-control-pipe-eof-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0140-probe-windows-control-pipe-eof.md" in rfc_index
