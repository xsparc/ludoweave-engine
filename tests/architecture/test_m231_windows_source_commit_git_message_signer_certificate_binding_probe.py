"""Protect M231's WinTrust message-to-provider signer-certificate boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_message_signer_certificate_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-message-signer-certificate-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0214-bind-git-message-signer-certificate-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0213-bind-git-signed-message-signer-info-for-source-commit-probe.md": (
        "4e254ae12fa2f5d80c04acb8974f5cb456358f3a95872348412012e03eba1785"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-signed-message-signer-info-binding-probe.md": (
        "c6a7db8913d8343f7bc7762872e7857461cf240cd073daaf41259917aa2dcff8"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m230_windows_source_commit_git_signed_message_signer_info_binding_probe.py": (
        "7e80df26bcde1255339e820928bc5268ac00ba12f0c1b0555470500f20387e13"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_signed_message_signer_info_binding_probe.py": (
        "d758f818264618c4b941a69887c8dfaca3f431ec24925635e9bebb7199bdc4a4"
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


def test_m231_preserves_runtime_ci_and_complete_m230_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m231_message_signer_certificate_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m231_uses_live_provider_message_stores_and_every_exact_signer_index() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "WTHelperProvDataFromStateData",
        "provider.chStores",
        "provider.pahStores",
        "provider.hMsg",
        "CryptMsgGetAndVerifySigner",
        "_CMSG_USE_SIGNER_INDEX_FLAG",
        "for signer_index in range(signer_count):",
        "requested_index = wintypes.DWORD(signer_index)",
    ):
        assert required in source


def test_m231_verifies_and_copies_the_message_signer_certificate() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_PROVIDER_STORES",
        "_MAX_CERTIFICATE_DER_BYTES",
        "message_certificate.contents.cbCertEncoded",
        "message_certificate.contents.pbCertEncoded",
        "ctypes.string_at",
        "hashlib.sha256(message_der).hexdigest()",
        "_MAX_MESSAGE_SIGNER_CERTIFICATE_BYTES",
    ):
        assert required in source


def test_m231_correlates_message_and_provider_certificate_bytes() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "WTHelperGetProvSignerFromChain",
        "WTHelperGetProvCertFromChain",
        "provider_certificate.contents.pCert.contents",
        "provider_der != message_der",
        "message and provider signer certificates differed",
        "provider_certificate_hashes.append(hashlib.sha256(provider_der).hexdigest())",
    ):
        assert required in source


def test_m231_frees_certificate_context_and_closes_provider_state() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "CertFreeCertificateContext",
        "finally:",
        "trust_data.dwStateAction = _WTD_STATEACTION_CLOSE",
        "message signer certificate free failed",
        "trust provider state close failed",
        "assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]",
    ):
        assert required in source


def test_m231_composes_the_complete_m230_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_certificate = verifier.observe(git_executable, retained.handle)",
        "_m230_module.test_git_signed_message_signer_info_matches_across_the_complete_m229_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_certificate = verifier.observe(git_executable, retained.handle)",
        "assert after_certificate == before_certificate",
    ):
        assert required in source


def test_m231_probe_is_windows_only_test_only_and_non_mutating() -> None:
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


def test_m231_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exact message signer index",
        "complete m230 boundary",
        "message and provider certificate bytes",
        "does not authorize a signer or publisher",
        "does not establish revocation freshness",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m231_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "correlate the verified message signer certificate" in compact
    assert "does not create signer or publisher authorization" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m231_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-git-message-signer-certificate-binding-probe"
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
    assert "0214-bind-git-message-signer-certificate-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m231_adds_no_runtime_crypto_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-message-signer-certificate",
        "git-publisher-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_message_signer_certificate.py",
        "src/ludoweave/platform/git_message_signer_certificate.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
