"""Canonical transaction receipts and sanitized diagnostics."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import cast
from uuid import UUID

from ludoweave.core.errors import LudoWeaveError
from ludoweave.world.canonical import (
    JsonLimits,
    JsonValue,
    canonical_dumps,
    canonical_loads,
    validate_json_value,
)
from ludoweave.world.command_schema import CommandActor, CommandTransaction
from ludoweave.world.diff import (
    AllocatorChange,
    AllocatorSlotChange,
    ComponentChange,
    EpochChange,
    ResourceChange,
    SemanticDiff,
    TableEpochChange,
)
from ludoweave.world.errors import IncompatibleReceiptError, ReceiptDecodeError

RECEIPT_PROTOCOL = "ludoweave.receipt/1"
_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_OPERATION_ID = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\Z")
_ERROR_CODE = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\Z")
_FIELD_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,127}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_ENTITY = re.compile(r"(0|[1-9][0-9]*):(0|[1-9][0-9]*)\Z")
_MAX_SIGNED_INT = 2**63 - 1


class ReceiptStatus(StrEnum):
    COMMITTED = "committed"
    DRY_RUN = "dry_run"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class ReceiptLimits:
    """Whole-document and semantic bounds for untrusted receipt readers."""

    max_bytes: int = 1_048_576
    max_depth: int = 32
    max_nodes: int = 100_000
    max_collection_items: int = 10_000
    max_string_bytes: int = 262_144
    max_outcomes: int = 1_024
    max_diagnostics: int = 64
    max_diagnostic_details: int = 64
    max_aliases: int = 1_024
    max_diff_records: int = 100_000

    def __post_init__(self) -> None:
        for field in (
            "max_aliases",
            "max_bytes",
            "max_collection_items",
            "max_depth",
            "max_diagnostic_details",
            "max_diagnostics",
            "max_diff_records",
            "max_nodes",
            "max_outcomes",
            "max_string_bytes",
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise ReceiptDecodeError(
                    "receipt limits must be positive integers",
                    code="world.receipt.invalid_limits",
                    subsystem="world",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )

    def json_limits(self) -> JsonLimits:
        """Return the canonical JSON limits enforced before schema decoding."""

        return JsonLimits(
            max_bytes=self.max_bytes,
            max_depth=self.max_depth,
            max_nodes=self.max_nodes,
            max_collection_items=self.max_collection_items,
            max_string_bytes=self.max_string_bytes,
        )


@dataclass(frozen=True, slots=True)
class CommandOutcome:
    command_id: str
    operation: str
    status: ReceiptStatus

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "command_id": self.command_id,
            "operation": self.operation,
            "status": self.status.value,
        }


@dataclass(frozen=True, slots=True)
class ReceiptDiagnostic:
    code: str
    phase: str | None
    message: str
    details: tuple[tuple[str, str | int | float | bool | None], ...]

    @classmethod
    def from_error(cls, error: LudoWeaveError) -> ReceiptDiagnostic:
        return cls(error.code, error.phase, error.message, error.details)

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "code": self.code,
            "phase": self.phase,
            "message": self.message,
            "details": {key: value for key, value in self.details},
        }


@dataclass(frozen=True, slots=True)
class TransactionReceipt:
    """Versioned machine result for one accepted transaction envelope."""

    world_id: str
    transaction_id: str
    actor: CommandActor
    status: ReceiptStatus
    pre_hash: str
    post_hash: str
    proposed_post_hash: str | None
    completed_ticks_before: int
    completed_ticks_after: int
    command_outcomes: tuple[CommandOutcome, ...]
    changes: SemanticDiff | None
    diagnostics: tuple[ReceiptDiagnostic, ...]
    aliases: tuple[tuple[str, str], ...] = ()
    protocol: str = RECEIPT_PROTOCOL

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        limits: ReceiptLimits | None = None,
    ) -> TransactionReceipt:
        """Validate and detach one decoded receipt object."""

        checked_limits = limits or ReceiptLimits()
        try:
            checked = validate_json_value(value, limits=checked_limits.json_limits())
            canonical_dumps(checked, limits=checked_limits.json_limits())
            return _decode_receipt(checked, limits=checked_limits)
        except ReceiptDecodeError:
            raise
        except LudoWeaveError as error:
            raise _nested_receipt_error(error) from error

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: ReceiptLimits | None = None,
    ) -> TransactionReceipt:
        """Decode one bounded canonical JSON receipt document."""

        checked_limits = limits or ReceiptLimits()
        try:
            decoded = canonical_loads(document, limits=checked_limits.json_limits())
            return _decode_receipt(decoded, limits=checked_limits)
        except ReceiptDecodeError:
            raise
        except LudoWeaveError as error:
            raise _nested_receipt_error(error) from error

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "protocol": self.protocol,
            "world_id": self.world_id,
            "transaction_id": self.transaction_id,
            "actor": cast(dict[str, JsonValue], self.actor.as_dict()),
            "status": self.status.value,
            "pre_hash": self.pre_hash,
            "post_hash": self.post_hash,
            "proposed_post_hash": self.proposed_post_hash,
            "completed_ticks_before": self.completed_ticks_before,
            "completed_ticks_after": self.completed_ticks_after,
            "command_outcomes": [item.as_dict() for item in self.command_outcomes],
            "changes": None if self.changes is None else self.changes.as_dict(),
            "diagnostics": [item.as_dict() for item in self.diagnostics],
            "aliases": [{"alias": alias, "entity": entity} for alias, entity in self.aliases],
        }

    def canonical_bytes(self, *, limits: ReceiptLimits | None = None) -> bytes:
        checked_limits = limits or ReceiptLimits()
        return canonical_dumps(self.as_dict(), limits=checked_limits.json_limits())


def _decode_receipt(value: object, *, limits: ReceiptLimits) -> TransactionReceipt:
    document = _object(value, role="receipt")
    _exact_fields(
        document,
        required={
            "protocol",
            "world_id",
            "transaction_id",
            "actor",
            "status",
            "pre_hash",
            "post_hash",
            "proposed_post_hash",
            "completed_ticks_before",
            "completed_ticks_after",
            "command_outcomes",
            "changes",
            "diagnostics",
            "aliases",
        },
        role="receipt",
    )
    protocol = _text(document["protocol"], field="protocol")
    if protocol != RECEIPT_PROTOCOL:
        raise IncompatibleReceiptError(
            "receipt protocol is incompatible",
            code="world.receipt.incompatible",
            subsystem="world",
            phase="compatibility",
            details={"field": "protocol"},
        )
    outcome_values = _array(document["command_outcomes"], role="command_outcomes")
    diagnostic_values = _array(document["diagnostics"], role="diagnostics")
    alias_values = _array(document["aliases"], role="aliases")
    _bounded_count("command_outcomes", len(outcome_values), limits.max_outcomes)
    _bounded_count("diagnostics", len(diagnostic_values), limits.max_diagnostics)
    _bounded_count("aliases", len(alias_values), limits.max_aliases)
    if not outcome_values:
        raise _receipt_decode_error(
            "receipt must contain at least one command outcome",
            phase="validate",
            details={"field": "command_outcomes"},
        )
    changes_value = document["changes"]
    receipt = TransactionReceipt(
        protocol=protocol,
        world_id=_stable_id(document["world_id"], field="world_id"),
        transaction_id=_stable_id(document["transaction_id"], field="transaction_id"),
        actor=_decode_actor(document["actor"]),
        status=_receipt_status(document["status"], field="status"),
        pre_hash=_sha256(document["pre_hash"], field="pre_hash"),
        post_hash=_sha256(document["post_hash"], field="post_hash"),
        proposed_post_hash=(
            None
            if document["proposed_post_hash"] is None
            else _sha256(document["proposed_post_hash"], field="proposed_post_hash")
        ),
        completed_ticks_before=_non_negative_int(
            document["completed_ticks_before"], field="completed_ticks_before"
        ),
        completed_ticks_after=_non_negative_int(
            document["completed_ticks_after"], field="completed_ticks_after"
        ),
        command_outcomes=tuple(_decode_outcome(item) for item in outcome_values),
        changes=(
            None if changes_value is None else _decode_semantic_diff(changes_value, limits=limits)
        ),
        diagnostics=tuple(_decode_diagnostic(item, limits=limits) for item in diagnostic_values),
        aliases=tuple(_decode_alias(item) for item in alias_values),
    )
    _validate_receipt(receipt)
    return receipt


def _decode_actor(value: object) -> CommandActor:
    document = _object(value, role="actor")
    _exact_fields(document, required={"kind", "id"}, role="actor")
    return CommandActor(
        _stable_id(document["kind"], field="actor.kind"),
        _stable_id(document["id"], field="actor.id"),
    )


def _decode_outcome(value: object) -> CommandOutcome:
    document = _object(value, role="command_outcome")
    _exact_fields(
        document,
        required={"command_id", "operation", "status"},
        role="command_outcome",
    )
    return CommandOutcome(
        _stable_id(document["command_id"], field="command_outcome.command_id"),
        _operation_id(document["operation"], field="command_outcome.operation"),
        _receipt_status(document["status"], field="command_outcome.status"),
    )


def _decode_diagnostic(value: object, *, limits: ReceiptLimits) -> ReceiptDiagnostic:
    document = _object(value, role="diagnostic")
    _exact_fields(
        document,
        required={"code", "phase", "message", "details"},
        role="diagnostic",
    )
    detail_document = _object(document["details"], role="diagnostic.details")
    _bounded_count("diagnostic.details", len(detail_document), limits.max_diagnostic_details)
    details: list[tuple[str, str | int | float | bool | None]] = []
    for key, item in detail_document.items():
        _field_name(key, field="diagnostic.details.key")
        if item is not None and type(item) not in (str, int, float, bool):
            raise _receipt_field_type_error("diagnostic.details.value", item, "scalar or null")
        details.append((key, cast(str | int | float | bool | None, item)))
    phase_value = document["phase"]
    phase = None if phase_value is None else _stable_id(phase_value, field="diagnostic.phase")
    message = _text(document["message"], field="diagnostic.message")
    if not message:
        raise _receipt_decode_error(
            "receipt diagnostic message must not be empty",
            phase="validate",
            details={"field": "diagnostic.message"},
        )
    return ReceiptDiagnostic(
        _error_code(document["code"], field="diagnostic.code"),
        phase,
        message,
        tuple(sorted(details)),
    )


def _decode_alias(value: object) -> tuple[str, str]:
    document = _object(value, role="alias")
    _exact_fields(document, required={"alias", "entity"}, role="alias")
    return (
        _stable_id(document["alias"], field="alias.alias"),
        _entity_id(document["entity"], field="alias.entity"),
    )


def _decode_semantic_diff(value: object, *, limits: ReceiptLimits) -> SemanticDiff:
    document = _object(value, role="changes")
    _exact_fields(
        document,
        required={
            "created_entities",
            "destroyed_entities",
            "changed_entities",
            "components_added",
            "components_removed",
            "components_changed",
            "resources_changed",
            "allocator",
            "epochs",
            "completed_ticks_before",
            "completed_ticks_after",
        },
        role="changes",
    )
    created_values = _array(document["created_entities"], role="changes.created_entities")
    destroyed_values = _array(document["destroyed_entities"], role="changes.destroyed_entities")
    changed_values = _array(document["changed_entities"], role="changes.changed_entities")
    added_values = _array(document["components_added"], role="changes.components_added")
    removed_values = _array(document["components_removed"], role="changes.components_removed")
    component_changed_values = _array(
        document["components_changed"], role="changes.components_changed"
    )
    resource_values = _array(document["resources_changed"], role="changes.resources_changed")
    allocator_document = _object(document["allocator"], role="changes.allocator")
    epoch_document = _object(document["epochs"], role="changes.epochs")
    _exact_fields(
        allocator_document,
        required={"free_before", "free_after", "slots"},
        role="changes.allocator",
    )
    _exact_fields(
        epoch_document,
        required={
            "world_before",
            "world_after",
            "structural_before",
            "structural_after",
            "tables",
        },
        role="changes.epochs",
    )
    slot_values = _array(allocator_document["slots"], role="changes.allocator.slots")
    table_values = _array(epoch_document["tables"], role="changes.epochs.tables")
    record_count = sum(
        len(items)
        for items in (
            created_values,
            destroyed_values,
            changed_values,
            added_values,
            removed_values,
            component_changed_values,
            resource_values,
            slot_values,
            table_values,
        )
    )
    _bounded_count("changes.records", record_count, limits.max_diff_records)
    result = SemanticDiff(
        created_entities=tuple(
            _entity_id(item, field="changes.created_entities") for item in created_values
        ),
        destroyed_entities=tuple(
            _entity_id(item, field="changes.destroyed_entities") for item in destroyed_values
        ),
        changed_entities=tuple(
            _entity_id(item, field="changes.changed_entities") for item in changed_values
        ),
        components_added=tuple(
            _decode_component_change(item, role="added") for item in added_values
        ),
        components_removed=tuple(
            _decode_component_change(item, role="removed") for item in removed_values
        ),
        components_changed=tuple(
            _decode_component_change(item, role="changed") for item in component_changed_values
        ),
        resources_changed=tuple(_decode_resource_change(item) for item in resource_values),
        allocator=_decode_allocator_change(allocator_document),
        epochs=_decode_epoch_change(epoch_document),
        completed_ticks_before=_non_negative_int(
            document["completed_ticks_before"], field="changes.completed_ticks_before"
        ),
        completed_ticks_after=_non_negative_int(
            document["completed_ticks_after"], field="changes.completed_ticks_after"
        ),
    )
    _validate_semantic_diff(result)
    return result


def _decode_component_change(value: object, *, role: str) -> ComponentChange:
    document = _object(value, role=f"component_{role}")
    _exact_fields(
        document,
        required={"entity", "type_id", "fields", "before_epoch", "after_epoch"},
        role=f"component_{role}",
    )
    field_values = _array(document["fields"], role=f"component_{role}.fields")
    fields = tuple(_field_name(item, field=f"component_{role}.fields") for item in field_values)
    _require_unique(fields, field=f"component_{role}.fields")
    before = _optional_non_negative_int(
        document["before_epoch"], field=f"component_{role}.before_epoch"
    )
    after = _optional_non_negative_int(
        document["after_epoch"], field=f"component_{role}.after_epoch"
    )
    valid_epochs = (
        (role == "added" and before is None and after is not None)
        or (role == "removed" and before is not None and after is None)
        or (role == "changed" and before is not None and after is not None and after > before)
    )
    if not valid_epochs:
        raise _receipt_decode_error(
            "component change epochs do not match the change role",
            phase="validate",
            details={"field": f"component_{role}.epochs"},
        )
    return ComponentChange(
        _entity_id(document["entity"], field=f"component_{role}.entity"),
        _type_id(document["type_id"], field=f"component_{role}.type_id"),
        fields,
        before,
        after,
    )


def _decode_resource_change(value: object) -> ResourceChange:
    document = _object(value, role="resource_change")
    _exact_fields(
        document,
        required={"type_id", "before_present", "after_present", "value_changed"},
        role="resource_change",
    )
    change = ResourceChange(
        _type_id(document["type_id"], field="resource_change.type_id"),
        _boolean(document["before_present"], field="resource_change.before_present"),
        _boolean(document["after_present"], field="resource_change.after_present"),
        _boolean(document["value_changed"], field="resource_change.value_changed"),
    )
    if change.before_present == change.after_present and not change.value_changed:
        raise _receipt_decode_error(
            "resource change must describe a presence or value change",
            phase="validate",
            details={"field": "resource_change"},
        )
    return change


def _decode_allocator_change(value: object) -> AllocatorChange:
    document = _object(value, role="allocator")
    _exact_fields(document, required={"free_before", "free_after", "slots"}, role="allocator")
    free_before = tuple(
        _non_negative_int(item, field="allocator.free_before")
        for item in _array(document["free_before"], role="allocator.free_before")
    )
    free_after = tuple(
        _non_negative_int(item, field="allocator.free_after")
        for item in _array(document["free_after"], role="allocator.free_after")
    )
    _require_unique(free_before, field="allocator.free_before")
    _require_unique(free_after, field="allocator.free_after")
    slots = tuple(
        _decode_allocator_slot(item) for item in _array(document["slots"], role="allocator.slots")
    )
    _require_unique((slot.index for slot in slots), field="allocator.slots.index")
    return AllocatorChange(free_before, free_after, slots)


def _decode_allocator_slot(value: object) -> AllocatorSlotChange:
    document = _object(value, role="allocator_slot")
    _exact_fields(
        document,
        required={
            "index",
            "before_generation",
            "after_generation",
            "before_alive",
            "after_alive",
        },
        role="allocator_slot",
    )
    before_generation = _optional_non_negative_int(
        document["before_generation"], field="allocator_slot.before_generation"
    )
    after_generation = _optional_non_negative_int(
        document["after_generation"], field="allocator_slot.after_generation"
    )
    before_alive = _optional_boolean(document["before_alive"], field="allocator_slot.before_alive")
    after_alive = _optional_boolean(document["after_alive"], field="allocator_slot.after_alive")
    if (before_generation is None) != (before_alive is None) or (
        (after_generation is None) != (after_alive is None)
    ):
        raise _receipt_decode_error(
            "allocator generation and alive values must be present together",
            phase="validate",
            details={"field": "allocator_slot"},
        )
    if (before_generation, before_alive) == (after_generation, after_alive):
        raise _receipt_decode_error(
            "allocator slot must describe a change",
            phase="validate",
            details={"field": "allocator_slot"},
        )
    return AllocatorSlotChange(
        _non_negative_int(document["index"], field="allocator_slot.index"),
        before_generation,
        after_generation,
        before_alive,
        after_alive,
    )


def _decode_epoch_change(value: object) -> EpochChange:
    document = _object(value, role="epochs")
    _exact_fields(
        document,
        required={
            "world_before",
            "world_after",
            "structural_before",
            "structural_after",
            "tables",
        },
        role="epochs",
    )
    tables = tuple(
        _decode_table_epoch(item) for item in _array(document["tables"], role="epochs.tables")
    )
    _require_unique((table.type_id for table in tables), field="epochs.tables.type_id")
    result = EpochChange(
        _non_negative_int(document["world_before"], field="epochs.world_before"),
        _non_negative_int(document["world_after"], field="epochs.world_after"),
        _non_negative_int(document["structural_before"], field="epochs.structural_before"),
        _non_negative_int(document["structural_after"], field="epochs.structural_after"),
        tables,
    )
    if result.world_after < result.world_before or (
        result.structural_after < result.structural_before
    ):
        raise _receipt_decode_error(
            "receipt epochs must not move backward",
            phase="validate",
            details={"field": "epochs"},
        )
    return result


def _decode_table_epoch(value: object) -> TableEpochChange:
    document = _object(value, role="table_epoch")
    _exact_fields(document, required={"type_id", "before", "after"}, role="table_epoch")
    before = _non_negative_int(document["before"], field="table_epoch.before")
    after = _non_negative_int(document["after"], field="table_epoch.after")
    if after <= before:
        raise _receipt_decode_error(
            "table epoch change must move forward",
            phase="validate",
            details={"field": "table_epoch"},
        )
    return TableEpochChange(
        _type_id(document["type_id"], field="table_epoch.type_id"), before, after
    )


def _validate_receipt(receipt: TransactionReceipt) -> None:
    _require_unique(
        (outcome.command_id for outcome in receipt.command_outcomes),
        field="command_outcomes.command_id",
    )
    if any(outcome.status is not receipt.status for outcome in receipt.command_outcomes):
        raise _receipt_decode_error(
            "command outcome status must match the receipt status",
            phase="validate",
            details={"field": "command_outcomes.status"},
        )
    alias_names = tuple(alias for alias, _ in receipt.aliases)
    alias_entities = tuple(entity for _, entity in receipt.aliases)
    _require_unique(alias_names, field="aliases.alias")
    _require_unique(alias_entities, field="aliases.entity")
    if receipt.completed_ticks_after < receipt.completed_ticks_before:
        raise _receipt_decode_error(
            "receipt completed ticks must not move backward",
            phase="validate",
            details={"field": "completed_ticks_after"},
        )
    if receipt.status is ReceiptStatus.REJECTED:
        valid = (
            receipt.pre_hash == receipt.post_hash
            and receipt.proposed_post_hash is None
            and receipt.completed_ticks_before == receipt.completed_ticks_after
            and receipt.changes is None
            and bool(receipt.diagnostics)
            and not receipt.aliases
        )
    elif receipt.status is ReceiptStatus.DRY_RUN:
        valid = (
            receipt.pre_hash == receipt.post_hash
            and receipt.proposed_post_hash is not None
            and receipt.completed_ticks_before == receipt.completed_ticks_after
            and receipt.changes is not None
            and not receipt.diagnostics
        )
    else:
        valid = (
            receipt.proposed_post_hash is None
            and receipt.changes is not None
            and not receipt.diagnostics
        )
    if not valid:
        raise _receipt_decode_error(
            "receipt fields do not match its status invariants",
            phase="validate",
            details={"field": "status"},
        )
    if receipt.changes is not None:
        if receipt.changes.completed_ticks_before != receipt.completed_ticks_before:
            raise _receipt_decode_error(
                "receipt and semantic diff disagree on the starting tick",
                phase="validate",
                details={"field": "changes.completed_ticks_before"},
            )
        if (
            receipt.status is ReceiptStatus.COMMITTED
            and receipt.changes.completed_ticks_after != receipt.completed_ticks_after
        ):
            raise _receipt_decode_error(
                "committed receipt and semantic diff disagree on the ending tick",
                phase="validate",
                details={"field": "changes.completed_ticks_after"},
            )


def _validate_semantic_diff(changes: SemanticDiff) -> None:
    for field, entities in (
        ("created_entities", changes.created_entities),
        ("destroyed_entities", changes.destroyed_entities),
        ("changed_entities", changes.changed_entities),
    ):
        _require_unique(entities, field=f"changes.{field}")
    entity_sets = (
        set(changes.created_entities),
        set(changes.destroyed_entities),
        set(changes.changed_entities),
    )
    if any(entity_sets[left] & entity_sets[right] for left, right in ((0, 1), (0, 2), (1, 2))):
        raise _receipt_decode_error(
            "semantic diff entity categories must be disjoint",
            phase="validate",
            details={"field": "changes.entities"},
        )
    component_keys = tuple(
        (change.entity, change.type_id)
        for change in (
            *changes.components_added,
            *changes.components_removed,
            *changes.components_changed,
        )
    )
    _require_unique(component_keys, field="changes.components")
    _require_unique(
        (change.type_id for change in changes.resources_changed),
        field="changes.resources_changed.type_id",
    )
    if changes.completed_ticks_after < changes.completed_ticks_before:
        raise _receipt_decode_error(
            "semantic diff completed ticks must not move backward",
            phase="validate",
            details={"field": "changes.completed_ticks_after"},
        )


def _exact_fields(value: Mapping[str, object], *, required: set[str], role: str) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required)
    if missing or unexpected:
        raise _receipt_decode_error(
            "receipt object fields do not match its schema",
            phase="decode",
            details={
                "role": role,
                "missing": ",".join(missing),
                "unexpected": ",".join(unexpected),
            },
        )


def _object(value: object, *, role: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise _receipt_decode_error(
            "receipt value must be an object",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, JsonValue], value)


def _array(value: object, *, role: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise _receipt_decode_error(
            "receipt value must be an array",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(list[JsonValue], value)


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _receipt_field_type_error(field, value, "string")
    return value


def _boolean(value: object, *, field: str) -> bool:
    if type(value) is not bool:
        raise _receipt_field_type_error(field, value, "boolean")
    return value


def _optional_boolean(value: object, *, field: str) -> bool | None:
    if value is None:
        return None
    return _boolean(value, field=field)


def _non_negative_int(value: object, *, field: str) -> int:
    if type(value) is not int or value < 0 or value > _MAX_SIGNED_INT:
        raise _receipt_decode_error(
            "receipt field must be a non-negative signed 64-bit integer",
            phase="validate",
            details={"field": field},
        )
    return value


def _optional_non_negative_int(value: object, *, field: str) -> int | None:
    if value is None:
        return None
    return _non_negative_int(value, field=field)


def _stable_id(value: object, *, field: str) -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _receipt_decode_error(
            "receipt identity must use bounded stable text",
            phase="validate",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _operation_id(value: object, *, field: str) -> str:
    if type(value) is not str or _OPERATION_ID.fullmatch(value) is None:
        raise _receipt_decode_error(
            "receipt operation must use a dotted stable identifier",
            phase="validate",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _error_code(value: object, *, field: str) -> str:
    if type(value) is not str or _ERROR_CODE.fullmatch(value) is None:
        raise _receipt_decode_error(
            "receipt diagnostic code must use a dotted stable identifier",
            phase="validate",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _field_name(value: object, *, field: str) -> str:
    if type(value) is not str or _FIELD_NAME.fullmatch(value) is None:
        raise _receipt_decode_error(
            "receipt field name must use bounded identifier text",
            phase="validate",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _sha256(value: object, *, field: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise _receipt_decode_error(
            "receipt hash must use canonical SHA-256 text",
            phase="validate",
            details={"field": field},
        )
    return value


def _entity_id(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _receipt_field_type_error(field, value, "entity text")
    match = _ENTITY.fullmatch(value)
    if match is None or any(not _bounded_decimal(part) for part in match.groups()):
        raise _receipt_decode_error(
            "receipt entity must use canonical index:generation text",
            phase="validate",
            details={"field": field},
        )
    return value


def _bounded_decimal(value: str) -> bool:
    maximum = str(_MAX_SIGNED_INT)
    return len(value) < len(maximum) or (len(value) == len(maximum) and value <= maximum)


def _type_id(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _receipt_field_type_error(field, value, "UUID text")
    try:
        parsed = UUID(value)
    except (ValueError, AttributeError) as error:
        raise _receipt_decode_error(
            "receipt type identity must use canonical UUID text",
            phase="validate",
            details={"field": field},
        ) from error
    if str(parsed) != value:
        raise _receipt_decode_error(
            "receipt type identity must use canonical UUID text",
            phase="validate",
            details={"field": field},
        )
    return value


def _receipt_status(value: object, *, field: str) -> ReceiptStatus:
    text = _text(value, field=field)
    try:
        return ReceiptStatus(text)
    except ValueError as error:
        raise _receipt_decode_error(
            "receipt status is not supported",
            phase="validate",
            details={"field": field},
        ) from error


def _require_unique(values: Iterable[object], *, field: str) -> None:
    items = tuple(values)
    try:
        unique_count = len(set(items))
    except TypeError as error:
        raise _receipt_decode_error(
            "receipt uniqueness field contains an unsupported value",
            phase="validate",
            details={"field": field},
        ) from error
    if unique_count != len(items):
        raise _receipt_decode_error(
            "receipt values must be unique",
            phase="validate",
            details={"field": field},
        )


def _bounded_count(field: str, actual: int, limit: int) -> None:
    if actual > limit:
        raise ReceiptDecodeError(
            "receipt exceeds a configured deterministic limit",
            code="world.receipt.oversized",
            subsystem="world",
            phase="validate",
            details={"field": field, "actual": actual, "limit": limit},
        )


def _receipt_field_type_error(field: str, value: object, expected: str) -> ReceiptDecodeError:
    return _receipt_decode_error(
        "receipt field has an invalid type",
        phase="decode",
        details={"field": field, "expected": expected, "actual_type": type(value).__name__},
    )


def _nested_receipt_error(error: LudoWeaveError) -> ReceiptDecodeError:
    nested = dict(error.details)
    if "limit" in nested:
        details: dict[str, str | int | float | bool | None] = {
            "cause_code": error.code,
            "field": f"json.{error.phase or 'value'}",
            "limit": nested["limit"],
        }
        if "actual" in nested:
            details["actual"] = nested["actual"]
        return ReceiptDecodeError(
            "receipt exceeds a configured deterministic limit",
            code="world.receipt.oversized",
            subsystem="world",
            phase=error.phase or "decode",
            details=details,
        )
    return _receipt_decode_error(
        "receipt contains an invalid nested protocol value",
        phase="decode",
        details={"cause_code": error.code},
    )


def _receipt_decode_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> ReceiptDecodeError:
    return ReceiptDecodeError(
        message,
        code="world.receipt.malformed",
        subsystem="world",
        phase=phase,
        details=details,
    )


def rejected_receipt(
    transaction: CommandTransaction,
    *,
    world_id: str,
    current_hash: str,
    completed_ticks: int,
    error: LudoWeaveError,
) -> TransactionReceipt:
    return TransactionReceipt(
        world_id=world_id,
        transaction_id=transaction.transaction_id,
        actor=transaction.actor,
        status=ReceiptStatus.REJECTED,
        pre_hash=current_hash,
        post_hash=current_hash,
        proposed_post_hash=None,
        completed_ticks_before=completed_ticks,
        completed_ticks_after=completed_ticks,
        command_outcomes=tuple(
            CommandOutcome(command.command_id, command.operation, ReceiptStatus.REJECTED)
            for command in transaction.commands
        ),
        changes=None,
        diagnostics=(ReceiptDiagnostic.from_error(error),),
    )
