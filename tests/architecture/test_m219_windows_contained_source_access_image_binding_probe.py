"""Protect M219's contained source-access image-binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_contained_source_access_image_binding_probe.py"
_DECISION = (
    _ROOT / "docs/security/windows-cache-cleanup-contained-source-access-image-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0202-probe-windows-contained-source-access-image-binding.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0201-probe-windows-contained-source-access-refusal.md": (
        "3aa13c2f3d01e4796f66481db571eb5b7b7ffe2f54eb268d445737f489461bc0"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-refusal-probe.md": (
        "a02ada5233ab6a919acd22ec8b5cea29360eded657727b5a9c2fedd27d18fb47"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m218_windows_contained_source_access_refusal_probe.py": (
        "e6fbda74b5b16d2813c729181cac0ec7ae6c978e80754b159ffefc79cc683515"
    ),
    "tests/fixtures/windows_contained_source_access_contender.py": (
        "76600561f6f3bf93dadf4b57175e78904c04d5d4815c92b409a84cb8e69192c0"
    ),
    "tests/integration/test_windows_contained_source_access_refusal_probe.py": (
        "d5f6709c73af3a545c2ab647f43f68a3f5bf3360137a5eec13830861ad0b0ed7"
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


def test_m219_changes_no_runtime_dependency_ci_fixture_or_m218_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m219_contained_source_access_image_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m219_retains_expected_image_before_suspended_creation() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def run_image_bound_contender") :]
    retained_expected = body.index("_RetainedImageFile(_DIRECT_PYTHON)")
    expected_snapshot = body.index("expected_image_file.snapshot()")
    created = body.index("self._create_process(")
    assigned = body.index("self._assign_process(")
    job_membership = body.index("self._process_is_in_job(")
    controller_binding = body.index("_RetainedTokenBinding(0)")
    contender_binding = body.index("_RetainedTokenBinding(process)")
    same_logon = body.index("_verify_same_logon(controller, contender)")
    retained_observed = body.index("_RetainedProcessImage(process)")
    observed_snapshot = body.index("observed_image.snapshot()")
    expected_match = body.index("_verify_expected_image(expected_image, image_before)")
    resumed = body.index("self._resume_thread(")
    waited = body.index("self.wait_process(process)", resumed)
    expected_stable = body.index(
        "_verify_image_stable(expected_image, expected_image_file.snapshot())",
        waited,
    )
    observed_stable = body.index(
        "observed_image._image.snapshot(",
        expected_stable,
    )
    assert (
        retained_expected
        < expected_snapshot
        < created
        < assigned
        < job_membership
        < controller_binding
        < contender_binding
        < retained_observed
        < same_logon
        < observed_snapshot
        < expected_match
        < resumed
        < waited
        < expected_stable
        < observed_stable
    )


def test_m219_preserves_exact_containment_and_settlement() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_contender_command_line()",
        "False,",
        "_CREATE_SUSPENDED | _CREATE_NO_WINDOW",
        "assert self.accounting(job) == (1, 1)",
        "assert self.process_ids(job) == (process_id,)",
        "assert self.exit_code(process) == _STILL_ACTIVE",
        "_require_contender_exit(exit_code, phase=phase)",
        "assert self.exit_code(process) == 0",
        "assert self.wait_job_empty(job) == (1, 0)",
        "assert self.owned_count == 0",
    ):
        assert required in source


def test_m219_runs_image_bound_refusal_at_three_ordered_phases() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[
        source.index("def test_contained_source_access_image_binding_preserves_boundary") :
    ]
    before = body.index('phase="before_launch"')
    start = body.index("_start_or_skip(probe)")
    connected = body.index('phase="after_connection"')
    challenge = body.index("_challenge(probe, session)")
    ready = body.index('phase="after_ready"')
    release = body.index('_canonical_document("release", session.challenge, 2)')
    settle = body.index("probe.settle(session, 0)")
    allowed = body.index("_require_source_access_allowed(_PARTICIPANT)")
    assert before < start < connected < challenge < ready < release < settle < allowed
    assert body.count("_require_image_bound_source_access_refused(") == 3
    for required in (
        "_verify_same_logon(controller, participant)",
        "_NativeSessionBinding().verify(session.pipe, session.pid, participant)",
        "probe._verify_pipe_dacl(",
        "_verify_expected_image(expected_image, image_before)",
        "_verify_token_stable(participant, participant_binding.snapshot())",
        "_verify_image_stable(expected_image, expected_image_file.snapshot())",
        "_verify_image_stable(image_before, observed_image.snapshot())",
        "_verify_source_stable(source_before, source_file.snapshot())",
        "assert probe.owned_count == 0",
    ):
        assert required in body
    assert "assert image_probe.owned_count == 0" in source


def test_m219_is_test_only_offline_nonmutating_and_non_authorizing() -> None:
    assert _imports(_PROBE).isdisjoint({"http", "socket", "subprocess", "urllib"})
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "WriteFile",
        "DeleteFile",
        "MoveFile",
        "ReplaceFile",
        "unlink(",
        "rename(",
        "replace(",
        "write_bytes(",
        "write_text(",
        "sys.remote_exec",
        "remote_exec(",
        "PyRemoteDebug",
        "ReadProcessMemory",
        "WriteProcessMemory",
        "CreateRemoteThread",
        "VirtualAllocEx",
        "LogonUser",
        "CreateProcessAsUser",
        "CreateProcessWithLogon",
        "AdjustTokenPrivileges",
        "ImpersonateNamedPipeClient",
        "shell=True",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source


def test_m219_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "contained source-access image binding",
        "expected interpreter image is retained before launch",
        "observed process image is retained before resume",
        "normalized name",
        "volume and file identity",
        "bounded size",
        "sha-256",
        "both retained image handles remain stable after child settlement",
        "does not bind contender script bytes",
        "source-commit provenance remains unproved",
        "imported standard-library module bytes remain unbound",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m219_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "does not establish source or build provenance" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m219_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-image-binding-probe"
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
    assert "0202-probe-windows-contained-source-access-image-binding.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m219_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "contained-source-access-image-binding-probe",
        "contender-image-binding",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_contained_source_access_image.py",
        "src/ludoweave/platform/windows_process_image.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
