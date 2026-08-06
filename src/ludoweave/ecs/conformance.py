"""Installed, storage-neutral conformance evidence for WorldStore adapters."""

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Final, cast
from uuid import UUID

from ludoweave.core.errors import LudoWeaveError
from ludoweave.core.version import __version__
from ludoweave.ecs.component import ComponentRegistry, component
from ludoweave.ecs.entity import EntityId
from ludoweave.ecs.errors import (
    ActiveQueryError,
    CommandBufferStateError,
    ComponentAlreadyPresentError,
    DeferredCommandError,
    InvalidComponentValueError,
    InvalidQueryError,
    MissingComponentError,
    QueryLifecycleError,
    StaleEntityError,
    WorldError,
)
from ludoweave.ecs.world import WorldStore

WORLD_STORE_CONFORMANCE_PROTOCOL: Final = "ludoweave.world-store-conformance/1"
WORLD_STORE_CONFORMANCE_PROFILE: Final = "world-store-baseline/1"

_ADAPTER_ID = re.compile(r"[a-z][a-z0-9]*(?:[._-][a-z0-9]+){1,15}\Z")
_ERROR_CODE = re.compile(r"world_store_conformance\.[a-z0-9_.-]{1,103}\Z")
_CHECK_IDS = (
    "factory_registry",
    "empty_state",
    "direct_mutation_epochs",
    "copy_isolation",
    "entity_generations",
    "query_semantics",
    "writable_query_lifecycle",
    "command_buffer_atomicity",
    "clone_independence",
    "structured_failures",
)
_REQUIRED_METHODS = (
    "spawn",
    "destroy",
    "add",
    "replace",
    "patch",
    "remove",
    "has",
    "get",
    "entities",
    "components",
    "component_epoch",
    "component_structural_epoch",
    "clone",
    "query",
    "commands",
    "flush",
)
_REQUIRED_ATTRIBUTES = ("registry", "epoch", "structural_epoch")
_MISSING = object()


