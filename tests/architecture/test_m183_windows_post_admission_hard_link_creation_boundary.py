"""Protect M183's Windows post-admission hard-link creation boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0165-probe-windows-hard-link-alias-non-exclusion.md": (
        "1308d41873045326771bfeeba1da1f594bfda4d0f667f744f6e8fe0c3337bd75"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-non-exclusion-probe.md": (
        "4e34edda25e1ae1bf695e081a685b33c95492a518fbd1194c319f72eddde6329"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m182_windows_hard_link_alias_non_exclusion_boundary.py": (
        "26dd1816897be03123110d23fd7ccc19c31041ede62801b711a325a35d4f5ed7"
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
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_non_exclusion_probe.py": (
        "d3af01c9ab45145fdd569b9403c59dbb04b287338b8ddfb07e4b7a2c2ecaa6f9"
    ),
    "tests/integration/test_windows_cache_cleanup_protected_guardian_handoff_probe.py": (
        "5f570f9e57de824cf0f08ec0694b539e4b435262b462504894394187ed3c3d18"
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
    / "tests/integration/test_windows_cache_cleanup_post_admission_hard_link_creation_probe.py"
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


def test_m183_changes_no_runtime_dependency_ci_or_m182_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m183_reuses_guardian_and_capability_helpers_without_native_duplication() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "os.link(coordination_path, alias_path)",
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


def test_m183_establishes_single_link_before_guardian_admission() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    original = probe.index("original_identity =")
    one_link = probe.index("identity_probe.link_count(original) == 1", original)
    started = probe.index("guardian = _start_identity_guardian", one_link)
    ready = probe.index('_read_identity_guardian_event(guardian) == "ready"', started)
    linked = probe.index("os.link(coordination_path, alias_path)", ready)
    assert original < one_link < started < ready < linked


def test_m183_orders_creation_identity_growth_and_persistent_fixed_refusal() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    blocked = probe.index("with pytest.raises(OSError) as blocked_coordination:", ready)
    sharing = probe.index("blocked_coordination.value.winerror", blocked)
    linked = probe.index("os.link(coordination_path, alias_path)", sharing)
    guardian_live = probe.index("assert guardian.poll() is None", linked)
    alias_identity = probe.index(
        "identity_probe.identity(alias) == original_identity", guardian_live
    )
    original_links = probe.index("identity_probe.link_count(original) == 2", alias_identity)
    alias_links = probe.index("identity_probe.link_count(alias) == 2", original_links)
    fixed_range = probe.index(
        "_assert_exclusive_available(lock_probe, coordination_path)", alias_links
    )
    alias_range = probe.index("_assert_exclusive_available(lock_probe, alias_path)", fixed_range)
    blocked_again = probe.index(
        "with pytest.raises(OSError) as still_blocked_coordination:", alias_range
    )
    sharing_again = probe.index("still_blocked_coordination.value.winerror", blocked_again)
    closed = probe.index('_release_identity_guardian(guardian) == "closed"', sharing_again)
    fixed_renamed = probe.index("coordination_path.rename(displaced_path)", closed)
    assert (
        ready
        < blocked
        < sharing
        < linked
        < guardian_live
        < alias_identity
        < original_links
        < alias_links
        < fixed_range
        < alias_range
        < blocked_again
        < sharing_again
        < closed
        < fixed_renamed
    )


def test_m183_preserves_identity_link_count_bytes_and_exact_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "identity_probe.identity(displaced) == original_identity",
        "identity_probe.identity(alias) == original_identity",
        "identity_probe.link_count(displaced) == 2",
        "identity_probe.link_count(alias) == 2",
        "displaced_path.read_bytes() == payload",
        "alias_path.read_bytes() == payload",
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


def test_m183_records_post_admission_link_set_non_exclusion() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-post-admission-hard-link-creation-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "post-admission",
        "link set is not frozen",
        "not root-confined ownership",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0166-probe-windows-post-admission-hard-link-creation.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "no retry or sleep" in " ".join(rfc.casefold().split())


def test_m183_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-post-admission-hard-link-creation-probe"
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
    assert "0166-probe-windows-post-admission-hard-link-creation.md" in rfc_index
