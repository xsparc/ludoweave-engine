"""Exercise the installed v1 built-in operation argument contract."""

import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from ludoweave import __version__
from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    World,
    WorldStore,
    component,
)
from ludoweave.world import (
    COMMAND_PROTOCOL,
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    RandomStreams,
    ReceiptStatus,
    TransactionReceipt,
    TransactionService,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue

_SCHEMA = "ludoweave.evaluation.operation-argument-compatibility/1"
_POSITION_ID = UUID("38b243d7-e301-4fa6-a06b-d03a6f50905b")
_SCORE_ID = UUID("f5e35494-6a0a-42f5-90df-04f46a6e3c99")
_POLICY = {
    "same_identity_change": "forbidden",
    "breaking_change": "new-operation-version",
    "unknown_fields": "reject",
    "new_operation_identity": "additive",
    "deprecation": "requires-supported-feature-release-after-preview",
}
_CONTRACTS: tuple[dict[str, object], ...] = (
    {
        "operation": "component.add",
        "version": 1,
        "required": ["component", "entity"],
        "optional": [],
        "rules": ["component-payload-v1", "entity-reference-v1"],
    },
    {
        "operation": "component.patch",
        "version": 1,
        "required": ["changes", "entity", "type_id", "version"],
        "optional": [],
        "rules": [
            "entity-reference-v1",
            "canonical-registered-component-type-id",
            "current-schema-version",
            "non-empty-exact-registered-field-map",
        ],
    },
    {
        "operation": "component.remove",
        "version": 1,
        "required": ["entity", "type_id"],
        "optional": [],
        "rules": ["entity-reference-v1", "canonical-registered-component-type-id"],
    },
    {
        "operation": "entity.destroy",
        "version": 1,
        "required": ["entity"],
        "optional": [],
        "rules": ["entity-reference-v1"],
    },
    {
        "operation": "entity.spawn",
        "version": 1,
        "required": ["components"],
        "optional": ["alias"],
        "rules": [
            "bounded-stable-optional-alias",
            "component-payload-v1-array",
            "unique-component-type-ids",
        ],
    },
    {
        "operation": "resource.patch",
        "version": 1,
        "required": ["type_id", "value", "version"],
        "optional": [],
        "rules": [
            "canonical-registered-resource-type-id",
            "authoritative-state-resource-only",
            "current-schema-version",
            "registered-codec-value",
        ],
    },
    {
        "operation": "world.tick",
        "version": 1,
        "required": ["count"],
        "optional": [],
        "rules": ["exact-positive-integer-one", "transaction-safe-point"],
    },
)


@component(type_id=_POSITION_ID)
@dataclass(slots=True)
class _Position:
    x: int
    y: int = 0


_SCORE = ResourceSpec("compatibility.score", int, int)


def _decode_score(value: JsonValue) -> int:
    if type(value) is not int:
        raise ValueError("score must be an integer")
    return value


_SCORE_SCHEMA = AuthorityResourceSchema(
    type_id=_SCORE_ID,
    version=1,
    spec=_SCORE,
    codec_id="compatibility.score/int-v1",
    encoder=int,
    decoder=_decode_score,
)


class _NoOpTickExecutor:
    __slots__ = ()

    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None:
        del world, resources, random_streams, tick


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("operation_argument_compatibility accepts no arguments")
    print(json.dumps(evaluate(), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate() -> dict[str, object]:
    """Return deterministic installed evidence for every built-in v1 argument shape."""

    results: list[dict[str, object]] = []
    for contract in _CONTRACTS:
        operation = cast(str, contract["operation"])
        required = cast(list[str], contract["required"])
        valid_session, valid_arguments = _case(operation)
        valid = _apply(valid_session, operation, valid_arguments, "valid")

        missing_session, missing_arguments = _case(operation)
        del missing_arguments[required[0]]
        missing = _apply(missing_session, operation, missing_arguments, "missing")

        unexpected_session, unexpected_arguments = _case(operation)
        unexpected_arguments["unexpected"] = True
        unexpected = _apply(unexpected_session, operation, unexpected_arguments, "unexpected")
        results.append(
            {
                **contract,
                "missing_required_code": _rejection_code(missing),
                "missing_required_status": missing.status.value,
                "unexpected_field_code": _rejection_code(unexpected),
                "unexpected_field_status": unexpected.status.value,
                "valid_status": valid.status.value,
            }
        )

    default_session, default_arguments = _case("entity.spawn")
    component_items = cast(list[object], default_arguments["components"])
    first_component = cast(dict[str, object], component_items[0])
    defaulted_values = cast(dict[str, object], first_component["values"])
    del defaulted_values["y"]
    default_omission = _apply(
        default_session,
        "entity.spawn",
        default_arguments,
        "default-omission",
    )

    gate_satisfied = (
        all(
            result["valid_status"] == ReceiptStatus.COMMITTED.value
            and result["missing_required_status"] == ReceiptStatus.REJECTED.value
            and result["unexpected_field_status"] == ReceiptStatus.REJECTED.value
            for result in results
        )
        and default_omission.status is ReceiptStatus.REJECTED
    )
    if not gate_satisfied:
        raise AssertionError("installed operation argument compatibility evidence failed")
    return {
        "command_protocol": COMMAND_PROTOCOL,
        "contracts": results,
        "cross_version_proven": False,
        "defaulted_component_field_omission_code": _rejection_code(default_omission),
        "defaulted_component_field_omission_status": default_omission.status.value,
        "evidence_level": "single-version-policy-baseline",
        "gate_satisfied": True,
        "ludoweave_version": __version__,
        "policy": _POLICY,
        "schema": _SCHEMA,
        "status": "pass",
    }


def _case(operation: str) -> tuple[WorldSession, dict[str, object]]:
    world = World(ComponentRegistry((_Position,)))
    entity = None
    if operation in {"component.patch", "component.remove", "entity.destroy"}:
        entity = world.spawn(_Position(1, 2))
    elif operation == "component.add":
        entity = world.spawn()
    resources = ResourceStore(ResourceRegistry((_SCORE,)), ((_SCORE, 0),))
    session = WorldSession(
        f"operation-arguments-{operation}",
        world,
        resources,
        authority_resources=AuthorityResourceRegistry((_SCORE_SCHEMA,)),
        tick_executor=_NoOpTickExecutor(),
    )
    reference = None if entity is None else {"generation": entity.generation, "index": entity.index}
    payload = {
        "type_id": str(_POSITION_ID),
        "values": {"x": 3, "y": 4},
        "version": 1,
    }
    arguments: dict[str, dict[str, object]] = {
        "component.add": {"component": payload, "entity": reference},
        "component.patch": {
            "changes": {"x": 9},
            "entity": reference,
            "type_id": str(_POSITION_ID),
            "version": 1,
        },
        "component.remove": {"entity": reference, "type_id": str(_POSITION_ID)},
        "entity.destroy": {"entity": reference},
        "entity.spawn": {"alias": "created", "components": [payload]},
        "resource.patch": {"type_id": str(_SCORE_ID), "value": 7, "version": 1},
        "world.tick": {"count": 1},
    }
    return session, dict(arguments[operation])


def _apply(
    session: WorldSession,
    operation: str,
    arguments: dict[str, object],
    case: str,
) -> TransactionReceipt:
    transaction_id = f"operation-arguments.{operation}.{case}"
    command = CommandEnvelope(
        command_id=f"{transaction_id}.command",
        transaction_id=transaction_id,
        actor=CommandActor("maintainer", "compatibility-evidence"),
        operation=operation,
        arguments=arguments,
        expected_world_hash=session.state_hash,
    )
    return TransactionService(session).apply(CommandTransaction((command,), session.world_id))


def _rejection_code(receipt: TransactionReceipt) -> str:
    if receipt.status is not ReceiptStatus.REJECTED or len(receipt.diagnostics) != 1:
        raise AssertionError("invalid operation arguments did not produce one rejection")
    return receipt.diagnostics[0].code


if __name__ == "__main__":
    raise SystemExit(main())
