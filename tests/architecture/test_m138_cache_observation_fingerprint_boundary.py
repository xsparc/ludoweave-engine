"""Protect deterministic read-only M138 cache observation fingerprinting."""

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
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_inventory_wheel.py": "b3d70140b5468e1cfb448d33c05f159b4260d3271592fe333abbe31f9e4d7ce4",
    "docs/rfcs/0120-add-bounded-asset-cache-inventory.md": "8e8adaf89431111739148d710743768f6233c26b8a9fc4f28166b62df6df8b44",
    "tests/architecture/test_m137_bounded_asset_cache_inventory_boundary.py": "67ce74ea2f7b9653bda2cec6960f951eef234a90ed266132b6723af949ee2c96",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m138_retains_ci_dependencies_storage_release_and_m137_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_fingerprint_reuses_one_bounded_verified_storage_observation() -> None:
    source = (_ROOT / "src/ludoweave/assets/inventory.py").read_text(encoding="utf-8")
    block = source.split("def fingerprint_asset_cache_observation(", 1)[1].split("\ndef ", 1)[0]
    assert block.count("_observe_storage(") == 1
    assert block.index("_observe_storage(") < block.index("_inventory_from_storage(")
    assert block.index("_inventory_from_storage(") < block.index("_observation_sha256(")
    assert "AssetCacheStore(" not in block


def test_fingerprint_has_domain_separated_sorted_length_framing() -> None:
    source = (_ROOT / "src/ludoweave/assets/inventory.py").read_text(encoding="utf-8")
    block = source.split("def _observation_sha256(", 1)[1].split("\ndef ", 1)[0]
    assert "ASSET_CACHE_FINGERPRINT_PROTOCOL.encode" in block
    assert "for cache_key in sorted(actions)" in block
    assert "for artifact_sha256 in sorted(blobs)" in block
    assert "_metadata_bytes(actions[cache_key].result)" in block
    assert 'len(payload).to_bytes(8, "big")' in block
    assert 'bytes.fromhex(artifact_sha256.removeprefix("sha256:"))' in block
    compact = "".join(block.split())
    assert 'blobs[artifact_sha256].to_bytes(8,"big")' in compact
    assert "st_mtime" not in source
    assert "time_ns" not in source


def test_fingerprint_adds_no_cleanup_mutation_remote_or_backend_capability() -> None:
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


def test_cli_verifies_current_plan_before_read_only_fingerprint() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-fingerprint"' in cli
    block = cli.split("def _run_asset_cache_fingerprint(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index(
        "fingerprint_asset_cache_observation"
    )
    assert "_acquire_asset_build_inputs" not in block
    assert "AssetCacheStore" not in block
    assert ".publish(" not in block


def test_m138_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_fingerprint.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_fingerprint_wheel.py",
        "docs/rfcs/0121-add-deterministic-cache-observation-fingerprint.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0121-add-deterministic-cache-observation-fingerprint.md",
        )
    ).casefold()
    assert "m138" in combined
    assert "ludoweave.asset-cache-fingerprint/1" in combined
    assert "sequential observation" in combined
    assert "not deletion eligibility" in combined
    assert "no ci change" in combined
