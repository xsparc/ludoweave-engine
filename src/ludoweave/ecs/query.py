# pyright: reportPrivateUsage=false
"""Storage-neutral typed query builders and explicit row cursor lifecycles.

Protected protocol hooks are intentionally called by their cursor collaborator
without becoming part of the public ``World`` API.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import TracebackType
from typing import Protocol, cast

from ludoweave.ecs.entity import EntityId
from ludoweave.ecs.errors import QueryLifecycleError


class QueryOrder(StrEnum):
    """Publicly meaningful query ordering choices."""

    NATIVE = "native"
    STABLE = "stable"


@dataclass(frozen=True, slots=True)
class QuerySpec:
    """Immutable storage-neutral query specification shared by world models."""

    included: tuple[type[object], ...]
    excluded: tuple[type[object], ...] = ()
    writable: tuple[type[object], ...] = ()
    changed_since: int | None = None
    changed_types: tuple[type[object], ...] = ()
    order: QueryOrder = QueryOrder.NATIVE


@dataclass(slots=True)
class QueryRowState:
    """Detached values plus captured scalar signatures for one candidate row."""

    entity_id: EntityId
    values: tuple[object, ...]
    signatures: tuple[tuple[object, ...], ...]


class QueryBackend(Protocol):
    """Internal storage-neutral hooks supplied independently by each world."""

    def _make_query_spec(
        self,
        included: tuple[type[object], ...],
        *,
        excluded: tuple[type[object], ...] = (),
        writable: tuple[type[object], ...] = (),
        changed_since: int | None = None,
        changed_types: tuple[type[object], ...] = (),
        order: QueryOrder = QueryOrder.NATIVE,
    ) -> QuerySpec: ...

    def _open_query(self, spec: QuerySpec) -> tuple[QueryRowState, ...]: ...

    def _commit_query_row(self, spec: QuerySpec, row: QueryRowState) -> None: ...

    def _release_query(self, spec: QuerySpec) -> None: ...


class Query[*ComponentTs]:
    """Immutable typed query builder detached from concrete storage layout."""

    __slots__ = ("_backend", "_spec")

    def __init__(self, backend: QueryBackend, spec: QuerySpec) -> None:
        self._backend = backend
        self._spec = spec

    def without(self, *component_types: type[object]) -> Query[*ComponentTs]:
        """Return a builder excluding entities with any supplied component."""

        spec = self._backend._make_query_spec(
            self._spec.included,
            excluded=(*self._spec.excluded, *component_types),
            writable=self._spec.writable,
            changed_since=self._spec.changed_since,
            changed_types=self._spec.changed_types,
            order=self._spec.order,
        )
        return Query(self._backend, spec)

    def writes(self, *component_types: type[object]) -> Query[*ComponentTs]:
        """Return a builder declaring included mutable component copies writable."""

        spec = self._backend._make_query_spec(
            self._spec.included,
            excluded=self._spec.excluded,
            writable=(*self._spec.writable, *component_types),
            changed_since=self._spec.changed_since,
            changed_types=self._spec.changed_types,
            order=self._spec.order,
        )
        return Query(self._backend, spec)

    def changed_since(self, epoch: int, *component_types: type[object]) -> Query[*ComponentTs]:
        """Return a builder matching rows changed strictly after ``epoch``."""

        watched = component_types or self._spec.included
        spec = self._backend._make_query_spec(
            self._spec.included,
            excluded=self._spec.excluded,
            writable=self._spec.writable,
            changed_since=epoch,
            changed_types=watched,
            order=self._spec.order,
        )
        return Query(self._backend, spec)

    def stable(self) -> Query[*ComponentTs]:
        """Return a builder requesting ascending generational entity order."""

        spec = self._backend._make_query_spec(
            self._spec.included,
            excluded=self._spec.excluded,
            writable=self._spec.writable,
            changed_since=self._spec.changed_since,
            changed_types=self._spec.changed_types,
            order=QueryOrder.STABLE,
        )
        return Query(self._backend, spec)

    def rows(self) -> QueryRows[*ComponentTs]:
        """Create one single-use row cursor for the current builder."""

        return QueryRows(self._backend, self._spec)


class QueryRows[*ComponentTs]:
    """Single-use iterator whose explicit lifecycle protects world mutation."""

    __slots__ = (
        "_backend",
        "_closed",
        "_context_entered",
        "_current",
        "_index",
        "_rows",
        "_spec",
        "_started",
    )

    def __init__(self, backend: QueryBackend, spec: QuerySpec) -> None:
        self._backend = backend
        self._spec = spec
        self._rows: tuple[QueryRowState, ...] = ()
        self._index = 0
        self._current: QueryRowState | None = None
        self._started = False
        self._closed = False
        self._context_entered = False

    def __enter__(self) -> QueryRows[*ComponentTs]:
        if self._closed or self._started or self._context_entered:
            raise _query_lifecycle_error(
                "query row cursor cannot be entered more than once", phase="enter"
            )
        self._context_entered = True
        self._start()
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        del exception, traceback
        if exception_type is None:
            self.close()
        else:
            self._close_without_commit()
        return False

    def __iter__(self) -> QueryRows[*ComponentTs]:
        if self._spec.writable and not self._context_entered:
            raise _query_lifecycle_error(
                "writable query rows require a context manager", phase="iterate"
            )
        self._start()
        return self

    def __next__(self) -> tuple[EntityId, *ComponentTs]:
        if self._closed:
            raise StopIteration
        if self._spec.writable and not self._context_entered:
            raise _query_lifecycle_error(
                "writable query rows require a context manager", phase="iterate"
            )
        self._start()
        self._commit_current()
        if self._index >= len(self._rows):
            self._finish_release()
            raise StopIteration
        self._current = self._rows[self._index]
        self._index += 1
        row = (self._current.entity_id, *self._current.values)
        return cast(tuple[EntityId, *ComponentTs], row)

    def close(self) -> None:
        """Commit the current writable row and release the cursor idempotently."""

        if self._closed:
            return
        try:
            self._commit_current()
        finally:
            self._finish_release()

    @property
    def closed(self) -> bool:
        """Return whether this cursor has released its world ownership."""

        return self._closed

    def abort(self) -> None:
        """Discard the current writable row and release ownership idempotently."""

        self._close_without_commit()

    def _start(self) -> None:
        if self._closed:
            raise _query_lifecycle_error("query row cursor is already closed", phase="iterate")
        if self._started:
            return
        try:
            self._rows = self._backend._open_query(self._spec)
        except Exception:
            self._closed = True
            raise
        self._started = True

    def _commit_current(self) -> None:
        current = self._current
        if current is None:
            return
        self._current = None
        if self._spec.writable:
            try:
                self._backend._commit_query_row(self._spec, current)
            except Exception:
                self._finish_release()
                raise

    def _close_without_commit(self) -> None:
        if self._closed:
            return
        self._current = None
        self._finish_release()

    def _finish_release(self) -> None:
        if self._closed:
            return
        if self._started:
            self._backend._release_query(self._spec)
        self._closed = True


def _query_lifecycle_error(message: str, *, phase: str) -> QueryLifecycleError:
    return QueryLifecycleError(
        message,
        code="ecs.query_lifecycle",
        subsystem="ecs",
        phase=phase,
    )
