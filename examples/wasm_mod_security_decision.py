"""Report the installed plugin boundary and WASM-mod security decision."""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Sequence
from dataclasses import fields
from importlib import metadata
from types import ModuleType
from typing import cast

import ludoweave as ludoweave_package
import ludoweave.plugins as plugins_package
from ludoweave import __version__
from ludoweave.plugins import (
    PLUGIN_MANIFEST_PROTOCOL,
    PluginCapability,
    PluginManifest,
    PluginManifestError,
)
from ludoweave.plugins import __stability__ as plugin_stability

_SCHEMA = "ludoweave.evaluation.wasm-mod-security/1"
_WASM_RUNTIME_PROJECTS = frozenset(
    {
        "pywasm",
        "wasi",
        "wasm3",
        "wasmedge",
        "wasmedge-sdk",
        "wasmer",
        "wasmtime",
    }
)
_EXPECTED_DISTRIBUTION_REQUIREMENTS = (
    "glfw==2.10.2; extra == 'graphics'",
    "rendercanvas[glfw]==2.7.2; extra == 'graphics'",
    "wgpu==0.32.0; extra == 'graphics'",
)
_EXECUTABLE_FIELDS = ("artifact", "entry_point", "host_imports", "module", "wasi", "wasm")
_ADMISSION_GATES = (
    "bounded_compile_and_artifact_policy",
    "capability_manifest_and_default_deny_host_calls",
    "cross_platform_installed_conformance",
    "deterministic_execution_profile",
    "fuel_and_cancellation_enforcement",
    "guest_value_validation_and_copy_boundary",
    "malicious_corpus_fuzz_and_differential_testing",
    "memory_table_stack_and_output_limits",
    "mod_identity_distribution_and_revocation_policy",
    "process_isolation_decision",
    "runtime_candidate_provenance_and_support_matrix",
    "security_advisory_and_update_ownership",
    "snapshot_replay_migration_contract",
    "trap_atomicity_reentrancy_and_recovery",
    "world_mutation_command_receipt_mapping",
)
_REQUIREMENT_NAME = re.compile(r"\A\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("wasm_mod_security_decision accepts no arguments")
    print(json.dumps(evaluate(), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate() -> dict[str, object]:
    """Return exact installed facts and the resulting security admission decision."""

    root_exports = _declared_exports(ludoweave_package)
    plugin_exports = _declared_exports(plugins_package)
    stability = {name: plugin_stability[name] for name in plugin_exports}
    all_preview = set(stability) == set(plugin_exports) and set(stability.values()) == {"preview"}
    manifest = _evidence_manifest()
    manifest_fields = tuple(manifest.as_dict())
    executable_field_rejections = {
        name: _rejection_evidence(manifest, name) for name in _EXECUTABLE_FIELDS
    }
    distribution_requirements = _installed_distribution_requirements()
    runtime_requirements = _wasm_runtime_requirements(distribution_requirements)
    wasm_public_exports = tuple(
        sorted(
            name
            for name in (*root_exports, *plugin_exports)
            if any(token in name.casefold() for token in ("guest", "modloader", "wasi", "wasm"))
        )
    )
    boundary = {
        "distribution_requirements": distribution_requirements,
        "executable_manifest_fields_rejected": executable_field_rejections,
        "manifest_capabilities": tuple(item.value for item in PluginCapability),
        "manifest_fields": manifest_fields,
        "manifest_protocol": PLUGIN_MANIFEST_PROTOCOL,
        "plugin_all_preview": all_preview,
        "plugin_exports": plugin_exports,
        "plugin_stability": stability,
        "public_execution_surface_exported": bool(wasm_public_exports),
        "root_exports": root_exports,
        "wasm_public_exports": wasm_public_exports,
        "wasm_runtime_requirements": runtime_requirements,
    }
    current_boundary_confirmed = (
        all_preview
        and manifest_fields
        == (
            "protocol",
            "plugin_id",
            "plugin_version",
            "engine",
            "python",
            "platforms",
            "capabilities",
            "determinism",
            "native",
            "requires",
        )
        and all(
            evidence
            == {
                "actual_count": 11,
                "code": "plugins.invalid_manifest",
                "expected_count": 10,
                "phase": "decode",
                "role": "plugin_manifest",
            }
            for evidence in executable_field_rejections.values()
        )
        and not runtime_requirements
        and distribution_requirements == _EXPECTED_DISTRIBUTION_REQUIREMENTS
        and not wasm_public_exports
        and boundary["public_execution_surface_exported"] is False
    )
    if not current_boundary_confirmed:
        raise AssertionError("M16 evidence no longer confirms the inert plugin boundary")

    gates = {name: False for name in _ADMISSION_GATES}
    admission_ready = all(gates.values())
    if admission_ready:
        raise AssertionError("M16 evidence unexpectedly satisfies every WASM-mod gate")
    return {
        "admission_ready": admission_ready,
        "current_boundary": boundary,
        "current_boundary_confirmed": current_boundary_confirmed,
        "decision": "retain-data-only-plugin-boundary",
        "gates": gates,
        "ludoweave_version": __version__,
        "schema": _SCHEMA,
        "status": "deferred",
    }


def _evidence_manifest() -> PluginManifest:
    return PluginManifest.from_mapping(
        {
            "protocol": PLUGIN_MANIFEST_PROTOCOL,
            "plugin_id": "org.ludoweave.security-evidence",
            "plugin_version": "1.0.0",
            "engine": {"minimum": "0.1.0a1", "maximum_exclusive": "0.2.0"},
            "python": {"minimum": "3.12", "maximum_exclusive": "3.15"},
            "platforms": ["linux", "macos", "windows"],
            "capabilities": ["resource.adapter"],
            "determinism": "d1",
            "native": False,
            "requires": [],
        }
    )


def _rejection_evidence(manifest: PluginManifest, field: str) -> dict[str, object]:
    document = cast(dict[str, object], manifest.as_dict())
    document[field] = "not-executed"
    try:
        PluginManifest.from_mapping(document)
    except PluginManifestError as error:
        details = dict(error.details)
        return {
            "actual_count": details.get("actual_count"),
            "code": error.code,
            "expected_count": details.get("expected_count"),
            "phase": error.phase,
            "role": details.get("role"),
        }
    raise AssertionError(f"plugin manifest unexpectedly accepted executable field {field!r}")


def _installed_distribution_requirements() -> tuple[str, ...]:
    value = cast(object, metadata.requires("ludoweave"))
    if value is None:
        return ()
    if not isinstance(value, list):
        raise AssertionError("installed distribution requirements are malformed")
    requirements: list[str] = []
    for requirement in cast(list[object], value):
        if (
            not isinstance(requirement, str)
            or not requirement
            or len(requirement) > 512
            or _REQUIREMENT_NAME.match(requirement) is None
        ):
            raise AssertionError("installed distribution requirement is malformed")
        requirements.append(requirement)
    if len(requirements) != len(set(requirements)):
        raise AssertionError("installed distribution requirements contain duplicates")
    return tuple(sorted(requirements))


def _wasm_runtime_requirements(requirements: tuple[str, ...]) -> tuple[str, ...]:
    names: set[str] = set()
    for requirement in requirements:
        match = _REQUIREMENT_NAME.match(requirement)
        if match is None:  # pragma: no cover - checked by _installed_distribution_requirements
            raise AssertionError("normalized distribution requirement is malformed")
        name = re.sub(r"[-_.]+", "-", match.group(1)).casefold()
        if name in _WASM_RUNTIME_PROJECTS:
            names.add(name)
    return tuple(sorted(names))


def _declared_exports(module: ModuleType) -> tuple[str, ...]:
    value: object = getattr(module, "__all__", None)
    if not isinstance(value, list):
        raise AssertionError("installed public exports are malformed")
    exports: list[str] = []
    for name in cast(list[object], value):
        if not isinstance(name, str):
            raise AssertionError("installed public exports are malformed")
        exports.append(name)
    return tuple(exports)


def _manifest_dataclass_fields() -> tuple[str, ...]:
    """Keep strict type checking aware that the manifest remains a value object."""

    return tuple(field.name for field in fields(PluginManifest))


if _manifest_dataclass_fields() != (
    "plugin_id",
    "plugin_version",
    "engine",
    "python",
    "platforms",
    "capabilities",
    "determinism",
    "native",
    "requires",
    "protocol",
):
    raise AssertionError("installed plugin manifest value fields drifted")


if __name__ == "__main__":
    raise SystemExit(main())
