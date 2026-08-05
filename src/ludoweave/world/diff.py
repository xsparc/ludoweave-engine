"""Exact semantic comparison of canonical authoritative logical images."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from ludoweave.world.canonical import JsonValue, canonical_dumps


@dataclass(frozen=True, slots=True)
class AllocatorSlotChange:
    index: int
    before_generation: int | None
    after_generation: int | None
    before_alive: bool | None
    after_alive: bool | None

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "index": self.index,
            "before_generation": self.before_generation,
            "after_generation": self.after_generation,
            "before_alive": self.before_alive,
            "after_alive": self.after_alive,
        }


@dataclass(frozen=True, slots=True)
class AllocatorChange:
    free_before: tuple[int, ...]
    free_after: tuple[int, ...]
    slots: tuple[AllocatorSlotChange, ...]

    @property
    def changed(self) -> bool:
        return bool(self.slots) or self.free_before != self.free_after

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "free_before": list(self.free_before),
            "free_after": list(self.free_after),
            "slots": [slot.as_dict() for slot in self.slots],
        }


@dataclass(frozen=True, slots=True)
class ComponentChange:
    entity: str
    type_id: str
    fields: tuple[str, ...]
    before_epoch: int | None
    after_epoch: int | None

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "entity": self.entity,
            "type_id": self.type_id,
            "fields": list(self.fields),
            "before_epoch": self.before_epoch,
            "after_epoch": self.after_epoch,
        }


@dataclass(frozen=True, slots=True)
class ResourceChange:
    type_id: str
    before_present: bool
    after_present: bool
    value_changed: bool

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "type_id": self.type_id,
            "before_present": self.before_present,
            "after_present": self.after_present,
            "value_changed": self.value_changed,
        }


@dataclass(frozen=True, slots=True)
class TableEpochChange:
    type_id: str
    before: int
    after: int

    def as_dict(self) -> dict[str, JsonValue]:
        return {"type_id": self.type_id, "before": self.before, "after": self.after}


@dataclass(frozen=True, slots=True)
class EpochChange:
    world_before: int
    world_after: int
    structural_before: int
    structural_after: int
    tables: tuple[TableEpochChange, ...]

    @property
    def changed(self) -> bool:
        return (
            self.world_before != self.world_after
            or self.structural_before != self.structural_after
            or bool(self.tables)
        )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "world_before": self.world_before,
            "world_after": self.world_after,
            "structural_before": self.structural_before,
            "structural_after": self.structural_after,
            "tables": [table.as_dict() for table in self.tables],
        }


@dataclass(frozen=True, slots=True)
class SemanticDiff:
    """Canonically ordered net changes plus future-behavior metadata changes."""

    created_entities: tuple[str, ...]
    destroyed_entities: tuple[str, ...]
    changed_entities: tuple[str, ...]
    components_added: tuple[ComponentChange, ...]
    components_removed: tuple[ComponentChange, ...]
    components_changed: tuple[ComponentChange, ...]
    resources_changed: tuple[ResourceChange, ...]
    allocator: AllocatorChange
    epochs: EpochChange
    completed_ticks_before: int
    completed_ticks_after: int

    @property
    def changed(self) -> bool:
        return (
            any(
                (
                    self.created_entities,
                    self.destroyed_entities,
                    self.components_added,
                    self.components_removed,
                    self.components_changed,
                    self.resources_changed,
                )
            )
            or self.allocator.changed
            or self.epochs.changed
            or (self.completed_ticks_before != self.completed_ticks_after)
        )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "created_entities": list(self.created_entities),
            "destroyed_entities": list(self.destroyed_entities),
            "changed_entities": list(self.changed_entities),
            "components_added": [item.as_dict() for item in self.components_added],
            "components_removed": [item.as_dict() for item in self.components_removed],
            "components_changed": [item.as_dict() for item in self.components_changed],
            "resources_changed": [item.as_dict() for item in self.resources_changed],
            "allocator": self.allocator.as_dict(),
            "epochs": self.epochs.as_dict(),
            "completed_ticks_before": self.completed_ticks_before,
            "completed_ticks_after": self.completed_ticks_after,
        }


def semantic_diff(
    before: dict[str, JsonValue],
    after: dict[str, JsonValue],
) -> SemanticDiff:
    """Compare two engine-produced authority documents without handler input."""

    before_allocator = _object(before["allocator"])
    after_allocator = _object(after["allocator"])
    before_generations = _int_list(before_allocator["generations"])
    after_generations = _int_list(after_allocator["generations"])
    before_alive_flags = _bool_list(before_allocator["alive"])
    after_alive_flags = _bool_list(after_allocator["alive"])
    slot_changes = tuple(
        AllocatorSlotChange(
            index=index,
            before_generation=_at(before_generations, index),
            after_generation=_at(after_generations, index),
            before_alive=_at(before_alive_flags, index),
            after_alive=_at(after_alive_flags, index),
        )
        for index in range(max(len(before_generations), len(after_generations)))
        if _at(before_generations, index) != _at(after_generations, index)
        or _at(before_alive_flags, index) != _at(after_alive_flags, index)
    )
    allocator = AllocatorChange(
        free_before=tuple(_int_list(before_allocator["free"])),
        free_after=tuple(_int_list(after_allocator["free"])),
        slots=slot_changes,
    )

    before_entities = _live_entities(before_generations, before_alive_flags)
    after_entities = _live_entities(after_generations, after_alive_flags)
    created = tuple(sorted(after_entities - before_entities, key=_entity_sort_key))
    destroyed = tuple(sorted(before_entities - after_entities, key=_entity_sort_key))

    before_components, before_table_epochs = _components(before)
    after_components, after_table_epochs = _components(after)
    before_keys = set(before_components)
    after_keys = set(after_components)
    added = tuple(
        _component_change(key, None, after_components[key])
        for key in sorted(after_keys - before_keys, key=_component_key)
    )
    removed = tuple(
        _component_change(key, before_components[key], None)
        for key in sorted(before_keys - after_keys, key=_component_key)
    )
    changed = tuple(
        _component_change(key, before_components[key], after_components[key])
        for key in sorted(before_keys & after_keys, key=_component_key)
        if _component_record_changed(before_components[key], after_components[key])
    )
    changed_entity_set = (
        {item.entity for item in (*added, *removed, *changed)} - set(created) - set(destroyed)
    )

    before_resources = _resources(before)
    after_resources = _resources(after)
    resource_changes = tuple(
        ResourceChange(
            type_id=type_id,
            before_present=before_resources.get(type_id, (False, None))[0],
            after_present=after_resources.get(type_id, (False, None))[0],
            value_changed=_canonical_not_equal(
                before_resources.get(type_id, (False, None))[1],
                after_resources.get(type_id, (False, None))[1],
            ),
        )
        for type_id in sorted(set(before_resources) | set(after_resources))
        if before_resources.get(type_id) != after_resources.get(type_id)
        or _canonical_not_equal(
            before_resources.get(type_id, (False, None))[1],
            after_resources.get(type_id, (False, None))[1],
        )
    )

    before_epochs = _object(before["epochs"])
    after_epochs = _object(after["epochs"])
    table_changes = tuple(
        TableEpochChange(
            type_id=type_id,
            before=before_table_epochs.get(type_id, 0),
            after=after_table_epochs.get(type_id, 0),
        )
        for type_id in sorted(set(before_table_epochs) | set(after_table_epochs))
        if before_table_epochs.get(type_id, 0) != after_table_epochs.get(type_id, 0)
    )
    epochs = EpochChange(
        world_before=_int(before_epochs["world"]),
        world_after=_int(after_epochs["world"]),
        structural_before=_int(before_epochs["structural"]),
        structural_after=_int(after_epochs["structural"]),
        tables=table_changes,
    )
    return SemanticDiff(
        created_entities=created,
        destroyed_entities=destroyed,
        changed_entities=tuple(sorted(changed_entity_set, key=_entity_sort_key)),
        components_added=added,
        components_removed=removed,
        components_changed=changed,
        resources_changed=resource_changes,
        allocator=allocator,
        epochs=epochs,
        completed_ticks_before=_int(before["completed_ticks"]),
        completed_ticks_after=_int(after["completed_ticks"]),
    )


type _ComponentRecord = tuple[dict[str, JsonValue], int]


def _components(
    document: dict[str, JsonValue],
) -> tuple[dict[tuple[str, str], _ComponentRecord], dict[str, int]]:
    records: dict[tuple[str, str], _ComponentRecord] = {}
    table_epochs: dict[str, int] = {}
    for table_value in _array(document["components"]):
        table = _object(table_value)
        type_id = _str(table["type_id"])
        table_epochs[type_id] = _int(table["structural_epoch"])
        for row_value in _array(table["rows"]):
            row = _object(row_value)
            entity_pair = _int_list(row["entity"])
            entity = f"{entity_pair[0]}:{entity_pair[1]}"
            records[(entity, type_id)] = (
                _object(row["values"]),
                _int(row["changed_epoch"]),
            )
    return records, table_epochs


def _component_change(
    key: tuple[str, str],
    before: _ComponentRecord | None,
    after: _ComponentRecord | None,
) -> ComponentChange:
    before_values = {} if before is None else before[0]
    after_values = {} if after is None else after[0]
    fields = tuple(
        field
        for field in sorted(set(before_values) | set(after_values))
        if field not in before_values
        or field not in after_values
        or _canonical_not_equal(before_values[field], after_values[field])
    )
    return ComponentChange(
        entity=key[0],
        type_id=key[1],
        fields=fields,
        before_epoch=None if before is None else before[1],
        after_epoch=None if after is None else after[1],
    )


def _component_record_changed(before: _ComponentRecord, after: _ComponentRecord) -> bool:
    return before[1] != after[1] or _canonical_not_equal(before[0], after[0])


def _resources(document: dict[str, JsonValue]) -> dict[str, tuple[bool, JsonValue]]:
    result: dict[str, tuple[bool, JsonValue]] = {}
    for value in _array(document["resources"]):
        record = _object(value)
        result[_str(record["type_id"])] = (
            _bool(record["present"]),
            record["value"],
        )
    return result


def _live_entities(generations: list[int], alive: list[bool]) -> set[str]:
    return {f"{index}:{generations[index]}" for index, is_alive in enumerate(alive) if is_alive}


def _canonical_not_equal(left: JsonValue, right: JsonValue) -> bool:
    return canonical_dumps(left) != canonical_dumps(right)


def _entity_sort_key(value: str) -> tuple[int, int]:
    index, generation = value.split(":", 1)
    return (int(index), int(generation))


def _component_key(value: tuple[str, str]) -> tuple[int, int, str]:
    entity = _entity_sort_key(value[0])
    return (entity[0], entity[1], value[1])


def _object(value: JsonValue) -> dict[str, JsonValue]:
    assert isinstance(value, dict)
    return value


def _array(value: JsonValue) -> list[JsonValue]:
    assert isinstance(value, list)
    return value


def _int_list(value: JsonValue) -> list[int]:
    values = _array(value)
    assert all(type(item) is int for item in values)
    return cast(list[int], values)


def _bool_list(value: JsonValue) -> list[bool]:
    values = _array(value)
    assert all(type(item) is bool for item in values)
    return cast(list[bool], values)


def _int(value: JsonValue) -> int:
    assert type(value) is int
    return value


def _bool(value: JsonValue) -> bool:
    assert type(value) is bool
    return value


def _str(value: JsonValue) -> str:
    assert type(value) is str
    return value


def _at[T](values: list[T], index: int) -> T | None:
    return values[index] if index < len(values) else None
