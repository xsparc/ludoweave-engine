"""Protect M166's test-only controlled concurrent inheritance-leak boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0148-probe-windows-inherited-restore-failure.md": (
        "7e2dd3e07178e91dd6390632e2cc854b2ee7d0e718afd7d2991b95fc6259f10d"
    ),
    "docs/security/cache-cleanup-windows-inherited-restore-failure-probe.md": (
        "95dea2d60de0726f69ee1ac63a05be63083df50e9e79f295b220c3a5375f25af"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m165_windows_inherited_restore_failure.py": (
        "7434a108068501e74ea781d4526a0a8336a6554a5ac3017792c5bc309f692739"
    ),
    "tests/fixtures/windows_share_delete_inherited_blocker_child.py": (
        "2c695324c4f7fecbbe98b71a540a1b4000f0361e55ab6f469c52ccb8b4110a4c"
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


def test_m166_changes_no_runtime_helper_fixture_dependency_ci_or_m165_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m166_pauses_only_the_explicit_launch_before_one_broad_launch() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_concurrent_inheritance_leak_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "original_popen = subprocess.Popen",
        "explicit_launch_waiting = threading.Event()",
        "permit_explicit_launch = threading.Event()",
        "def pause_explicit_launch(",
        'startupinfo.lpAttributeList == {"handle_list": [blocker_handle]}',
        "explicit_launch_waiting.set()",
        "permit_explicit_launch.wait(timeout=_TIMEOUT_SECONDS)",
        'monkeypatch.setattr(\n            inherited_probe,\n            "subprocess",',
        "SimpleNamespace(",
        "explicit_thread = threading.Thread(target=spawn_explicit_child, daemon=True)",
        "assert explicit_launch_waiting.wait(timeout=_TIMEOUT_SECONDS)",
        "assert os.get_handle_inheritable(blocker_handle) is True",
        "broad_process = original_popen(",
        "close_fds=False",
        "executable=sys.executable",
        'assert inherited_probe._read_phase(broad_process) == "ready"',
        "permit_explicit_launch.set()",
        "assert os.get_handle_inheritable(blocker_handle) is False",
    ):
        assert required in probe
    wait_index = probe.index("assert explicit_launch_waiting.wait(")
    inheritable_index = probe.index("assert os.get_handle_inheritable(blocker_handle) is True")
    broad_index = probe.index("broad_process = original_popen(")
    broad_ready_index = probe.index('assert inherited_probe._read_phase(broad_process) == "ready"')
    release_index = probe.index("permit_explicit_launch.set()", broad_ready_index)
    join_index = probe.index("explicit_thread.join(", release_index)
    restored_index = probe.index("assert os.get_handle_inheritable(blocker_handle) is False")
    assert (
        wait_index
        < inheritable_index
        < broad_index
        < broad_ready_index
        < release_index
        < join_index
        < restored_index
    )
    assert "monkeypatch.setattr(inherited_probe.subprocess" not in probe
    assert "time.sleep" not in probe
    assert "os.system" not in probe
    assert "communicate(" not in probe
    assert '"-c"' not in probe
    assert "shell=True" not in probe
    assert "env=" not in probe


def test_m166_orders_broad_child_as_the_final_blocker_owner() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_concurrent_inheritance_leak_probe.py"
    ).read_text(encoding="utf-8")
    rename_call = "_attempt_native_child_rename(tmp_path)"
    first_rename_index = probe.index(rename_call)
    parent_release_index = probe.index("blocker_probe.release(blocker_handle)")
    second_rename_index = probe.index(rename_call, first_rename_index + len(rename_call))
    explicit_release_index = probe.index("_release_inherited_blocker(explicit_process)")
    third_rename_index = probe.index(rename_call, second_rename_index + len(rename_call))
    broad_live_index = probe.index("assert broad_process.poll() is None", third_rename_index)
    broad_release_index = probe.index("_release_inherited_blocker(broad_process)")
    fourth_rename_index = probe.index(rename_call, third_rename_index + len(rename_call))
    assert (
        first_rename_index
        < parent_release_index
        < second_rename_index
        < explicit_release_index
        < third_rename_index
        < broad_live_index
        < broad_release_index
        < fourth_rename_index
    )
    assert probe.count(rename_call) == 4
    assert probe.count("succeeded=False") == 3
    assert probe.count("succeeded=True") == 1
    assert "assert blocker_probe.owned_count == 0" in probe
    assert "assert displaced_candidate.read_bytes()" in probe


def test_m166_failure_cleanup_recovers_queued_child_ownership() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_concurrent_inheritance_leak_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "finally:",
        "permit_explicit_launch.set()",
        "explicit_thread.join(timeout=_TIMEOUT_SECONDS)",
        "if explicit_process is None:",
        "pending_result = explicit_results.get_nowait()",
        "if not isinstance(pending_result, BaseException):",
        "explicit_process = pending_result",
        "if not parent_released and os.get_handle_inheritable(blocker_handle):",
        "original_set_handle_inheritable(blocker_handle, False)",
        "for process in (explicit_process, broad_process):",
        "_close_child(process)",
        "assert not explicit_thread.is_alive()",
        "assert process.returncode == 0",
        "assert stream is not None and stream.closed",
    ):
        assert required in probe
    finally_index = probe.index("finally:", probe.index("explicit_thread.start()"))
    gate_index = probe.index("permit_explicit_launch.set()", finally_index)
    join_index = probe.index("explicit_thread.join(", gate_index)
    drain_index = probe.index("pending_result = explicit_results.get_nowait()", join_index)
    repair_index = probe.index("original_set_handle_inheritable(", drain_index)
    close_index = probe.index("_close_child(process)", repair_index)
    settled_index = probe.index("assert not explicit_thread.is_alive()", close_index)
    assert finally_index < gate_index < join_index < drain_index < repair_index < close_index
    assert close_index < settled_index


def test_m166_documents_a_hazard_not_a_concurrency_solution() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "real current-host hazard",
        "not a concurrency solution",
        "not a safe concurrency contract",
        "no hosted check is added",
    ):
        assert required in compact


def test_m166_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0149-probe-windows-concurrent-inheritance-leak.md").read_text(
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
        assert "cache-cleanup-windows-concurrent-inheritance-leak-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0149-probe-windows-concurrent-inheritance-leak.md" in rfc_index
