"""Protect M168's concurrent explicit-list launch-failure isolation boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0150-probe-windows-concurrent-explicit-inheritance.md": (
        "87b4493ee532388343fa03a35ab338ba79cfe54eb84188f4c092b2ceb7b04a68"
    ),
    "docs/security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md": (
        "26ad09564b472d7ea60a9f0ba42a0757c049d638c954780f73cad5e1dcbc2a70"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m167_windows_concurrent_explicit_inheritance.py": (
        "3c0989fe5bfe2abe33cb5f144cdfa1d0b6c64dd77389186367d8401888ab2f33"
    ),
    "tests/fixtures/windows_share_delete_inherited_blocker_child.py": (
        "2c695324c4f7fecbbe98b71a540a1b4000f0361e55ab6f469c52ccb8b4110a4c"
    ),
    "tests/integration/test_windows_cache_cleanup_concurrent_explicit_inheritance_probe.py": (
        "f42ddcc39899c8842e11fe540460a0a9c70b1af04d1ebc761c4e4cfd43436030"
    ),
    "tests/integration/test_windows_cache_cleanup_inherited_handle_probe.py": (
        "d7085aebd2cb6f067bdaec6c5de839e6581ffe4cd432abf43da0ee15646748ae"
    ),
    "tests/integration/test_windows_cache_cleanup_inherited_launch_failure_probe.py": (
        "f3e811b8a1c319401e20434f10dfbd9e36095f95465c319eb42828c51db7c723"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_concurrent_explicit_launch_failure_probe.py"
)


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


def test_m168_changes_no_runtime_helper_fixture_dependency_ci_or_m167_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m168_overlaps_success_and_failure_outcomes_before_restoration() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "both_marked = threading.Event()",
        "both_launching = threading.Event()",
        "permit_launch = threading.Event()",
        "both_outcomes = threading.Event()",
        "permit_outcome_return = threading.Event()",
        "both_restoring = threading.Event()",
        "permit_restore = threading.Event()",
        "marked_handles == expected_handles",
        'launching_roles == {"success", "failure"}',
        'outcome_roles == {"success", "failure"}',
        "restoring_handles == expected_handles",
        'wait_for_launch("success")',
        'wait_for_launch("failure")',
        'record_outcome("success")',
        'record_outcome("failure")',
        "assert both_marked.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_launching.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_outcomes.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)",
    ):
        assert required in probe

    marked_index = probe.index("assert both_marked.wait(timeout=_TIMEOUT_SECONDS)")
    launching_index = probe.index("assert both_launching.wait(timeout=_TIMEOUT_SECONDS)")
    permit_launch_index = probe.index("permit_launch.set()", launching_index)
    outcomes_index = probe.index("assert both_outcomes.wait(timeout=_TIMEOUT_SECONDS)")
    permit_outcome_index = probe.index("permit_outcome_return.set()", outcomes_index)
    restoring_index = probe.index("assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)")
    permit_restore_index = probe.index("permit_restore.set()", restoring_index)
    join_index = probe.index("thread.join(timeout=_TIMEOUT_SECONDS)", permit_restore_index)
    assert (
        marked_index
        < launching_index
        < permit_launch_index
        < outcomes_index
        < permit_outcome_index
        < restoring_index
        < permit_restore_index
        < join_index
    )
    assert probe.count("original_get_handle_inheritable(handle) for handle") == 3


def test_m168_uses_exact_success_and_missing_executable_explicit_lists() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        'handle_list == {"handle_list": [success_handle]}',
        'handle_list == {"handle_list": [failure_handle]}',
        "tuple(arguments) == (str(missing_executable),)",
        "executable == str(missing_executable)",
        "close_fds is True",
        "shell is False",
        "stdin == subprocess.PIPE",
        "stdin == subprocess.DEVNULL",
        "inherited_probe._spawn_inherited_blocker(",
        "failure_probe._attempt_missing_executable_launch(",
        "type(observed_failure) is FileNotFoundError",
        "observed_failure.errno == errno.ENOENT",
        "observed_failure.winerror == failure_probe._ERROR_FILE_NOT_FOUND",
        'set(created_processes) == {"success"}',
    ):
        assert required in probe
    for forbidden in (
        "close_fds=False",
        "shell=True",
        "os.system",
        "time.sleep",
        "communicate(",
        '"-c"',
        "env=",
    ):
        assert forbidden not in probe


def test_m168_failed_root_releases_before_the_successful_child() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    denied_loop = probe.index("_attempt_native_child_rename(roots[label]) == denied")
    parent_release = probe.index("blocker_probe.release(handle)", denied_loop)
    failed_success = probe.index(
        "_attempt_native_child_rename(roots[failure_label])", parent_release
    )
    successful_denial = probe.index(
        "_attempt_native_child_rename(roots[success_label]) == denied", failed_success
    )
    child_live = probe.index("assert success_process.poll() is None", successful_denial)
    child_release = probe.index("_release_inherited_blocker(success_process)", child_live)
    successful_success = probe.index(
        "_attempt_native_child_rename(roots[success_label])", child_release
    )
    assert (
        denied_loop
        < parent_release
        < failed_success
        < successful_denial
        < child_live
        < child_release
        < successful_success
    )
    for required in (
        "assert not os.path.lexists(live_paths[failure_label])",
        "assert displaced_paths[failure_label].is_dir()",
        "assert live_paths[success_label].is_dir()",
        "assert not os.path.lexists(displaced_paths[success_label])",
        'displaced_paths[label] / "candidate.bin"',
    ):
        assert required in probe


def test_m168_cleanup_retains_every_parent_child_and_thread_owner() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        'created_processes["success"] = process',
        'created_processes["failure"] = process',
        "finally:",
        "both_marked.set()",
        "both_launching.set()",
        "permit_launch.set()",
        "both_outcomes.set()",
        "permit_outcome_return.set()",
        "both_restoring.set()",
        "permit_restore.set()",
        'success_process = created_processes.get("success")',
        "original_set_handle_inheritable(handle, False)",
        "blocker_probe.release(handle)",
        "for process in created_processes.values():",
        "_close_child(process)",
        "assert blocker_probe.owned_count == 0",
        "assert all(not thread.is_alive() for thread in threads.values())",
        'assert set(created_processes) == {"success"}',
        "success_process.returncode == 0",
        "assert stream is not None and stream.closed",
    ):
        assert required in probe
    capture_index = probe.index('created_processes["success"] = process')
    outcome_wait = probe.index('record_outcome("success")', capture_index)
    finally_index = probe.index("finally:", probe.index("success_process:"))
    recover_index = probe.index('success_process = created_processes.get("success")', finally_index)
    repair_index = probe.index("original_set_handle_inheritable(handle, False)", recover_index)
    release_index = probe.index("blocker_probe.release(handle)", repair_index)
    close_index = probe.index("_close_child(process)", release_index)
    assert capture_index < outcome_wait < finally_index < recover_index
    assert recover_index < repair_index < release_index < close_index


def test_m168_rfc_and_public_boundary_are_registered() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "failed-launch root",
        "not a concurrency-safe process-creation contract",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0151-probe-windows-concurrent-explicit-launch-failure.md").read_text(
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
        assert "cache-cleanup-windows-concurrent-explicit-launch-failure-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0151-probe-windows-concurrent-explicit-launch-failure.md" in rfc_index
