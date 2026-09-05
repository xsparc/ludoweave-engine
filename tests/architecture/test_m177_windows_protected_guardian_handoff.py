"""Protect M177's Windows coordination guardian-handoff boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0159-probe-windows-cooperative-lock-abrupt-settlement.md": (
        "88e78e97d531ecce1e61dccd1afeebad578abbad419c35d75e84167021da81d1"
    ),
    "docs/security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md": (
        "808dfe11cb3184eb2307ba3b7882ad11249012cba1abc1833ee28d338c05063d"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m176_windows_cooperative_lock_abrupt_settlement.py": (
        "9345d7f8b05b2f1da3dc24a34bd36a6be6902ee6078d45e70a6e91dde542d0b2"
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
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
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
