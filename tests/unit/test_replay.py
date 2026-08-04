"""Deterministic replay, checkpoint verification, and immutable branches."""

from dataclasses import dataclass
from hashlib import sha256
from uuid import UUID

import pytest
from hypothesis import given
from hypothesis import strategies as st

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
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    IncompatibleReplayError,
    RandomStreams,
    ReceiptStatus,
    ReplayBranchError,
    ReplayCheckpoint,
    ReplayDecodeError,
    ReplayDivergenceError,
    ReplayError,
    ReplayLimits,
    ReplayRecorder,
    ReplayRunner,
    ReplayTimeline,
    SnapshotCodec,
    TickExecutor,
    TransactionService,
    WorldSession,
    canonical_dumps,
    canonical_loads,
)
from ludoweave.world.canonical import JsonValue

PROJECT_SCHEMA = f"sha256:{sha256(b'replay-test-project').hexdigest()}"
LOCK_HASH = f"sha256:{sha256(b'uv-lock-fixture').hexdigest()}"
PLATFORM = "cpython-3.12-standard-test"
POSITION_ID = UUID("16493345-e99c-4f5b-8cc1-e30326bc9de6")
SCORE_ID = UUID("e1026b41-8e34-46f4-b2a1-90229384243d")


@component(type_id=POSITION_ID)
@dataclass(slots=True)
class Position:
    x: int


SCORE = ResourceSpec("replay.score", int, int)


def _decode_score(value: JsonValue) -> int:
    if type(value) is not int:
        raise ValueError
    return value


SCORE_SCHEMA = AuthorityResourceSchema(
    SCORE_ID,
    1,
    SCORE,
    "replay.score/int-v1",
    lambda value: value,
    _decode_score,
)


class ReplayTickKernel:
    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None:
        del world, tick
        resources.replace(SCORE, resources.require(SCORE) + random_streams.randbelow("score", 7))


def _composition() -> tuple[WorldSession, SnapshotCodec, TickExecutor]:
    components = ComponentRegistry((Position,))
    resources = ResourceRegistry((SCORE,))
    authority = AuthorityResourceRegistry((SCORE_SCHEMA,))
    kernel = ReplayTickKernel()
    session = WorldSession(
        "replay-world",
        World(components),
        ResourceStore(resources, ((SCORE, 0),)),
        authority_resources=authority,
        random_streams=RandomStreams(42),
        tick_executor=kernel,
    )
    return session, SnapshotCodec(components, resources, authority_resources=authority), kernel


def _transaction(
    session: WorldSession,
    transaction_id: str,
    operations: list[tuple[str, dict[str, object]]],
    *,
    expected_hash: str | None = None,
    dry_run: bool = False,
) -> CommandTransaction:
    actor = CommandActor("test", "replay-suite")
    return CommandTransaction(
        tuple(
            CommandEnvelope(
                command_id=f"{transaction_id}.command-{index}",
                transaction_id=transaction_id,
                actor=actor,
                operation=operation,
                arguments=arguments,
                expected_world_hash=expected_hash,
            )
            for index, (operation, arguments) in enumerate(operations)
        ),
        session.world_id,
        dry_run=dry_run,
    )


def _spawn(session: WorldSession, transaction_id: str, x: int) -> CommandTransaction:
    return _transaction(
        session,
        transaction_id,
        [
            (
                "entity.spawn",
                {
                    "alias": "subject",
                    "components": [
                        {
                            "type_id": str(POSITION_ID),
                            "version": 1,
                            "values": {"x": x},
                        }
                    ],
                },
            )
        ],
    )


def _tick(session: WorldSession, transaction_id: str, count: int) -> CommandTransaction:
    return _transaction(session, transaction_id, [("world.tick", {"count": count})])


def _patch_score(session: WorldSession, transaction_id: str, value: int) -> CommandTransaction:
    return _transaction(
        session,
        transaction_id,
        [
            (
                "resource.patch",
                {"type_id": str(SCORE_ID), "version": 1, "value": value},
            )
        ],
    )


def _recorder(
    session: WorldSession,
    codec: SnapshotCodec,
    *,
    timeline_id: str = "timeline-main",
    limits: ReplayLimits | None = None,
) -> ReplayRecorder:
    return ReplayRecorder(
        session,
        codec,
        timeline_id=timeline_id,
        project_schema=PROJECT_SCHEMA,
        dependency_lock_hash=LOCK_HASH,
        platform_profile=PLATFORM,
        replay_limits=limits,
    )


def _runner(codec: SnapshotCodec) -> ReplayRunner:
    return ReplayRunner(
        codec,
        project_schema=PROJECT_SCHEMA,
        dependency_lock_hash=LOCK_HASH,
        platform_profile=PLATFORM,
    )


def _mapping(timeline: ReplayTimeline) -> dict[str, JsonValue]:
    decoded = canonical_loads(timeline.canonical_bytes())
    assert isinstance(decoded, dict)
    return decoded


