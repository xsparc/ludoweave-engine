"""Protect M185's Windows hard-link alias delete/recreate ABA boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0167-probe-windows-hard-link-alias-deletion-non-exclusion.md": (
        "7cc83e407ea6444b99dfb702a75d6dbea565c9dad41f4ff73d050736385f5521"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-deletion-non-exclusion-probe.md": (
        "6d7231e00b56075358d2e5bedc95421dadc0be8e397d7a90b3a8aef10f9ed200"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m184_windows_hard_link_alias_deletion_non_exclusion_boundary.py": (
        "2a82a7f375272a9c72eeef60264933a69c124cf2aafcb4e67f92bf01787bd42f"
    ),
    "tests/fixtures/windows_coordination_identity_guardian_child.py": (
        "c244b29a120d61c957faa2e6d6a16b7482f85da214879f61ae56fc5e92ef6007"
    ),
    "tests/integration/test_windows_cache_cleanup_capability_probe.py": (
        "151c2e0a102c622fdb66d4d78ee803564b26081a0da34b76341e86596e11d973"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_probe.py": (
        "d0ea6af78537cd60d1e6da35e6d9db8f17416d93e9034e8f8d25f2c3b2a1c044"
    ),
    "tests/integration/test_windows_cache_cleanup_expected_identity_guardian_admission_probe.py": (
        "8eb5e5b2bc4d554c3e3da3a01e238d27666a1da5e263501be93e0ae364ad0de0"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_deletion_non_exclusion_probe.py": (
        "ca6cd98879f1270aa0418179e4092b24530468129bd5faba3126a89cfcab5c21"
    ),
    "tests/integration/test_windows_cache_cleanup_protected_guardian_handoff_probe.py": (
        "5f570f9e57de824cf0f08ec0694b539e4b435262b462504894394187ed3c3d18"
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
    / "tests/integration/test_windows_cache_cleanup_hard_link_alias_delete_recreate_aba_probe.py"
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


def test_m185_changes_no_runtime_dependency_ci_or_corrected_m184_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m185_reuses_guardian_and_capability_helpers_without_native_duplication() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "os.link(coordination_path, alias_path)",
        "alias_path.unlink()",
        "_WindowsCapabilityProbe",
        "_CoordinationLockProbe",
        "_create_fixture",
        "_start_identity_guardian",
        "_read_identity_guardian_event",
        "_release_identity_guardian",
        "_assert_exclusive_available",
    ):
        assert required in probe
    for forbidden in (
        "import ctypes",
        "subprocess.Popen(",
        "env=",
        "os.system",
        "shell=True",
    ):
        assert forbidden not in probe


def test_m185_establishes_two_matching_names_before_guardian_admission() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    linked = probe.index("os.link(coordination_path, alias_path)")
    original_identity = probe.index("original_identity =", linked)
    alias_identity = probe.index("identity_probe.identity(alias) == original_identity")
    original_links = probe.index("identity_probe.link_count(original) == 2", alias_identity)
    alias_links = probe.index("identity_probe.link_count(alias) == 2", original_links)
    started = probe.index("guardian = _start_identity_guardian", alias_links)
    ready = probe.index('_read_identity_guardian_event(guardian) == "ready"', started)
    assert (
        linked < original_identity < alias_identity < original_links < alias_links < started < ready
    )


def test_m185_orders_delete_recreate_aba_and_persistent_fixed_name_refusal() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    blocked = probe.index("with pytest.raises(OSError) as blocked_coordination:", ready)
    deleted = probe.index("alias_path.unlink()", blocked)
    absent = probe.index("assert not alias_path.exists()", deleted)
    one_link = probe.index("identity_probe.link_count(original) == 1", absent)
    recreated = probe.index("os.link(coordination_path, alias_path)", one_link)
    alias_opened = probe.index('"coordination.alias", delete_access=False', recreated)
    original_two = probe.index("identity_probe.link_count(original) == 2", alias_opened)
    alias_two = probe.index("identity_probe.link_count(alias) == 2", original_two)
    blocked_again = probe.index(
        "with pytest.raises(OSError) as still_blocked_coordination:", alias_two
    )
    closed = probe.index('_release_identity_guardian(guardian) == "closed"', blocked_again)
    fixed_renamed = probe.index("coordination_path.rename(displaced_path)", closed)
    assert (
        ready
        < blocked
        < deleted
        < absent
        < one_link
        < recreated
        < alias_opened
        < original_two
        < alias_two
        < blocked_again
        < closed
        < fixed_renamed
    )


def test_m185_preserves_identity_bytes_link_counts_liveness_and_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "assert guardian.poll() is None",
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


def test_m185_records_delete_recreate_aba_and_process_correction() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-hard-link-alias-delete-recreate-aba-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "pathname-membership aba",
        "2 -> 1 -> 2",
        "two-process, same-principal",
        "not root-confined ownership",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0168-probe-windows-hard-link-alias-delete-recreate-aba.md").read_text(
        encoding="utf-8"
    )
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "parent process and the guardian is a child process" in rfc_compact
    assert "no retry or sleep" in rfc_compact


def test_m185_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-hard-link-alias-delete-recreate-aba-probe"
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
    assert "0168-probe-windows-hard-link-alias-delete-recreate-aba.md" in rfc_index
