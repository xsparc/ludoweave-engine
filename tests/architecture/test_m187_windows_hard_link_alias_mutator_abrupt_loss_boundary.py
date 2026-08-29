"""Protect M187's Windows hard-link alias mutator abrupt-loss boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0169-probe-windows-independent-hard-link-alias-mutator-aba.md": (
        "4165080dddf304091f0e3fb23e457ef6f15281857cc10b374e167721422b3ac3"
    ),
    "docs/security/cache-cleanup-windows-independent-hard-link-alias-mutator-aba-probe.md": (
        "9a7987206c35435e4e9a8cbce3e98676c6472330a594944ec50d8e2db907b9fe"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m186_windows_independent_hard_link_alias_mutator_aba_boundary.py": (
        "c230ba596091b5d4faf4c9044259a1a9482508b58433101ae5b90c08cc3e1c00"
    ),
    "tests/fixtures/windows_hard_link_alias_mutator_child.py": (
        "19688156f08643aa31a05f53a8a6fc31ff1b60ec1f311e5c557d9fcd87ad2b0a"
    ),
    "tests/integration/test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe.py": (
        "0217545916b6e9f587f1c642296c10b6f539c83238cad8fe2c68ec379ecdc68f"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_abrupt_loss_probe.py"
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


def test_m187_changes_no_runtime_dependency_ci_fixture_or_m186_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m187_reuses_m186_child_and_existing_abrupt_settlement_helper() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "from test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe import (",
        "_read_alias_mutator_event",
        "_start_alias_mutator",
        "from test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe import (",
        "_terminate_and_assert_abrupt",
    ):
        assert required in probe
    for forbidden in (
        "subprocess.Popen(",
        "process.kill(",
        "_send_alias_mutator_token",
        "_RECREATE_TOKEN",
        "_close_alias_mutator",
    ):
        assert forbidden not in probe


def test_m187_orders_delete_abrupt_reap_guardian_release_and_rename() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    mutator_started = probe.index("mutator = _start_alias_mutator", guardian_ready)
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"', mutator_started)
    one_link_before_loss = probe.index("identity_probe.link_count(original) == 1", deleted)
    abrupt = probe.index(
        "mutator_return_code = _terminate_and_assert_abrupt(mutator)",
        one_link_before_loss,
    )
    reaped = probe.index("assert mutator.poll() == mutator_return_code", abrupt)
    one_link_after_loss = probe.index("identity_probe.link_count(original) == 1", reaped)
    blocked = probe.index("blocked_after_mutator_loss.value.winerror", one_link_after_loss)
    guardian_closed = probe.index('_release_identity_guardian(guardian) == "closed"', blocked)
    renamed = probe.index("coordination_path.rename(displaced_path)", guardian_closed)
    assert (
        guardian_ready
        < mutator_started
        < deleted
        < one_link_before_loss
        < abrupt
        < reaped
        < one_link_after_loss
        < blocked
        < guardian_closed
        < renamed
    )


def test_m187_never_recreates_alias_and_keeps_guardian_live_after_loss() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("os.link(coordination_path, alias_path)") == 1
    initial_link = probe.index("os.link(coordination_path, alias_path)")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    assert initial_link < guardian_ready
    abrupt = probe.index("mutator_return_code = _terminate_and_assert_abrupt(mutator)")
    after_abrupt = probe[abrupt:]
    assert "assert guardian.poll() is None" in after_abrupt
    assert "assert not alias_path.exists()" in after_abrupt
    for forbidden in ("os.link(", "_send_alias_mutator_token", 'b"+"'):
        assert forbidden not in after_abrupt


def test_m187_preserves_identity_bytes_ranges_and_one_link_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "identity_probe.identity(original) == original_identity",
        "identity_probe.identity(displaced) == original_identity",
        "identity_probe.link_count(original) == 2",
        "identity_probe.link_count(original) == 1",
        "identity_probe.link_count(displaced) == 1",
        "coordination_path.read_bytes() == payload",
        "displaced_path.read_bytes() == payload",
        "_assert_exclusive_available(lock_probe, coordination_path)",
        "mutator_return_code is not None and mutator_return_code != 0",
        "guardian is not None and guardian.returncode == 0",
        "for process in (mutator, guardian):",
        "stream.closed",
        "identity_probe.owned_count == 0",
        "lock_probe.owned_count == 0",
        "assert not alias_path.exists()",
        "assert not coordination_path.exists()",
    ):
        assert required in probe
    for forbidden in ("time.sleep", "retry", "communicate(", "shell=True", "env="):
        assert forbidden not in probe


def test_m187_records_negative_recovery_and_three_process_limit() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "abrupt process loss",
        "leaves the peer alias absent",
        "three-process, same-principal",
        "no automatic rollback or recovery",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0170-probe-windows-hard-link-alias-mutator-abrupt-loss.md").read_text(
        encoding="utf-8"
    )
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "recovery gap" in rfc_compact
    assert "does not establish cross-principal behavior" in rfc_compact
    assert "no retry or sleep" in rfc_compact


def test_m187_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-probe"
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
    assert "0170-probe-windows-hard-link-alias-mutator-abrupt-loss.md" in rfc_index


def test_m187_keeps_abrupt_termination_controlled_and_test_only() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("_terminate_and_assert_abrupt(mutator)") == 1
    assert "tests/integration" not in probe
    assert not (_ROOT / "tests/fixtures/windows_hard_link_alias_mutator_abrupt_loss.py").exists()

    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    assert "controlled test child" in compact
    assert "not a production cleanup action" in compact
