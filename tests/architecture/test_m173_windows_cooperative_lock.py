"""Protect M173's Windows cooperative shared/exclusive lock boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0155-probe-windows-descendant-non-exclusion.md": (
        "57237fac9b93178ca9cff05f133083a80f9218cd1410afb8da202fe2fa76d930"
    ),
    "docs/security/cache-cleanup-windows-descendant-non-exclusion-probe.md": (
        "7469550745044d9a11e4fad4f81809e022bd9e10417de4733eb045c0bc027753"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m172_windows_descendant_non_exclusion.py": (
        "a407e869a58c0813858dee7040532ecfd2fcaea36bedc06015ecae1bea77c830"
    ),
    "tests/fixtures/windows_descendant_file_holder_child.py": (
        "b0f2424104432eecac2cbfcb97ad61bf15f44c614367210733259d0179a6b091"
    ),
    "tests/integration/test_windows_cache_cleanup_descendant_non_exclusion_probe.py": (
        "f752e145527f1d197d6d6f357398001547928f62b3e2901e73f91e4e268462c9"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_PROBE = _ROOT / "tests/integration/test_windows_cache_cleanup_cooperative_lock_probe.py"
_CHILD = _ROOT / "tests/fixtures/windows_coordination_lock_participant_child.py"


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


def test_m173_changes_no_runtime_dependency_ci_or_m172_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m173_child_owns_one_fixed_shared_noninheritable_lock() -> None:
    child = _CHILD.read_text(encoding="utf-8")
    for required in (
        '_SCHEMA = "ludoweave.test.windows-coordination-lock-participant/1"',
        '_FILE_NAME = r"live\\coordination.lock"',
        "_GENERIC_READ = 0x80000000",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE",
        "os.get_handle_inheritable(handle)",
        "lock_file_ex(",
        "_LOCKFILE_FAIL_IMMEDIATELY,",
        "ctypes.byref(overlapped)",
        "unlock_file_ex(",
        '_emit("ready")',
        '_emit("refused", error_code=error_code)',
        '_emit("closed")',
    ):
        assert required in child
    lock_call = child.index("        lock_file_ex(")
    lock_end = child.index("        ),", lock_call)
    assert "_LOCKFILE_EXCLUSIVE_LOCK" not in child[lock_call:lock_end]
    for forbidden in ("sys.argv", "input(", "subprocess", "os.environ", "pathlib", "Path("):
        assert forbidden not in child


def test_m173_parent_owns_one_fail_immediate_exclusive_range() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    acquire = probe.index("def acquire_exclusive")
    lock = probe.index("self._lock_file_ex(", acquire)
    exclusive = probe.index("_LOCKFILE_FAIL_IMMEDIATELY | _LOCKFILE_EXCLUSIVE_LOCK", lock)
    one_byte = probe.index("                    1,", exclusive)
    adopt = probe.index("self._exclusive[handle] = overlapped", one_byte)
    release = probe.index("def release_exclusive", adopt)
    unlock = probe.index("self._unlock_file_ex(", release)
    close = probe.index("self._close_owned(handle)", unlock)
    assert acquire < lock < exclusive < one_byte < adopt < release < unlock < close
    assert "self._reject_reparse(handle)" in probe[acquire:release]


def test_m173_two_shared_participants_hold_barrier_until_last_close() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index(
        "def test_shared_participants_collectively_refuse_exclusive_until_last_close"
    )
    first = probe.index("first = _start_participant(tmp_path)", test)
    second = probe.index("second = _start_participant(tmp_path)", first)
    first_ready = probe.index('_read_event(first) == ("ready", 0)', second)
    second_ready = probe.index('_read_event(second) == ("ready", 0)', first_ready)
    both_refuse = probe.index("probe.acquire_exclusive(coordination_path)", second_ready)
    first_close = probe.index("_release_and_read_closed(first)", both_refuse)
    one_refuses = probe.index("probe.acquire_exclusive(coordination_path)", first_close)
    second_close = probe.index("_release_and_read_closed(second)", one_refuses)
    acquired = probe.index("exclusive = probe.acquire_exclusive(coordination_path)", second_close)
    assert (
        test
        < first
        < second
        < first_ready
        < second_ready
        < both_refuse
        < first_close
        < one_refuses
        < second_close
        < acquired
    )


def test_m173_exclusive_holder_refuses_late_shared_participant() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_exclusive_refuses_late_participant_until_release")
    exclusive = probe.index("exclusive = probe.acquire_exclusive(coordination_path)", test)
    denied = probe.index("denied = _start_participant(tmp_path)", exclusive)
    refused = probe.index('_read_refused(denied) == ("refused", _ERROR_LOCK_VIOLATION)', denied)
    release = probe.index("probe.release_exclusive(exclusive)", refused)
    admitted = probe.index("admitted = _start_participant(tmp_path)", release)
    ready = probe.index('_read_event(admitted) == ("ready", 0)', admitted)
    closed = probe.index("_release_and_read_closed(admitted)", ready)
    assert test < exclusive < denied < refused < release < admitted < ready < closed


def test_m173_processes_and_cleanup_are_bounded_without_timing_or_shells() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "close_fds=True",
        "shell=False",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "timeout=_TIMEOUT_SECONDS",
        "finally:",
        "_close_participant(first)",
        "_close_participant(second)",
        "probe.owned_count == 0",
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
        "cmd.exe",
    ):
        assert forbidden not in probe


def test_m173_decision_records_cooperative_not_authoritative_boundary() -> None:
    decision = (_ROOT / "docs/security/cache-cleanup-windows-cooperative-lock-probe.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "cooperative",
        "not cleanup authority",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0156-probe-windows-cooperative-lock.md").read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "multiple shared participants" in " ".join(rfc.casefold().split())
    assert "uncooperative" in " ".join(rfc.casefold().split())


def test_m173_public_boundary_is_registered_without_ci_expansion() -> None:
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
        assert "cache-cleanup-windows-cooperative-lock-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0156-probe-windows-cooperative-lock.md" in rfc_index
