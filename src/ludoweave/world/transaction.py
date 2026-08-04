# pyright: reportPrivateUsage=false
"""Validate and atomically apply persistent operations to a staged session."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import StrEnum

from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs import EntityId
from ludoweave.world.canonical import JsonValue
from ludoweave.world.command_schema import (
    CommandTransaction,
    OperationRegistry,
    builtin_operation_registry,
)
from ludoweave.world.diff import SemanticDiff, semantic_diff
from ludoweave.world.errors import (
    StaleWorldHashError,
    TransactionApplicationError,
    TransactionValidationError,
)
from ludoweave.world.operations import (
    AddComponentOperation,
    DestroyOperation,
    PatchComponentOperation,
    PatchResourceOperation,
    RemoveComponentOperation,
    SpawnOperation,
    TickOperation,
    TypedOperation,
    parse_operation,
)
from ludoweave.world.receipt import (
    CommandOutcome,
    ReceiptStatus,
    TransactionReceipt,
    rejected_receipt,
)
from ludoweave.world.state import WorldSession, _SessionRecord


@dataclass(frozen=True, slots=True)
class TransactionLimits:
    """Deterministic work limits checked before session adoption."""

    max_bytes: int = 1_048_576
    max_commands: int = 1_024
    max_ticks: int = 10_000
    max_aliases: int = 1_024
    max_diff_records: int = 100_000
    max_receipt_bytes: int = 1_048_576

    def __post_init__(self) -> None:
        for field_name in (
            "max_aliases",
            "max_bytes",
            "max_commands",
            "max_diff_records",
            "max_receipt_bytes",
            "max_ticks",
        ):
            value = getattr(self, field_name)
            if type(value) is not int or value <= 0:
                raise TransactionValidationError(
                    "transaction limits must be positive integers",
                    code="world.transaction.invalid_limits",
                    subsystem="world",
                    phase="configure",
                    details={"field": field_name, "actual_type": type(value).__name__},
                )


class ApplicationStatus(StrEnum):
    """Successful staged outcome before M2-03 receipt projection."""

    COMMITTED = "committed"
    DRY_RUN = "dry_run"


@dataclass(frozen=True, slots=True)
class TransactionApplication:
    """Successful M2-02 apply result; M2-03 projects it into a receipt."""

    transaction_id: str
    status: ApplicationStatus
    pre_hash: str
    resulting_hash: str
    completed_ticks_before: int
    completed_ticks_after: int
    operation_count: int
    aliases: tuple[tuple[str, EntityId], ...]
    pre_document: dict[str, JsonValue]
    resulting_document: dict[str, JsonValue]
    staged_record: _SessionRecord = field(repr=False)


class TransactionService:
    """One serial validator and clone-stage-adopt transaction service."""

    __slots__ = ("_limits", "_operations", "_session")

    def __init__(
        self,
        session: WorldSession,
        *,
        operations: OperationRegistry | None = None,
        limits: TransactionLimits | None = None,
    ) -> None:
        self._session = session
        self._operations = operations or builtin_operation_registry()
        self._limits = limits or TransactionLimits()

    @property
    def session(self) -> WorldSession:
        return self._session

    def validate(self, transaction: CommandTransaction) -> TransactionReceipt:
        """Fully stage a dry-run without changing authoritative session state."""

        return self.apply(replace(transaction, dry_run=True))

    def apply(self, transaction: CommandTransaction) -> TransactionReceipt:
        """Return a canonical committed, dry-run, or rejected transaction receipt."""

        pre_document, pre_hash = self._session._capture_current()
        ticks_before = self._session.completed_ticks
        try:
            application = self._apply_checked(
                transaction,
                pre_document=pre_document,
                pre_hash=pre_hash,
            )
            status = (
                ReceiptStatus.DRY_RUN
                if application.status is ApplicationStatus.DRY_RUN
                else ReceiptStatus.COMMITTED
            )
            changes = semantic_diff(application.pre_document, application.resulting_document)
            self._validate_diff_size(changes)
            receipt = TransactionReceipt(
                world_id=self._session.world_id,
                transaction_id=transaction.transaction_id,
                actor=transaction.actor,
                status=status,
                pre_hash=application.pre_hash,
                post_hash=(
                    application.pre_hash
                    if status is ReceiptStatus.DRY_RUN
                    else application.resulting_hash
                ),
                proposed_post_hash=(
                    application.resulting_hash if status is ReceiptStatus.DRY_RUN else None
                ),
                completed_ticks_before=application.completed_ticks_before,
                completed_ticks_after=(
                    application.completed_ticks_before
                    if status is ReceiptStatus.DRY_RUN
                    else application.completed_ticks_after
                ),
                command_outcomes=tuple(
                    CommandOutcome(command.command_id, command.operation, status)
                    for command in transaction.commands
                ),
                changes=changes,
                diagnostics=(),
                aliases=tuple(
                    (alias, f"{entity.index}:{entity.generation}")
                    for alias, entity in application.aliases
                ),
            )
            receipt_size = len(receipt.canonical_bytes())
            if receipt_size > self._limits.max_receipt_bytes:
                raise _limit_error("receipt_bytes", receipt_size, self._limits.max_receipt_bytes)
        except LudoWeaveError as error:
            return rejected_receipt(
                transaction,
                world_id=self._session.world_id,
                current_hash=pre_hash,
                completed_ticks=ticks_before,
                error=error,
            )

        if status is ReceiptStatus.COMMITTED:
            self._session._adopt(application.staged_record)
        return receipt

    def _apply_checked(
        self,
        transaction: CommandTransaction,
        *,
        pre_document: dict[str, JsonValue],
        pre_hash: str,
    ) -> TransactionApplication:
        """Apply one complete transaction or raise without live adoption."""

        self._validate_batch_boundary(transaction)
        expected = transaction.expected_world_hash
        if expected is not None:
            if not expected.startswith("sha256:"):
                raise TransactionValidationError(
                    "expected world hash uses an unsupported algorithm",
                    code="world.hash.unsupported_algorithm",
                    subsystem="world",
                    phase="validate",
                    details={"algorithm": expected.partition(":")[0]},
                )
            if expected != pre_hash:
                raise StaleWorldHashError(
                    "expected world hash does not match current authoritative state",
                    code="world.transaction.stale_hash",
                    subsystem="world",
                    phase="precondition",
                    details={"expected_hash": expected, "actual_hash": pre_hash},
                )

        typed_operations = self._decode_operations(transaction)
        self._validate_operation_sequence(typed_operations)
        try:
            staged = self._session._stage()
        except Exception as error:
            raise _application_error(
                "authoritative session could not be staged",
                operation_index=None,
                command_id=None,
                cause=error,
            ) from error

        aliases: dict[str, EntityId] = {}
        current = staged
        for index, (command, operation) in enumerate(
            zip(transaction.commands, typed_operations, strict=True)
        ):
            try:
                current = self._apply_operation(current, operation, aliases)
            except Exception as error:
                raise _application_error(
                    "transaction operation failed against staged state",
                    operation_index=index,
                    command_id=command.command_id,
                    cause=error,
                ) from error

        try:
            resulting_document, resulting_hash = self._session._capture_staged(current)
        except Exception as error:
            raise _application_error(
                "staged authoritative state could not be hashed",
                operation_index=None,
                command_id=None,
                cause=error,
            ) from error

        status = ApplicationStatus.DRY_RUN if transaction.dry_run else ApplicationStatus.COMMITTED
        return TransactionApplication(
            transaction_id=transaction.transaction_id,
            status=status,
            pre_hash=pre_hash,
            resulting_hash=resulting_hash,
            completed_ticks_before=staged.completed_ticks,
            completed_ticks_after=current.completed_ticks,
            operation_count=len(typed_operations),
            aliases=tuple(sorted(aliases.items())),
            pre_document=pre_document,
            resulting_document=resulting_document,
            staged_record=current,
        )

    def _validate_diff_size(self, changes: SemanticDiff) -> None:
        records = sum(
            (
                len(changes.created_entities),
                len(changes.destroyed_entities),
                len(changes.components_added),
                len(changes.components_removed),
                len(changes.components_changed),
                len(changes.resources_changed),
                len(changes.allocator.slots),
                len(changes.epochs.tables),
            )
        )
        if records > self._limits.max_diff_records:
            raise _limit_error("diff_records", records, self._limits.max_diff_records)

    def _validate_batch_boundary(self, transaction: CommandTransaction) -> None:
        if transaction.world_id != self._session.world_id:
            raise TransactionValidationError(
                "transaction targets a different world",
                code="world.transaction.world_mismatch",
                subsystem="world",
                phase="validate",
                details={"world_id": transaction.world_id},
            )
        count = len(transaction.commands)
        if count > self._limits.max_commands:
            raise _limit_error("commands", count, self._limits.max_commands)
        byte_count = len(transaction.canonical_bytes())
        if byte_count > self._limits.max_bytes:
            raise _limit_error("bytes", byte_count, self._limits.max_bytes)

    def _decode_operations(self, transaction: CommandTransaction) -> tuple[TypedOperation, ...]:
        decoded: list[TypedOperation] = []
        for index, command in enumerate(transaction.commands):
            try:
                decoded.append(
                    parse_operation(command, registry=self._operations, session=self._session)
                )
            except TransactionValidationError as error:
                details = dict(error.details)
                details.update(
                    {
                        "operation_index": index,
                        "command_id": command.command_id,
                        "operation": command.operation,
                    }
                )
                raise TransactionValidationError(
                    error.message,
                    code=error.code,
                    subsystem=error.subsystem,
                    phase=error.phase,
                    details=details,
                ) from error
            except Exception as error:
                cause_code = (
                    error.code if isinstance(error, LudoWeaveError) else type(error).__name__
                )
                raise TransactionValidationError(
                    "transaction operation could not be decoded",
                    code="world.transaction.validation_failed",
                    subsystem="world",
                    phase="validate",
                    details={
                        "operation_index": index,
                        "command_id": command.command_id,
                        "operation": command.operation,
                        "cause_code": cause_code,
                    },
                ) from error
        return tuple(decoded)

    def _validate_operation_sequence(self, operations: tuple[TypedOperation, ...]) -> None:
        aliases: set[str] = set()
        tick_indexes: list[int] = []
        total_ticks = 0
        for index, operation in enumerate(operations):
            target = (
                operation.target
                if isinstance(
                    operation,
                    (
                        DestroyOperation,
                        AddComponentOperation,
                        RemoveComponentOperation,
                        PatchComponentOperation,
                    ),
                )
                else None
            )
            if target is not None and target.alias is not None and target.alias not in aliases:
                raise TransactionValidationError(
                    "transaction-local entity aliases must refer to an earlier spawn",
                    code="world.transaction.validation_failed",
                    subsystem="world",
                    phase="validate",
                    details={"alias": target.alias, "operation_index": index},
                )
            if isinstance(operation, SpawnOperation) and operation.alias is not None:
                if operation.alias in aliases:
                    raise TransactionValidationError(
                        "transaction-local spawn aliases must be unique",
                        code="world.transaction.validation_failed",
                        subsystem="world",
                        phase="validate",
                        details={"alias": operation.alias, "operation_index": index},
                    )
                aliases.add(operation.alias)
            if isinstance(operation, TickOperation):
                tick_indexes.append(index)
                total_ticks += operation.count
        if len(aliases) > self._limits.max_aliases:
            raise _limit_error("aliases", len(aliases), self._limits.max_aliases)
        if len(tick_indexes) > 1 or (tick_indexes and tick_indexes[0] != len(operations) - 1):
            raise TransactionValidationError(
                "world.tick may appear at most once and must be the final operation",
                code="world.transaction.validation_failed",
                subsystem="world",
                phase="validate",
                details={"operation": "world.tick"},
            )
        if total_ticks > self._limits.max_ticks:
            raise _limit_error("ticks", total_ticks, self._limits.max_ticks)

    def _apply_operation(
        self,
        staged: _SessionRecord,
        operation: TypedOperation,
        aliases: dict[str, EntityId],
    ) -> _SessionRecord:
        world = staged.world
        if isinstance(operation, SpawnOperation):
            entity_id = world.spawn(*operation.components)
            if operation.alias is not None:
                aliases[operation.alias] = entity_id
            return staged
        if isinstance(operation, DestroyOperation):
            world.destroy(operation.target.resolve(aliases))
            return staged
        if isinstance(operation, AddComponentOperation):
            world.add(operation.target.resolve(aliases), operation.component)
            return staged
        if isinstance(operation, RemoveComponentOperation):
            world.remove(operation.target.resolve(aliases), operation.component_type)
            return staged
        if isinstance(operation, PatchComponentOperation):
            world.patch(
                operation.target.resolve(aliases),
                operation.component_type,
                **dict(operation.changes),
            )
            return staged
        if isinstance(operation, PatchResourceOperation):
            staged.resources.replace(operation.schema.spec, operation.value)
            return staged
        for _ in range(operation.count):
            staged = self._session._execute_tick(staged)
        return staged


def _limit_error(field: str, actual: int, limit: int) -> TransactionValidationError:
    return TransactionValidationError(
        "transaction exceeds a configured deterministic limit",
        code="world.transaction.limit_exceeded",
        subsystem="world",
        phase="validate",
        details={"field": field, "actual": actual, "limit": limit},
    )


def _application_error(
    message: str,
    *,
    operation_index: int | None,
    command_id: str | None,
    cause: Exception,
) -> TransactionApplicationError:
    cause_code = cause.code if isinstance(cause, LudoWeaveError) else type(cause).__name__
    return TransactionApplicationError(
        message,
        code="world.transaction.apply_failed",
        subsystem="world",
        phase="apply",
        details={
            "operation_index": operation_index,
            "command_id": command_id,
            "cause_code": cause_code,
        },
    )
