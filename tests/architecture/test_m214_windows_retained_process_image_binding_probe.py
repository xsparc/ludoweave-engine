"""Protect M214's test-only Windows retained process-image boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = _ROOT / "tests/integration/test_windows_retained_process_image_binding_probe.py"
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-retained-process-image-binding-probe.md"
_RFC = _ROOT / "docs/rfcs/0197-probe-windows-retained-process-image-binding.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0196-probe-windows-local-control-token-binding.md": (
        "d495255671cf4c2e3928b08e24c7566e6fa490056cc8a9966a603bb16ec24437"
    ),
    "docs/security/windows-cache-cleanup-local-control-token-binding-probe.md": (
        "71073941cc301fe1681f9c70d0168739cdbca0a76dfd9e7044cdc4064919059f"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m213_windows_local_control_token_binding_probe.py": (
        "06b0151ce5e5144262996ac95c12079e4c4eba1b07c8c086c6c57a6a7637902e"
    ),
    "tests/integration/test_windows_local_control_token_binding_probe.py": (
        "0f4c3e5d701b68b225adc9c6b9735efe4940c3d528caf05521c219128e1172ee"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "f1774c37b8002dcd420b6aafe885c8289e2be44300e3d03f88cbcb03a43bc7a0",
    "scripts": "a21166a0d275e9583c39d280c8ca77c016da2048e510970c2601f5250ddefdbf",
    "src/ludoweave": "e6c951393b86b0673a25e0f6b1f4cf41224d3cb7807dd85c76aad482820cde36",
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


def test_m214_changes_no_runtime_dependency_ci_or_m213_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m214_retained_process_image_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m214_uses_supported_process_and_handle_identity_observations() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "QueryFullProcessImageNameW",
        "CreateFileW",
        "GetFileInformationByHandleEx",
        "_FILE_ID_INFO",
        "_FILE_ID_INFO_CLASS",
        "GetFileSizeEx",
        "SetFilePointerEx",
        "ReadFile",
        "hashlib.sha256",
    ):
        assert required in source


def test_m214_expected_image_is_retained_before_launch() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def test_retained_process_image_is_stable") :]
    assert body.index("_RetainedImageFile(_DIRECT_PYTHON)") < body.index("_start_or_skip(probe)")
    assert "session.process" in body
    assert "_verify_expected_image(expected, before)" in body


def test_m214_rechecks_same_retained_image_before_release() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    body = source[source.index("def test_retained_process_image_is_stable") :]
    assert body.index("before = observed.snapshot()") < body.index("_challenge(probe, session)")
    assert body.index("_verify_stable(before, observed.snapshot())") < body.index(
        '_canonical_document("release", session.challenge, 2)'
    )
    assert "retained process image changed before release" in source


def test_m214_image_reads_are_bounded_private_and_handle_owned() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_IMAGE_BYTES = 64 * 1_024 * 1_024",
        "_READ_CHUNK_BYTES = 64 * 1_024",
        "image file size was outside the fixed bound",
        "self.close()",
        "self._close_handle",
    ):
        assert required in source
    for forbidden in (
        "read_bytes(",
        "print(",
        "json.dumps",
        "pathlib.Path.open",
    ):
        assert forbidden not in source


def test_m214_native_surface_is_test_only_offline_and_non_authorizing() -> None:
    assert _imports(_PROBE).isdisjoint({"http", "socket", "subprocess", "urllib"})
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "ImpersonateNamedPipeClient",
        "OpenThreadToken",
        "LogonUser",
        "CreateProcessAsUser",
        "CreateProcessWithLogon",
        "AdjustTokenPrivileges",
        "WriteFile",
        "DeleteFile",
    ):
        assert forbidden not in source


def test_m214_documentation_preserves_non_admission_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "current-host process-image observation",
        "retained expected-image handle",
        "image identity values remain private",
        "does not bind the loaded python script bytes",
        "does not prove hostile aba resistance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "no public self-hosted runner is introduced",
    ):
        assert required in compact


def test_m214_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no collection or cleanup authority increase" in compact
    assert "no distinct-principal or independent-host run has occurred" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m214_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-retained-process-image-binding-probe"
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
    assert "0197-probe-windows-retained-process-image-binding.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m214_adds_no_runtime_command_collector_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "retained-process-image-probe",
        "query-process-image",
        "windows-image-bind",
        "windows-host-harness",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_retained_process_image.py",
        "src/ludoweave/assets/process_image.py",
        "src/ludoweave/assets/windows_image_binding.py",
    ):
        assert not (_ROOT / path).exists()
