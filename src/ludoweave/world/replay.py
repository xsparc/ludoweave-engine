# pyright: reportPrivateUsage=false
"""Bounded deterministic replay, checkpoint, and immutable branch contracts."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.core.version import __version__
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps, canonical_loads
from ludoweave.world.command_schema import (
    CommandTransaction,
    OperationRegistry,
    builtin_operation_registry,
)
from ludoweave.world.errors import (
    IncompatibleReplayError,
    ReplayBranchError,
    ReplayDecodeError,
    ReplayDivergenceError,
    ReplayError,
    WorldProtocolError,
)
from ludoweave.world.receipt import ReceiptStatus, TransactionReceipt
from ludoweave.world.snapshot import SnapshotCodec
from ludoweave.world.state import TickExecutor, WorldSession
from ludoweave.world.transaction import TransactionLimits, TransactionService

REPLAY_PROTOCOL = "ludoweave.replay/1"
DETERMINISM_PROFILE = "D1"
_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+-]{0,127}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class ReplayLimits:
    """Whole-document and semantic bounds for replay codecs and recorders."""

    max_bytes: int = 134_217_728
    max_depth: int = 96
    max_nodes: int = 12_000_000
    max_collection_items: int = 4_000_000
    max_batches: int = 1_000_000
    max_checkpoints: int = 1_000_000
    max_snapshot_bytes: int = 67_108_864

    def __post_init__(self) -> None:
        for field in (
            "max_batches",
            "max_bytes",
            "max_checkpoints",
            "max_collection_items",
            "max_depth",
            "max_nodes",
            "max_snapshot_bytes",
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _replay_decode_error(
                    "replay limits must be positive integers",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )

    def json_limits(self) -> JsonLimits:
        return JsonLimits(
            max_bytes=self.max_bytes,
            max_depth=self.max_depth,
            max_nodes=self.max_nodes,
            max_collection_items=self.max_collection_items,
            max_string_bytes=min(self.max_bytes, 1_048_576),
        )


@dataclass(frozen=True, slots=True)
class ReplayParent:
    """Immutable reference to the complete parent timeline and branch boundary."""

    timeline_id: str
    timeline_hash: str
    after_batch: int
    tick: int
    state_hash: str

    def __post_init__(self) -> None:
        _stable_id(self.timeline_id, field="parent.timeline_id")
        _sha256(self.timeline_hash, field="parent.timeline_hash")
        _non_negative_int(self.after_batch, field="parent.after_batch")
        _non_negative_int(self.tick, field="parent.tick")
        _sha256(self.state_hash, field="parent.state_hash")

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "timeline_id": self.timeline_id,
            "timeline_hash": self.timeline_hash,
            "after_batch": self.after_batch,
            "tick": self.tick,
            "state_hash": self.state_hash,
        }


@dataclass(frozen=True, slots=True)
class ReplayHeader:
    """Compatibility and authority identity for one immutable timeline."""

    timeline_id: str
    world_id: str
    project_schema: str
    dependency_lock_hash: str
    platform_profile: str
    operation_fingerprint: str
    random_seed: str
    initial_tick: int
    initial_state_hash: str
    parent: ReplayParent | None = None
    engine_version: str = __version__
    determinism: str = DETERMINISM_PROFILE

    def __post_init__(self) -> None:
        _stable_id(self.timeline_id, field="header.timeline_id")
        _stable_id(self.world_id, field="header.world_id")
        _sha256(self.project_schema, field="header.project_schema")
        _sha256(self.dependency_lock_hash, field="header.dependency_lock_hash")
        _stable_id(self.platform_profile, field="header.platform_profile")
        _sha256(self.operation_fingerprint, field="header.operation_fingerprint")
        _hex_u64(self.random_seed, field="header.random_seed")
        _non_negative_int(self.initial_tick, field="header.initial_tick")
        _sha256(self.initial_state_hash, field="header.initial_state_hash")
        if self.engine_version != __version__:
            raise _incompatible_replay("replay engine version is incompatible", "engine_version")
        if self.determinism != DETERMINISM_PROFILE:
            raise _incompatible_replay("replay determinism profile is incompatible", "determinism")
        if self.parent is not None and (
            self.parent.tick != self.initial_tick
            or self.parent.state_hash != self.initial_state_hash
        ):
            raise _replay_decode_error(
                "branch parent does not identify the initial replay state",
                phase="validate",
                details={"field": "header.parent"},
            )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "timeline_id": self.timeline_id,
            "world_id": self.world_id,
            "project_schema": self.project_schema,
            "dependency_lock_hash": self.dependency_lock_hash,
            "platform_profile": self.platform_profile,
            "operation_fingerprint": self.operation_fingerprint,
            "random_seed": self.random_seed,
            "initial_tick": self.initial_tick,
            "initial_state_hash": self.initial_state_hash,
            "parent": None if self.parent is None else self.parent.as_dict(),
            "engine_version": self.engine_version,
            "determinism": self.determinism,
        }


@dataclass(frozen=True, slots=True)
class ReplayBatch:
    """One committed transaction at an exact completed-tick boundary."""

    index: int
    start_tick: int
    end_tick: int
    pre_hash: str
    post_hash: str
    transaction: CommandTransaction

    def __post_init__(self) -> None:
        _non_negative_int(self.index, field="batch.index")
        _non_negative_int(self.start_tick, field="batch.start_tick")
        _non_negative_int(self.end_tick, field="batch.end_tick")
        if self.end_tick < self.start_tick:
            raise _replay_decode_error(
                "replay batch cannot move completed ticks backward",
                phase="validate",
                details={"batch": self.index},
            )
        _sha256(self.pre_hash, field="batch.pre_hash")
        _sha256(self.post_hash, field="batch.post_hash")
        if self.transaction.dry_run:
            raise _replay_decode_error(
                "replay batches must contain committed transactions",
                phase="validate",
                details={"batch": self.index},
            )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "index": self.index,
            "start_tick": self.start_tick,
            "end_tick": self.end_tick,
            "pre_hash": self.pre_hash,
            "post_hash": self.post_hash,
            "transaction": self.transaction.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class ReplayCheckpoint:
    """Recorded authority hash after exactly ``after_batch`` batches."""

    after_batch: int
    tick: int
    state_hash: str

    def __post_init__(self) -> None:
        _non_negative_int(self.after_batch, field="checkpoint.after_batch")
        _non_negative_int(self.tick, field="checkpoint.tick")
        _sha256(self.state_hash, field="checkpoint.state_hash")

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "after_batch": self.after_batch,
            "tick": self.tick,
            "state_hash": self.state_hash,
        }


@dataclass(frozen=True, slots=True)
class ReplayTimeline:
    """One self-contained initial snapshot plus ordered committed batches."""

    header: ReplayHeader
    initial_snapshot: bytes
    batches: tuple[ReplayBatch, ...]
    checkpoints: tuple[ReplayCheckpoint, ...]
    protocol: str = REPLAY_PROTOCOL

    def __post_init__(self) -> None:
        if self.protocol != REPLAY_PROTOCOL:
            raise _incompatible_replay("replay protocol is incompatible", "protocol")
        if type(self.initial_snapshot) is not bytes or not self.initial_snapshot:
            raise _replay_decode_error(
                "replay initial snapshot must contain canonical bytes",
                phase="validate",
                details={"field": "initial_snapshot"},
            )
        batches = tuple(self.batches)
        checkpoints = tuple(self.checkpoints)
        expected_tick = self.header.initial_tick
        expected_hash = self.header.initial_state_hash
        transaction_ids: set[str] = set()
        for expected_index, batch in enumerate(batches):
            if batch.index != expected_index:
                raise _replay_decode_error(
                    "replay batch indexes must be contiguous",
                    phase="validate",
                    details={"batch": expected_index},
                )
            if batch.start_tick != expected_tick or batch.pre_hash != expected_hash:
                raise _replay_decode_error(
                    "replay batch tick/hash chain contains a gap",
                    phase="validate",
                    details={"batch": expected_index},
                )
            if batch.transaction.world_id != self.header.world_id:
                raise _replay_decode_error(
                    "replay transaction targets a different world",
                    phase="validate",
                    details={"batch": expected_index},
                )
            if batch.transaction.transaction_id in transaction_ids:
                raise _replay_decode_error(
                    "replay transaction IDs must be unique",
                    phase="validate",
                    details={"batch": expected_index},
                )
            transaction_ids.add(batch.transaction.transaction_id)
            expected_tick = batch.end_tick
            expected_hash = batch.post_hash

        checkpoint_positions: set[int] = set()
        for checkpoint in checkpoints:
            if checkpoint.after_batch in checkpoint_positions:
                raise _replay_decode_error(
                    "replay checkpoint positions must be unique",
                    phase="validate",
                    details={"after_batch": checkpoint.after_batch},
                )
            checkpoint_positions.add(checkpoint.after_batch)
            if checkpoint.after_batch > len(batches):
                raise _replay_decode_error(
                    "replay checkpoint is outside the timeline",
                    phase="validate",
                    details={"after_batch": checkpoint.after_batch},
                )
            if checkpoint.after_batch == 0:
                tick = self.header.initial_tick
                state_hash = self.header.initial_state_hash
            else:
                boundary = batches[checkpoint.after_batch - 1]
                tick = boundary.end_tick
                state_hash = boundary.post_hash
            if checkpoint.tick != tick or checkpoint.state_hash != state_hash:
                raise _replay_decode_error(
                    "replay checkpoint disagrees with its batch boundary",
                    phase="validate",
                    details={"after_batch": checkpoint.after_batch},
                )
        object.__setattr__(self, "batches", batches)
        object.__setattr__(
            self, "checkpoints", tuple(sorted(checkpoints, key=lambda item: item.after_batch))
        )

    @property
    def final_tick(self) -> int:
        return self.batches[-1].end_tick if self.batches else self.header.initial_tick

    @property
    def final_state_hash(self) -> str:
        return self.batches[-1].post_hash if self.batches else self.header.initial_state_hash

    def as_dict(self, *, limits: ReplayLimits | None = None) -> dict[str, JsonValue]:
        checked_limits = limits or ReplayLimits()
        try:
            snapshot = canonical_loads(self.initial_snapshot, limits=checked_limits.json_limits())
        except WorldProtocolError as error:
            raise _replay_decode_error(
                "replay initial snapshot bytes are malformed",
                phase="encode",
                details={"cause_code": error.code},
            ) from error
        return {
            "protocol": self.protocol,
            "header": self.header.as_dict(),
            "initial_snapshot": snapshot,
            "batches": [batch.as_dict() for batch in self.batches],
            "checkpoints": [checkpoint.as_dict() for checkpoint in self.checkpoints],
        }

    def canonical_bytes(self, *, limits: ReplayLimits | None = None) -> bytes:
        checked_limits = limits or ReplayLimits()
        if len(self.batches) > checked_limits.max_batches:
            raise _replay_limit("batches", len(self.batches), checked_limits.max_batches)
        if len(self.checkpoints) > checked_limits.max_checkpoints:
            raise _replay_limit(
                "checkpoints", len(self.checkpoints), checked_limits.max_checkpoints
            )
        if len(self.initial_snapshot) > checked_limits.max_snapshot_bytes:
            raise _replay_limit(
                "initial_snapshot_bytes",
                len(self.initial_snapshot),
                checked_limits.max_snapshot_bytes,
            )
        return canonical_dumps(
            self.as_dict(limits=checked_limits), limits=checked_limits.json_limits()
        )

    def timeline_hash(self, *, limits: ReplayLimits | None = None) -> str:
        return f"sha256:{sha256(self.canonical_bytes(limits=limits)).hexdigest()}"

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: ReplayLimits | None = None,
    ) -> ReplayTimeline:
        checked_limits = limits or ReplayLimits()
        try:
            decoded = canonical_loads(document, limits=checked_limits.json_limits())
            return _decode_timeline(decoded, limits=checked_limits)
        except ReplayError:
            raise
        except LudoWeaveError as error:
            raise _replay_decode_error(
                "replay document contains an invalid nested protocol value",
                phase="decode",
                details={"cause_code": error.code},
            ) from error


@dataclass(frozen=True, slots=True)
class ReplayResult:
    """Successful replay result and exact checkpoints verified during execution."""

    session: WorldSession
    batches_applied: int
    verified_checkpoints: tuple[ReplayCheckpoint, ...]


class ReplayRecorder:
    """Single-owner recorder that applies and appends only committed batches."""

    __slots__ = (
        "_batches",
        "_checkpoint_interval",
        "_checkpoints",
        "_header",
        "_initial_snapshot",
        "_limits",
        "_service",
    )

    def __init__(
        self,
        session: WorldSession,
        snapshot_codec: SnapshotCodec,
        *,
        timeline_id: str,
        project_schema: str,
        dependency_lock_hash: str,
        platform_profile: str,
        operations: OperationRegistry | None = None,
        transaction_limits: TransactionLimits | None = None,
        replay_limits: ReplayLimits | None = None,
        checkpoint_interval: int | None = 1,
        parent: ReplayParent | None = None,
    ) -> None:
        if checkpoint_interval is not None and (
            type(checkpoint_interval) is not int or checkpoint_interval <= 0
        ):
            raise _replay_decode_error(
                "checkpoint interval must be a positive integer or null",
                phase="configure",
                details={"field": "checkpoint_interval"},
            )
        checked_operations = operations or builtin_operation_registry()
        self._limits = replay_limits or ReplayLimits()
        self._service = TransactionService(
            session,
            operations=checked_operations,
            limits=transaction_limits,
        )
        self._initial_snapshot = snapshot_codec.encode(session)
        self._header = ReplayHeader(
            timeline_id=timeline_id,
            world_id=session.world_id,
            project_schema=project_schema,
            dependency_lock_hash=dependency_lock_hash,
            platform_profile=platform_profile,
            operation_fingerprint=checked_operations.fingerprint,
            random_seed=f"{session.random_seed:016x}",
            initial_tick=session.completed_ticks,
            initial_state_hash=session.state_hash,
            parent=parent,
        )
        self._batches: list[ReplayBatch] = []
        self._checkpoints: list[ReplayCheckpoint] = [
            ReplayCheckpoint(0, session.completed_ticks, session.state_hash)
        ]
        self._checkpoint_interval = checkpoint_interval
        self.timeline().canonical_bytes(limits=self._limits)

    @property
    def session(self) -> WorldSession:
        return self._service.session

    def record(self, transaction: CommandTransaction) -> TransactionReceipt:
        """Apply one transaction and append its exact committed result."""

        if transaction.dry_run:
            raise _replay_record_error(
                "dry-run transactions cannot enter a replay timeline",
                details={"transaction_id": transaction.transaction_id},
            )
        if len(self._batches) >= self._limits.max_batches:
            raise _replay_limit("batches", len(self._batches) + 1, self._limits.max_batches)
        expected_tick, expected_hash = self._current_boundary()
        if (
            self.session.completed_ticks != expected_tick
            or self.session.state_hash != expected_hash
        ):
            raise _replay_record_error(
                "authoritative state changed outside the replay recorder",
                details={"timeline_id": self._header.timeline_id},
            )
        if transaction.world_id != self._header.world_id:
            return self._service.apply(transaction)
        self._preflight_append(transaction, expected_tick, expected_hash)

        receipt = self._service.apply(transaction)
        if receipt.status is not ReceiptStatus.COMMITTED:
            return receipt
        batch = ReplayBatch(
            index=len(self._batches),
            start_tick=receipt.completed_ticks_before,
            end_tick=receipt.completed_ticks_after,
            pre_hash=receipt.pre_hash,
            post_hash=receipt.post_hash,
            transaction=transaction,
        )
        self._batches.append(batch)
        if (
            self._checkpoint_interval is not None
            and len(self._batches) % self._checkpoint_interval == 0
        ):
            self._checkpoints.append(
                ReplayCheckpoint(len(self._batches), batch.end_tick, batch.post_hash)
            )
        self.timeline().canonical_bytes(limits=self._limits)
        return receipt

    def checkpoint(self) -> ReplayCheckpoint:
        """Add or return the checkpoint at the recorder's current boundary."""

        tick, state_hash = self._current_boundary()
        after_batch = len(self._batches)
        if self._checkpoints and self._checkpoints[-1].after_batch == after_batch:
            return self._checkpoints[-1]
        if len(self._checkpoints) >= self._limits.max_checkpoints:
            raise _replay_limit(
                "checkpoints", len(self._checkpoints) + 1, self._limits.max_checkpoints
            )
        checkpoint = ReplayCheckpoint(after_batch, tick, state_hash)
        ReplayTimeline(
            self._header,
            self._initial_snapshot,
            tuple(self._batches),
            (*self._checkpoints, checkpoint),
        ).canonical_bytes(limits=self._limits)
        self._checkpoints.append(checkpoint)
        return checkpoint

    def timeline(self) -> ReplayTimeline:
        return ReplayTimeline(
            self._header,
            self._initial_snapshot,
            tuple(self._batches),
            tuple(self._checkpoints),
        )

    def _current_boundary(self) -> tuple[int, str]:
        if self._batches:
            batch = self._batches[-1]
            return batch.end_tick, batch.post_hash
        return self._header.initial_tick, self._header.initial_state_hash

    def _preflight_append(
        self,
        transaction: CommandTransaction,
        start_tick: int,
        pre_hash: str,
    ) -> None:
        """Conservatively bound the future canonical record before commit."""

        index = len(self._batches)
        maximum_tick = 2**63 - 1
        placeholder_hash = "sha256:" + "0" * 64
        projected_batch = ReplayBatch(
            index,
            start_tick,
            maximum_tick,
            pre_hash,
            placeholder_hash,
            transaction,
        )
        checkpoints = list(self._checkpoints)
        if self._checkpoint_interval is not None and (index + 1) % self._checkpoint_interval == 0:
            if len(checkpoints) >= self._limits.max_checkpoints:
                raise _replay_limit(
                    "checkpoints", len(checkpoints) + 1, self._limits.max_checkpoints
                )
            checkpoints.append(ReplayCheckpoint(index + 1, maximum_tick, placeholder_hash))
        ReplayTimeline(
            self._header,
            self._initial_snapshot,
            (*self._batches, projected_batch),
            tuple(checkpoints),
        ).canonical_bytes(limits=self._limits)


