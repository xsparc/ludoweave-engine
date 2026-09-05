"""Protect M211's test-only Windows participant-containment boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PARTICIPANT = _ROOT / "tests/fixtures/windows_independent_host_process_tree_participant.py"
_PROBE = _ROOT / "tests/integration/test_windows_independent_host_process_containment_probe.py"
_DECISION = (
    _ROOT / "docs/security/windows-cache-cleanup-independent-host-process-containment-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0194-probe-windows-independent-host-process-containment.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0193-adopt-windows-independent-host-collection-plan-validator.md": (
        "2e3574fa3ecf6f209b32a14d5306c689d543ce0ea554cf450524a4ba7c008d69"
    ),
    "docs/security/windows-cache-cleanup-independent-host-collection-plan-validator.md": (
        "8e339d49aaf25da9fab8d2276edebdb67ccc968527f638e4908cac79b07baa10"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m210_windows_independent_host_collection_plan_validator.py": (
        "b166e81e82b730ea3162ac1e9644b72bd891ae380237d826371b234740388cda"
    ),
    "tests/fixtures/windows_cleanup_independent_host_collection_plan.json": (
        "c9c8e2f082583d4458d6a7a0b56d34c5d373149d15e3e9ca9528a5bdc915e8c6"
    ),
    "tests/integration/test_windows_independent_host_collection_plan.py": (
        "eb93e42125c7a7f0363ac490d5c011012e50cf970aa4be4cc034f753265ca310"
    ),
    "tests/tools/validate_windows_independent_host_collection_plan.py": (
        "bc773a81b10b0df6c0ff0f8ccd3f22d9c11eb6a1d66de69520294b45abdc0ed5"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
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


def test_m211_changes_no_runtime_dependency_ci_or_m210_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m211_test_only_process_containment_boundary_exists() -> None:
    assert _PARTICIPANT.is_file()
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m211_root_is_suspended_assigned_then_resumed() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    launch = source[source.index("    def launch_tree(") : source.index("    def terminate_job(")]
    assert "_PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002" in source
    for required in (
        "CreateProcessW",
        "_CREATE_SUSPENDED",
        "_EXTENDED_STARTUPINFO_PRESENT",
        "self._attribute_list((output_write,))",
        "self._assign_process",
        "self._process_is_in_job",
        "available.value == 0",
        "self._resume_thread",
        "previous_suspend_count == 1",
    ):
        assert required in launch
    assert launch.index("self._assign_process") < launch.index("self._resume_thread")
    assert "CREATE_BREAKAWAY_FROM_JOB" not in source
    assert "JOB_OBJECT_LIMIT_BREAKAWAY_OK" not in source
    assert "JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK" not in source


def test_m211_job_has_exact_membership_and_fail_safe_limits() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "CreateJobObjectW",
        "_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE",
        "AssignProcessToJobObject",
        "IsProcessInJob",
        "Job Object contained an unexpected process",
        "self.process_ids(job)",
        "self.accounting(job) == (2, 2)",
        "TerminateJobObject",
        "WaitForSingleObject",
        "probe.wait_job_empty(job) == (2, 0)",
    ):
        assert required in source


def test_m211_retains_root_and_descendant_handles_not_pid_only_termination() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "root_handle=root",
        "descendant_handle=descendant",
        "OpenProcess",
        "GetProcessId",
        "probe.wait_process(tree.root_handle)",
        "probe.wait_process(tree.descendant_handle)",
        "probe.close_handle(tree.root_handle)",
        "probe.close_handle(tree.descendant_handle)",
    ):
        assert required in source
    assert "os.kill" not in source
    assert "taskkill" not in source.casefold()


def test_m211_uses_fixed_direct_interpreters_and_one_private_output_handle() -> None:
    participant = _PARTICIPANT.read_text(encoding="utf-8")
    probe = _PROBE.read_text(encoding="utf-8")
    assert '_DIRECT_PYTHON = Path(sys.base_prefix) / "pythonw.exe"' in probe
    assert "self._attribute_list((output_write,))" in probe
    assert 'Path(sys.executable).with_name("pythonw.exe")' in participant
    assert "subprocess.Popen" not in participant
    assert 'sys.argv[1] in {"participant", "descendant"}' in participant
    assert "CreateProcessW" in participant
    assert "shell=True" not in participant


def test_m211_native_surface_is_test_only_offline_and_non_privileged() -> None:
    assert _imports(_PARTICIPANT).isdisjoint({"http", "socket", "urllib"})
    assert _imports(_PROBE).isdisjoint({"http", "socket", "urllib"})
    for source in (
        _PARTICIPANT.read_text(encoding="utf-8"),
        _PROBE.read_text(encoding="utf-8"),
    ):
        for forbidden in (
            "LogonUser",
            "CreateProcessAsUser",
            "CreateProcessWithLogon",
            "AdjustTokenPrivileges",
            "OpenSCManager",
            "WinHttp",
            "WSAStartup",
        ):
            assert forbidden not in source


def test_m211_has_explicit_termination_and_last_close_observations() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for test_name in (
        "test_job_scoped_termination_settles_exact_process_tree",
        "test_last_job_handle_close_is_a_fail_safe_for_the_tree",
    ):
        assert f"def {test_name}()" in source
    assert "current host does not permit the required nested Job Object" in source
    assert "_ERROR_ACCESS_DENIED" in source


def test_m211_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "current-host test evidence",
        "no independent-host collection has occurred",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "pid termination",
        "any extra process invalidates the observation",
        "vm power cut remains external hypervisor authority",
        "physical power loss remains operator-only",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m211_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "no independent-host run has occurred" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m211_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-independent-host-process-containment-probe"
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
    assert "0194-probe-windows-independent-host-process-containment.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m211_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "independent-host-collect",
        "process-containment-probe",
        "terminate-job",
        "windows-host-harness",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_independent_host_process_containment.py",
        "src/ludoweave/assets/collection_harness.py",
        "src/ludoweave/assets/process_containment.py",
        "src/ludoweave/assets/windows_job.py",
    ):
        assert not (_ROOT / path).exists()
