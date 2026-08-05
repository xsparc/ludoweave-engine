"""Transport-independent M5 service behavior, safety, and acceptance tests."""

from __future__ import annotations

import threading
from collections.abc import Mapping
from hashlib import sha256

import pytest

from ludoweave.agent import (
    AgentCapabilities,
    AgentCapabilityError,
    AgentCapture,
    AgentCommandService,
    AgentConcurrencyError,
    AgentLimitError,
    AgentLimits,
    AgentProject,
)
from ludoweave.core import VirtualClock
from ludoweave.ecs import ComponentRegistry, ResourceRegistry, ResourceStore, World, WorldStore
from ludoweave.samples import (
    BUILDER_OBJECT_ID,
    builder_adjust_transaction,
    builder_create_transaction,
    create_agent_world_builder,
    run_agent_world_builder_acceptance,
)
from ludoweave.world import (
    AuthorityResourceRegistry,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    RandomStreams,
    ReceiptStatus,
    SnapshotBinding,
    SnapshotCodec,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue


class _Capture:
    def __init__(self) -> None:
        self.closed = 0

    def capture(self, width: int, height: int) -> AgentCapture:
        return AgentCapture(width, height, b"\x11\x22\x33\xff" * (width * height))

    def close(self) -> None:
        self.closed += 1


def _receipt(result: Mapping[str, JsonValue]) -> dict[str, JsonValue]:
    value = result.get("receipt")
    assert isinstance(value, dict)
    return value


def test_read_tools_are_stable_and_do_not_mutate_authority() -> None:
    builder = create_agent_world_builder()
    service = builder.service
    before = service.session.state_hash

    project = service.call("project_describe")
    world = service.call("world_describe")
    query = service.call("world_query", {"limit": 10})

    assert project["protocol"] == "ludoweave.agent.project/1"
    assert project["capabilities"] == {
        "capture": False,
        "read": True,
        "tests": True,
        "write": False,
    }
    assert world["entity_count"] == 0
    assert query["entities"] == []
    assert service.session.state_hash == before
    builder.close()


def test_writes_require_explicit_capability() -> None:
    builder = create_agent_world_builder()
    transaction = builder_create_transaction(
        builder.service.actor,
        expected_world_hash=builder.service.session.state_hash,
    )

    with pytest.raises(AgentCapabilityError) as denied:
        builder.service.call(
            "transaction_apply",
            {"transaction": transaction.as_dict()},
        )

    assert denied.value.code == "agent.capability_denied"
    assert builder.service.session.completed_ticks == 0
    assert builder.service.call("world_describe")["entity_count"] == 0
    builder.close()


def test_validate_apply_query_snapshot_diff_and_stale_hash_are_atomic() -> None:
    builder = create_agent_world_builder(write=True)
    service = builder.service
    initial_hash = service.session.state_hash
    before = service.call("world_snapshot")
    transaction = builder_create_transaction(service.actor, expected_world_hash=initial_hash)

    validated = _receipt(
        service.call("transaction_validate", {"transaction": transaction.as_dict()})
    )
    assert validated["status"] == ReceiptStatus.DRY_RUN.value
    assert validated["pre_hash"] == validated["post_hash"] == initial_hash
    assert validated["proposed_post_hash"] != initial_hash
    assert service.session.state_hash == initial_hash

    committed = _receipt(service.call("transaction_apply", {"transaction": transaction.as_dict()}))
    assert committed["status"] == ReceiptStatus.COMMITTED.value
    committed_hash = service.session.state_hash
    assert committed_hash == committed["post_hash"] != initial_hash

    query = service.call(
        "world_query",
        {"include": [str(BUILDER_OBJECT_ID)], "limit": 32},
    )
    assert query["matched"] == query["returned"] == 6
    entities = query["entities"]
    assert isinstance(entities, list)
    first = entities[0]
    assert isinstance(first, dict)
    entity = service.call("entity_get", {"entity": first["entity"]})
    assert entity["entity"] == first["entity"]

    stale = builder_adjust_transaction(
        service.actor,
        expected_world_hash=initial_hash,
        player_entity="1:0",
    )
    rejected = _receipt(service.call("transaction_apply", {"transaction": stale.as_dict()}))
    assert rejected["status"] == ReceiptStatus.REJECTED.value
    assert rejected["pre_hash"] == rejected["post_hash"] == committed_hash
    assert service.session.state_hash == committed_hash

    diff = service.call("world_diff", {"before_snapshot": before["snapshot"]})
    changes = diff["changes"]
    assert isinstance(changes, dict)
    created = changes["created_entities"]
    assert isinstance(created, list)
    assert len(created) == 6
    builder.close()


def test_tick_capture_tests_telemetry_replay_and_close() -> None:
    capture = _Capture()
    builder = create_agent_world_builder(
        write=True,
        capture_provider=capture,
    )
    service = builder.service
    transaction = builder_create_transaction(
        service.actor,
        expected_world_hash=service.session.state_hash,
    )
    service.call("transaction_apply", {"transaction": transaction.as_dict()})

    ticked = service.call(
        "world_tick",
        {
            "request_id": "test.advance",
            "count": 4,
            "expected_world_hash": service.session.state_hash,
        },
    )
    image = service.call(
        "render_capture",
        {"width": 8, "height": 4, "include_pixels": True},
    )
    tests = service.call("test_run")
    telemetry = service.call("telemetry_get")

    assert ticked["status"] == "committed"
    assert ticked["completed"] == ticked["completed_ticks"] == 4
    assert image["bytes"] == 128
    assert image["encoding"] == "base64"
    assert tests["passed"] is True
    assert telemetry["replay_batches"] == 5
    application = telemetry["application"]
    assert isinstance(application, dict)
    assert application["objects"] == 6
    assert service.replay_bytes().startswith(b'{"batches"')

    builder.close()
    builder.close()
    assert capture.closed == 1
    with pytest.raises(AgentConcurrencyError) as closed:
        service.call("world_describe")
    assert closed.value.code == "agent.closed"


def test_limits_rate_and_wrong_thread_fail_predictably() -> None:
    clock = VirtualClock()
    limits = AgentLimits(
        max_query_entities=2,
        max_ticks_per_request=2,
        max_capture_pixels=16,
        max_requests_per_window=3,
        rate_window_ns=10,
    )
    builder = create_agent_world_builder(write=True, limits=limits, clock=clock)
    service = builder.service

    with pytest.raises(AgentLimitError) as query_limit:
        service.call("world_query", {"limit": 3})
    assert dict(query_limit.value.details)["field"] == "query_entities"
    service.call("world_describe")
    service.call("world_describe")
    with pytest.raises(AgentLimitError) as rate_limit:
        service.call("world_describe")
    assert dict(rate_limit.value.details)["field"] == "requests_per_window"
    clock.advance_ns(11)
    assert service.call("world_describe")["entity_count"] == 0

    error: list[AgentConcurrencyError] = []

    def other_thread() -> None:
        try:
            service.call("world_describe")
        except AgentConcurrencyError as caught:
            error.append(caught)

    thread = threading.Thread(target=other_thread)
    thread.start()
    thread.join()
    assert len(error) == 1
    assert error[0].code == "agent.wrong_thread"
    builder.close()


def test_oversized_mutation_and_capture_requests_fail_before_work() -> None:
    capture = _Capture()
    limits = AgentLimits(
        max_transaction_commands=4,
        max_ticks_per_request=2,
        max_capture_pixels=16,
    )
    builder = create_agent_world_builder(
        write=True,
        capture_provider=capture,
        limits=limits,
    )
    service = builder.service
    transaction = builder_create_transaction(
        service.actor,
        expected_world_hash=service.session.state_hash,
    )

    with pytest.raises(AgentLimitError) as transaction_limit:
        service.call("transaction_apply", {"transaction": transaction.as_dict()})
    assert dict(transaction_limit.value.details)["field"] == "transaction_commands"
    with pytest.raises(AgentLimitError) as tick_limit:
        service.call("world_tick", {"request_id": "too-many", "count": 3})
    assert dict(tick_limit.value.details)["field"] == "ticks"
    with pytest.raises(AgentLimitError) as capture_limit:
        service.call("render_capture", {"width": 5, "height": 4})
    assert dict(capture_limit.value.details)["field"] == "capture_pixels"
    assert service.session.state_hash == service.call("world_describe")["state_hash"]
    assert capture.closed == 0
    builder.close()


def test_reentrant_overlapping_mutation_is_rejected_at_safe_point() -> None:
    class ReentrantExecutor:
        def __init__(self) -> None:
            self.service: AgentCommandService | None = None
            self.error: AgentConcurrencyError | None = None

        def execute_tick(
            self,
            world: WorldStore,
            resources: ResourceStore,
            random_streams: RandomStreams,
            tick: int,
        ) -> None:
            del world, resources, random_streams, tick
            service = self.service
            assert service is not None
            transaction = CommandTransaction(
                (
                    CommandEnvelope(
                        command_id="nested.spawn",
                        transaction_id="nested.transaction",
                        actor=service.actor,
                        operation="entity.spawn",
                        arguments={"components": []},
                        expected_world_hash=service.session.state_hash,
                    ),
                ),
                service.session.world_id,
            )
            try:
                service.call("transaction_apply", {"transaction": transaction.as_dict()})
            except AgentConcurrencyError as error:
                self.error = error
                raise

    executor = ReentrantExecutor()
    components = ComponentRegistry()
    resources = ResourceRegistry()
    authority = AuthorityResourceRegistry()
    session = WorldSession(
        "reentrant",
        World(components),
        ResourceStore(resources),
        authority_resources=authority,
        tick_executor=executor,
    )
    project_hash = f"sha256:{sha256(b'reentrant-project').hexdigest()}"
    lock_hash = f"sha256:{sha256(b'reentrant-lock').hexdigest()}"
    codec = SnapshotCodec(
        components,
        resources,
        authority_resources=authority,
        binding=SnapshotBinding(project_hash, lock_hash, "cpython-standard-d1"),
    )
    service = AgentCommandService(
        session,
        codec,
        AgentProject(
            "reentrant",
            "reentrant",
            project_hash,
            lock_hash,
            "cpython-standard-d1",
        ),
        CommandActor("agent", "reentrant"),
        capabilities=AgentCapabilities(write=True),
    )
    executor.service = service
    before = service.session.state_hash

    result = service.call("world_tick", {"request_id": "outer", "count": 1})

    assert result["status"] == "rejected"
    assert result["completed"] == 0
    assert executor.error is not None
    assert executor.error.code == "agent.mutation_busy"
    assert service.session.state_hash == before
    service.close()


def test_agent_world_builder_clean_acceptance_loop_uses_only_typed_tools() -> None:
    capture = _Capture()
    builder = create_agent_world_builder(write=True, capture_provider=capture)

    result = run_agent_world_builder_acceptance(builder.service)

    assert result["protocol"] == "ludoweave.sample.agent_world_builder/1"
    assert result["validation_status"] == "dry_run"
    assert result["apply_status"] == result["adjust_status"] == "committed"
    assert result["ticks"] == 3
    assert result["capture_width"] == 320
    assert result["capture_height"] == 180
    assert result["query_matches"] == 6
    assert result["diff_changed"] is True
    assert result["tests_passed"] is True
    assert result["replay_batches"] == 5
    assert str(result["state_hash"]).startswith("sha256:")
    assert str(result["replay_sha256"]).startswith("sha256:")
    builder.close()


def test_public_result_redaction_removes_secret_named_values() -> None:
    class SecretTelemetry:
        def telemetry(self) -> Mapping[str, object]:
            return {
                "api_key": "do-not-return-either",
                "authorization": "Bearer do-not-return",
                "api_token": "do-not-return",
                "nested": {"password": "also-secret", "safe": 7},
            }

    builder = create_agent_world_builder()
    session = builder.service.session
    codec = builder.codec
    builder.close()
    command_service = AgentCommandService(
        session,
        codec,
        AgentProject(
            "redaction",
            "redaction",
            f"sha256:{sha256(b'redaction-project').hexdigest()}",
            f"sha256:{sha256(b'redaction-lock').hexdigest()}",
            "cpython-standard-d1",
        ),
        CommandActor("agent", "redaction"),
        capabilities=AgentCapabilities(),
        telemetry_provider=SecretTelemetry(),
    )

    telemetry = command_service.call("telemetry_get")

    application = telemetry["application"]
    assert isinstance(application, dict)
    assert application["api_key"] == "[redacted]"
    assert application["authorization"] == "[redacted]"
    assert application["api_token"] == "[redacted]"
    nested = application["nested"]
    assert isinstance(nested, dict)
    assert nested == {"password": "[redacted]", "safe": 7}
    command_service.close()
