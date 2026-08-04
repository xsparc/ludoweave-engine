"""Deterministic null render-graph validation tests."""

from itertools import permutations

import pytest

from ludoweave.core.errors import RenderError
from ludoweave.render import (
    CommandList,
    GraphResource,
    GraphResourceKind,
    GraphResourceLifetime,
    NullRenderDevice,
    RenderGraph,
    RenderPass,
)


def _resource() -> GraphResource:
    return GraphResource(
        "color",
        GraphResourceKind.TEXTURE,
        GraphResourceLifetime.TRANSIENT,
        first_pass="produce",
        last_pass="present",
    )


def _passes() -> tuple[RenderPass, ...]:
    return (
        RenderPass("produce", writes=("color",), commands=CommandList("produce", ())),
        RenderPass(
            "consume",
            reads=("color",),
            depends_on=("produce",),
            commands=CommandList("consume", ()),
        ),
        RenderPass(
            "present",
            reads=("color",),
            depends_on=("consume",),
            commands=CommandList("present", ()),
        ),
    )


def test_valid_graph_compiles_independently_of_declaration_order() -> None:
    expected = ("produce", "consume", "present")
    for order in permutations(_passes()):
        compiled = RenderGraph((_resource(),), order).compile()
        assert tuple(render_pass.name for render_pass in compiled.passes) == expected
        assert compiled.resources == (_resource(),)


@pytest.mark.parametrize(
    "graph",
    [
        RenderGraph(
            (_resource(),),
            (
                RenderPass("produce", writes=("color",)),
                RenderPass("consume", reads=("color",)),
            ),
        ),
        RenderGraph(
            (_resource(),),
            (
                RenderPass("produce", writes=("color",), depends_on=("consume",)),
                RenderPass("consume", reads=("color",), depends_on=("produce",)),
                RenderPass("present", reads=("color",), depends_on=("consume",)),
            ),
        ),
        RenderGraph(
            (_resource(),),
            (RenderPass("produce", writes=("unknown",)),),
        ),
        RenderGraph(
            (
                GraphResource(
                    "color",
                    GraphResourceKind.TEXTURE,
                    GraphResourceLifetime.TRANSIENT,
                    first_pass="consume",
                    last_pass="consume",
                ),
            ),
            (RenderPass("consume", reads=("color",)),),
        ),
    ],
)
def test_invalid_dependencies_hazards_and_lifetimes_fail_without_submission(
    graph: RenderGraph,
) -> None:
    device = NullRenderDevice()
    with pytest.raises(RenderError) as raised:
        device.submit_graph(graph)
    assert raised.value.code == "render.invalid_graph"
    assert device.completed_submission == 0


def test_external_resources_may_be_read_without_a_graph_writer() -> None:
    external = GraphResource("swapchain", GraphResourceKind.SURFACE, GraphResourceLifetime.EXTERNAL)
    graph = RenderGraph(
        (external,),
        (RenderPass("present", reads=("swapchain",), commands=CommandList("present", ())),),
    )
    assert tuple(item.name for item in graph.compile().passes) == ("present",)


def test_unordered_multiple_writers_fail_and_ordered_writers_pass() -> None:
    resource = GraphResource(
        "target",
        GraphResourceKind.TEXTURE,
        GraphResourceLifetime.TRANSIENT,
        first_pass="first",
        last_pass="second",
    )
    unordered = RenderGraph(
        (resource,),
        (RenderPass("first", writes=("target",)), RenderPass("second", writes=("target",))),
    )
    with pytest.raises(RenderError):
        unordered.compile()

    ordered = RenderGraph(
        (resource,),
        (
            RenderPass("second", writes=("target",), depends_on=("first",)),
            RenderPass("first", writes=("target",)),
        ),
    )
    assert tuple(item.name for item in ordered.compile().passes) == ("first", "second")