class ReplayRunner:
    """Composition-owned decoder, verifier, and immutable branch factory."""

    __slots__ = (
        "_dependency_lock_hash",
        "_limits",
        "_operations",
        "_platform_profile",
        "_project_schema",
        "_snapshot_codec",
        "_transaction_limits",
    )

    def __init__(
        self,
        snapshot_codec: SnapshotCodec,
        *,
        project_schema: str,
        dependency_lock_hash: str,
        platform_profile: str,
        operations: OperationRegistry | None = None,
        transaction_limits: TransactionLimits | None = None,
        replay_limits: ReplayLimits | None = None,
    ) -> None:
        self._snapshot_codec = snapshot_codec
        self._project_schema = _sha256(project_schema, field="project_schema")
        self._dependency_lock_hash = _sha256(dependency_lock_hash, field="dependency_lock_hash")
        self._platform_profile = _stable_id(platform_profile, field="platform_profile")
        self._operations = operations or builtin_operation_registry()
        self._transaction_limits = transaction_limits
        self._limits = replay_limits or ReplayLimits()

    def decode(self, document: str | bytes) -> ReplayTimeline:
        timeline = ReplayTimeline.from_json(document, limits=self._limits)
        self._require_compatible(timeline.header)
        return timeline

    def replay(
        self,
        timeline: ReplayTimeline | str | bytes,
        *,
        tick_executor: TickExecutor | None = None,
        verify_hashes: bool = True,
        max_batches: int | None = None,
    ) -> ReplayResult:
        """Replay from the embedded snapshot and verify every reached checkpoint."""

        checked = self.decode(timeline) if isinstance(timeline, (str, bytes)) else timeline
        self._require_compatible(checked.header)
        checked.canonical_bytes(limits=self._limits)
        if max_batches is None:
            batch_count = len(checked.batches)
        else:
            if (
                type(max_batches) is not int
                or max_batches < 0
                or max_batches > len(checked.batches)
            ):
                raise _replay_decode_error(
                    "replay batch prefix is outside the timeline",
                    phase="configure",
                    details={"field": "max_batches"},
                )
            batch_count = max_batches

        session = self._snapshot_codec.decode(
            checked.initial_snapshot,
            tick_executor=tick_executor,
        )
        if (
            session.world_id != checked.header.world_id
            or session.completed_ticks != checked.header.initial_tick
            or session.state_hash != checked.header.initial_state_hash
            or f"{session.random_seed:016x}" != checked.header.random_seed
        ):
            raise _replay_divergence(
                "initial snapshot does not reproduce the replay header",
                batch=None,
                field="initial_snapshot",
                tick=session.completed_ticks,
                expected=checked.header.initial_state_hash,
                actual=session.state_hash,
            )

        checkpoints = {item.after_batch: item for item in checked.checkpoints}
        verified: list[ReplayCheckpoint] = []
        initial_checkpoint = checkpoints.get(0)
        if initial_checkpoint is not None and verify_hashes:
            self._verify_checkpoint(initial_checkpoint, session, batch=0)
            verified.append(initial_checkpoint)

        service = TransactionService(
            session,
            operations=self._operations,
            limits=self._transaction_limits,
        )
        for batch in checked.batches[:batch_count]:
            if session.completed_ticks != batch.start_tick:
                raise _replay_divergence(
                    "replay reached an unexpected tick boundary",
                    batch=batch.index,
                    field="start_tick",
                    tick=session.completed_ticks,
                    expected=batch.start_tick,
                    actual=session.completed_ticks,
                )
            if verify_hashes and session.state_hash != batch.pre_hash:
                raise _replay_divergence(
                    "replay pre-state hash diverged",
                    batch=batch.index,
                    field="pre_hash",
                    tick=session.completed_ticks,
                    expected=batch.pre_hash,
                    actual=session.state_hash,
                )
            receipt = service.apply(batch.transaction)
            if receipt.status is not ReceiptStatus.COMMITTED:
                cause = receipt.diagnostics[0].code if receipt.diagnostics else "unknown"
                raise _replay_divergence(
                    "recorded transaction was rejected during replay",
                    batch=batch.index,
                    field="status",
                    tick=session.completed_ticks,
                    expected="committed",
                    actual=f"rejected:{cause}",
                )
            if receipt.completed_ticks_after != batch.end_tick:
                raise _replay_divergence(
                    "replay completed-tick count diverged",
                    batch=batch.index,
                    field="end_tick",
                    tick=session.completed_ticks,
                    expected=batch.end_tick,
                    actual=receipt.completed_ticks_after,
                )
            if verify_hashes and receipt.post_hash != batch.post_hash:
                raise _replay_divergence(
                    "replay post-state hash diverged",
                    batch=batch.index,
                    field="post_hash",
                    tick=session.completed_ticks,
                    expected=batch.post_hash,
                    actual=receipt.post_hash,
                )
            checkpoint = checkpoints.get(batch.index + 1)
            if checkpoint is not None and verify_hashes:
                self._verify_checkpoint(checkpoint, session, batch=batch.index)
                verified.append(checkpoint)
        return ReplayResult(session, batch_count, tuple(verified))

    def branch(
        self,
        parent: ReplayTimeline | str | bytes,
        *,
        at_tick: int,
        timeline_id: str,
        tick_executor: TickExecutor | None = None,
        checkpoint_interval: int | None = 1,
    ) -> ReplayRecorder:
        """Create a self-contained child timeline after all parent work at a tick."""

        checked = self.decode(parent) if isinstance(parent, (str, bytes)) else parent
        self._require_compatible(checked.header)
        after_batch = self._boundary_after_tick(checked, at_tick)
        result = self.replay(
            checked,
            tick_executor=tick_executor,
            max_batches=after_batch,
        )
        parent_reference = ReplayParent(
            timeline_id=checked.header.timeline_id,
            timeline_hash=checked.timeline_hash(limits=self._limits),
            after_batch=after_batch,
            tick=at_tick,
            state_hash=result.session.state_hash,
        )
        return ReplayRecorder(
            result.session,
            self._snapshot_codec,
            timeline_id=timeline_id,
            project_schema=self._project_schema,
            dependency_lock_hash=self._dependency_lock_hash,
            platform_profile=self._platform_profile,
            operations=self._operations,
            transaction_limits=self._transaction_limits,
            replay_limits=self._limits,
            checkpoint_interval=checkpoint_interval,
            parent=parent_reference,
        )

    def replay_branch(
        self,
        branch: ReplayTimeline | str | bytes,
        parent: ReplayTimeline | str | bytes,
        *,
        tick_executor: TickExecutor | None = None,
        verify_hashes: bool = True,
    ) -> ReplayResult:
        """Verify immutable parent lineage, then replay the child timeline."""

        child = self.decode(branch) if isinstance(branch, (str, bytes)) else branch
        parent_timeline = self.decode(parent) if isinstance(parent, (str, bytes)) else parent
        self._require_compatible(child.header)
        self._require_compatible(parent_timeline.header)
        reference = child.header.parent
        if reference is None:
            raise _invalid_branch("timeline has no parent reference", field="parent")
        actual_parent_hash = parent_timeline.timeline_hash(limits=self._limits)
        if (
            reference.timeline_id != parent_timeline.header.timeline_id
            or reference.timeline_hash != actual_parent_hash
        ):
            raise _invalid_branch("parent timeline identity or hash differs", field="parent_hash")
        if reference.after_batch > len(parent_timeline.batches):
            raise _invalid_branch(
                "parent batch boundary is outside the timeline", field="after_batch"
            )
        parent_result = self.replay(
            parent_timeline,
            tick_executor=tick_executor,
            verify_hashes=verify_hashes,
            max_batches=reference.after_batch,
        )
        if (
            parent_result.session.completed_ticks != reference.tick
            or parent_result.session.state_hash != reference.state_hash
        ):
            raise _invalid_branch(
                "parent does not reproduce the branch boundary", field="state_hash"
            )
        return self.replay(
            child,
            tick_executor=tick_executor,
            verify_hashes=verify_hashes,
        )

    def replay_to_tick(
        self,
        timeline: ReplayTimeline | str | bytes,
        *,
        at_tick: int,
        tick_executor: TickExecutor | None = None,
        verify_hashes: bool = True,
    ) -> ReplayResult:
        """Replay through all recorded work at one exact tick boundary."""

        checked = self.decode(timeline) if isinstance(timeline, (str, bytes)) else timeline
        self._require_compatible(checked.header)
        after_batch = self._boundary_after_tick(checked, at_tick)
        return self.replay(
            checked,
            tick_executor=tick_executor,
            verify_hashes=verify_hashes,
            max_batches=after_batch,
        )

    def _require_compatible(self, header: ReplayHeader) -> None:
        checks = (
            (header.project_schema, self._project_schema, "project_schema"),
            (
                header.dependency_lock_hash,
                self._dependency_lock_hash,
                "dependency_lock_hash",
            ),
            (header.platform_profile, self._platform_profile, "platform_profile"),
            (
                header.operation_fingerprint,
                self._operations.fingerprint,
                "operation_fingerprint",
            ),
        )
        for actual, expected, field in checks:
            if actual != expected:
                raise _incompatible_replay("replay composition is incompatible", field)

    @staticmethod
    def _boundary_after_tick(timeline: ReplayTimeline, at_tick: int) -> int:
        _non_negative_int(at_tick, field="at_tick")
        matching = [0] if timeline.header.initial_tick == at_tick else []
        matching.extend(batch.index + 1 for batch in timeline.batches if batch.end_tick == at_tick)
        if not matching:
            raise ReplayBranchError(
                "tick is not a recorded transaction boundary",
                code="world.replay.invalid_branch",
                subsystem="world",
                phase="branch",
                details={"tick": at_tick},
            )
        return max(matching)

    @staticmethod
    def _verify_checkpoint(
        checkpoint: ReplayCheckpoint,
        session: WorldSession,
        *,
        batch: int,
    ) -> None:
        if (
            checkpoint.tick != session.completed_ticks
            or checkpoint.state_hash != session.state_hash
        ):
            raise _replay_divergence(
                "replay checkpoint hash or tick diverged",
                batch=batch,
                field="checkpoint",
                tick=session.completed_ticks,
                expected=f"{checkpoint.tick}|{checkpoint.state_hash}",
                actual=f"{session.completed_ticks}|{session.state_hash}",
            )


