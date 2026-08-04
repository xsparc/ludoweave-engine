# pyright: reportPrivateUsage=false
"""Canonical snapshot round-trip, migration, limit, and rejection tests."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast
from uuid import UUID

import pytest

from ludoweave.ecs import (
    ComponentMigration,
    ComponentRegistry,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    World,
    component,
)
from ludoweave.world import (
    AuthorityResourceMigration,
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    IncompatibleSnapshotError,
    RandomStreams,
    ResourceRole,
    ResourceSchemaError,
    SnapshotBinding,
    SnapshotCaptureError,
    SnapshotCodec,
    SnapshotDecodeError,
    SnapshotHashMismatchError,
    SnapshotLimits,
    WorldSession,
    authority_hash,
    canonical_dumps,
    canonical_loads,
)
from ludoweave.world.canonical import JsonValue

POSITION_ID = UUID("b481565d-02b2-4051-9a1d-ccce915a1927")


@component(type_id=POSITION_ID)
@dataclass(slots=True)
class Position:
    x: float
    name: str


SCORE = ResourceSpec("snapshot.score", int, int)
SCORE_ID = UUID("21ddb612-b20f-40c6-96ab-bf476134710d")


def encode_score(value: int) -> object:
    return value


def decode_score(value: JsonValue) -> int:
    if type(value) is not int:
        raise ValueError
    return value


SCORE_SCHEMA = AuthorityResourceSchema(
    SCORE_ID,
    1,
    SCORE,
    "snapshot.score/int-v1",
    encode_score,
    decode_score,
)


def test_resource_schema_rejects_untyped_domains_and_freezes_migrations() -> None:
    with pytest.raises(ResourceSchemaError):
        AuthorityResourceSchema(
            cast(UUID, "not-a-uuid"), 1, SCORE, "score/int-v1", encode_score, decode_score
        )
    with pytest.raises(ResourceSchemaError):
        AuthorityResourceSchema(
            SCORE_ID,
            1,
            cast(ResourceSpec[int], "not-a-spec"),
            "score/int-v1",
            encode_score,
            decode_score,
        )
    with pytest.raises(ResourceSchemaError):
        AuthorityResourceSchema(
            SCORE_ID,
            1,
            SCORE,
            "score/int-v1",
            encode_score,
            decode_score,
            role=cast(ResourceRole, "state"),
        )
    with pytest.raises(ResourceSchemaError):
        AuthorityResourceSchema(
            SCORE_ID,
            2**63,
            SCORE,
            "score/int-v1",
            encode_score,
            decode_score,
        )
    with pytest.raises(ResourceSchemaError):
        AuthorityResourceMigration(2**63 - 1, 2**63, lambda value: value)
    with pytest.raises(ResourceSchemaError):
        AuthorityResourceSchema(
            SCORE_ID,
            2,
            SCORE,
            "score/int-v1",
            encode_score,
            decode_score,
            migrations=cast(tuple[AuthorityResourceMigration, ...], ("bad",)),
        )

    source = [AuthorityResourceMigration(1, 2, lambda value: value)]
    schema = AuthorityResourceSchema(
        SCORE_ID,
        2,
        SCORE,
        "score/int-v1",
        encode_score,
        decode_score,
        migrations=cast(tuple[AuthorityResourceMigration, ...], source),
    )
    source.clear()
    assert len(schema.migrations) == 1


def _composition() -> tuple[
    ComponentRegistry,
    ResourceRegistry,
    AuthorityResourceRegistry,
]:
    return (
        ComponentRegistry((Position,)),
        ResourceRegistry((SCORE,)),
        AuthorityResourceRegistry((SCORE_SCHEMA,)),
    )


def _populated_session() -> tuple[WorldSession, SnapshotCodec]:
    components, resources, authority = _composition()
    world = World(components)
    entities = [world.spawn(Position(float(index), f"entity-{index}")) for index in range(4)]
    world.patch(entities[0], Position, x=-0.0)
    world.destroy(entities[1])
    world.destroy(entities[3])
    store = ResourceStore(resources, ((SCORE, 17),))
    random = RandomStreams(0xFEDCBA9876543210)
    for _ in range(5):
        random.next_u32("waves")
    random.next_u32("loot")
    session = WorldSession(
        "snapshot-world",
        world,
        store,
        authority_resources=authority,
        completed_ticks=23,
        random_streams=random,
    )
    return session, SnapshotCodec(components, resources, authority_resources=authority)


def _decoded_wrapper(snapshot: bytes) -> dict[str, JsonValue]:
    value = canonical_loads(snapshot)
    assert isinstance(value, dict)
    return value


def _rehash(wrapper: dict[str, JsonValue]) -> bytes:
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    wrapper["state_hash"] = authority_hash(authority)
    return canonical_dumps(wrapper)


def test_snapshot_round_trip_preserves_hash_bytes_future_allocation_and_epochs() -> None:
    source, codec = _populated_session()
    source_hash = source.state_hash
    source_document = source.authority_document()

    snapshot = codec.encode(source)
    restored = codec.decode(snapshot)

    assert restored.state_hash == source_hash
    assert restored.authority_document() == source_document
    assert codec.encode(restored) == snapshot
    assert restored.completed_ticks == 23
    assert restored.resources.require(SCORE) == 17
    assert restored.random_streams.next_u32("waves") == source.random_streams.next_u32("waves")
    assert restored.random_streams.next_u32("loot") == source.random_streams.next_u32("loot")

    source_view = source.world
    restored_view = restored.world
    source_next = source_view.spawn(Position(99.0, "next"))
    restored_next = restored_view.spawn(Position(99.0, "next"))
    assert restored_next == source_next
    assert restored_view.component_epoch(restored_next, Position) == source_view.component_epoch(
        source_next, Position
    )
    assert tuple(restored_view.query(Position).changed_since(2).stable().rows()) == tuple(
        source_view.query(Position).changed_since(2).stable().rows()
    )


@pytest.mark.parametrize(
    "malformed",
    [
        b"{",
        b'{"protocol":"ludoweave.snapshot/1","protocol":"duplicate"}',
        b"\xef\xbb\xbf{}",
        b"{} trailing",
    ],
)
def test_malformed_snapshot_bytes_are_bounded_structured_failures(malformed: bytes) -> None:
    _, codec = _populated_session()
    with pytest.raises(SnapshotDecodeError):
        codec.decode(malformed)


@pytest.mark.parametrize(
    "binding",
    [
        ("sha256:bad", "sha256:" + "0" * 64, "portable"),
        ("sha256:" + "0" * 64, "sha256:bad", "portable"),
        ("sha256:" + "0" * 64, "sha256:" + "1" * 64, "line\nbreak"),
    ],
)
def test_snapshot_binding_requires_exact_stable_identifiers(
    binding: tuple[str, str, str],
) -> None:
    with pytest.raises(SnapshotDecodeError):
        SnapshotBinding(*binding)


def test_hash_mismatch_and_unknown_wrapper_field_are_rejected() -> None:
    source, codec = _populated_session()
    wrapper = _decoded_wrapper(codec.encode(source))
    wrapper["state_hash"] = "sha256:" + "0" * 64
    with pytest.raises(SnapshotHashMismatchError):
        codec.decode(canonical_dumps(wrapper))

    wrapper = _decoded_wrapper(codec.encode(source))
    wrapper["unexpected"] = True
    with pytest.raises(SnapshotDecodeError):
        codec.decode(canonical_dumps(wrapper))


def test_invalid_resource_and_random_payloads_are_structured_failures() -> None:
    source, codec = _populated_session()
    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    resources = authority["resources"]
    assert isinstance(resources, list) and isinstance(resources[0], dict)
    resources[0]["value"] = "not-an-integer"
    with pytest.raises(SnapshotDecodeError) as resource_error:
        codec.decode(_rehash(wrapper))
    assert resource_error.value.phase == "migrate"

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    random = authority["random"]
    assert isinstance(random, dict)
    streams = random["streams"]
    assert isinstance(streams, list) and streams
    streams.append(streams[0])
    with pytest.raises(SnapshotDecodeError) as random_error:
        codec.decode(_rehash(wrapper))
    assert random_error.value.phase == "validate"


def test_absent_resource_record_must_match_its_manifest_version() -> None:
    source, codec = _populated_session()
    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    resources = authority["resources"]
    assert isinstance(resources, list) and isinstance(resources[0], dict)
    resources[0]["present"] = False
    resources[0]["value"] = None
    resources[0]["version"] = 999

    with pytest.raises(SnapshotDecodeError):
        codec.decode(_rehash(wrapper))


def test_invalid_allocator_and_duplicate_component_rows_reject_without_destination_mutation() -> (
    None
):
    source, codec = _populated_session()
    destination, _ = _populated_session()
    before_document = destination.authority_document()
    before_hash = destination.state_hash

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    allocator = authority["allocator"]
    assert isinstance(allocator, dict)
    allocator["free"] = []
    invalid_allocator = _rehash(wrapper)
    with pytest.raises(SnapshotDecodeError):
        codec.load_into(destination, invalid_allocator)
    assert destination.authority_document() == before_document
    assert destination.state_hash == before_hash

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    epochs = authority["epochs"]
    assert isinstance(epochs, dict)
    epochs["world"] = 0
    epochs["structural"] = 0
    tables = authority["components"]
    assert isinstance(tables, list) and isinstance(tables[0], dict)
    tables[0]["structural_epoch"] = 0
    tables[0]["rows"] = []
    with pytest.raises(SnapshotDecodeError):
        codec.load_into(destination, _rehash(wrapper))
    assert destination.authority_document() == before_document
    assert destination.state_hash == before_hash

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    tables = authority["components"]
    assert isinstance(tables, list) and isinstance(tables[0], dict)
    tables[0]["structural_epoch"] = 0
    rows = tables[0]["rows"]
    assert isinstance(rows, list) and isinstance(rows[0], dict)
    rows[0]["changed_epoch"] = 0
    with pytest.raises(SnapshotDecodeError):
        codec.load_into(destination, _rehash(wrapper))
    assert destination.authority_document() == before_document
    assert destination.state_hash == before_hash

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    allocator = authority["allocator"]
    assert isinstance(allocator, dict)
    generations = allocator["generations"]
    assert isinstance(generations, list)
    generations[1] = 0
    with pytest.raises(SnapshotDecodeError):
        codec.load_into(destination, _rehash(wrapper))
    assert destination.authority_document() == before_document
    assert destination.state_hash == before_hash

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    epochs = authority["epochs"]
    assert isinstance(epochs, dict)
    epochs["structural"] = 1
    tables = authority["components"]
    assert isinstance(tables, list) and isinstance(tables[0], dict)
    tables[0]["structural_epoch"] = 2
    with pytest.raises(SnapshotDecodeError):
        codec.load_into(destination, _rehash(wrapper))
    assert destination.authority_document() == before_document
    assert destination.state_hash == before_hash

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    tables = authority["components"]
    assert isinstance(tables, list)
    table = tables[0]
    assert isinstance(table, dict)
    rows = table["rows"]
    assert isinstance(rows, list)
    first_row = rows[0]
    assert isinstance(first_row, dict)
    rows.append(dict(first_row))
    with pytest.raises(SnapshotDecodeError):
        codec.load_into(destination, _rehash(wrapper))
    assert destination.authority_document() == before_document
    assert destination.state_hash == before_hash


def test_future_component_schema_and_wrong_engine_are_incompatible() -> None:
    source, codec = _populated_session()
    wrapper = _decoded_wrapper(codec.encode(source))
    wrapper["engine_version"] = "999.0"
    with pytest.raises(IncompatibleSnapshotError):
        codec.decode(canonical_dumps(wrapper))

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    manifests = authority["component_schemas"]
    assert isinstance(manifests, list)
    manifest = manifests[0]
    assert isinstance(manifest, dict)
    manifest["version"] = 999
    with pytest.raises(IncompatibleSnapshotError):
        codec.decode(_rehash(wrapper))

    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    manifests = authority["component_schemas"]
    assert isinstance(manifests, list) and isinstance(manifests[0], dict)
    manifests[0]["fields"] = [{"name": "forged", "type": "str", "optional": True}]
    with pytest.raises(IncompatibleSnapshotError):
        codec.decode(_rehash(wrapper))


def test_malformed_world_id_is_wrapped_in_snapshot_error_hierarchy() -> None:
    source, codec = _populated_session()
    wrapper = _decoded_wrapper(codec.encode(source))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    authority["world_id"] = "../not-a-world"

    with pytest.raises(SnapshotDecodeError) as raised:
        codec.decode(_rehash(wrapper))

    assert raised.value.phase == "restore"
    assert raised.value.details == (("cause_code", "world.invalid_authority"),)


def test_snapshot_semantic_limits_apply_before_restore() -> None:
    source, _ = _populated_session()
    components, resources, authority = _composition()
    codec = SnapshotCodec(
        components,
        resources,
        authority_resources=authority,
        limits=SnapshotLimits(max_entities=1, max_components=1),
    )
    roomy_codec = SnapshotCodec(components, resources, authority_resources=authority)

    with pytest.raises(SnapshotDecodeError) as raised:
        codec.decode(roomy_codec.encode(source))
    assert raised.value.code == "world.snapshot.oversized"

    stream_limited = SnapshotCodec(
        components,
        resources,
        authority_resources=authority,
        limits=SnapshotLimits(max_random_streams=1),
    )
    with pytest.raises(SnapshotDecodeError) as streams_raised:
        stream_limited.decode(roomy_codec.encode(source))
    assert streams_raised.value.code == "world.snapshot.oversized"


def migrate_counter_v1(values: Mapping[str, object]) -> dict[str, object]:
    return {"value": values["old_value"]}


COUNTER_ID = UUID("80aad7f3-a4d1-4ac0-9385-5c8dc51b0fd5")


@component(
    type_id=COUNTER_ID,
    version=2,
    migrations=(ComponentMigration(1, 2, migrate_counter_v1),),
)
@dataclass(slots=True)
class Counter:
    value: int


def test_historical_component_record_uses_registered_forward_migration() -> None:
    components = ComponentRegistry((Counter,))
    resources = ResourceRegistry()
    world = World(components)
    world.spawn(Counter(7))
    session = WorldSession("migration-world", world, ResourceStore(resources))
    codec = SnapshotCodec(components, resources)
    wrapper = _decoded_wrapper(codec.encode(session))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    manifest = authority["component_schemas"]
    tables = authority["components"]
    assert isinstance(manifest, list) and isinstance(tables, list)
    assert isinstance(manifest[0], dict) and isinstance(tables[0], dict)
    manifest[0]["version"] = 1
    tables[0]["version"] = 1
    rows = tables[0]["rows"]
    assert isinstance(rows, list) and isinstance(rows[0], dict)
    rows[0]["values"] = {"old_value": 11}

    restored = codec.decode(_rehash(wrapper))

    entity = restored.world.entities()[0]
    assert restored.world.get(entity, Counter) == Counter(11)


def fail_component_migration(values: Mapping[str, object]) -> Mapping[str, object]:
    del values
    raise RuntimeError("migration fixture failure")


FAILING_ID = UUID("548c955f-bde3-4269-934c-1b1665360afd")


@component(
    type_id=FAILING_ID,
    version=2,
    migrations=(ComponentMigration(1, 2, fail_component_migration),),
)
@dataclass(slots=True)
class FailingMigration:
    value: int


def test_throwing_snapshot_migration_is_structured_and_returns_no_session() -> None:
    components = ComponentRegistry((FailingMigration,))
    resources = ResourceRegistry()
    world = World(components)
    world.spawn(FailingMigration(7))
    session = WorldSession("failing-migration", world, ResourceStore(resources))
    codec = SnapshotCodec(components, resources)
    wrapper = _decoded_wrapper(codec.encode(session))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    manifests = authority["component_schemas"]
    tables = authority["components"]
    assert isinstance(manifests, list) and isinstance(tables, list)
    assert isinstance(manifests[0], dict) and isinstance(tables[0], dict)
    manifests[0]["version"] = 1
    tables[0]["version"] = 1

    with pytest.raises(SnapshotDecodeError) as raised:
        codec.decode(_rehash(wrapper))

    assert raised.value.phase == "migrate"
    assert session.world.get(session.world.entities()[0], FailingMigration) == FailingMigration(7)


def migrate_score_v1(value: JsonValue) -> object:
    if type(value) is not int:
        raise ValueError
    return value + 1


def test_historical_resource_value_uses_registered_forward_migration() -> None:
    score_v2 = AuthorityResourceSchema(
        SCORE_ID,
        2,
        SCORE,
        "snapshot.score/int-v1",
        encode_score,
        decode_score,
        migrations=(AuthorityResourceMigration(1, 2, migrate_score_v1),),
    )
    components = ComponentRegistry()
    resources = ResourceRegistry((SCORE,))
    authority_registry = AuthorityResourceRegistry((score_v2,))
    session = WorldSession(
        "resource-migration",
        World(components),
        ResourceStore(resources, ((SCORE, 4),)),
        authority_resources=authority_registry,
    )
    codec = SnapshotCodec(components, resources, authority_resources=authority_registry)
    wrapper = _decoded_wrapper(codec.encode(session))
    authority = wrapper["authority"]
    assert isinstance(authority, dict)
    manifests = authority["resource_schemas"]
    records = authority["resources"]
    assert isinstance(manifests, list) and isinstance(records, list)
    assert isinstance(manifests[0], dict) and isinstance(records[0], dict)
    manifests[0]["version"] = 1
    records[0]["version"] = 1
    records[0]["value"] = 8

    restored = codec.decode(_rehash(wrapper))

    assert restored.resources.require(SCORE) == 9


def test_snapshot_load_preserves_input_and_runtime_excluded_resources() -> None:
    input_spec = ResourceSpec("snapshot.input_frame", int, int)
    runtime_spec = ResourceSpec("snapshot.runtime_cache", int, int, deterministic=False)
    input_schema = AuthorityResourceSchema(
        UUID("5ae11e70-5e72-409f-ad18-731b928e2a86"),
        1,
        input_spec,
        "snapshot.input/int-v1",
        int,
        decode_score,
        role=ResourceRole.INPUT,
    )
    runtime_schema = AuthorityResourceSchema(
        UUID("05c87a87-73a7-4f06-8bbf-8233c7e805ea"),
        1,
        runtime_spec,
        "snapshot.runtime/int-v1",
        int,
        decode_score,
        role=ResourceRole.RUNTIME_EXCLUDED,
    )
    components = ComponentRegistry()
    resources = ResourceRegistry((SCORE, input_spec, runtime_spec))
    authority = AuthorityResourceRegistry((SCORE_SCHEMA, input_schema, runtime_schema))
    source = WorldSession(
        "preserve-excluded",
        World(components),
        ResourceStore(resources, ((SCORE, 17), (input_spec, 1), (runtime_spec, 2))),
        authority_resources=authority,
    )
    destination = WorldSession(
        "preserve-excluded",
        World(components),
        ResourceStore(resources, ((SCORE, 3), (input_spec, 91), (runtime_spec, 92))),
        authority_resources=authority,
    )
    codec = SnapshotCodec(components, resources, authority_resources=authority)

    codec.load_into(destination, codec.encode(source))

    assert destination.resources.require(SCORE) == 17
    assert destination.resources.require(input_spec) == 91
    assert destination.resources.require(runtime_spec) == 92


def test_snapshot_load_rejects_active_query_without_mutating_destination() -> None:
    source, codec = _populated_session()
    destination, _ = _populated_session()
    before_hash = destination.state_hash
    rows = destination._world.query(Position).rows()
    rows.__enter__()
    try:
        with pytest.raises(SnapshotDecodeError):
            codec.load_into(destination, codec.encode(source))
    finally:
        rows.close()
    assert destination.state_hash == before_hash


def test_snapshot_capture_rejects_active_query_with_structured_safe_point_error() -> None:
    session, codec = _populated_session()
    before_hash = session.state_hash
    rows = session._world.query(Position).rows()
    rows.__enter__()
    try:
        with pytest.raises(SnapshotCaptureError) as raised:
            codec.encode(session)
        assert raised.value.code == "world.snapshot.capture_failed"
        assert raised.value.details == (("cause_code", "ecs.active_query"),)
    finally:
        rows.close()
    assert session.state_hash == before_hash
