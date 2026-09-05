"""Protect M181's Windows expected-identity guardian admission boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0163-probe-windows-zero-owner-guardian-restart-boundary.md": (
        "4392fe4da0038877b166d66ce06c8c5cb5bdbd818a6beb37975c7efb9ea58f62"
    ),
    "docs/security/cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe.md": (
        "e39474e358c0238afce3d91c6514d4e97cc0d803412c2c674073260a5ddb6481"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m180_windows_zero_owner_guardian_restart_boundary.py": (
        "0ea288713731b15fa64bb9d9d84556aadbb807fcf6a0a41f9f3af9369e872a4b"
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
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_probe.py": (
        "d0ea6af78537cd60d1e6da35e6d9db8f17416d93e9034e8f8d25f2c3b2a1c044"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_substitution_probe.py": (
        "e2f926d122bae494f94b9636178cc4664ca70080474e259b9d6a75822b5e2f61"
    ),
    "tests/integration/test_windows_cache_cleanup_protected_guardian_handoff_probe.py": (
        "5f570f9e57de824cf0f08ec0694b539e4b435262b462504894394187ed3c3d18"
    ),
    "tests/integration/test_windows_cache_cleanup_zero_owner_guardian_restart_boundary_probe.py": (
        "c4f73153bf60833a37c83e4c17c6ae14e2c620241f8c4a4b26f604ceae4c77f0"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_FIXTURE = _ROOT / "tests/fixtures/windows_coordination_identity_guardian_child.py"
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_cache_cleanup_expected_identity_guardian_admission_probe.py"
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


def test_m181_changes_no_runtime_dependency_ci_or_m180_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m181_fixture_protects_then_compares_the_same_open_handle() -> None:
    fixture = _FIXTURE.read_text(encoding="utf-8")
    main = fixture.index("def main()")
    opened = fixture.index("raw_handle = create_file(", main)
    share_mode = fixture.index("_FILE_SHARE_READ | _FILE_SHARE_WRITE,", opened)
    attributes = fixture.index("attributes = _FileAttributeTagInfo()", share_mode)
    attribute_query = fixture.index("_FILE_ATTRIBUTE_TAG_INFO_CLASS,", attributes)
    identity = fixture.index("identity = _FileIdInfo()", attribute_query)
    identity_query = fixture.index("_FILE_ID_INFO_CLASS,", identity)
    observed = fixture.index("observed_identity =", identity_query)
    compared = fixture.index("if observed_identity != expected_identity:", observed)
    closed = fixture.index("close_handle(wintypes.HANDLE(handle))", compared)
    mismatch = fixture.index('_emit("identity_mismatch")', closed)
    ready = fixture.index('_emit("ready")', mismatch)
    assert opened < share_mode < attributes < attribute_query < identity < identity_query
    assert identity_query < observed < compared < closed < mismatch < ready
    assert "_FILE_SHARE_DELETE" not in fixture
    assert "_FILE_FLAG_OPEN_REPARSE_POINT" in fixture
    assert "os.get_handle_inheritable(handle)" in fixture


def test_m181_parent_passes_exact_identity_without_runtime_native_or_shell_surface() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_start_identity_guardian",
        "str(volume_serial)",
        "file_id.hex()",
        "close_fds=True",
        "shell=False",
        "_WindowsCapabilityProbe",
        "_attempt_substitution",
        "_assert_exclusive_available",
    ):
        assert required in probe
    for forbidden in (
        "import ctypes",
        "env=",
        "os.system",
        "shell=True",
    ):
        assert forbidden not in probe


def test_m181_orders_matching_admission_protection_and_exact_close() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_expected_identity_guardian_admits_matching_opened_identity")
    original = probe.index("original_identity =", test)
    started = probe.index("guardian = _start_identity_guardian", original)
    ready = probe.index('_read_identity_guardian_event(guardian) == "ready"', started)
    blocked = probe.index("with pytest.raises(OSError) as blocked:", ready)
    sharing = probe.index("blocked.value.winerror == _ERROR_SHARING_VIOLATION", blocked)
    range_available = probe.index("_assert_exclusive_available", sharing)
    closed = probe.index('_release_identity_guardian(guardian) == "closed"', range_available)
    renamed = probe.index("coordination_path.rename(displaced_path)", closed)
    moved_identity = probe.index("identity_probe.identity(moved) == original_identity", renamed)
    assert (
        test
        < original
        < started
        < ready
        < blocked
        < sharing
        < range_available
        < closed
        < renamed
        < moved_identity
    )


def test_m181_orders_substitution_before_identity_mismatch_and_release() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_expected_identity_guardian_rejects_preexisting_replacement")
    original = probe.index("original_identity =", test)
    substituted = probe.index("_attempt_substitution(tmp_path)", original)
    replacement = probe.index("replacement_identity =", substituted)
    started = probe.index("guardian = _start_identity_guardian", replacement)
    mismatch = probe.index(
        '_read_identity_guardian_event(guardian) == "identity_mismatch"', started
    )
    finished = probe.index("_finish_identity_mismatch(guardian)", mismatch)
    renamed = probe.index("coordination_path.rename(second_displaced_path)", finished)
    range_available = probe.index("_assert_exclusive_available", renamed)
    moved_identity = probe.index(
        "identity_probe.identity(moved_replacement) == replacement_identity",
        range_available,
    )
    assert (
        test
        < original
        < substituted
        < replacement
        < started
        < mismatch
        < finished
        < renamed
        < range_available
        < moved_identity
    )


def test_m181_cleanup_is_bounded_exact_and_has_no_retry_or_delay() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "process.wait(timeout=_TIMEOUT_SECONDS)",
        "process.kill()",
        "_close_participant(guardian)",
        "stream.closed",
        "identity_probe.owned_count == 0",
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


def test_m181_decision_records_admission_boundary_not_identity_authority() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-expected-identity-guardian-admission-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "expected identity",
        "not trusted identity provenance",
        "not generation authority",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT / "docs/rfcs/0164-probe-windows-expected-identity-guardian-admission.md"
    ).read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "no retry or sleep" in " ".join(rfc.casefold().split())


def test_m181_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-expected-identity-guardian-admission-probe"
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
    assert "0164-probe-windows-expected-identity-guardian-admission.md" in rfc_index
