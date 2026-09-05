"""Protect M216's test-only retained launch-source access-refusal boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_retained_launch_source_access_refusal_probe.py"
_DECISION = (
    _ROOT / "docs/security/windows-cache-cleanup-retained-launch-source-access-refusal-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0199-probe-windows-retained-launch-source-access-refusal.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0198-probe-windows-retained-launch-source-binding.md": (
        "b52a0c938a1e356671633936f9e50c667a8a873bf40638d97b36c4e97ce20e52"
    ),
    "docs/security/windows-cache-cleanup-retained-launch-source-binding-probe.md": (
        "fdc862ce0ad7ec89e4388f420ceee37232ed1daf5d00a82556be0ad87170db1f"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m215_windows_retained_launch_source_binding_probe.py": (
        "bc355dccabba1356a7d7486e64eedb8e423864a4fe09660cb3c29b7690764a58"
    ),
    "tests/fixtures/windows_local_control_channel_participant.py": (
        "b3e33d4e70fef4fa3acc3fbb3e8526705c5625b7865344a2a63243415194f452"
    ),
    "tests/integration/test_windows_retained_launch_source_binding_probe.py": (
        "66e4037dd32f4d7516969c1233063cc35563fe93895905bfc5c8ccb9f12a7b82"
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


def test_m216_changes_no_runtime_dependency_ci_fixture_or_m215_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m216_retained_source_access_refusal_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m216_requests_exact_write_and_delete_access_without_mutation() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_DELETE = 0x00010000",
        "_ERROR_SHARING_VIOLATION = 32",
        "_GENERIC_WRITE",
        "_FILE_SHARE_DELETE",
        "_FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE",
        "_OPEN_EXISTING",
        "CreateFileW",
        "get_last_error",
        "_INVALID_HANDLE_VALUE",
    ):
        assert required in source


def test_m216_observes_refusal_at_three_ordered_live_phases() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def test_retained_launch_source_refuses_competing_access") :]
    before = body.index('phase="before_launch"')
    start = body.index("_start_or_skip(probe)")
    connected = body.index('phase="after_connection"')
    challenge = body.index("_challenge(probe, session)")
    ready = body.index('phase="after_ready"')
    release = body.index('_canonical_document("release", session.challenge, 2)')
    assert before < start < connected < challenge < ready < release
    assert body.count("_require_source_access_refused(") == 3


def test_m216_requires_access_only_after_retained_source_settlement() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def test_retained_launch_source_refuses_competing_access") :]
    assert body.index("probe.settle(session, 0)") < body.index(
        "_require_source_access_allowed(_PARTICIPANT)"
    )
    assert body.index("_require_source_access_allowed(_PARTICIPANT)") < body.index(
        "post_file.snapshot()"
    )
    assert "_verify_source_stable(source_before, post_file.snapshot())" in body


def test_m216_closes_unexpected_or_allowed_handles_and_checks_exact_error() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "if result.error_code != _ERROR_SHARING_VIOLATION",
        "close_handle(handle)",
        "competing source access unexpectedly succeeded",
        "competing source access did not settle",
        "CloseHandle",
    ):
        assert required in source
    for test_name in (
        "test_unexpected_competing_access_success_closes_before_failure",
        "test_nonsharing_native_error_fails_closed",
        "test_allowed_access_closes_each_handle",
        "test_missing_post_settlement_access_fails_closed",
    ):
        assert f"def {test_name}" in source


def test_m216_performs_no_source_mutation_operation() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "WriteFile",
        "SetEndOfFile",
        "DeleteFile",
        "MoveFile",
        "ReplaceFile",
        "CREATE_ALWAYS",
        "TRUNCATE_EXISTING",
        "FILE_FLAG_DELETE_ON_CLOSE",
        "unlink(",
        "rename(",
        "replace(",
        "write_bytes(",
        "write_text(",
    ):
        assert forbidden not in source


def test_m216_native_surface_is_test_only_offline_and_non_authorizing() -> None:
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


def test_m216_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "retained launch-source access refusal",
        "write and delete access",
        "exact native sharing error 32",
        "before launch",
        "after connection",
        "after ready",
        "after retained source settlement",
        "does not attempt write, rename, replace, truncate, or delete",
        "same-process cooperative observation",
        "source-commit provenance remains unproved",
        "imported standard-library module bytes remain unbound",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m216_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "performs no content or namespace mutation" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m216_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-retained-launch-source-access-refusal-probe"
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
    assert "0199-probe-windows-retained-launch-source-access-refusal.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m216_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "source-access-refusal-probe",
        "source-write-refusal",
        "source-delete-refusal",
        "windows-host-harness",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_retained_source_access.py",
        "src/ludoweave/assets/source_access.py",
        "src/ludoweave/platform/windows_source_access.py",
    ):
        assert not (_ROOT / path).exists()
