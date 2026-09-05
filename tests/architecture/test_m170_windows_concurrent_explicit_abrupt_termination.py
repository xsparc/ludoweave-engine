"""Protect M170's concurrent explicit-list abrupt-termination boundary."""

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
    "docs/rfcs/0152-probe-windows-concurrent-explicit-restore-failure.md": (
        "322beff063b8fef519b6378cb48d7a364ca2d0332fcc520ff5fd25ca966458d0"
    ),
    "docs/security/cache-cleanup-windows-abrupt-blocker-termination-probe.md": (
        "324cdc4deca3e95f97d0dbc3dc3ce34a9047e693e386dfe66e59f52e29c72420"
    ),
    "docs/security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md": (
        "93446e438027a2359606b3c565b91d856c39463fadbd47422ba55855e7c1482e"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m156_windows_abrupt_blocker_termination.py": (
        "99db0aed3bb0eb84741fe72a5be3ffc00af09b33dce0ab47a03199f36662ded4"
    ),
    "tests/architecture/test_m167_windows_concurrent_explicit_inheritance.py": (
        "3c0989fe5bfe2abe33cb5f144cdfa1d0b6c64dd77389186367d8401888ab2f33"
    ),
    "tests/architecture/test_m169_windows_concurrent_explicit_restore_failure.py": (
        "a2331b15631eb8fb0541e001933e341cf36bddba742bdf8d78175ad7c3b92cbb"
    ),
    "tests/fixtures/windows_share_delete_inherited_blocker_child.py": (
        "2c695324c4f7fecbbe98b71a540a1b4000f0361e55ab6f469c52ccb8b4110a4c"
    ),
    "tests/integration/test_windows_cache_cleanup_abrupt_blocker_termination_probe.py": (
        "2c32cd507db78552d6372cc31588e44408fa1bd9b7bf2615c85a5ec5b72a1b0c"
    ),
    "tests/integration/test_windows_cache_cleanup_concurrent_explicit_inheritance_probe.py": (
        "f42ddcc39899c8842e11fe540460a0a9c70b1af04d1ebc761c4e4cfd43436030"
    ),
    "tests/integration/test_windows_cache_cleanup_concurrent_explicit_restore_failure_probe.py": (
        "6ea0f7859eb3a34ae9ad0e2ca3d8fd05cf991784bf4e99375e6ec4aa15694489"
    ),
    "tests/integration/test_windows_cache_cleanup_inherited_handle_probe.py": (
        "d7085aebd2cb6f067bdaec6c5de839e6581ffe4cd432abf43da0ee15646748ae"
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
    / "tests/integration/test_windows_cache_cleanup_concurrent_explicit_abrupt_termination_probe.py"
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


def test_m170_changes_no_runtime_helper_fixture_dependency_ci_or_m169_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m170_creates_two_overlapping_exact_explicit_handle_lists() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "both_marked = threading.Event()",
        "both_created = threading.Event()",
        "permit_launch_return = threading.Event()",
        "both_restoring = threading.Event()",
        "permit_restore = threading.Event()",
        "marked_handles == expected_handles",
        "created_handles == expected_handles",
        "restoring_handles == expected_handles",
        'assert set(handle_list) == {"handle_list"}',
        "assert len(listed_handles) == 1",
        "str(inherited_probe._CHILD)",
        "close_fds is True",
        "shell is False",
        "stdin == subprocess.PIPE",
        "stdout == subprocess.PIPE",
        "stderr == subprocess.PIPE",
        "created_processes[label] = process",
        "inherited_probe._spawn_inherited_blocker(",
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


def test_m170_restores_and_releases_both_parents_before_termination() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    marked_index = probe.index("assert both_marked.wait(timeout=_TIMEOUT_SECONDS)")
    created_index = probe.index("assert both_created.wait(timeout=_TIMEOUT_SECONDS)")
    launch_release_index = probe.index("permit_launch_return.set()", created_index)
    restoring_index = probe.index("assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)")
    restore_release_index = probe.index("permit_restore.set()", restoring_index)
    ready_index = probe.index('inherited_probe._read_phase(process) == "ready"')
    parent_release_index = probe.index("blocker_probe.release(handle)", ready_index)
    kill_index = probe.index("abrupt_process.kill()", parent_release_index)
    assert (
        marked_index
        < created_index
        < launch_release_index
        < restoring_index
        < restore_release_index
        < ready_index
        < parent_release_index
        < kill_index
    )
    assert probe.count("original_get_handle_inheritable(handle) for handle") == 3
    assert "assert process.poll() is None" in probe
    assert "assert blocker_probe.owned_count == 0" in probe


def test_m170_waits_for_real_abrupt_exit_without_graceful_acknowledgement() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "abrupt_process.kill()",
        "abrupt_process.wait(timeout=_TIMEOUT_SECONDS)",
        "abrupt_return_code != 0",
        'abrupt_stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'abrupt_stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "processes[abrupt_label].returncode != 0",
        "processes[survivor_label].returncode == 0",
    ):
        assert required in probe
    kill_index = probe.index("abrupt_process.kill()")
    wait_index = probe.index("abrupt_process.wait(timeout=_TIMEOUT_SECONDS)", kill_index)
    stdout_index = probe.index("abrupt_stdout.read(_MAX_LINE_BYTES + 1)", wait_index)
    rename_index = probe.index("_attempt_native_child_rename(roots[abrupt_label])", stdout_index)
    assert kill_index < wait_index < stdout_index < rename_index


