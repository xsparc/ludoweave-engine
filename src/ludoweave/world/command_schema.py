"""Versioned persistent command envelopes and operation identities."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from hashlib import sha256
from types import MappingProxyType
from typing import cast

from ludoweave.world.canonical import (
    FrozenJsonValue,
    JsonValue,
    canonical_dumps,
    canonical_loads,
    freeze_json_object,
    thaw_json,
)
from ludoweave.world.errors import (
    CommandSchemaError,
    DuplicateOperationError,
    UnknownOperationError,
)

COMMAND_PROTOCOL = "ludoweave.command/1"
TRANSACTION_PROTOCOL = "ludoweave.transaction/1"

_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_OPERATION_ID = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\Z")
_HASH = re.compile(r"(?:sha256|blake3):[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class CommandActor:
    """Attribution attached to every externally initiated command."""

    kind: str
    id: str

    def __post_init__(self) -> None:
        _require_stable_id(self.kind, field="actor.kind")
        _require_stable_id(self.id, field="actor.id")

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "id": self.id}


@dataclass(frozen=True, slots=True, eq=False)
class CommandEnvelope:
    """One immutable, versioned command addressed to a world transaction."""

    command_id: str
    transaction_id: str
    actor: CommandActor
    operation: str
    arguments: Mapping[str, object]
    operation_version: int = 1
    expected_world_hash: str | None = None
    protocol: str = COMMAND_PROTOCOL

    def __post_init__(self) -> None:
        if self.protocol != COMMAND_PROTOCOL:
            raise _schema_error(
                "command protocol is incompatible",
                phase="construct",
                details={"protocol": self.protocol},
            )
        _require_stable_id(self.command_id, field="command_id")
        _require_stable_id(self.transaction_id, field="transaction_id")
        _require_operation_id(self.operation)
        _require_positive_version(self.operation_version, field="operation_version")
        if (
            self.expected_world_hash is not None
            and _HASH.fullmatch(self.expected_world_hash) is None
        ):
            raise _schema_error(
                "expected world hash has an unsupported format",
                phase="construct",
                details={"field": "expected_world_hash"},
            )
        object.__setattr__(self, "arguments", freeze_json_object(self.arguments))

    @classmethod
    def from_mapping(cls, value: object) -> CommandEnvelope:
        """Validate and construct an envelope from a decoded JSON object."""

        document = _require_object(value, role="command")
        _require_exact_fields(
            document,
            required={
                "protocol",
                "command_id",
                "transaction_id",
                "actor",
                "operation",
                "arguments",
            },
            optional={"operation_version", "expected_world_hash"},
            role="command",
        )
        actor_document = _require_object(document["actor"], role="actor")
        _require_exact_fields(actor_document, required={"kind", "id"}, optional=set(), role="actor")
        actor = CommandActor(
            kind=_require_string(actor_document["kind"], field="actor.kind"),
            id=_require_string(actor_document["id"], field="actor.id"),
        )
        expected = document.get("expected_world_hash")
        if expected is not None and type(expected) is not str:
            raise _field_type_error("expected_world_hash", expected, "string or null")
        version = document.get("operation_version", 1)
        return cls(
            protocol=_require_string(document["protocol"], field="protocol"),
            command_id=_require_string(document["command_id"], field="command_id"),
            transaction_id=_require_string(document["transaction_id"], field="transaction_id"),
            actor=actor,
            operation=_require_string(document["operation"], field="operation"),
            operation_version=_require_int(version, field="operation_version"),
            expected_world_hash=expected,
            arguments=freeze_json_object(document["arguments"]),
        )

    @classmethod
    def from_json(cls, document: str | bytes) -> CommandEnvelope:
        return cls.from_mapping(canonical_loads(document))

    def as_dict(self) -> dict[str, JsonValue]:
        result: dict[str, JsonValue] = {
            "protocol": self.protocol,
            "command_id": self.command_id,
            "transaction_id": self.transaction_id,
            "actor": cast(dict[str, JsonValue], self.actor.as_dict()),
            "operation": self.operation,
            "operation_version": self.operation_version,
            "arguments": thaw_json(cast(FrozenJsonValue, self.arguments)),
        }
        if self.expected_world_hash is not None:
            result["expected_world_hash"] = self.expected_world_hash
        return result

    def canonical_bytes(self) -> bytes:
        return canonical_dumps(self.as_dict())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CommandEnvelope):
            return NotImplemented
        return self.canonical_bytes() == other.canonical_bytes()


@dataclass(frozen=True, slots=True)
class CommandTransaction:
    """A bounded ordered command batch sharing attribution and concurrency intent."""

    commands: tuple[CommandEnvelope, ...]
    world_id: str
    dry_run: bool = False
    protocol: str = TRANSACTION_PROTOCOL

    def __post_init__(self) -> None:
        if self.protocol != TRANSACTION_PROTOCOL:
            raise _schema_error(
                "transaction protocol is incompatible",
                phase="construct",
                details={"protocol": self.protocol},
            )
        _require_stable_id(self.world_id, field="world_id")
        commands = tuple(self.commands)
        if not commands:
            raise _schema_error(
                "transaction must contain at least one command",
                phase="construct",
                details={"field": "commands"},
            )
        if type(self.dry_run) is not bool:
            raise _field_type_error("dry_run", self.dry_run, "boolean")
        first = commands[0]
        command_ids: set[str] = set()
        for index, command in enumerate(commands):
            if command.command_id in command_ids:
                raise _schema_error(
                    "transaction command IDs must be unique",
                    phase="construct",
                    details={"command_id": command.command_id},
                )
            command_ids.add(command.command_id)
            if command.transaction_id != first.transaction_id:
                raise _schema_error(
                    "commands must share one transaction ID",
                    phase="construct",
                    details={"command_index": index},
                )
            if command.actor != first.actor:
                raise _schema_error(
                    "commands must share one actor",
                    phase="construct",
                    details={"command_index": index},
                )
            if command.expected_world_hash != first.expected_world_hash:
                raise _schema_error(
                    "commands must share one expected world hash",
                    phase="construct",
                    details={"command_index": index},
                )
        object.__setattr__(self, "commands", commands)

    @property
    def transaction_id(self) -> str:
        return self.commands[0].transaction_id

    @property
    def actor(self) -> CommandActor:
        return self.commands[0].actor

    @property
    def expected_world_hash(self) -> str | None:
        return self.commands[0].expected_world_hash

    @classmethod
    def from_mapping(cls, value: object) -> CommandTransaction:
        document = _require_object(value, role="transaction")
        _require_exact_fields(
            document,
            required={"protocol", "commands", "world_id"},
            optional={"dry_run"},
            role="transaction",
        )
        raw_commands = document["commands"]
        if not isinstance(raw_commands, list):
            raise _field_type_error("commands", raw_commands, "array")
        command_values = cast(list[object], raw_commands)
        dry_run = document.get("dry_run", False)
        if type(dry_run) is not bool:
            raise _field_type_error("dry_run", dry_run, "boolean")
        return cls(
            protocol=_require_string(document["protocol"], field="protocol"),
            commands=tuple(CommandEnvelope.from_mapping(command) for command in command_values),
            world_id=_require_string(document["world_id"], field="world_id"),
            dry_run=dry_run,
        )

    @classmethod
    def from_json(cls, document: str | bytes) -> CommandTransaction:
        return cls.from_mapping(canonical_loads(document))

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "protocol": self.protocol,
            "world_id": self.world_id,
            "dry_run": self.dry_run,
            "commands": [command.as_dict() for command in self.commands],
        }

    def canonical_bytes(self) -> bytes:
        return canonical_dumps(self.as_dict())


@dataclass(frozen=True, slots=True)
class OperationSpec:
    """Stable identity and transaction classification for one operation schema."""

    operation: str
    version: int = 1
    mutating: bool = True
    transactional: bool = True

    def __post_init__(self) -> None:
        _require_operation_id(self.operation)
        _require_positive_version(self.version, field="version")
        if type(self.mutating) is not bool:
            raise _field_type_error("mutating", self.mutating, "boolean")
        if type(self.transactional) is not bool:
            raise _field_type_error("transactional", self.transactional, "boolean")
        if self.transactional and not self.mutating:
            raise _schema_error(
                "read-only operations cannot be transaction-required",
                phase="define_operation",
                details={"operation": self.operation, "version": self.version},
            )


class OperationRegistry:
    """Immutable composition-owned index of operation schema versions."""

    __slots__ = ("_by_identity", "_specs")

    def __init__(self, specs: Iterable[object] = ()) -> None:
        by_identity: dict[tuple[str, int], OperationSpec] = {}
        for candidate in specs:
            if not isinstance(candidate, OperationSpec):
                raise _field_type_error("operations", candidate, "operation spec")
            identity = (candidate.operation, candidate.version)
            if identity in by_identity:
                raise DuplicateOperationError(
                    "operation identity is already registered",
                    code="world.duplicate_operation",
                    subsystem="world",
                    phase="register",
                    details={"operation": candidate.operation, "version": candidate.version},
                )
            by_identity[identity] = candidate
        self._by_identity = MappingProxyType(by_identity)
        self._specs = tuple(by_identity[key] for key in sorted(by_identity))

    @property
    def specs(self) -> tuple[OperationSpec, ...]:
        return self._specs

    @property
    def fingerprint(self) -> str:
        """Return a content identity for compatibility headers."""

        document = [
            {
                "operation": spec.operation,
                "version": spec.version,
                "mutating": spec.mutating,
                "transactional": spec.transactional,
            }
            for spec in self._specs
        ]
        return f"sha256:{sha256(canonical_dumps(document)).hexdigest()}"

    def resolve(self, operation: str, version: int) -> OperationSpec:
        checked_operation = _require_operation_id(operation)
        checked_version = _require_positive_version(version, field="version")
        spec = self._by_identity.get((checked_operation, checked_version))
        if spec is None:
            raise UnknownOperationError(
                "operation identity is not registered",
                code="world.unknown_operation",
                subsystem="world",
                phase="resolve",
                details={"operation": checked_operation, "version": checked_version},
            )
        return spec


def _require_object(value: object, *, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _schema_error(
            f"{role} document must be a JSON object",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, object], value)


def _require_exact_fields(
    value: Mapping[str, object],
    *,
    required: set[str],
    optional: set[str],
    role: str,
) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required - optional)
    if missing or unexpected:
        raise _schema_error(
            f"{role} document fields do not match its schema",
            phase="decode",
            details={
                "role": role,
                "missing": ",".join(missing),
                "unexpected": ",".join(unexpected),
            },
        )


def _require_string(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _field_type_error(field, value, "string")
    return value


def _require_int(value: object, *, field: str) -> int:
    if type(value) is not int:
        raise _field_type_error(field, value, "integer")
    return value


def _require_stable_id(value: object, *, field: str) -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _schema_error(
            "command identity must use bounded stable text",
            phase="construct",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _require_operation_id(value: object) -> str:
    if type(value) is not str or _OPERATION_ID.fullmatch(value) is None:
        raise _schema_error(
            "operation ID must be a dotted stable identifier",
            phase="construct",
            details={"field": "operation", "actual_type": type(value).__name__},
        )
    return value


def _require_positive_version(value: object, *, field: str) -> int:
    if type(value) is not int or value <= 0 or value > 2**63 - 1:
        raise _schema_error(
            "schema versions must be positive signed 64-bit integers",
            phase="construct",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _field_type_error(field: str, value: object, expected: str) -> CommandSchemaError:
    return _schema_error(
        "command field has an invalid type",
        phase="construct",
        details={"field": field, "expected": expected, "actual_type": type(value).__name__},
    )


def _schema_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> CommandSchemaError:
    return CommandSchemaError(
        message,
        code="world.invalid_command_schema",
        subsystem="world",
        phase=phase,
        details=details,
    )


BUILTIN_OPERATION_SPECS = (
    OperationSpec("component.add"),
    OperationSpec("component.patch"),
    OperationSpec("component.remove"),
    OperationSpec("entity.destroy"),
    OperationSpec("entity.spawn"),
    OperationSpec("resource.patch"),
    OperationSpec("world.tick"),
)


def builtin_operation_registry() -> OperationRegistry:
    """Build the explicit registry implemented by the current M2 service scope."""

    return OperationRegistry(BUILTIN_OPERATION_SPECS)
