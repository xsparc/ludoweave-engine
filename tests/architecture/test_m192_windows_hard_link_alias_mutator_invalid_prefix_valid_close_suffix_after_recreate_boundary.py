"""Protect M192's Windows post-recreate invalid-prefix boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0174-probe-windows-hard-link-alias-mutator-valid-close-prefix-trailing-byte-after-recreate.md": (
        "2594423c3109ef3462e69c521413714aed2e110efc458b6ef44e08e2d61f6785"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-mutator-valid-close-prefix-trailing-byte-after-recreate-probe.md": (
        "4a7ca6f37d4dda99dbdcb9d4c1c3061d889470a04d5c0505ab57117f3a3e051d"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m186_windows_independent_hard_link_alias_mutator_aba_boundary.py": (
        "c230ba596091b5d4faf4c9044259a1a9482508b58433101ae5b90c08cc3e1c00"
    ),
    "tests/architecture/test_m191_windows_hard_link_alias_mutator_valid_close_prefix_trailing_byte_after_recreate_boundary.py": (
        "a17455d02c9d07445ed51b308d11d574e2f7df4f681bc84889bc0f7ee0846c5f"
    ),
    "tests/fixtures/windows_hard_link_alias_mutator_child.py": (
        "19688156f08643aa31a05f53a8a6fc31ff1b60ec1f311e5c557d9fcd87ad2b0a"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_valid_close_prefix_trailing_byte_after_recreate_probe.py": (
        "a1276c9661750cc3d8eb874de52fb24069c5e378038ab7b3e10b1ae902e5c581"
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
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_after_recreate_probe.py"
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


def test_m192_changes_no_runtime_dependency_ci_fixture_or_prior_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m192_reuses_m186_child_and_existing_bounded_protocol() -> None:
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
        "_close_alias_mutator,",
        "communicate(",
    ):
        assert forbidden not in probe


def test_m192_orders_recreate_invalid_prefix_guardian_release_and_rename() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    mutator_started = probe.index("mutator = _start_alias_mutator", guardian_ready)
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"', mutator_started)
    recreated = probe.index(
        '_send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"',
        deleted,
    )
    two_links_before_invalid = probe.index("identity_probe.link_count(original) == 2", recreated)
    invalid = probe.index(
        "_send_invalid_prefix_with_valid_close_suffix_and_assert_settlement(mutator)",
        two_links_before_invalid,
    )
    settled = probe.index("assert mutator.poll() == _INVALID_CONTROL_EXIT_CODE", invalid)
    two_links_after_invalid = probe.index("identity_probe.link_count(original) == 2", settled)
    blocked = probe.index("blocked_after_invalid_prefix.value.winerror", two_links_after_invalid)
    guardian_closed = probe.index('_release_identity_guardian(guardian) == "closed"', blocked)
    renamed = probe.index("coordination_path.rename(displaced_path)", guardian_closed)
    assert (
        guardian_ready
        < mutator_started
        < deleted
        < recreated
        < two_links_before_invalid
        < invalid
        < settled
        < two_links_after_invalid
        < blocked
        < guardian_closed
        < renamed
    )


def test_m192_writes_one_fixed_two_byte_sequence_and_no_second_control_write() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("os.link(coordination_path, alias_path)") == 1
    assert probe.count("_send_alias_mutator_token(mutator, _RECREATE_TOKEN)") == 1
    assert probe.count("stdin.write(_INVALID_PREFIX_WITH_VALID_CLOSE_SUFFIX)") == 1
    assert probe.count("stdin.flush()") == 1
    assert probe.count("stdin.close()") == 1
    assert 'b"?!"' in probe
    sequence = probe.index(
        "mutator_return_code = (\n"
        "                _send_invalid_prefix_with_valid_close_suffix_and_assert_settlement(mutator)"
    )
    after_sequence = probe[sequence:]
    for forbidden in ("stdin.write(", "_send_alias_mutator_token", "os.link("):
        assert forbidden not in after_sequence


def test_m192_proves_invalid_settlement_without_closed_event_and_two_link_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "stdin.write(_INVALID_PREFIX_WITH_VALID_CLOSE_SUFFIX) == len(",
        "stdin.flush()",
        "stdin.close()",
        "assert stdin.closed",
        "return_code == _INVALID_CONTROL_EXIT_CODE",
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
    assert '_read_alias_mutator_event(process) == "closed"' not in probe
    for forbidden in ("time.sleep", "retry", "shell=True", "env="):
        assert forbidden not in probe


def test_m192_records_prefix_precedence_and_protocol_framing_limit() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "fixed invalid prefix with one valid close suffix",
        "emits no `closed`",
        "leaves the peer alias present",
        "three-process, same-principal",
        "leading-byte rejection",
        "not general message framing",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT
        / "docs/rfcs/0175-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate.md"
    ).read_text(encoding="utf-8")
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "prefix-precedence rejection evidence" in rfc_compact
    assert "does not establish arbitrary malformed input" in rfc_compact
    assert "use no retry or sleep" in rfc_compact


def test_m192_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = (
        "cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-"
        "valid-close-suffix-after-recreate-probe"
    )
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
        "0175-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate.md"
        in rfc_index
    )


def test_m192_keeps_invalid_prefix_condition_controlled_and_test_only() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert (
        probe.count("_send_invalid_prefix_with_valid_close_suffix_and_assert_settlement(mutator)")
        == 1
    )
    assert "tests/integration" not in probe
    assert not (
        _ROOT
        / "tests/fixtures/windows_hard_link_alias_mutator_invalid_prefix_valid_close_suffix.py"
    ).exists()

    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    assert "controlled test-only protocol condition" in compact
    assert "not a production cleanup action" in compact
