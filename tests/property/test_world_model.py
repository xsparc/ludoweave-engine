"""Hypothesis state-machine comparison of dense and dictionary worlds."""

from collections.abc import Callable
from dataclasses import dataclass
from math import inf, nan
from uuid import UUID

from hypothesis import settings
from hypothesis.stateful import RuleBasedStateMachine, invariant, precondition, rule
from hypothesis.strategies import booleans, integers, sampled_from, text

from ludoweave.core import LudoWeaveError
from ludoweave.ecs import (
    ComponentRegistry,
    EntityId,
    ReferenceWorld,
    StaleEntityError,
    World,
    component,
)


@component(type_id=UUID("ffffffff-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class ModelCounter:
    value: int = 0
    label: str | None = None


@component(type_id=UUID("ffffffff-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class ModelMotion:
    speed: float = 0.0
    enabled: bool = True


REGISTRY = ComponentRegistry((ModelMotion, ModelCounter))


class WorldModelMachine(RuleBasedStateMachine):
    """Generate valid and failing operations and compare after every step."""

    production: World
    reference: ReferenceWorld
    live: list[EntityId]
    stale: list[EntityId]

    def __init__(self) -> None:
        super().__init__()
        self.production = World(REGISTRY)
        self.reference = ReferenceWorld(REGISTRY)
        self.live = []
        self.stale = []

    @rule(
        value=integers(min_value=-100, max_value=100),
        label=text(max_size=8),
        with_counter=booleans(),
        with_motion=booleans(),
    )
    def spawn(self, value: int, label: str, with_counter: bool, with_motion: bool) -> None:
        components: list[object] = []
        if with_counter:
            components.append(ModelCounter(value, label or None))
        if with_motion:
            components.append(ModelMotion(float(value), bool(value % 2)))
        result = self._same_call(self.production.spawn, self.reference.spawn, *components)
        assert isinstance(result, EntityId)
        self.live.append(result)

    @precondition(lambda self: bool(self.live))
    @rule(selector=integers(min_value=0))
    def destroy(self, selector: int) -> None:
        entity_id = self.live.pop(selector % len(self.live))
        self._same_call(self.production.destroy, self.reference.destroy, entity_id)
        self.stale.append(entity_id)

    @precondition(lambda self: bool(self.live))
    @rule(selector=integers(min_value=0), value=integers(min_value=-100, max_value=100))
    def add_counter(self, selector: int, value: int) -> None:
        entity_id = self.live[selector % len(self.live)]
        self._same_call(
            self.production.add,
            self.reference.add,
            entity_id,
            ModelCounter(value),
        )

    @precondition(lambda self: bool(self.live))
    @rule(selector=integers(min_value=0))
    def remove_counter(self, selector: int) -> None:
        entity_id = self.live[selector % len(self.live)]
        self._same_call(
            self.production.remove,
            self.reference.remove,
            entity_id,
            ModelCounter,
        )

    @precondition(lambda self: bool(self.live))
    @rule(
        selector=integers(min_value=0),
        value=integers(min_value=-100, max_value=100),
        label=text(max_size=8),
    )
    def patch_counter(self, selector: int, value: int, label: str) -> None:
        entity_id = self.live[selector % len(self.live)]
        self._same_call(
            self.production.patch,
            self.reference.patch,
            entity_id,
            ModelCounter,
            value=value,
            label=label or None,
        )

    @precondition(lambda self: bool(self.live))
    @rule(selector=integers(min_value=0), value=integers(min_value=-100, max_value=100))
    def replace_counter(self, selector: int, value: int) -> None:
        entity_id = self.live[selector % len(self.live)]
        self._same_call(
            self.production.replace,
            self.reference.replace,
            entity_id,
            ModelCounter(value),
        )

    @precondition(lambda self: bool(self.live))
    @rule(selector=integers(min_value=0), invalid=sampled_from((nan, inf, -inf)))
    def invalid_motion_patch(self, selector: int, invalid: float) -> None:
        entity_id = self.live[selector % len(self.live)]
        self._same_call(
            self.production.patch,
            self.reference.patch,
            entity_id,
            ModelMotion,
            speed=invalid,
            unknown="not-stored",
        )

    @precondition(lambda self: bool(self.live))
    @rule(selector=integers(min_value=0))
    def empty_patch(self, selector: int) -> None:
        entity_id = self.live[selector % len(self.live)]
        self._same_call(
            self.production.patch,
            self.reference.patch,
            entity_id,
            ModelCounter,
        )

    @precondition(lambda self: bool(self.live))
    @rule(selector=integers(min_value=0), choose_motion=booleans())
    def inspect(self, selector: int, choose_motion: bool) -> None:
        entity_id = self.live[selector % len(self.live)]
        component_type = ModelMotion if choose_motion else ModelCounter
        self._same_call(
            self.production.has,
            self.reference.has,
            entity_id,
            component_type,
        )
        self._same_call(
            self.production.get,
            self.reference.get,
            entity_id,
            component_type,
        )

    @rule(exclude_motion=booleans())
    def stable_query(self, exclude_motion: bool) -> None:
        production_query = self.production.query(ModelCounter)
        reference_query = self.reference.query(ModelCounter)
        if exclude_motion:
            production_query = production_query.without(ModelMotion)
            reference_query = reference_query.without(ModelMotion)
        assert list(production_query.stable().rows()) == list(reference_query.stable().rows())

    @rule(delta=integers(min_value=-5, max_value=5))
    def writable_query(self, delta: int) -> None:
        with (
            self.production.query(ModelCounter).writes(ModelCounter).stable().rows() as left,
            self.reference.query(ModelCounter).writes(ModelCounter).stable().rows() as right,
        ):
            for left_row, right_row in zip(left, right, strict=True):
                assert left_row == right_row
                left_row[1].value += delta
                right_row[1].value += delta

    @rule(
        value=integers(min_value=-100, max_value=100),
        with_motion=booleans(),
    )
    def deferred_spawn(self, value: int, with_motion: bool) -> None:
        left = self.production.commands()
        right = self.reference.commands()
        left_token = left.spawn(ModelCounter(value))
        right_token = right.spawn(ModelCounter(value))
        if with_motion:
            left.add(left_token, ModelMotion(float(value)))
            right.add(right_token, ModelMotion(float(value)))
        left_result = self.production.flush(left)
        right_result = self.reference.flush(right)
        left_id = left_result.resolve(left_token)
        right_id = right_result.resolve(right_token)
        assert left_id == right_id
        assert left_result.command_count == right_result.command_count
        assert left_result.end_epoch == right_result.end_epoch
        self.live.append(left_id)

    @rule(value=integers(min_value=-100, max_value=100))
    def failing_deferred_spawn(self, value: int) -> None:
        left = self.production.commands()
        right = self.reference.commands()
        left_token = left.spawn(ModelCounter(value))
        right_token = right.spawn(ModelCounter(value))
        left.add(left_token, ModelCounter(value + 1))
        right.add(right_token, ModelCounter(value + 1))
        left_result = _capture(self.production.flush, (left,), {})
        right_result = _capture(self.reference.flush, (right,), {})
        assert left_result == right_result
        assert len(left) == len(right) == 2
        left.clear()
        right.clear()

    @invariant()
    def public_state_remains_equivalent(self) -> None:
        assert self.production.entities() == self.reference.entities()
        assert self.production.epoch == self.reference.epoch
        assert self.production.structural_epoch == self.reference.structural_epoch
        for component_type in REGISTRY.component_types:
            assert self.production.components(component_type) == self.reference.components(
                component_type
            )
            assert self.production.component_structural_epoch(
                component_type
            ) == self.reference.component_structural_epoch(component_type)
            for entity_id, _ in self.production.components(component_type):
                assert self.production.component_epoch(
                    entity_id, component_type
                ) == self.reference.component_epoch(entity_id, component_type)
        for stale in self.stale:
            for world in (self.production, self.reference):
                try:
                    world.has(stale, ModelCounter)
                except StaleEntityError:
                    pass
                else:
                    raise AssertionError("a retained stale handle became valid")
        self.production._check_invariants()  # pyright: ignore[reportPrivateUsage]

    def _same_call(
        self,
        production_call: Callable[..., object],
        reference_call: Callable[..., object],
        *arguments: object,
        **keywords: object,
    ) -> object:
        production_result = _capture(production_call, arguments, keywords)
        reference_result = _capture(reference_call, arguments, keywords)
        assert production_result == reference_result
        if production_result[0] == "return":
            return production_result[1]
        return production_result


def _capture(
    call: Callable[..., object],
    arguments: tuple[object, ...],
    keywords: dict[str, object],
) -> tuple[object, ...]:
    try:
        return ("return", call(*arguments, **keywords))
    except LudoWeaveError as error:
        return ("error", type(error), error.as_dict())


WorldModelTest = WorldModelMachine.TestCase  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
WorldModelTest.settings = settings(max_examples=40, stateful_step_count=60, deadline=None)
