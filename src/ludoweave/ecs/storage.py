"""Private pure-Python dense rows with sparse entity-index locations."""

from __future__ import annotations

from collections.abc import Callable

from ludoweave.ecs.entity import EntityId

_MISSING_ROW = -1


class DenseComponentTable:
    """One component type's private dense/sparse storage.

    Dense offsets are deliberately absent from public APIs. Full generational
    IDs are retained in dense rows so reuse of a sparse index cannot make an
    old allocation observe a replacement entity's component.
    """

    __slots__ = (
        "_changed_epochs",
        "_entities",
        "_sparse",
        "_values",
        "structural_epoch",
    )

    def __init__(self) -> None:
        self._entities: list[EntityId] = []
        self._values: list[object] = []
        self._changed_epochs: list[int] = []
        self._sparse: list[int] = []
        self.structural_epoch = 0

    def __len__(self) -> int:
        return len(self._entities)

    def contains(self, entity_id: EntityId) -> bool:
        row = self._located_row(entity_id)
        return row is not None

    def add(self, entity_id: EntityId, value: object, *, epoch: int) -> None:
        self._ensure_sparse_index(entity_id.index)
        row = len(self._entities)
        self._entities.append(entity_id)
        self._values.append(value)
        self._changed_epochs.append(epoch)
        self._sparse[entity_id.index] = row
        self.structural_epoch = epoch

    def get(self, entity_id: EntityId) -> object:
        row = self._located_row(entity_id)
        if row is None:
            raise KeyError(entity_id)
        return self._values[row]

    def changed_epoch(self, entity_id: EntityId) -> int:
        row = self._located_row(entity_id)
        if row is None:
            raise KeyError(entity_id)
        return self._changed_epochs[row]

    def replace(self, entity_id: EntityId, value: object, *, epoch: int) -> None:
        row = self._located_row(entity_id)
        if row is None:
            raise KeyError(entity_id)
        self._values[row] = value
        self._changed_epochs[row] = epoch

    def remove(self, entity_id: EntityId, *, epoch: int) -> object:
        row = self._located_row(entity_id)
        if row is None:
            raise KeyError(entity_id)
        last_row = len(self._entities) - 1
        removed = self._values[row]
        if row != last_row:
            moved_entity = self._entities[last_row]
            self._entities[row] = moved_entity
            self._values[row] = self._values[last_row]
            self._changed_epochs[row] = self._changed_epochs[last_row]
            self._sparse[moved_entity.index] = row
        self._entities.pop()
        self._values.pop()
        self._changed_epochs.pop()
        self._sparse[entity_id.index] = _MISSING_ROW
        self.structural_epoch = epoch
        return removed

    def items(self) -> tuple[tuple[EntityId, object], ...]:
        return tuple(zip(self._entities, self._values, strict=True))

    def entity_ids(self) -> tuple[EntityId, ...]:
        """Return the private dense entity order for internal plan execution."""

        return tuple(self._entities)

    def clone(self, copy_value: Callable[[object], object]) -> DenseComponentTable:
        duplicate = DenseComponentTable()
        duplicate._entities = list(self._entities)
        duplicate._values = [copy_value(value) for value in self._values]
        duplicate._changed_epochs = list(self._changed_epochs)
        duplicate._sparse = list(self._sparse)
        duplicate.structural_epoch = self.structural_epoch
        return duplicate

    def check_invariants(self) -> None:
        assert len(self._entities) == len(self._values) == len(self._changed_epochs)
        for row, entity_id in enumerate(self._entities):
            assert entity_id.index < len(self._sparse)
            assert self._sparse[entity_id.index] == row
        for index, row in enumerate(self._sparse):
            if row != _MISSING_ROW:
                assert row < len(self._entities)
                assert self._entities[row].index == index

    def _located_row(self, entity_id: EntityId) -> int | None:
        if entity_id.index >= len(self._sparse):
            return None
        row = self._sparse[entity_id.index]
        if row == _MISSING_ROW or self._entities[row] != entity_id:
            return None
        return row

    def _ensure_sparse_index(self, index: int) -> None:
        missing = index + 1 - len(self._sparse)
        if missing > 0:
            self._sparse.extend([_MISSING_ROW] * missing)