def _decode_timeline(value: object, *, limits: ReplayLimits) -> ReplayTimeline:
    document = _object(value, role="replay")
    _exact_fields(
        document,
        required={"protocol", "header", "initial_snapshot", "batches", "checkpoints"},
        role="replay",
    )
    protocol = _text(document["protocol"], field="protocol")
    if protocol != REPLAY_PROTOCOL:
        raise _incompatible_replay("replay protocol is incompatible", "protocol")
    header = _decode_header(document["header"])
    batch_values = _array(document["batches"], role="batches")
    checkpoint_values = _array(document["checkpoints"], role="checkpoints")
    if len(batch_values) > limits.max_batches:
        raise _replay_limit("batches", len(batch_values), limits.max_batches)
    if len(checkpoint_values) > limits.max_checkpoints:
        raise _replay_limit("checkpoints", len(checkpoint_values), limits.max_checkpoints)
    snapshot_value = _object(document["initial_snapshot"], role="initial_snapshot")
    snapshot_bytes = canonical_dumps(snapshot_value, limits=limits.json_limits())
    if len(snapshot_bytes) > limits.max_snapshot_bytes:
        raise _replay_limit(
            "initial_snapshot_bytes", len(snapshot_bytes), limits.max_snapshot_bytes
        )
    batches = tuple(_decode_batch(item) for item in batch_values)
    checkpoints = tuple(_decode_checkpoint(item) for item in checkpoint_values)
    return ReplayTimeline(header, snapshot_bytes, batches, checkpoints, protocol)


