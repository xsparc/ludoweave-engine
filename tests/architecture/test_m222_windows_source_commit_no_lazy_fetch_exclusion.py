"""Protect M222's no-lazy-fetch exclusion for fixed Git object reads."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_no_lazy_fetch_probe.py"
)
_SOURCE_COMMIT_PROBE = (
    _ROOT / "tests/integration/test_windows_contained_source_access_source_commit_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-no-lazy-fetch-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0205-exclude-git-lazy-fetch-from-source-commit-probe.md"
_M221_SOURCE_COMMIT_PROBE_SHA256 = (
    "00d63acbe5a8cb2cba06a2a063d502f197557d717dc9ff3b9c384f81e9a1be62"
)
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0204-probe-windows-contained-source-access-source-commit-binding.md": (
        "2382888bc043038d86a30ed59916b76e0a39ff73503fe1bd4da34d6489a8ea36"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-binding-probe.md": (
        "0b33424f5b1abe73c09b5312882398605475ac7ea3bfad011e22f20995b10845"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m221_windows_contained_source_access_source_commit_binding_probe.py": (
        "2b03b42afb2e6cf0fdca14cd495f16279af1ab16cfb1bc61b6b0d13f3920d68a"
    ),
    "tests/fixtures/windows_contained_source_access_bound_contender.py": (
        "fa01dae3119f817c62d0b27b0f575642c9837ad5259d79507bd2a1c09c41d2dd"
    ),
    "tests/integration/test_windows_contained_source_access_source_binding_probe.py": (
        "750a5bb3547ebe20fc36f92041a5876dd5a6358eceece797edee740d6172509c"
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


def test_m222_changes_no_runtime_dependency_ci_fixture_or_m221_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m222_no_lazy_fetch_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m222_hardens_m221_reader_by_exactly_two_lines() -> None:
    source = _SOURCE_COMMIT_PROBE.read_text(encoding="utf-8")
    command_line = '                "--no-lazy-fetch",\n'
    environment_line = '            "GIT_NO_LAZY_FETCH": "1",\n'
    assert source.count(command_line) == 1
    assert source.count(environment_line) == 1
    restored = source.replace(command_line, "").replace(environment_line, "")
    assert hashlib.sha256(restored.encode()).hexdigest() == _M221_SOURCE_COMMIT_PROBE_SHA256


def test_m222_git_reader_has_dual_no_lazy_fetch_exclusion_in_order() -> None:
    source = _SOURCE_COMMIT_PROBE.read_text(encoding="utf-8")
    body = source[source.index("def _run_git") : source.index("def _git_line")]
    command = body[body.index("subprocess.run(") :]
    positions = [
        command.index('"--no-pager"'),
        command.index('"--no-replace-objects"'),
        command.index('"--no-lazy-fetch"'),
        command.index('"-C"'),
        command.index("str(_ROOT)"),
        command.index("*arguments"),
    ]
    assert positions == sorted(positions)
    environment = source[source.index("def _git_environment") : source.index("def _run_git")]
    assert 'not name.upper().startswith("GIT_")' in environment
    assert environment.count('"GIT_NO_LAZY_FETCH": "1"') == 1


def test_m222_regression_exercises_command_environment_and_full_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "def test_no_lazy_fetch_exclusion_preserves_m221_boundary",
        "_commit_module.test_committed_source_binding_preserves_m220_boundary()",
        "def test_git_reader_passes_dual_no_lazy_fetch_exclusion",
        'patch.object(_commit_module.subprocess, "run"',
        'command.count("--no-lazy-fetch") == 1',
        'environment["GIT_NO_LAZY_FETCH"] == "1"',
        "def test_git_environment_rejects_ambient_lazy_fetch_override",
        '"GIT_NO_LAZY_FETCH": "0"',
        '"GIT_OBJECT_DIRECTORY": "ambient-object-directory"',
        '"LUDOWEAVE_M222_SENTINEL": "preserved"',
    ):
        assert required in source


def test_m222_regression_is_windows_only_test_only_and_non_authorizing() -> None:
    assert _imports(_PROBE).issubset(
        {
            "__future__",
            "os",
            "subprocess",
            "sys",
            "unittest",
            "typing",
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


def test_m222_documentation_states_corrected_offline_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "source-commit no-lazy-fetch exclusion",
        "--no-lazy-fetch",
        "git_no_lazy_fetch=1",
        "promisor remote",
        "m221's source-commit reader",
        "historical m221 evidence is not rewritten",
        "trusted git executable and local object store remain outside",
        "not a source provenance attestation",
        "build provenance remains unproved",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m222_rfc_is_accepted_corrective_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "corrective" in compact
    assert "both the command-line option and environment variable" in compact
    assert "does not establish a slsa source attestation or build provenance" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m222_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-no-lazy-fetch-probe"
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
    assert "0205-exclude-git-lazy-fetch-from-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m222_adds_no_runtime_git_network_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "source-commit-no-lazy-fetch",
        "git-no-lazy-fetch",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_reader.py",
        "src/ludoweave/platform/git_source.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
