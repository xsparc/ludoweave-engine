"""Structured failures for persistent world protocols."""

from ludoweave.core.errors import LudoWeaveError


class WorldProtocolError(LudoWeaveError):
    """Base class for command, snapshot, hash, and replay failures."""


class CanonicalJsonError(WorldProtocolError):
    """Raised when input cannot participate in canonical JSON encoding."""


class CommandSchemaError(WorldProtocolError):
    """Raised when a persistent command document violates its schema."""


class ReceiptDecodeError(WorldProtocolError):
    """Raised when a receipt document violates its bounded wire schema."""


class IncompatibleReceiptError(ReceiptDecodeError):
    """Raised when a valid receipt document uses an unsupported protocol."""


class DuplicateOperationError(CommandSchemaError):
    """Raised when an operation registry contains a duplicate identity."""


class UnknownOperationError(CommandSchemaError):
    """Raised when a command names an unregistered operation version."""


class AuthorityError(WorldProtocolError):
    """Raised when authoritative session composition is invalid."""


class ResourceSchemaError(AuthorityError):
    """Raised for invalid persistent resource identity or codec behavior."""


class TransactionError(WorldProtocolError):
    """Base class for atomic transaction failures."""


class StaleWorldHashError(TransactionError):
    """Raised before staging when optimistic concurrency detects stale state."""


class TransactionValidationError(TransactionError):
    """Raised when a transaction cannot be applied to a target session."""


class TransactionApplicationError(TransactionError):
    """Raised when a fully decoded operation fails against staged state."""


class SnapshotError(WorldProtocolError):
    """Base class for canonical snapshot failures."""


class SnapshotDecodeError(SnapshotError):
    """Raised when snapshot bytes or logical invariants are malformed."""


class SnapshotCaptureError(SnapshotError):
    """Raised when a session cannot be captured at the current safe point."""


class IncompatibleSnapshotError(SnapshotError):
    """Raised when a valid snapshot targets incompatible engine schemas."""


class SnapshotHashMismatchError(SnapshotError):
    """Raised when declared and computed authoritative hashes differ."""


class ReplayError(WorldProtocolError):
    """Base class for replay recording, decoding, and execution failures."""


class ReplayDecodeError(ReplayError):
    """Raised when a replay document violates its bounded wire schema."""


class IncompatibleReplayError(ReplayError):
    """Raised when a replay targets a different engine/project composition."""


class ReplayDivergenceError(ReplayError):
    """Raised when replay execution differs from a recorded tick or hash."""


class ReplayBranchError(ReplayError):
    """Raised when a requested immutable branch point is not representable."""
