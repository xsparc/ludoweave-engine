"""Protect M163's test-only inherited blocker-handle boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0145-probe-windows-duplicated-blocker-handle.md": (
        "889da30f5bf8aec590f718ac2d134d1dcaa6f111fc526376ec5b59f5e1089b3c"
    ),
    "docs/security/cache-cleanup-windows-duplicated-handle-probe.md": (
        "8781ddcfb0b7fe3a4220f314c58fbf43180465884a7850fecee41d4ae71c8d82"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m162_windows_duplicated_handle.py": (
        "53ffef719020ef9faf598badf8f6253570b2c31f4dc064f6a24d68b214df322c"
    ),
    "tests/integration/test_windows_cache_cleanup_duplicated_handle_probe.py": (
        "de32c80aa74c28d64484c0faa07b3c32f7d884246ad9838afe2202d2d79bf926"
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