def test_recorded_replay_round_trip_reaches_every_checkpoint_repeatedly() -> None:
    session, codec, kernel = _composition()
    recorder = _recorder(session, codec)
    recorder.record(_spawn(session, "tx-spawn", 3))
    for tick in range(4):
        recorder.record(_tick(session, f"tx-tick-{tick}", 1))
    recorder.record(_patch_score(session, "tx-score", 91))
    timeline = recorder.timeline()

    encoded = timeline.canonical_bytes()
    decoded = ReplayTimeline.from_json(encoded)
    assert decoded.canonical_bytes() == encoded
    assert decoded.final_tick == 4
    assert len(decoded.checkpoints) == 7

    runner = _runner(codec)
    first = runner.replay(decoded, tick_executor=kernel)
    second = runner.replay(encoded, tick_executor=kernel)

    assert first.session.state_hash == timeline.final_state_hash
    assert second.session.state_hash == timeline.final_state_hash
    assert first.session.authority_document() == second.session.authority_document()
    assert first.verified_checkpoints == timeline.checkpoints
    assert second.verified_checkpoints == timeline.checkpoints


def test_empty_replay_verifies_its_initial_checkpoint() -> None:
    session, codec, kernel = _composition()
    timeline = _recorder(session, codec).timeline()

    result = _runner(codec).replay(timeline, tick_executor=kernel)

    assert result.batches_applied == 0
    assert result.session.state_hash == session.state_hash
    assert result.verified_checkpoints == timeline.checkpoints


@given(
    spawn_values=st.lists(st.integers(min_value=-10, max_value=10), max_size=4),
    tick_batch_count=st.integers(min_value=0, max_value=8),
)
def test_generated_direct_recording_and_repeated_replay_are_equivalent(
    spawn_values: list[int],
    tick_batch_count: int,
) -> None:
    session, codec, kernel = _composition()
    recorder = _recorder(session, codec)
    for index, value in enumerate(spawn_values):
        recorder.record(_spawn(session, f"generated-spawn-{index}", value))
    for index in range(tick_batch_count):
        recorder.record(_tick(session, f"generated-tick-{index}", 1))
    timeline = recorder.timeline()

    first = _runner(codec).replay(timeline, tick_executor=kernel)
    second = _runner(codec).replay(timeline.canonical_bytes(), tick_executor=kernel)

    assert first.session.authority_document() == session.authority_document()
    assert second.session.authority_document() == session.authority_document()
    assert first.verified_checkpoints == second.verified_checkpoints == timeline.checkpoints


def test_replay_detects_post_hash_divergence_at_the_exact_batch() -> None:
    session, codec, kernel = _composition()
    recorder = _recorder(session, codec)
    recorder.record(_spawn(session, "tx-spawn", 1))
    recorder.record(_tick(session, "tx-tick", 1))
    document = _mapping(recorder.timeline())
    batches = document["batches"]
    checkpoints = document["checkpoints"]
    assert isinstance(batches, list) and isinstance(batches[-1], dict)
    assert isinstance(checkpoints, list) and isinstance(checkpoints[-1], dict)
    forged_hash = "sha256:" + "f" * 64
    batches[-1]["post_hash"] = forged_hash
    checkpoints[-1]["state_hash"] = forged_hash
    forged = ReplayTimeline.from_json(canonical_dumps(document))

    with pytest.raises(ReplayDivergenceError) as raised:
        _runner(codec).replay(forged, tick_executor=kernel)

    details = dict(raised.value.details)
    assert details["batch"] == 1
    assert details["tick"] == 1
    assert details["field"] == "post_hash"
    assert details["expected"] == forged_hash
    assert details["actual"] != forged_hash


def test_replay_schema_rejects_gaps_duplicates_malformed_and_limits() -> None:
    session, codec, _ = _composition()
    recorder = _recorder(session, codec)
    recorder.record(_spawn(session, "tx-spawn", 1))
    document = _mapping(recorder.timeline())
    batches = document["batches"]
    assert isinstance(batches, list) and isinstance(batches[0], dict)
    batches[0]["start_tick"] = 7
    with pytest.raises(ReplayDecodeError):
        ReplayTimeline.from_json(canonical_dumps(document))

    for malformed in (b"{", b"{} trailing", b'{"protocol":1,"protocol":2}'):
        with pytest.raises(ReplayDecodeError):
            ReplayTimeline.from_json(malformed)

    with pytest.raises(ReplayDecodeError) as limited:
        ReplayTimeline.from_json(
            recorder.timeline().canonical_bytes(),
            limits=ReplayLimits(max_batches=1, max_checkpoints=1),
        )
    assert limited.value.code == "world.replay.oversized"


