"""Protect bounded whole-cache M137 inventory and prior cache contracts."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5",
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
    "src/ludoweave/__init__.py": "dc8ac74a439a1e190a976a6a87713612fa27ce3b8218f1c11695f2c52c65970e",
    "src/ludoweave/assets/cache.py": "bc0c253a46bd81735e15d5ba899d7e3b7cdcd7ecedde5b726f6c27dab410699f",
    "src/ludoweave/assets/population_verification.py": "d08bef93809082cee7d0adc353db68c15c58e5ab815af620515fb63c42c9596d",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_population_verification_wheel.py": "056af8032c21fcaf8ae068b92747304ff578a5bfc8bd383b3dac1bb7e7fcc5c7",
    "docs/rfcs/0119-add-saved-cache-population-verification.md": "bcc5b8bd0b9ebfa0ac56e4b425c3960ce8b51535fac4e5ebef541f47f472222c",
    "tests/architecture/test_m136_saved_cache_population_verification_boundary.py": "d399dee4484d2373da0444aabededd07c46288f352327b1a0d772b97698ca0f6",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m137_retains_ci_dependencies_storage_and_m136_contracts() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_inventory_is_bounded_strict_no_follow_and_content_verifying() -> None:
    source = (_ROOT / "src/ludoweave/assets/inventory.py").read_text(encoding="utf-8")
    assert "ASSET_CACHE_INVENTORY_MAX_ACTIONS" in source
    assert "ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS" in source
    assert "ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES" in source
    assert "ASSET_CACHE_INVENTORY_MAX_CAS_BYTES" in source
    assert "os.scandir" in source
    assert ".lstat()" in source
    assert "_is_reparse" in source
    assert "object_pairs_hook=_unique_object" in source
    assert "parse_constant=_reject_constant" in source
    assert "payload != _metadata_bytes(result)" in source
    assert "observed != blob.name" in source
    assert "_require_action_blobs" in source
    assert ".rglob(" not in source
    assert ".walk(" not in source


def test_inventory_enforces_aggregate_budgets_before_file_open() -> None:
    source = (_ROOT / "src/ludoweave/assets/inventory.py").read_text(encoding="utf-8")
    regular = source.split("def _read_regular(", 1)[1].split("\ndef ", 1)[0]
    hashing = source.split("def _hash_regular(", 1)[1].split("\ndef ", 1)[0]
    assert regular.index("total_before + info.st_size > total_limit") < regular.index(
        'path.open("rb")'
    )
    assert hashing.index("total_before + info.st_size > total_limit") < hashing.index(
        'path.open("rb")'
    )


def test_inventory_has_no_mutation_remote_or_backend_capability() -> None:
    source = (_ROOT / "src/ludoweave/assets/inventory.py").read_text(encoding="utf-8").casefold()
    for forbidden in (
        "write_bytes",
        "write_text",
        "mkdir",
        "unlink",
        "rmtree",
        "remove(",
        "replace(",
        "tempfile",
        "requests",
        "urllib",
        "socket",
        "subprocess",
        "thread",
        "asyncio",
        "multiprocessing",
        "wgpu",
        "glfw",
        "numpy",
        "importlib",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source


def test_cli_verifies_current_plan_before_read_only_inventory() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-inventory"' in cli
    block = cli.split("def _run_asset_cache_inventory(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index(
        "inspect_asset_cache_inventory"
    )
    assert "_acquire_asset_build_inputs" not in block
    assert "AssetCacheStore" not in block
    assert ".publish(" not in block


def test_m137_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_inventory.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_inventory_wheel.py",
        "docs/rfcs/0120-add-bounded-asset-cache-inventory.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0120-add-bounded-asset-cache-inventory.md",
        )
    ).casefold()
    assert "m137" in combined
    assert "ludoweave.asset-cache-inventory/1" in combined
    assert "read-only" in combined
    assert "not deletion eligibility" in combined
    assert "no ci change" in combined
