"""Agent World Builder: an exercised typed-tool acceptance composition."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from math import isfinite
from typing import cast
from uuid import UUID

from ludoweave.agent import (
    AgentCapabilities,
    AgentCapture,
    AgentCaptureProvider,
    AgentCommandService,
    AgentLimits,
    AgentProject,
    AgentTelemetryProvider,
    AgentTestProvider,
    AgentTestResult,
)
from ludoweave.core.clock import Clock
from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceStore,
    World,
    WorldStore,
    component,
)
from ludoweave.render import (
    Camera2D,
    Color,
    PipelineDescriptor,
    PipelineHandle,
    RenderDevice,
    RenderExtractor,
    SpriteExtractionSource,
    SurfaceDescriptor,
    SurfaceHandle,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureHandle,
    TextureUsage,
)
from ludoweave.world import (
    AuthorityResourceRegistry,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    RandomStreams,
    SnapshotBinding,
    SnapshotCodec,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue

BUILDER_SEED = 4217
BUILDER_PROJECT_SCHEMA = f"sha256:{sha256(b'agent-world-builder-schema/1').hexdigest()}"
BUILDER_LOCK_HASH = f"sha256:{sha256(b'ludoweave-lock-m5').hexdigest()}"
BUILDER_PLATFORM_PROFILE = "cpython-standard-d1"

BUILDER_TRANSFORM_ID = UUID("a102740f-2e01-47c4-91fb-764e07b22f02")
BUILDER_OBJECT_ID = UUID("07a7b29a-4b76-48dd-972a-2259c974062a")

_OBJECT_KINDS = frozenset({"effect", "light", "player", "prop", "room"})


@component(type_id=BUILDER_TRANSFORM_ID)
@dataclass(frozen=True, slots=True)
class BuilderTransform:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if not all(isfinite(value) for value in (self.x, self.y, self.width, self.height)):
            raise ValueError("builder transform values must be finite")
        if self.width <= 0.0 or self.height <= 0.0:
            raise ValueError("builder transform extent must be positive")


@component(type_id=BUILDER_OBJECT_ID)
@dataclass(frozen=True, slots=True)
class BuilderObject:
    name: str
    kind: str

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name or len(self.name.encode("utf-8")) > 128:
            raise ValueError("builder object name must be bounded non-empty text")
        if self.kind not in _OBJECT_KINDS:
            raise ValueError("builder object kind is not registered")


class BuilderTickExecutor:
    """Deterministic no-op safe point for layout-world tick acceptance."""

    __slots__ = ()

    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None:
        del world, resources, random_streams, tick


class BuilderTestProvider(AgentTestProvider):
    """Explicit in-process layout checks; no shell or test-name imports."""

    __slots__ = ("_session",)

    _NAMES = (
        "layout.objects_inside_room",
        "layout.player_present",
        "layout.props_non_overlapping",
        "layout.unique_names",
    )

    def __init__(self, session: WorldSession) -> None:
        self._session = session

    def test_names(self) -> tuple[str, ...]:
        return self._NAMES

    def run_tests(self, names: Sequence[str]) -> tuple[AgentTestResult, ...]:
        world = self._session.world
        records = _builder_records(world)
        results: list[AgentTestResult] = []
        for name in names:
            if name == "layout.objects_inside_room":
                results.append(self._inside_room(records))
            elif name == "layout.player_present":
                players = tuple(record for record in records if record[1].kind == "player")
                results.append(
                    AgentTestResult(
                        name,
                        len(players) == 1,
                        () if len(players) == 1 else ("expected exactly one player",),
                    )
                )
            elif name == "layout.props_non_overlapping":
                results.append(self._props_non_overlapping(records))
            elif name == "layout.unique_names":
                object_names = tuple(record[1].name for record in records)
                unique = len(object_names) == len(set(object_names))
                results.append(
                    AgentTestResult(
                        name,
                        unique,
                        () if unique else ("object names are not unique",),
                    )
                )
            else:
                raise ValueError("test name is outside the builder allowlist")
        return tuple(results)

    @staticmethod
    def _inside_room(
        records: tuple[tuple[BuilderTransform, BuilderObject], ...],
    ) -> AgentTestResult:
        rooms = tuple(record for record in records if record[1].kind == "room")
        if len(rooms) != 1:
            return AgentTestResult(
                "layout.objects_inside_room",
                False,
                ("expected exactly one room",),
            )
        room = rooms[0][0]
        inside = all(_inside(transform, room) for transform, item in records if item.kind != "room")
        return AgentTestResult(
            "layout.objects_inside_room",
            inside,
            () if inside else ("one or more objects cross room bounds",),
        )

    @staticmethod
    def _props_non_overlapping(
        records: tuple[tuple[BuilderTransform, BuilderObject], ...],
    ) -> AgentTestResult:
        props = tuple(transform for transform, item in records if item.kind == "prop")
        overlap = any(
            _overlap(left, right)
            for index, left in enumerate(props)
            for right in props[index + 1 :]
        )
        return AgentTestResult(
            "layout.props_non_overlapping",
            not overlap,
            () if not overlap else ("two props overlap",),
        )


class BuilderTelemetryProvider(AgentTelemetryProvider):
    __slots__ = ("_session",)

    def __init__(self, session: WorldSession) -> None:
        self._session = session

    def telemetry(self) -> Mapping[str, object]:
        records = _builder_records(self._session.world)
        counts = {kind: 0 for kind in sorted(_OBJECT_KINDS)}
        for _, item in records:
            counts[item.kind] += 1
        return {"objects": len(records), "by_kind": counts}


class BuilderRenderCapture:
    """Renderer-backed offscreen capture owned and closed by the agent service."""

    __slots__ = ("_device", "_extractor", "_pipeline", "_session", "_surface", "_texture")

    def __init__(self, session: WorldSession, device: RenderDevice) -> None:
        self._session = session
        self._device = device
        self._extractor = RenderExtractor()
        self._surface: SurfaceHandle | None = None
        self._texture: TextureHandle | None = None
        self._pipeline: PipelineHandle | None = None

    def capture(self, width: int, height: int) -> AgentCapture:
        self._ensure_resources(width, height)
        surface = self._surface
        texture = self._texture
        pipeline = self._pipeline
        if surface is None or texture is None or pipeline is None:
            raise AssertionError("builder renderer resources were not initialized")
        sources: list[SpriteExtractionSource] = []
        world = self._session.world
        for entity, item in world.components(BuilderObject):
            transform = world.get(entity, BuilderTransform)
            sources.append(
                SpriteExtractionSource(
                    texture,
                    entity.index,
                    entity.generation,
                    transform.x,
                    transform.y,
                    transform.x,
                    transform.y,
                    0.0,
                    0.0,
                    transform.width,
                    transform.height,
                    tint=_kind_color(item.kind),
                    layer=_kind_layer(item.kind),
                )
            )
        frame = self._extractor.extract_sprites(
            sources,
            completed_ticks=self._session.completed_ticks,
            interpolation_alpha=1.0,
            camera=Camera2D(viewport_width=24.0, viewport_height=14.0),
        )
        commands = self._extractor.build_command_list(
            frame,
            target=surface,
            pipeline=pipeline,
            label="agent-world-builder-capture",
        )
        self._device.submit((commands,))
        self._device.poll()
        image = self._device.capture_surface(surface)
        return AgentCapture(image.width, image.height, image.pixels)

    def close(self) -> None:
        self._device.close()

    def _ensure_resources(self, width: int, height: int) -> None:
        if self._surface is None:
            self._surface = self._device.create_surface(
                SurfaceDescriptor(
                    width,
                    height,
                    TextureFormat.RGBA8_UNORM,
                    SurfaceKind.OFFSCREEN,
                    "Agent World Builder",
                )
            )
            self._texture = self._device.create_texture(
                TextureDescriptor(
                    1,
                    1,
                    TextureFormat.RGBA8_UNORM,
                    TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
                    label="builder-white",
                ),
                TextureData(b"\xff\xff\xff\xff", 4),
            )
            self._pipeline = self._device.create_pipeline(
                PipelineDescriptor(TextureFormat.RGBA8_UNORM)
            )
            return
        self._device.resize_surface(self._surface, width, height)


@dataclass(frozen=True, slots=True)
class AgentWorldBuilder:
    """Owned Agent World Builder composition."""

    service: AgentCommandService
    codec: SnapshotCodec

    def close(self) -> None:
        self.service.close()


def create_agent_world_builder(
    *,
    write: bool = False,
    actor: CommandActor | None = None,
    device: RenderDevice | None = None,
    capture_provider: AgentCaptureProvider | None = None,
    limits: AgentLimits | None = None,
    clock: Clock | None = None,
) -> AgentWorldBuilder:
    """Create one explicit built-in sample; no project data selects Python code."""

    components = ComponentRegistry((BuilderTransform, BuilderObject))
    resources = ResourceRegistry()
    authority = AuthorityResourceRegistry()
    executor = BuilderTickExecutor()
    session = WorldSession(
        "agent-world-builder",
        World(components),
        ResourceStore(resources),
        authority_resources=authority,
        random_streams=RandomStreams(BUILDER_SEED),
        tick_executor=executor,
    )
    codec = SnapshotCodec(
        components,
        resources,
        authority_resources=authority,
        binding=SnapshotBinding(
            BUILDER_PROJECT_SCHEMA,
            BUILDER_LOCK_HASH,
            BUILDER_PLATFORM_PROFILE,
        ),
    )
    if device is not None and capture_provider is not None:
        raise ValueError("builder composition accepts one capture provider")
    capture = BuilderRenderCapture(session, device) if device is not None else capture_provider
    service = AgentCommandService(
        session,
        codec,
        AgentProject(
            "agent-world-builder",
            "Agent-World-Builder",
            BUILDER_PROJECT_SCHEMA,
            BUILDER_LOCK_HASH,
            BUILDER_PLATFORM_PROFILE,
            "Typed room, player, light, effect, and prop layout acceptance world.",
        ),
        actor or CommandActor("agent", "world-builder"),
        capabilities=AgentCapabilities(write=write, capture=capture is not None, tests=True),
        limits=limits,
        clock=clock,
        capture_provider=capture,
        test_provider=BuilderTestProvider(session),
        telemetry_provider=BuilderTelemetryProvider(session),
        timeline_id="agent-world-builder-session",
    )
    return AgentWorldBuilder(service, codec)


def builder_create_transaction(
    actor: CommandActor,
    *,
    expected_world_hash: str,
    transaction_id: str = "builder.create-layout",
) -> CommandTransaction:
    """Return the canonical typed transaction used by the acceptance loop."""

    objects = (
        ("room", "room", 0.0, 0.0, 20.0, 12.0),
        ("player", "player", 0.0, 0.0, 1.0, 1.0),
        ("key-light", "light", -6.0, -4.0, 1.4, 1.4),
        ("console", "prop", 4.0, 2.0, 2.0, 1.2),
        ("crate", "prop", -4.0, 2.0, 1.5, 1.5),
        ("beacon", "effect", 0.0, -3.0, 1.0, 1.0),
    )
    commands = tuple(
        CommandEnvelope(
            command_id=f"{transaction_id}.{index}",
            transaction_id=transaction_id,
            actor=actor,
            operation="entity.spawn",
            expected_world_hash=expected_world_hash,
            arguments={
                "alias": alias,
                "components": [
                    _component(
                        BUILDER_TRANSFORM_ID,
                        {"x": x, "y": y, "width": width, "height": height},
                    ),
                    _component(BUILDER_OBJECT_ID, {"name": alias, "kind": kind}),
                ],
            },
        )
        for index, (alias, kind, x, y, width, height) in enumerate(objects)
    )
    return CommandTransaction(commands, "agent-world-builder")


def builder_adjust_transaction(
    actor: CommandActor,
    *,
    expected_world_hash: str,
    player_entity: str,
) -> CommandTransaction:
    """Move the player after capture metadata has been inspected."""

    index_text, generation_text = player_entity.split(":", 1)
    transaction_id = "builder.adjust-layout"
    return CommandTransaction(
        (
            CommandEnvelope(
                command_id=f"{transaction_id}.player",
                transaction_id=transaction_id,
                actor=actor,
                operation="component.patch",
                expected_world_hash=expected_world_hash,
                arguments={
                    "entity": {
                        "index": int(index_text),
                        "generation": int(generation_text),
                    },
                    "type_id": str(BUILDER_TRANSFORM_ID),
                    "version": 1,
                    "changes": {"x": 1.0, "y": 0.5},
                },
            ),
        ),
        "agent-world-builder",
    )


def run_agent_world_builder_acceptance(service: AgentCommandService) -> dict[str, JsonValue]:
    """Run the complete clean typed-tool loop and return a structured summary."""

    project = service.call("project_describe")
    before = service.call("world_snapshot")
    transaction = builder_create_transaction(
        service.actor,
        expected_world_hash=service.session.state_hash,
    )
    validation = service.call("transaction_validate", {"transaction": transaction.as_dict()})
    applied = service.call("transaction_apply", {"transaction": transaction.as_dict()})
    ticked = service.call(
        "world_tick",
        {
            "request_id": "builder.advance",
            "count": 3,
            "expected_world_hash": service.session.state_hash,
        },
    )
    capture = service.call(
        "render_capture",
        {"width": 320, "height": 180, "include_pixels": False},
    )
    query = service.call(
        "world_query",
        {"include": [str(BUILDER_OBJECT_ID), str(BUILDER_TRANSFORM_ID)], "limit": 32},
    )
    player_entity = _player_entity(query)
    adjustment = builder_adjust_transaction(
        service.actor,
        expected_world_hash=service.session.state_hash,
        player_entity=player_entity,
    )
    adjusted = service.call("transaction_apply", {"transaction": adjustment.as_dict()})
    diff = service.call(
        "world_diff",
        {"before_snapshot": _required_text(before, "snapshot")},
    )
    tests = service.call("test_run")
    telemetry = service.call("telemetry_get")
    replay = service.replay_bytes()
    return {
        "protocol": "ludoweave.sample.agent_world_builder/1",
        "project_protocol": _required_text(project, "protocol"),
        "validation_status": _receipt_status(validation),
        "apply_status": _receipt_status(applied),
        "adjust_status": _receipt_status(adjusted),
        "ticks": _required_int(ticked, "completed_ticks"),
        "capture_sha256": _required_text(capture, "pixel_sha256"),
        "capture_width": _required_int(capture, "width"),
        "capture_height": _required_int(capture, "height"),
        "query_matches": _required_int(query, "matched"),
        "diff_changed": _diff_changed(diff),
        "tests_passed": _required_bool(tests, "passed"),
        "replay_sha256": f"sha256:{sha256(replay).hexdigest()}",
        "replay_batches": _required_int(telemetry, "replay_batches"),
        "state_hash": service.session.state_hash,
    }


def _component(type_id: UUID, values: Mapping[str, object]) -> dict[str, object]:
    return {"type_id": str(type_id), "version": 1, "values": dict(values)}


def _builder_records(
    world: WorldStore,
) -> tuple[tuple[BuilderTransform, BuilderObject], ...]:
    return tuple(
        (world.get(entity, BuilderTransform), item)
        for entity, item in world.components(BuilderObject)
    )


def _inside(item: BuilderTransform, room: BuilderTransform) -> bool:
    return (
        item.x - item.width / 2 >= room.x - room.width / 2
        and item.x + item.width / 2 <= room.x + room.width / 2
        and item.y - item.height / 2 >= room.y - room.height / 2
        and item.y + item.height / 2 <= room.y + room.height / 2
    )


def _overlap(left: BuilderTransform, right: BuilderTransform) -> bool:
    return (
        abs(left.x - right.x) < (left.width + right.width) / 2
        and abs(left.y - right.y) < (left.height + right.height) / 2
    )


def _kind_color(kind: str) -> Color:
    return {
        "room": Color(0.12, 0.16, 0.22, 1.0),
        "player": Color(0.2, 0.8, 1.0, 1.0),
        "light": Color(1.0, 0.9, 0.3, 1.0),
        "prop": Color(0.7, 0.42, 0.2, 1.0),
        "effect": Color(0.8, 0.3, 1.0, 1.0),
    }[kind]


def _kind_layer(kind: str) -> int:
    return 0 if kind == "room" else 2 if kind == "player" else 1


def _player_entity(query: Mapping[str, JsonValue]) -> str:
    entities = query.get("entities")
    if not isinstance(entities, list):
        raise AssertionError("builder query result has no entity list")
    for value in entities:
        if not isinstance(value, dict):
            continue
        entity = cast(dict[str, JsonValue], value)
        components = entity.get("components")
        if not isinstance(components, list):
            continue
        for component_value in components:
            if not isinstance(component_value, dict):
                continue
            component = cast(dict[str, JsonValue], component_value)
            if component.get("type_id") != str(BUILDER_OBJECT_ID):
                continue
            values = component.get("values")
            if isinstance(values, dict) and values.get("kind") == "player":
                return _required_text(entity, "entity")
    raise AssertionError("builder query did not return a player")


def _receipt_status(value: Mapping[str, JsonValue]) -> str:
    receipt = value.get("receipt")
    if not isinstance(receipt, dict):
        raise AssertionError("builder result has no receipt")
    return _required_text(receipt, "status")


def _diff_changed(value: Mapping[str, JsonValue]) -> bool:
    changes = value.get("changes")
    if not isinstance(changes, dict):
        raise AssertionError("builder result has no semantic diff")
    created = changes.get("created_entities")
    return isinstance(created, list) and bool(created)


def _required_text(value: Mapping[str, JsonValue], field: str) -> str:
    item = value.get(field)
    if type(item) is not str:
        raise AssertionError(f"builder result field {field!r} is not text")
    return item


def _required_int(value: Mapping[str, JsonValue], field: str) -> int:
    item = value.get(field)
    if type(item) is not int:
        raise AssertionError(f"builder result field {field!r} is not an integer")
    return item


def _required_bool(value: Mapping[str, JsonValue], field: str) -> bool:
    item = value.get(field)
    if type(item) is not bool:
        raise AssertionError(f"builder result field {field!r} is not a boolean")
    return item
