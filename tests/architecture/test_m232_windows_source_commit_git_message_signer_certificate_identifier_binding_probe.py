"""Protect M232's message-to-certificate identifier binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_message_signer_certificate_identifier_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-message-signer-certificate-identifier-binding-probe.md"
)
_RFC = (
    _ROOT
    / "docs/rfcs/0215-bind-git-message-signer-certificate-identifier-for-source-commit-probe.md"
)
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0214-bind-git-message-signer-certificate-for-source-commit-probe.md": (
        "c70c49a8c2c060c4c7dd0cc9cf46308c0e9b9ae05ef4d19292eef35e02ae0e9c"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-message-signer-certificate-binding-probe.md": (
        "b17e76c884f94cd67e689ade8a3b8a1f99f098999be8565dd3bec027fdee1a72"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m231_windows_source_commit_git_message_signer_certificate_binding_probe.py": (
        "d99e506a2fe90274bae66128411b075f57b57da3a2d4c35f5cd831c83fda71dd"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_message_signer_certificate_binding_probe.py": (
        "7449e76fcfefdf755b8891d76d00bd111af110669a839ac95e4a6a25e3595820"
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


def test_m232_preserves_runtime_ci_and_complete_m231_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m232_message_signer_certificate_identifier_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m232_reads_every_exact_signer_certificate_identifier() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_CMSG_SIGNER_CERT_INFO_PARAM = 7",
        "for signer_index in range(signer_count):",
        "message_identifier = self._read_message_certificate_info(",
        "info.SerialNumber",
        "info.Issuer",
    ):
        assert required in source


def test_m232_uses_bounded_two_phase_certificate_info_reads() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_CERTIFICATE_INFO_BYTES",
        "_MAX_CERTIFICATE_IDENTIFIER_BYTES",
        "ctypes.c_void_p()",
        "ctypes.create_string_buffer(info_size)",
        "certificate-info size changed",
        "certificate-info query failed",
        "certificate-info read failed",
    ):
        assert required in source


def test_m232_compares_message_verified_and_provider_identifiers() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "message_identifier != verified_identifier",
        "message and verified certificate identifiers differed",
        "verified_identifier != provider_identifier",
        "verified and provider certificate identifiers differed",
        "certificate_identifier_sizes.append",
        "message_hashes.append(_identifier_sha256(message_identifier))",
        "verified_hashes.append(_identifier_sha256(verified_identifier))",
        "provider_hashes.append(_identifier_sha256(provider_identifier))",
    ):
        assert required in source


def test_m232_composes_the_complete_m231_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_identifier = verifier.observe(git_executable, retained.handle)",
        "_m231_module.test_git_message_signer_certificates_match_across_the_complete_m230_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_identifier = verifier.observe(git_executable, retained.handle)",
        "assert after_identifier == before_identifier",
    ):
        assert required in source


def test_m232_probe_is_windows_only_test_only_and_non_mutating() -> None:
    assert _imports(_PROBE).issubset(
        {
            "__future__",
            "collections",
            "ctypes",
            "dataclasses",
            "hashlib",
            "pathlib",
            "sys",
            "typing",
            "unittest",
            "pytest",
            "tests",
        }
    )
    source = _PROBE.read_text(encoding="utf-8")
    for forbidden in (
        "http",
        "socket",
        "urllib",
        "requests",
        "shell=True",
        "git checkout",
        "git reset",
        "git clean",
        "git update-ref",
        "git fetch",
        "git pull",
        "git push",
        "unlink(",
        "rename(",
        "replace(",
        "write_bytes(",
        "write_text(",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source


def test_m232_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exact message signer index",
        "complete m231 boundary",
        "issuer and serial-number blobs",
        "does not authorize a signer or publisher",
        "does not establish revocation freshness",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m232_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind the message signer certificate identifier" in compact
    assert "does not create signer or publisher authorization" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m232_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-git-message-signer-certificate-identifier-binding-probe"
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
    assert "0215-bind-git-message-signer-certificate-identifier-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m232_adds_no_runtime_crypto_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-message-signer-certificate-identifier",
        "git-publisher-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_message_signer_certificate_identifier.py",
        "src/ludoweave/platform/git_message_signer_certificate_identifier.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
