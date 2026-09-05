"""Protect M175's Windows live coordination-substitution boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0157-probe-windows-cooperative-lock-substitution.md": (
        "eeffe686df689ac9234c77bc4bf9860094d2a8db6bb270fe041b3f651ca4bb77"
    ),
    "docs/security/cache-cleanup-windows-cooperative-lock-substitution-probe.md": (
        "8d681d4f6d9c7dfa545d247beeccee904b4658945133eef884343bcfb1f56a01"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m174_windows_cooperative_lock_substitution.py": (
        "913de141b81fc6db5feab1c3744615bfca9e86bd38a79ecd9918995734958e27"
    ),
    "tests/fixtures/windows_coordination_lock_substitution_child.py": (
        "2aa89b4c4947eb7c84e478e4f1fd2ce498405e7b78262722b53796bffd01eee8"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_substitution_probe.py": (
        "e2f926d122bae494f94b9636178cc4664ca70080474e259b9d6a75822b5e2f61"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_PROBE = (
    _ROOT / "tests/integration/"
    "test_windows_cache_cleanup_cooperative_lock_live_substitution_exclusion_probe.py"
)
_CHILD = _ROOT / "tests/fixtures/windows_coordination_lock_protected_participant_child.py"


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


def test_m175_changes_no_runtime_dependency_ci_or_m174_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m175_child_owns_fixed_shared_lock_without_delete_sharing() -> None:
    child = _CHILD.read_text(encoding="utf-8")
    for required in (
        '_SCHEMA = "ludoweave.test.windows-coordination-lock-participant/1"',
        '_FILE_NAME = r"live\\coordination.lock"',
        "_GENERIC_READ = 0x80000000",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE,",
        "os.get_handle_inheritable(handle)",
        "lock_file_ex(",
        "_LOCKFILE_FAIL_IMMEDIATELY,",
        "unlock_file_ex(",
        '_emit("ready")',
        '_emit("closed")',
    ):
        assert required in child
    for forbidden in (
        "_FILE_SHARE_DELETE",
        "sys.argv",
        "input(",
        "os.environ",
        "subprocess",
        "pathlib",
        "Path(",
    ):
        assert forbidden not in child


def test_m175_probe_preserves_both_refusals_until_last_close() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_live_protected_participants_exclude_substitution_until_last_close")
    first = probe.index("first = _start_protected_participant(tmp_path)", test)
    second = probe.index("second = _start_protected_participant(tmp_path)", first)
    first_ready = probe.index('_read_event(first) == ("ready", 0)', second)
    second_ready = probe.index('_read_event(second) == ("ready", 0)', first_ready)
    both_substitution = probe.index("_attempt_substitution(tmp_path)", second_ready)
    both_exclusive = probe.index(
        "lock_probe.acquire_exclusive(coordination_path)", both_substitution
    )
    first_close = probe.index("_release_and_read_closed(first)", both_exclusive)
    one_substitution = probe.index("_attempt_substitution(tmp_path)", first_close)
    one_exclusive = probe.index("lock_probe.acquire_exclusive(coordination_path)", one_substitution)
    second_close = probe.index("_release_and_read_closed(second)", one_exclusive)
    exclusive = probe.index(
        "exclusive = lock_probe.acquire_exclusive(coordination_path)", second_close
    )
    substituted = probe.index("_attempt_substitution(tmp_path)", exclusive)
    identity = probe.index("identity_probe.identity(displaced) == original_identity", substituted)
    assert (
        test
        < first
        < second
        < first_ready
        < second_ready
        < both_substitution
        < both_exclusive
        < first_close
        < one_substitution
        < one_exclusive
        < second_close
        < exclusive
        < substituted
        < identity
    )
    assert probe.count('phase="rename_failed"') == 2
    assert probe.count("error_code=_ERROR_SHARING_VIOLATION") == 2


def test_m175_processes_and_cleanup_are_bounded_without_timing_or_shells() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "first: subprocess.Popen[bytes] | None = None",
        "second: subprocess.Popen[bytes] | None = None",
        "try:\n        first = _start_protected_participant(tmp_path)",
        "close_fds=True",
        "shell=False",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "finally:",
        "if first is not None:",
        "_close_participant(first)",
        "if second is not None:",
        "_close_participant(second)",
        "lock_probe.owned_count == 0",
    ):
        assert required in probe
    for forbidden in (
        "close_fds=False",
        "shell=True",
        "os.system",
        "time.sleep",
        '"-c"',
        "env=",
        "cmd.exe",
    ):
        assert forbidden not in probe


def test_m175_decision_records_live_only_not_authoritative_boundary() -> None:
    decision = (
        _ROOT / "docs/security/"
        "cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "continuous live-ownership interval",
        "not cleanup authority",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT / "docs/rfcs/0158-probe-windows-live-coordination-substitution-exclusion.md"
    ).read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "zero-participant window" in " ".join(rfc.casefold().split())
    assert "native error 32" in " ".join(rfc.casefold().split())


def test_m175_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe"
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
        assert slug in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0158-probe-windows-live-coordination-substitution-exclusion.md" in rfc_index
