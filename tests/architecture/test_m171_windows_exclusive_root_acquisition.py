"""Protect M171's Windows exclusive-root acquisition boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0136-probe-windows-share-delete-exclusion.md": (
        "b9fcb48752dc51a66ef5b8c5245a39d7f03b4c858b685eb0b2e69ca8823a5975"
    ),
    "docs/rfcs/0153-probe-windows-concurrent-explicit-abrupt-termination.md": (
        "4da67685aeb4a13facb4ab9f9072e720821d8b87a21a120be5830465e5e931ba"
    ),
    "docs/security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md": (
        "c929fcc3161df0f861570bc7a5f5310437a5822ed10bb6f5fa4732e0412d87de"
    ),
    "docs/security/cache-cleanup-windows-share-delete-exclusion-probe.md": (
        "57aa6c26387ba3a1739bbe9499ec5640473218bc7830f51fd1c7cb0a71f92225"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m170_windows_concurrent_explicit_abrupt_termination.py": (
        "dbd62d05c1a4ceab679da36659e7cf36fd66267a456a286ecd60e9147a2b87c4"
    ),
    "tests/fixtures/windows_share_delete_blocker_child.py": (
        "be8da81a030f5de9490410e23d67147d777368f4b66e10cc580103add41b8f5d"
    ),
    "tests/integration/test_windows_cache_cleanup_capability_probe.py": (
        "151c2e0a102c622fdb66d4d78ee803564b26081a0da34b76341e86596e11d973"
    ),
    "tests/integration/test_windows_cache_cleanup_child_owned_blocker_probe.py": (
        "c5feb520a1a6b95f8f819e743f82327f9bd59d42c93b4e5189660d418def75f7"
    ),
    "tests/integration/test_windows_cache_cleanup_concurrent_explicit_abrupt_termination_probe.py": (
        "0522932ec82816302a49a4efa7a22ee31891c31d2e6ebc3fcce4a1430a92cfba"
    ),
    "tests/integration/test_windows_cache_cleanup_share_delete_probe.py": (
        "41877f26d92168b802c0b7d712b2fccb524fd9c3dcee913fc9e254921b8f440c"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_PROBE = _ROOT / "tests/integration/test_windows_cache_cleanup_exclusive_root_acquisition_probe.py"
_CHILD = _ROOT / "tests/fixtures/windows_exclusive_directory_open_child.py"


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


def test_m171_changes_no_runtime_helper_dependency_ci_or_m170_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m171_opens_one_owned_noninheritable_zero_sharing_directory() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "class _ExclusiveDirectoryProbe(_ShareDeleteProbe):",
        "def open_directory_exclusive(self, path: Path) -> int:",
        "_FILE_LIST_DIRECTORY | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE",
        "_FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT",
        '"CreateFileW(exclusive directory)"',
        "handle = self._adopt(result)",
        "self._reject_reparse(handle)",
        "self._close_owned(handle)",
        "os.get_handle_inheritable(exclusive) is False",
    ):
        assert required in probe
    create_call = probe.index("self._create_file(")
    zero_sharing = probe.index("                0,", create_call)
    null_security = probe.index("                None,", zero_sharing)
    assert create_call < zero_sharing < null_security
    assert probe.count("os.get_handle_inheritable(exclusive) is False") == 2


def test_m171_denies_late_child_then_releases_exact_owner() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    owner = probe.index("exclusive = probe.open_directory_exclusive(live_path)")
    denial = probe.index("assert _attempt_child_open(tmp_path) == _DirectoryOpenResult(", owner)
    error = probe.index("error_code=_ERROR_SHARING_VIOLATION", denial)
    release = probe.index("probe.release(exclusive)", error)
    success = probe.index("assert _attempt_child_open(tmp_path) == _DirectoryOpenResult(", release)
    assert owner < denial < error < release < success
    assert "succeeded=True" in probe[success:]
    assert "error_code=0" in probe[success:]
    assert 'candidate_path.read_bytes() == b"m171-exclusive-owner"' in probe


def test_m171_existing_child_forces_fail_closed_acquisition_before_release() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    start = probe.index("participant = _start_existing_participant(tmp_path)")
    ready = probe.index('_read_ready(participant) == "ready"', start)
    refusal = probe.index("denied_probe.open_directory_exclusive(live_path)", ready)
    exact_error = probe.index("raised.value.code == _ERROR_SHARING_VIOLATION", refusal)
    no_owner = probe.index("denied_probe.owned_count == 0", exact_error)
    live = probe.index("participant.poll() is None", no_owner)
    release = probe.index('_release_and_read_closed(participant) == "closed"', live)
    acquire = probe.index("acquired_probe.open_directory_exclusive(live_path)", release)
    assert start < ready < refusal < exact_error < no_owner < live < release < acquire
    assert "participant.returncode == 0" in probe[release:]
    assert 'candidate_path.read_bytes() == b"m171-existing-participant"' in probe


def test_m171_child_is_fixed_bounded_and_path_silent() -> None:
    child = _CHILD.read_text(encoding="utf-8")
    for required in (
        '_SCHEMA = "ludoweave.test.windows-directory-open/1"',
        '_DIRECTORY_NAME = "live"',
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE",
        "_FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT",
        "_emit(succeeded=False, error_code=get_last_error())",
        "close_handle(wintypes.HANDLE(handle))",
        "_emit(succeeded=True, error_code=0)",
    ):
        assert required in child
    for forbidden in ("sys.argv", "input(", "subprocess", "os.environ", "pathlib", "Path("):
        assert forbidden not in child


def test_m171_processes_and_cleanup_are_bounded_without_timing_or_shells() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "check=False",
        "capture_output=True",
        "close_fds=True",
        "shell=False",
        "stdin=subprocess.DEVNULL",
        "timeout=_TIMEOUT_SECONDS",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "finally:",
        "_close_child(participant)",
        "probe.owned_count == 0",
        "denied_probe.owned_count == 0",
        "acquired_probe.owned_count == 0",
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


def test_m171_rfc_and_public_boundary_are_registered() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-exclusive-root-acquisition-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "sharing mode zero",
        "not a complete cache quiescence capability",
        "not a lock api",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0154-probe-windows-exclusive-root-acquisition.md").read_text(
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
        assert "cache-cleanup-windows-exclusive-root-acquisition-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0154-probe-windows-exclusive-root-acquisition.md" in rfc_index
