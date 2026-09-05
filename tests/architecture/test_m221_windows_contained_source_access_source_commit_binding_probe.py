"""Protect M221's contained source-access source-commit binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT / "tests/integration/test_windows_contained_source_access_source_commit_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0204-probe-windows-contained-source-access-source-commit-binding.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0203-probe-windows-contained-source-access-source-binding.md": (
        "93ea4821403d2d94bb260c12c5b43de9be88cb9bff9e53bcaee64403b6cc54ad"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-binding-probe.md": (
        "be607279310e425398e438c7ddd8e8a1a235dc286bfd79d95254dc9f657718e9"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m220_windows_contained_source_access_source_binding_probe.py": (
        "d28c229b7f545aadc3f8052edcf1efafa3ccc5ae7a17b871175ab957b5a01da6"
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


def test_m221_changes_no_runtime_dependency_ci_fixture_or_m220_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m221_contained_source_access_source_commit_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m221_commit_descriptor_is_exact_and_ref_free() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    compact_source = "".join(source.split())
    for required in (
        '_M220_COMMIT = "734d4eb943c3da7a1a8357ef3e180cac4353cb6b"',
        '_M220_TREE = "5575eeeb8123a0eaed9028a6281227b64fdfb73d"',
        '_M220_PARENT = "09e6d3390040498371912d7d47bff5b75be03c35"',
        '_M220_SOURCE_PATH = "tests/fixtures/windows_contained_source_access_bound_contender.py"',
        '_M220_SOURCE_BLOB = "10b71fc7d2d555160bf4a2869190a0b3e66d3330"',
        "_M220_SOURCE_BYTES = 3252",
        '_M220_SOURCE_SHA256 = bytes.fromhex("fa01dae3119f817c62d0b27b0f575642c9837ad5259d79507bd2a1c09c41d2dd")',
    ):
        assert "".join(required.split()) in compact_source
    for forbidden in ('"HEAD"', '"main"', '"origin/main"', "git describe"):
        assert forbidden not in source


def test_m221_git_reader_is_fixed_bounded_sanitized_and_no_shell() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def _run_git") : source.index("def _git_line")]
    for required in (
        "subprocess.run(",
        '"--no-pager"',
        '"--no-replace-objects"',
        '"-C"',
        "str(_ROOT)",
        "stdin=subprocess.DEVNULL",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        "shell=False",
        "check=False",
        "timeout=_GIT_TIMEOUT_SECONDS",
        "creationflags=_CREATE_NO_WINDOW",
        "env=_git_environment()",
        "len(completed.stdout) > max_output_bytes",
        'completed.stderr != b""',
    ):
        assert required in body
    environment = source[source.index("def _git_environment") : source.index("def _run_git")]
    for required in (
        'not name.upper().startswith("GIT_")',
        '"GIT_CONFIG_NOSYSTEM": "1"',
        '"GIT_CONFIG_GLOBAL": os.devnull',
        '"GIT_CONFIG_SYSTEM": os.devnull',
        '"GIT_NO_REPLACE_OBJECTS": "1"',
        '"GIT_OPTIONAL_LOCKS": "0"',
        '"GIT_TERMINAL_PROMPT": "0"',
    ):
        assert required in environment


def test_m221_resolves_exact_commit_tree_parent_path_and_blob() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def _load_committed_source") :]
    ordered = (
        '_git_line("cat-file", "-t", _M220_COMMIT)',
        'f"{_M220_COMMIT}^{{commit}}"',
        'f"{_M220_COMMIT}^{{tree}}"',
        'f"{_M220_COMMIT}^"',
        'f"{_M220_COMMIT}:{_M220_SOURCE_PATH}"',
        '_git_line("cat-file", "-t", _M220_SOURCE_BLOB)',
        '_git_line("cat-file", "-s", _M220_SOURCE_BLOB)',
        '_run_git("cat-file", "blob", _M220_SOURCE_BLOB',
        "hashlib.sha256(blob).digest()",
    )
    positions = [body.index(item) for item in ordered]
    assert positions == sorted(positions)


def test_m221_verifies_commit_before_launch_and_after_settlement() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def _require_committed_source_bound_access_refused") :]
    retained = body.index("_InheritedLaunchSource(_SOURCE_BOUND_CONTENDER)")
    committed_before = body.index("_load_committed_source()")
    snapshot_before = body.index("source_file.snapshot()")
    verified_before = body.index("_verify_committed_source(")
    launched = body.index("probe.run_source_bound_contender(")
    committed_after = body.index("_load_committed_source()", committed_before + 1)
    stable_commit = body.index("assert committed_after == committed_before")
    snapshot_after = body.index("source_file.snapshot()", snapshot_before + 1)
    verified_after = body.index("_verify_committed_source(", verified_before + 1)
    access = body.index("_require_source_access_allowed(_SOURCE_BOUND_CONTENDER)")
    assert (
        retained
        < committed_before
        < snapshot_before
        < verified_before
        < launched
        < committed_after
        < stable_commit
        < snapshot_after
        < verified_after
        < access
    )


def test_m221_preserves_m220_three_phase_participant_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def test_committed_source_binding_preserves_m220_boundary") :]
    compact_body = "".join(body.split())
    assert (
        'patch.object(_source_module,"_require_source_bound_source_access_refused"' in compact_body
    )
    assert "_source_module.test_contained_source_access_source_binding_preserves_boundary()" in body
    assert "_require_committed_source_bound_access_refused" in body


def test_m221_has_fail_closed_commit_and_source_mismatch_tests() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "def test_committed_source_descriptor_is_exact",
        "def test_committed_source_verifier_rejects_size_drift",
        "def test_committed_source_verifier_rejects_digest_drift",
        "with pytest.raises(RuntimeError, match=",
    ):
        assert required in source


def test_m221_is_test_only_offline_read_only_and_non_authorizing() -> None:
    assert _imports(_PROBE).issubset(
        {
            "__future__",
            "dataclasses",
            "hashlib",
            "os",
            "pathlib",
            "shutil",
            "subprocess",
            "sys",
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
        "WriteFile",
        "DeleteFile",
        "MoveFile",
        "ReplaceFile",
        "unlink(",
        "rename(",
        "replace(",
        "write_bytes(",
        "write_text(",
        "LogonUser",
        "CreateProcessAsUser",
        "AdjustTokenPrivileges",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source


def test_m221_documentation_preserves_non_attestation_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "contained source-access source-commit binding",
        "exact m220 commit",
        "commit, tree, parent, path, and blob",
        "retained source matches the committed blob before child creation",
        "committed blob remains stable after child settlement",
        "trusted git executable and local object store remain outside",
        "not a source provenance attestation",
        "build provenance remains unproved",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m221_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "does not establish a slsa source attestation or build provenance" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m221_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-binding-probe"
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
    assert "0204-probe-windows-contained-source-access-source-commit-binding.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m221_adds_no_runtime_git_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "contained-source-access-source-commit-binding-probe",
        "source-commit-binding",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_source_commit.py",
        "src/ludoweave/platform/git_source.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
