"""Protect M218's test-only contained source-access refusal boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_contained_source_access_refusal_probe.py"
_CONTENDER = _ROOT / "tests/fixtures/windows_contained_source_access_contender.py"
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-contained-source-access-refusal-probe.md"
_RFC = _ROOT / "docs/rfcs/0201-probe-windows-contained-source-access-refusal.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0200-probe-windows-retained-launch-source-remote-debug-exclusion.md": (
        "0dca2ce92ee53871596bf4d5d3dbed643d641e6f1e18f85ccbb1e4446c35652a"
    ),
    "docs/security/windows-cache-cleanup-retained-launch-source-remote-debug-exclusion-probe.md": (
        "ac132746c1a8c0c54242c1c14806a19e275650f6fc7922b1125181522ca7a0cb"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m217_windows_remote_debug_exclusion_probe.py": (
        "dc14bd81a245d64a52a4d0de5405c400521bca2febc246ac465f3dc508ad2464"
    ),
    "tests/fixtures/windows_local_control_channel_participant.py": (
        "b3e33d4e70fef4fa3acc3fbb3e8526705c5625b7865344a2a63243415194f452"
    ),
    "tests/integration/test_windows_remote_debug_exclusion_probe.py": (
        "5d5d33f7fcdb20e8030a650b5d4b71fb06294c0f040ef706989463e38a596b37"
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


def test_m218_changes_no_runtime_dependency_ci_participant_or_m217_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m218_contained_source_access_refusal_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _CONTENDER.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m218_uses_a_fixed_argument_free_direct_contender() -> None:
    contender = _CONTENDER.read_text(encoding="utf-8")
    probe = _PROBE.read_text(encoding="utf-8")
    for required in (
        'Path(__file__).with_name("windows_local_control_channel_participant.py")',
        "if len(sys.argv) != 1:",
        "_GENERIC_WRITE",
        "_DELETE",
        "_ERROR_SHARING_VIOLATION",
        "CreateFileW",
        "OPEN_EXISTING",
    ):
        assert required in contender
    for required in (
        "_DIRECT_PYTHON",
        "-I -B",
        "_CONTENDER",
        "False,",
        "_CREATE_SUSPENDED | _CREATE_NO_WINDOW",
    ):
        assert required in probe


def test_m218_assigns_suspended_same_logon_contender_before_resume() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def run_contender") :]
    created = body.index("self._create_process(")
    assigned = body.index("self._assign_process(")
    job_membership = body.index("self._process_is_in_job(")
    controller_binding = body.index("_RetainedTokenBinding(0)")
    contender_binding = body.index("_RetainedTokenBinding(process)")
    same_logon = body.index("_verify_same_logon(controller, contender)")
    resumed = body.index("self._resume_thread(")
    waited = body.index("self.wait_process(process)", resumed)
    assert (
        created
        < assigned
        < job_membership
        < controller_binding
        < contender_binding
        < same_logon
        < resumed
        < waited
    )
    for required in (
        "assert self.accounting(job) == (1, 1)",
        "assert self.process_ids(job) == (process_id,)",
        "assert self.exit_code(process) == _STILL_ACTIVE",
        "assert self.exit_code(process) == 0",
        "assert self.wait_job_empty(job) == (1, 0)",
        "assert self.owned_count == 0",
    ):
        assert required in source


def test_m218_runs_contained_refusal_at_three_ordered_live_phases() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def test_contained_source_access_refusal_preserves_boundary") :]
    before = body.index('phase="before_launch"')
    start = body.index("_start_or_skip(probe)")
    connected = body.index('phase="after_connection"')
    challenge = body.index("_challenge(probe, session)")
    ready = body.index('phase="after_ready"')
    release = body.index('_canonical_document("release", session.challenge, 2)')
    settle = body.index("probe.settle(session, 0)")
    allowed = body.index("_require_source_access_allowed(_PARTICIPANT)")
    assert before < start < connected < challenge < ready < release < settle < allowed
    assert body.count("_require_contained_source_access_refused(") == 3
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
    assert "assert contender_probe.owned_count == 0" in source


def test_m218_contender_is_access_only_offline_and_non_authorizing() -> None:
    assert _imports(_CONTENDER).isdisjoint({"http", "socket", "subprocess", "urllib"})
    assert _imports(_PROBE).isdisjoint({"http", "socket", "subprocess", "urllib"})
    combined = _CONTENDER.read_text(encoding="utf-8") + _PROBE.read_text(encoding="utf-8")
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
        assert forbidden not in combined


def test_m218_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "job-contained same-logon child process",
        "access-only createfilew requests",
        "write and delete access",
        "error_sharing_violation",
        "assigned while suspended",
        "job_object_limit_kill_on_job_close",
        "one assigned process and one active process",
        "source bytes remain unchanged",
        "does not prove a distinct security principal",
        "source-commit provenance remains unproved",
        "imported standard-library module bytes remain unbound",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m218_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "performs no write, delete, rename, or replacement operation" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m218_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-refusal-probe"
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
    assert "0201-probe-windows-contained-source-access-refusal.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m218_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "contained-source-access-refusal-probe",
        "source-access-contender",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_contained_source_access.py",
        "src/ludoweave/platform/windows_source_access.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