def test_m170_releases_only_abrupt_root_before_survivor_close() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    abrupt_success = probe.index(
        "_attempt_native_child_rename(roots[abrupt_label])",
        probe.index("abrupt_process.wait(timeout=_TIMEOUT_SECONDS)"),
    )
    survivor_denial = probe.index(
        "_attempt_native_child_rename(roots[survivor_label]) == denied",
        abrupt_success,
    )
    survivor_live = probe.index("assert survivor_process.poll() is None", survivor_denial)
    survivor_release = probe.index("_release_inherited_blocker(survivor_process)", survivor_live)
    survivor_success = probe.index(
        "_attempt_native_child_rename(roots[survivor_label])", survivor_release
    )
    assert abrupt_success < survivor_denial < survivor_live < survivor_release < survivor_success
    for required in (
        "assert not os.path.lexists(live_paths[abrupt_label])",
        "assert displaced_paths[abrupt_label].is_dir()",
        "assert live_paths[survivor_label].is_dir()",
        "assert not os.path.lexists(displaced_paths[survivor_label])",
        'displaced_paths[label] / "candidate.bin"',
    ):
        assert required in probe


def test_m170_cleanup_retains_every_parent_child_and_thread_owner() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "finally:",
        "both_marked.set()",
        "permit_launch_return.set()",
        "both_restoring.set()",
        "permit_restore.set()",
        "thread.join(timeout=_TIMEOUT_SECONDS)",
        "processes.setdefault(label, process)",
        "original_set_handle_inheritable(handle, False)",
        "blocker_probe.release(handle)",
        "for process in processes.values():",
        "_close_child(process)",
        "assert blocker_probe.owned_count == 0",
        "assert all(not thread.is_alive() for thread in threads.values())",
        "assert set(processes) == set(_LABELS)",
        "assert stream is not None and stream.closed",
    ):
        assert required in probe


def test_m170_rfc_and_public_boundary_are_registered() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "abruptly terminated root",
        "no graceful closed acknowledgement",
        "not crash recovery",
        "not a concurrency-safe process-creation contract",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT / "docs/rfcs/0153-probe-windows-concurrent-explicit-abrupt-termination.md"
    ).read_text(encoding="utf-8")
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
        assert "cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0153-probe-windows-concurrent-explicit-abrupt-termination.md" in rfc_index
