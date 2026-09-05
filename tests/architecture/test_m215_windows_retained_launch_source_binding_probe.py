"""Protect M215's test-only Windows retained launch-source boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_retained_launch_source_binding_probe.py"
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-retained-launch-source-binding-probe.md"
_RFC = _ROOT / "docs/rfcs/0198-probe-windows-retained-launch-source-binding.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0197-probe-windows-retained-process-image-binding.md": (
        "6ce7eb4f5be85f09e4760ecb9901ce55ae3b77b1ef3ed76073edfe3059f607e3"
    ),
    "docs/security/windows-cache-cleanup-retained-process-image-binding-probe.md": (
        "5657eb4cc01a67660166ab493721b6c6978f37055a13d3af87bc831ac8a394d0"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m214_windows_retained_process_image_binding_probe.py": (
        "d0632c5662c579bb045207944527a4a3869215f60b92805dec9da96834249c64"
    ),
    "tests/fixtures/windows_local_control_channel_participant.py": (
        "b3e33d4e70fef4fa3acc3fbb3e8526705c5625b7865344a2a63243415194f452"
    ),
    "tests/integration/test_windows_local_control_channel_probe.py": (
        "a71451ba5600a0bc0a5e2d2ce126af31e5cd9a28770476f618d087c0bf2a320e"
    ),
    "tests/integration/test_windows_local_control_token_binding_probe.py": (
        "0f4c3e5d701b68b225adc9c6b9735efe4940c3d528caf05521c219128e1172ee"
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


def test_m215_changes_no_runtime_dependency_ci_or_m214_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m215_retained_launch_source_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m215_uses_documented_explicit_inheritance_surface() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002",
        "_EXTENDED_STARTUPINFO_PRESENT = 0x00080000",
        "_STARTF_USESTDHANDLES = 0x00000100",
        "InitializeProcThreadAttributeList",
        "UpdateProcThreadAttribute",
        "DeleteProcThreadAttributeList",
        "GetHandleInformation",
        "_HANDLE_FLAG_INHERIT",
        "CreateProcessW",
    ):
        assert required in source


def test_m215_executes_retained_source_as_isolated_standard_input() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    fixed_command = source[
        source.index("def _fixed_command_line(") : source.index(
            "def _require_exact_standard_handles("
        )
    ]
    launch = source[source.index("    def launch_suspended(") : source.index("def test_")]
    assert 'str(_DIRECT_PYTHON), "-I", "-B", "-", pipe_name' in fixed_command
    assert "str(_PARTICIPANT)" not in launch
    assert "startup.StartupInfo.hStdInput = wintypes.HANDLE(self._source.handle)" in launch
    assert "startup.StartupInfo.dwFlags = _STARTF_USESTDHANDLES" in launch
    assert "self._source.rewind()" in launch


def test_m215_inherits_exactly_three_fixed_standard_handles() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    launch = source[source.index("    def launch_suspended(") : source.index("def test_")]
    assert "_require_exact_standard_handles(standard_handles)" in launch
    assert "self._attribute_list(standard_handles)" in launch
    assert "True," in launch
    assert "_EXTENDED_STARTUPINFO_PRESENT" in launch
    assert "NUL" in source
    assert "inherited standard handles were not exact" in source


def test_m215_retains_and_rechecks_source_across_ready() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def test_retained_launch_source_is_stable") :]
    assert body.index("_InheritedLaunchSource(_PARTICIPANT)") < body.index("_start_or_skip(probe)")
    assert body.index("source_before = source_file.snapshot()") < body.index(
        "_start_or_skip(probe)"
    )
    assert body.index("_challenge(probe, session)") < body.index(
        "_verify_source_stable(source_before, source_file.snapshot())"
    )
    assert body.index("_verify_source_stable(source_before, source_file.snapshot())") < (
        body.index('_canonical_document("release", session.challenge, 2)')
    )
    assert "retained launch source changed before release" in source


def test_m215_source_read_is_bounded_private_and_handle_owned() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_IMAGE_BYTES",
        "_READ_CHUNK_BYTES",
        "self.close()",
        "self._close_handle",
        "source_file.snapshot()",
    ):
        assert required in source
    for forbidden in ("read_bytes(", "print(", "json.dumps", "pathlib.Path.open"):
        assert forbidden not in source


def test_m215_rejects_unstable_remote_process_introspection() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "NtQueryInformationProcess",
        "ReadProcessMemory",
        "PROCESS_VM_READ",
        "ProcessCommandLineInformation",
        "RTL_USER_PROCESS_PARAMETERS",
    ):
        assert forbidden not in source


def test_m215_native_surface_is_test_only_offline_and_non_authorizing() -> None:
    assert _imports(_PROBE).isdisjoint({"http", "socket", "subprocess", "urllib"})
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "LogonUser",
        "CreateProcessAsUser",
        "CreateProcessWithLogon",
        "AdjustTokenPrivileges",
        "ImpersonateNamedPipeClient",
        "DeleteFile",
        "MoveFile",
    ):
        assert forbidden not in source


def test_m215_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "retained launch-source handle",
        "participant source bytes are read from inherited standard input",
        "exact three-handle allowlist",
        "imported standard-library module bytes remain unbound",
        "source-commit provenance remains unproved",
        "does not prove hostile aba resistance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m215_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "no distinct-principal or independent-host run has occurred" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m215_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-retained-launch-source-binding-probe"
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
    assert "0198-probe-windows-retained-launch-source-binding.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m215_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "retained-launch-source-probe",
        "inherit-launch-source",
        "windows-source-bind",
        "windows-host-harness",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_retained_launch_source.py",
        "src/ludoweave/assets/launch_source.py",
        "src/ludoweave/platform/windows_source_binding.py",
    ):
        assert not (_ROOT / path).exists()
