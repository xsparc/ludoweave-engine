"""Installed WorldStore conformance value, behavior, and failure tests."""

from collections.abc import Callable
from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from ludoweave.core import LudoWeaveError
from ludoweave.ecs import (
    WORLD_STORE_CONFORMANCE_PROFILE,
    WORLD_STORE_CONFORMANCE_PROTOCOL,
    ComponentRegistry,
    EntityId,
    FlushResult,
    ReferenceWorld,
    World,
    WorldError,
    WorldStore,
    WorldStoreConformanceCheck,
    WorldStoreConformanceReport,
    WorldStoreConformanceStatus,
    run_world_store_conformance,
)

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


def _check(report: WorldStoreConformanceReport, check_id: str) -> WorldStoreConformanceCheck:
    return report.checks[_CHECK_IDS.index(check_id)]


@pytest.mark.parametrize(
    ("adapter_id", "factory"),
    (("ludoweave.world", World), ("ludoweave.reference", ReferenceWorld)),
)
def test_builtin_world_stores_pass_exact_deterministic_profile(
    adapter_id: str,
    factory: Callable[[ComponentRegistry], WorldStore],
) -> None:
    first = run_world_store_conformance(adapter_id, factory)
    second = run_world_store_conformance(adapter_id, factory)

    assert first == second
    assert first.passed
    assert first.status is WorldStoreConformanceStatus.PASS
    assert tuple(check.check_id for check in first.checks) == _CHECK_IDS
    assert all(check.status is WorldStoreConformanceStatus.PASS for check in first.checks)
    document = first.as_dict()
    assert document["protocol"] == WORLD_STORE_CONFORMANCE_PROTOCOL
    assert document["profile"] == WORLD_STORE_CONFORMANCE_PROFILE
    assert document["adapter_id"] == adapter_id
    assert first.to_json().endswith("\n")
    assert "\\" not in first.to_json()


def test_factory_receives_exact_registry_once() -> None:
    registries: list[ComponentRegistry] = []

    def factory(registry: ComponentRegistry) -> WorldStore:
        registries.append(registry)
        return World(registry)

    report = run_world_store_conformance("org.example.explicit", factory)

    assert report.passed
    assert len(registries) == 1
    assert len(registries[0].component_types) == 3


@pytest.mark.parametrize(
    "adapter_id",
    ["", "world", "Org.World", ".world", "org..world", "org/world", "a." + "b" * 129],
)
def test_invalid_adapter_identity_is_rejected_before_factory_call(adapter_id: str) -> None:
    called = False

    def factory(registry: ComponentRegistry) -> WorldStore:
        nonlocal called
        called = True
        return World(registry)

    with pytest.raises(WorldError) as raised:
        run_world_store_conformance(adapter_id, factory)

    assert raised.value.code == "ecs.conformance_invalid_request"
    assert not called


def test_non_callable_factory_is_rejected() -> None:
    with pytest.raises(WorldError) as raised:
        run_world_store_conformance(
            "org.example.invalid",
            cast("object", object()),  # type: ignore[arg-type]
        )
    assert raised.value.code == "ecs.conformance_invalid_request"


def test_invalid_adapter_shape_and_registry_identity_are_reported() -> None:
    invalid = run_world_store_conformance(
        "org.example.invalid-shape",
        lambda _registry: cast("WorldStore", object()),
    )
    wrong_registry = run_world_store_conformance(
        "org.example.wrong-registry", lambda _registry: World(ComponentRegistry())
    )

    assert _check(invalid, "factory_registry").code == ("world_store_conformance.invalid_adapter")
    assert _check(wrong_registry, "factory_registry").code == (
        "world_store_conformance.registry_identity"
    )
    assert all(check.status is WorldStoreConformanceStatus.NOT_RUN for check in invalid.checks[1:])


def test_factory_failures_are_sanitized_and_control_flow_propagates() -> None:
    def unstructured(_registry: ComponentRegistry) -> WorldStore:
        raise RuntimeError(r"private token at C:\Users\someone\secret")

    def structured(_registry: ComponentRegistry) -> WorldStore:
        raise WorldError(
            "provider private detail",
            code="ecs.provider_secret",
            subsystem="ecs",
            phase="create",
        )

    first = run_world_store_conformance("org.example.unstructured", unstructured)
    second = run_world_store_conformance("org.example.structured", structured)

    assert _check(first, "factory_registry").code == (
        "world_store_conformance.unstructured_exception"
    )
    assert _check(second, "factory_registry").code == (
        "world_store_conformance.structured_adapter_error"
    )
    assert "private" not in first.to_json() + second.to_json()
    assert "Users" not in first.to_json()

    def interrupted(_registry: ComponentRegistry) -> WorldStore:
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_world_store_conformance("org.example.interrupted", interrupted)


class _InterruptedWorld(World):
    def entities(self) -> tuple[EntityId, ...]:
        raise KeyboardInterrupt


