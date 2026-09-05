"""Protect M164's test-only inherited-handle launch-failure boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0146-probe-windows-inherited-blocker-handle.md": (
        "f02acc8403b0ce9101e0bdceb0f888ccbcc76cce4242dd0276457181471a041f"
    ),
    "docs/security/cache-cleanup-windows-inherited-handle-probe.md": (
        "f4fef0a7833bec9ffcdff83b2e162988671edd1f286cc67564526239c53708b6"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m163_windows_inherited_handle.py": (
        "d98424dec75855281d3ec4eb02e18f089be1f6674a819d00157e9554b21a4cb1"
    ),
    "tests/integration/test_windows_cache_cleanup_inherited_handle_probe.py": (
        "d7085aebd2cb6f067bdaec6c5de839e6581ffe4cd432abf43da0ee15646748ae"
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


def test_m164_changes_no_runtime_example_script_dependency_ci_or_m163_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m164_probe_uses_one_handle_and_a_fixed_missing_executable() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_inherited_launch_failure_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        '_MISSING_EXECUTABLE_NAME = "m164-missing-launch-target.exe"',
        "if os.path.lexists(missing_executable):",
        'startup_info.lpAttributeList = {"handle_list": [handle]}',
        "if os.get_handle_inheritable(handle):",
        "os.set_handle_inheritable(handle, True)",
        "process = subprocess.Popen(",
        "(str(missing_executable),)",
        "close_fds=True",
        "cwd=working_directory",
        "executable=str(missing_executable)",
        "shell=False",
        "startupinfo=startup_info",
        "stdin=subprocess.DEVNULL",
        "stdout=subprocess.DEVNULL",
        "stderr=subprocess.DEVNULL",
        "except FileNotFoundError as candidate:",
        "os.set_handle_inheritable(handle, False)",
        "if process is not None:",
        "_close_child(process)",
        "return error",
    ):
        assert required in probe
    missing_index = probe.index("if os.path.lexists(missing_executable):")
    inherit_index = probe.index("os.set_handle_inheritable(handle, True)")
    spawn_index = probe.index("process = subprocess.Popen(")
    restore_index = probe.index("os.set_handle_inheritable(handle, False)")
    return_index = probe.index("return error")
    assert missing_index < inherit_index < spawn_index < restore_index < return_index
    assert probe.count('startup_info.lpAttributeList = {"handle_list": [handle]}') == 1
    assert "time.sleep" not in probe
    assert "communicate(" not in probe
    assert '"-c"' not in probe
    assert "env=" not in probe


def test_m164_probe_orders_failed_launch_before_denial_and_release() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_inherited_launch_failure_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "error = _attempt_missing_executable_launch(blocker_handle, tmp_path)",
        "assert type(error) is FileNotFoundError",
        "assert error.errno == errno.ENOENT",
        "assert error.winerror == _ERROR_FILE_NOT_FOUND",
        "assert os.get_handle_inheritable(blocker_handle) is False",
        "assert blocker_probe.owned_count == 1",
        "blocker_probe.release(blocker_handle)",
        "assert blocker_probe.owned_count == 0",
        "_ERROR_SHARING_VIOLATION",
        "succeeded=False",
        "succeeded=True",
    ):
        assert required in probe
    launch_index = probe.index("error = _attempt_missing_executable_launch(")
    restored_index = probe.index("assert os.get_handle_inheritable(blocker_handle) is False")
    rename_call = "_attempt_native_child_rename(tmp_path)"
    first_rename_index = probe.index(rename_call)
    release_index = probe.index("blocker_probe.release(blocker_handle)")
    second_rename_index = probe.index(rename_call, first_rename_index + len(rename_call))
    assert launch_index < restored_index < first_rename_index < release_index
    assert release_index < second_rename_index
    assert probe.count(rename_call) == 2


def test_m164_documents_narrow_launch_failure_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-inherited-launch-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "real process-creation failure",
        "not restoration-failure injection",
        "not a concurrency-safe inheritance contract",
        "no hosted check is added",
    ):
        assert required in compact


def test_m164_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0147-probe-windows-inherited-launch-failure.md").read_text(
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
        assert "cache-cleanup-windows-inherited-launch-failure-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0147-probe-windows-inherited-launch-failure.md" in rfc_index
