"""Typed resource identity, copy ownership, and singleton storage tests."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_type

import pytest

from ludoweave.ecs import (
    DuplicateResourceError,
    InvalidResourceSpecError,
    MissingResourceError,
    ResourceCopyError,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    UnknownResourceError,
)


@dataclass(slots=True)
class Settings:
    rate: int = 60


@dataclass(slots=True)
class SettingsSubclass(Settings):
    pass


@dataclass(slots=True)
class Bag:
    values: list[int]


@dataclass(slots=True)
class HostileResource:
    value: int = 0

    def __getattribute__(self, name: str) -> object:
        if name == "value":
            raise AssertionError("resource adapters must choose how fields are read")
        return object.__getattribute__(self, name)


SETTINGS = ResourceSpec("simulation.settings", Settings, lambda value: Settings(value.rate))
SECOND_SETTINGS = ResourceSpec(
    "presentation.settings",
    Settings,
    lambda value: Settings(value.rate),
    deterministic=False,
)
BAG = ResourceSpec("simulation.bag", Bag, lambda value: Bag(list(value.values)))
HOSTILE = ResourceSpec(
    "simulation.hostile",
    HostileResource,
    lambda value: HostileResource(object.__getattribute__(value, "value")),
)
REGISTRY = ResourceRegistry((SETTINGS, SECOND_SETTINGS, BAG, HOSTILE))


if TYPE_CHECKING:

    def _assert_resource_types(store: ResourceStore) -> None:
        assert_type(store.require(SETTINGS), Settings)
        assert_type(store.replace(SETTINGS, Settings()), Settings)
        assert_type(store.remove(SETTINGS), Settings)

    _ = _assert_resource_types


def test_resource_specs_and_registry_are_explicit_stable_and_isolated() -> None:
    assert SETTINGS.name == "simulation.settings"
    assert SETTINGS.value_type is Settings
    assert SETTINGS.deterministic
    assert not SECOND_SETTINGS.deterministic
    assert [spec.name for spec in REGISTRY.specs] == [
        "presentation.settings",
        "simulation.bag",
        "simulation.hostile",
        "simulation.settings",
    ]
    assert REGISTRY.contains(SETTINGS)
    assert REGISTRY.spec_for_name("simulation.settings") is SETTINGS

    separate = ResourceRegistry((SETTINGS,))
    assert separate.contains(SETTINGS)
    assert not ResourceRegistry().contains(SETTINGS)


def test_immutable_scalar_resource_does_not_require_impossible_identity_change() -> None:
    tick = ResourceSpec("time.tick", int, int)
    store = ResourceStore(ResourceRegistry((tick,)), ((tick, 4),))

    assert store.require(tick) == 4
    assert store.replace(tick, 5) == 4
    assert store.remove(tick) == 5


@pytest.mark.parametrize("name", ["", " ", "bad name", "9invalid", "line\nbreak"])
def test_resource_spec_rejects_unstable_names(name: str) -> None:
    with pytest.raises(InvalidResourceSpecError):
        ResourceSpec(name, Settings, lambda value: Settings(value.rate))


def test_resource_spec_rejects_invalid_type_copier_determinism_and_local_type() -> None:
    with pytest.raises(InvalidResourceSpecError):
        ResourceSpec("bad.type", "Settings", lambda value: value)  # type: ignore[arg-type]
    with pytest.raises(InvalidResourceSpecError):
        ResourceSpec("bad.copier", Settings, object())  # type: ignore[arg-type]
    with pytest.raises(InvalidResourceSpecError):
        ResourceSpec(
            "bad.determinism",
            Settings,
            lambda value: Settings(value.rate),
            deterministic=1,  # type: ignore[arg-type]
        )

    @dataclass(slots=True)
    class LocalResource:
        value: int

    with pytest.raises(InvalidResourceSpecError):
        ResourceSpec("bad.local", LocalResource, lambda value: LocalResource(value.value))


def test_registry_rejects_duplicates_and_non_specs_atomically() -> None:
    duplicate = ResourceSpec(
        SETTINGS.name,
        Settings,
        lambda value: Settings(value.rate),
    )
    with pytest.raises(DuplicateResourceError):
        ResourceRegistry((SETTINGS, duplicate))
    with pytest.raises(InvalidResourceSpecError):
        ResourceRegistry((SETTINGS, object()))
    with pytest.raises(InvalidResourceSpecError):
        ResourceRegistry(1)  # type: ignore[arg-type]
    with pytest.raises(InvalidResourceSpecError):
        ResourceRegistry("simulation.settings")


def test_store_copy_in_copy_out_replace_remove_and_singleton_failures() -> None:
    store = ResourceStore(REGISTRY)
    source = Settings(30)
    store.insert(SETTINGS, source)
    source.rate = 99

    first = store.require(SETTINGS)
    second = store.require(SETTINGS)
    assert first == second == Settings(30)
    assert first is not second
    first.rate = 1
    assert store.require(SETTINGS) == Settings(30)
    assert store.contains(SETTINGS)

    with pytest.raises(DuplicateResourceError):
        store.insert(SETTINGS, Settings(40))
    previous = store.replace(SETTINGS, Settings(40))
    assert previous == Settings(30)
    previous.rate = 2
    assert store.require(SETTINGS) == Settings(40)
    removed = store.remove(SETTINGS)
    assert removed == Settings(40)
    assert not store.contains(SETTINGS)
    with pytest.raises(MissingResourceError):
        store.require(SETTINGS)
    with pytest.raises(MissingResourceError):
        store.replace(SETTINGS, Settings())
    with pytest.raises(MissingResourceError):
        store.remove(SETTINGS)


def test_store_rejects_wrong_exact_types_and_foreign_or_cloned_keys() -> None:
    store = ResourceStore(REGISTRY)
    with pytest.raises(ResourceCopyError):
        store.insert(SETTINGS, SettingsSubclass())
    with pytest.raises(UnknownResourceError):
        store.insert(
            ResourceSpec(
                SETTINGS.name,
                Settings,
                lambda value: Settings(value.rate),
            ),
            Settings(),
        )
    with pytest.raises(UnknownResourceError):
        store.contains(object())  # type: ignore[arg-type]
    assert len(store) == 0


def test_mutable_nested_values_stores_and_clones_remain_independent() -> None:
    first = ResourceStore(REGISTRY)
    first.insert(BAG, Bag([1, 2]))
    returned = first.require(BAG)
    returned.values.append(3)
    duplicate = first.clone()
    duplicate_value = duplicate.require(BAG)
    duplicate_value.values.append(4)
    duplicate.replace(BAG, duplicate_value)

    assert first.require(BAG) == Bag([1, 2])
    assert duplicate.require(BAG) == Bag([1, 2, 4])
    second = ResourceStore(REGISTRY)
    assert not second.contains(BAG)


def test_explicit_adapter_bypasses_hostile_author_getters() -> None:
    store = ResourceStore(REGISTRY)
    source = HostileResource(7)
    store.insert(HOSTILE, source)
    returned = store.require(HOSTILE)

    assert object.__getattribute__(source, "value") == 7
    assert object.__getattribute__(returned, "value") == 7


def test_copy_failures_are_structured_and_compliant_adapters_preserve_state() -> None:
    def raises(value: Settings) -> Settings:
        del value
        raise RuntimeError("copy failed")

    raising = ResourceSpec("broken.raise", Settings, raises)
    wrong = ResourceSpec(
        "broken.wrong",
        Settings,
        lambda value: SettingsSubclass(value.rate),  # type: ignore[arg-type, return-value]
    )
    same = ResourceSpec("broken.same", Settings, lambda value: value)
    registry = ResourceRegistry((raising, wrong, same))
    store = ResourceStore(registry)

    with pytest.raises(ResourceCopyError) as raised:
        store.insert(raising, Settings())
    assert isinstance(raised.value.__cause__, RuntimeError)
    assert dict(raised.value.details)["resource"] == "broken.raise"
    for spec in (wrong, same):
        with pytest.raises(ResourceCopyError):
            store.insert(spec, Settings())
    assert len(store) == 0

    should_fail = False

    def controlled_copy(value: Settings) -> Settings:
        if should_fail:
            raise RuntimeError("copy failed without mutating input")
        return Settings(value.rate)

    controlled = ResourceSpec("broken.controlled", Settings, controlled_copy)
    controlled_store = ResourceStore(ResourceRegistry((controlled,)))
    controlled_store.insert(controlled, Settings(72))
    should_fail = True
    with pytest.raises(ResourceCopyError):
        controlled_store.require(controlled)
    should_fail = False
    assert controlled_store.require(controlled) == Settings(72)


def test_constructor_initial_values_are_typed_and_copy_owned() -> None:
    settings = Settings(20)
    store = ResourceStore(REGISTRY, ((SETTINGS, settings), (BAG, Bag([1]))))
    settings.rate = 90

    assert store.require(SETTINGS) == Settings(20)
    assert store.require(BAG) == Bag([1])

    with pytest.raises(InvalidResourceSpecError):
        ResourceStore(REGISTRY, (SETTINGS,))  # type: ignore[arg-type]


def test_replace_many_is_batch_atomic_for_compliant_adapters() -> None:
    store = ResourceStore(
        REGISTRY,
        ((SETTINGS, Settings(60)), (BAG, Bag([1]))),
    )

    store.replace_many(((SETTINGS, Settings(120)), (BAG, Bag([2]))))
    assert store.require(SETTINGS) == Settings(120)
    assert store.require(BAG) == Bag([2])

    with pytest.raises(ResourceCopyError):
        store.replace_many(((SETTINGS, Settings(30)), (BAG, Settings(1))))
    assert store.require(SETTINGS) == Settings(120)
    assert store.require(BAG) == Bag([2])

    with pytest.raises(DuplicateResourceError):
        store.replace_many(((SETTINGS, Settings(30)), (SETTINGS, Settings(40))))
    assert store.require(SETTINGS) == Settings(120)
