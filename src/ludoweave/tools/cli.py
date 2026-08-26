"""Standard-library command-line adapters for deterministic headless workflows."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave import __version__
from ludoweave.agent import AGENT_TOOL_NAMES
from ludoweave.assets import (
    ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES,
    ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
    ASSET_CACHE_POPULATION_RECORD_MAX_BYTES,
    ASSET_SOURCE_MAX_BYTES,
    ASSET_SOURCE_TOTAL_MAX_BYTES,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCachePopulationRecord,
    AssetCacheStore,
    AssetError,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    compare_asset_cache_fingerprint,
    compare_asset_cache_fingerprint_records,
    decode_asset_cache_fingerprint,
    decode_asset_cache_fingerprint_comparison,
    execute_asset_build_plan,
    fingerprint_asset_cache_observation,
    inspect_asset_cache_inventory,
    materialize_asset_build_plan,
    populate_asset_build_cache,
    realize_asset_build_plan,
    verify_asset_cache_fingerprint,
    verify_asset_cache_fingerprint_comparison,
    verify_asset_cache_population,
)
from ludoweave.core.errors import LudoWeaveError
from ludoweave.plugins import (
    PluginDeterminism,
    PluginManifest,
    PluginManifestError,
    check_plugin_compatibility,
    current_plugin_context,
)
from ludoweave.samples import create_agent_world_builder
from ludoweave.scene import SourceLock, SourceLockEntry
from ludoweave.tools.agent_service import headless_agent_service
from ludoweave.tools.doctor import run_doctor
from ludoweave.tools.headless_project import HeadlessProject
from ludoweave.tools.inspector import InspectorConfig, run_inspector
from ludoweave.tools.mcp import McpServer, run_stdio
from ludoweave.world import (
    CommandActor,
    CommandTransaction,
    ReceiptStatus,
    ReplayRecorder,
    TransactionService,
    canonical_dumps,
    canonical_loads,
    semantic_diff,
)
from ludoweave.world.canonical import JsonValue

_MAX_TRANSACTION_BYTES = 1_048_576
_MAX_SNAPSHOT_BYTES = 67_108_864
_MAX_REPLAY_BYTES = 134_217_728
_MAX_AGENT_REQUEST_BYTES = 1_048_576
_MAX_PLUGIN_MANIFEST_BYTES = 65_536
_MAX_PLUGIN_MANIFESTS = 64


@dataclass(frozen=True, slots=True)
class _SourceAssetDeclaration:
    entry_id: str
    kind: str
    dependencies: tuple[AssetUri, ...]


@dataclass(frozen=True, slots=True)
class _SourceManifestInspection:
    lock: SourceLock
    manifest_protocol: str
    check_entries: tuple[JsonValue, ...]
    asset_dependencies: tuple[_SourceAssetDeclaration, ...]
    scenes: int
    prefabs: int
    entities: int
    overrides: int
    dependencies: int


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ludoweave",
        description="Deterministic, headless-first Python engine for agent-operable 2D worlds.",
    )
    parser.add_argument("--version", action="version", version=f"ludoweave {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("doctor", help="run structured local environment diagnostics")

    source_parser = subparsers.add_parser("source", help="validate project-confined sources")
    source_subparsers = source_parser.add_subparsers(dest="source_command", required=True)
    source_check_parser = source_subparsers.add_parser(
        "check",
        help="check one scene or one explicit prefab source/instance pair",
    )
    source_check_parser.add_argument("project", type=Path, help="project directory")
    source_mode = source_check_parser.add_mutually_exclusive_group(required=True)
    source_mode.add_argument("--scene", help="project-relative scene JSON")
    source_mode.add_argument("--prefab", help="project-relative prefab source JSON")
    source_mode.add_argument("--manifest", help="project-relative explicit source manifest")
    source_check_parser.add_argument(
        "--instance",
        help="project-relative prefab instance JSON; required with --prefab",
    )
    source_lock_parser = source_subparsers.add_parser(
        "lock",
        help="emit a canonical path-independent lock for one explicit source manifest",
    )
    source_lock_parser.add_argument("project", type=Path, help="project directory")
    source_lock_parser.add_argument(
        "--manifest", required=True, help="project-relative explicit source manifest"
    )
    source_verify_parser = source_subparsers.add_parser(
        "verify",
        help="verify current explicit sources against one confined source lock",
    )
    source_verify_parser.add_argument("project", type=Path, help="project directory")
    source_verify_parser.add_argument(
        "--manifest", required=True, help="project-relative explicit source manifest"
    )
    source_verify_parser.add_argument(
        "--lock", required=True, help="project-relative source-integrity lock"
    )
    source_assets_parser = source_subparsers.add_parser(
        "assets",
        help="check declared source assets and resolve their asset-graph dependencies",
    )
    source_assets_parser.add_argument("project", type=Path, help="project directory")
    source_assets_parser.add_argument(
        "--manifest", required=True, help="project-relative explicit source manifest"
    )
    source_assets_parser.add_argument(
        "--assets", required=True, help="project-relative asset manifest"
    )
    source_asset_lock_parser = source_subparsers.add_parser(
        "asset-lock",
        help="emit a canonical lock for source-selected asset input bytes",
    )
    _add_asset_source_arguments(source_asset_lock_parser)
    source_asset_verify_parser = source_subparsers.add_parser(
        "asset-verify",
        help="verify selected asset input bytes against one confined lock",
    )
    _add_asset_source_arguments(source_asset_verify_parser)
    source_asset_verify_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_plan_parser = source_subparsers.add_parser(
        "asset-plan",
        help="emit a dependency-first plan for verified selected asset inputs",
    )
    _add_asset_source_arguments(source_asset_plan_parser)
    source_asset_plan_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_plan_verify_parser = source_subparsers.add_parser(
        "asset-plan-verify",
        help="verify a saved asset plan against current selected inputs",
    )
    _add_asset_source_arguments(source_asset_plan_verify_parser)
    source_asset_plan_verify_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_plan_verify_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_build_parser = source_subparsers.add_parser(
        "asset-build",
        help="execute built-in decoders for one verified asset build plan",
    )
    _add_asset_source_arguments(source_asset_build_parser)
    source_asset_build_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_build_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_parser = source_subparsers.add_parser(
        "asset-cache",
        help="publish verified built-in decoder outputs to one explicit local cache",
    )
    _add_asset_source_arguments(source_asset_cache_parser)
    source_asset_cache_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_cache_check_parser = source_subparsers.add_parser(
        "asset-cache-check",
        help="inspect verified local cache hits for one exact current asset plan",
    )
    _add_asset_source_arguments(source_asset_cache_check_parser)
    source_asset_cache_check_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_check_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_check_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_cache_inventory_parser = source_subparsers.add_parser(
        "asset-cache-inventory",
        help="verify and classify one bounded engine-owned local cache read-only",
    )
    _add_asset_source_arguments(source_asset_cache_inventory_parser)
    source_asset_cache_inventory_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_inventory_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_inventory_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_cache_fingerprint_parser = source_subparsers.add_parser(
        "asset-cache-fingerprint",
        help="fingerprint one verified sequential local-cache observation",
    )
    _add_asset_source_arguments(source_asset_cache_fingerprint_parser)
    source_asset_cache_fingerprint_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_fingerprint_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_fingerprint_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_cache_fingerprint_verify_parser = source_subparsers.add_parser(
        "asset-cache-fingerprint-verify",
        help="verify saved fingerprint evidence against an exact current plan and cache",
    )
    _add_asset_source_arguments(source_asset_cache_fingerprint_verify_parser)
    source_asset_cache_fingerprint_verify_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_fingerprint_verify_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_fingerprint_verify_parser.add_argument(
        "--fingerprint", required=True, help="project-relative saved cache fingerprint"
    )
    source_asset_cache_fingerprint_verify_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_cache_fingerprint_compare_parser = source_subparsers.add_parser(
        "asset-cache-fingerprint-compare",
        help="diagnose path-free aggregate changes from one saved cache fingerprint",
    )
    _add_asset_source_arguments(source_asset_cache_fingerprint_compare_parser)
    source_asset_cache_fingerprint_compare_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_fingerprint_compare_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_fingerprint_compare_parser.add_argument(
        "--fingerprint", required=True, help="project-relative saved cache fingerprint"
    )
    source_asset_cache_fingerprint_compare_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_cache_fingerprint_record_compare_parser = source_subparsers.add_parser(
        "asset-cache-fingerprint-record-compare",
        help="compare two saved cache fingerprints without cache access",
    )
    _add_asset_source_arguments(source_asset_cache_fingerprint_record_compare_parser)
    source_asset_cache_fingerprint_record_compare_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_fingerprint_record_compare_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_fingerprint_record_compare_parser.add_argument(
        "--expected-fingerprint",
        required=True,
        help="project-relative expected cache fingerprint",
    )
    source_asset_cache_fingerprint_record_compare_parser.add_argument(
        "--current-fingerprint",
        required=True,
        help="project-relative current cache fingerprint",
    )
    source_asset_cache_fingerprint_comparison_verify_parser = source_subparsers.add_parser(
        "asset-cache-fingerprint-comparison-verify",
        help="verify a saved comparison against two saved cache fingerprints",
    )
    _add_asset_source_arguments(source_asset_cache_fingerprint_comparison_verify_parser)
    source_asset_cache_fingerprint_comparison_verify_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_fingerprint_comparison_verify_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_fingerprint_comparison_verify_parser.add_argument(
        "--expected-fingerprint",
        required=True,
        help="project-relative expected cache fingerprint",
    )
    source_asset_cache_fingerprint_comparison_verify_parser.add_argument(
        "--current-fingerprint",
        required=True,
        help="project-relative current cache fingerprint",
    )
    source_asset_cache_fingerprint_comparison_verify_parser.add_argument(
        "--comparison",
        required=True,
        help="project-relative saved cache-fingerprint comparison",
    )
    source_asset_cache_populate_parser = source_subparsers.add_parser(
        "asset-cache-populate",
        help="realize one exact plan before explicitly populating a local cache",
    )
    _add_asset_source_arguments(source_asset_cache_populate_parser)
    source_asset_cache_populate_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_populate_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_populate_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_cache_population_verify_parser = source_subparsers.add_parser(
        "asset-cache-population-verify",
        help="verify saved population evidence against an exact current plan and cache",
    )
    _add_asset_source_arguments(source_asset_cache_population_verify_parser)
    source_asset_cache_population_verify_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_cache_population_verify_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_cache_population_verify_parser.add_argument(
        "--population", required=True, help="project-relative saved population report"
    )
    source_asset_cache_population_verify_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )
    source_asset_realize_parser = source_subparsers.add_parser(
        "asset-realize",
        help="realize one verified asset plan from read-only cache hits and decoded misses",
    )
    _add_asset_source_arguments(source_asset_realize_parser)
    source_asset_realize_parser.add_argument(
        "--lock", required=True, help="project-relative asset-source lock"
    )
    source_asset_realize_parser.add_argument(
        "--plan", required=True, help="project-relative asset build plan"
    )
    source_asset_realize_parser.add_argument(
        "--cache", required=True, type=Path, help="local cache directory outside the project"
    )

    apply_parser = subparsers.add_parser(
        "apply",
        help="apply one typed transaction to an empty headless project",
    )
    apply_parser.add_argument("project", type=Path, help="project directory")
    apply_parser.add_argument("transaction", help="project-relative transaction JSON")
    apply_parser.add_argument("--state", help="project-relative input snapshot")
    apply_parser.add_argument("--snapshot-out", help="project-relative output snapshot")
    apply_parser.add_argument("--receipt-out", help="project-relative output receipt")
    apply_parser.add_argument("--replay-out", help="project-relative output replay")
    apply_parser.add_argument("--timeline-id", default="cli-timeline")

    snapshot_parser = subparsers.add_parser(
        "snapshot",
        help="materialize a canonical snapshot from a replay tick boundary",
    )
    snapshot_parser.add_argument("project", type=Path, help="project directory")
    snapshot_parser.add_argument("replay", help="project-relative replay document")
    snapshot_parser.add_argument("--tick", type=int, required=True)
    snapshot_parser.add_argument("--out", required=True, help="project-relative output snapshot")

    replay_parser = subparsers.add_parser(
        "replay",
        help="run a canonical replay through the typed transaction service",
    )
    replay_parser.add_argument("project", type=Path, help="project directory")
    replay_parser.add_argument("replay", help="project-relative replay document")
    replay_parser.add_argument("--verify-hashes", action="store_true")
    replay_parser.add_argument("--snapshot-out", help="project-relative final snapshot")

    diff_parser = subparsers.add_parser(
        "diff",
        help="compute a semantic diff between two canonical snapshots",
    )
    diff_parser.add_argument("project", type=Path, help="project directory")
    diff_parser.add_argument("before", help="project-relative base snapshot")
    diff_parser.add_argument("after", help="project-relative candidate snapshot")

    agent_parser = subparsers.add_parser(
        "agent",
        help="invoke one transport-independent typed agent tool",
    )
    agent_parser.add_argument("project", type=Path, help="data-only project directory")
    agent_parser.add_argument("tool", choices=AGENT_TOOL_NAMES)
    agent_parser.add_argument("request", help="project-relative canonical tool arguments")
    agent_parser.add_argument("--state", help="project-relative input snapshot")
    agent_parser.add_argument("--write", action="store_true", help="enable world mutations")
    agent_parser.add_argument("--actor-kind", default="agent")
    agent_parser.add_argument("--actor-id", default="local-cli")

    mcp_parser = subparsers.add_parser(
        "mcp",
        help="run the local-only MCP stdio adapter",
    )
    mcp_parser.add_argument("project", type=Path, nargs="?", help="data-only project directory")
    mcp_parser.add_argument("--sample", choices=("agent-world-builder",))
    mcp_parser.add_argument("--state", help="project-relative input snapshot")
    mcp_parser.add_argument("--write", action="store_true", help="enable world mutations")
    mcp_parser.add_argument("--actor-kind", default="agent")
    mcp_parser.add_argument("--actor-id", default="local-mcp")
    mcp_parser.add_argument(
        "--renderer",
        choices=("none", "wgpu"),
        default="none",
        help="optional built-in sample capture provider",
    )

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="stream semantic observations from an owned local MCP child",
    )
    inspect_parser.add_argument("project", type=Path, nargs="?", help="data-only project directory")
    inspect_parser.add_argument("--sample", choices=("agent-world-builder",))
    inspect_parser.add_argument("--state", help="project-relative input snapshot")
    inspect_parser.add_argument("--write", action="store_true", help="enable world mutations")
    inspect_parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="create the built-in sample through a receipted transaction",
    )
    inspect_parser.add_argument("--ticks", type=int, default=0)
    inspect_parser.add_argument("--query-limit", type=int, default=32)
    inspect_parser.add_argument("--actor-kind", default="inspector")
    inspect_parser.add_argument("--actor-id", default="local-inspector")

    plugin_parser = subparsers.add_parser(
        "plugin",
        help="validate explicit data-only plugin manifests",
    )
    plugin_subparsers = plugin_parser.add_subparsers(dest="plugin_command", required=True)
    plugin_check_parser = plugin_subparsers.add_parser(
        "check",
        help="check manifests against the current CPython and desktop platform",
    )
    plugin_check_parser.add_argument("manifests", type=Path, nargs="+")
    plugin_check_parser.add_argument(
        "--minimum-determinism",
        default=PluginDeterminism.D0.value,
        metavar="{d0,d1,d2}",
    )
    plugin_check_parser.add_argument(
        "--allow-native",
        action="store_true",
        help="allow manifests that declare native implementation code",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""

    parser = _build_parser()
    args = parser.parse_args(argv)
    command: object = getattr(args, "command", None)
    if command == "doctor":
        report, exit_code = run_doctor()
        _print_json(report)
        return exit_code
    try:
        if command == "source":
            source_command: object = getattr(args, "source_command", None)
            if source_command == "check":
                return _run_source_check(args)
            if source_command == "lock":
                return _run_source_lock(args)
            if source_command == "verify":
                return _run_source_verify(args)
            if source_command == "assets":
                return _run_source_assets(args)
            if source_command == "asset-lock":
                return _run_asset_source_lock(args)
            if source_command == "asset-verify":
                return _run_asset_source_verify(args)
            if source_command == "asset-plan":
                return _run_asset_build_plan(args)
            if source_command == "asset-plan-verify":
                return _run_asset_build_plan_verify(args)
            if source_command == "asset-build":
                return _run_asset_build_plan_execute(args)
            if source_command == "asset-cache":
                return _run_asset_cache_publish(args)
            if source_command == "asset-cache-check":
                return _run_asset_cache_check(args)
            if source_command == "asset-cache-inventory":
                return _run_asset_cache_inventory(args)
            if source_command == "asset-cache-fingerprint":
                return _run_asset_cache_fingerprint(args)
            if source_command == "asset-cache-fingerprint-compare":
                return _run_asset_cache_fingerprint_compare(args)
            if source_command == "asset-cache-fingerprint-record-compare":
                return _run_asset_cache_fingerprint_record_compare(args)
            if source_command == "asset-cache-fingerprint-comparison-verify":
                return _run_asset_cache_fingerprint_comparison_verify(args)
            if source_command == "asset-cache-fingerprint-verify":
                return _run_asset_cache_fingerprint_verify(args)
            if source_command == "asset-cache-populate":
                return _run_asset_cache_populate(args)
            if source_command == "asset-cache-population-verify":
                return _run_asset_cache_population_verify(args)
            if source_command == "asset-realize":
                return _run_asset_realize(args)
            raise _argument_error("source_command")
        if command == "apply":
            return _run_apply(args)
        if command == "snapshot":
            return _run_snapshot(args)
        if command == "replay":
            return _run_replay(args)
        if command == "diff":
            return _run_diff(args)
        if command == "agent":
            return _run_agent(args)
        if command == "mcp":
            return _run_mcp(args)
        if command == "inspect":
            return _run_inspect(args)
        if command == "plugin":
            return _run_plugin(args)
    except LudoWeaveError as error:
        _print_error(error)
        return 2
    parser.print_help()
    return 0


def _run_source_check(args: argparse.Namespace) -> int:
    if _text_argument(args, "source_command") != "check":
        raise _argument_error("source_command")
    project = HeadlessProject.load(_path_argument(args, "project"))
    scene_name = _optional_text_argument(args, "scene")
    prefab_name = _optional_text_argument(args, "prefab")
    manifest_name = _optional_text_argument(args, "manifest")
    instance_name = _optional_text_argument(args, "instance")
    if scene_name is not None:
        if instance_name is not None:
            raise _argument_error("source_mode")
        scene = project.load_scene(scene_name)
        _write_stdout(
            canonical_dumps(
                {
                    "protocol": "ludoweave.cli.source-check/1",
                    "status": "valid",
                    "kind": "scene",
                    "source_protocol": scene.protocol,
                    "source_id": scene.scene_id,
                    "source_sha256": f"sha256:{sha256(scene.canonical_bytes()).hexdigest()}",
                    "entities": len(scene.entities),
                    "dependencies": len(scene.dependencies),
                }
            )
        )
        return 0
    if manifest_name is not None:
        if instance_name is not None:
            raise _argument_error("source_mode")
        inspection = _inspect_source_manifest(project, manifest_name)
        _write_stdout(
            canonical_dumps(
                {
                    "protocol": "ludoweave.cli.source-manifest-check/1",
                    "status": "valid",
                    "manifest_protocol": inspection.manifest_protocol,
                    "manifest_id": inspection.lock.manifest_id,
                    "manifest_sha256": inspection.lock.manifest_sha256,
                    "entries": list(inspection.check_entries),
                    "entry_count": len(inspection.check_entries),
                    "scenes": inspection.scenes,
                    "prefabs": inspection.prefabs,
                    "entities": inspection.entities,
                    "overrides": inspection.overrides,
                    "dependencies": inspection.dependencies,
                }
            )
        )
        return 0
    if prefab_name is None or instance_name is None:
        raise _argument_error("source_mode")
    prefab = project.load_prefab(prefab_name)
    instance = project.load_prefab_instance(instance_name)
    _require_prefab_pair(prefab.prefab_id, instance.prefab_id)
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.source-check/1",
                "status": "valid",
                "kind": "prefab",
                "source_protocol": prefab.protocol,
                "instance_protocol": instance.protocol,
                "source_id": prefab.prefab_id,
                "instance_id": instance.instance_id,
                "source_sha256": f"sha256:{sha256(prefab.canonical_bytes()).hexdigest()}",
                "instance_sha256": f"sha256:{sha256(instance.canonical_bytes()).hexdigest()}",
                "entities": len(prefab.entities),
                "overrides": len(instance.overrides),
                "dependencies": len(prefab.dependencies),
            }
        )
    )
    return 0


def _require_prefab_pair(source_id: str, instance_source_id: str) -> None:
    if source_id != instance_source_id:
        raise LudoWeaveError(
            "prefab instance does not identify the supplied source",
            code="tools.prefab_source_mismatch",
            subsystem="tools",
            phase="check_source",
            details={"field": "prefab_id"},
        )


def _run_source_lock(args: argparse.Namespace) -> int:
    inspection = _inspect_source_manifest(
        HeadlessProject.load(_path_argument(args, "project")),
        _text_argument(args, "manifest"),
    )
    _write_stdout(inspection.lock.canonical_bytes())
    return 0


def _run_source_verify(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected = project.load_source_lock(_text_argument(args, "lock"))
    inspection = _inspect_source_manifest(project, _text_argument(args, "manifest"))
    expected.verify(inspection.lock)
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.source-lock-verify/1",
                "status": "verified",
                "manifest_id": inspection.lock.manifest_id,
                "manifest_sha256": inspection.lock.manifest_sha256,
                "entry_count": len(inspection.lock.entries),
            }
        )
    )
    return 0


def _run_source_assets(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    inspection = _inspect_source_manifest(project, _text_argument(args, "manifest"))
    asset_manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    entries: list[JsonValue] = []
    all_direct: set[AssetUri] = set()
    all_resolved: set[AssetUri] = set()
    for declaration in inspection.asset_dependencies:
        for dependency in declaration.dependencies:
            try:
                asset_manifest.entry(dependency)
            except AssetError as error:
                raise LudoWeaveError(
                    "source declares an asset absent from the explicit asset manifest",
                    code="tools.missing_asset_dependency",
                    subsystem="tools",
                    phase="check_source_assets",
                    details={
                        "entry_id": declaration.entry_id,
                        "dependency": dependency.value,
                    },
                ) from error
        resolved = asset_manifest.dependency_closure(declaration.dependencies)
        all_direct.update(declaration.dependencies)
        all_resolved.update(resolved)
        entries.append(
            {
                "entry_id": declaration.entry_id,
                "kind": declaration.kind,
                "direct": [dependency.value for dependency in declaration.dependencies],
                "resolved": [dependency.value for dependency in resolved],
            }
        )
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.source-asset-check/1",
                "status": "valid",
                "source_manifest_protocol": inspection.manifest_protocol,
                "source_manifest_id": inspection.lock.manifest_id,
                "source_manifest_sha256": inspection.lock.manifest_sha256,
                "asset_manifest_protocol": asset_manifest.protocol,
                "asset_manifest_sha256": (
                    f"sha256:{sha256(asset_manifest.canonical_bytes()).hexdigest()}"
                ),
                "entries": entries,
                "entry_count": len(entries),
                "direct_asset_count": len(all_direct),
                "resolved_asset_count": len(all_resolved),
            }
        )
    )
    return 0


def _add_asset_source_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("project", type=Path, help="project directory")
    parser.add_argument(
        "--manifest", required=True, help="project-relative explicit source manifest"
    )
    parser.add_argument("--assets", required=True, help="project-relative asset manifest")


def _run_asset_source_lock(args: argparse.Namespace) -> int:
    _write_stdout(_current_asset_source_lock(args).canonical_bytes())
    return 0


def _run_asset_source_verify(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected = project.load_asset_source_lock(_text_argument(args, "lock"))
    current = _current_asset_source_lock(args, project=project)
    expected.verify(current)
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.asset-source-lock-verify/1",
                "status": "valid",
                "lock_protocol": current.protocol,
                "root_count": len(current.roots),
                "entry_count": len(current.entries),
            }
        )
    )
    return 0


def _run_asset_build_plan(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected = project.load_asset_source_lock(_text_argument(args, "lock"))
    current = _current_asset_source_lock(args, project=project)
    expected.verify(current)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    plan = AssetBuildPlan.from_inputs(manifest, current)
    _write_stdout(plan.canonical_bytes())
    return 0


def _run_asset_build_plan_verify(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.asset-build-plan-verify/1",
                "status": "valid",
                "plan_protocol": current_plan.protocol,
                "loader_protocol": current_plan.loader_protocol,
                "root_count": len(current_plan.roots),
                "entry_count": len(current_plan.entries),
            }
        )
    )
    return 0


def _run_asset_build_plan_execute(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    inputs = _acquire_asset_build_inputs(project, manifest, current_plan)
    result = execute_asset_build_plan(current_plan, inputs)
    _write_stdout(result.canonical_bytes())
    return 0


def _run_asset_cache_publish(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    inputs = _acquire_asset_build_inputs(project, manifest, current_plan)
    materialized = materialize_asset_build_plan(current_plan, inputs)
    store = AssetCacheStore(_path_argument(args, "cache"), project_root=project.root)
    summary = store.publish(materialized)
    _write_stdout(summary.canonical_bytes())
    return 0


def _run_asset_cache_check(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    store = AssetCacheStore(
        _path_argument(args, "cache"),
        project_root=project.root,
        writable=False,
    )
    summary = store.inspect(current_plan)
    _write_stdout(summary.canonical_bytes())
    return 0


def _run_asset_cache_inventory(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    inventory = inspect_asset_cache_inventory(
        current_plan,
        _path_argument(args, "cache"),
        project_root=project.root,
    )
    _write_stdout(inventory.canonical_bytes())
    return 0


def _run_asset_cache_fingerprint(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    fingerprint = fingerprint_asset_cache_observation(
        current_plan,
        _path_argument(args, "cache"),
        project_root=project.root,
    )
    _write_stdout(fingerprint.canonical_bytes())
    return 0


def _run_asset_cache_fingerprint_verify(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    fingerprint_document = project.read_relative(
        _text_argument(args, "fingerprint"),
        max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
        role="asset_cache_fingerprint",
    )
    fingerprint = decode_asset_cache_fingerprint(fingerprint_document)
    verification = verify_asset_cache_fingerprint(
        current_plan,
        fingerprint,
        _path_argument(args, "cache"),
        project_root=project.root,
    )
    _write_stdout(verification.canonical_bytes())
    return 0


def _run_asset_cache_fingerprint_compare(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    fingerprint_document = project.read_relative(
        _text_argument(args, "fingerprint"),
        max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
        role="asset_cache_fingerprint",
    )
    fingerprint = decode_asset_cache_fingerprint(fingerprint_document)
    comparison = compare_asset_cache_fingerprint(
        current_plan,
        fingerprint,
        _path_argument(args, "cache"),
        project_root=project.root,
    )
    _write_stdout(comparison.canonical_bytes())
    return 0 if comparison.equal else 1


def _run_asset_cache_fingerprint_record_compare(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    expected_document = project.read_relative(
        _text_argument(args, "expected_fingerprint"),
        max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
        role="expected_asset_cache_fingerprint",
    )
    current_document = project.read_relative(
        _text_argument(args, "current_fingerprint"),
        max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
        role="current_asset_cache_fingerprint",
    )
    expected = decode_asset_cache_fingerprint(expected_document)
    current = decode_asset_cache_fingerprint(current_document)
    comparison = compare_asset_cache_fingerprint_records(current_plan, expected, current)
    _write_stdout(comparison.canonical_bytes())
    return 0 if comparison.equal else 1


def _run_asset_cache_fingerprint_comparison_verify(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    expected = decode_asset_cache_fingerprint(
        project.read_relative(
            _text_argument(args, "expected_fingerprint"),
            max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
            role="expected_asset_cache_fingerprint",
        )
    )
    current = decode_asset_cache_fingerprint(
        project.read_relative(
            _text_argument(args, "current_fingerprint"),
            max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
            role="current_asset_cache_fingerprint",
        )
    )
    comparison = decode_asset_cache_fingerprint_comparison(
        project.read_relative(
            _text_argument(args, "comparison"),
            max_bytes=ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES,
            role="asset_cache_fingerprint_comparison",
        )
    )
    verification = verify_asset_cache_fingerprint_comparison(
        current_plan,
        expected,
        current,
        comparison,
    )
    _write_stdout(verification.canonical_bytes())
    return 0


def _run_asset_realize(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    inputs = _acquire_asset_build_inputs(project, manifest, current_plan)
    store = AssetCacheStore(
        _path_argument(args, "cache"),
        project_root=project.root,
        writable=False,
    )
    realization = realize_asset_build_plan(current_plan, inputs, store)
    _write_stdout(realization.canonical_bytes())
    return 0


def _run_asset_cache_populate(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    inputs = _acquire_asset_build_inputs(project, manifest, current_plan)
    population = populate_asset_build_cache(
        current_plan,
        inputs,
        _path_argument(args, "cache"),
        project_root=project.root,
    )
    _write_stdout(population.canonical_bytes())
    return 0


def _run_asset_cache_population_verify(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    expected_plan = project.load_asset_build_plan(_text_argument(args, "plan"))
    expected_lock = project.load_asset_source_lock(_text_argument(args, "lock"))
    current_lock = _current_asset_source_lock(args, project=project)
    expected_lock.verify(current_lock)
    manifest = project.load_asset_manifest(_text_argument(args, "assets"))
    current_plan = AssetBuildPlan.from_inputs(manifest, current_lock)
    expected_plan.verify(current_plan)
    population_document = project.read_relative(
        _text_argument(args, "population"),
        max_bytes=ASSET_CACHE_POPULATION_RECORD_MAX_BYTES,
        role="asset_cache_population",
    )
    population = AssetCachePopulationRecord.from_json(population_document)
    verification = verify_asset_cache_population(
        current_plan,
        population,
        _path_argument(args, "cache"),
        project_root=project.root,
    )
    _write_stdout(verification.canonical_bytes())
    return 0


def _acquire_asset_build_inputs(
    project: HeadlessProject,
    manifest: AssetManifest,
    plan: AssetBuildPlan,
) -> tuple[AssetBuildInput, ...]:
    inputs: list[AssetBuildInput] = []
    total_bytes = 0
    for entry in plan.entries:
        source = manifest.entry(entry.uri).source
        try:
            payload = project.read_relative(
                source,
                max_bytes=ASSET_SOURCE_MAX_BYTES,
                role="asset_build_source",
            )
        except LudoWeaveError as error:
            raise LudoWeaveError(
                "verified asset source could not be acquired for execution",
                code="tools.asset_build_source_unavailable",
                subsystem="tools",
                phase="execute_asset_plan",
                details={"uri": entry.uri.value, "cause_code": error.code},
            ) from error
        total_bytes += len(payload)
        if total_bytes > ASSET_SOURCE_TOTAL_MAX_BYTES:
            raise LudoWeaveError(
                "asset build sources exceed the aggregate execution bound",
                code="tools.asset_build_sources_oversized",
                subsystem="tools",
                phase="execute_asset_plan",
                details={"uri": entry.uri.value, "limit": ASSET_SOURCE_TOTAL_MAX_BYTES},
            )
        inputs.append(AssetBuildInput(entry.uri, payload))
    return tuple(inputs)


def _current_asset_source_lock(
    args: argparse.Namespace,
    *,
    project: HeadlessProject | None = None,
) -> AssetSourceLock:
    selected_project = (
        HeadlessProject.load(_path_argument(args, "project")) if project is None else project
    )
    inspection = _inspect_source_manifest(
        selected_project,
        _text_argument(args, "manifest"),
    )
    manifest = selected_project.load_asset_manifest(_text_argument(args, "assets"))
    roots = _source_asset_roots(inspection, manifest)
    resolved = manifest.dependency_closure(roots)
    locked: list[AssetSourceLockEntry] = []
    total_bytes = 0
    for uri in resolved:
        entry = manifest.entry(uri)
        try:
            source_hash, source_bytes = selected_project.hash_relative(
                entry.source,
                max_bytes=ASSET_SOURCE_MAX_BYTES,
                role="asset_source",
            )
        except LudoWeaveError as error:
            code = (
                "tools.asset_source_oversized"
                if error.code == "tools.input_oversized"
                else "tools.asset_source_unavailable"
            )
            raise LudoWeaveError(
                "selected asset source could not be read within its bounds",
                code=code,
                subsystem="tools",
                phase="lock_asset_sources",
                details={"uri": uri.value, "cause_code": error.code},
            ) from error
        total_bytes += source_bytes
        if total_bytes > ASSET_SOURCE_TOTAL_MAX_BYTES:
            raise LudoWeaveError(
                "selected asset sources exceed the aggregate byte bound",
                code="tools.asset_sources_oversized",
                subsystem="tools",
                phase="lock_asset_sources",
                details={"uri": uri.value, "limit": ASSET_SOURCE_TOTAL_MAX_BYTES},
            )
        locked.append(
            AssetSourceLockEntry(
                uri=uri,
                kind=entry.kind,
                source_sha256=source_hash,
                source_bytes=source_bytes,
            )
        )
    return AssetSourceLock(
        source_lock_sha256=(f"sha256:{sha256(inspection.lock.canonical_bytes()).hexdigest()}"),
        asset_manifest_sha256=(f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}"),
        roots=roots,
        entries=tuple(locked),
    )


def _source_asset_roots(
    inspection: _SourceManifestInspection,
    manifest: AssetManifest,
) -> tuple[AssetUri, ...]:
    roots: set[AssetUri] = set()
    for declaration in inspection.asset_dependencies:
        for dependency in declaration.dependencies:
            try:
                manifest.entry(dependency)
            except AssetError as error:
                raise LudoWeaveError(
                    "source declares an asset absent from the explicit asset manifest",
                    code="tools.missing_asset_dependency",
                    subsystem="tools",
                    phase="check_source_assets",
                    details={
                        "entry_id": declaration.entry_id,
                        "dependency": dependency.value,
                    },
                ) from error
            roots.add(dependency)
    return tuple(sorted(roots))


def _inspect_source_manifest(
    project: HeadlessProject,
    manifest_name: str,
) -> _SourceManifestInspection:
    manifest = project.load_source_manifest(manifest_name)
    lock_entries: list[SourceLockEntry] = []
    check_entries: list[JsonValue] = []
    asset_dependencies: list[_SourceAssetDeclaration] = []
    scenes = 0
    prefabs = 0
    entities = 0
    dependencies = 0
    overrides = 0
    for entry in manifest.entries:
        if entry.kind == "scene":
            scene = project.load_scene(entry.source)
            dependencies_for_entry = scene.dependencies
            source_sha256 = f"sha256:{sha256(scene.canonical_bytes()).hexdigest()}"
            lock_entries.append(
                SourceLockEntry(
                    entry.entry_id,
                    "scene",
                    scene.protocol,
                    scene.scene_id,
                    source_sha256,
                )
            )
            result: dict[str, JsonValue] = {
                "entry_id": entry.entry_id,
                "kind": "scene",
                "source_protocol": scene.protocol,
                "source_id": scene.scene_id,
                "source_sha256": source_sha256,
                "entities": len(scene.entities),
                "dependencies": len(scene.dependencies),
            }
            scenes += 1
            entities += len(scene.entities)
            dependencies += len(scene.dependencies)
        else:
            if entry.instance is None:
                raise _argument_error("source_manifest")
            prefab = project.load_prefab(entry.source)
            instance = project.load_prefab_instance(entry.instance)
            _require_prefab_pair(prefab.prefab_id, instance.prefab_id)
            dependencies_for_entry = prefab.dependencies
            source_sha256 = f"sha256:{sha256(prefab.canonical_bytes()).hexdigest()}"
            instance_sha256 = f"sha256:{sha256(instance.canonical_bytes()).hexdigest()}"
            lock_entries.append(
                SourceLockEntry(
                    entry.entry_id,
                    "prefab",
                    prefab.protocol,
                    prefab.prefab_id,
                    source_sha256,
                    instance_protocol=instance.protocol,
                    instance_id=instance.instance_id,
                    instance_sha256=instance_sha256,
                )
            )
            result = {
                "entry_id": entry.entry_id,
                "kind": "prefab",
                "source_protocol": prefab.protocol,
                "instance_protocol": instance.protocol,
                "source_id": prefab.prefab_id,
                "instance_id": instance.instance_id,
                "source_sha256": source_sha256,
                "instance_sha256": instance_sha256,
                "entities": len(prefab.entities),
                "overrides": len(instance.overrides),
                "dependencies": len(prefab.dependencies),
            }
            prefabs += 1
            entities += len(prefab.entities)
            overrides += len(instance.overrides)
            dependencies += len(prefab.dependencies)
        asset_dependencies.append(
            _SourceAssetDeclaration(
                entry_id=entry.entry_id,
                kind=entry.kind,
                dependencies=dependencies_for_entry,
            )
        )
        check_entries.append(result)
    manifest_sha256 = f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}"
    return _SourceManifestInspection(
        lock=SourceLock(manifest.manifest_id, manifest_sha256, tuple(lock_entries)),
        manifest_protocol=manifest.protocol,
        check_entries=tuple(check_entries),
        asset_dependencies=tuple(asset_dependencies),
        scenes=scenes,
        prefabs=prefabs,
        entities=entities,
        overrides=overrides,
        dependencies=dependencies,
    )


def _run_apply(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    state_name = _optional_text_argument(args, "state")
    if state_name is None:
        session = project.new_session()
    else:
        session = project.load_snapshot(
            project.read_relative(
                state_name,
                max_bytes=_MAX_SNAPSHOT_BYTES,
                role="state",
            )
        )
    transaction_name = _text_argument(args, "transaction")
    transaction = CommandTransaction.from_json(
        project.read_relative(
            transaction_name,
            max_bytes=_MAX_TRANSACTION_BYTES,
            role="transaction",
        )
    )
    recorder: ReplayRecorder | None = None
    if transaction.dry_run:
        receipt = TransactionService(session).apply(transaction)
    else:
        recorder = ReplayRecorder(
            session,
            project.snapshot_codec,
            timeline_id=_text_argument(args, "timeline_id"),
            project_schema=project.project_schema,
            dependency_lock_hash=project.dependency_lock_hash,
            platform_profile=project.platform_profile,
        )
        receipt = recorder.record(transaction)
    receipt_bytes = receipt.canonical_bytes()
    receipt_name = _optional_text_argument(args, "receipt_out")
    if receipt_name is not None:
        project.write_relative(receipt_name, receipt_bytes, role="receipt")
    if receipt.status is ReceiptStatus.COMMITTED:
        snapshot_name = _optional_text_argument(args, "snapshot_out")
        if snapshot_name is not None:
            project.write_relative(
                snapshot_name,
                project.snapshot_codec.encode(session),
                role="snapshot",
            )
        replay_name = _optional_text_argument(args, "replay_out")
        if replay_name is not None and recorder is not None:
            project.write_relative(
                replay_name,
                recorder.timeline().canonical_bytes(),
                role="replay",
            )
    _write_stdout(receipt_bytes)
    return 2 if receipt.status is ReceiptStatus.REJECTED else 0


def _run_snapshot(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    replay_bytes = project.read_relative(
        _text_argument(args, "replay"),
        max_bytes=_MAX_REPLAY_BYTES,
        role="replay",
    )
    result = project.replay_runner().replay_to_tick(
        replay_bytes,
        at_tick=_int_argument(args, "tick"),
        tick_executor=project.tick_executor,
    )
    snapshot = project.snapshot_codec.encode(result.session)
    project.write_relative(_text_argument(args, "out"), snapshot, role="snapshot")
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.snapshot/1",
                "tick": result.session.completed_ticks,
                "state_hash": result.session.state_hash,
            }
        )
    )
    return 0


def _run_replay(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    replay_bytes = project.read_relative(
        _text_argument(args, "replay"),
        max_bytes=_MAX_REPLAY_BYTES,
        role="replay",
    )
    verify_hashes = getattr(args, "verify_hashes", False)
    if type(verify_hashes) is not bool:
        raise _argument_error("verify_hashes")
    result = project.replay_runner().replay(
        replay_bytes,
        tick_executor=project.tick_executor,
        verify_hashes=verify_hashes,
    )
    snapshot_name = _optional_text_argument(args, "snapshot_out")
    if snapshot_name is not None:
        project.write_relative(
            snapshot_name,
            project.snapshot_codec.encode(result.session),
            role="snapshot",
        )
    _write_stdout(
        canonical_dumps(
            {
                "protocol": "ludoweave.cli.replay/1",
                "status": "verified" if verify_hashes else "completed",
                "batches": result.batches_applied,
                "checkpoints_verified": len(result.verified_checkpoints),
                "tick": result.session.completed_ticks,
                "state_hash": result.session.state_hash,
            }
        )
    )
    return 0


def _run_diff(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    before = project.load_snapshot(
        project.read_relative(
            _text_argument(args, "before"),
            max_bytes=_MAX_SNAPSHOT_BYTES,
            role="before_snapshot",
        )
    )
    after = project.load_snapshot(
        project.read_relative(
            _text_argument(args, "after"),
            max_bytes=_MAX_SNAPSHOT_BYTES,
            role="after_snapshot",
        )
    )
    changes = semantic_diff(before.authority_document(), after.authority_document())
    document: dict[str, JsonValue] = {
        "protocol": "ludoweave.cli.diff/1",
        "world_id": before.world_id,
        "pre_hash": before.state_hash,
        "post_hash": after.state_hash,
        "changes": changes.as_dict(),
    }
    _write_stdout(canonical_dumps(document))
    return 0


def _run_agent(args: argparse.Namespace) -> int:
    project = HeadlessProject.load(_path_argument(args, "project"))
    session = _agent_session(project, _optional_text_argument(args, "state"))
    actor = CommandActor(
        _text_argument(args, "actor_kind"),
        _text_argument(args, "actor_id"),
    )
    write = _bool_argument(args, "write")
    request = canonical_loads(
        project.read_relative(
            _text_argument(args, "request"),
            max_bytes=_MAX_AGENT_REQUEST_BYTES,
            role="agent_request",
        )
    )
    if not isinstance(request, dict):
        raise _argument_error("request")
    service = headless_agent_service(
        project,
        session,
        actor=actor,
        write=write,
    )
    try:
        result = service.call(
            _text_argument(args, "tool"),
            cast(dict[str, object], request),
        )
    finally:
        service.close()
    _write_stdout(canonical_dumps(result))
    return 0


def _run_mcp(args: argparse.Namespace) -> int:
    actor = CommandActor(
        _text_argument(args, "actor_kind"),
        _text_argument(args, "actor_id"),
    )
    write = _bool_argument(args, "write")
    project_value: object = getattr(args, "project", None)
    sample = _optional_text_argument(args, "sample")
    renderer = _text_argument(args, "renderer")
    if sample is not None:
        if isinstance(project_value, Path):
            raise _argument_error("project_or_sample")
        device = None
        if renderer == "wgpu":
            from ludoweave.render.backends.wgpu import WgpuRenderDevice

            device = WgpuRenderDevice()
        builder = create_agent_world_builder(
            write=write,
            actor=actor,
            device=device,
        )
        return run_stdio(McpServer(builder.service))
    if not isinstance(project_value, Path):
        raise _argument_error("project_or_sample")
    if renderer != "none":
        raise _argument_error("renderer")
    project = HeadlessProject.load(project_value)
    session = _agent_session(project, _optional_text_argument(args, "state"))
    service = headless_agent_service(project, session, actor=actor, write=write)
    return run_stdio(McpServer(service))


def _run_inspect(args: argparse.Namespace) -> int:
    project_value: object = getattr(args, "project", None)
    project = project_value if isinstance(project_value, Path) else None
    config = InspectorConfig(
        actor=CommandActor(
            _text_argument(args, "actor_kind"),
            _text_argument(args, "actor_id"),
        ),
        project=project,
        sample=_optional_text_argument(args, "sample"),
        state=_optional_text_argument(args, "state"),
        write=_bool_argument(args, "write"),
        bootstrap=_bool_argument(args, "bootstrap"),
        ticks=_int_argument(args, "ticks"),
        query_limit=_int_argument(args, "query_limit"),
    )
    run_inspector(config, output=sys.stdout)
    return 0


def _run_plugin(args: argparse.Namespace) -> int:
    if _text_argument(args, "plugin_command") != "check":
        raise _argument_error("plugin_command")
    determinism_text = _text_argument(args, "minimum_determinism")
    try:
        minimum_determinism = PluginDeterminism(determinism_text)
    except ValueError as error:
        raise _argument_error("minimum_determinism") from error
    paths = _path_arguments(args, "manifests", maximum=_MAX_PLUGIN_MANIFESTS)
    manifests = tuple(PluginManifest.from_json(_read_plugin_manifest(path)) for path in paths)
    context = current_plugin_context(
        minimum_determinism=minimum_determinism,
        allow_native=_bool_argument(args, "allow_native"),
    )
    report = check_plugin_compatibility(manifests, context)
    _write_stdout(report.canonical_bytes())
    return 0 if report.compatible else 1


def _read_plugin_manifest(path: Path) -> bytes:
    try:
        with path.open("rb") as stream:
            document = stream.read(_MAX_PLUGIN_MANIFEST_BYTES + 1)
    except OSError as error:
        raise PluginManifestError(
            "plugin manifest file could not be read",
            code="plugins.manifest_read_failed",
            subsystem="plugins",
            phase="read",
            details={"cause_type": type(error).__name__},
        ) from error
    if len(document) > _MAX_PLUGIN_MANIFEST_BYTES:
        raise PluginManifestError(
            "plugin manifest file exceeds its byte limit",
            code="plugins.manifest_too_large",
            subsystem="plugins",
            phase="read",
            details={"limit": _MAX_PLUGIN_MANIFEST_BYTES},
        )
    return document


def _agent_session(project: HeadlessProject, state_name: str | None):
    if state_name is None:
        return project.new_session()
    return project.load_snapshot(
        project.read_relative(
            state_name,
            max_bytes=_MAX_SNAPSHOT_BYTES,
            role="state",
        )
    )


def _path_argument(args: argparse.Namespace, name: str) -> Path:
    value = getattr(args, name, None)
    if not isinstance(value, Path):
        raise _argument_error(name)
    return value


def _path_arguments(args: argparse.Namespace, name: str, *, maximum: int) -> tuple[Path, ...]:
    value = getattr(args, name, None)
    if not isinstance(value, list):
        raise _argument_error(name)
    items = cast(list[object], value)
    if not items or len(items) > maximum:
        raise _argument_error(name)
    if any(not isinstance(item, Path) for item in items):
        raise _argument_error(name)
    return tuple(cast(Path, item) for item in items)


def _text_argument(args: argparse.Namespace, name: str) -> str:
    value = getattr(args, name, None)
    if type(value) is not str:
        raise _argument_error(name)
    return value


def _optional_text_argument(args: argparse.Namespace, name: str) -> str | None:
    value = getattr(args, name, None)
    if value is not None and type(value) is not str:
        raise _argument_error(name)
    return value


def _int_argument(args: argparse.Namespace, name: str) -> int:
    value = getattr(args, name, None)
    if type(value) is not int:
        raise _argument_error(name)
    return value


def _bool_argument(args: argparse.Namespace, name: str) -> bool:
    value = getattr(args, name, None)
    if type(value) is not bool:
        raise _argument_error(name)
    return value


def _argument_error(field: str) -> LudoWeaveError:
    return LudoWeaveError(
        "CLI argument has an invalid type",
        code="tools.invalid_argument",
        subsystem="tools",
        phase="dispatch",
        details={"field": field},
    )


def _print_json(document: object) -> None:
    print(json.dumps(document, sort_keys=True, separators=(",", ":")))


def _print_error(error: LudoWeaveError) -> None:
    print(
        json.dumps(
            {"protocol": "ludoweave.cli.error/1", "error": error.as_dict()},
            sort_keys=True,
            separators=(",", ":"),
        ),
        file=sys.stderr,
    )


def _write_stdout(document: bytes) -> None:
    sys.stdout.buffer.write(document)
    sys.stdout.buffer.write(b"\n")
