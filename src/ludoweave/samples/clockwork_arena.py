"""Clockwork Arena: one deterministic ECS-backed M4 gameplay vertical slice."""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from hashlib import sha256
from math import hypot
from typing import cast
from uuid import UUID

from ludoweave.app import ActionValue, InputSnapshot, InputSource, VirtualInputSource
from ludoweave.collision import (
    Aabb,
    Circle,
    Collider,
    SpatialGrid,
    Vec2,
    overlaps,
    resolve_kinematic_aabb,
)
from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs import (
    ComponentRegistry,
    EntityId,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    World,
    WorldStore,
    component,
)
from ludoweave.render import (
    Camera2D,
    Color,
    PresentationFrame,
    RenderExtractor,
    SpriteExtractionSource,
    TextureHandle,
)
from ludoweave.world import (
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    RandomStreams,
    ReceiptStatus,
    SnapshotBinding,
    SnapshotCodec,
    TransactionReceipt,
    TransactionService,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue

ARENA_FIXED_SEED = 0xC10C_A11E
ARENA_PROJECT_SCHEMA = f"sha256:{sha256(b'clockwork-arena-schema/1').hexdigest()}"
ARENA_LOCK_HASH = f"sha256:{sha256(b'ludoweave-lock-m4').hexdigest()}"
ARENA_PLATFORM_PROFILE = "cpython-standard-d1"

_TRANSFORM_ID = UUID("08f5b82b-0fc3-4fe2-af20-d8cae4af28c7")
_PLAYER_ID = UUID("1a86ee6c-e1f6-4c0f-9132-6eb31d8fb297")
_ENEMY_ID = UUID("68b2f174-9a75-4f60-8bb6-c1a15e5414b6")
_PROJECTILE_ID = UUID("aef70930-b56c-4b91-a934-d4161809a47d")
_ARENA_STATE_ID = UUID("e26435d0-7fbc-46c1-ab2b-d1d5d79ab4f4")
_HALF_WIDTH = 16.0
_HALF_HEIGHT = 9.0
_PLAYER_SPEED = 0.22
_ENEMY_SPEED = 0.03
_PROJECTILE_SPEED = 0.35
_WAVE_INTERVAL = 300


class ArenaError(LudoWeaveError):
    """Raised when the sample cannot preserve its deterministic contract."""


@component(type_id=_TRANSFORM_ID)
@dataclass(frozen=True, slots=True)
class Transform:
    previous_x: float
    previous_y: float
    x: float
    y: float


@component(type_id=_PLAYER_ID)
@dataclass(frozen=True, slots=True)
class Player:
    health: int
    cooldown: int


@component(type_id=_ENEMY_ID)
@dataclass(frozen=True, slots=True)
class Enemy:
    health: int
    wave: int


@component(type_id=_PROJECTILE_ID)
@dataclass(frozen=True, slots=True)
class Projectile:
    velocity_x: float
    velocity_y: float
    remaining_ticks: int
    damage: int


@dataclass(frozen=True, slots=True)
class ArenaState:
    score: int = 0
    wave: int = 0
    next_wave_tick: int = 0
    enemies_spawned: int = 0
    enemies_destroyed: int = 0
    shots_fired: int = 0
    damage_taken: int = 0
    restarts: int = 0
    game_over: bool = False
    stress: int = 1

    def __post_init__(self) -> None:
        for field in (
            "score",
            "wave",
            "next_wave_tick",
            "enemies_spawned",
            "enemies_destroyed",
            "shots_fired",
            "damage_taken",
            "restarts",
        ):
            value = getattr(self, field)
            if type(value) is not int or value < 0:
                raise _arena_error("arena counters must be non-negative integers", field=field)
        if type(self.game_over) is not bool:
            raise _arena_error("arena game-over state must be an exact boolean", field="game_over")
        if type(self.stress) is not int or not 1 <= self.stress <= 16:
            raise _arena_error("arena stress must be between one and sixteen", field="stress")


def _copy_state(value: ArenaState) -> ArenaState:
    return replace(value)


ARENA_STATE = ResourceSpec("clockwork_arena.state", ArenaState, _copy_state)


def _encode_state(value: ArenaState) -> object:
    return {
        "damage_taken": value.damage_taken,
        "enemies_destroyed": value.enemies_destroyed,
        "enemies_spawned": value.enemies_spawned,
        "game_over": value.game_over,
        "next_wave_tick": value.next_wave_tick,
        "restarts": value.restarts,
        "score": value.score,
        "shots_fired": value.shots_fired,
        "stress": value.stress,
        "wave": value.wave,
    }


def _decode_state(value: JsonValue) -> ArenaState:
    if type(value) is not dict:
        raise ValueError("arena state must be an object")
    document = cast(dict[str, object], value)
    expected = {
        "damage_taken",
        "enemies_destroyed",
        "enemies_spawned",
        "game_over",
        "next_wave_tick",
        "restarts",
        "score",
        "shots_fired",
        "stress",
        "wave",
    }
    if set(document) != expected:
        raise ValueError("arena state fields do not match")
    return ArenaState(
        score=_int(document["score"]),
        wave=_int(document["wave"]),
        next_wave_tick=_int(document["next_wave_tick"]),
        enemies_spawned=_int(document["enemies_spawned"]),
        enemies_destroyed=_int(document["enemies_destroyed"]),
        shots_fired=_int(document["shots_fired"]),
        damage_taken=_int(document["damage_taken"]),
        restarts=_int(document["restarts"]),
        game_over=_bool(document["game_over"]),
        stress=_int(document["stress"]),
    )


ARENA_STATE_SCHEMA = AuthorityResourceSchema(
    _ARENA_STATE_ID,
    1,
    ARENA_STATE,
    "clockwork_arena.state/json-v1",
    _encode_state,
    _decode_state,
)


class ArenaTickExecutor:
    """Application-owned kernel invoked only against a staged world record."""

    __slots__ = ("_input_source",)

    def __init__(self, input_source: InputSource) -> None:
        self._input_source = input_source

    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None:
        snapshot = self._sample(tick)
        state = resources.require(ARENA_STATE)
        if state.game_over and (snapshot.just_pressed("restart") or snapshot.pressed("restart")):
            state = replace(self._restart(world, state), next_wave_tick=tick)
        if state.game_over:
            resources.replace(ARENA_STATE, state)
            return

        state = self._spawn_wave(world, random_streams, tick, state)
        player_id, player_transform, player = self._player(world)
        player_transform, player = self._move_player(
            world, player_id, player_transform, player, snapshot
        )
        state = self._fire(world, player_transform, player_id, player, snapshot, state)
        player = world.get(player_id, Player)
        state, player = self._move_enemies(world, player_transform, player, state)
        state = self._move_projectiles(world, state)
        if player.health <= 0:
            state = replace(state, game_over=True)
        resources.replace(ARENA_STATE, state)

    def _sample(self, tick: int) -> InputSnapshot:
        try:
            snapshot = self._input_source.snapshot_for_tick(tick)
        except Exception as error:
            raise _arena_error(
                "arena input source failed",
                field="input",
                cause_type=type(error).__name__,
                code="sample.arena.input_failed",
            ) from error
        if type(snapshot) is not InputSnapshot or snapshot.tick != tick:
            raise _arena_error(
                "arena input source returned a mismatched snapshot",
                field="input",
                code="sample.arena.input_mismatch",
            )
        return snapshot

    @staticmethod
    def _player(world: WorldStore) -> tuple[EntityId, Transform, Player]:
        players = world.components(Player)
        if len(players) != 1:
            raise _arena_error("arena requires exactly one player", field="player")
        entity_id, player = players[0]
        return entity_id, world.get(entity_id, Transform), player

    @staticmethod
    def _move_player(
        world: WorldStore,
        player_id: EntityId,
        transform: Transform,
        player: Player,
        snapshot: InputSnapshot,
    ) -> tuple[Transform, Player]:
        axis_x, axis_y = snapshot.axis2d("move")
        moving = Aabb(Vec2(transform.x, transform.y), 0.45, 0.45)
        walls = _arena_walls()
        resolved = resolve_kinematic_aabb(
            moving,
            Vec2(axis_x * _PLAYER_SPEED, axis_y * _PLAYER_SPEED),
            walls,
        )
        updated_transform = Transform(
            transform.x,
            transform.y,
            resolved.shape.center.x,
            resolved.shape.center.y,
        )
        updated_player = Player(player.health, max(0, player.cooldown - 1))
        world.replace(player_id, updated_transform)
        world.replace(player_id, updated_player)
        return updated_transform, updated_player

    @staticmethod
    def _fire(
        world: WorldStore,
        transform: Transform,
        player_id: EntityId,
        player: Player,
        snapshot: InputSnapshot,
        state: ArenaState,
    ) -> ArenaState:
        if not snapshot.pressed("fire") or player.cooldown > 0:
            return state
        aim_x, aim_y = snapshot.axis2d("aim")
        if aim_x == 0.0 and aim_y == 0.0:
            aim_x, aim_y = snapshot.axis2d("pointer")
        enemies = world.components(Enemy)
        if snapshot.pressed("aim.auto") and enemies:
            targets = tuple(
                (
                    (world.get(entity_id, Transform).x - transform.x) ** 2
                    + (world.get(entity_id, Transform).y - transform.y) ** 2,
                    entity_id.index,
                    world.get(entity_id, Transform),
                )
                for entity_id, _enemy in enemies
            )
            target = min(targets, key=lambda item: (item[0], item[1]))[2]
            aim_x = target.x - transform.x
            aim_y = target.y - transform.y
        magnitude = hypot(aim_x, aim_y)
        if magnitude > 0.0:
            velocity_x = _PROJECTILE_SPEED * aim_x / magnitude
            velocity_y = _PROJECTILE_SPEED * aim_y / magnitude
        else:
            velocity_x = 0.0
            velocity_y = _PROJECTILE_SPEED
        world.spawn(
            Transform(transform.x, transform.y, transform.x, transform.y),
            Projectile(velocity_x, velocity_y, 80, 1),
        )
        world.replace(player_id, Player(player.health, 6))
        return replace(state, shots_fired=state.shots_fired + 1)

    @staticmethod
    def _spawn_wave(
        world: WorldStore,
        random_streams: RandomStreams,
        tick: int,
        state: ArenaState,
    ) -> ArenaState:
        if tick < state.next_wave_tick:
            return state
        wave = state.wave + 1
        capacity = max(0, 24 - len(world.components(Enemy)))
        count = min(2 + wave * state.stress, capacity)
        for _ in range(count):
            side = random_streams.randbelow("clockwork.spawn.side", 4)
            offset = float(random_streams.randbelow("clockwork.spawn.offset", 61) - 30) / 4.0
            if side == 0:
                x, y = -_HALF_WIDTH + 1.0, offset
            elif side == 1:
                x, y = _HALF_WIDTH - 1.0, offset
            elif side == 2:
                x, y = offset, -_HALF_HEIGHT + 1.0
            else:
                x, y = offset, _HALF_HEIGHT - 1.0
            world.spawn(Transform(x, y, x, y), Enemy(1 + wave // 5, wave))
        return replace(
            state,
            wave=wave,
            next_wave_tick=state.next_wave_tick + _WAVE_INTERVAL,
            enemies_spawned=state.enemies_spawned + count,
        )

    @staticmethod
    def _move_enemies(
        world: WorldStore,
        player_transform: Transform,
        player: Player,
        state: ArenaState,
    ) -> tuple[ArenaState, Player]:
        destroyed: list[EntityId] = []
        health = player.health
        for entity_id, _enemy in world.components(Enemy):
            transform = world.get(entity_id, Transform)
            dx = _step(player_transform.x - transform.x, _ENEMY_SPEED)
            dy = _step(player_transform.y - transform.y, _ENEMY_SPEED)
            updated = Transform(transform.x, transform.y, transform.x + dx, transform.y + dy)
            world.replace(entity_id, updated)
            if overlaps(
                Circle(Vec2(updated.x, updated.y), 0.42),
                Circle(Vec2(player_transform.x, player_transform.y), 0.45),
            ):
                destroyed.append(entity_id)
                health -= 1
        for entity_id in destroyed:
            world.destroy(entity_id)
        updated_player = Player(max(0, health), world.components(Player)[0][1].cooldown)
        player_id = world.components(Player)[0][0]
        world.replace(player_id, updated_player)
        return (
            replace(state, damage_taken=state.damage_taken + len(destroyed)),
            updated_player,
        )

    @staticmethod
    def _move_projectiles(world: WorldStore, state: ArenaState) -> ArenaState:
        enemies = world.components(Enemy)
        grid_colliders = tuple(
            Collider(
                entity_id.index,
                Circle(
                    Vec2(world.get(entity_id, Transform).x, world.get(entity_id, Transform).y),
                    0.42,
                ),
            )
            for entity_id, _ in enemies
        )
        enemy_by_index = {entity_id.index: (entity_id, enemy) for entity_id, enemy in enemies}
        grid = SpatialGrid(1.5)
        grid.rebuild(grid_colliders)
        destroyed_enemies: set[EntityId] = set()
        destroyed_projectiles: set[EntityId] = set()
        for projectile_id, projectile in world.components(Projectile):
            transform = world.get(projectile_id, Transform)
            x = transform.x + projectile.velocity_x
            y = transform.y + projectile.velocity_y
            remaining = projectile.remaining_ticks - 1
            world.replace(projectile_id, Transform(transform.x, transform.y, x, y))
            if remaining <= 0 or abs(x) > _HALF_WIDTH or abs(y) > _HALF_HEIGHT:
                destroyed_projectiles.add(projectile_id)
                continue
            projectile_shape = Circle(Vec2(x, y), 0.35)
            hit_ids = grid.query(projectile_shape)
            if not hit_ids:
                world.replace(
                    projectile_id,
                    Projectile(
                        projectile.velocity_x,
                        projectile.velocity_y,
                        remaining,
                        projectile.damage,
                    ),
                )
                continue
            enemy_id, enemy = enemy_by_index[min(hit_ids)]
            if enemy_id not in destroyed_enemies:
                health = enemy.health - projectile.damage
                if health <= 0:
                    destroyed_enemies.add(enemy_id)
                else:
                    world.replace(enemy_id, Enemy(health, enemy.wave))
            destroyed_projectiles.add(projectile_id)
        for entity_id in sorted(
            destroyed_projectiles, key=lambda item: (item.index, item.generation)
        ):
            world.destroy(entity_id)
        for entity_id in sorted(destroyed_enemies, key=lambda item: (item.index, item.generation)):
            if entity_id not in destroyed_projectiles:
                world.destroy(entity_id)
        count = len(destroyed_enemies)
        return replace(
            state,
            score=state.score + count * 100,
            enemies_destroyed=state.enemies_destroyed + count,
        )

    @staticmethod
    def _restart(world: WorldStore, state: ArenaState) -> ArenaState:
        for entity_id, _ in world.components(Enemy):
            world.destroy(entity_id)
        for entity_id, _ in world.components(Projectile):
            world.destroy(entity_id)
        player_id, transform, _ = ArenaTickExecutor._player(world)
        world.replace(player_id, Transform(transform.x, transform.y, 0.0, 0.0))
        world.replace(player_id, Player(20, 0))
        return ArenaState(restarts=state.restarts + 1, stress=state.stress)


@dataclass(frozen=True, slots=True)
class ArenaSummary:
    ticks: int
    state_hash: str
    score: int
    wave: int
    player_health: int
    enemies_active: int
    projectiles_active: int
    enemies_spawned: int
    enemies_destroyed: int
    shots_fired: int
    damage_taken: int
    restarts: int
    game_over: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "damage_taken": self.damage_taken,
            "enemies_active": self.enemies_active,
            "enemies_destroyed": self.enemies_destroyed,
            "enemies_spawned": self.enemies_spawned,
            "game_over": self.game_over,
            "player_health": self.player_health,
            "projectiles_active": self.projectiles_active,
            "restarts": self.restarts,
            "score": self.score,
            "shots_fired": self.shots_fired,
            "state_hash": self.state_hash,
            "ticks": self.ticks,
            "wave": self.wave,
        }


class ClockworkArena:
    """Composition root around one authoritative session and transaction service."""

    __slots__ = ("_service", "codec", "kernel", "session")

    def __init__(
        self,
        session: WorldSession,
        codec: SnapshotCodec,
        kernel: ArenaTickExecutor,
    ) -> None:
        self.session = session
        self.codec = codec
        self.kernel = kernel
        self._service = TransactionService(session)

    def tick(self) -> TransactionReceipt:
        receipt = self._service.apply(arena_tick_transaction(self.session))
        if receipt.status is not ReceiptStatus.COMMITTED:
            diagnostic = receipt.diagnostics[0] if receipt.diagnostics else None
            cause = None if diagnostic is None else diagnostic.code
            raise _arena_error(
                "clockwork arena tick transaction was rejected",
                field="transaction",
                cause_type=cause,
                code="sample.arena.tick_rejected",
            )
        return receipt

    def run(self, ticks: int) -> ArenaSummary:
        if type(ticks) is not int or ticks < 0:
            raise _arena_error("arena tick count must be non-negative", field="ticks")
        for _ in range(ticks):
            self.tick()
        return self.summary()

    def summary(self) -> ArenaSummary:
        state = self.session.resources.require(ARENA_STATE)
        world = self.session.world
        players = world.components(Player)
        if len(players) != 1:
            raise _arena_error("arena summary requires exactly one player", field="player")
        return ArenaSummary(
            ticks=self.session.completed_ticks,
            state_hash=self.session.state_hash,
            score=state.score,
            wave=state.wave,
            player_health=players[0][1].health,
            enemies_active=len(world.components(Enemy)),
            projectiles_active=len(world.components(Projectile)),
            enemies_spawned=state.enemies_spawned,
            enemies_destroyed=state.enemies_destroyed,
            shots_fired=state.shots_fired,
            damage_taken=state.damage_taken,
            restarts=state.restarts,
            game_over=state.game_over,
        )

    def presentation(self, texture: TextureHandle) -> PresentationFrame:
        """Extract immutable renderer-neutral sprites from a detached world view."""

        if type(texture) is not TextureHandle:
            raise _arena_error("arena presentation requires a texture handle", field="texture")
        world = self.session.world
        sources: list[SpriteExtractionSource] = []
        for component_type, width, height, tint, layer in (
            (Player, 0.9, 0.9, Color(0.25, 0.8, 1.0, 1.0), 2),
            (Enemy, 0.84, 0.84, Color(1.0, 0.25, 0.2, 1.0), 1),
            (Projectile, 0.3, 0.3, Color(1.0, 0.9, 0.2, 1.0), 3),
        ):
            for entity_id, _ in world.components(component_type):
                transform = world.get(entity_id, Transform)
                sources.append(
                    SpriteExtractionSource(
                        texture,
                        entity_id.index,
                        entity_id.generation,
                        transform.previous_x,
                        transform.previous_y,
                        transform.x,
                        transform.y,
                        0.0,
                        0.0,
                        width,
                        height,
                        tint=tint,
                        layer=layer,
                    )
                )
        return RenderExtractor().extract_sprites(
            sources,
            completed_ticks=self.session.completed_ticks,
            interpolation_alpha=1.0,
            camera=Camera2D(viewport_width=34.0, viewport_height=20.0),
        )


def create_clockwork_arena(
    input_source: InputSource,
    *,
    seed: int = ARENA_FIXED_SEED,
    stress: int = 1,
) -> ClockworkArena:
    """Compose one Arena world; the returned session owns all canonical state."""

    state = ArenaState(stress=stress)
    components = ComponentRegistry((Transform, Player, Enemy, Projectile))
    resources = ResourceRegistry((ARENA_STATE,))
    authority = AuthorityResourceRegistry((ARENA_STATE_SCHEMA,))
    world = World(components)
    world.spawn(Transform(0.0, 0.0, 0.0, 0.0), Player(20, 0))
    kernel = ArenaTickExecutor(input_source)
    binding = SnapshotBinding(
        ARENA_PROJECT_SCHEMA,
        ARENA_LOCK_HASH,
        ARENA_PLATFORM_PROFILE,
    )
    session = WorldSession(
        "clockwork-arena",
        world,
        ResourceStore(resources, ((ARENA_STATE, state),)),
        authority_resources=authority,
        random_streams=RandomStreams(seed),
        tick_executor=kernel,
    )
    codec = SnapshotCodec(
        components,
        resources,
        authority_resources=authority,
        binding=binding,
    )
    return ClockworkArena(session, codec, kernel)


def arena_tick_transaction(session: WorldSession) -> CommandTransaction:
    tick = session.completed_ticks
    transaction_id = f"arena.tick-{tick}"
    return CommandTransaction(
        (
            CommandEnvelope(
                command_id=f"{transaction_id}.advance",
                transaction_id=transaction_id,
                actor=CommandActor("sample", "clockwork-arena"),
                operation="world.tick",
                arguments={"count": 1},
                expected_world_hash=session.state_hash,
            ),
        ),
        session.world_id,
    )


def clockwork_input(ticks: int) -> VirtualInputSource:
    """Return the deterministic headless/autoplay action timeline."""

    if type(ticks) is not int or ticks < 0:
        raise _arena_error("input timeline tick count must be non-negative", field="ticks")
    timeline: dict[int, Mapping[str, ActionValue]] = {}
    for tick in range(ticks):
        phase = (tick // 180) % 4
        move_x = 1.0 if phase == 0 else -1.0 if phase == 2 else 0.0
        move_y = 1.0 if phase == 1 else -1.0 if phase == 3 else 0.0
        aim_phase = (tick // 90) % 4
        aim_x = 1.0 if aim_phase == 0 else -1.0 if aim_phase == 2 else 0.0
        aim_y = 1.0 if aim_phase == 1 else -1.0 if aim_phase == 3 else 0.0
        timeline[tick] = {
            "aim.x": aim_x,
            "aim.y": aim_y,
            "aim.auto": True,
            "fire": tick % 5 == 0,
            "move.x": move_x,
            "move.y": move_y,
            "restart": True,
        }
    return VirtualInputSource(timeline)


def _arena_walls() -> tuple[Collider, ...]:
    return (
        Collider(0, Aabb(Vec2(-_HALF_WIDTH - 0.5, 0.0), 0.5, _HALF_HEIGHT + 1.0)),
        Collider(1, Aabb(Vec2(_HALF_WIDTH + 0.5, 0.0), 0.5, _HALF_HEIGHT + 1.0)),
        Collider(2, Aabb(Vec2(0.0, -_HALF_HEIGHT - 0.5), _HALF_WIDTH + 1.0, 0.5)),
        Collider(3, Aabb(Vec2(0.0, _HALF_HEIGHT + 0.5), _HALF_WIDTH + 1.0, 0.5)),
    )


def _step(delta: float, maximum: float) -> float:
    return min(maximum, max(-maximum, delta))


def _int(value: object) -> int:
    if type(value) is not int or value < 0:
        raise ValueError("expected non-negative integer")
    return value


def _bool(value: object) -> bool:
    if type(value) is not bool:
        raise ValueError("expected boolean")
    return value


def _arena_error(
    message: str,
    *,
    field: str,
    cause_type: str | None = None,
    code: str = "sample.arena.invalid_value",
) -> ArenaError:
    details: dict[str, str | int | float | bool | None] = {"field": field}
    if cause_type is not None:
        details["cause_type"] = cause_type
    return ArenaError(
        message,
        code=code,
        subsystem="sample",
        phase="clockwork_arena",
        details=details,
    )
