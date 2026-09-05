"""Protect M225's suspended Git child process-image binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_child_image_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-child-image-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0208-bind-git-child-image-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0207-retain-git-executable-file-for-source-commit-probe.md": (
        "1809d2c69038fc2aab5a9e67bdd4dba6783c68b1f589d19e83a441781b158d04"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-file-retention-probe.md": (
        "0e0ed1005c7c903779f9c76d1f11596a413284aa72fe665846665625f81692e3"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m224_windows_source_commit_git_file_retention_probe.py": (
        "19b1e8d65eab56861f62e5789479d109ddc280f668019da26ce103528d27936f"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_file_retention_probe.py": (
        "c4ab1210d4e04d0d58aff66bc9fdaba305d63bb3e4d875f4006e68a1851e2208"
    ),
    "tests/integration/test_windows_retained_process_image_binding_probe.py": (
        "4f86ecf9664ec41648ceda08275959fa27ac1b7d645daf27c9963e6985b4a681"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "benchmarks": "d55f1c0d5da18cb4ed72bd94713525e5c76ee64738ff5110935ee389e6a4f771",
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
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


def test_m225_preserves_runtime_ci_and_complete_m224_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m225_child_image_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m225_observes_each_child_before_its_primary_thread_runs() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_CREATE_SUSPENDED = 0x00000004",
        "creation_flags | _CREATE_SUSPENDED",
        "observed_snapshot = _snapshot_retained_image(retained)",
        "_verify_expected_image(expected, observed_snapshot)",
        "previous_suspend_count = api.resume_thread(thread_handle)",
        "if previous_suspend_count != 1:",
    ):
        assert required in source


def test_m225_requires_exactly_48_stable_bound_images() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_EXPECTED_GIT_READS = 48",
        "assert creation.call_count == _EXPECTED_GIT_READS",
        "assert len(observations) == _EXPECTED_GIT_READS",
        "_verify_image_stable(snapshot, _snapshot_retained_image(retained))",
        "for retained, snapshot in reversed(observations):",
        "retained.close()",
    ):
        assert required in source


def test_m225_fails_closed_before_createprocess_returns_ownership() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "except BaseException:",
        "api.terminate_wait_and_close(process_handle, thread_handle)",
        "raise",
        "_TERMINATION_EXIT_CODE = 113",
        "_SETTLEMENT_TIMEOUT_MS = 5_000",
        "WaitForSingleObject",
        "CloseHandle",
    ):
        assert required in source


def test_m225_performs_one_selection_inside_m224_file_retention() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "real_which = _commit_module.shutil.which",
        "side_effect=real_which",
        "lookup.call_count == 1",
        "with _RetainedGitExecutableFile(git_executable) as expected_file:",
        "expected = expected_file.snapshot()",
        "_selection_module._require_git_selection_bound_m222_boundary()",
        "_verify_image_stable(expected, expected_file.snapshot())",
        "with _RetainedImageFile(git_executable) as settled:",
    ):
        assert required in source


def test_m225_probe_is_windows_only_test_only_and_non_mutating() -> None:
    assert _imports(_PROBE).issubset(
        {
            "__future__",
            "collections",
            "ctypes",
            "pathlib",
            "subprocess",
            "sys",
            "types",
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


def test_m225_documentation_preserves_process_image_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "git child process-image binding",
        "create_suspended",
        "before its primary thread runs",
        "all 48 fixed git object reads",
        "retained m224 executable",
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


def test_m225_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind each git child process image" in compact
    assert "does not establish executable authenticity or provenance" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m225_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = (
        "windows-cache-cleanup-contained-source-access-source-commit-git-child-image-binding-probe"
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
    assert "0208-bind-git-child-image-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m225_adds_no_runtime_git_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-child-image-binding",
        "git-image-binding",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_child_image.py",
        "src/ludoweave/platform/git_source.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
