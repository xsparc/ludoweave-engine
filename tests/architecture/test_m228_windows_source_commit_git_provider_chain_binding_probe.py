"""Protect M228's ordered WinTrust provider-chain binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_provider_chain_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-provider-chain-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0211-bind-git-provider-chain-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0210-bind-git-signer-certificate-for-source-commit-probe.md": (
        "a8a86451b82b2ffe774c6d7cbccc575ef15b3e7652980157b5600c033f0cf8bd"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-signer-certificate-binding-probe.md": (
        "2a1daed0564eee3320f555c29857db9cb95f42ba24c4bdd90ad9a1ea201eb293"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m227_windows_source_commit_git_signer_certificate_binding_probe.py": (
        "fd6b5a6c2d2aa397a7b50cfa124371f34324c573f20e506c6ed2b3acd021a185"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_signer_certificate_binding_probe.py": (
        "037bcc079c9aa6caf784d62fb194675166302f585d68d7f7c5a84ce48efa3770"
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


def test_m228_preserves_runtime_ci_and_complete_m227_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m228_provider_chain_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m228_reads_every_indexed_provider_certificate_from_live_state() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "WTHelperProvDataFromStateData",
        "WTHelperGetProvSignerFromChain",
        "WTHelperGetProvCertFromChain",
        "chain_length = int(signer.contents.csCertChain)",
        "for certificate_index in range(chain_length):",
        "self._get_certificate_from_chain(",
        "signer, certificate_index",
    ):
        assert required in source


def test_m228_copies_and_hashes_an_unambiguous_bounded_chain() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_CERTIFICATE_DER_BYTES",
        "_MAX_PROVIDER_CHAIN_DER_BYTES",
        "ctypes.string_at",
        "certificate_index.to_bytes",
        "encoded_size.to_bytes",
        "hashlib.sha256(encoded).hexdigest()",
        "provider_chain_sha256=chain_digest.hexdigest()",
        "certificate_sha256=tuple(certificate_hashes)",
    ):
        assert required in source


def test_m228_closes_provider_state_after_success_rejection_and_extraction_failure() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_WTD_STATEACTION_VERIFY",
        "_WTD_STATEACTION_CLOSE",
        "finally:",
        "trust_data.dwStateAction = _WTD_STATEACTION_CLOSE",
        "provider chain data was unavailable",
        "provider chain signer was unavailable",
        "provider certificate was unavailable at index",
        "provider certificate DER size was invalid at index",
        "provider certificate DER was unavailable at index",
        "provider chain DER total was invalid",
        "assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]",
    ):
        assert required in source


def test_m228_composes_the_complete_m227_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_chain = verifier.observe(git_executable, retained.handle)",
        "_m227_module.test_git_signer_certificate_matches_across_the_complete_m226_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_chain = verifier.observe(git_executable, retained.handle)",
        "assert after_chain == before_chain",
    ):
        assert required in source


def test_m228_probe_is_windows_only_test_only_and_non_mutating() -> None:
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


def test_m228_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "complete ordered provider-certificate sequence",
        "provider index order",
        "bounded aggregate der bytes",
        "complete m227 boundary",
        "does not define portable chain semantics",
        "does not authorize a signer or publisher",
        "does not persist the observed chain identity",
        "revocation freshness remains unproved",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m228_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind the complete ordered wintrust provider-certificate sequence" in compact
    assert "does not establish signer or publisher authorization" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m228_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-git-provider-chain-binding-probe"
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
    assert "0211-bind-git-provider-chain-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m228_adds_no_runtime_chain_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-provider-chain",
        "git-chain-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_provider_chain.py",
        "src/ludoweave/platform/git_provider_chain.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
