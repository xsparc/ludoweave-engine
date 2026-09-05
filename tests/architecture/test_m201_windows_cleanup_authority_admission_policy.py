"""Protect M201's Windows cleanup-authority admission policy boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0183-adopt-windows-singleton-link-refusal-policy.md": (
        "91bce964d1095e9d8312337d9f9192ef9d04da86b86c3e345e899e01b92996af"
    ),
    "docs/security/windows-cache-cleanup-singleton-link-refusal-policy.md": (
        "f7c78d6794a6f9af300f3f3648609b1a1464b57908f326a15e16e3aa5cd4d008"
    ),
    "pyproject.toml": ("42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"),
    "tests/architecture/test_m200_windows_singleton_link_refusal_policy.py": (
        "ee873966ba6750a551a7ca9a464f7729985b7264ba21c35794e30669d9710faa"
    ),
    "uv.lock": ("e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"),
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-authority-admission-policy.md"
_RFC = _ROOT / "docs/rfcs/0184-adopt-windows-cleanup-authority-admission-policy.md"


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


def test_m201_changes_no_runtime_dependency_ci_or_m200_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m201_requires_trusted_composition_and_exact_effective_token_binding() -> None:
    compact = _compact(_DECISION)
    for required in (
        "trusted composition root",
        "effective windows access token",
        "token_user",
        "token_statistics",
        "user sid",
        "token id",
        "authentication id",
        "modified id",
        "token type",
        "impersonation level",
        "securityanonymous",
        "securityidentification",
        "agentcapabilities.write",
        "not authentication",
        "refuse before authority issuance",
    ):
        assert required in compact


def test_m201_requires_retained_identity_and_security_bound_root() -> None:
    compact = _compact(_DECISION)
    for required in (
        "retained root handle",
        "file_id_info",
        "volume serial number",
        "128-bit file identifier",
        "getsecurityinfo",
        "owner sid",
        "non-null dacl",
        "accesscheck",
        "untrusted writer",
        "file_attribute_tag_info",
        "pathname is not authority",
        "refuse before authority issuance",
    ):
        assert required in compact


def test_m201_requires_a_separate_durable_generation_binding() -> None:
    compact = _compact(_DECISION)
    for required in (
        "durable generation record",
        "root-confined",
        "versioned",
        "immutable",
        "generation identifier",
        "root identity",
        "policy identifier",
        "generation-record object identity",
        "sha-256",
        "logon session is not generation authority",
        "refuse before authority issuance",
    ):
        assert required in compact


def test_m201_keeps_the_authority_private_least_privilege_and_path_silent() -> None:
    compact = _compact(_DECISION)
    for required in (
        "private",
        "non-serializable",
        "operation-scoped",
        "single-use",
        "cleanup-only",
        "not request data",
        "raw sid",
        "token identifiers",
        "must not enter public output",
        "saved evidence cannot mint",
    ):
        assert required in compact


def test_m201_resolves_only_the_authority_policy_criterion() -> None:
    compact = _compact(_DECISION)
    for required in (
        "criterion 1 is resolved as policy",
        "criterion 2 remains resolved as policy",
        "criteria 3 through 7 remain unresolved",
        "security-descriptor revalidation remains criterion 3",
        "cross-principal adversarial proof remains criterion 6",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact

    for forbidden in (
        "windows is admitted",
        "cleanup is authorized",
        "production ready",
    ):
        assert forbidden not in compact


def test_m201_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no authority increase" in compact
    assert "no production adapter" in compact
    assert "no new hosted allocation" in compact


def test_m201_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-authority-admission-policy"
    for path in (
        "README.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        content = (_ROOT / path).read_text(encoding="utf-8")
        assert slug in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0184-adopt-windows-cleanup-authority-admission-policy.md" in rfc_index


def test_m201_adds_no_cleanup_command_adapter_or_public_authority() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "asset-cache-capabilities",
        "asset-cache-prune",
        "asset-cache-delete",
    ):
        assert command not in cli

    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_authority.py",
        "cleanup_capabilities.py",
        "filesystem_adapter.py",
        "garbage_collection.py",
        "retention.py",
    }.isdisjoint(names)
