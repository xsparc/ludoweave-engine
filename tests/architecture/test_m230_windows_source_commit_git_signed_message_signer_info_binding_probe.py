"""Protect M230's encoded WinTrust signed-message SignerInfo boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_signed_message_signer_info_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-signed-message-signer-info-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0213-bind-git-signed-message-signer-info-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0212-bind-git-countersigner-chain-for-source-commit-probe.md": (
        "b4f6b4c2b66605221685d0122196a0962246b9a6ad7c887e4f424057e5102780"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-countersigner-chain-binding-probe.md": (
        "009457102fc1d9c9c00d12cc340beeda06a90bb465d9f7bcc40f7a27421c6974"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m229_windows_source_commit_git_countersigner_chain_binding_probe.py": (
        "dde73b3ab022be1cb72d7fa309ebd91a29f6bf66cdf0276d9ea70452591950ac"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_countersigner_chain_binding_probe.py": (
        "7210b56df929ecb56ea11e77a2590de94e385e0f5f91db0dc2bfddb141a2bca1"
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


def test_m230_preserves_runtime_ci_and_complete_m229_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m230_signed_message_signer_info_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m230_reads_the_live_provider_message_and_complete_signer_count() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "class _CRYPT_PROVIDER_DATA_PREFIX",
        "WTHelperProvDataFromStateData",
        "provider.hMsg",
        "provider.dwEncoding",
        "provider.csSigners",
        "_CMSG_SIGNER_COUNT_PARAM",
    ):
        assert required in source


def test_m230_copies_every_encoded_signer_info_with_two_phase_queries() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "CryptMsgGetParam",
        "for signer_index in range(message_signer_count):",
        "_CMSG_ENCODED_SIGNER",
        "requested_size = wintypes.DWORD()",
        "actual_size = wintypes.DWORD(requested_size.value)",
        "ctypes.string_at",
    ):
        assert required in source


def test_m230_bounds_and_hashes_the_exact_encoded_signer_sequence() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_SIGNED_MESSAGE_SIGNERS",
        "_MAX_ENCODED_SIGNER_INFO_BYTES",
        "_MAX_SIGNED_MESSAGE_SIGNER_INFO_BYTES",
        "signer_index.to_bytes",
        "encoded_size.to_bytes",
        "hashlib.sha256(encoded).hexdigest()",
        "signed_message_signer_sequence_sha256=sequence_digest.hexdigest()",
    ):
        assert required in source


def test_m230_closes_provider_state_after_every_outcome() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_WTD_STATEACTION_VERIFY",
        "_WTD_STATEACTION_CLOSE",
        "finally:",
        "trust_data.dwStateAction = _WTD_STATEACTION_CLOSE",
        "signed-message provider data was unavailable",
        "signed-message handle was unavailable",
        "encoded SignerInfo size query failed",
        "encoded SignerInfo read failed",
        "assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]",
    ):
        assert required in source


def test_m230_composes_the_complete_m229_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_signers = verifier.observe(git_executable, retained.handle)",
        "_m229_module.test_git_countersigner_chains_match_across_the_complete_m228_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_signers = verifier.observe(git_executable, retained.handle)",
        "assert after_signers == before_signers",
    ):
        assert required in source


def test_m230_probe_is_windows_only_test_only_and_non_mutating() -> None:
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


def test_m230_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "complete bounded encoded signerinfo sequence",
        "two-phase cryptmsggetparam queries",
        "complete m229 boundary",
        "does not parse signerinfo",
        "does not establish portable timestamp semantics",
        "does not authorize a signer, publisher, or timestamp authority",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m230_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind the complete bounded encoded signerinfo sequence" in compact
    assert "does not independently parse or validate signerinfo" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m230_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-git-signed-message-signer-info-binding-probe"
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
    assert "0213-bind-git-signed-message-signer-info-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m230_adds_no_runtime_crypto_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-signer-info",
        "git-timestamp-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_signer_info.py",
        "src/ludoweave/platform/git_signer_info.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