def test_composition_mismatch_is_incompatible_before_execution() -> None:
    session, codec, _ = _composition()
    timeline = _recorder(session, codec).timeline()
    wrong_runner = ReplayRunner(
        codec,
        project_schema="sha256:" + "0" * 64,
        dependency_lock_hash=LOCK_HASH,
        platform_profile=PLATFORM,
    )

    with pytest.raises(IncompatibleReplayError) as raised:
        wrong_runner.replay(timeline)
    assert raised.value.details == (("field", "project_schema"),)


def test_rejected_or_dry_run_transactions_never_enter_the_timeline() -> None:
    session, codec, _ = _composition()
    recorder = _recorder(session, codec)
    before_hash = session.state_hash
    invalid = _transaction(
        session,
        "tx-invalid",
        [("entity.destroy", {"entity": {"index": 99, "generation": 0}})],
    )

    receipt = recorder.record(invalid)
    assert receipt.status.value == "rejected"
    assert session.state_hash == before_hash
    assert recorder.timeline().batches == ()

    wrong_world = CommandTransaction(invalid.commands, "different-world")
    direct_session, _, _ = _composition()
    direct = TransactionService(direct_session).apply(wrong_world)
    recorded = recorder.record(wrong_world)
    assert recorded.canonical_bytes() == direct.canonical_bytes()
    assert recorder.timeline().batches == ()

    with pytest.raises(ReplayError):
        recorder.record(
            _transaction(
                session,
                "tx-dry",
                [("world.tick", {"count": 1})],
                dry_run=True,
            )
        )
    assert session.state_hash == before_hash
    assert recorder.timeline().batches == ()


def test_recorder_batch_limit_rejects_before_the_next_commit() -> None:
    session, codec, _ = _composition()
    recorder = _recorder(session, codec, limits=ReplayLimits(max_batches=1))
    recorder.record(_spawn(session, "tx-first", 1))
    before_hash = session.state_hash

    with pytest.raises(ReplayDecodeError) as raised:
        recorder.record(_patch_score(session, "tx-too-many", 5))

    assert raised.value.code == "world.replay.oversized"
    assert session.state_hash == before_hash
    assert len(recorder.timeline().batches) == 1


def test_branch_references_parent_boundary_and_diverges_only_after_it() -> None:
    session, codec, kernel = _composition()
    parent_recorder = _recorder(session, codec)
    parent_recorder.record(_spawn(session, "tx-parent-spawn", 5))
    parent_recorder.record(_tick(session, "tx-parent-to-1", 1))
    parent_recorder.record(_tick(session, "tx-parent-to-2", 1))
    parent_boundary_hash = session.state_hash
    parent_recorder.record(_tick(session, "tx-parent-to-3", 1))
    parent = parent_recorder.timeline()
    runner = _runner(codec)

    branch = runner.branch(
        parent,
        at_tick=2,
        timeline_id="timeline-branch",
        tick_executor=kernel,
    )
    branch_initial = branch.timeline()
    parent_reference = branch_initial.header.parent
    assert parent_reference is not None
    assert parent_reference.timeline_hash == parent.timeline_hash()
    assert parent_reference.after_batch == 3
    assert parent_reference.state_hash == parent_boundary_hash
    assert branch_initial.header.initial_state_hash == parent_boundary_hash

    branch.record(_patch_score(branch.session, "tx-branch-score", 999))
    branch.record(_tick(branch.session, "tx-branch-to-3", 1))
    branch_timeline = branch.timeline()
    branch_result = runner.replay_branch(
        branch_timeline,
        parent,
        tick_executor=kernel,
    )
    parent_result = runner.replay(parent, tick_executor=kernel)

    assert branch_result.session.completed_ticks == parent_result.session.completed_ticks == 3
    assert branch_result.session.state_hash != parent_result.session.state_hash
    assert branch_timeline.header.parent is not None
    assert branch_timeline.header.parent.state_hash == parent_boundary_hash

    mutated_parent_document = _mapping(parent)
    mutated_header = mutated_parent_document["header"]
    assert isinstance(mutated_header, dict)
    mutated_header["timeline_id"] = "different-parent"
    mutated_parent = ReplayTimeline.from_json(canonical_dumps(mutated_parent_document))
    with pytest.raises(ReplayBranchError):
        runner.replay_branch(branch_timeline, mutated_parent, tick_executor=kernel)


def test_replay_rejects_multi_tick_batches_that_would_hide_branch_points() -> None:
    session, codec, kernel = _composition()
    recorder = _recorder(session, codec)
    receipt = recorder.record(_tick(session, "tx-three-ticks", 3))

    assert receipt.status is ReceiptStatus.REJECTED
    assert recorder.timeline().batches == ()
    assert (
        _runner(codec).replay(recorder.timeline(), tick_executor=kernel).session.completed_ticks
        == 0
    )


def test_direct_replay_integer_fields_must_fit_the_canonical_domain() -> None:
    with pytest.raises(ReplayDecodeError):
        ReplayCheckpoint(2**63, 0, "sha256:" + "0" * 64)
    with pytest.raises(ReplayDecodeError):
        ReplayCheckpoint(0, 2**63, "sha256:" + "0" * 64)
