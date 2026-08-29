"""Protect M186's independent Windows hard-link alias mutator ABA boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0168-probe-windows-hard-link-alias-delete-recreate-aba.md": (
        "954c72078a6d21bde044dad5668075aaa71e887a3ede99bd8ca962ace11b48ea"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-delete-recreate-aba-probe.md": (
        "2d4fedab0be5f56ea8ff69953f765483f7f9d5854eb798d3da563284375c251e"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m185_windows_hard_link_alias_delete_recreate_aba_boundary.py": (
        "2242fbdeb4ac05f6d40ba822477a4bff44ce69dcca0f5318dc146f34191b17ee"
    ),
    "tests/fixtures/windows_coordination_identity_guardian_child.py": (
        "c244b29a120d61c957faa2e6d6a16b7482f85da214879f61ae56fc5e92ef6007"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_delete_recreate_aba_probe.py": (
        "f668ed811f9954a5afc981ea9a4a845a3ba6836bd523a63eec96c320cb88a835"
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
    / "tests/integration/test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe.py"
)
_FIXTURE = _ROOT / "tests/fixtures/windows_hard_link_alias_mutator_child.py"


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


def test_m186_changes_no_runtime_dependency_ci_or_m185_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m186_parent_only_coordinates_two_distinct_child_processes() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "guardian = _start_identity_guardian",
        "mutator = _start_alias_mutator",
        "assert mutator.pid != guardian.pid",
        "assert mutator.pid != os.getpid()",
        '== "deleted"',
        '== "recreated"',
        '== "closed"',
    ):
        assert required in probe
    for forbidden in (
        "alias_path.unlink()",
        "os.unlink(alias_path)",
        "shell=True",
        "env=",
    ):
        assert forbidden not in probe
    assert probe.count("os.link(coordination_path, alias_path)") == 1
    assert probe.index("os.link(coordination_path, alias_path)") < probe.index(
        "guardian = _start_identity_guardian"
    )


def test_m186_fixture_has_fixed_names_and_exact_fail_closed_protocol() -> None:
    fixture = _FIXTURE.read_text(encoding="utf-8")
    for required in (
        r'_SOURCE_NAME = r"live\coordination.lock"',
        r'_ALIAS_NAME = r"peer\coordination.alias"',
        "if len(sys.argv) != 1:",
        "os.unlink(_ALIAS_NAME)",
        '_emit("deleted")',
        "sys.stdin.buffer.read(1) != _RECREATE_TOKEN",
        "os.link(_SOURCE_NAME, _ALIAS_NAME)",
        '_emit("recreated")',
        "sys.stdin.buffer.read(1) != _CLOSE_TOKEN",
        '_emit("closed")',
    ):
        assert required in fixture
    for forbidden in (
        "import ctypes",
        "subprocess",
        "socket",
        "eval(",
        "exec(",
        "os.system",
        "shell=True",
    ):
        assert forbidden not in fixture


def test_m186_launch_is_isolated_bounded_and_argument_free() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    launch = probe.index("def _start_alias_mutator")
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"')
    launch_text = probe[launch:deleted]
    for required in (
        '(sys.executable, "-I", "-B", str(_CHILD))',
        "close_fds=True",
        "cwd=working_directory",
        "shell=False",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "_MAX_LINE_BYTES = 192",
        "_TIMEOUT_SECONDS = 15.0",
    ):
        assert required in probe
    for forbidden in ("env=", "pass_fds=", "handle_list", "creationflags="):
        assert forbidden not in launch_text


def test_m186_orders_child_owned_delete_recreate_and_exact_closure() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    guardian_ready = probe.index('_read_identity_guardian_event(guardian) == "ready"')
    mutator_started = probe.index("mutator = _start_alias_mutator", guardian_ready)
    deleted = probe.index('_read_alias_mutator_event(mutator) == "deleted"', mutator_started)
    one_link = probe.index("identity_probe.link_count(original) == 1", deleted)
    recreated = probe.index(
        '_send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"', one_link
    )
    original_two = probe.index("identity_probe.link_count(original) == 2", recreated)
    alias_two = probe.index("identity_probe.link_count(alias) == 2", original_two)
    mutator_closed = probe.index('_close_alias_mutator(mutator) == "closed"', alias_two)
    guardian_still_live = probe.index("assert guardian.poll() is None", mutator_closed)
    guardian_closed = probe.index(
        '_release_identity_guardian(guardian) == "closed"', guardian_still_live
    )
    fixed_renamed = probe.index("coordination_path.rename(displaced_path)", guardian_closed)
    assert (
        guardian_ready
        < mutator_started
        < deleted
        < one_link
        < recreated
        < original_two
        < alias_two
        < mutator_closed
        < guardian_still_live
        < guardian_closed
        < fixed_renamed
    )


def test_m186_preserves_identity_bytes_liveness_ranges_and_cleanup() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "assert mutator.poll() is None",
        "assert guardian.poll() is None",
        "identity_probe.identity(original) == original_identity",
        "identity_probe.identity(alias) == original_identity",
        "identity_probe.identity(displaced) == original_identity",
        "identity_probe.link_count(original) == 1",
        "identity_probe.link_count(original) == 2",
        "identity_probe.link_count(alias) == 2",
        "coordination_path.read_bytes() == payload",
        "alias_path.read_bytes() == payload",
        "displaced_path.read_bytes() == payload",
        "_assert_exclusive_available(lock_probe, coordination_path)",
        "_assert_exclusive_available(lock_probe, alias_path)",
        "blocked_after_mutator_close.value.winerror == _ERROR_SHARING_VIOLATION",
        "for process in (mutator, guardian):",
        "stream.closed",
        "identity_probe.owned_count == 0",
        "lock_probe.owned_count == 0",
        "assert not coordination_path.exists()",
    ):
        assert required in probe
    for forbidden in ("time.sleep", "retry", "communicate(", "shell=True", "env="):
        assert forbidden not in probe


def test_m186_records_three_process_same_principal_limit() -> None:
    decision = (
        _ROOT
        / "docs/security/cache-cleanup-windows-independent-hard-link-alias-mutator-aba-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "three-process, same-principal",
        "parent only coordinates and observes",
        "not root-confined ownership",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (
        _ROOT / "docs/rfcs/0169-probe-windows-independent-hard-link-alias-mutator-aba.md"
    ).read_text(encoding="utf-8")
    rfc_compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "parent coordinator, guardian child, and mutator child" in rfc_compact
    assert "does not establish cross-principal behavior" in rfc_compact
    assert "no retry or sleep" in rfc_compact


def test_m186_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-independent-hard-link-alias-mutator-aba-probe"
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
    assert "0169-probe-windows-independent-hard-link-alias-mutator-aba.md" in rfc_index
