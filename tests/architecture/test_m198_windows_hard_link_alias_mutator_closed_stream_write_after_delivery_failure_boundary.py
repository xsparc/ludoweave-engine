"""Protect M198's closed-stream write disposition boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0180-probe-windows-hard-link-alias-mutator-closed-stream-flush-after-delivery-failure.md": (
        "a16c3f8254d9ec69a6301da734e565942ec50401297e6247e3feed12cf303555"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-flush-after-delivery-failure-probe.md": (
        "b4a140494757d9da8fcae1462d2b5dfae236e3e75308a5ddb957a4eb5ce25eab"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m197_windows_hard_link_alias_mutator_closed_stream_flush_after_delivery_failure_boundary.py": (
        "55324430acb6a1564256d95c4727e84c0e7b21ba8b12990b6b59f83978ebcef5"
    ),
    "tests/fixtures/windows_hard_link_alias_mutator_child.py": (
        "19688156f08643aa31a05f53a8a6fc31ff1b60ec1f311e5c557d9fcd87ad2b0a"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_closed_stream_flush_after_delivery_failure_probe.py": (
        "ed82b9b2ad5cd65c28ceadddf627b0f5714d957e2400f1b3dc512e16acdd034f"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_PRIOR_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_closed_stream_flush_after_delivery_failure_probe.py"
)
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_closed_stream_write_after_delivery_failure_probe.py"
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


def test_m198_changes_no_runtime_dependency_ci_fixture_or_prior_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m198_reuses_m197_closed_flush_and_m186_bounded_child() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "from test_windows_cache_cleanup_hard_link_alias_mutator_closed_stream_flush_after_delivery_failure_probe import (",
        "_send_invalid_sequence_then_assert_closed_stream_flush",
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


def test_m198_orders_recreate_closed_write_guardian_release_and_rename() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    mutator_started = probe.index("mutator = _start_alias_mutator", guardian_ready)
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"', mutator_started)
    recreated = probe.index(
        '_send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"',
        deleted,
    )
    two_links_before_write = probe.index("identity_probe.link_count(original) == 2", recreated)
    closed_write = probe.index(
        "_send_invalid_sequence_then_assert_closed_stream_write(",
        two_links_before_write,
    )
    settled = probe.index("assert mutator.poll() == _INVALID_CONTROL_EXIT_CODE", closed_write)
    two_links_after_write = probe.index("identity_probe.link_count(original) == 2", settled)
    blocked = probe.index("blocked_after_closed_stream_write.value.winerror", two_links_after_write)
    guardian_closed = probe.index('_release_identity_guardian(guardian) == "closed"', blocked)
    renamed = probe.index("coordination_path.rename(displaced_path)", guardian_closed)
    assert (
        guardian_ready
        < mutator_started
        < deleted
        < recreated
        < two_links_before_write
        < closed_write
        < settled
        < two_links_after_write
        < blocked
        < guardian_closed
        < renamed
    )


def test_m198_writes_only_after_m197_left_stream_closed() -> None:
    prior = _PRIOR_PROBE.read_text(encoding="utf-8")
    probe = _PROBE.read_text(encoding="utf-8")
    prior_helper = prior[
        prior.index("def _send_invalid_sequence") : prior.index("def test_flush_raises")
    ]
    helper = probe[probe.index("def _send_invalid_sequence") : probe.index("def test_write_raises")]
    assert "stdin.flush()" in prior_helper
    assert prior_helper.count("assert stdin.closed") == 2
    delegated = helper.index("_send_invalid_sequence_then_assert_closed_stream_flush(")
    closed_before_write = helper.index("assert stdin.closed", delegated)
    value_error = helper.index("with pytest.raises(ValueError):", closed_before_write)
    write = helper.index('stdin.write(b"!")', value_error)
    closed_after_write = helper.index("assert stdin.closed", write)
    assert delegated < closed_before_write < value_error < write < closed_after_write
    assert helper.count('stdin.write(b"!")') == 1
    assert "match=" not in helper
    assert ".errno" not in helper
    assert ".winerror" not in helper


def test_m198_preserves_identity_count_ranges_rename_and_cleanup() -> None:
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


def test_m198_records_closed_write_disposition_and_limits() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "first `close()`",
        "generic `oserror`",
        "second `close()`",
        "one `flush()`",
        'one `write(b"!")`',
        "generic `valueerror`",
        "no acknowledgement",
        "three-process, same-principal",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT
        / "docs/rfcs/0181-probe-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure.md"
    ).read_text(encoding="utf-8")
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "closed-stream write disposition evidence" in rfc_compact
    assert "does not establish native-call suppression" in rfc_compact
    assert "use no retry or sleep" in rfc_compact


def test_m198_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = (
        "cache-cleanup-windows-hard-link-alias-mutator-closed-stream-write-"
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
        "0181-probe-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure.md"
        in rfc_index
    )


def test_m198_keeps_closed_write_controlled_and_test_only() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("_send_invalid_sequence_then_assert_closed_stream_write(") == 2
    assert "tests/integration" not in probe
    assert not (
        _ROOT / "tests/fixtures/windows_hard_link_alias_mutator_closed_stream_write.py"
    ).exists()

    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    assert "controlled test-only stream condition" in compact
    assert "not a production cleanup action" in compact
