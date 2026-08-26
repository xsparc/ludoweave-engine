"""Protect bounded path-free M140 saved cache-fingerprint comparison."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5",
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
    "src/ludoweave/assets/cache.py": "bc0c253a46bd81735e15d5ba899d7e3b7cdcd7ecedde5b726f6c27dab410699f",
    "src/ludoweave/assets/inventory.py": "5da1b6074bae2c09d2737a404ff10b0091b089a627615e2d0af755aed98017e8",
    "src/ludoweave/assets/fingerprint_verification.py": "19f992d3a9ab6465e41808789453823d29cbb228ffc277b5e0e55c7cb8a27f8c",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_fingerprint_verification_wheel.py": "00cf1b7042b169af640f831d5eed1e67e1899e9de5688e23764a957b49926ee8",
    "docs/rfcs/0122-add-saved-cache-fingerprint-verification.md": "bc1136e4ea3548f28d87e68c620769d0786f96509bc71e7a0956cebe5bd75370",
    "tests/architecture/test_m139_saved_cache_fingerprint_verification_boundary.py": "3122331859b265673f614adb75c80ef03e602761bc440b636261946250b9235c",
}
_DELTA_FIELDS = (
    "current_actions",
    "missing_actions",
    "other_actions",
    "current_action_metadata_bytes",
    "other_action_metadata_bytes",
    "cas_blobs",
    "current_blobs",
    "other_blobs",
    "current_blob_bytes",
    "other_blob_bytes",
    "unreferenced_blobs",
    "unreferenced_blob_bytes",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source() -> str:
    return (_ROOT / "src/ludoweave/assets/fingerprint_comparison.py").read_text(encoding="utf-8")


def test_m140_retains_ci_dependencies_storage_release_and_m139_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_comparison_preflights_before_exactly_one_m138_observation() -> None:
    block = _source().split("def compare_asset_cache_fingerprint(", 1)[1].split("\ndef ", 1)[0]
    assert block.count("fingerprint_asset_cache_observation(") == 1
    assert block.index("_preflight(plan, fingerprint)") < block.index(
        "fingerprint_asset_cache_observation("
    )
    assert "AssetCacheStore(" not in block


def test_report_has_only_fixed_aggregate_deltas_and_equality_flag() -> None:
    tree = ast.parse(_source())
    field_method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "field_names"
    )
    returned = next(node for node in ast.walk(field_method) if isinstance(node, ast.Return))
    assert isinstance(returned.value, ast.Tuple)
    assert tuple(ast.literal_eval(item) for item in returned.value.elts) == _DELTA_FIELDS
    report_block = (
        _source().split("def as_dict(self) -> dict[str, object]:", 1)[1].split("\n    def ", 1)[0]
    )
    assert '"observation_equal": self.observation_equal' in report_block
    assert '"deltas": self.deltas.as_dict()' in report_block
    assert '"observation_sha256"' not in report_block
    assert '"path"' not in report_block
    assert '"identity"' not in report_block


def test_comparison_adds_no_mutation_remote_cleanup_or_backend_capability() -> None:
    source = _source().casefold()
    for forbidden in (
        "write_bytes",
        "write_text",
        "mkdir",
        "unlink",
        "rmdir",
        "rmtree",
        "remove(",
        "replace(",
        "tempfile",
        "requests",
        "urllib",
        "socket",
        "subprocess",
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


def test_cli_checks_current_inputs_then_record_then_cache_and_uses_diagnostic_exit() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-fingerprint-compare"' in cli
    block = cli.split("def _run_asset_cache_fingerprint_compare(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index("project.read_relative(")
    assert block.index("decode_asset_cache_fingerprint(") < block.index(
        "compare_asset_cache_fingerprint("
    )
    assert "return 0 if comparison.equal else 1" in block
    assert "_acquire_asset_build_inputs" not in block
    assert ".publish(" not in block


def test_m140_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_fingerprint_comparison.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_fingerprint_comparison_wheel.py",
        "docs/rfcs/0123-add-path-free-cache-fingerprint-comparison.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0123-add-path-free-cache-fingerprint-comparison.md",
        )
    ).casefold()
    compact = " ".join(combined.split())
    assert "m140" in combined
    assert "ludoweave.asset-cache-fingerprint-comparison/1" in combined
    assert "aggregate" in combined
    assert "path-free" in combined
    assert "not authenticity" in combined
    assert "no ci change" in compact
