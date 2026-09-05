"""Protect M169's concurrent explicit-list restoration-failure boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0151-probe-windows-concurrent-explicit-launch-failure.md": (
        "2415a1a8070c79377537312fdc095e375a46f271a57418423de311db9cc35ed7"
    ),
    "docs/security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md": (
        "8c64309370d3418e5bd62d07174f5a76b0d7fc12f3d57f367a79f7f8879eeb8b"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m165_windows_inherited_restore_failure.py": (
        "7434a108068501e74ea781d4526a0a8336a6554a5ac3017792c5bc309f692739"
    ),
    "tests/architecture/test_m168_windows_concurrent_explicit_launch_failure.py": (
        "5841f46b30281f139045567e738bd34193bb604fd1e45a81e46fa1aff13dd0b1"
    ),
    "tests/fixtures/windows_share_delete_inherited_blocker_child.py": (
        "2c695324c4f7fecbbe98b71a540a1b4000f0361e55ab6f469c52ccb8b4110a4c"
    ),
    "tests/integration/test_windows_cache_cleanup_concurrent_explicit_launch_failure_probe.py": (
        "8eed62b2f2f332273490cf1ec1c70870fd711a04968548bb74e20f697b07dc77"
    ),
    "tests/integration/test_windows_cache_cleanup_inherited_handle_probe.py": (
        "d7085aebd2cb6f067bdaec6c5de839e6581ffe4cd432abf43da0ee15646748ae"
    ),
    "tests/integration/test_windows_cache_cleanup_inherited_restore_failure_probe.py": (
        "c0ddd685306c8fe9d70f99504eadbcd963a39273499f435f8d1977ea8397a977"
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
    / "tests/integration/test_windows_cache_cleanup_concurrent_explicit_restore_failure_probe.py"
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


def test_m169_changes_no_runtime_helper_fixture_dependency_ci_or_m168_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m169_overlaps_two_launches_and_restores_before_injection() -> None:
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
        "launching_handles == expected_handles",
        "outcome_handles == expected_handles",
        "restoring_handles == expected_handles",
        "assert both_marked.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_launching.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_outcomes.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)",
        "raise injected",
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
    assert (
        "original_get_handle_inheritable(handle) is False for handle in expected_handles"
    ) in probe


def test_m169_uses_exact_two_successful_explicit_handle_lists() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        'assert set(handle_list) == {"handle_list"}',
        "assert len(listed_handles) == 1",
        "assert handle in expected_handles",
        "str(inherited_probe._CHILD)",
        "str(handle)",
        "close_fds is True",
        "shell is False",
        "stdin == subprocess.PIPE",
        "stdout == subprocess.PIPE",
        "stderr == subprocess.PIPE",
        "inherited_probe._spawn_inherited_blocker(",
        "assert set(created_processes) == expected_handles",
        "assert launch_errors == {}",
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


def test_m169_reaps_failed_restore_child_before_parent_repair() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_InjectedRestoreFailure",
        "if handle == failure_handle:",
        "restore_failure_attempts += 1",
        "assert restore_failure_attempts == 1",
        'monkeypatch.setattr(inherited_probe, "_close_child", capture_helper_close)',
        "helper_closed_processes.append(process)",
        "helper_preclose_returncodes.append(process.poll())",
        "original_close_child(process)",
        "assert failure_result.error is injected",
        "assert helper_closed_processes == [failed_process]",
        "assert helper_preclose_returncodes == [None]",
        "assert failed_process.returncode is not None",
        "assert stream is not None and stream.closed",
        "assert original_get_handle_inheritable(failure_handle) is True",
        "original_set_handle_inheritable(failure_handle, False)",
    ):
        assert required in probe
    failure_index = probe.index("assert failure_result.error is injected")
    reaped_index = probe.index("assert failed_process.returncode is not None", failure_index)
    inherited_index = probe.index(
        "assert original_get_handle_inheritable(failure_handle) is True", reaped_index
    )
    repair_index = probe.index(
        "original_set_handle_inheritable(failure_handle, False)", inherited_index
    )
    assert failure_index < reaped_index < inherited_index < repair_index


def test_m169_failed_restore_root_releases_before_surviving_child() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    repair_index = probe.index("original_set_handle_inheritable(failure_handle, False)")
    parent_release = probe.index("blocker_probe.release(handle)", repair_index)
    failed_success = probe.index(
        "_attempt_native_child_rename(roots[failure_label])", parent_release
    )
    survivor_denial = probe.index(
        "_attempt_native_child_rename(roots[survivor_label]) == denied", failed_success
    )
    child_live = probe.index("assert survivor_process.poll() is None", survivor_denial)
    child_release = probe.index("_release_inherited_blocker(survivor_process)", child_live)
    survivor_success = probe.index(
        "_attempt_native_child_rename(roots[survivor_label])", child_release
    )
    assert (
        repair_index
        < parent_release
        < failed_success
        < survivor_denial
        < child_live
        < child_release
        < survivor_success
    )
    for required in (
        "assert not os.path.lexists(live_paths[failure_label])",
        "assert displaced_paths[failure_label].is_dir()",
        "assert live_paths[survivor_label].is_dir()",
        "assert not os.path.lexists(displaced_paths[survivor_label])",
        'displaced_paths[label] / "candidate.bin"',
    ):
        assert required in probe


def test_m169_cleanup_retains_every_parent_child_and_thread_owner() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "created_processes[handle] = process",
        "finally:",
        "both_marked.set()",
        "both_launching.set()",
        "permit_launch.set()",
        "both_outcomes.set()",
        "permit_outcome_return.set()",
        "both_restoring.set()",
        "permit_restore.set()",
        "survivor_process = created_processes.get(survivor_handle)",
        "original_set_handle_inheritable(handle, False)",
        "blocker_probe.release(handle)",
        "for process in created_processes.values():",
        "original_close_child(process)",
        "assert blocker_probe.owned_count == 0",
        "assert all(not thread.is_alive() for thread in threads.values())",
        "assert set(created_processes) == expected_handles",
        "survivor_process.returncode == 0",
        "assert stream is not None and stream.closed",
    ):
        assert required in probe
    capture_index = probe.index("created_processes[handle] = process")
    outcome_wait = probe.index("record_launch_outcome(handle)", capture_index)
    finally_index = probe.index("finally:", probe.index("survivor_process:"))
    recover_index = probe.index(
        "survivor_process = created_processes.get(survivor_handle)", finally_index
    )
    repair_index = probe.index("original_set_handle_inheritable(handle, False)", recover_index)
    release_index = probe.index("blocker_probe.release(handle)", repair_index)
    close_index = probe.index("original_close_child(process)", release_index)
    assert capture_index < outcome_wait < finally_index < recover_index
    assert recover_index < repair_index < release_index < close_index


def test_m169_rfc_and_public_boundary_are_registered() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "failed-restoration root",
        "not a real native restoration failure",
        "not a concurrency-safe process-creation contract",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0152-probe-windows-concurrent-explicit-restore-failure.md").read_text(
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
        assert "cache-cleanup-windows-concurrent-explicit-restore-failure-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0152-probe-windows-concurrent-explicit-restore-failure.md" in rfc_index
