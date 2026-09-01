"""Protect M213's test-only Windows retained-token binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_local_control_token_binding_probe.py"
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-local-control-token-binding-probe.md"
_RFC = _ROOT / "docs/rfcs/0196-probe-windows-local-control-token-binding.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0195-probe-windows-local-control-channel.md": (
        "88403c4f0ddd509f329a9978db632d170dff415b054a760f514043ea3b0b1e38"
    ),
    "docs/security/windows-cache-cleanup-local-control-channel-probe.md": (
        "b7b533e256b178166f841db3eb13f71638ff17a52e435ec434a85396a532cd03"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m212_windows_local_control_channel_probe.py": (
        "bd6134436c75216bd2f951b0a1f8bde504d02f053c352bcbb0f9b918c5fe641b"
    ),
    "tests/fixtures/windows_local_control_channel_participant.py": (
        "b3e33d4e70fef4fa3acc3fbb3e8526705c5625b7865344a2a63243415194f452"
    ),
    "tests/integration/test_windows_local_control_channel_probe.py": (
        "a71451ba5600a0bc0a5e2d2ce126af31e5cd9a28770476f618d087c0bf2a320e"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
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


def test_m213_changes_no_runtime_dependency_ci_or_m212_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m213_token_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m213_retains_and_queries_one_primary_process_token() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "OpenProcessToken",
        "GetTokenInformation",
        "_TOKEN_USER",
        "_TOKEN_LOGON_SID",
        "_TOKEN_STATISTICS",
        "_TOKEN_SESSION_ID",
        "_TOKEN_PRIMARY",
        "TOKEN_QUERY",
    ):
        assert required in source
    assert "session.process" in source
    assert "_RetainedTokenBinding(session.process) as binding" in source
    assert "self._close_handle(wintypes.HANDLE(token))" in source


def test_m213_binds_native_pipe_process_and_token_sessions() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "GetNamedPipeClientSessionId",
        "ProcessIdToSessionId",
        "participant.session_id",
        "pipe_session.value",
        "process_session.value",
        "participant user identity did not match the controller",
        "participant logon identity did not match the controller",
        "participant authentication identity did not match the controller",
    ):
        assert required in source


def test_m213_rechecks_stable_token_identity_before_release() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    test_body = source[source.index("def test_retained_client_token_binding_is_stable") :]
    assert test_body.count("participant = binding.snapshot()") == 1
    assert test_body.index("participant = binding.snapshot()") < test_body.index(
        "_challenge(probe, session)"
    )
    assert test_body.index("_verify_stable(participant, binding.snapshot())") < test_body.index(
        '_canonical_document("release", session.challenge, 2)'
    )
    assert "participant token identity changed before release" in source


def test_m213_revalidates_m212_dacl_with_participant_logon_sid() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_verify_pipe_dacl",
        "participant.logon_sid",
        "ctypes.create_string_buffer(participant.logon_sid)",
    ):
        assert required in source


def test_m213_native_surface_is_test_only_offline_and_non_impersonating() -> None:
    assert _imports(_PROBE).isdisjoint({"http", "socket", "urllib"})
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "ImpersonateNamedPipeClient",
        "OpenThreadToken",
        "RevertToSelf",
        "LogonUser",
        "CreateProcessAsUser",
        "CreateProcessWithLogon",
        "AdjustTokenPrivileges",
        "DuplicateToken",
    ):
        assert forbidden not in source


def test_m213_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "same-host, same-logon observation",
        "retained primary token",
        "token identity values remain private",
        "impersonation is not used",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m213_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "no distinct-principal or independent-host run has occurred" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m213_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-local-control-token-binding-probe"
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
    assert "0196-probe-windows-local-control-token-binding.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m213_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "local-control-token-binding-probe",
        "query-client-token",
        "windows-token-bind",
        "windows-host-harness",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_local_control_token_binding.py",
        "src/ludoweave/assets/local_control_token.py",
        "src/ludoweave/assets/windows_token_binding.py",
    ):
        assert not (_ROOT / path).exists()
