"""Protect M163's test-only inherited blocker-handle boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "23f4cf86fdf46be2f56b38345f09bac61c7753ad15f05302874afb99d4a20394",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0145-probe-windows-duplicated-blocker-handle.md": (
        "889da30f5bf8aec590f718ac2d134d1dcaa6f111fc526376ec5b59f5e1089b3c"
    ),
    "docs/security/cache-cleanup-windows-duplicated-handle-probe.md": (
        "8781ddcfb0b7fe3a4220f314c58fbf43180465884a7850fecee41d4ae71c8d82"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m162_windows_duplicated_handle.py": (
        "c56d1147597664880d4e837868a7c380351179ad2ebd05b0a86d0ce0f80a3b6a"
    ),
    "tests/integration/test_windows_cache_cleanup_duplicated_handle_probe.py": (
        "de32c80aa74c28d64484c0faa07b3c32f7d884246ad9838afe2202d2d79bf926"
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


def test_m163_changes_no_runtime_example_script_dependency_ci_or_m162_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m163_fixture_validates_and_closes_only_the_inherited_handle() -> None:
    fixture = (_ROOT / "tests/fixtures/windows_share_delete_inherited_blocker_child.py").read_text(
        encoding="utf-8"
    )
    for required in (
        '_SCHEMA = "ludoweave.test.windows-inherited-share-delete-blocker/1"',
        "len(sys.argv) != 2",
        "not argument.isascii()",
        "not argument.isdecimal()",
        "value <= 0 or argument != str(value)",
        '_emit("ready")',
        "sys.stdin.buffer.read(1) != _RELEASE_TOKEN",
        "handle_to_close = owned_handle",
        "owned_handle = None",
        "close_handle(wintypes.HANDLE(handle_to_close))",
        '_emit("closed")',
    ):
        assert required in fixture
    ready_index = fixture.index('_emit("ready")')
    token_index = fixture.index("sys.stdin.buffer.read(1) != _RELEASE_TOKEN")
    clear_index = fixture.index("owned_handle = None")
    close_index = fixture.index("close_handle(wintypes.HANDLE(handle_to_close))")
    closed_index = fixture.index('_emit("closed")')
    assert ready_index < token_index < clear_index < close_index < closed_index
    assert fixture.count("close_handle(wintypes.HANDLE(handle_to_close))") == 1
    assert "time.sleep" not in fixture


def test_m163_probe_allowlists_one_handle_and_orders_all_rename_results() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_inherited_handle_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        'startup_info.lpAttributeList = {"handle_list": [handle]}',
        "os.set_handle_inheritable(handle, True)",
        "os.set_handle_inheritable(handle, False)",
        "if os.get_handle_inheritable(handle):",
        "if process is not None:",
        "_close_child(process)",
        '(sys.executable, "-I", "-B", str(_CHILD), str(handle))',
        "close_fds=True",
        "cwd=working_directory",
        "shell=False",
        "startupinfo=startup_info",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "assert os.get_handle_inheritable(blocker_handle) is False",
        'assert _read_phase(blocker) == "ready"',
        "blocker_probe.release(blocker_handle)",
        "stdin.write(_RELEASE_TOKEN)",
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
    parent_release_index = probe.index("blocker_probe.release(blocker_handle)")
    child_release_index = probe.index("stdin.write(_RELEASE_TOKEN)")
    closed_index = probe.index('assert _read_phase(blocker) == "closed"')
    assert rename_indexes[0] < parent_release_index < rename_indexes[1]
    assert rename_indexes[1] < child_release_index < closed_index < rename_indexes[2]
    inherit_index = probe.index("os.set_handle_inheritable(handle, True)")
    spawn_index = probe.index("process = subprocess.Popen(")
    restore_index = probe.index("os.set_handle_inheritable(handle, False)")
    assert inherit_index < spawn_index < restore_index
    assert probe.count(rename_call) == 3
    assert '"-c"' not in probe
    assert "blocker.kill()" not in probe
    assert "communicate(" not in probe
    assert "time.sleep" not in probe


def test_m163_documents_narrow_inherited_handle_evidence() -> None:
    decision = (_ROOT / "docs/security/cache-cleanup-windows-inherited-handle-probe.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "explicit handle list",
        "not a concurrency-safe inheritance contract",
        "no hosted check is added",
    ):
        assert required in compact


def test_m163_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0146-probe-windows-inherited-blocker-handle.md").read_text(
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
        assert "cache-cleanup-windows-inherited-handle-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0146-probe-windows-inherited-blocker-handle.md" in rfc_index
