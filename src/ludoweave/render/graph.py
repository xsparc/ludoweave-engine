"""Deterministic render-graph dependency, hazard, and lifetime validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import StrEnum

from ludoweave.core.errors import RenderError
from ludoweave.render.contracts import CommandList

_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,127}\Z")


class GraphResourceKind(StrEnum):
    BUFFER = "buffer"
    TEXTURE = "texture"
    SURFACE = "surface"


class GraphResourceLifetime(StrEnum):
    EXTERNAL = "external"
    TRANSIENT = "transient"


@dataclass(frozen=True, slots=True)
class GraphResource:
    name: str
    kind: GraphResourceKind
    lifetime: GraphResourceLifetime
    first_pass: str | None = None
    last_pass: str | None = None

    def __post_init__(self) -> None:
        _name(self.name, field="resource")
        if type(self.kind) is not GraphResourceKind:
            raise _graph_error("graph resource kind has the wrong exact type", field=self.name)
        if type(self.lifetime) is not GraphResourceLifetime:
            raise _graph_error("graph resource lifetime has the wrong exact type", field=self.name)
        if self.lifetime is GraphResourceLifetime.TRANSIENT:
            if self.first_pass is None or self.last_pass is None:
                raise _graph_error(
                    "transient graph resources require explicit first and last passes",
                    field=self.name,
                )
            _name(self.first_pass, field="first_pass")
            _name(self.last_pass, field="last_pass")
        elif self.first_pass is not None or self.last_pass is not None:
            raise _graph_error(
                "external graph resources cannot declare transient lifetimes", field=self.name
            )


@dataclass(frozen=True, slots=True)
class RenderPass:
    name: str
    reads: tuple[str, ...] = ()
    writes: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    commands: CommandList = dataclass_field(default_factory=lambda: CommandList("empty-pass", ()))

    def __post_init__(self) -> None:
        _name(self.name, field="pass")
        for field in ("reads", "writes", "depends_on"):
            try:
                values = tuple(getattr(self, field))
            except Exception as error:
                raise _graph_error(
                    "render pass collection could not be frozen", field=field
                ) from error
            if any(type(value) is not str or _NAME.fullmatch(value) is None for value in values):
                raise _graph_error("render pass references contain an invalid name", field=field)
            if len(values) != len(set(values)):
                raise _graph_error("render pass references must be unique", field=field)
            object.__setattr__(self, field, values)
        if set(self.reads) & set(self.writes):
            raise _graph_error(
                "one render pass cannot declare the same resource for read and write",
                field=self.name,
            )
        if self.name in self.depends_on:
            raise _graph_error("render pass cannot depend on itself", field=self.name)
        if type(self.commands) is not CommandList:
            raise _graph_error("render pass requires an exact CommandList", field="commands")


@dataclass(frozen=True, slots=True)
class CompiledRenderGraph:
    resources: tuple[GraphResource, ...]
    passes: tuple[RenderPass, ...]

    @property
    def command_lists(self) -> tuple[CommandList, ...]:
        return tuple(render_pass.commands for render_pass in self.passes)


@dataclass(frozen=True, slots=True)
class RenderGraph:
    resources: tuple[GraphResource, ...]
    passes: tuple[RenderPass, ...]

    def __post_init__(self) -> None:
        resources = tuple(self.resources)
        passes = tuple(self.passes)
        if any(type(resource) is not GraphResource for resource in resources):
            raise _graph_error("render graph contains an invalid resource", field="resources")
        if any(type(render_pass) is not RenderPass for render_pass in passes):
            raise _graph_error("render graph contains an invalid pass", field="passes")
        object.__setattr__(self, "resources", resources)
        object.__setattr__(self, "passes", passes)

    def compile(self) -> CompiledRenderGraph:
        resource_by_name = _unique(self.resources, role="resource")
        pass_by_name = _unique(self.passes, role="pass")
        if not pass_by_name:
            raise _graph_error("render graph requires at least one pass", field="passes")

        for render_pass in self.passes:
            for dependency in render_pass.depends_on:
                if dependency not in pass_by_name:
                    raise _graph_error(
                        "render pass depends on an unknown pass",
                        field=dependency,
                        pass_name=render_pass.name,
                    )
            for resource_name in (*render_pass.reads, *render_pass.writes):
                if resource_name not in resource_by_name:
                    raise _graph_error(
                        "render pass references an unknown resource",
                        field=resource_name,
                        pass_name=render_pass.name,
                    )

        ordered = _topological_order(pass_by_name)
        positions = {render_pass.name: index for index, render_pass in enumerate(ordered)}
        ancestors = {
            render_pass.name: _ancestors(render_pass.name, pass_by_name) for render_pass in ordered
        }

        for resource in self.resources:
            accesses = [
                render_pass
                for render_pass in ordered
                if resource.name in render_pass.reads or resource.name in render_pass.writes
            ]
            if resource.lifetime is GraphResourceLifetime.TRANSIENT:
                assert resource.first_pass is not None and resource.last_pass is not None
                if (
                    resource.first_pass not in pass_by_name
                    or resource.last_pass not in pass_by_name
                ):
                    raise _graph_error(
                        "transient resource lifetime references an unknown pass",
                        field=resource.name,
                    )
                first = positions[resource.first_pass]
                last = positions[resource.last_pass]
                if first > last:
                    raise _graph_error(
                        "transient resource lifetime moves backward", field=resource.name
                    )
                if resource.name not in pass_by_name[resource.first_pass].writes:
                    raise _graph_error(
                        "transient resource first pass must write the resource", field=resource.name
                    )
                for render_pass in accesses:
                    if not first <= positions[render_pass.name] <= last:
                        raise _graph_error(
                            "render pass accesses a transient resource outside its lifetime",
                            field=resource.name,
                            pass_name=render_pass.name,
                        )

            writers = [item for item in accesses if resource.name in item.writes]
            if resource.lifetime is GraphResourceLifetime.TRANSIENT and not writers:
                raise _graph_error("transient resource is never written", field=resource.name)
            for reader in (item for item in accesses if resource.name in item.reads):
                prior_writers = [
                    writer for writer in writers if writer.name in ancestors[reader.name]
                ]
                if resource.lifetime is GraphResourceLifetime.TRANSIENT and not prior_writers:
                    raise _graph_error(
                        "transient resource is read without a dependency on a writer",
                        field=resource.name,
                        pass_name=reader.name,
                    )

            for left_index, left in enumerate(accesses):
                left_writes = resource.name in left.writes
                for right in accesses[left_index + 1 :]:
                    right_writes = resource.name in right.writes
                    if not left_writes and not right_writes:
                        continue
                    if (
                        left.name not in ancestors[right.name]
                        and right.name not in ancestors[left.name]
                    ):
                        raise _graph_error(
                            "render resource hazard requires an explicit dependency path",
                            field=resource.name,
                        )

        return CompiledRenderGraph(
            tuple(sorted(self.resources, key=lambda item: item.name)), ordered
        )


def _unique[ValueT: (GraphResource, RenderPass)](
    values: tuple[ValueT, ...], *, role: str
) -> dict[str, ValueT]:
    result: dict[str, ValueT] = {}
    for value in values:
        if value.name in result:
            raise _graph_error(f"render graph {role} names must be unique", field=value.name)
        result[value.name] = value
    return result


def _topological_order(pass_by_name: dict[str, RenderPass]) -> tuple[RenderPass, ...]:
    remaining = {name: set(item.depends_on) for name, item in pass_by_name.items()}
    ordered: list[RenderPass] = []
    while remaining:
        ready = sorted(name for name, dependencies in remaining.items() if not dependencies)
        if not ready:
            cycle = ",".join(sorted(remaining))
            raise _graph_error("render graph dependency cycle detected", field=cycle)
        for name in ready:
            ordered.append(pass_by_name[name])
            del remaining[name]
        for dependencies in remaining.values():
            dependencies.difference_update(ready)
    return tuple(ordered)


def _ancestors(name: str, pass_by_name: dict[str, RenderPass]) -> frozenset[str]:
    result: set[str] = set()
    pending = list(pass_by_name[name].depends_on)
    while pending:
        dependency = pending.pop()
        if dependency in result:
            continue
        result.add(dependency)
        pending.extend(pass_by_name[dependency].depends_on)
    return frozenset(result)


def _name(value: object, *, field: str) -> str:
    if type(value) is not str or _NAME.fullmatch(value) is None:
        raise _graph_error("render graph names must use bounded stable text", field=field)
    return value


def _graph_error(message: str, *, field: str, pass_name: str | None = None) -> RenderError:
    details: dict[str, str] = {"field": field}
    if pass_name is not None:
        details["pass"] = pass_name
    return RenderError(
        message,
        code="render.invalid_graph",
        subsystem="render",
        phase="graph",
        details=details,
    )
