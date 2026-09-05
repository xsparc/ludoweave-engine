"""Protect M194's Windows late valid-close delivery-failure boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0176-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate.md": (
        "a4ca43c5132960296ea60c98d505e33bdf30eb35c60f0cd2b4255f357f297e27"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate-probe.md": (
        "203f061092caf8e2ee8f7692f0dcc4e612120270456d7f105bbac8288d245da4"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m186_windows_independent_hard_link_alias_mutator_aba_boundary.py": (
        "44c8a8e5bb2b2ec707332381a5cb55cc3fa3f23356aefa2978ba9aee7c754c7c"
    ),
    "tests/architecture/test_m193_windows_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_open_writer_settlement_after_recreate_boundary.py": (
        "6f5a6fecf9def0169d6ce493f01d15049665dd114632b14ac307a8ae430b88f4"
    ),
    "tests/fixtures/windows_hard_link_alias_mutator_child.py": (
        "19688156f08643aa31a05f53a8a6fc31ff1b60ec1f311e5c557d9fcd87ad2b0a"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_open_writer_settlement_after_recreate_probe.py": (
        "895316247bd0eab526bc351bc83e78484d7b325158c2039f51bc45e9b3eaca79"
    ),
    "tests/integration/test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe.py": (
        "0217545916b6e9f587f1c642296c10b6f539c83238cad8fe2c68ec379ecdc68f"
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
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_late_valid_close_delivery_failure_after_invalid_settlement_probe.py"
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


def test_m194_changes_no_runtime_dependency_ci_fixture_or_prior_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m194_reuses_m186_child_and_existing_bounded_protocol() -> None:
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


def test_m194_orders_recreate_settlement_late_delivery_guardian_release_and_rename() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    mutator_started = probe.index("mutator = _start_alias_mutator", guardian_ready)
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"', mutator_started)
    recreated = probe.index(
        '_send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"',
        deleted,
    )
    two_links_before_invalid = probe.index("identity_probe.link_count(original) == 2", recreated)
    invalid_then_late = probe.index(
        "_send_invalid_sequence_then_assert_late_valid_close_delivery_failure(",
        two_links_before_invalid,
    )
    settled = probe.index("assert mutator.poll() == _INVALID_CONTROL_EXIT_CODE", invalid_then_late)
    two_links_after_late = probe.index("identity_probe.link_count(original) == 2", settled)
    blocked = probe.index("blocked_after_late_close.value.winerror", two_links_after_late)
    guardian_closed = probe.index('_release_identity_guardian(guardian) == "closed"', blocked)
    renamed = probe.index("coordination_path.rename(displaced_path)", guardian_closed)
    assert (
        guardian_ready
        < mutator_started
        < deleted
        < recreated
        < two_links_before_invalid
        < invalid_then_late
        < settled
        < two_links_after_late
        < blocked
        < guardian_closed
        < renamed
    )


def test_m194_buffers_one_late_byte_only_after_bounded_invalid_settlement() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("os.link(coordination_path, alias_path)") == 1
    assert probe.count("_send_alias_mutator_token(mutator, _RECREATE_TOKEN)") == 1
    assert probe.count("stdin.write(") == 2
    assert probe.count("stdin.flush()") == 2
    assert probe.count("stdin.close()") == 1
    assert 'b"?!"' in probe
    assert 'b"!"' in probe
    helper = probe[probe.index("def _send_invalid_sequence") : probe.index("def test_late_valid")]
    first_write = helper.index("stdin.write(_INVALID_PREFIX_WITH_VALID_CLOSE_SUFFIX)")
    first_flush = helper.index("stdin.flush()", first_write)
    waited = helper.index("process.wait(timeout=_TIMEOUT_SECONDS)", first_flush)
    stdout_eof = helper.index('stdout.read(_MAX_LINE_BYTES + 1) == b""', waited)
    late_write = helper.index("stdin.write(_LATE_VALID_CLOSE_TOKEN)", stdout_eof)
    late_flush = helper.index("stdin.flush()", late_write)
    closed = helper.index("stdin.close()", late_flush)
    assert first_write < first_flush < waited < stdout_eof < late_write < late_flush < closed


def test_m194_proves_buffer_acceptance_not_delivery_and_complete_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "stdin.write(_INVALID_PREFIX_WITH_VALID_CLOSE_SUFFIX) == len(",
        "return_code == _INVALID_CONTROL_EXIT_CODE",
        'stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "stdin.write(_LATE_VALID_CLOSE_TOKEN) == len(_LATE_VALID_CLOSE_TOKEN)",
        "with pytest.raises(OSError):",
        "with suppress(OSError):",
        "assert stdin.closed",
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
    helper = probe[probe.index("def _send_invalid_sequence") : probe.index("def test_late_valid")]
    assert helper.count("assert not stdin.closed") == 4
    assert ".errno" not in helper
    assert ".winerror" not in helper
    assert '_read_alias_mutator_event(process) == "closed"' not in probe
    for forbidden in ("time.sleep", "retry", "shell=True", "env="):
        assert forbidden not in probe


def test_m194_records_buffered_delivery_failure_and_translation_limit() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-late-valid-close-delivery-failure-after-invalid-settlement-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "late valid close byte",
        "buffer acceptance is not peer receipt",
        "delivery fails on flush",
        "child has already settled",
        "emits no `closed`",
        "three-process, same-principal",
        "no exact python exception code",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT
        / "docs/rfcs/0177-probe-windows-hard-link-alias-mutator-late-valid-close-delivery-failure-after-invalid-settlement.md"
    ).read_text(encoding="utf-8")
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "buffered acceptance-versus-delivery evidence" in rfc_compact
    assert "does not establish arbitrary buffered input" in rfc_compact
    assert "generic `oserror`" in rfc_compact
    assert "use no retry or sleep" in rfc_compact


def test_m194_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = (
        "cache-cleanup-windows-hard-link-alias-mutator-late-valid-close-"
        "delivery-failure-after-invalid-settlement-probe"
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
        "0177-probe-windows-hard-link-alias-mutator-late-valid-close-delivery-failure-after-invalid-settlement.md"
        in rfc_index
    )


def test_m194_keeps_late_delivery_condition_controlled_and_test_only() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("_send_invalid_sequence_then_assert_late_valid_close_delivery_failure(") == 2
    assert "tests/integration" not in probe
    assert not (
        _ROOT / "tests/fixtures/windows_hard_link_alias_mutator_late_valid_close.py"
    ).exists()

    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-late-valid-close-delivery-failure-after-invalid-settlement-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    assert "controlled test-only protocol condition" in compact
    assert "not a production cleanup action" in compact
