"""Protect M196's repeated buffered-close disposition boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0178-probe-windows-hard-link-alias-mutator-buffered-close-delivery-failure-after-invalid-settlement.md": (
        "3a8ab1e62f0b4e4aa977256a5570bbf712ad4ae84836ed408272d9ebb379de01"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-mutator-buffered-close-delivery-failure-after-invalid-settlement-probe.md": (
        "24336d980328c5a2b9d72acf6aceb12eb0c427900910f869cae04d9af9a1c547"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m195_windows_hard_link_alias_mutator_buffered_close_delivery_failure_after_invalid_settlement_boundary.py": (
        "8cc449666cdec8fcbefc57ba057f73c696849a2251fee1df7124c1c1e907f5fe"
    ),
    "tests/fixtures/windows_hard_link_alias_mutator_child.py": (
        "19688156f08643aa31a05f53a8a6fc31ff1b60ec1f311e5c557d9fcd87ad2b0a"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_buffered_close_delivery_failure_after_invalid_settlement_probe.py": (
        "f24175fb88ef7c1c04b7c446186c22b13fbeca5ef49d7daf320e7f2c2950d0c5"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_PRIOR_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_buffered_close_delivery_failure_after_invalid_settlement_probe.py"
)
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_repeated_buffered_close_after_delivery_failure_probe.py"
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


def test_m196_changes_no_runtime_dependency_ci_fixture_or_prior_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m196_reuses_m195_close_failure_and_m186_bounded_child() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "from test_windows_cache_cleanup_hard_link_alias_mutator_buffered_close_delivery_failure_after_invalid_settlement_probe import (",
        "_send_invalid_sequence_then_assert_buffered_close_delivery_failure",
        "from test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe import (",
        "_RECREATE_TOKEN",
        "_read_alias_mutator_event",
        "_send_alias_mutator_token",
        "_start_alias_mutator",
    ):
        assert required in probe
    for forbidden in (
        "subprocess.Popen(",
        "process.kill(",
        "communicate(",
        "time.sleep",
        "retry",
        "shell=True",
        "env=",
    ):
        assert forbidden not in probe


def test_m196_orders_recreate_failed_close_repeat_guardian_release_and_rename() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    mutator_started = probe.index("mutator = _start_alias_mutator", guardian_ready)
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"', mutator_started)
    recreated = probe.index(
        '_send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"',
        deleted,
    )
    two_links_before_close = probe.index("identity_probe.link_count(original) == 2", recreated)
    repeated_close = probe.index(
        "_send_invalid_sequence_then_assert_repeated_buffered_close(",
        two_links_before_close,
    )
    settled = probe.index("assert mutator.poll() == _INVALID_CONTROL_EXIT_CODE", repeated_close)
    two_links_after_close = probe.index("identity_probe.link_count(original) == 2", settled)
    blocked = probe.index("blocked_after_repeated_close.value.winerror", two_links_after_close)
    guardian_closed = probe.index('_release_identity_guardian(guardian) == "closed"', blocked)
    renamed = probe.index("coordination_path.rename(displaced_path)", guardian_closed)
    assert (
        guardian_ready
        < mutator_started
        < deleted
        < recreated
        < two_links_before_close
        < repeated_close
        < settled
        < two_links_after_close
        < blocked
        < guardian_closed
        < renamed
    )


def test_m196_repeats_close_only_after_m195_failure_left_stream_closed() -> None:
    prior = _PRIOR_PROBE.read_text(encoding="utf-8")
    probe = _PROBE.read_text(encoding="utf-8")
    prior_helper = prior[
        prior.index("def _send_invalid_sequence") : prior.index("def test_late_valid")
    ]
    helper = probe[
        probe.index("def _send_invalid_sequence") : probe.index("def test_repeated_close")
    ]
    assert "with pytest.raises(OSError):" in prior_helper
    assert "stdin.close()" in prior_helper
    assert "assert stdin.closed" in prior_helper
    delegated = helper.index("_send_invalid_sequence_then_assert_buffered_close_delivery_failure(")
    closed_before_repeat = helper.index("assert stdin.closed", delegated)
    repeated = helper.index("assert stdin.close() is None", closed_before_repeat)
    closed_after_repeat = helper.index("assert stdin.closed", repeated)
    assert delegated < closed_before_repeat < repeated < closed_after_repeat
    assert helper.count("stdin.close()") == 1
    assert "pytest.raises" not in helper
    assert ".errno" not in helper
    assert ".winerror" not in helper


def test_m196_preserves_identity_count_ranges_rename_and_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "os.link(coordination_path, alias_path)",
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


def test_m196_records_repeat_close_disposition_and_limits() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "first `close()`",
        "generic `oserror`",
        "already closed",
        "second `close()`",
        "returns `none`",
        "no acknowledgement",
        "three-process, same-principal",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT
        / "docs/rfcs/0179-probe-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure.md"
    ).read_text(encoding="utf-8")
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "repeated-close disposition evidence" in rfc_compact
    assert "does not retry delivery" in rfc_compact
    assert "use no retry or sleep" in rfc_compact


def test_m196_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = (
        "cache-cleanup-windows-hard-link-alias-mutator-repeated-buffered-close-"
        "after-delivery-failure-probe"
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
        "0179-probe-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure.md"
        in rfc_index
    )


def test_m196_keeps_repeated_close_controlled_and_test_only() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("_send_invalid_sequence_then_assert_repeated_buffered_close(") == 2
    assert "tests/integration" not in probe
    assert not (_ROOT / "tests/fixtures/windows_hard_link_alias_mutator_repeated_close.py").exists()

    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    assert "controlled test-only stream condition" in compact
    assert "not a production cleanup action" in compact
