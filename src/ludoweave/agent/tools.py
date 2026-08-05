"""Versioned agent tool discovery records shared by Python, CLI, and MCP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from ludoweave.world.canonical import JsonValue


@dataclass(frozen=True, slots=True)
class AgentTool:
    """One immutable tool definition with a transport-neutral JSON Schema."""

    name: str
    description: str
    input_schema: dict[str, JsonValue]
    read_only: bool
    idempotent: bool
    destructive: bool

    def as_mcp_dict(self) -> dict[str, JsonValue]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
            "outputSchema": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
            },
            "annotations": {
                "readOnlyHint": self.read_only,
                "idempotentHint": self.idempotent,
                "destructiveHint": self.destructive,
                "openWorldHint": False,
            },
        }


_EMPTY_SCHEMA: dict[str, JsonValue] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}

_TRANSACTION_SCHEMA: dict[str, JsonValue] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {"transaction": {"type": "object"}},
    "required": ["transaction"],
    "additionalProperties": False,
}


def _schema(
    properties: dict[str, object],
    *,
    required: tuple[str, ...] = (),
) -> dict[str, JsonValue]:
    return cast(
        dict[str, JsonValue],
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": properties,
            "required": list(required),
            "additionalProperties": False,
        },
    )


AGENT_TOOLS: tuple[AgentTool, ...] = (
    AgentTool(
        "project_describe",
        "Describe project identity, schemas, limits, and enabled capabilities.",
        _EMPTY_SCHEMA,
        True,
        True,
        False,
    ),
    AgentTool(
        "world_describe",
        "Describe current authoritative tick, hash, entity, component, and resource counts.",
        _EMPTY_SCHEMA,
        True,
        True,
        False,
    ),
    AgentTool(
        "world_query",
        "Query entities by included and excluded component UUIDs in stable order.",
        _schema(
            {
                "include": {"type": "array", "items": {"type": "string"}},
                "exclude": {"type": "array", "items": {"type": "string"}},
                "limit": {"type": "integer", "minimum": 1},
            }
        ),
        True,
        True,
        False,
    ),
    AgentTool(
        "entity_get",
        "Read one live entity and all canonical component values by index:generation ID.",
        _schema({"entity": {"type": "string"}}, required=("entity",)),
        True,
        True,
        False,
    ),
    AgentTool(
        "transaction_validate",
        "Dry-run one canonical transaction and return its proposed receipt and semantic diff.",
        _TRANSACTION_SCHEMA,
        True,
        True,
        False,
    ),
    AgentTool(
        "transaction_apply",
        "Atomically apply one canonical transaction through the world transaction service.",
        _TRANSACTION_SCHEMA,
        False,
        False,
        True,
    ),
    AgentTool(
        "world_tick",
        "Advance bounded fixed ticks as individually receipted, replayable safe-point transactions.",
        _schema(
            {
                "request_id": {"type": "string"},
                "count": {"type": "integer", "minimum": 1},
                "expected_world_hash": {"type": ["string", "null"]},
            },
            required=("request_id", "count"),
        ),
        False,
        False,
        True,
    ),
    AgentTool(
        "world_snapshot",
        "Capture the complete canonical authority snapshot as bounded base64 data.",
        _EMPTY_SCHEMA,
        True,
        True,
        False,
    ),
    AgentTool(
        "world_diff",
        "Compare a validated base64 snapshot with another snapshot or the current authority.",
        _schema(
            {
                "before_snapshot": {"type": "string"},
                "after_snapshot": {"type": "string"},
            },
            required=("before_snapshot",),
        ),
        True,
        True,
        False,
    ),
    AgentTool(
        "render_capture",
        "Capture bounded provider-neutral RGBA8 presentation pixels and metadata.",
        _schema(
            {
                "width": {"type": "integer", "minimum": 1},
                "height": {"type": "integer", "minimum": 1},
                "include_pixels": {"type": "boolean"},
            },
            required=("width", "height"),
        ),
        True,
        True,
        False,
    ),
    AgentTool(
        "telemetry_get",
        "Read bounded non-authoritative service and application telemetry.",
        _EMPTY_SCHEMA,
        True,
        True,
        False,
    ),
    AgentTool(
        "test_run",
        "Run only explicitly registered in-process acceptance checks by stable name.",
        _schema({"tests": {"type": "array", "items": {"type": "string"}}}),
        True,
        True,
        False,
    ),
)

AGENT_TOOL_NAMES = tuple(tool.name for tool in AGENT_TOOLS)


def tool_for_name(name: str) -> AgentTool | None:
    for tool in AGENT_TOOLS:
        if tool.name == name:
            return tool
    return None
