"""Protect M179's Windows overlapping-guardian rotation boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0161-probe-windows-guardian-abrupt-handoff.md": (
        "39f9da2f2672528e9d56913d658ee98d7042bfc93fd6863b960effb339c16460"
    ),
    "docs/security/cache-cleanup-windows-guardian-abrupt-handoff-probe.md": (
        "517af51a6a8ae41ae7362faadaaefeb4fba35245d460fcc805e3b038109f4d70"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m178_windows_guardian_abrupt_handoff.py": (
        "fad3a3d4d59efcedf9c95d2472dd5a33a6264a9afdd6f516932a7aac17c7be89"
    ),
    "tests/fixtures/windows_coordination_guardian_child.py": (
        "89f0b520c1e8966a5b577f63b254385a61c23c2427fb39b4911680b4fe5549d9"
    ),
    "tests/integration/test_windows_cache_cleanup_guardian_abrupt_handoff_probe.py": (
        "6ffe2f776f58c3f2f4b4b180fb0f7a106f8b5d11577b9afcf17c8969003ec9f1"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_PROBE = (
    _ROOT / "tests/integration/test_windows_cache_cleanup_overlapping_guardian_rotation_probe.py"
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


def test_m179_changes_no_runtime_dependency_ci_or_m178_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m179_reuses_fixed_guardian_participant_and_bounded_wait() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_start_guardian",
        "_read_guardian_event",
        "_release_guardian",
        "_start_protected_participant",
        "_terminate_and_assert_abrupt",
        "_assert_substitution_refused",
        "_assert_exclusive_available",
        "_assert_exclusive_refused",
        "_release_and_read_closed",
    ):
        assert required in probe
    assert probe.count("_start_guardian(tmp_path)") == 2
    assert "subprocess.Popen(" not in probe


def test_m179_orders_overlap_abrupt_rotation_and_final_release() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_overlapping_guardian_rotation")
    original = probe.index("original_identity =", test)
    first_start = probe.index("first_guardian = _start_guardian", original)
    first_ready = probe.index('_read_guardian_event(first_guardian) == "ready"', first_start)
    participant_start = probe.index("participant = _start_protected_participant", first_ready)
    participant_ready = probe.index('_read_event(participant) == ("ready", 0)', participant_start)
    second_start = probe.index("second_guardian = _start_guardian", participant_ready)
    second_ready = probe.index('_read_guardian_event(second_guardian) == "ready"', second_start)
    overlap_identity = probe.index(
        "identity_probe.identity(after_second) == original_identity", second_ready
    )
    first_killed = probe.index("_terminate_and_assert_abrupt(first_guardian)", overlap_identity)
    survivor_identity = probe.index(
        "identity_probe.identity(after_first_loss) == original_identity", first_killed
    )
    participant_closed = probe.index("_release_and_read_closed(participant)", survivor_identity)
    guardian_only_identity = probe.index(
        "identity_probe.identity(guardian_only) == original_identity", participant_closed
    )
    guardian_only_substitution = probe.index("_assert_substitution_refused", guardian_only_identity)
    guardian_only_exclusive = probe.index("_assert_exclusive_available", guardian_only_substitution)
    second_closed = probe.index("_release_guardian(second_guardian)", guardian_only_exclusive)
    substituted = probe.index("_attempt_substitution(tmp_path)", second_closed)
    assert (
        test
        < original
        < first_start
        < first_ready
        < participant_start
        < participant_ready
        < second_start
        < second_ready
        < overlap_identity
        < first_killed
        < survivor_identity
        < participant_closed
        < guardian_only_identity
        < guardian_only_substitution
        < guardian_only_exclusive
        < second_closed
        < substituted
    )


def test_m179_cleanup_is_exact_and_has_no_retry_or_delay() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "first_guardian: subprocess.Popen[bytes] | None = None",
        "second_guardian: subprocess.Popen[bytes] | None = None",
        "participant: subprocess.Popen[bytes] | None = None",
        "for process in (first_guardian, second_guardian, participant):",
        "_close_participant(process)",
        "first_guardian.returncode != 0",
        "second_guardian.returncode == 0",
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


def test_m179_decision_records_rotation_not_restart_or_recovery() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-overlapping-guardian-rotation-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "overlapping rotation",
        "not guardian restart",
        "not crash recovery",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0162-probe-windows-overlapping-guardian-rotation.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "no retry or sleep" in " ".join(rfc.casefold().split())


def test_m179_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-overlapping-guardian-rotation-probe"
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
    assert "0162-probe-windows-overlapping-guardian-rotation.md" in rfc_index
