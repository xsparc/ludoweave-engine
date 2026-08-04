"""Canonical transaction receipts and sanitized diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.world.canonical import JsonValue, canonical_dumps
from ludoweave.world.command_schema import CommandActor, CommandTransaction
from ludoweave.world.diff import SemanticDiff

RECEIPT_PROTOCOL = "ludoweave.receipt/1"


class ReceiptStatus(StrEnum):
    COMMITTED = "committed"
    DRY_RUN = "dry_run"
    REJECTED = "rejected"


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

    def canonical_bytes(self) -> bytes:
        return canonical_dumps(self.as_dict())


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