def test_control_flow_from_an_adapter_stage_propagates() -> None:
    def factory(registry: ComponentRegistry) -> WorldStore:
        return cast("WorldStore", _InterruptedWorld(registry))

    with pytest.raises(KeyboardInterrupt):
        run_world_store_conformance("org.example.interrupted-stage", factory)


class _EpochMismatchWorld(World):
    def component_epoch(self, entity_id: EntityId, component_type: type[object]) -> int:
        return super().component_epoch(entity_id, component_type) + 1


class _QueryMismatchWorld(World):
    def patch(self, entity_id: EntityId, component_type: type[object], **changes: object) -> object:  # type: ignore[override]
        if changes.get("value") == 21:
            changes["value"] = 20
        return super().patch(entity_id, component_type, **changes)


class _CommandResultMismatchWorld(World):
    def flush(self, commands: object) -> FlushResult:  # type: ignore[override]
        result = super().flush(commands)  # type: ignore[arg-type]
        return FlushResult(
            result.command_count + 1,
            result.start_epoch,
            result.end_epoch,
            result.resolutions,
        )


class _CloneAliasWorld(World):
    __slots__ = ("_clone_calls",)

    def __init__(self, registry: ComponentRegistry) -> None:
        super().__init__(registry)
        self._clone_calls = 0

    def clone(self) -> World:
        self._clone_calls += 1
        if self._clone_calls == 4:
            return self
        return super().clone()


class _FailureAcceptanceWorld(World):
    def spawn(self, *components: object) -> EntityId:
        if len(components) == 2 and type(components[0]) is type(components[1]):
            return super().spawn(components[0])
        return super().spawn(*components)


@pytest.mark.parametrize(
    ("world_type", "check_id", "code"),
    (
        (
            _EpochMismatchWorld,
            "direct_mutation_epochs",
            "world_store_conformance.direct_mutation_mismatch",
        ),
        (
            _QueryMismatchWorld,
            "query_semantics",
            "world_store_conformance.query_result_mismatch",
        ),
        (
            _CommandResultMismatchWorld,
            "command_buffer_atomicity",
            "world_store_conformance.command_result_mismatch",
        ),
        (
            _CloneAliasWorld,
            "clone_independence",
            "world_store_conformance.clone_state_mismatch",
        ),
        (
            _FailureAcceptanceWorld,
            "structured_failures",
            "world_store_conformance.duplicate_spawn_mismatch",
        ),
    ),
)
def test_behavioral_mismatches_fail_at_the_exact_stage(
    world_type: type[World], check_id: str, code: str
) -> None:
    report = run_world_store_conformance("org.example.mismatch", world_type)

    assert not report.passed
    assert _check(report, check_id).code == code
    position = _CHECK_IDS.index(check_id)
    assert all(
        check.status is WorldStoreConformanceStatus.NOT_RUN
        for check in report.checks[position + 1 :]
    )


class _UnstructuredEpochFailureWorld(World):
    def component_epoch(self, entity_id: EntityId, component_type: type[object]) -> int:
        del entity_id, component_type
        raise RuntimeError(r"credential=C:\provider\secret")


class _StructuredEpochFailureWorld(World):
    def component_epoch(self, entity_id: EntityId, component_type: type[object]) -> int:
        del entity_id, component_type
        raise LudoWeaveError(
            "do not expose",
            code="provider.secret-code",
            subsystem="provider",
        )


@pytest.mark.parametrize(
    ("world_type", "code"),
    (
        (_UnstructuredEpochFailureWorld, "world_store_conformance.unstructured_exception"),
        (_StructuredEpochFailureWorld, "world_store_conformance.structured_adapter_error"),
    ),
)
def test_adapter_errors_are_reduced_to_runner_owned_codes(
    world_type: type[World], code: str
) -> None:
    report = run_world_store_conformance("org.example.adapter-error", world_type)

    assert _check(report, "direct_mutation_epochs").code == code
    assert "credential" not in report.to_json()
    assert "secret-code" not in report.to_json()


def test_report_and_check_records_are_frozen_slotted_and_validate_invariants() -> None:
    report = run_world_store_conformance("ludoweave.world", World)
    with pytest.raises(FrozenInstanceError):
        report.adapter_id = "org.example.changed"  # type: ignore[misc]
    assert not hasattr(report, "__dict__")
    assert not hasattr(report.checks[0], "__dict__")

    with pytest.raises(WorldError):
        WorldStoreConformanceCheck("unknown", WorldStoreConformanceStatus.PASS)
    with pytest.raises(WorldError):
        WorldStoreConformanceCheck(
            "factory_registry", WorldStoreConformanceStatus.PASS, "unexpected"
        )
    with pytest.raises(WorldError):
        WorldStoreConformanceReport(
            "org.example.invalid",
            WorldStoreConformanceStatus.PASS,
            report.checks[:-1],
        )
