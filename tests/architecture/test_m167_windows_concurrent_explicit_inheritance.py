"""Protect M167's simultaneous explicit handle-list isolation boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "23f4cf86fdf46be2f56b38345f09bac61c7753ad15f05302874afb99d4a20394",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0149-probe-windows-concurrent-inheritance-leak.md": (
        "b36d5f1a73913026933f02241769d2f1d3aeaa4d66ade95a34975007c081c2f6"
    ),
    "docs/security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md": (
        "f8b205bee1f634843b69c24997302dd10dc306eafb9d5d33b3ed0fa4e9e618ac"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m166_windows_concurrent_inheritance_leak.py": (
        "458cfd15c5441e7b437a285f6bc7e1111f0bb91c1f8cd7f43bd2a9b01d514499"
    ),
    "tests/fixtures/windows_share_delete_inherited_blocker_child.py": (
        "2c695324c4f7fecbbe98b71a540a1b4000f0361e55ab6f469c52ccb8b4110a4c"
    ),
    "tests/integration/test_windows_cache_cleanup_concurrent_inheritance_leak_probe.py": (
        "45e208ec7827e7c03a620fdf8a8de209ef48356ed48585f4c4b1566fe752dc41"
    ),
    "tests/integration/test_windows_cache_cleanup_inherited_handle_probe.py": (
        "d7085aebd2cb6f067bdaec6c5de839e6581ffe4cd432abf43da0ee15646748ae"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "8e8d3a618b8bb14c439d4c0809db345fe471dc7c07f1765b03c4bb507f8fc98a",
    "scripts": "8833e1120f60e74f4b5024ef6a6049821a72afef44c0143bab3f7bbd9298e247",
    "src/ludoweave": "1e7f21b3d5bb0a8021f47f9bf1089873a59cb3e798b02933569d3eee3c9a35c1",
}
_PROBE = (
    _ROOT / "tests/integration/test_windows_cache_cleanup_concurrent_explicit_inheritance_probe.py"
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


def test_m167_changes_no_runtime_helper_fixture_dependency_ci_or_m166_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m167_overlaps_two_real_explicit_list_creations_and_restorations() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        '_LABELS = ("a", "b")',
        "original_popen = subprocess.Popen",
        "both_marked = threading.Event()",
        "both_created = threading.Event()",
        "permit_launch_return = threading.Event()",
        "both_restoring = threading.Event()",
        "permit_restore = threading.Event()",
        "original_set_handle_inheritable(handle, True)",
        "marked_handles == set(handles.values())",
        'assert set(handle_list) == {"handle_list"}',
        "assert len(listed_handles) == 1",
        "process = original_popen(",
        "created_handles == set(handles.values())",
        "permit_launch_return.wait(timeout=_TIMEOUT_SECONDS)",
        "restoring_handles == set(handles.values())",
        "permit_restore.wait(timeout=_TIMEOUT_SECONDS)",
        "original_set_handle_inheritable(handle, False)",
        'monkeypatch.setattr(\n            inherited_probe,\n            "os",',
        'monkeypatch.setattr(\n            inherited_probe,\n            "subprocess",',
        "assert both_marked.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_created.wait(timeout=_TIMEOUT_SECONDS)",
        "assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)",
    ):
        assert required in probe

    marked_index = probe.index("assert both_marked.wait(timeout=_TIMEOUT_SECONDS)")
    created_index = probe.index("assert both_created.wait(timeout=_TIMEOUT_SECONDS)")
    release_launch_index = probe.index("permit_launch_return.set()", created_index)
    restoring_index = probe.index("assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)")
    release_restore_index = probe.index("permit_restore.set()", restoring_index)
    join_index = probe.index("thread.join(timeout=_TIMEOUT_SECONDS)", release_restore_index)
    assert (
        marked_index
        < created_index
        < release_launch_index
        < restoring_index
        < release_restore_index
        < join_index
    )
    assert probe.count("original_get_handle_inheritable(handle) for handle") == 3


def test_m167_uses_only_explicit_lists_and_fixed_local_children() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "close_fds is True",
        "shell is False",
        "cwd == roots[label]",
        "stdin == subprocess.PIPE",
        "stdout == subprocess.PIPE",
        "stderr == subprocess.PIPE",
        "inherited_probe._spawn_inherited_blocker(",
        "handles[label]",
        "roots[label]",
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
    assert probe.count("inherited_probe._spawn_inherited_blocker(") == 1


def test_m167_proves_pairwise_isolation_in_both_release_orders() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        '@pytest.mark.parametrize("release_order"',
        "((_LABELS[0], _LABELS[1]), (_LABELS[1], _LABELS[0]))",
        "first, second = release_order",
        "_release_inherited_blocker(processes[first])",
        "_attempt_native_child_rename(roots[first])",
        "assert _denied_rename(roots[second]) == denied",
        "assert live_paths[second].is_dir()",
        "_release_inherited_blocker(processes[second])",
        "_attempt_native_child_rename(roots[second])",
        'displaced_paths[label] / "candidate.bin"',
    ):
        assert required in probe
    first_release = probe.index("_release_inherited_blocker(processes[first])")
    first_success = probe.index("_attempt_native_child_rename(roots[first])", first_release)
    second_denial = probe.index("_denied_rename(roots[second])", first_success)
    second_release = probe.index("_release_inherited_blocker(processes[second])", second_denial)
    second_success = probe.index("_attempt_native_child_rename(roots[second])", second_release)
    assert first_release < first_success < second_denial < second_release < second_success


def test_m167_cleanup_retains_every_parent_child_and_thread_owner() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "created_processes[label] = process",
        "finally:",
        "both_marked.set()",
        "permit_launch_return.set()",
        "both_restoring.set()",
        "permit_restore.set()",
        "processes.setdefault(label, process)",
        "original_get_handle_inheritable(handle)",
        "original_set_handle_inheritable(handle, False)",
        "blocker_probe.release(handle)",
        "_close_child(process)",
        "assert blocker_probe.owned_count == 0",
        "assert all(not thread.is_alive() for thread in threads.values())",
        "assert set(processes) == set(_LABELS)",
        "assert process.returncode == 0",
        "assert stream is not None and stream.closed",
    ):
        assert required in probe
    creation_index = probe.index("created_processes[label] = process")
    wait_index = probe.index("permit_launch_return.wait(", creation_index)
    finally_index = probe.index("finally:", probe.index("processes: dict"))
    capture_index = probe.index("processes.setdefault(label, process)", finally_index)
    repair_index = probe.index("original_set_handle_inheritable(handle, False)", capture_index)
    release_index = probe.index("blocker_probe.release(handle)", repair_index)
    close_index = probe.index("_close_child(process)", release_index)
    assert creation_index < wait_index < finally_index < capture_index
    assert capture_index < repair_index < release_index < close_index


def test_m167_rfc_and_public_boundary_are_registered() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "pairwise isolation",
        "not a concurrency-safe process-creation contract",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0150-probe-windows-concurrent-explicit-inheritance.md").read_text(
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
        assert "cache-cleanup-windows-concurrent-explicit-inheritance-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0150-probe-windows-concurrent-explicit-inheritance.md" in rfc_index
