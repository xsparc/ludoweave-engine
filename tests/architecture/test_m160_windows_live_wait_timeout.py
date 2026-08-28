"""Protect M160's test-only Windows live-wait-timeout boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0142-probe-windows-broken-control-pipe.md": (
        "f7ebfda6bf0971849e7ac4f24f88f88f6e97e0f99f3300360054f9c507b6fb8b"
    ),
    "docs/security/cache-cleanup-windows-broken-control-pipe-probe.md": (
        "f13219cc91418d2bf511862e7bee937e4a0a75ac3919ff43a29183852bec0ecb"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m159_windows_broken_control_pipe.py": (
        "5368bc7d20a78f242d6b05f6c63dde9b10fdbd587f87747efc17eb1a59bc2a29"
    ),
    "tests/integration/test_windows_cache_cleanup_broken_control_pipe_probe.py": (
        "e3fb34dd17f17cdcb8e68723ff04434fb8bfa289f68fe203d0690028a6aef235"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
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


def test_m160_changes_no_runtime_example_script_dependency_ci_or_m159_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m160_timeout_preserves_live_denial_before_graceful_close() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_live_wait_timeout_probe.py"
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
        "_IMMEDIATE_WAIT_SECONDS = 0.0",
        "pytest.raises(subprocess.TimeoutExpired)",
        "blocker.wait(timeout=_IMMEDIATE_WAIT_SECONDS)",
        "raised.value.cmd == blocker.args",
        "raised.value.timeout == _IMMEDIATE_WAIT_SECONDS",
        "blocker.returncode is None",
        "_release_and_read_closed(blocker)",
        '== "closed"',
        "_ERROR_SHARING_VIOLATION",
        "succeeded=False",
        "succeeded=True",
    ):
        assert required in probe
    rename_call = "_attempt_native_child_rename(tmp_path)"
    rename_indexes: list[int] = []
    next_index = 0
    for _ in range(3):
        next_index = probe.index(rename_call, next_index)
        rename_indexes.append(next_index)
        next_index += len(rename_call)
    wait_index = probe.index("blocker.wait(timeout=_IMMEDIATE_WAIT_SECONDS)")
    release_index = probe.index("_release_and_read_closed(blocker)")
    assert rename_indexes[0] < wait_index < rename_indexes[1]
    assert rename_indexes[1] < release_index < rename_indexes[2]
    assert probe.count(rename_call) == 3
    assert probe.count("blocker.wait(timeout=_IMMEDIATE_WAIT_SECONDS)") == 1
    assert "blocker.kill()" not in probe
    assert "communicate(" not in probe
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m160_documents_narrow_live_wait_timeout_evidence() -> None:
    decision = (_ROOT / "docs/security/cache-cleanup-windows-live-wait-timeout-probe.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "zero-duration wait",
        "not a timeout recovery contract",
        "no hosted check is added",
    ):
        assert required in compact


def test_m160_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0143-probe-windows-live-wait-timeout.md").read_text(encoding="utf-8")
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
        assert "cache-cleanup-windows-live-wait-timeout-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0143-probe-windows-live-wait-timeout.md" in rfc_index
