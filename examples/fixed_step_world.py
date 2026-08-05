"""Run a deterministic ECS schedule from immutable virtual input."""

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from ludoweave import __version__
from ludoweave.app import (
    INPUT_SNAPSHOT_RESOURCE,
    ApplicationConfig,
    ApplicationRunSummary,
    FixedStepApplication,
    VirtualInputSource,
)
from ludoweave.core.clock import VirtualClock
from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    Scheduler,
    SystemContext,
    SystemPhase,
    World,
    component,
    system,
)
from ludoweave.render import NullRenderBackend, RenderDescriptor


@component(type_id=UUID("d7000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class InputEntity:
    active: bool = False


@dataclass(slots=True)
class Totals:
    entities: int = 0
    active: int = 0


TOTALS = ResourceSpec(
    "example.totals",
    Totals,
    lambda value: Totals(value.entities, value.active),
)


@system(
    name="example.spawn_from_input",
    phase=SystemPhase.PRE_SIMULATE,
    component_writes=(InputEntity,),
    resource_reads=(INPUT_SNAPSHOT_RESOURCE,),
)
def spawn_from_input(context: SystemContext, delta: float) -> None:
    del delta
    snapshot = context.resource(INPUT_SNAPSHOT_RESOURCE)
    context.commands.spawn(InputEntity(active=snapshot.value("activate") is True))


@system(
    name="example.count_after_flush",
    phase=SystemPhase.POST_SIMULATE,
    component_reads=(InputEntity,),
    resource_writes=(TOTALS,),
)
def count_after_flush(context: SystemContext, delta: float) -> None:
    del delta
    totals = context.resource(TOTALS)
    values = tuple(entity.active for _entity_id, entity in context.query(InputEntity).rows())
    totals.entities = len(values)
    totals.active = sum(values)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=6, help="non-negative tick count")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    ticks: object = getattr(args, "ticks", None)
    if type(ticks) is not int or ticks < 0:
        _parser().error("--ticks must be a non-negative integer")

    components = ComponentRegistry((InputEntity,))
    resource_registry = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE, TOTALS))
    resources = ResourceStore(resource_registry, ((TOTALS, Totals()),))
    schedule = Scheduler(components, resource_registry).build((count_after_flush, spawn_from_input))
    world = World(components)
    backend = NullRenderBackend()
    clock = VirtualClock()
    input_source = VirtualInputSource({tick: {"activate": tick % 2 == 0} for tick in range(ticks)})
    application = FixedStepApplication(
        ApplicationConfig(),
        backend,
        world,
        resources,
        schedule,
        input_source,
        clock=clock,
        descriptor=RenderDescriptor(label="fixed_step_world"),
    )
    summary: ApplicationRunSummary | None = None
    with application:
        summary = application.run_ticks(ticks)
    assert summary is not None
    totals = resources.require(TOTALS)

    payload: dict[str, object] = {
        "schema": "ludoweave.example.fixed_step_world/1",
        "ludoweave_version": __version__,
        "ticks": summary.ticks,
        "frames": summary.frames,
        "entities": totals.entities,
        "active": totals.active,
        "elapsed_ns": summary.elapsed_ns,
        "renderer": summary.renderer,
        "final_state": application.state.value,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
