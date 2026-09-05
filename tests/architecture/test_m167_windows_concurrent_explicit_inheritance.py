"""Protect M167's simultaneous explicit handle-list isolation boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0149-probe-windows-concurrent-inheritance-leak.md": (
        "b36d5f1a73913026933f02241769d2f1d3aeaa4d66ade95a34975007c081c2f6"
    ),
    "docs/security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md": (
        "f8b205bee1f634843b69c24997302dd10dc306eafb9d5d33b3ed0fa4e9e618ac"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m166_windows_concurrent_inheritance_leak.py": (
        "d101416ad3eec5ea15b75effa27a80b18227d313374a0598c8042d97683a0652"
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
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
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