def _decode_header(value: object) -> ReplayHeader:
    document = _object(value, role="header")
    _exact_fields(
        document,
        required={
            "timeline_id",
            "world_id",
            "project_schema",
            "dependency_lock_hash",
            "platform_profile",
            "operation_fingerprint",
            "random_seed",
            "initial_tick",
            "initial_state_hash",
            "parent",
            "engine_version",
            "determinism",
        },
        role="header",
    )
    parent_value = document["parent"]
    parent = None if parent_value is None else _decode_parent(parent_value)
    return ReplayHeader(
        timeline_id=_text(document["timeline_id"], field="header.timeline_id"),
        world_id=_text(document["world_id"], field="header.world_id"),
        project_schema=_text(document["project_schema"], field="header.project_schema"),
        dependency_lock_hash=_text(
            document["dependency_lock_hash"], field="header.dependency_lock_hash"
        ),
        platform_profile=_text(document["platform_profile"], field="header.platform_profile"),
        operation_fingerprint=_text(
            document["operation_fingerprint"], field="header.operation_fingerprint"
        ),
        random_seed=_text(document["random_seed"], field="header.random_seed"),
        initial_tick=_non_negative_int(document["initial_tick"], field="header.initial_tick"),
        initial_state_hash=_text(document["initial_state_hash"], field="header.initial_state_hash"),
        parent=parent,
        engine_version=_text(document["engine_version"], field="header.engine_version"),
        determinism=_text(document["determinism"], field="header.determinism"),
    )


