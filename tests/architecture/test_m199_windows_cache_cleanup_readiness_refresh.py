"""Protect M199's evidence-based Windows cache-cleanup deferral."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0181-probe-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure.md": (
        "8b9157cd1391c0963641dbf634c3ac5075536b9242b4063b443fb04b2a143538"
    ),
    "docs/security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure-probe.md": (
        "faed470b54ab8798b08969105d0a80a3bdee1584ab91ec35a8ffe3c120f66e1e"
    ),
    "pyproject.toml": ("42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"),
    "tests/architecture/test_m198_windows_hard_link_alias_mutator_closed_stream_write_after_delivery_failure_boundary.py": (
        "2f9fe2b0c6776b2a7d37cda5fadcc7fbc174a457d92e107b8d716776f092b81a"
    ),
    "tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_closed_stream_write_after_delivery_failure_probe.py": (
        "246d0015e30b8ecd563b915d44ffadd30bf31009eb185c8cd73ece0f1b61c58b"
    ),
    "uv.lock": ("e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"),
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_DECISION = _ROOT / "docs/security/cache-cleanup-windows-readiness-refresh.md"
_RFC = _ROOT / "docs/rfcs/0182-refresh-windows-cache-cleanup-readiness.md"


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


def _milestone_test_numbers() -> set[int]:
    numbers: set[int] = set()
    for path in (_ROOT / "tests/architecture").glob("test_m*.py"):
        match = re.match(r"test_m(\d+)_", path.name)
        if match is not None:
            number = int(match.group(1))
            if 149 <= number <= 198:
                numbers.add(number)
    return numbers


def test_m199_changes_no_runtime_dependency_ci_or_m198_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m199_consolidates_the_complete_m149_m198_probe_sequence() -> None:
    assert _milestone_test_numbers() == set(range(149, 199))

    roadmap = (_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    roadmap_numbers = {
        int(number)
        for number in re.findall(r"^## M(\d+) ", roadmap, flags=re.MULTILINE)
        if 149 <= int(number) <= 198
    }
    assert roadmap_numbers == set(range(149, 199))

    integration = sorted((_ROOT / "tests/integration").glob("test_windows_cache_cleanup*.py"))
    security = [
        path
        for path in (_ROOT / "docs/security").glob("cache-cleanup-windows*.md")
        if path.name != "cache-cleanup-windows-readiness-refresh.md"
    ]
    assert len(integration) == 50
    assert len(security) == 50


def test_m199_records_the_unresolved_admission_criteria() -> None:
    compact = " ".join(_DECISION.read_text(encoding="utf-8").casefold().split())
    for required in (
        "windows is not admitted",
        "m149-m198",
        "50-milestone",
        "current-host",
        "same-principal",
        "authenticated authority",
        "trusted root",
        "hard-link enumeration",
        "use-time identity and link-count revalidation",
        "durable intent",
        "idempotent recovery",
        "typed receipts",
        "cross-principal",
        "independent-host",
        "no hosted check is added",
    ):
        assert required in compact


def test_m199_closes_method_level_probing_without_claiming_portability() -> None:
    compact = " ".join(_DECISION.read_text(encoding="utf-8").casefold().split())
    for required in (
        "method-by-method closed-stream probe tail is closed",
        "future milestone must resolve a named admission criterion",
        "does not establish portable behavior",
        "does not establish native-call suppression",
        "no cleanup authority",
    ):
        assert required in compact

    for forbidden in (
        "windows is admitted",
        "cleanup is authorized",
        "production ready",
    ):
        assert forbidden not in compact


def test_m199_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "no authority increase" in compact
    assert "readiness remains deferred" in compact
    assert "not a new architecture direction" in compact
    assert "use no new hosted allocation" in compact


def test_m199_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "cache-cleanup-windows-readiness-refresh"
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
    assert "0182-refresh-windows-cache-cleanup-readiness.md" in rfc_index


def test_m199_adds_no_cleanup_command_adapter_or_public_probe() -> None:
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
        "cleanup_capabilities.py",
        "filesystem_adapter.py",
        "garbage_collection.py",
        "retention.py",
    }.isdisjoint(names)
