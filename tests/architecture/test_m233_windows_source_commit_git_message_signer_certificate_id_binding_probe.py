"""Protect M233's explicit message signer CERT_ID binding boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SLUG = (
    "windows-cache-cleanup-contained-source-access-source-commit-git-message-"
    "signer-certificate-id-binding-probe"
)
_PROBE = (
    _ROOT
    / "tests/integration/test_windows_contained_source_access_source_commit_git_message_signer_certificate_id_binding_probe.py"
)
_DECISION = _ROOT / "docs/security" / f"{_SLUG}.md"
_RFC = _ROOT / "docs/rfcs/0216-bind-git-message-signer-certificate-id-for-source-commit-probe.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0215-bind-git-message-signer-certificate-identifier-for-source-commit-probe.md": (
        "12569799d42517af5dc06f5664a1c10ff300ad1838b50df74155d2916c7430d1"
    ),
    "docs/security/windows-cache-cleanup-contained-source-access-source-commit-git-message-signer-certificate-identifier-binding-probe.md": (
        "149e89819604b892522cf96989ff03b58431b4196c62619183863019d8935b99"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m232_windows_source_commit_git_message_signer_certificate_identifier_binding_probe.py": (
        "565d84d8eedc5f4b5909dc2dc93f944c6503c2dd7ea751286131c76335a3b724"
    ),
    "tests/integration/test_windows_contained_source_access_source_commit_git_message_signer_certificate_identifier_binding_probe.py": (
        "8bd2329f20ec0a8af210da6ffb819ed70a7949b3d6f9f0cdcb578e6715610a9b"
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


def test_m233_preserves_runtime_ci_and_complete_m232_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m233_certificate_id_binding_boundary_exists() -> None:
    assert _PROBE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m233_reads_every_exact_signer_certificate_id() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_CMSG_SIGNER_CERT_ID_PARAM = 38",
        "_CERT_ID_ISSUER_SERIAL_NUMBER = 1",
        "for signer_index in range(signer_count):",
        "message_certificate_id = self._read_message_certificate_id(",
        "certificate_id.dwIdChoice",
        "certificate_id.value.IssuerSerialNumber",
    ):
        assert required in source


def test_m233_uses_bounded_two_phase_certificate_id_reads() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "_MAX_CERTIFICATE_ID_BYTES",
        "ctypes.c_void_p()",
        "ctypes.create_string_buffer(certificate_id_size)",
        "certificate-ID size changed",
        "certificate-ID query failed",
        "certificate-ID read failed",
    ):
        assert required in source


def test_m233_binds_explicit_choice_and_issuer_serial_payload() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "unsupported message signer certificate-ID choice",
        "message_certificate_id.identifier != legacy_identifier",
        "message certificate-ID and legacy certificate identifier differed",
        "certificate_id_choices.append(message_certificate_id.choice)",
        "certificate_id_hashes.append(_certificate_id_sha256(message_certificate_id))",
        "certificate_id_sequence_sha256=digest.hexdigest()",
    ):
        assert required in source


def test_m233_composes_the_complete_m232_boundary() -> None:
    source = _PROBE.read_text(encoding="utf-8")
    for required in (
        "base_observation = super()._read_identifier_sequence(trust_data)",
        "with _RetainedGitExecutableFile(git_executable) as retained:",
        "before_file = retained.snapshot()",
        "before_certificate_id = verifier.observe(git_executable, retained.handle)",
        "_m232_module.test_git_message_signer_certificate_identifiers_match_across_the_complete_m231_boundary()",
        "_verify_image_stable(before_file, retained.snapshot())",
        "after_certificate_id = verifier.observe(git_executable, retained.handle)",
        "assert after_certificate_id == before_certificate_id",
    ):
        assert required in source


def test_m233_probe_is_windows_only_test_only_and_non_mutating() -> None:
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


def test_m233_documentation_preserves_observation_only_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exact message signer index",
        "complete m232 boundary",
        "explicit certificate-id choice",
        "does not authorize a signer or publisher",
        "does not establish revocation freshness",
        "not source or build provenance",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact


def test_m233_rfc_is_accepted_direction_preserving_and_ci_neutral() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "bind the explicit message signer certificate-id" in compact
    assert "does not create signer or publisher authorization" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m233_public_boundary_is_registered_without_ci_expansion() -> None:
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
    assert "0216-bind-git-message-signer-certificate-id-for-source-commit-probe.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m233_adds_no_runtime_crypto_policy_cleanup_or_admission_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "git-message-signer-certificate-id",
        "git-publisher-policy",
        "windows-cleanup",
    ):
        assert command not in cli
    for path in (
        "scripts/windows_git_message_signer_certificate_id.py",
        "src/ludoweave/platform/git_message_signer_certificate_id.py",
        "src/ludoweave/tools/windows_cleanup.py",
    ):
        assert not (_ROOT / path).exists()