@component(type_id=UUID("19000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class _Counter:
    value: int = 0


@component(type_id=UUID("19000000-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class _Enabled:
    value: bool = True


@component(type_id=UUID("19000000-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class _Excluded:
    value: int = 0


class WorldStoreConformanceStatus(StrEnum):
    """Stable states used by installed world-store conformance reports."""

    PASS = "pass"
    FAIL = "fail"
    NOT_RUN = "not_run"


@dataclass(frozen=True, slots=True)
class WorldStoreConformanceCheck:
    """One deterministic check result without adapter diagnostic text."""

    check_id: str
    status: WorldStoreConformanceStatus
    code: str | None = None

    def __post_init__(self) -> None:
        if type(self.check_id) is not str or self.check_id not in _CHECK_IDS:
            raise _request_error("check_id")
        if type(self.status) is not WorldStoreConformanceStatus:
            raise _request_error("status")
        if self.status is WorldStoreConformanceStatus.PASS:
            if self.code is not None:
                raise _request_error("code")
        elif type(self.code) is not str or _ERROR_CODE.fullmatch(self.code) is None:
            raise _request_error("code")

    def as_dict(self) -> dict[str, object]:
        """Return one JSON-compatible check record."""

        return {"id": self.check_id, "status": self.status.value, "code": self.code}


@dataclass(frozen=True, slots=True)
class WorldStoreConformanceReport:
    """Versioned evidence from one explicit WorldStore factory invocation."""

    adapter_id: str
    status: WorldStoreConformanceStatus
    checks: tuple[WorldStoreConformanceCheck, ...]

    def __post_init__(self) -> None:
        _validate_adapter_id(self.adapter_id)
        if type(self.status) is not WorldStoreConformanceStatus or (
            self.status is WorldStoreConformanceStatus.NOT_RUN
        ):
            raise _request_error("status")
        try:
            checks = tuple(self.checks)
        except Exception as error:
            raise _request_error("checks") from error
        if (
            len(checks) != len(_CHECK_IDS)
            or any(type(check) is not WorldStoreConformanceCheck for check in checks)
            or tuple(check.check_id for check in checks) != _CHECK_IDS
        ):
            raise _request_error("checks")
        expected = (
            WorldStoreConformanceStatus.PASS
            if all(check.status is WorldStoreConformanceStatus.PASS for check in checks)
            else WorldStoreConformanceStatus.FAIL
        )
        if self.status is not expected:
            raise _request_error("status")
        object.__setattr__(self, "checks", checks)

    @property
    def passed(self) -> bool:
        """Whether every baseline check passed."""

        return self.status is WorldStoreConformanceStatus.PASS

    def as_dict(self) -> dict[str, object]:
        """Return deterministic, path-free, JSON-compatible evidence."""

        return {
            "protocol": WORLD_STORE_CONFORMANCE_PROTOCOL,
            "profile": WORLD_STORE_CONFORMANCE_PROFILE,
            "ludoweave_version": __version__,
            "adapter_id": self.adapter_id,
            "status": self.status.value,
            "checks": [check.as_dict() for check in self.checks],
        }

    def to_json(self) -> str:
        """Encode canonical presentation JSON with a trailing newline."""

        return (
            json.dumps(
                self.as_dict(),
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )


class _CheckFailure(Exception):
    __slots__ = ("code",)

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(slots=True)
class _RunState:
    world: WorldStore
    registry: ComponentRegistry
    first: EntityId | None = None
    replacement: EntityId | None = None
    third: EntityId | None = None


type _WorldImage = tuple[
    int,
    int,
    tuple[EntityId, ...],
    tuple[tuple[type[object], int, tuple[tuple[EntityId, object, int], ...]], ...],
]


def run_world_store_conformance(
    adapter_id: str,
    factory: Callable[[ComponentRegistry], WorldStore],
) -> WorldStoreConformanceReport:
    """Exercise one trusted, explicitly supplied WorldStore factory.

    The runner performs no discovery, import, installation, filesystem,
    subprocess, network, or global-registration operation. The existing
    WorldStore contract owns no external-resource lifecycle; factories that
    require one are outside this profile.
    """

    checked_id = _validate_adapter_id(adapter_id)
    if not callable(factory):
        raise _request_error("factory")

    checks: list[WorldStoreConformanceCheck] = []
    state: _RunState | None = None
    blocked = False
    try:
        registry = ComponentRegistry((_Counter, _Enabled, _Excluded))
        world_object = cast(object, factory(registry))
        if not all(
            callable(getattr(world_object, name, None)) for name in _REQUIRED_METHODS
        ) or any(
            getattr(world_object, name, _MISSING) is _MISSING for name in _REQUIRED_ATTRIBUTES
        ):
            raise _CheckFailure("world_store_conformance.invalid_adapter")
        world = cast(WorldStore, world_object)
        if world.registry is not registry:
            raise _CheckFailure("world_store_conformance.registry_identity")
        state = _RunState(world, registry)
    except Exception as error:
        checks.append(_failed("factory_registry", error))
        blocked = True
    else:
        checks.append(_passed("factory_registry"))

    stages: tuple[tuple[str, Callable[[_RunState], None]], ...] = (
        ("empty_state", _check_empty_state),
        ("direct_mutation_epochs", _check_direct_mutation_epochs),
        ("copy_isolation", _check_copy_isolation),
        ("entity_generations", _check_entity_generations),
        ("query_semantics", _check_query_semantics),
        ("writable_query_lifecycle", _check_writable_query_lifecycle),
        ("command_buffer_atomicity", _check_command_buffer_atomicity),
        ("clone_independence", _check_clone_independence),
        ("structured_failures", _check_structured_failures),
    )
    for check_id, operation in stages:
        if blocked or state is None:
            checks.append(_not_run(check_id))
            continue
        try:
            operation(state)
        except Exception as error:
            checks.append(_failed(check_id, error))
            blocked = True
        else:
            checks.append(_passed(check_id))

    frozen = tuple(checks)
    status = (
        WorldStoreConformanceStatus.PASS
        if all(check.status is WorldStoreConformanceStatus.PASS for check in frozen)
        else WorldStoreConformanceStatus.FAIL
    )
    return WorldStoreConformanceReport(checked_id, status, frozen)


def _check_empty_state(state: _RunState) -> None:
    world = state.world
    if world.epoch != 0 or world.structural_epoch != 0 or world.entities() != ():
        raise _CheckFailure("world_store_conformance.invalid_empty_state")
    for component_type in state.registry.component_types:
        if (
            world.components(component_type) != ()
            or world.component_structural_epoch(component_type) != 0
        ):
            raise _CheckFailure("world_store_conformance.invalid_empty_state")


def _check_direct_mutation_epochs(state: _RunState) -> None:
    world = state.world
    first_source = _Counter(1)
    first = world.spawn(first_source)
    first_source.value = 91
    second = world.spawn(_Counter(2), _Enabled(False), _Excluded(7))
    added_source = _Enabled(True)
    added = world.add(first, added_source)
    added_source.value = False
    added.value = False
    replaced_source = _Counter(3)
    replaced = world.replace(first, replaced_source)
    replaced_source.value = 93
    replaced.value = 94
    patched = world.patch(first, _Counter, value=4)
    patched.value = 95
    removed = world.remove(first, _Enabled)
    removed.value = False

    expected_entities = (EntityId(0, 0), EntityId(1, 0))
    if (
        first != expected_entities[0]
        or second != expected_entities[1]
        or world.entities() != expected_entities
        or world.epoch != 6
        or world.structural_epoch != 6
        or world.get(first, _Counter) != _Counter(4)
        or world.has(first, _Enabled)
        or world.get(second, _Counter) != _Counter(2)
        or world.get(second, _Enabled) != _Enabled(False)
        or world.get(second, _Excluded) != _Excluded(7)
        or world.component_epoch(first, _Counter) != 5
        or world.component_epoch(second, _Counter) != 2
        or world.component_epoch(second, _Enabled) != 2
        or world.component_structural_epoch(_Counter) != 2
        or world.component_structural_epoch(_Enabled) != 6
        or world.component_structural_epoch(_Excluded) != 2
    ):
        raise _CheckFailure("world_store_conformance.direct_mutation_mismatch")
    state.first = first
    state.replacement = second


def _check_copy_isolation(state: _RunState) -> None:
    world = state.world
    first = _required(state.first, "first")
    source = _Counter(11)
    returned = world.replace(first, source)
    source.value = 96
    returned.value = 97
    fetched = world.get(first, _Counter)
    fetched.value = 98
    inspected = world.components(_Counter)
    inspected[0][1].value = 99
    if (
        world.get(first, _Counter) != _Counter(11)
        or world.epoch != 7
        or world.structural_epoch != 6
        or world.component_epoch(first, _Counter) != 7
    ):
        raise _CheckFailure("world_store_conformance.copy_isolation_mismatch")


def _check_entity_generations(state: _RunState) -> None:
    world = state.world
    retired = _required(state.replacement, "replacement")
    world.destroy(retired)
    _expect_error(
        lambda: world.get(retired, _Counter),
        StaleEntityError,
        "ecs.stale_entity",
        "world_store_conformance.stale_entity_mismatch",
    )
    replacement = world.spawn(_Counter(20), _Enabled(False))
    if (
        replacement != EntityId(retired.index, retired.generation + 1)
        or world.epoch != 9
        or world.structural_epoch != 9
        or world.component_structural_epoch(_Counter) != 9
        or world.component_structural_epoch(_Enabled) != 9
        or world.component_structural_epoch(_Excluded) != 8
    ):
        raise _CheckFailure("world_store_conformance.entity_generation_mismatch")
    state.replacement = replacement


def _check_query_semantics(state: _RunState) -> None:
    world = state.world
    replacement = _required(state.replacement, "replacement")
    third = world.spawn(_Counter(30), _Enabled(True), _Excluded(1))
    baseline = world.epoch
    world.patch(replacement, _Counter, value=21)
    rows = list(
        world.query(_Counter, _Enabled)
        .without(_Excluded)
        .changed_since(baseline, _Counter)
        .stable()
        .rows()
    )
    expected = [(replacement, _Counter(21), _Enabled(False))]
    all_entities = [row[0] for row in world.query().stable().rows()]
    if rows != expected or all_entities != list(world.entities()):
        raise _CheckFailure("world_store_conformance.query_result_mismatch")
    rows[0][1].value = 100
    if world.get(replacement, _Counter) != _Counter(21) or world.epoch != 11:
        raise _CheckFailure("world_store_conformance.query_copy_mismatch")
    state.third = third


def _check_writable_query_lifecycle(state: _RunState) -> None:
    world = state.world
    replacement = _required(state.replacement, "replacement")
    before_structural = world.structural_epoch
    with (
        world.query(_Counter, _Enabled).without(_Excluded).writes(_Counter).stable().rows() as rows
    ):
        entity_id, counter, _enabled = next(rows)
        if entity_id != replacement:
            raise _CheckFailure("world_store_conformance.query_write_target")
        counter.value = 22
    if (
        world.get(replacement, _Counter) != _Counter(22)
        or world.epoch != 12
        or world.structural_epoch != before_structural
    ):
        raise _CheckFailure("world_store_conformance.query_writeback_mismatch")

    before = _world_image(state)
    with world.query(_Counter).writes(_Counter).stable().rows() as rows:
        next(rows)
        _expect_error(
            world.spawn,
            ActiveQueryError,
            "ecs.active_query",
            "world_store_conformance.query_ownership_mismatch",
        )
    if _world_image(state) != before:
        raise _CheckFailure("world_store_conformance.query_failure_mutated")

    cursor = world.query(_Counter).writes(_Counter).stable().rows()
    _expect_error(
        lambda: next(iter(cursor)),
        QueryLifecycleError,
        "ecs.query_lifecycle",
        "world_store_conformance.query_lifecycle_mismatch",
    )
    before = _world_image(state)
    with world.query(_Counter).writes(_Counter).stable().rows() as rows:
        _entity_id, counter = next(rows)
        counter.value = 101
        rows.abort()
    if _world_image(state) != before:
        raise _CheckFailure("world_store_conformance.query_abort_mutated")


def _check_command_buffer_atomicity(state: _RunState) -> None:
    world = state.world
    first = _required(state.first, "first")
    commands = world.commands()
    token = commands.spawn(_Counter(40))
    commands.add(token, _Enabled(True))
    commands.remove(token, _Counter)
    commands.destroy(first)
    result = world.flush(commands)
    created = result.resolve(token)
    if (
        result.command_count != 4
        or result.start_epoch != 12
        or result.end_epoch != 16
        or created != EntityId(3, 0)
        or len(commands) != 0
        or world.has(created, _Counter)
        or world.get(created, _Enabled) != _Enabled(True)
        or first in world.entities()
    ):
        raise _CheckFailure("world_store_conformance.command_result_mismatch")

    failing = world.commands()
    failed_token = failing.spawn(_Counter(50))
    failing.add(failed_token, _Counter(51))
    before = _world_image(state)
    for _ in range(2):
        _expect_error(
            lambda: world.flush(failing),
            DeferredCommandError,
            "ecs.deferred_command_failed",
            "world_store_conformance.command_failure_mismatch",
        )
        if len(failing) != 2 or _world_image(state) != before:
            raise _CheckFailure("world_store_conformance.command_failure_mutated")


def _check_clone_independence(state: _RunState) -> None:
    world = state.world
    replacement = _required(state.replacement, "replacement")
    before = _world_image(state)
    clone = world.clone()
    if (
        clone is world
        or clone.registry is not state.registry
        or _world_image_for(clone, state.registry) != before
    ):
        raise _CheckFailure("world_store_conformance.clone_state_mismatch")

    expected = EntityId(0, 1)
    if world.spawn() != expected or clone.spawn() != expected:
        raise _CheckFailure("world_store_conformance.clone_allocator_mismatch")
    clone.patch(replacement, _Counter, value=99)
    if world.get(replacement, _Counter) != _Counter(22) or clone.get(
        replacement, _Counter
    ) != _Counter(99):
        raise _CheckFailure("world_store_conformance.clone_isolation_mismatch")

    foreign = world.commands()
    world_before = _world_image(state)
    clone_before = _world_image_for(clone, state.registry)
    _expect_error(
        lambda: clone.flush(foreign),
        CommandBufferStateError,
        "ecs.command_buffer_wrong_world",
        "world_store_conformance.command_owner_mismatch",
    )
    if (
        _world_image(state) != world_before
        or _world_image_for(clone, state.registry) != clone_before
    ):
        raise _CheckFailure("world_store_conformance.foreign_command_mutated")


def _check_structured_failures(state: _RunState) -> None:
    world = state.world
    replacement = _required(state.replacement, "replacement")
    stale = _required(state.first, "first")
    operations: tuple[tuple[Callable[[], object], type[LudoWeaveError], str, str], ...] = (
        (
            lambda: world.add(replacement, _Enabled(True)),
            ComponentAlreadyPresentError,
            "ecs.component_already_present",
            "world_store_conformance.duplicate_add_mismatch",
        ),
        (
            lambda: world.remove(replacement, _Excluded),
            MissingComponentError,
            "ecs.missing_component",
            "world_store_conformance.missing_remove_mismatch",
        ),
        (
            lambda: world.patch(replacement, _Counter),
            InvalidComponentValueError,
            "ecs.invalid_component_value",
            "world_store_conformance.empty_patch_mismatch",
        ),
        (
            lambda: world.spawn(_Counter(1), _Counter(2)),
            ComponentAlreadyPresentError,
            "ecs.component_already_present",
            "world_store_conformance.duplicate_spawn_mismatch",
        ),
        (
            lambda: world.get(stale, _Counter),
            StaleEntityError,
            "ecs.stale_entity",
            "world_store_conformance.stale_failure_mismatch",
        ),
        (
            lambda: world.query(_Counter, _Counter),
            InvalidQueryError,
            "ecs.invalid_query",
            "world_store_conformance.invalid_query_mismatch",
        ),
    )
    before = _world_image(state)
    for operation, error_type, code, runner_code in operations:
        _expect_error(operation, error_type, code, runner_code)
        if _world_image(state) != before:
            raise _CheckFailure("world_store_conformance.failure_mutated")

    malformed = _Counter(1)
    object.__setattr__(malformed, "value", "invalid")
    _expect_error(
        lambda: world.spawn(malformed),
        InvalidComponentValueError,
        "ecs.invalid_component_value",
        "world_store_conformance.invalid_value_mismatch",
    )
    if _world_image(state) != before or world.spawn() != EntityId(4, 0):
        raise _CheckFailure("world_store_conformance.failure_allocation_mismatch")


def _world_image(state: _RunState) -> _WorldImage:
    return _world_image_for(state.world, state.registry)


def _world_image_for(world: WorldStore, registry: ComponentRegistry) -> _WorldImage:
    tables: list[tuple[type[object], int, tuple[tuple[EntityId, object, int], ...]]] = []
    for component_type in registry.component_types:
        rows = tuple(
            (entity_id, value, world.component_epoch(entity_id, component_type))
            for entity_id, value in world.components(component_type)
        )
        tables.append(
            (
                component_type,
                world.component_structural_epoch(component_type),
                rows,
            )
        )
    return (world.epoch, world.structural_epoch, world.entities(), tuple(tables))


def _expect_error(
    operation: Callable[[], object],
    error_type: type[LudoWeaveError],
    code: str,
    runner_code: str,
) -> None:
    try:
        operation()
    except LudoWeaveError as error:
        if not isinstance(error, error_type) or error.code != code:
            raise _CheckFailure(runner_code) from error
    else:
        raise _CheckFailure(runner_code)


def _required[ValueT](value: ValueT | None, field: str) -> ValueT:
    if value is None:
        raise _CheckFailure(f"world_store_conformance.missing_{field}")
    return value


def _passed(check_id: str) -> WorldStoreConformanceCheck:
    return WorldStoreConformanceCheck(check_id, WorldStoreConformanceStatus.PASS)


def _not_run(check_id: str) -> WorldStoreConformanceCheck:
    return WorldStoreConformanceCheck(
        check_id,
        WorldStoreConformanceStatus.NOT_RUN,
        "world_store_conformance.prerequisite_failed",
    )


def _failed(check_id: str, error: Exception) -> WorldStoreConformanceCheck:
    if type(error) is _CheckFailure:
        code = error.code
    elif isinstance(error, LudoWeaveError):
        code = "world_store_conformance.structured_adapter_error"
    else:
        code = "world_store_conformance.unstructured_exception"
    return WorldStoreConformanceCheck(check_id, WorldStoreConformanceStatus.FAIL, code)


def _validate_adapter_id(value: object) -> str:
    if type(value) is not str or len(value) > 128 or _ADAPTER_ID.fullmatch(value) is None:
        raise _request_error("adapter_id")
    return value


def _request_error(field: str) -> WorldError:
    return WorldError(
        "world-store conformance request is invalid",
        code="ecs.conformance_invalid_request",
        subsystem="ecs",
        phase="conformance",
        details={"field": field},
    )
