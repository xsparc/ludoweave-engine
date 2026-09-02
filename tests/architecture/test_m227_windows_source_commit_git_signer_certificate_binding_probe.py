"""Protect M227's WinTrust signer-certificate binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_signer_certificate_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-signer-certificate-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0210-bind-git-signer-certificate-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0209-verify-git-authenticode-trust-for-source-commit-probe.md": (
        "b24894f4bb10e90b7799c798cdef423fe0373a547cccd84bbc79f54b4637266a"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-authenticode-trust-probe.md": (
        "9733cd3f28bca7462cc3629fa68a0ebbe55a2f750496ea3489d11c9ce8989900"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m226_windows_source_commit_git_authenticode_trust_probe.py": (
        "057e11e6405bba8efe59aff2abc30509e484e4929b62cad26558cbb41dd6527f"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_authenticode_trust_probe.py": (
        "1f5e02d67b8e7fc4a8f8c4c67960f386e36988a1ebe4510c7f232197f1dd5bb3"
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


def test_m227_preserves_runtime_ci_and_complete_m226_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m227_signer_certificate_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m227_reads_the_primary_signer_from_live_trust_state() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "WTHelperProvDataFromStateData",
        "WTHelperGetProvSignerFromChain",
        "WTHelperGetProvCertFromChain",
        "trust_data.hWVTStateData",
        "signer.contents.csCertChain",
        "provider_certificate.contents.pCert",
    ):
        assert required in source


def test_m227_copies_and_hashes_bounded_certificate_der() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "class _CERT_CONTEXT",
        "pbCertEncoded",
        "cbCertEncoded",
        "_MAX_CERTIFICATE_DER_BYTES",
        "ctypes.string_at",
        "hashlib.sha256(encoded).hexdigest()",
        "verify_as_of_filetime",
    ):
        assert required in source


def test_m227_closes_provider_state_after_success_and_extraction_failure() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_WTD_STATEACTION_VERIFY",
        "_WTD_STATEACTION_CLOSE",
        "finally:",
        "trust_data.dwStateAction = _WTD_STATEACTION_CLOSE",
        "signer provider data was unavailable",
        "primary signer was unavailable",
        "primary signer certificate chain was invalid",
        "signer certificate was unavailable",
        "signer certificate DER size was invalid",
        "signer certificate DER was unavailable",
        "signer verification time was invalid",
        "assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]",
    ):
        assert required in source


def test_m227_composes_the_complete_m226_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_signer = verifier.observe(git_executable, retained.handle)",
        "_m226_module.test_retained_git_authenticode_trust_survives_the_m225_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_signer = verifier.observe(git_executable, retained.handle)",
        "assert after_signer == before_signer",
    ):
        assert required in source


def test_m227_probe_is_windows_only_test_only_and_non_mutating() -> None:
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


def test_m227_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "live wintrust provider state",
        "primary signer certificate",
        "bounded der bytes",
        "verification time",
        "complete m226 boundary",
        "does not authorize a signer or publisher",
        "does not persist the observed certificate identity",
        "revocation freshness remains unproved",
        "native dll and loader identity remain outside",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m227_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind retained git authenticode signer certificate" in compact
    assert "does not establish signer or publisher authorization" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m227_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-git-signer-certificate-binding-probe"
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
    assert "0210-bind-git-signer-certificate-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m227_adds_no_runtime_signer_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-signer-certificate",
        "git-publisher-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_signer.py",
        "src/ludoweave/platform/git_signer.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
