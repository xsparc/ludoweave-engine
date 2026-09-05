"""Protect M217's test-only retained-source remote-debug exclusion boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_remote_debug_exclusion_probe.py"
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-retained-launch-source-remote-debug-exclusion-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0200-probe-windows-retained-launch-source-remote-debug-exclusion.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0199-probe-windows-retained-launch-source-access-refusal.md": (
        "1d91a0b95f533d72bb1f0647af034d525ebfd2c30969081d19faa3d62d3fb00f"
    ),
    "docs/security/windows-cache-cleanup-retained-launch-source-access-refusal-probe.md": (
        "3340cda1909236553d29228d26fc2e13510d11892ba0d74e56800b90dcbcfca2"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m216_windows_retained_launch_source_access_refusal_probe.py": (
        "e12c3be9ccd271b4f3000d1580236b91c34ef29e70bb2c533291c5eac64a5ad0"
    ),
    "tests/fixtures/windows_local_control_channel_participant.py": (
        "b3e33d4e70fef4fa3acc3fbb3e8526705c5625b7865344a2a63243415194f452"
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


def test_m217_changes_no_runtime_dependency_ci_fixture_or_m216_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m217_remote_debug_exclusion_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m217_composes_exact_fixed_direct_launch() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_M215_FIXED_COMMAND_LINE(",
        "_launch_source_module._fixed_command_line",
        "f'\"{_DIRECT_PYTHON}\" -I -B -X disable_remote_debug - {pipe_name}'",
        "patch.object(",
        '"_fixed_command_line"',
        "_start_or_skip(probe)",
    ):
        assert required in source


def test_m217_preserves_full_retained_source_lifecycle() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[
        source.index("def test_remote_debug_exclusion_preserves_retained_source_boundary") :
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
    assert body.count("_require_source_access_refused(") == 3
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


def test_m217_performs_no_remote_attach_injection_or_mutation() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "sys.remote_exec",
        "remote_exec(",
        "PyRemoteDebug",
        "OpenProcess",
        "ReadProcessMemory",
        "WriteProcessMemory",
        "CreateRemoteThread",
        "VirtualAllocEx",
        "WriteFile",
        "DeleteFile",
        "MoveFile",
        "ReplaceFile",
        "unlink(",
        "rename(",
        "replace(",
        "write_bytes(",
        "write_text(",
    ):
        assert forbidden not in source


def test_m217_native_surface_is_test_only_offline_and_non_authorizing() -> None:
    assert _imports(_PROBE).isdisjoint({"http", "socket", "subprocess", "urllib"})
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "LogonUser",
        "CreateProcessAsUser",
        "CreateProcessWithLogon",
        "AdjustTokenPrivileges",
        "ImpersonateNamedPipeClient",
    ):
        assert forbidden not in source


def test_m217_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "remote-debug exclusion",
        "-x disable_remote_debug",
        "python 3.14",
        "python 3.12 and 3.13",
        "does not attempt remote attachment, code injection, or process-memory access",
        "retained launch-source access refusal",
        "same-process cooperative observation",
        "source-commit provenance remains unproved",
        "imported standard-library module bytes remain unbound",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m217_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "performs no remote attachment, injection, or memory access" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m217_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-retained-launch-source-remote-debug-exclusion-probe"
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
    assert "0200-probe-windows-retained-launch-source-remote-debug-exclusion.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m217_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "remote-debug-exclusion-probe",
        "disable-remote-debug",
        "windows-host-harness",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_remote_debug_exclusion.py",
        "src/ludoweave/platform/windows_remote_debug.py",
        "src/ludoweave/tools/remote_debug.py",
    ):
        assert not (_ROOT / path).exists()
