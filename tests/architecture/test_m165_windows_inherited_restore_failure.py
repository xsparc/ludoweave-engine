"""Protect M165's test-only inherited-handle restore-failure boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0147-probe-windows-inherited-launch-failure.md": (
        "1fa757490cb122009b25a2f3c5e532b980782bf51fa99d4b5f39dbf9dd8f5aa0"
    ),
    "docs/security/cache-cleanup-windows-inherited-launch-failure-probe.md": (
        "b0e3217c35fbbe66461f721fbcc6f0988780716104fafbe4ac2fcc6d464f7c8e"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m164_windows_inherited_launch_failure.py": (
        "0992a1c0bb0da00d4b746be06c1f868af67efc83d3317951602091e4128703b3"
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


def test_m165_changes_no_runtime_example_script_dependency_ci_or_m164_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m165_injects_only_the_first_restore_after_real_child_creation() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_inherited_restore_failure_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "original_set_handle_inheritable = os.set_handle_inheritable",
        "def fail_first_restore(handle: int, inheritable: bool) -> None:",
        "and inheritable is False",
        "and restore_attempts == 0",
        "restore_attempts += 1",
        "raise injected",
        'monkeypatch.setattr(inherited_probe, "_close_child", capture_close)',
        "returned_process = inherited_probe._spawn_inherited_blocker(",
        "except _InjectedRestoreFailure as candidate:",
        "assert returned_process is None",
        "assert caught is injected",
        "assert restore_attempts == 1",
    ):
        assert required in probe
    inject_index = probe.index("def fail_first_restore(")
    spawn_index = probe.index("returned_process = inherited_probe._spawn_inherited_blocker(")
    caught_index = probe.index("assert caught is injected")
    assert inject_index < spawn_index < caught_index
    assert "time.sleep" not in probe
    assert "communicate(" not in probe
    assert '"-c"' not in probe
    assert "env=" not in probe


def test_m165_requires_child_reap_before_explicit_parent_repair() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_inherited_restore_failure_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "closed_processes.append(process)",
        "preclose_returncodes.append(process.poll())",
        "original_close_child(process)",
        "assert len(closed_processes) == 1",
        "assert preclose_returncodes == [None]",
        "assert closed_process.returncode is not None",
        "assert stream is not None and stream.closed",
        "assert os.get_handle_inheritable(blocker_handle) is True",
        "original_set_handle_inheritable(blocker_handle, False)",
        "assert os.get_handle_inheritable(blocker_handle) is False",
    ):
        assert required in probe
    reaped_index = probe.index("assert closed_process.returncode is not None")
    inherited_index = probe.index("assert os.get_handle_inheritable(blocker_handle) is True")
    repair_index = probe.index("original_set_handle_inheritable(blocker_handle, False)")
    repaired_index = probe.index("assert os.get_handle_inheritable(blocker_handle) is False")
    assert reaped_index < inherited_index < repair_index < repaired_index


def test_m165_orders_parent_denial_before_release_and_success() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_inherited_restore_failure_probe.py"
    ).read_text(encoding="utf-8")
    rename_call = "_attempt_native_child_rename(tmp_path)"
    repaired_index = probe.index("assert os.get_handle_inheritable(blocker_handle) is False")
    first_rename_index = probe.index(rename_call)
    release_index = probe.index("blocker_probe.release(blocker_handle)")
    second_rename_index = probe.index(rename_call, first_rename_index + len(rename_call))
    assert repaired_index < first_rename_index < release_index < second_rename_index
    assert probe.count(rename_call) == 2
    assert "succeeded=False" in probe
    assert "succeeded=True" in probe


def test_m165_documents_narrow_injected_failure_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-inherited-restore-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "injected restoration failure",
        "not a real native restoration failure",
        "not a concurrency-safe inheritance contract",
        "no hosted check is added",
    ):
        assert required in compact


def test_m165_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0148-probe-windows-inherited-restore-failure.md").read_text(
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
        assert "cache-cleanup-windows-inherited-restore-failure-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0148-probe-windows-inherited-restore-failure.md" in rfc_index
