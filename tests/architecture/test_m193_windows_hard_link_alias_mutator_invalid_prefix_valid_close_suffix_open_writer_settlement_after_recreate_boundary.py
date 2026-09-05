"""Protect M193's Windows open-writer invalid-prefix settlement boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0175-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate.md": (
        "43303bae497490e717f43cf3bd1a8eb51dcba90ffecacacb8d830c8d247c68dc"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate-probe.md": (
        "2fed461580b49fefdaa29f0c590ccacc697f611c2c45b80d8b3b3702046b5b69"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m186_windows_independent_hard_link_alias_mutator_aba_boundary.py": (
        "44c8a8e5bb2b2ec707332381a5cb55cc3fa3f23356aefa2978ba9aee7c754c7c"
    ),
    "tests/architecture/test_m192_windows_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_after_recreate_boundary.py": (
        "1122edb564bd33723678bd30be0169e44feedd29dacf863470f4d17ec0483e19"
    ),
    "tests/fixtures/windows_hard_link_alias_mutator_child.py": (
        "19688156f08643aa31a05f53a8a6fc31ff1b60ec1f311e5c557d9fcd87ad2b0a"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_after_recreate_probe.py": (
        "83f1f08466e5a764ec55b804abaa72152d4b32a6bca45f2c62da1d869739fe9b"
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
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_open_writer_settlement_after_recreate_probe.py"
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


def test_m193_changes_no_runtime_dependency_ci_fixture_or_prior_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m193_reuses_m186_child_and_existing_bounded_protocol() -> None:
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


def test_m193_orders_recreate_open_writer_settlement_guardian_release_and_rename() -> None:
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
        "_send_invalid_prefix_with_valid_close_suffix_and_assert_open_writer_settlement(",
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


def test_m193_writes_one_fixed_sequence_and_closes_only_after_wait() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert probe.count("os.link(coordination_path, alias_path)") == 1
    assert probe.count("_send_alias_mutator_token(mutator, _RECREATE_TOKEN)") == 1
    assert probe.count("stdin.write(_INVALID_PREFIX_WITH_VALID_CLOSE_SUFFIX)") == 1
    assert probe.count("stdin.flush()") == 1
    assert probe.count("stdin.close()") == 1
    assert 'b"?!"' in probe
    helper = probe.index("def _send_invalid_prefix_with_valid_close_suffix")
    flushed = probe.index("stdin.flush()", helper)
    waited = probe.index("process.wait(timeout=_TIMEOUT_SECONDS)", flushed)
    closed = probe.index("stdin.close()", waited)
    assert flushed < waited < closed
    after_sequence = probe[probe.index("mutator_return_code = (", helper) :]
    for forbidden in ("stdin.write(", "_send_alias_mutator_token", "os.link("):
        assert forbidden not in after_sequence


def test_m193_proves_open_writer_settlement_without_closed_event_and_cleans_up() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "stdin.write(_INVALID_PREFIX_WITH_VALID_CLOSE_SUFFIX) == len(",
        "stdin.flush()",
        "assert not stdin.closed",
        "process.wait(timeout=_TIMEOUT_SECONDS)",
        "return_code == _INVALID_CONTROL_EXIT_CODE",
        'stdout.read(_MAX_LINE_BYTES + 1) == b""',
        'stderr.read(_MAX_LINE_BYTES + 1) == b""',
        "stdin.close()",
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
    helper = probe[probe.index("def _send_invalid_prefix") : probe.index("def test_invalid_prefix")]
    assert helper.count("assert not stdin.closed") == 2
    assert helper.index("assert not stdin.closed") < helper.index("process.wait(")
    assert helper.rindex("assert not stdin.closed") > helper.index("process.wait(")
    assert '_read_alias_mutator_event(process) == "closed"' not in probe
    for forbidden in ("time.sleep", "retry", "shell=True", "env="):
        assert forbidden not in probe


def test_m193_records_open_writer_settlement_and_bounded_output_limit() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "fixed invalid prefix with one valid close suffix",
        "parent writer remains open",
        "emits no `closed`",
        "settles independently of control-pipe eof",
        "bounded-output fixture",
        "three-process, same-principal",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT
        / "docs/rfcs/0176-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate.md"
    ).read_text(encoding="utf-8")
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "open-writer settlement evidence" in rfc_compact
    assert "does not establish arbitrary malformed input" in rfc_compact
    assert "use no retry or sleep" in rfc_compact


def test_m193_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = (
        "cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-"
        "suffix-open-writer-settlement-after-recreate-probe"
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
        "0176-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate.md"
        in rfc_index
    )


def test_m193_keeps_open_writer_condition_controlled_and_test_only() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    assert (
        probe.count(
            "_send_invalid_prefix_with_valid_close_suffix_and_assert_open_writer_settlement("
        )
        == 2
    )
    assert "tests/integration" not in probe
    assert not (
        _ROOT / "tests/fixtures/windows_hard_link_alias_mutator_open_writer_settlement.py"
    ).exists()

    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    assert "controlled test-only protocol condition" in compact
    assert "not a production cleanup action" in compact
