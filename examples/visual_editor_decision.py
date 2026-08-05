"""Report the installed protocol foundation and visual-editor admission decision."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from dataclasses import fields
from types import ModuleType
from typing import cast

import ludoweave as ludoweave_package
import ludoweave.tools as tools_package
from ludoweave import __version__
from ludoweave.agent import (
    AGENT_SERVICE_PROTOCOL,
    AGENT_TOOL_NAMES,
    AGENT_TOOLS,
)
from ludoweave.agent import (
    __all__ as agent_exports,
)
from ludoweave.agent import (
    __stability__ as agent_stability,
)
from ludoweave.samples import builder_create_transaction, create_agent_world_builder
from ludoweave.tools.inspector import INSPECTOR_EVENT_PROTOCOL, InspectorConfig
from ludoweave.tools.mcp import MCP_PROTOCOL_VERSION
from ludoweave.world import (
    BUILTIN_OPERATION_SPECS,
    COMMAND_PROTOCOL,
    RECEIPT_PROTOCOL,
    TRANSACTION_PROTOCOL,
    ReceiptStatus,
)

_SCHEMA = "ludoweave.evaluation.visual-editor/1"
_EDITOR_GATES = (
    "accessibility_usability_evidence",
    "asset_authoring_workflow",
    "cross_platform_desktop_packaging",
    "document_scene_roundtrip",
    "performance_support_budget",
    "property_metadata_contract",
    "public_inspector_compatibility",
    "recovery_dirty_state_contract",
    "selection_hierarchy_contract",
    "stable_command_editor_profile",
    "undo_redo_conflict_contract",
    "viewport_picking_gizmo_contract",
)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("visual_editor_decision accepts no arguments")
    print(json.dumps(evaluate(), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate() -> dict[str, object]:
    """Return exact installed facts and the resulting product admission decision."""

    operations = tuple(spec.operation for spec in BUILTIN_OPERATION_SPECS)
    tools = tuple(tool.name for tool in AGENT_TOOLS)
    read_only_tools = tuple(tool.name for tool in AGENT_TOOLS if tool.read_only)
    mutating_tools = tuple(tool.name for tool in AGENT_TOOLS if not tool.read_only)
    inspector_field_specs = fields(InspectorConfig)
    inspector_fields = tuple(field.name for field in inspector_field_specs)
    write_default = next(field.default for field in inspector_field_specs if field.name == "write")
    root_exports = _declared_exports(ludoweave_package)
    tools_exports = _declared_exports(tools_package)
    inspector_exports = tuple(
        name for name in (*root_exports, *tools_exports) if "inspect" in name.casefold()
    )
    agent_export_names = tuple(agent_exports)
    agent_stability_map = {name: agent_stability[name] for name in agent_export_names}
    agent_all_experimental = set(agent_stability_map) == set(agent_export_names) and set(
        agent_stability_map.values()
    ) == {"experimental"}
    semantic_mutation = _semantic_mutation_evidence()
    foundations = {
        "agent_all_experimental": agent_all_experimental,
        "agent_exports": agent_export_names,
        "agent_service_protocol": AGENT_SERVICE_PROTOCOL,
        "agent_stability": agent_stability_map,
        "agent_tools": tools,
        "builtin_operations": operations,
        "command_protocol": COMMAND_PROTOCOL,
        "inspector_config_fields": inspector_fields,
        "inspector_event_protocol": INSPECTOR_EVENT_PROTOCOL,
        "inspector_public_exported": bool(inspector_exports),
        "mcp_protocol_version": MCP_PROTOCOL_VERSION,
        "mutating_tools": mutating_tools,
        "read_only_default": write_default is False,
        "read_only_tools": read_only_tools,
        "receipt_protocol": RECEIPT_PROTOCOL,
        "root_exports": root_exports,
        "semantic_mutation": semantic_mutation,
        "tools_exports": tools_exports,
        "transaction_protocol": TRANSACTION_PROTOCOL,
    }
    foundation_confirmed = (
        tools == AGENT_TOOL_NAMES
        and "transaction_apply" in mutating_tools
        and "world_tick" in mutating_tools
        and {"telemetry_get", "world_describe", "world_diff", "world_query"} <= set(read_only_tools)
        and foundations["read_only_default"] is True
        and foundations["inspector_public_exported"] is False
        and foundations["agent_all_experimental"] is True
        and semantic_mutation
        == {
            "authority_hash_matched": True,
            "command_count": 6,
            "completed_ticks_unchanged": True,
            "entity_count_after": 6,
            "outcomes_committed": True,
            "post_hash_changed": True,
            "pre_hash_matched": True,
            "receipt_protocol": RECEIPT_PROTOCOL,
            "status": ReceiptStatus.COMMITTED.value,
        }
    )
    if not foundation_confirmed:
        raise AssertionError("M15 evidence no longer confirms the required protocol foundation")

    gates = {name: False for name in _EDITOR_GATES}
    admission_ready = all(gates.values())
    if admission_ready:
        raise AssertionError("M15 evidence unexpectedly satisfies every visual-editor gate")
    return {
        "admission_ready": admission_ready,
        "decision": "retain-headless-inspector",
        "foundation_confirmed": foundation_confirmed,
        "foundations": foundations,
        "gates": gates,
        "ludoweave_version": __version__,
        "schema": _SCHEMA,
        "status": "deferred",
    }


def _declared_exports(module: ModuleType) -> tuple[str, ...]:
    value: object = getattr(module, "__all__", None)
    if value is None:
        return ()
    if not isinstance(value, list):
        raise AssertionError("installed public exports are malformed")
    exports: list[str] = []
    for name in cast(list[object], value):
        if not isinstance(name, str):
            raise AssertionError("installed public exports are malformed")
        exports.append(name)
    return tuple(exports)


def _semantic_mutation_evidence() -> dict[str, object]:
    builder = create_agent_world_builder(write=True)
    try:
        service = builder.service
        initial_hash = service.session.state_hash
        transaction = builder_create_transaction(
            service.actor,
            expected_world_hash=initial_hash,
            transaction_id="visual-editor-admission",
        )
        result = service.call(
            "transaction_apply",
            {"transaction": transaction.as_dict()},
        )
        receipt_value: object = result.get("receipt")
        if not isinstance(receipt_value, dict):
            raise AssertionError("installed semantic mutation returned no receipt")
        receipt = cast(dict[str, object], receipt_value)
        outcomes_value = receipt.get("command_outcomes")
        if not isinstance(outcomes_value, list):
            raise AssertionError("installed semantic mutation returned no command outcomes")
        outcomes = cast(list[object], outcomes_value)
        outcome_statuses = tuple(_outcome_status(item) for item in outcomes)
        world = service.call("world_describe")
        post_hash = receipt.get("post_hash")
        return {
            "authority_hash_matched": post_hash == service.session.state_hash,
            "command_count": len(outcome_statuses),
            "completed_ticks_unchanged": (
                receipt.get("completed_ticks_before") == receipt.get("completed_ticks_after") == 0
            ),
            "entity_count_after": world.get("entity_count"),
            "outcomes_committed": all(
                status == ReceiptStatus.COMMITTED.value for status in outcome_statuses
            ),
            "post_hash_changed": isinstance(post_hash, str) and post_hash != initial_hash,
            "pre_hash_matched": receipt.get("pre_hash") == initial_hash,
            "receipt_protocol": receipt.get("protocol"),
            "status": receipt.get("status"),
        }
    finally:
        builder.close()


def _outcome_status(value: object) -> str:
    if not isinstance(value, dict):
        raise AssertionError("installed semantic mutation returned a malformed outcome")
    status = cast(dict[object, object], value).get("status")
    if not isinstance(status, str):
        raise AssertionError("installed semantic mutation returned an untyped outcome")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
