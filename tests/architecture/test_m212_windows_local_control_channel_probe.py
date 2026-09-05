"""Protect M212's test-only Windows local control-channel boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PARTICIPANT = _ROOT / "tests/fixtures/windows_local_control_channel_participant.py"
_PROBE = _ROOT / "tests/integration/test_windows_local_control_channel_probe.py"
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-local-control-channel-probe.md"
_RFC = _ROOT / "docs/rfcs/0195-probe-windows-local-control-channel.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0194-probe-windows-independent-host-process-containment.md": (
        "de2f974d3fe92406b0fb17a7adf1ee05a8971554c5a60d4559faaf348e49cf57"
    ),
    "docs/security/windows-cache-cleanup-independent-host-process-containment-probe.md": (
        "335cc93f7ad5f8e03645e5661e602a686a2967efefc94e00c1d5983f5bf52527"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m211_windows_independent_host_process_containment_probe.py": (
        "7107f7392fd2cfe6be76f707fcecde5db87c5e670d66cab651fd89301cab1be1"
    ),
    "tests/fixtures/windows_independent_host_process_tree_participant.py": (
        "218330d71df63277b2c9ab8edcbfbdfa4745675ab0cb2a7d017fbd845d01774a"
    ),
    "tests/integration/test_windows_independent_host_process_containment_probe.py": (
        "56059d31f547fefebb4e7776fe7983f85833ea7340e6f2d77d128c7dd84338e0"
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


def test_m212_changes_no_runtime_dependency_ci_or_m211_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m212_local_control_channel_boundary_exists() -> None:
    assert _PARTICIPANT.is_file()
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m212_pipe_uses_exact_local_security_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "CreateNamedPipeW",
        "_FILE_FLAG_FIRST_PIPE_INSTANCE",
        "_PIPE_REJECT_REMOTE_CLIENTS",
        "_TOKEN_LOGON_SID",
        "OpenProcessToken",
        "GetTokenInformation",
        "ConvertSidToStringSidW",
        "D:P(A;;0x",
        "GetSecurityInfo",
        "GetSecurityDescriptorDacl",
        "GetSecurityDescriptorControl",
        "GetAce",
        "EqualSid",
        "acl.AceCount != 1",
        "ace.Mask != _CONTROL_PIPE_ACCESS",
        "assert_first_instance_exclusive",
    ):
        assert required in source
    assert "bInheritHandle=False" in source


def test_m212_binds_the_native_client_to_a_suspended_contained_process() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    start = source[source.index("def _start_or_skip(") : source.index("def _challenge(")]
    launch = source[
        source.index("    def launch_suspended(") : source.index("    def begin_connect(")
    ]
    for required in (
        "CreateProcessW",
        "_CREATE_SUSPENDED",
        "AssignProcessToJobObject",
        "IsProcessInJob",
        "self.process_ids(job)",
        "GetNamedPipeClientProcessId",
        "GetProcessId",
    ):
        assert required in source
    assert "False," in launch
    assert start.index("launch_suspended") < start.index("begin_connect")
    assert start.index("begin_connect") < start.index("probe.resume")
    assert start.index("complete_connect") < start.index("verify_client_identity")
    assert "CREATE_BREAKAWAY_FROM_JOB" not in source
    assert "PROC_THREAD_ATTRIBUTE_HANDLE_LIST" not in source


def test_m212_protocol_is_bounded_canonical_challenged_and_sequenced() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    participant = _PARTICIPANT.read_text(encoding="utf-8")
    for required in (
        "_MAX_MESSAGE_BYTES = 1_024",
        "secrets.token_hex(32)",
        '_canonical_document("challenge", session.challenge, 0)',
        '_canonical_document("ready", session.challenge, 1)',
        '_canonical_document("release", session.challenge, 2)',
        '_canonical_document("released", session.challenge, 3)',
        "_encode(document) != message",
    ):
        assert required in source
    assert "_encode(document) != message" in participant
    assert "set(document)" in source
    assert "set(document)" in participant


def test_m212_controller_io_is_overlapped_bounded_and_cancelled() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_FILE_FLAG_OVERLAPPED",
        "CreateEventW",
        "ConnectNamedPipe",
        "WaitForSingleObject",
        "GetOverlappedResult",
        "CancelIoEx",
        "_TIMEOUT_MILLISECONDS = 5_000",
    ):
        assert required in source
    assert "time.sleep" not in source


def test_m212_observes_release_and_fixed_refusal_categories() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for test_name in (
        "test_valid_challenge_releases_one_bound_participant",
        "test_replayed_challenge_is_rejected_before_release",
        "test_wrong_release_challenge_is_rejected",
        "test_malformed_challenge_is_rejected",
        "test_disconnect_is_rejected_without_release",
    ):
        assert f"def {test_name}()" in source
    for category in ("_EXIT_PROTOCOL", "_EXIT_CHALLENGE", "_EXIT_DISCONNECT"):
        assert category in source


def test_m212_native_surface_is_test_only_offline_and_fixed() -> None:
    assert _imports(_PARTICIPANT).isdisjoint({"http", "socket", "urllib"})
    assert _imports(_PROBE).isdisjoint({"http", "socket", "urllib"})
    participant = _PARTICIPANT.read_text(encoding="utf-8")
    source = _PROBE.read_text(encoding="utf-8")
    assert "subprocess.Popen" not in source
    assert "shell=True" not in source
    assert "_valid_pipe_name" in participant
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
        assert forbidden not in participant


def test_m212_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "current-host test evidence",
        "same-host, same-logon observation",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "default pipe security descriptor",
        "one allow ace for the exact logon sid",
        "participant-reported pid",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m212_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "no distinct-principal or independent-host run has occurred" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m212_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-local-control-channel-probe"
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
    assert "0195-probe-windows-local-control-channel.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m212_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "local-control-channel-probe",
        "independent-host-collect",
        "named-pipe-control",
        "windows-host-harness",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_local_control_channel.py",
        "src/ludoweave/assets/collection_harness.py",
        "src/ludoweave/assets/local_control_channel.py",
        "src/ludoweave/assets/windows_named_pipe.py",
    ):
        assert not (_ROOT / path).exists()
