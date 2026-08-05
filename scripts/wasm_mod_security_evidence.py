"""Strict expected document for M16 installed WASM-mod security evidence."""

from typing import cast

_PLUGIN_EXPORTS = [
    "PLUGIN_CHECK_PROTOCOL",
    "PLUGIN_MANIFEST_PROTOCOL",
    "PluginCapability",
    "PluginCompatibilityContext",
    "PluginCompatibilityError",
    "PluginCompatibilityIssue",
    "PluginCompatibilityReport",
    "PluginDeterminism",
    "PluginError",
    "PluginManifest",
    "PluginManifestError",
    "PluginPlatform",
    "PluginRequirement",
    "PythonVersionRange",
    "VersionRange",
    "check_plugin_compatibility",
    "current_plugin_context",
]
_REJECTION = {
    "actual_count": 11,
    "code": "plugins.invalid_manifest",
    "expected_count": 10,
    "phase": "decode",
    "role": "plugin_manifest",
}
_BOUNDARY: dict[str, object] = {
    "distribution_requirements": [
        "glfw==2.10.2; extra == 'graphics'",
        "rendercanvas[glfw]==2.7.2; extra == 'graphics'",
        "wgpu==0.32.0; extra == 'graphics'",
    ],
    "executable_manifest_fields_rejected": {
        name: _REJECTION
        for name in ("artifact", "entry_point", "host_imports", "module", "wasi", "wasm")
    },
    "manifest_capabilities": [
        "agent.capture",
        "agent.telemetry",
        "agent.test",
        "audio.backend",
        "render.backend",
        "render.device",
        "resource.adapter",
        "simulation.tick_executor",
    ],
    "manifest_fields": [
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
    ],
    "manifest_protocol": "ludoweave.plugin-manifest/1",
    "plugin_all_preview": True,
    "plugin_exports": _PLUGIN_EXPORTS,
    "plugin_stability": {name: "preview" for name in _PLUGIN_EXPORTS},
    "public_execution_surface_exported": False,
    "root_exports": ["Engine", "EngineConfig", "LifecycleState", "__version__"],
    "wasm_public_exports": [],
    "wasm_runtime_requirements": [],
}
_GATES: dict[str, object] = {
    "bounded_compile_and_artifact_policy": False,
    "capability_manifest_and_default_deny_host_calls": False,
    "cross_platform_installed_conformance": False,
    "deterministic_execution_profile": False,
    "fuel_and_cancellation_enforcement": False,
    "guest_value_validation_and_copy_boundary": False,
    "malicious_corpus_fuzz_and_differential_testing": False,
    "memory_table_stack_and_output_limits": False,
    "mod_identity_distribution_and_revocation_policy": False,
    "process_isolation_decision": False,
    "runtime_candidate_provenance_and_support_matrix": False,
    "security_advisory_and_update_ownership": False,
    "snapshot_replay_migration_contract": False,
    "trap_atomicity_reentrancy_and_recovery": False,
    "world_mutation_command_receipt_mapping": False,
}


def validate_wasm_mod_security_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject WASM-mod security evidence drift, including JSON type drift."""

    expected: dict[str, object] = {
        "admission_ready": False,
        "current_boundary": _BOUNDARY,
        "current_boundary_confirmed": True,
        "decision": "retain-data-only-plugin-boundary",
        "gates": _GATES,
        "ludoweave_version": version,
        "schema": "ludoweave.evaluation.wasm-mod-security/1",
        "status": "deferred",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("WASM-mod installed security evidence drifted")


def _exact_json(actual: object, expected: object) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        actual_mapping = cast(dict[object, object], actual)
        expected_mapping = cast(dict[object, object], expected)
        return actual_mapping.keys() == expected_mapping.keys() and all(
            _exact_json(actual_mapping[key], value) for key, value in expected_mapping.items()
        )
    if isinstance(expected, list):
        actual_items = cast(list[object], actual)
        expected_items = cast(list[object], expected)
        return len(actual_items) == len(expected_items) and all(
            _exact_json(actual_item, expected_item)
            for actual_item, expected_item in zip(actual_items, expected_items, strict=True)
        )
    return actual == expected
