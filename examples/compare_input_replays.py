"""Compare two verified Clockwork Arena recordings without a renderer."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from ludoweave.app import InputSnapshot, RecordedInputSource
from ludoweave.app.replay import InputReplay
from ludoweave.core.errors import LudoWeaveError
from ludoweave.samples import create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
)
from ludoweave.world import (
    IncompatibleReplayError,
    ReceiptStatus,
    ReplayBatch,
    ReplayRunner,
    TransactionService,
    WorldSession,
    semantic_diff,
)
from ludoweave.world.canonical import JsonValue, canonical_dumps

_MAX_BYTES = 67_108_864
_MAX_HISTORY = 3600
_DETAIL_NODES = 128
_DETAIL_TEXT = 128


@dataclass(frozen=True, slots=True)
class _Admission:
    artifact: InputReplay | None
    content_hash: str | None
    artifact_hash: str | None
    status: str
    error: str | None = None

    def document(self) -> dict[str, JsonValue]:
        return {
            "content_hash": self.content_hash,
            "artifact_hash": self.artifact_hash,
            "verification": self.status,
            "error": self.error,
        }


def _runner() -> ReplayRunner:
    composition = create_clockwork_arena(RecordedInputSource())
    return ReplayRunner(
        composition.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )


def _admit(data: bytes | None) -> _Admission:
    if data is None:
        return _Admission(None, None, None, "invalid", "read_failure")
    if len(data) > _MAX_BYTES:
        return _Admission(None, None, None, "invalid", "byte_limit")
    content_hash = "sha256:" + sha256(data).hexdigest()
    artifact: InputReplay | None = None
    artifact_hash: str | None = None
    try:
        artifact = InputReplay.from_json(data)
        artifact_hash = artifact.artifact_hash()
        if len(artifact.snapshots) > _MAX_HISTORY or len(artifact.timeline.batches) > _MAX_HISTORY:
            return _Admission(artifact, content_hash, artifact_hash, "invalid", "history_limit")
        # Never let an early difference hide corruption later in either file.
        artifact.replay(_runner(), ArenaTickExecutor)
    except IncompatibleReplayError:
        return _Admission(artifact, content_hash, artifact_hash, "incompatible", "composition")
    except LudoWeaveError:
        return _Admission(artifact, content_hash, artifact_hash, "invalid", "artifact_validation")
    return _Admission(artifact, content_hash, artifact_hash, "pass")


def _bounded(value: JsonValue) -> dict[str, JsonValue]:
    """Limit the entire detail tree, not each individual collection independently."""
    remaining = _DETAIL_NODES
    truncated = False

    def visit(item: JsonValue) -> JsonValue:
        nonlocal remaining, truncated
        remaining -= 1
        if isinstance(item, str):
            truncated |= len(item) > _DETAIL_TEXT
            return item[:_DETAIL_TEXT]
        if isinstance(item, (list, dict)):
            values = list(item.items()) if isinstance(item, dict) else list(enumerate(item))
            result: dict[str, JsonValue] = {}
            array: list[JsonValue] = []
            for key, child in values:
                if remaining == 0:
                    truncated = True
                    break
                clipped = visit(child)
                if isinstance(item, dict):
                    text = str(key)
                    truncated |= len(text) > _DETAIL_TEXT
                    result[text[:_DETAIL_TEXT]] = clipped
                else:
                    array.append(clipped)
            return result if isinstance(item, dict) else array
        return item

    detail = visit(value)
    return {
        "value": detail,
        "truncated": truncated,
        "node_limit": _DETAIL_NODES,
        "text_limit": _DETAIL_TEXT,
    }


def _input_document(snapshot: InputSnapshot) -> dict[str, JsonValue]:
    return {
        "actions": {action.name: action.value for action in snapshot.actions},
        "just_pressed": list(snapshot.just_pressed_actions),
        "just_released": list(snapshot.just_released_actions),
    }


def _advance(service: TransactionService, batch: ReplayBatch) -> bool:
    session = service.session
    if session.completed_ticks != batch.start_tick or session.state_hash != batch.pre_hash:
        return False
    receipt = service.apply(batch.transaction)
    return (
        receipt.status is ReceiptStatus.COMMITTED
        and receipt.completed_ticks_after == batch.end_tick
        and receipt.post_hash == batch.post_hash
        and session.state_hash == batch.post_hash
    )


def _state_detail(left: WorldSession, right: WorldSession) -> dict[str, JsonValue]:
    before = left.authority_document()
    after = right.authority_document()
    return {
        "left_hash": left.state_hash,
        "right_hash": right.state_hash,
        "random_changed": canonical_dumps(before["random"]) != canonical_dumps(after["random"]),
        "changes": semantic_diff(before, after).as_dict(),
    }


def _compare(left: InputReplay, right: InputReplay) -> dict[str, JsonValue] | None:
    """Walk paired boundaries once; initial labels and parent labels are not gameplay."""
    a = left.timeline
    b = right.timeline
    initial_left = _runner().replay(a, tick_executor=ArenaTickExecutor(left), max_batches=0)
    initial_right = _runner().replay(b, tick_executor=ArenaTickExecutor(right), max_batches=0)
    left_session = initial_left.session
    right_session = initial_right.session
    services = (TransactionService(left_session), TransactionService(right_session))
    checkpoints = (
        {item.after_batch: item for item in a.checkpoints},
        {item.after_batch: item for item in b.checkpoints},
    )

    def difference(category: str, boundary: int, detail: JsonValue) -> dict[str, JsonValue]:
        return {
            "category": category,
            "after_batch": boundary,
            "left_tick": left_session.completed_ticks,
            "right_tick": right_session.completed_ticks,
            "detail": _bounded(detail),
        }

    for index in range(max(len(a.batches), len(b.batches)) + 1):
        if left_session.state_hash != right_session.state_hash:
            return difference("state", index, _state_detail(left_session, right_session))
        ca = checkpoints[0].get(index)
        cb = checkpoints[1].get(index)
        for checkpoint, session in ((ca, left_session), (cb, right_session)):
            if checkpoint is not None and (
                checkpoint.tick != session.completed_ticks
                or checkpoint.state_hash != session.state_hash
            ):
                raise RuntimeError("verified replay checkpoint changed during comparison")
        if (ca is None) != (cb is None):
            return difference(
                "checkpoint",
                index,
                {"left_present": ca is not None, "right_present": cb is not None},
            )
        end_left = index == len(a.batches)
        end_right = index == len(b.batches)
        if end_left or end_right:
            if end_left != end_right:
                return difference(
                    "length",
                    index,
                    {"left_batches": len(a.batches), "right_batches": len(b.batches)},
                )
            return None
        ba = a.batches[index]
        bb = b.batches[index]
        if (ba.start_tick, ba.end_tick) != (bb.start_tick, bb.end_tick):
            return difference(
                "transaction",
                index,
                {
                    "reason": "tick_range",
                    "left_end_tick": ba.end_tick,
                    "right_end_tick": bb.end_tick,
                },
            )
        # Zero-tick transactions consume no snapshot. Persistent world.tick spans
        # at most one tick; do not manufacture inputs for command-only batches.
        for tick in range(ba.start_tick, ba.end_tick):
            la = _input_document(left.snapshot_for_tick(tick))
            rb = _input_document(right.snapshot_for_tick(tick))
            if canonical_dumps(la) != canonical_dumps(rb):
                return difference("input", index, {"input_tick": tick, "left": la, "right": rb})
        ta = canonical_dumps(ba.transaction.as_dict())
        tb = canonical_dumps(bb.transaction.as_dict())
        if ta != tb:
            return difference(
                "transaction",
                index,
                {
                    "reason": "content",
                    "left_hash": "sha256:" + sha256(ta).hexdigest(),
                    "right_hash": "sha256:" + sha256(tb).hexdigest(),
                },
            )
        if not _advance(services[0], ba) or not _advance(services[1], bb):
            raise RuntimeError("verified replay receipt changed during comparison")
    raise AssertionError("comparison must reach the final boundary")


def compare_documents(left: bytes | None, right: bytes | None) -> dict[str, JsonValue]:
    """Return bounded deterministic evidence, with complete independent preflight."""
    a = _admit(left)
    b = _admit(right)
    report: dict[str, JsonValue] = {
        "schema": "ludoweave.input-replay-comparison/1",
        "left": a.document(),
        "right": b.document(),
        "status": "identical",
        "difference": None,
    }
    if a.status == "invalid" or b.status == "invalid":
        report["status"] = "invalid"
        return report
    if a.status == "incompatible" or b.status == "incompatible":
        report["status"] = "incompatible"
        return report
    assert a.artifact is not None and b.artifact is not None
    la = a.artifact.timeline.header
    rb = b.artifact.timeline.header
    if la.world_id != rb.world_id or la.initial_tick != rb.initial_tick:
        report["status"] = "incompatible"
        report["difference"] = {
            "category": "composition",
            "detail": _bounded(
                {
                    "world_id_matches": la.world_id == rb.world_id,
                    "initial_tick_matches": la.initial_tick == rb.initial_tick,
                }
            ),
        }
        return report
    report["difference"] = _compare(a.artifact, b.artifact)
    if report["difference"] is not None:
        report["status"] = "different"
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    args = parser.parse_args(argv)
    admissions: list[bytes | None] = []
    for path in (Path(args.left), Path(args.right)):
        try:
            with path.open("rb") as source:
                admissions.append(source.read(_MAX_BYTES + 1))
        except OSError:
            # Do not publish paths or OS-controlled error text.
            admissions.append(None)
    report = compare_documents(*admissions)
    print(json.dumps(report, sort_keys=True, ensure_ascii=True))
    return {"identical": 0, "different": 1, "invalid": 2, "incompatible": 2}[str(report["status"])]


if __name__ == "__main__":
    raise SystemExit(main())
