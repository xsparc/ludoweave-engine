"""Protect M180's Windows zero-owner guardian restart boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0162-probe-windows-overlapping-guardian-rotation.md": (
        "0795dbbca5e413afa3f50cc76487eae7959e701ecd79192c10d8385f4ec2fc42"
    ),
    "docs/security/cache-cleanup-windows-overlapping-guardian-rotation-probe.md": (
        "9143d5054ed093d4df5ac80408d28f2c314799b4421d7b9b31b1cc785678f146"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m179_windows_overlapping_guardian_rotation.py": (
        "bd5f4adc69de01fbcf002d6672b5496efb1c09322dea678772d45ec7d0708b80"
    ),
    "tests/fixtures/windows_coordination_guardian_child.py": (
        "89f0b520c1e8966a5b577f63b254385a61c23c2427fb39b4911680b4fe5549d9"
    ),
    "tests/fixtures/windows_coordination_lock_substitution_child.py": (
        "2aa89b4c4947eb7c84e478e4f1fd2ce498405e7b78262722b53796bffd01eee8"
    ),
    "tests/integration/test_windows_cache_cleanup_capability_probe.py": (
        "151c2e0a102c622fdb66d4d78ee803564b26081a0da34b76341e86596e11d973"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe.py": (
        "875d8ddd9c242cc7e0af2f5aabaf02d293ad6106309a3a1d6b2dce0a3c97f5ec"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_probe.py": (
        "d0ea6af78537cd60d1e6da35e6d9db8f17416d93e9034e8f8d25f2c3b2a1c044"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_substitution_probe.py": (
        "e2f926d122bae494f94b9636178cc4664ca70080474e259b9d6a75822b5e2f61"
    ),
    "tests/integration/test_windows_cache_cleanup_guardian_abrupt_handoff_probe.py": (
        "6ffe2f776f58c3f2f4b4b180fb0f7a106f8b5d11577b9afcf17c8969003ec9f1"
    ),
    "tests/integration/test_windows_cache_cleanup_overlapping_guardian_rotation_probe.py": (
        "38a0719471e6688148f963accadf0c2c164b4ae2d718b7210bba6053dfab5cc3"
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
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_zero_owner_guardian_restart_boundary_probe.py"
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


def test_m180_changes_no_runtime_dependency_ci_or_m179_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m180_reuses_fixed_guardian_substitution_and_bounded_wait() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_start_guardian",
        "_read_guardian_event",
        "_release_guardian",
        "_terminate_and_assert_abrupt",
        "_attempt_substitution",
        "_assert_substitution_refused",
        "_assert_exclusive_available",
    ):
        assert required in probe
    assert probe.count("_start_guardian(tmp_path)") == 4
    assert "subprocess.Popen(" not in probe


def test_m180_orders_benign_post_wait_restart_and_final_substitution() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_benign_zero_owner_guardian_restart")
    original = probe.index("original_identity =", test)
    first_ready = probe.index('_read_guardian_event(first_guardian) == "ready"', original)
    first_killed = probe.index("_terminate_and_assert_abrupt(first_guardian)", first_ready)
    exposed_identity = probe.index(
        "identity_probe.identity(exposed) == original_identity", first_killed
    )
    exposed_range = probe.index("_assert_exclusive_available", exposed_identity)
    second_start = probe.index("second_guardian = _start_guardian", exposed_range)
    second_ready = probe.index('_read_guardian_event(second_guardian) == "ready"', second_start)
    restarted_identity = probe.index(
        "identity_probe.identity(restarted) == original_identity", second_ready
    )
    restarted_refusal = probe.index("_assert_substitution_refused", restarted_identity)
    second_closed = probe.index("_release_guardian(second_guardian)", restarted_refusal)
    substituted = probe.index("_attempt_substitution(tmp_path)", second_closed)
    assert (
        test
        < original
        < first_ready
        < first_killed
        < exposed_identity
        < exposed_range
        < second_start
        < second_ready
        < restarted_identity
        < restarted_refusal
        < second_closed
        < substituted
    )


def test_m180_orders_zero_owner_substitution_before_replacement_guardian() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_zero_owner_substitution_redirects")
    first_ready = probe.index('_read_guardian_event(first_guardian) == "ready"', test)
    first_killed = probe.index("_terminate_and_assert_abrupt(first_guardian)", first_ready)
    substituted = probe.index("_attempt_substitution(tmp_path)", first_killed)
    replacement_identity = probe.index("replacement_identity =", substituted)
    second_start = probe.index("second_guardian = _start_guardian", replacement_identity)
    second_ready = probe.index('_read_guardian_event(second_guardian) == "ready"', second_start)
    redirected = probe.index(
        "identity_probe.identity(restarted) == replacement_identity", second_ready
    )
    blocked_rename = probe.index("with pytest.raises(OSError) as blocked", redirected)
    sharing_violation = probe.index("blocked.value.winerror == 32", blocked_rename)
    range_available = probe.index("_assert_exclusive_available", sharing_violation)
    second_closed = probe.index("_release_guardian(second_guardian)", range_available)
    final_rename = probe.index("coordination_path.rename(second_displaced_path)", second_closed)
    moved_identity = probe.index(
        "identity_probe.identity(moved_replacement) == replacement_identity",
        final_rename,
    )
    assert (
        test
        < first_ready
        < first_killed
        < substituted
        < replacement_identity
        < second_start
        < second_ready
        < redirected
        < blocked_rename
        < sharing_violation
        < range_available
        < second_closed
        < final_rename
        < moved_identity
    )


def test_m180_cleanup_is_exact_and_has_no_retry_or_delay() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "for process in (first_guardian, second_guardian):",
        "_close_participant(process)",
        "first_guardian.returncode != 0",
        "second_guardian.returncode == 0",
        "stream.closed",
        "lock_probe.owned_count == 0",
        "assert not coordination_path.exists()",
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


def test_m180_decision_records_boundary_not_recovery_or_authority() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "zero-owner interval",
        "not crash recovery",
        "not generation authority",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT / "docs/rfcs/0163-probe-windows-zero-owner-guardian-restart-boundary.md"
    ).read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "no retry or sleep" in " ".join(rfc.casefold().split())


def test_m180_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe"
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
    assert "0163-probe-windows-zero-owner-guardian-restart-boundary.md" in rfc_index
