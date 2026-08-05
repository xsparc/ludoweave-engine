"""Strict expected document for M15 installed-surface artifact smoke."""

from typing import cast

_AGENT_TOOLS = [
    "project_describe",
    "world_describe",
    "world_query",
    "entity_get",
    "transaction_validate",
    "transaction_apply",
    "world_tick",
    "world_snapshot",
    "world_diff",
    "render_capture",
    "telemetry_get",
    "test_run",
]
_AGENT_EXPORTS = [
    "AGENT_ERROR_PROTOCOL",
    "AGENT_SERVICE_PROTOCOL",
    "AGENT_TOOLS",
    "AGENT_TOOL_NAMES",
    "AgentCapabilities",
    "AgentCapabilityError",
    "AgentCapture",
    "AgentCaptureProvider",
    "AgentCommandService",
    "AgentConcurrencyError",
    "AgentError",
    "AgentLimitError",
    "AgentLimits",
    "AgentProject",
    "AgentProviderError",
    "AgentRequestError",
    "AgentTelemetryProvider",
    "AgentTestProvider",
    "AgentTestResult",
    "AgentTool",
]
_FOUNDATIONS: dict[str, object] = {
    "agent_all_experimental": True,
    "agent_exports": _AGENT_EXPORTS,
    "agent_service_protocol": "ludoweave.agent.service/1",
    "agent_stability": {name: "experimental" for name in _AGENT_EXPORTS},
    "agent_tools": _AGENT_TOOLS,
    "builtin_operations": [
        "component.add",
        "component.patch",
        "component.remove",
        "entity.destroy",
        "entity.spawn",
        "resource.patch",
        "world.tick",
    ],
    "command_protocol": "ludoweave.command/1",
    "inspector_config_fields": [
        "actor",
        "project",
        "sample",
        "state",
        "write",
        "bootstrap",
        "ticks",
        "query_limit",
    ],
    "inspector_event_protocol": "ludoweave.inspector.event/1",
    "inspector_public_exported": False,
    "mcp_protocol_version": "2025-11-25",
    "mutating_tools": ["transaction_apply", "world_tick"],
    "read_only_default": True,
    "read_only_tools": [
        "project_describe",
        "world_describe",
        "world_query",
        "entity_get",
        "transaction_validate",
        "world_snapshot",
        "world_diff",
        "render_capture",
        "telemetry_get",
        "test_run",
    ],
    "receipt_protocol": "ludoweave.receipt/1",
    "root_exports": ["Engine", "EngineConfig", "LifecycleState", "__version__"],
    "semantic_mutation": {
        "authority_hash_matched": True,
        "command_count": 6,
        "completed_ticks_unchanged": True,
        "entity_count_after": 6,
        "outcomes_committed": True,
        "post_hash_changed": True,
        "pre_hash_matched": True,
        "receipt_protocol": "ludoweave.receipt/1",
        "status": "committed",
    },
    "tools_exports": [],
    "transaction_protocol": "ludoweave.transaction/1",
}
_GATES: dict[str, object] = {
    "accessibility_usability_evidence": False,
    "asset_authoring_workflow": False,
    "cross_platform_desktop_packaging": False,
    "document_scene_roundtrip": False,
    "performance_support_budget": False,
    "property_metadata_contract": False,
    "public_inspector_compatibility": False,
    "recovery_dirty_state_contract": False,
    "selection_hierarchy_contract": False,
    "stable_command_editor_profile": False,
    "undo_redo_conflict_contract": False,
    "viewport_picking_gizmo_contract": False,
}


def validate_visual_editor_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject any visual-editor admission evidence drift with exact JSON types."""

    expected: dict[str, object] = {
        "admission_ready": False,
        "decision": "retain-headless-inspector",
        "foundation_confirmed": True,
        "foundations": _FOUNDATIONS,
        "gates": _GATES,
        "ludoweave_version": version,
        "schema": "ludoweave.evaluation.visual-editor/1",
        "status": "deferred",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("visual-editor installed-surface evidence drifted")


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
