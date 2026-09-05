"""Protect M235's CMS signer hash-algorithm binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SLUG = (
    "windows-cache-cleanup-contained-source-access-source-commit-git-cms-"
    "signer-hash-algorithm-binding-probe"
)
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_cms_signer_hash_algorithm_binding_probe.py"
)
_DECISION = _ROOT / "docs/security" / f"{_SLUG}.md"
_RFC = _ROOT / "docs/rfcs/0218-bind-git-cms-signer-hash-algorithm-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0217-bind-git-cms-signer-info-certificate-id-for-source-commit-probe.md": (
        "123db7f590c2a337e343691af8206f6760f4c4e9fb929ec1bc92cf9637939201"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-cms-signer-info-certificate-id-binding-probe.md": (
        "71618fb04c05dd26d59da0452ad346d1e5f536a4da980629449e0460e2168bca"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m234_windows_source_commit_git_cms_signer_info_certificate_id_binding_probe.py": (
        "7ef15c8aff3ed59a12802db2af863856b29c6853af932a4148279bb89af4bca5"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_cms_signer_info_certificate_id_binding_probe.py": (
        "60ec2ba3eb6da1b21bb7aa525e1fc6c7c44010e17986af01a8d4c95efee88110"
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


def test_m235_preserves_runtime_ci_and_complete_m234_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m235_cms_signer_hash_algorithm_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m235_reads_both_hash_algorithm_representations_per_exact_signer() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_CMSG_SIGNER_HASH_ALGORITHM_PARAM = 8",
        "_CMSG_CMS_SIGNER_INFO_PARAM = 39",
        "for signer_index in range(signer_count):",
        "cms_hash_algorithm = self._read_cms_signer_hash_algorithm(",
        "dedicated_hash_algorithm = self._read_dedicated_signer_hash_algorithm(",
        "prefix.HashAlgorithm",
    ):
        assert required in source


def test_m235_uses_bounded_two_phase_hash_algorithm_reads() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_CMS_SIGNER_INFO_BYTES",
        "_MAX_HASH_ALGORITHM_BYTES",
        "ctypes.c_void_p()",
        "ctypes.create_string_buffer(cms_signer_info_size)",
        "ctypes.create_string_buffer(hash_algorithm_size)",
        "CMS signer hash-algorithm size changed",
        "dedicated signer hash-algorithm size changed",
    ):
        assert required in source


def test_m235_confines_and_detaches_pointer_bearing_algorithm_data() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_ALGORITHM_OID_BYTES",
        "_MAX_ALGORITHM_PARAMETER_BYTES",
        "algorithm OID pointer escaped its owning buffer",
        "algorithm parameters escaped their owning buffer",
        "algorithm OID was not terminated inside its owning buffer",
        "algorithm OID was malformed",
        "ctypes.string_at(oid_address, oid_extent)",
        "ctypes.string_at(parameter_address, parameter_size)",
    ):
        assert required in source


def test_m235_binds_exact_algorithm_identity_without_policy() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "cms_hash_algorithm != dedicated_hash_algorithm",
        "CMS and dedicated signer hash algorithms differed",
        "hash_algorithm_oids.append(cms_hash_algorithm.oid)",
        "hash_algorithm_parameter_sizes.append(",
        "hash_algorithm_sequence_sha256=digest.hexdigest()",
    ):
        assert required in source


def test_m235_composes_the_complete_m234_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "base_observation = super()._read_identifier_sequence(trust_data)",
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_hash_algorithm = verifier.observe(git_executable, retained.handle)",
        "_m234_module.test_git_cms_signer_info_certificate_ids_match_across_the_complete_m233_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_hash_algorithm = verifier.observe(git_executable, retained.handle)",
        "assert after_hash_algorithm == before_hash_algorithm",
    ):
        assert required in source


def test_m235_probe_is_windows_only_test_only_and_non_mutating() -> None:
    assert _imports(_PROBE).issubset(
        {
            "__future__",
            "collections",
            "ctypes",
            "dataclasses",
            "hashlib",
            "pathlib",
            "re",
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


def test_m235_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exact message signer index",
        "complete m234 boundary",
        "cms hashalgorithm",
        "does not approve or reject an algorithm",
        "does not revalidate the signature",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m235_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind the cms signer hash algorithm" in compact
    assert "does not create an algorithm allowlist" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m235_public_boundary_is_registered_without_ci_expansion() -> None:
    for path in (
        "README.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        assert _SLUG in (_ROOT / path).read_text(encoding="utf-8")
    assert "0218-bind-git-cms-signer-hash-algorithm-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m235_adds_no_runtime_algorithm_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-cms-signer-hash-algorithm",
        "git-algorithm-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_cms_signer_hash_algorithm.py",
        "src/ludoweave/platform/git_cms_signer_hash_algorithm.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
