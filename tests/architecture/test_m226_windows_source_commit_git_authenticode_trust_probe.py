"""Protect M226's retained-handle Git Authenticode trust boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_authenticode_trust_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-authenticode-trust-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0209-verify-git-authenticode-trust-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0208-bind-git-child-image-for-source-commit-probe.md": (
        "682211c9514d2043916e63b75bf87b31f448fb2d636fdeeee81697e43da2acdc"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-child-image-binding-probe.md": (
        "9c660e9f986a9eeacf6d607e15bba2d92b5d8bec103f69e342645e856bd53299"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m225_windows_source_commit_git_child_image_binding_probe.py": (
        "a386fb689c14cfe84fcd8396a6ab90092e667e58d10b78e3575be8f54fc375cf"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_child_image_binding_probe.py": (
        "2a71dd1a486e2ed117b02b90544ce71d292345ffacb62c8131632a16d5666535"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "benchmarks": "d55f1c0d5da18cb4ed72bd94713525e5c76ee64738ff5110935ee389e6a4f771",
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}


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


def _compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    return imported


def test_m226_preserves_runtime_ci_and_complete_m225_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m226_authenticode_trust_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m226_verifies_the_retained_git_file_handle() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_WINTRUST_ACTION_GENERIC_VERIFY_V2",
        "class _WINTRUST_FILE_INFO",
        "wintypes.HANDLE(handle)",
        "file_info.pcwszFilePath",
        "file_info.hFile",
        "status = cast(",
        "self._win_verify_trust(",
        "if status != _ERROR_SUCCESS:",
    ):
        assert required in source


def test_m226_is_noninteractive_cache_only_and_revocation_explicit() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_WTD_UI_NONE = 2",
        "_WTD_REVOKE_NONE = 0",
        "_WTD_CACHE_ONLY_URL_RETRIEVAL = 0x00001000",
        "_WTD_REVOCATION_CHECK_NONE = 0x00000010",
        "trust_data.dwUIChoice = _WTD_UI_NONE",
        "trust_data.fdwRevocationChecks = _WTD_REVOKE_NONE",
        "_WTD_CACHE_ONLY_URL_RETRIEVAL | _WTD_REVOCATION_CHECK_NONE",
    ):
        assert required in source


def test_m226_closes_every_trust_provider_state() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_WTD_STATEACTION_VERIFY = 0x00000001",
        "_WTD_STATEACTION_CLOSE = 0x00000002",
        "finally:",
        "trust_data.dwStateAction = _WTD_STATEACTION_CLOSE",
        "close_status = cast(",
        "trust provider state close failed",
        "assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]",
    ):
        assert required in source


def test_m226_composes_the_complete_m225_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before = retained.snapshot()",
        "verifier.verify(git_executable, retained.handle)",
        "_m225_module.test_git_child_images_match_the_retained_m224_executable()",
        "assert lookup.call_count == 1",
        "_verify_image_stable(before, retained.snapshot())",
        "verifier.verify(git_executable, retained.handle)",
    ):
        assert required in source


def test_m226_probe_is_windows_only_test_only_and_non_mutating() -> None:
    assert _imports(_PROBE).issubset(
        {
            "__future__",
            "collections",
            "ctypes",
            "pathlib",
            "sys",
            "typing",
            "unittest",
            "pytest",
            "tests",
        }
    )
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "http",
        "socket",
        "urllib",
        "requests",
        "shell=True",
        "git checkout",
        "git reset",
        "git clean",
        "git update-ref",
        "git fetch",
        "git pull",
        "git push",
        "unlink(",
        "rename(",
        "replace(",
        "write_bytes(",
        "write_text(",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source


def test_m226_documentation_preserves_local_trust_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "retained-handle authenticode trust",
        "wintrust_action_generic_verify_v2",
        "cache-only url retrieval",
        "no user interface",
        "explicitly closes provider state",
        "complete m225 boundary",
        "does not allowlist a signer or publisher",
        "revocation freshness remains unproved",
        "native dll and loader identity remain outside",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m226_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "verify retained git authenticode trust" in compact
    assert "does not establish signer or publisher authorization" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m226_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = (
        "windows-cache-cleanup-contained-source-access-source-commit-git-authenticode-trust-probe"
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
        assert slug in (_ROOT / path).read_text(encoding="utf-8")
    assert "0209-verify-git-authenticode-trust-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m226_adds_no_runtime_git_trust_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-authenticode-trust",
        "git-signer-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_authenticode.py",
        "src/ludoweave/platform/git_trust.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
