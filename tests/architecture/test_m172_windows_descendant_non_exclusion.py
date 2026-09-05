"""Protect M172's Windows directory/descendant non-exclusion boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0154-probe-windows-exclusive-root-acquisition.md": (
        "4be34008110a3a09b0acfc26112480da1b942fa4ec427374786fadd1416d5f1a"
    ),
    "docs/security/cache-cleanup-windows-exclusive-root-acquisition-probe.md": (
        "6ea3e25dae3bb488af2939a79640c99e14f958e911adf492ffeebcbf3c6d83a3"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m171_windows_exclusive_root_acquisition.py": (
        "c3208f58bccc36d3faf8067020dfc94292204142d134e75a65b17cd0a59dee10"
    ),
    "tests/fixtures/windows_exclusive_directory_open_child.py": (
        "763bc2dbb558f244c4050fc1529c5158bdb5890c34f4d75185c65e32665c8e22"
    ),
    "tests/fixtures/windows_share_delete_blocker_child.py": (
        "be8da81a030f5de9490410e23d67147d777368f4b66e10cc580103add41b8f5d"
    ),
    "tests/integration/test_windows_cache_cleanup_capability_probe.py": (
        "151c2e0a102c622fdb66d4d78ee803564b26081a0da34b76341e86596e11d973"
    ),
    "tests/integration/test_windows_cache_cleanup_child_owned_blocker_probe.py": (
        "c5feb520a1a6b95f8f819e743f82327f9bd59d42c93b4e5189660d418def75f7"
    ),
    "tests/integration/test_windows_cache_cleanup_exclusive_root_acquisition_probe.py": (
        "336fb747fa2b748fed2d3b5d21b4230dc7629b317658986be88816d6826ce552"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_PROBE = _ROOT / "tests/integration/test_windows_cache_cleanup_descendant_non_exclusion_probe.py"
_CHILD = _ROOT / "tests/fixtures/windows_descendant_file_holder_child.py"


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


def test_m172_changes_no_runtime_dependency_ci_or_m171_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m172_child_owns_only_one_fixed_noninheritable_descendant() -> None:
    child = _CHILD.read_text(encoding="utf-8")
    for required in (
        '_SCHEMA = "ludoweave.test.windows-descendant-file-holder/1"',
        '_FILE_NAME = r"live\\candidate.bin"',
        "_GENERIC_READ = 0x80000000",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE",
        "os.get_handle_inheritable(handle)",
        '_emit("ready")',
        "sys.stdin.buffer.read(1) != _RELEASE_TOKEN",
        "close_handle(wintypes.HANDLE(handle))",
        '_emit("closed")',
    ):
        assert required in child
    create_call = child.index("raw_handle = create_file(")
    null_security = child.index("        None,", create_call)
    open_existing = child.index("        _OPEN_EXISTING,", null_security)
    assert create_call < null_security < open_existing
    for forbidden in ("sys.argv", "input(", "subprocess", "os.environ", "pathlib", "Path("):
        assert forbidden not in child


def test_m172_root_first_keeps_both_owners_live_until_independent_close() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_exclusive_root_does_not_refuse_late_descendant_holder")
    root = probe.index("probe.open_directory_exclusive(live_path)", test)
    child = probe.index("holder = _start_holder(tmp_path)", root)
    ready = probe.index('_read_ready(holder) == "ready"', child)
    simultaneous = probe.index("probe.owned_count == 1", ready)
    child_close = probe.index('_release_and_read_closed(holder) == "closed"', simultaneous)
    root_still_owned = probe.index("probe.owned_count == 1", child_close)
    root_close = probe.index("probe.release(exclusive)", root_still_owned)
    assert test < root < child < ready < simultaneous < child_close < root_still_owned < root_close
    assert 'payload = b"m172-root-first-descendant"' in probe[test:]


def test_m172_descendant_first_keeps_both_owners_live_until_independent_close() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_existing_descendant_holder_does_not_refuse_exclusive_root")
    child = probe.index("holder = _start_holder(tmp_path)", test)
    ready = probe.index('_read_ready(holder) == "ready"', child)
    root = probe.index("probe.open_directory_exclusive(live_path)", ready)
    simultaneous = probe.index("holder.poll() is None", root)
    root_close = probe.index("probe.release(exclusive)", simultaneous)
    child_still_live = probe.index("holder.poll() is None", root_close)
    child_close = probe.index('_release_and_read_closed(holder) == "closed"', child_still_live)
    assert test < child < ready < root < simultaneous < root_close < child_still_live < child_close
    assert 'payload = b"m172-descendant-first-root"' in probe[test:]


def test_m172_processes_and_cleanup_are_bounded_without_timing_or_shells() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        "close_fds=True",
        "shell=False",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "timeout=_TIMEOUT_SECONDS",
        "finally:",
        "_close_holder(holder)",
        "probe.owned_count == 0",
    ):
        assert required in probe
    for forbidden in (
        "close_fds=False",
        "shell=True",
        "os.system",
        "time.sleep",
        "communicate(",
        '"-c"',
        "env=",
        "cmd.exe",
    ):
        assert forbidden not in probe


def test_m172_decision_records_exact_negative_capability_boundary() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-descendant-non-exclusion-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "not a subtree lock",
        "negative capability evidence",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0155-probe-windows-descendant-non-exclusion.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "windows is not admitted" in " ".join(rfc.casefold().split())
    assert "does not recursively exclude access" in " ".join(rfc.casefold().split())


def test_m172_public_boundary_is_registered_without_ci_expansion() -> None:
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
        assert "cache-cleanup-windows-descendant-non-exclusion-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0155-probe-windows-descendant-non-exclusion.md" in rfc_index
