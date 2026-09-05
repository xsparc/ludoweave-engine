"""Protect M174's Windows cooperative-lock substitution boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0156-probe-windows-cooperative-lock.md": (
        "fbf518f3d24961cf17f8e114b4fa6c3b8a68cbb3c68ef8b9e22a7dfb0322dca9"
    ),
    "docs/security/cache-cleanup-windows-cooperative-lock-probe.md": (
        "87b46e0c67d100200a2ce852861e011beebd1d6fb8dd7458fef3ee37818d11ae"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m173_windows_cooperative_lock.py": (
        "1cff19552ac5f0c9634c22866d42a4d5132364c4413ad7786b15ae77b052860a"
    ),
    "tests/fixtures/windows_coordination_lock_participant_child.py": (
        "edd544660138b0637c6fd66934f9f3458e76a2d3aa9c4ffd25924ee5a3768d84"
    ),
    "tests/integration/test_windows_cache_cleanup_cooperative_lock_probe.py": (
        "d0ea6af78537cd60d1e6da35e6d9db8f17416d93e9034e8f8d25f2c3b2a1c044"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_PROBE = (
    _ROOT / "tests/integration/test_windows_cache_cleanup_cooperative_lock_substitution_probe.py"
)
_CHILD = _ROOT / "tests/fixtures/windows_coordination_lock_substitution_child.py"


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


def test_m174_changes_no_runtime_dependency_ci_or_m173_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m174_child_is_fixed_native_bounded_and_noninheritable() -> None:
    child = _CHILD.read_text(encoding="utf-8")
    for required in (
        '"MoveFileExW"',
        '"CreateFileW"',
        '"WriteFile"',
        '_SOURCE_NAME = r"live\\coordination.lock"',
        '_DISPLACED_NAME = r"live\\coordination.displaced"',
        '_PAYLOAD = b"ludoweave-m173-coordination-v1\\n"',
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE",
        "os.get_handle_inheritable(handle)",
        '_emit("substituted")',
    ):
        assert required in child
    for forbidden in (
        "sys.argv",
        "input(",
        "os.environ",
        "subprocess",
        "pathlib",
        "Path(",
        "eval(",
        "exec(",
    ):
        assert forbidden not in child


def test_m174_probe_proves_identity_split_and_independent_generations() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    test = probe.index("def test_path_substitution_splits_cooperative_lock_generations")
    original_ready = probe.index('_read_event(original_participant) == ("ready", 0)', test)
    mutation = probe.index("_attempt_substitution(tmp_path)", original_ready)
    same_identity = probe.index("original_identity == displaced_identity", mutation)
    different_identity = probe.index("replacement_identity != original_identity", same_identity)
    replacement_ready = probe.index(
        '_read_event(replacement_participant) == ("ready", 0)', different_identity
    )
    old_refused = probe.index("lock_probe.acquire_exclusive(displaced_path)", replacement_ready)
    new_refused = probe.index("lock_probe.acquire_exclusive(coordination_path)", old_refused)
    replacement_close = probe.index(
        "_release_and_read_closed(replacement_participant)", new_refused
    )
    replacement_exclusive = probe.index(
        "replacement_exclusive = lock_probe.acquire_exclusive(coordination_path)",
        replacement_close,
    )
    old_still_refused = probe.index(
        "lock_probe.acquire_exclusive(displaced_path)", replacement_exclusive
    )
    original_close = probe.index(
        "_release_and_read_closed(original_participant)", old_still_refused
    )
    displaced_exclusive = probe.index(
        "displaced_exclusive = lock_probe.acquire_exclusive(displaced_path)",
        original_close,
    )
    assert (
        test
        < original_ready
        < mutation
        < same_identity
        < different_identity
        < replacement_ready
        < old_refused
        < new_refused
        < replacement_close
        < replacement_exclusive
        < old_still_refused
        < original_close
        < displaced_exclusive
    )


def test_m174_processes_and_output_are_bounded_without_timing_or_shells() -> None:
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        '(sys.executable, "-I", "-B", str(_CHILD))',
        "capture_output=True",
        "close_fds=True",
        "shell=False",
        "stdin=subprocess.DEVNULL",
        "timeout=_TIMEOUT_SECONDS",
        "_MAX_CHILD_OUTPUT_BYTES = 256",
        "finally:",
        "_close_participant(original_participant)",
        "lock_probe.owned_count == 0",
    ):
        assert required in probe
    for forbidden in (
        "close_fds=False",
        "shell=True",
        "os.system",
        "time.sleep",
        '"-c"',
        "env=",
        "cmd.exe",
    ):
        assert forbidden not in probe


def test_m174_decision_records_negative_not_authoritative_boundary() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-cooperative-lock-substitution-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "negative capability evidence",
        "not cleanup authority",
        "no hosted check is added",
    ):
        assert required in compact

    rfc = (_ROOT / "docs/rfcs/0157-probe-windows-cooperative-lock-substitution.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "independent lock generations" in " ".join(rfc.casefold().split())
    assert "reusable pathname" in " ".join(rfc.casefold().split())


def test_m174_public_boundary_is_registered_without_ci_expansion() -> None:
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
        assert "cache-cleanup-windows-cooperative-lock-substitution-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0157-probe-windows-cooperative-lock-substitution.md" in rfc_index
