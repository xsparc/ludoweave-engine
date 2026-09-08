"""Protect M177's Windows coordination guardian-handoff boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "23f4cf86fdf46be2f56b38345f09bac61c7753ad15f05302874afb99d4a20394",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0159-probe-windows-cooperative-lock-abrupt-settlement.md": (
        "88e78e97d531ecce1e61dccd1afeebad578abbad419c35d75e84167021da81d1"
    ),
    "docs/security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md": (
        "808dfe11cb3184eb2307ba3b7882ad11249012cba1abc1833ee28d338c05063d"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m176_windows_cooperative_lock_abrupt_settlement.py": (
        "0d6efd7e6b42281680c0151c79e95d61bd49a460a5929706f379d77ce2c5aeed"
    ),
    "tests/fixtures/windows_coordination_lock_protected_participant_child.py": (
        "bad17ab99ac177ed90af258a27a48a9f5e35a693d65659c95963bced8a4e2ab6"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe.py": (
        "875d8ddd9c242cc7e0af2f5aabaf02d293ad6106309a3a1d6b2dce0a3c97f5ec"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_live_substitution_exclusion_probe.py": (
        "83bf090744744065af71a8c2f84f88dd3ce59725c930d0a922c42e23109595c3"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "8e8d3a618b8bb14c439d4c0809db345fe471dc7c07f1765b03c4bb507f8fc98a",
    "scripts": "8833e1120f60e74f4b5024ef6a6049821a72afef44c0143bab3f7bbd9298e247",
    "src/ludoweave": "1e7f21b3d5bb0a8021f47f9bf1089873a59cb3e798b02933569d3eee3c9a35c1",
}
_PROBE = _ROOT / "tests/integration/test_windows_cache_cleanup_protected_guardian_handoff_probe.py"


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


def test_m177_changes_no_runtime_dependency_ci_or_m176_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m177_reuses_the_fixed_m175_participant_without_a_new_fixture() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert "_start_protected_participant" in probe
    assert "windows_coordination_lock_protected_participant_child.py" not in probe
    assert "subprocess.Popen(" not in probe


def test_m177_orders_guardian_gap_join_and_handoff_exactly() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_guardian_bridges_participant_free_interval")
    guardian = probe.index("guardian = guardian_probe.acquire", test)
    guardian_substitution = probe.index("_assert_substitution_refused", guardian)
    guardian_exclusive = probe.index("_assert_exclusive_available", guardian_substitution)
    first_start = probe.index("first = _start_protected_participant", guardian_exclusive)
    first_ready = probe.index('_read_event(first) == ("ready", 0)', first_start)
    first_exclusive = probe.index("_assert_exclusive_refused", first_ready)
    first_closed = probe.index("_release_and_read_closed(first)", first_exclusive)
    gap_substitution = probe.index("_assert_substitution_refused", first_closed)
    gap_exclusive = probe.index("_assert_exclusive_available", gap_substitution)
    second_start = probe.index("second = _start_protected_participant", gap_exclusive)
    second_ready = probe.index('_read_event(second) == ("ready", 0)', second_start)
    joined_identity = probe.index(
        "identity_probe.identity(joined) == original_identity", second_ready
    )
    guardian_release = probe.index("guardian_probe.release(guardian)", joined_identity)
    handoff_substitution = probe.index("_assert_substitution_refused", guardian_release)
    handoff_exclusive = probe.index("_assert_exclusive_refused", handoff_substitution)
    second_closed = probe.index("_release_and_read_closed(second)", handoff_exclusive)
    final_exclusive = probe.index("_assert_exclusive_available", second_closed)
    substituted = probe.index("_attempt_substitution(tmp_path)", final_exclusive)
    assert (
        test
        < guardian
        < guardian_substitution
        < guardian_exclusive
        < first_start
        < first_ready
        < first_exclusive
        < first_closed
        < gap_substitution
        < gap_exclusive
        < second_start
        < second_ready
        < joined_identity
        < guardian_release
        < handoff_substitution
        < handoff_exclusive
        < second_closed
        < final_exclusive
        < substituted
    )


def test_m177_guardian_is_noninheritable_identity_only_and_cleanup_is_exact() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "class _ProtectedCoordinationGuardianProbe",
        "_GENERIC_READ",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE",
        "None,\n                _OPEN_EXISTING",
        "self._reject_reparse(handle)",
        "os.get_handle_inheritable(guardian) is False",
        "guardian_probe.identity(guardian) == original_identity",
        "guardian: int | None = None",
        "with identity_probe, guardian_probe, lock_probe:",
        "finally:",
        "guardian_probe.release(guardian)",
        "_close_participant(first)",
        "_close_participant(second)",
        "guardian_probe.owned_count == 0",
        "lock_probe.owned_count == 0",
        "stream.closed",
    ):
        assert required in probe
    for forbidden in (
        "_FILE_SHARE_DELETE",
        "LockFileEx",
        "time.sleep",
        "shell=True",
        "os.system",
        "env=",
        "communicate(",
        "if guardian is not None",
    ):
        assert forbidden not in probe


def test_m177_decision_records_bridge_not_generation_or_cleanup_authority() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-protected-guardian-handoff-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "participant-free interval",
        "does not own the byte range",
        "not generation authority",
        "not crash recovery",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0160-probe-windows-protected-guardian-handoff.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "no retry or sleep" in " ".join(rfc.casefold().split())


def test_m177_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-protected-guardian-handoff-probe"
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
    assert "0160-probe-windows-protected-guardian-handoff.md" in rfc_index
