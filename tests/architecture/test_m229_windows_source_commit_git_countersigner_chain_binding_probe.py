"""Protect M229's indexed WinTrust countersigner-chain binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_countersigner_chain_binding_probe.py"
)
_DECISION = (
    _ROOT
    / "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-countersigner-chain-binding-probe.md"
)
_RFC = _ROOT / "docs/rfcs/0212-bind-git-countersigner-chain-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0211-bind-git-provider-chain-for-source-commit-probe.md": (
        "edd504167db4780d3ef6bbb0661bf96d6884c512df38971822a37ba02d221dbd"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-provider-chain-binding-probe.md": (
        "eda8a71fe4fc8b7aceb9e5fb23b204ce89d09e4023d5a23b7f7eb1f9ec5110be"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m228_windows_source_commit_git_provider_chain_binding_probe.py": (
        "918702df325bbfdf74005aa56143294940a1baf361a8d36229c98376ef218105"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_provider_chain_binding_probe.py": (
        "e359ce52acc940402f0be136b754d1b47ab3e4e08c579c974bacd0383f3c1d41"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "benchmarks": "d55f1c0d5da18cb4ed72bd94713525e5c76ee64738ff5110935ee389e6a4f771",
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


def test_m229_preserves_runtime_ci_and_complete_m228_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m229_countersigner_chain_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m229_reads_every_indexed_countersigner_from_live_state() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "WTHelperProvDataFromStateData",
        "WTHelperGetProvSignerFromChain",
        "WTHelperGetProvCertFromChain",
        "counter_signer_count = int(primary_signer.contents.csCounterSigners)",
        "for counter_signer_index in range(counter_signer_count):",
        "provider_data, 0, True, counter_signer_index",
    ):
        assert required in source


def test_m229_copies_and_hashes_every_bounded_countersigner_chain() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_COUNTER_SIGNERS",
        "_MAX_COUNTER_SIGNER_DER_BYTES",
        "ctypes.string_at",
        "counter_signer_index.to_bytes",
        "certificate_index.to_bytes",
        "encoded_size.to_bytes",
        "hashlib.sha256(encoded).hexdigest()",
        "counter_signer_sequence_sha256=sequence_digest.hexdigest()",
    ):
        assert required in source


def test_m229_closes_provider_state_after_every_outcome() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_WTD_STATEACTION_VERIFY",
        "_WTD_STATEACTION_CLOSE",
        "finally:",
        "trust_data.dwStateAction = _WTD_STATEACTION_CLOSE",
        "countersigner data was unavailable",
        "primary signer was unavailable",
        "provider countersigner was unavailable at index",
        "countersigner certificate was unavailable at indexes",
        "countersigner DER total was invalid",
        "assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]",
    ):
        assert required in source


def test_m229_composes_the_complete_m228_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_counter_signers = verifier.observe(git_executable, retained.handle)",
        "_m228_module.test_git_provider_chain_matches_across_the_complete_m227_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_counter_signers = verifier.observe(git_executable, retained.handle)",
        "assert after_counter_signers == before_counter_signers",
    ):
        assert required in source


def test_m229_probe_is_windows_only_test_only_and_non_mutating() -> None:
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


def test_m229_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "complete indexed countersigner sequence",
        "countersigner provider-chain order",
        "bounded aggregate der bytes",
        "complete m228 boundary",
        "does not establish portable timestamp semantics",
        "does not authorize a signer, publisher, or timestamp authority",
        "does not persist the observed countersigner identity",
        "revocation freshness remains unproved",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m229_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind the complete indexed wintrust countersigner sequence" in compact
    assert "does not establish timestamp-authority authorization" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m229_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-contained-source-access-source-commit-git-countersigner-chain-binding-probe"
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
    assert "0212-bind-git-countersigner-chain-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m229_adds_no_runtime_timestamp_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-countersigner-chain",
        "git-timestamp-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_countersigner_chain.py",
        "src/ludoweave/platform/git_countersigner_chain.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