def _decode_parent(value: object) -> ReplayParent:
    document = _object(value, role="parent")
    _exact_fields(
        document,
        required={"timeline_id", "timeline_hash", "after_batch", "tick", "state_hash"},
        role="parent",
    )
    return ReplayParent(
        timeline_id=_text(document["timeline_id"], field="parent.timeline_id"),
        timeline_hash=_text(document["timeline_hash"], field="parent.timeline_hash"),
        after_batch=_non_negative_int(document["after_batch"], field="parent.after_batch"),
        tick=_non_negative_int(document["tick"], field="parent.tick"),
        state_hash=_text(document["state_hash"], field="parent.state_hash"),
    )


def _decode_batch(value: object) -> ReplayBatch:
    document = _object(value, role="batch")
    _exact_fields(
        document,
        required={"index", "start_tick", "end_tick", "pre_hash", "post_hash", "transaction"},
        role="batch",
    )
    try:
        transaction = CommandTransaction.from_mapping(document["transaction"])
    except LudoWeaveError as error:
        raise _replay_decode_error(
            "replay batch contains an invalid transaction",
            phase="decode",
            details={"cause_code": error.code},
        ) from error
    return ReplayBatch(
        index=_non_negative_int(document["index"], field="batch.index"),
        start_tick=_non_negative_int(document["start_tick"], field="batch.start_tick"),
        end_tick=_non_negative_int(document["end_tick"], field="batch.end_tick"),
        pre_hash=_text(document["pre_hash"], field="batch.pre_hash"),
        post_hash=_text(document["post_hash"], field="batch.post_hash"),
        transaction=transaction,
    )


