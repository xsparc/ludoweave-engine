"""Protect M154's test-only native sharing-violation boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0136-probe-windows-share-delete-exclusion.md": (
        "b9fcb48752dc51a66ef5b8c5245a39d7f03b4c858b685eb0b2e69ca8823a5975"
    ),
    "docs/security/cache-cleanup-windows-share-delete-exclusion-probe.md": (
        "57aa6c26387ba3a1739bbe9499ec5640473218bc7830f51fd1c7cb0a71f92225"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m153_windows_share_delete_exclusion_probe.py": (
        "72c36302cda822db16a57cfca7213d8a82151af7134719d5498ad025c9fd9b1f"
    ),
    "tests/integration/test_windows_cache_cleanup_share_delete_probe.py": (
        "41877f26d92168b802c0b7d712b2fccb524fd9c3dcee913fc9e254921b8f440c"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "1921748b24fe4c1b696c7e10d452b6f3e4093384d237bca001dfe1c0b74900ac",
    "scripts": "b0794063b12244ffb5d3845e710e50b1e7452964136fc0efd86e455ea5f83456",
    "src/ludoweave": "e6c951393b86b0673a25e0f6b1f4cf41224d3cb7807dd85c76aad482820cde36",
}


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


def test_m154_changes_no_runtime_example_script_dependency_ci_or_m153_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m154_native_child_is_fixed_isolated_test_only_and_not_installed() -> None:
    child_path = _ROOT / "tests/fixtures/windows_share_delete_rename_child.py"
    child = child_path.read_text(encoding="utf-8")
    for required in (
        '"MoveFileExW"',
        '"live"',
        '"displaced"',
        "get_last_error()",
        'sys.platform != "win32"',
        '"ludoweave.test.windows-native-rename/1"',
    ):
        assert required in child
    for forbidden in ("sys.argv", "input(", "os.environ", "subprocess", "eval(", "exec("):
        assert forbidden not in child

    metadata = (_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'packages = ["src/ludoweave"]' in metadata
    assert "windows_share_delete_rename_child" not in metadata


def test_m154_probe_exercises_bounded_direct_native_result_transition() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_native_error_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        "_filesystem_information",
        "_ShareDeleteProbe",
        '(sys.executable, "-I", "-B", str(_CHILD))',
        "close_fds=True",
        "cwd=working_directory",
        "shell=False",
        "stdin=subprocess.DEVNULL",
        "timeout=15.0",
        "_MAX_CHILD_OUTPUT_BYTES = 512",
        "completed.stderr",
        "set(document)",
        "_ERROR_SHARING_VIOLATION = 32",
        "probe.release(blocker)",
        "succeeded=False",
        "succeeded=True",
        "probe.owned_count == 0",
    ):
        assert required in probe
    assert probe.count("_attempt_native_child_rename(tmp_path)") == 2
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m154_documents_narrow_direct_native_error_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-native-sharing-violation-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "direct current-host error evidence",
        "error returns can vary",
        "no `-c` evaluation",
        "missing admission evidence",
        "no hosted check is added",
    ):
        assert required in compact


def test_m154_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0137-probe-windows-native-sharing-violation.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "windows is not admitted" in " ".join(rfc.casefold().split())
    for path in (
        "docs/readme-history.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        content = (_ROOT / path).read_text(encoding="utf-8")
        assert "cache-cleanup-windows-native-sharing-violation-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0137-probe-windows-native-sharing-violation.md" in rfc_index
