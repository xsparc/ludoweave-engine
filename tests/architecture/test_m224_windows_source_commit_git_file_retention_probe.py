"""Protect M224's retained Git executable file boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_file_retention_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-file-retention-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0207-retain-git-executable-file-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0206-bind-git-executable-selection-for-source-commit-probe.md": (
        "94b681dab85077e584d2abefb2b5eacb80ae7b4f32c13cce6080c5e04d495484"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-selection-binding-probe.md": (
        "6c62516559d6f60483233d0f41387743e891bd119f789861024a412a2a530805"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m223_windows_source_commit_git_selection_binding_probe.py": (
        "1989cc341cfd9b91db2177d2f1a7157bb4728fda816c30331d35d08bfa080b61"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_selection_binding_probe.py": (
        "dc7825e95cf3260b117cef97298086807ecd22fd86839597ee34219f9932be7b"
    ),
    "tests/integration/test_windows_retained_launch_source_access_refusal_probe.py": (
        "d6da5fe5a77d50bf7416e1b18f0afe034bb593b3f7b3a3bab501a72c026549c2"
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


def test_m224_preserves_runtime_ci_and_complete_m223_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m224_git_file_retention_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m224_opens_one_noninheritable_read_only_git_handle() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "class _RetainedGitExecutableFile(_RetainedImageFile)",
        "self._api.create_file(",
        "_GENERIC_READ,",
        "_FILE_SHARE_READ,",
        "None,",
        "_OPEN_EXISTING,",
        "_FILE_ATTRIBUTE_NORMAL,",
        'self.handle = _handle_value(raw, "CreateFileW")',
    ):
        assert required in source


def test_m224_retains_identity_and_refuses_replacement_access() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before = retained.snapshot()",
        "_selection_module._require_git_selection_bound_m222_boundary()",
        "_verify_image_stable(before, retained.snapshot())",
        "with _RetainedImageFile(git_executable) as settled:",
        "_verify_image_stable(before, settled.snapshot())",
        "def test_git_file_retainer_refuses_replacement_access_without_mutation",
        "probe_file = Path(__file__).resolve(strict=True)",
        "with _RetainedGitExecutableFile(probe_file) as retained:",
        '_require_source_access_refused(probe_file, phase="retained_probe")',
        "_require_source_access_allowed(probe_file)",
    ):
        assert required in source


def test_m224_performs_one_real_selection_before_retention() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "real_which = _commit_module.shutil.which",
        "side_effect=real_which",
        "git_executable = _commit_module._git_executable()",
        "lookup.call_count == 1",
        '_commit_module, "_git_executable", return_value=git_executable',
        "selection.call_count == 1",
    ):
        assert required in source


def test_m224_probe_is_windows_only_test_only_and_non_authorizing() -> None:
    assert _imports(_PROBE).issubset(
        {
            "__future__",
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


def test_m224_documentation_preserves_file_retention_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "git executable file retention",
        "one non-inheritable read-only handle",
        "file_share_read",
        "all 48 fixed git object reads",
        "write and delete/rename access",
        "does not authenticate the executable",
        "native dll and loader identity remain outside",
        "local object store remains outside",
        "not a source provenance attestation",
        "build provenance remains unproved",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m224_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "retain the selected git executable file" in compact
    assert "does not establish executable authenticity or provenance" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m224_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-git-file-retention-probe"
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
    assert "0207-retain-git-executable-file-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m224_adds_no_runtime_git_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-file-retention",
        "git-executable-retention",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_retainer.py",
        "src/ludoweave/platform/git_source.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
