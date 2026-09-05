"""Protect M178's Windows guardian abrupt-handoff boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0160-probe-windows-protected-guardian-handoff.md": (
        "8a6ee63d88020bc7481e0d91421af5602ee6ead9f182bd55db00cd27c924fcbe"
    ),
    "docs/security/cache-cleanup-windows-protected-guardian-handoff-probe.md": (
        "7dfe7a33892a68a8b79666a4eec9bd23a89a1a2bddbd2323056cfaf6240ab131"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m177_windows_protected_guardian_handoff.py": (
        "8719b5f3775206a19d867e4026fa9e03974af513b982edf00db143b5c8e5c4a2"
    ),
    "tests/fixtures/windows_coordination_lock_protected_participant_child.py": (
        "bad17ab99ac177ed90af258a27a48a9f5e35a693d65659c95963bced8a4e2ab6"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe.py": (
        "875d8ddd9c242cc7e0af2f5aabaf02d293ad6106309a3a1d6b2dce0a3c97f5ec"
    ),
    "tests/integration/test_windows_cache_cleanup_protected_guardian_handoff_probe.py": (
        "5f570f9e57de824cf0f08ec0694b539e4b435262b462504894394187ed3c3d18"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_FIXTURE = _ROOT / "tests/fixtures/windows_coordination_guardian_child.py"
_PROBE = _ROOT / "tests/integration/test_windows_cache_cleanup_guardian_abrupt_handoff_probe.py"


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


def test_m178_changes_no_runtime_dependency_ci_or_m177_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m178_guardian_fixture_is_fixed_noninheritable_and_nonlocking() -> None:
    fixture = _FIXTURE.read_text(encoding="utf-8")
    for required in (
        'r"live\\coordination.lock"',
        '"ludoweave.test.windows-coordination-guardian/1"',
        "_GENERIC_READ",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE",
        "None,\n        _OPEN_EXISTING",
        "_FILE_ATTRIBUTE_NORMAL | _FILE_FLAG_OPEN_REPARSE_POINT",
        "_FILE_FLAG_OPEN_REPARSE_POINT",
        "_FILE_ATTRIBUTE_REPARSE_POINT",
        "os.get_handle_inheritable(handle)",
        "GetFileInformationByHandleEx",
        '_emit("ready")',
        '_emit("closed")',
    ):
        assert required in fixture
    for forbidden in (
        "LockFileEx",
        "_FILE_SHARE_DELETE",
        "sys.argv",
        "os.environ",
        "getenv(",
        "time.sleep",
        "shell=True",
    ):
        assert forbidden not in fixture


def test_m178_reuses_fixed_participant_and_bounded_abrupt_wait() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "windows_coordination_guardian_child.py",
        "_start_protected_participant",
        "_terminate_and_assert_abrupt",
        "_assert_substitution_refused",
        "_assert_exclusive_available",
        "_assert_exclusive_refused",
        "_release_and_read_closed",
        "_release_guardian",
        "close_fds=True",
        "shell=False",
    ):
        assert required in probe
    assert probe.count("subprocess.Popen(") == 1


def test_m178_orders_guardian_join_abrupt_handoff_and_final_settlement() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_abrupt_guardian_settlement")
    original = probe.index("original_identity =", test)
    guardian_start = probe.index("guardian = _start_guardian", original)
    guardian_ready = probe.index('_read_guardian_event(guardian) == "ready"', guardian_start)
    guardian_substitution = probe.index("_assert_substitution_refused", guardian_ready)
    guardian_exclusive = probe.index("_assert_exclusive_available", guardian_substitution)
    participant_start = probe.index(
        "participant = _start_protected_participant", guardian_exclusive
    )
    participant_ready = probe.index('_read_event(participant) == ("ready", 0)', participant_start)
    joined_identity = probe.index(
        "identity_probe.identity(joined) == original_identity", participant_ready
    )
    both_substitution = probe.index("_assert_substitution_refused", joined_identity)
    both_exclusive = probe.index("_assert_exclusive_refused", both_substitution)
    guardian_killed = probe.index("_terminate_and_assert_abrupt", both_exclusive)
    survivor_live = probe.index("participant.poll() is None", guardian_killed)
    retained_identity = probe.index(
        "identity_probe.identity(retained) == original_identity", survivor_live
    )
    survivor_substitution = probe.index("_assert_substitution_refused", retained_identity)
    survivor_exclusive = probe.index("_assert_exclusive_refused", survivor_substitution)
    participant_closed = probe.index("_release_and_read_closed(participant)", survivor_exclusive)
    final_exclusive = probe.index("_assert_exclusive_available", participant_closed)
    substituted = probe.index("_attempt_substitution(tmp_path)", final_exclusive)
    assert (
        test
        < original
        < guardian_start
        < guardian_ready
        < guardian_substitution
        < guardian_exclusive
        < participant_start
        < participant_ready
        < joined_identity
        < both_substitution
        < both_exclusive
        < guardian_killed
        < survivor_live
        < retained_identity
        < survivor_substitution
        < survivor_exclusive
        < participant_closed
        < final_exclusive
        < substituted
    )


def test_m178_cleanup_is_exact_and_has_no_retry_or_delay() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "guardian: subprocess.Popen[bytes] | None = None",
        "participant: subprocess.Popen[bytes] | None = None",
        "finally:",
        "_close_participant(guardian)",
        "_close_participant(participant)",
        "guardian.returncode != 0",
        "participant.returncode == 0",
        "stream.closed",
        "lock_probe.owned_count == 0",
    ):
        assert required in probe
    for forbidden in (
        "time.sleep",
        "retry",
        "communicate(",
        "env=",
        "os.system",
        "shell=True",
    ):
        assert forbidden not in probe


def test_m178_decision_records_failure_observation_not_recovery_authority() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-guardian-abrupt-handoff-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "after bounded process wait",
        "not crash recovery",
        "not generation authority",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0161-probe-windows-guardian-abrupt-handoff.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "no retry or sleep" in " ".join(rfc.casefold().split())


def test_m178_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-guardian-abrupt-handoff-probe"
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
    assert "0161-probe-windows-guardian-abrupt-handoff.md" in rfc_index
