"""Protect M189's Windows post-recreate alias-mutator control-EOF boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0171-probe-windows-hard-link-alias-mutator-abrupt-loss-after-recreate.md": (
        "1898cb1ef878c63860a61743a5a6c1c6803de8fb08d2eabf7309acf128496309"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-after-recreate-probe.md": (
        "a6f0bafc7a38cb45dd3bd7e8505b7f23b14dd2f180a63aa37bda6880bc3d23e0"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m186_windows_independent_hard_link_alias_mutator_aba_boundary.py": (
        "a68bbb0a6870d5c56c7556f16830610f8e5fe9a71157d46dc5b70b4dab68d9dc"
    ),
    "tests/architecture/test_m188_windows_hard_link_alias_mutator_abrupt_loss_after_recreate_boundary.py": (
        "e5bd92759f2839ebd0f01b8a5731df4cdc634ff9b17044584842abb8d9bc3951"
    ),
    "tests/fixtures/windows_hard_link_alias_mutator_child.py": (
        "19688156f08643aa31a05f53a8a6fc31ff1b60ec1f311e5c557d9fcd87ad2b0a"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_abrupt_loss_after_recreate_probe.py": (
        "246b6276dfba4a5809c61e57a67aba792c401c76d507093a8b10f837f008b23d"
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
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_control_pipe_eof_after_recreate_probe.py"
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


def test_m189_changes_no_runtime_dependency_ci_fixture_or_prior_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m189_reuses_m186_child_and_existing_bounded_protocol() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "from test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe import (",
        "_MAX_LINE_BYTES",
        "_read_alias_mutator_event",
        "_RECREATE_TOKEN",
        "_send_alias_mutator_token",
        "_start_alias_mutator",
        "_TIMEOUT_SECONDS",
        "process.wait(timeout=_TIMEOUT_SECONDS)",
    ):
        assert required in probe
    for forbidden in (
        "subprocess.Popen(",
        "process.kill(",
        "_terminate_and_assert_abrupt",
        "_CLOSE_TOKEN",
        "_close_alias_mutator,",
        "communicate(",
    ):
        assert forbidden not in probe


def test_m189_orders_recreate_eof_settlement_guardian_release_and_rename() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    mutator_started = probe.index("mutator = _start_alias_mutator", guardian_ready)
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"', mutator_started)
    recreated = probe.index(
        '_send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"',
        deleted,
    )
    two_links_before_eof = probe.index("identity_probe.link_count(original) == 2", recreated)
    eof = probe.index(
        "mutator_return_code = _close_alias_mutator_control_and_assert_eof(mutator)",
        two_links_before_eof,
    )
    settled = probe.index("assert mutator.poll() == _CONTROL_EOF_EXIT_CODE", eof)
    two_links_after_eof = probe.index("identity_probe.link_count(original) == 2", settled)
    blocked = probe.index("blocked_after_control_eof.value.winerror", two_links_after_eof)
    guardian_closed = probe.index('_release_identity_guardian(guardian) == "closed"', blocked)
    renamed = probe.index("coordination_path.rename(displaced_path)", guardian_closed)
    assert (
        guardian_ready
        < mutator_started
        < deleted
        < recreated
        < two_links_before_eof
        < eof
        < settled
        < two_links_after_eof
        < blocked
        < guardian_closed
        < renamed
    )


def test_m189_recreates_once_and_keeps_alias_and_guardian_live_after_eof() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("os.link(coordination_path, alias_path)") == 1
    assert probe.count("_send_alias_mutator_token(mutator, _RECREATE_TOKEN)") == 1
    assert probe.count("stdin.close()") == 1
    eof = probe.index("mutator_return_code = _close_alias_mutator_control_and_assert_eof")
    after_eof = probe[eof:]
    assert "assert guardian.poll() is None" in after_eof
    assert "assert alias_path.exists()" in after_eof
    for forbidden in ("os.link(", "_send_alias_mutator_token", 'b"!"'):
        assert forbidden not in after_eof


def test_m189_preserves_identity_bytes_ranges_eof_and_two_link_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "stdin.close()",
        "assert stdin.closed",
        "return_code == _CONTROL_EOF_EXIT_CODE",
        'stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "identity_probe.identity(original) == original_identity",
        "identity_probe.identity(alias) == original_identity",
        "identity_probe.identity(displaced) == original_identity",
        "identity_probe.link_count(original) == 1",
        "identity_probe.link_count(original) == 2",
        "identity_probe.link_count(alias) == 2",
        "identity_probe.link_count(displaced) == 2",
        "coordination_path.read_bytes() == payload",
        "alias_path.read_bytes() == payload",
        "displaced_path.read_bytes() == payload",
        "_assert_exclusive_available(lock_probe, coordination_path)",
        "_assert_exclusive_available(lock_probe, alias_path)",
        "guardian is not None and guardian.returncode == 0",
        "for process in (mutator, guardian):",
        "stream.closed",
        "identity_probe.owned_count == 0",
        "lock_probe.owned_count == 0",
        "assert alias_path.exists()",
        "assert not coordination_path.exists()",
    ):
        assert required in probe
    for forbidden in ("time.sleep", "retry", "shell=True", "env="):
        assert forbidden not in probe


def test_m189_records_negative_rollback_and_three_process_limit() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "control-pipe eof after",
        "leaves the peer alias present",
        "three-process, same-principal",
        "no automatic rollback to one link",
        "not abrupt process termination",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT
        / "docs/rfcs/0172-probe-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate.md"
    ).read_text(encoding="utf-8")
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "negative rollback evidence" in rfc_compact
    assert "does not establish cross-principal behavior" in rfc_compact
    assert "use no retry or sleep" in rfc_compact


def test_m189_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate-probe"
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
    assert (
        "0172-probe-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate.md" in rfc_index
    )


def test_m189_keeps_eof_controlled_and_test_only() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("_close_alias_mutator_control_and_assert_eof(mutator)") == 1
    assert "tests/integration" not in probe
    assert not (
        _ROOT / "tests/fixtures/windows_hard_link_alias_mutator_control_pipe_eof_after_recreate.py"
    ).exists()

    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    assert "controlled test-only protocol condition" in compact
    assert "not a production cleanup action" in compact
