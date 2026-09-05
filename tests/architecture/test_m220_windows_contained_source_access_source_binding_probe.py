"""Protect M220's contained source-access source-binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_contained_source_access_source_binding_probe.py"
_CONTENDER = _ROOT / "tests/fixtures/windows_contained_source_access_bound_contender.py"
_DECISION = (
    _ROOT / "docs/security/windows-cache-cleanup-contained-source-access-source-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0203-probe-windows-contained-source-access-source-binding.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0202-probe-windows-contained-source-access-image-binding.md": (
        "d5daf74f1ca968cc413944142ef67376947a5ac5135e0fe2b266d13d43fead66"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-image-binding-probe.md": (
        "db229b1aff0b3bb6e67ac45d51052907da4b54ad716ac235f7c662a9ec80823f"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m219_windows_contained_source_access_image_binding_probe.py": (
        "0aff8522373eae645d1d544f34007b5a885d2ffda68c768d750201614bf7f651"
    ),
    "tests/integration/test_windows_contained_source_access_image_binding_probe.py": (
        "115e64cb45de12087869dcb73fb8f7387f1dddd99dc5c243572532a2f698b488"
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


def test_m220_changes_no_runtime_dependency_ci_or_m219_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m220_contained_source_access_source_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _CONTENDER.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m220_retains_exact_source_and_standard_handles_before_creation() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def _require_source_bound_source_access_refused") :]
    retained_source = body.index("_InheritedLaunchSource(_SOURCE_BOUND_CONTENDER)")
    output_handle = body.index("_InheritedNullHandle() as output_handle")
    error_handle = body.index("_InheritedNullHandle() as error_handle")
    invoked = body.index("run_source_bound_contender(")
    assert retained_source < output_handle < error_handle < invoked

    run = source[source.index("def run_source_bound_contender") :]
    source_snapshot = run.index("source_file.snapshot()")
    source_rewind = run.index("source_file.rewind()", source_snapshot)
    retained_image = run.index("_RetainedImageFile(_DIRECT_PYTHON)")
    exact_handles = run.index("_require_exact_standard_handles(standard_handles)")
    attribute_list = run.index("self._attribute_list(")
    standard_input = run.index("startup.StartupInfo.hStdInput")
    standard_output = run.index("startup.StartupInfo.hStdOutput")
    standard_error = run.index("startup.StartupInfo.hStdError")
    command = run.index("_source_bound_contender_command_line()")
    created = run.index("self._create_process(")
    assert (
        source_snapshot
        < source_rewind
        < retained_image
        < exact_handles
        < attribute_list
        < standard_input
        < standard_output
        < standard_error
        < command
        < created
    )
    for required in (
        "True,",
        "_CREATE_SUSPENDED | _CREATE_NO_WINDOW | _EXTENDED_STARTUPINFO_PRESENT",
        "source_file.handle",
        "output_handle.handle",
        "error_handle.handle",
        "_STARTF_USESTDHANDLES",
        "return f'\"{_DIRECT_PYTHON}\" -I -B -'",
    ):
        assert required in run or required in source
    assert (
        "_SOURCE_BOUND_CONTENDER"
        not in source[
            source.index("def _source_bound_contender_command_line") : source.index(
                "class _ContainedSourceBoundAccessProbe"
            )
        ]
    )


def test_m220_verifies_identity_and_source_before_resume_then_settles() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def run_source_bound_contender") :]
    assigned = body.index("self._assign_process(")
    membership = body.index("self._process_is_in_job(")
    controller = body.index("_RetainedTokenBinding(0)")
    contender = body.index("_RetainedTokenBinding(process)")
    observed_image = body.index("_RetainedProcessImage(process)")
    same_logon = body.index("_verify_same_logon(controller, contender)")
    image_match = body.index("_verify_expected_image(expected_image, image_before)")
    source_stable_before = body.index(
        "_verify_source_stable(source_before, source_file.snapshot())"
    )
    rewind_before_resume = body.index("source_file.rewind()", source_stable_before)
    resumed = body.index("self._resume_thread(")
    waited = body.index("self.wait_process(process)", resumed)
    source_stable_after = body.index(
        "_verify_source_stable(source_before, source_file.snapshot())",
        waited,
    )
    expected_stable = body.index(
        "_verify_image_stable(expected_image, expected_image_file.snapshot())",
        source_stable_after,
    )
    observed_stable = body.index("observed_image._image.snapshot(", expected_stable)
    job_empty = body.index("self.wait_job_empty(job)", observed_stable)
    zero_owned = body.index("assert self.owned_count == 0", job_empty)
    assert (
        assigned
        < membership
        < controller
        < contender
        < observed_image
        < same_logon
        < image_match
        < source_stable_before
        < rewind_before_resume
        < resumed
        < waited
        < source_stable_after
        < expected_stable
        < observed_stable
        < job_empty
        < zero_owned
    )
    for required in (
        "assert self.accounting(job) == (1, 1)",
        "assert self.process_ids(job) == (process_id,)",
        "assert self.exit_code(process) == _STILL_ACTIVE",
        "_require_contender_exit(exit_code, phase=phase)",
        "assert self.exit_code(process) == 0",
        "assert self.wait_job_empty(job) == (1, 0)",
        "_require_source_access_allowed(_SOURCE_BOUND_CONTENDER)",
    ):
        assert required in source


def test_m220_preserves_three_phase_participant_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[
        source.index("def test_contained_source_access_source_binding_preserves_boundary") :
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
    assert body.count("_require_source_bound_source_access_refused(") == 3
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


def test_m220_contender_is_fixed_access_only_and_argument_free() -> None:
    assert _imports(_CONTENDER).issubset(
        {"__future__", "collections", "ctypes", "pathlib", "sys", "typing"}
    )
    source = _CONTENDER.read_text(encoding="utf-8")
    for required in (
        'Path.cwd() / "tests/fixtures/windows_local_control_channel_participant.py"',
        "if len(sys.argv) != 1:",
        "(_GENERIC_WRITE, _DELETE)",
        "_ERROR_SHARING_VIOLATION = 32",
        "_OPEN_EXISTING = 3",
        "_COMPETING_SHARE_MODE",
    ):
        assert required in source
    for forbidden in (
        "sys.stdin",
        "sys.stdout",
        "sys.stderr",
        "os.environ",
        "argparse",
        "input(",
        "print(",
        "write(",
        "unlink(",
        "rename(",
        "replace(",
    ):
        assert forbidden not in source


def test_m220_is_test_only_offline_nonmutating_and_non_authorizing() -> None:
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


def test_m220_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "contained source-access source binding",
        "source is retained before child creation",
        "executed through inherited standard input",
        "exactly three inherited handles",
        "source snapshot remains stable after child settlement",
        "imported standard-library module bytes remain unbound",
        "source-commit provenance remains unproved",
        "build provenance remains unproved",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m220_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "does not establish source-commit or build provenance" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m220_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-binding-probe"
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
    assert "0203-probe-windows-contained-source-access-source-binding.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m220_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "contained-source-access-source-binding-probe",
        "contender-source-binding",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_contained_source_access_source.py",
        "src/ludoweave/platform/windows_launch_source.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