def _decode_checkpoint(value: object) -> ReplayCheckpoint:
    document = _object(value, role="checkpoint")
    _exact_fields(
        document,
        required={"after_batch", "tick", "state_hash"},
        role="checkpoint",
    )
    return ReplayCheckpoint(
        after_batch=_non_negative_int(document["after_batch"], field="checkpoint.after_batch"),
        tick=_non_negative_int(document["tick"], field="checkpoint.tick"),
        state_hash=_text(document["state_hash"], field="checkpoint.state_hash"),
    )


def _exact_fields(value: Mapping[str, object], *, required: set[str], role: str) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required)
    if missing or unexpected:
        raise _replay_decode_error(
            "replay object fields do not match its schema",
            phase="decode",
            details={
                "role": role,
                "missing": ",".join(missing),
                "unexpected": ",".join(unexpected),
            },
        )


def _object(value: object, *, role: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise _replay_decode_error(
            "replay value must be an object",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, JsonValue], value)


def _array(value: object, *, role: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise _replay_decode_error(
            "replay value must be an array",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(list[JsonValue], value)


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _replay_decode_error(
            "replay field has an invalid type",
            phase="decode",
            details={"field": field, "expected": "string"},
        )
    return value


def _non_negative_int(value: object, *, field: str) -> int:
    if type(value) is not int or value < 0 or value > 2**63 - 1:
        raise _replay_decode_error(
            "replay field must be a non-negative signed 64-bit integer",
            phase="decode",
            details={"field": field},
        )
    return value


def _stable_id(value: object, *, field: str) -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _replay_decode_error(
            "replay identity must use bounded stable text",
            phase="validate",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _sha256(value: object, *, field: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise _replay_decode_error(
            "replay hash must use canonical SHA-256 text",
            phase="validate",
            details={"field": field},
        )
    return value


def _hex_u64(value: object, *, field: str) -> str:
    if (
        type(value) is not str
        or len(value) != 16
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise _replay_decode_error(
            "replay random seed must use fixed-width unsigned hexadecimal text",
            phase="validate",
            details={"field": field},
        )
    return value


def _replay_limit(field: str, actual: int, limit: int) -> ReplayDecodeError:
    return ReplayDecodeError(
        "replay exceeds a configured deterministic limit",
        code="world.replay.oversized",
        subsystem="world",
        phase="validate",
        details={"field": field, "actual": actual, "limit": limit},
    )


def _replay_decode_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> ReplayDecodeError:
    return ReplayDecodeError(
        message,
        code="world.replay.malformed",
        subsystem="world",
        phase=phase,
        details=details,
    )


def _incompatible_replay(message: str, field: str) -> IncompatibleReplayError:
    return IncompatibleReplayError(
        message,
        code="world.replay.incompatible",
        subsystem="world",
        phase="compatibility",
        details={"field": field},
    )


def _replay_record_error(
    message: str,
    *,
    details: dict[str, str | int | float | bool | None],
) -> ReplayError:
    return ReplayError(
        message,
        code="world.replay.record_failed",
        subsystem="world",
        phase="record",
        details=details,
    )


def _replay_divergence(
    message: str,
    *,
    batch: int | None,
    field: str,
    tick: int,
    expected: str | int,
    actual: str | int,
) -> ReplayDivergenceError:
    return ReplayDivergenceError(
        message,
        code="world.replay.diverged",
        subsystem="world",
        phase="replay",
        details={
            "batch": batch,
            "tick": tick,
            "field": field,
            "expected": expected,
            "actual": actual,
        },
    )


def _invalid_branch(message: str, *, field: str) -> ReplayBranchError:
    return ReplayBranchError(
        message,
        code="world.replay.invalid_branch",
        subsystem="world",
        phase="branch",
        details={"field": field},
    )
