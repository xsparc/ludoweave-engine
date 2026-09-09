"""Protect M162's test-only duplicated blocker-handle boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0144-probe-windows-acknowledged-release-timeout.md": (
        "0aa5ca4493f60afe4b9fdd3b96dabc9dd6490b07a703dbd5a961dc2d09d111b7"
    ),
    "docs/security/cache-cleanup-windows-acknowledged-release-timeout-probe.md": (
        "3ad24097136110935f3466bd40c241e386ef63f5684272aabd52bac3920693b9"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m161_windows_acknowledged_release_timeout.py": (
        "ffecc12a5ddfe8b2e0df4affbb2c54a1bea083c744e8c45515baa5ca7f58f36c"
    ),
    "tests/integration/test_windows_cache_cleanup_acknowledged_release_timeout_probe.py": (
        "653cc2e34cd4ddea922c82fe45df0405435f9181631022217759883deb90de4e"
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


def test_m162_changes_no_runtime_example_script_dependency_ci_or_m161_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m162_fixture_duplicates_then_closes_each_handle_once_in_order() -> None:
    fixture = (_ROOT / "tests/fixtures/windows_share_delete_duplicated_blocker_child.py").read_text(
        encoding="utf-8"
    )
    for required in (
        '_SCHEMA = "ludoweave.test.windows-duplicated-share-delete-blocker/1"',
        '_CLOSE_ORIGINAL_TOKEN = b"1"',
        '_CLOSE_DUPLICATE_TOKEN = b"2"',
        '"GetCurrentProcess"',
        '"DuplicateHandle"',
        "_DUPLICATE_SAME_ACCESS",
        "ctypes.byref(duplicate_result)",
        "False,",
        '_emit("ready")',
        "sys.stdin.buffer.read(1) != _CLOSE_ORIGINAL_TOKEN",
        "close_handle(wintypes.HANDLE(source_to_close))",
        '_emit("original-closed")',
        "sys.stdin.buffer.read(1) != _CLOSE_DUPLICATE_TOKEN",
        "close_handle(wintypes.HANDLE(duplicate_to_close))",
        '_emit("closed")',
    ):
        assert required in fixture
    duplicate_index = fixture.index("duplicate_handle(")
    ready_index = fixture.index('_emit("ready")')
    original_token_index = fixture.index("sys.stdin.buffer.read(1) != _CLOSE_ORIGINAL_TOKEN")
    original_close_index = fixture.index("close_handle(wintypes.HANDLE(source_to_close))")
    original_closed_index = fixture.index('_emit("original-closed")')
    duplicate_token_index = fixture.index("sys.stdin.buffer.read(1) != _CLOSE_DUPLICATE_TOKEN")
    duplicate_close_index = fixture.index("close_handle(wintypes.HANDLE(duplicate_to_close))")
    closed_index = fixture.index('_emit("closed")')
    assert duplicate_index < ready_index < original_token_index < original_close_index
    assert original_close_index < original_closed_index < duplicate_token_index
    assert duplicate_token_index < duplicate_close_index < closed_index
    assert fixture.count("close_handle(wintypes.HANDLE(source_to_close))") == 1
    assert fixture.count("close_handle(wintypes.HANDLE(duplicate_to_close))") == 1
    assert "time.sleep" not in fixture


def test_m162_probe_orders_both_denials_before_final_close() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_duplicated_handle_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        '(sys.executable, "-I", "-B", str(_CHILD))',
        "close_fds=True",
        "cwd=tmp_path",
        "shell=False",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        'assert _read_phase(blocker) == "ready"',
        "except queue.Empty:",
        "process.kill()",
        "process.wait(timeout=_TIMEOUT_SECONDS)",
        "reader.join(timeout=_TIMEOUT_SECONDS)",
        "stdin.write(_CLOSE_ORIGINAL_TOKEN)",
        'assert _read_phase(blocker) == "original-closed"',
        "stdin.write(_CLOSE_DUPLICATE_TOKEN)",
        'assert _read_phase(blocker) == "closed"',
        "blocker.wait(timeout=_TIMEOUT_SECONDS) == 0",
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
    original_token_index = probe.index("stdin.write(_CLOSE_ORIGINAL_TOKEN)")
    original_closed_index = probe.index('assert _read_phase(blocker) == "original-closed"')
    duplicate_token_index = probe.index("stdin.write(_CLOSE_DUPLICATE_TOKEN)")
    closed_index = probe.index('assert _read_phase(blocker) == "closed"')
    assert rename_indexes[0] < original_token_index < original_closed_index
    assert original_closed_index < rename_indexes[1] < duplicate_token_index
    assert duplicate_token_index < closed_index < rename_indexes[2]
    assert probe.count(rename_call) == 3
    assert "blocker.kill()" not in probe
    assert "communicate(" not in probe
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m162_documents_narrow_duplicated_handle_evidence() -> None:
    decision = (_ROOT / "docs/security/cache-cleanup-windows-duplicated-handle-probe.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "same-process duplicate",
        "not inherited-handle evidence",
        "no hosted check is added",
    ):
        assert required in compact


def test_m162_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0145-probe-windows-duplicated-blocker-handle.md").read_text(
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
        assert "cache-cleanup-windows-duplicated-handle-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0145-probe-windows-duplicated-blocker-handle.md" in rfc_index
