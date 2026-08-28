"""Protect M176's Windows cooperative-lock abrupt-settlement boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0158-probe-windows-live-coordination-substitution-exclusion.md": (
        "a0af5a6f1a8dec632424d371eed1747b545103a45de0252f484300f94991a64a"
    ),
    "docs/security/cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md": (
        "427f0dfd35c211ec213a271ace55514a3c2eae4dd998628c451b5c17c856c347"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m175_windows_live_substitution_exclusion.py": (
        "885de8a918043c467a887e75b68916d0266c7467c8e28d3ebe956eccdf1d488f"
    ),
    "tests/fixtures/windows_coordination_lock_protected_participant_child.py": (
        "bad17ab99ac177ed90af258a27a48a9f5e35a693d65659c95963bced8a4e2ab6"
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
_PROBE = (
    _ROOT / "tests/integration/"
    "test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe.py"
)


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


def test_m176_changes_no_runtime_dependency_ci_or_m175_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m176_reuses_the_fixed_m175_protected_participant() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert "_start_protected_participant" in probe
    assert "windows_coordination_lock_protected_participant_child.py" not in probe
    assert "subprocess.Popen(" not in probe


def test_m176_preserves_survivor_refusals_before_final_settlement() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_abrupt_participant_settlement_preserves_survivor")
    first_ready = probe.index('_read_event(first) == ("ready", 0)', test)
    second_ready = probe.index('_read_event(second) == ("ready", 0)', first_ready)
    both_substitution = probe.index("_attempt_substitution(tmp_path)", second_ready)
    both_exclusive = probe.index(
        "lock_probe.acquire_exclusive(coordination_path)", both_substitution
    )
    first_terminated = probe.index("_terminate_and_assert_abrupt(first)", both_exclusive)
    survivor_substitution = probe.index("_attempt_substitution(tmp_path)", first_terminated)
    survivor_exclusive = probe.index(
        "lock_probe.acquire_exclusive(coordination_path)", survivor_substitution
    )
    second_terminated = probe.index("_terminate_and_assert_abrupt(second)", survivor_exclusive)
    exclusive = probe.index(
        "exclusive = lock_probe.acquire_exclusive(coordination_path)", second_terminated
    )
    substituted = probe.index("_attempt_substitution(tmp_path)", exclusive)
    identity = probe.index("identity_probe.identity(displaced) == original_identity", substituted)
    assert (
        test
        < first_ready
        < second_ready
        < both_substitution
        < both_exclusive
        < first_terminated
        < survivor_substitution
        < survivor_exclusive
        < second_terminated
        < exclusive
        < substituted
        < identity
    )
    assert probe.count('phase="rename_failed"') == 2
    assert probe.count("error_code=_ERROR_SHARING_VIOLATION") == 2


def test_m176_abrupt_wait_and_cleanup_are_exact_and_bounded() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "process.kill()",
        "process.wait(timeout=_TIMEOUT_SECONDS)",
        "assert return_code != 0",
        'stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "first: subprocess.Popen[bytes] | None = None",
        "second: subprocess.Popen[bytes] | None = None",
        "finally:",
        "_close_participant(first)",
        "_close_participant(second)",
        "stream.closed",
    ):
        assert required in probe
    for forbidden in (
        "time.sleep",
        "shell=True",
        "os.system",
        "env=",
        "communicate(",
        "_release_and_read_closed",
    ):
        assert forbidden not in probe


def test_m176_decision_records_host_bounded_not_recovery_authority() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "not crash recovery",
        "release can be delayed",
        "zero-participant substitution window remains",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0159-probe-windows-cooperative-lock-abrupt-settlement.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "without retry or sleep" in " ".join(rfc.casefold().split())
    assert "native error 33" in " ".join(rfc.casefold().split())


def test_m176_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe"
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
    assert "0159-probe-windows-cooperative-lock-abrupt-settlement.md" in rfc_index
