"""Evaluate local rollback replay readiness without implementing networking."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ludoweave import __version__
from ludoweave.app import InputSnapshot, RecordedInputSource
from ludoweave.samples import clockwork_input, create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
    arena_tick_transaction,
)
from ludoweave.world import (
    ReceiptStatus,
    ReplayDivergenceError,
    ReplayRecorder,
    ReplayRunner,
)

_SCHEMA = "ludoweave.evaluation.rollback-readiness/1"
_MAX_TICKS = 600


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=120)
    parser.add_argument("--branch-tick", type=int, default=60)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    ticks = _exact_int(arguments.ticks, field="ticks")
    branch_tick = _exact_int(arguments.branch_tick, field="branch_tick")
    if not 2 <= ticks <= _MAX_TICKS:
        parser.error(f"ticks must be between 2 and {_MAX_TICKS}")
    if not 1 <= branch_tick < ticks:
        parser.error("branch-tick must be between 1 and ticks - 1")

    document = evaluate(ticks=ticks, branch_tick=branch_tick)
    encoded = json.dumps(document, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    output = arguments.output
    if output is not None:
        output.write_text(encoded + "\n", encoding="utf-8", newline="\n")
    print(encoded)
    return 0


def evaluate(*, ticks: int, branch_tick: int) -> dict[str, object]:
    """Run one bounded parent/correction branch and return sanitized evidence."""

    ticks = _exact_int(ticks, field="ticks")
    branch_tick = _exact_int(branch_tick, field="branch_tick")
    if not 2 <= ticks <= _MAX_TICKS:
        raise ValueError(f"ticks must be between 2 and {_MAX_TICKS}")
    if not 1 <= branch_tick < ticks:
        raise ValueError("branch_tick must be between 1 and ticks - 1")

    baseline = clockwork_input(ticks)
    parent_snapshots = tuple(baseline.snapshot_for_tick(tick) for tick in range(ticks))
    corrected_snapshots = tuple(
        parent_snapshots[tick] if tick < branch_tick else InputSnapshot(tick)
        for tick in range(ticks)
    )

    arena = create_clockwork_arena(RecordedInputSource(parent_snapshots))
    recorder = ReplayRecorder(
        arena.session,
        arena.codec,
        timeline_id="rollback-readiness-parent",
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
        checkpoint_interval=1,
    )
    for _ in range(ticks):
        receipt = recorder.record(arena_tick_transaction(recorder.session))
        if receipt.status is not ReceiptStatus.COMMITTED:
            raise AssertionError("parent readiness transaction was rejected")
    parent = recorder.timeline()
    runner = ReplayRunner(
        arena.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )

    first_parent = runner.replay(
        parent,
        tick_executor=ArenaTickExecutor(RecordedInputSource(parent_snapshots)),
    )
    second_parent = runner.replay(
        parent,
        tick_executor=ArenaTickExecutor(RecordedInputSource(parent_snapshots)),
    )
    parent_checkpoints_verified = (
        len(parent.checkpoints) == ticks + 1
        and first_parent.verified_checkpoints == parent.checkpoints
        and second_parent.verified_checkpoints == parent.checkpoints
    )
    parent_repeatable = parent_checkpoints_verified and (
        first_parent.session.state_hash
        == second_parent.session.state_hash
        == parent.final_state_hash
    )

    input_rehydration_required = False
    try:
        runner.replay(
            parent,
            tick_executor=ArenaTickExecutor(RecordedInputSource()),
        )
    except ReplayDivergenceError:
        input_rehydration_required = True

    corrected_source = RecordedInputSource(corrected_snapshots)
    branch_recorder = runner.branch(
        parent,
        at_tick=branch_tick,
        timeline_id="rollback-readiness-correction",
        tick_executor=ArenaTickExecutor(corrected_source),
        checkpoint_interval=1,
    )
    for _ in range(ticks - branch_tick):
        receipt = branch_recorder.record(arena_tick_transaction(branch_recorder.session))
        if receipt.status is not ReceiptStatus.COMMITTED:
            raise AssertionError("correction readiness transaction was rejected")
    branch = branch_recorder.timeline()
    first_branch = runner.replay_branch(
        branch,
        parent,
        tick_executor=ArenaTickExecutor(RecordedInputSource(corrected_snapshots)),
    )
    second_branch = runner.replay_branch(
        branch,
        parent,
        tick_executor=ArenaTickExecutor(RecordedInputSource(corrected_snapshots)),
    )
    reference = branch.header.parent
    lineage_verified = (
        reference is not None
        and reference.timeline_hash == parent.timeline_hash()
        and reference.tick == branch_tick
        and reference.state_hash == branch.header.initial_state_hash
    )
    correction_checkpoints_verified = (
        len(branch.checkpoints) == len(branch.batches) + 1
        and first_branch.verified_checkpoints == branch.checkpoints
        and second_branch.verified_checkpoints == branch.checkpoints
    )
    correction_repeatable = correction_checkpoints_verified and (
        first_branch.session.state_hash
        == second_branch.session.state_hash
        == branch.final_state_hash
    )
    correction_diverged = branch.final_state_hash != parent.final_state_hash
    local_proof = all(
        (
            parent_repeatable,
            parent_checkpoints_verified,
            input_rehydration_required,
            lineage_verified,
            correction_repeatable,
            correction_checkpoints_verified,
            correction_diverged,
        )
    )
    if not local_proof:
        raise AssertionError("rollback readiness invariants were not reproduced")

    return {
        "decision": "defer-network-rollback",
        "gates": {
            "bounded_runtime_budget": False,
            "canonical_tick_inputs": False,
            "cross_platform_loss_simulation": False,
            "local_branch_lineage": lineage_verified,
            "local_repeatable_resimulation": correction_repeatable,
            "transport_security": False,
            "versioned_network_snapshot_protocol": False,
        },
        "hashes": {
            "corrected_final": branch.final_state_hash,
            "parent_final": parent.final_state_hash,
            "parent_timeline": parent.timeline_hash(),
        },
        "ludoweave_version": __version__,
        "metrics": {
            "branch_timeline_bytes": len(branch.canonical_bytes()),
            "parent_snapshot_bytes": len(parent.initial_snapshot),
            "parent_timeline_bytes": len(parent.canonical_bytes()),
        },
        "proof": {
            "correction_changed_state": correction_diverged,
            "correction_checkpoints_verified": correction_checkpoints_verified,
            "correction_repeatable": correction_repeatable,
            "input_rehydration_required": input_rehydration_required,
            "lineage_verified": lineage_verified,
            "parent_checkpoints_verified": parent_checkpoints_verified,
            "parent_repeatable": parent_repeatable,
        },
        "schema": _SCHEMA,
        "status": "deferred",
        "transport_implemented": False,
        "work": {
            "branch_batches": len(branch.batches),
            "branch_checkpoints": len(branch.checkpoints),
            "branch_tick": branch_tick,
            "parent_batches": len(parent.batches),
            "parent_checkpoints": len(parent.checkpoints),
            "ticks": ticks,
        },
    }


def _exact_int(value: object, *, field: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{field} must be an exact integer")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
