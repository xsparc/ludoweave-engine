# pyright: reportPrivateUsage=false
"""Explicit typed resource keys, registries, and copy-owned singleton values."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import cast

from ludoweave.ecs.errors import (
    DuplicateResourceError,
    InvalidResourceSpecError,
    MissingResourceError,
    ResourceCopyError,
    UnknownResourceError,
)

_RESOURCE_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.:-]*\Z")
_IMMUTABLE_SCALAR_TYPES = (bool, int, float, str, bytes, type(None))


@dataclass(frozen=True, slots=True, eq=False, init=False)
class ResourceSpec[ResourceT]:
    """Exact typed singleton key with an explicit detachment operation."""

    name: str
    value_type: type[ResourceT]
    deterministic: bool
    qualified_type_name: str
    _copier: Callable[[ResourceT], ResourceT] = field(repr=False, compare=False)

    def __init__(
        self,
        name: str,
        value_type: type[ResourceT],
        copier: Callable[[ResourceT], ResourceT],
        *,
        deterministic: bool = True,
    ) -> None:
        checked_name = _validate_resource_name(name)
        checked_type, qualified_name = _validate_resource_type(value_type)
        if not callable(copier):
            raise _invalid_resource_spec(
                "resource copier must be callable",
                details={"resource": checked_name, "actual_type": type(copier).__name__},
            )
        if type(deterministic) is not bool:
            raise _invalid_resource_spec(
                "resource deterministic eligibility must be a boolean",
                details={
                    "resource": checked_name,
                    "actual_type": type(deterministic).__name__,
                },
            )
        object.__setattr__(self, "name", checked_name)
        object.__setattr__(self, "value_type", checked_type)
        object.__setattr__(self, "deterministic", deterministic)
        object.__setattr__(self, "qualified_type_name", qualified_name)
        object.__setattr__(self, "_copier", copier)

    def _copy(self, value: ResourceT, *, operation: str) -> ResourceT:
        if type(value) is not self.value_type:
            raise _resource_copy_error(
                "resource value must have its key's exact type",
                spec=self,
                operation=operation,
                details={"actual_type": type(value).__name__},
            )
        try:
            copied = self._copier(value)
        except Exception as error:
            raise _resource_copy_error(
                "resource copier raised an exception",
                spec=self,
                operation=operation,
                details={"cause_type": type(error).__name__},
            ) from error
        if type(copied) is not self.value_type:
            raise _resource_copy_error(
                "resource copier returned the wrong exact type",
                spec=self,
                operation=operation,
                details={"actual_type": type(copied).__name__},
            )
        if copied is value and self.value_type not in _IMMUTABLE_SCALAR_TYPES:
            raise _resource_copy_error(
                "resource copier must return a detached instance",
                spec=self,
                operation=operation,
                details={"reason": "same_instance"},
            )
        return copied


class ResourceRegistry:
    """Immutable explicit registry of identity-owned resource specifications."""

    __slots__ = ("_by_name", "_specs")

    def __init__(self, specs: Iterable[object] = ()) -> None:
        by_name: dict[str, ResourceSpec[object]] = {}
        for candidate in _materialize_resource_items(specs, phase="register", role="specs"):
            if not isinstance(candidate, ResourceSpec):
                raise _invalid_resource_spec(
                    "resource registry entries must be ResourceSpec values",
                    details={"actual_type": type(candidate).__name__},
                    phase="register",
                )
            spec = cast(ResourceSpec[object], candidate)
            if spec.name in by_name:
                raise DuplicateResourceError(
                    "resource identity is already registered",
                    code="ecs.duplicate_resource",
                    subsystem="ecs",
                    phase="register",
                    details={"resource": spec.name},
                )
            by_name[spec.name] = spec
        self._by_name = MappingProxyType(by_name)
        self._specs = tuple(by_name[name] for name in sorted(by_name))

    @property
    def specs(self) -> tuple[ResourceSpec[object], ...]:
        return self._specs

    def contains(self, spec: object) -> bool:
        """Return whether this registry owns this exact specification object."""

        return isinstance(spec, ResourceSpec) and self._by_name.get(spec.name) is spec

    def spec_for_name(self, name: str) -> ResourceSpec[object]:
        checked = _validate_resource_name(name, phase="lookup")
        spec = self._by_name.get(checked)
        if spec is None:
            raise UnknownResourceError(
                "resource identity is not registered",
                code="ecs.unknown_resource",
                subsystem="ecs",
                phase="lookup",
                details={"resource": checked},
            )
        return spec


class ResourceStore:
    """Single-owner resource values copied at every public boundary."""

    __slots__ = ("_registry", "_values")

    def __init__(
        self,
        registry: ResourceRegistry,
        initial: Iterable[tuple[object, object]] = (),
    ) -> None:
        self._registry = registry
        self._values: dict[ResourceSpec[object], object] = {}
        for candidate in _materialize_resource_items(initial, phase="insert", role="initial"):
            if type(candidate) is not tuple:
                raise _invalid_resource_spec(
                    "initial resource entries must be two-item tuples",
                    details={"actual_type": type(candidate).__name__},
                    phase="insert",
                )
            entry = cast(tuple[object, ...], candidate)
            if len(entry) != 2:
                raise _invalid_resource_spec(
                    "initial resource entries must be two-item tuples",
                    details={"actual_type": "tuple"},
                    phase="insert",
                )
            spec, value = entry
            self._insert_object(spec, value)

    @property
    def registry(self) -> ResourceRegistry:
        return self._registry

    def __len__(self) -> int:
        return len(self._values)

    def contains(self, spec: object) -> bool:
        """Return whether one registered key currently has a value."""

        checked = self._validate_spec(spec, operation="contains")
        return checked in self._values

    def insert[ResourceT](self, spec: ResourceSpec[ResourceT], value: ResourceT) -> None:
        """Copy a value into an empty registered singleton slot."""

        self._insert_object(spec, value)

    def require[ResourceT](self, spec: ResourceSpec[ResourceT]) -> ResourceT:
        """Return a detached copy of one required singleton value."""

        checked = self._validate_spec(spec, operation="require")
        value = self._require_value(checked, operation="require")
        return spec._copy(cast(ResourceT, value), operation="require")

    def replace[ResourceT](self, spec: ResourceSpec[ResourceT], value: ResourceT) -> ResourceT:
        """Replace one singleton after a contract-compliant adapter succeeds."""

        checked = self._validate_spec(spec, operation="replace")
        previous = self._require_value(checked, operation="replace")
        replacement = spec._copy(value, operation="replace")
        returned = spec._copy(cast(ResourceT, previous), operation="replace_return")
        self._values[checked] = replacement
        return returned

    def remove[ResourceT](self, spec: ResourceSpec[ResourceT]) -> ResourceT:
        """Remove one singleton and transfer a detached value to the caller."""

        checked = self._validate_spec(spec, operation="remove")
        previous = self._require_value(checked, operation="remove")
        returned = spec._copy(cast(ResourceT, previous), operation="remove")
        del self._values[checked]
        return returned

    def replace_many(self, replacements: Iterable[tuple[object, object]]) -> None:
        """Atomically adopt copied replacements under the trusted-adapter contract."""

        copied: dict[ResourceSpec[object], object] = {}
        for candidate in _materialize_resource_items(
            replacements, phase="replace_many", role="replacements"
        ):
            if type(candidate) is not tuple:
                raise _invalid_resource_spec(
                    "resource replacements must be two-item tuples",
                    details={"actual_type": type(candidate).__name__},
                    phase="replace_many",
                )
            entry = cast(tuple[object, ...], candidate)
            if len(entry) != 2:
                raise _invalid_resource_spec(
                    "resource replacements must be two-item tuples",
                    details={"actual_type": "tuple"},
                    phase="replace_many",
                )
            spec, value = entry
            checked = self._validate_spec(spec, operation="replace_many")
            self._require_value(checked, operation="replace_many")
            if checked in copied:
                raise DuplicateResourceError(
                    "resource replacement batch repeats a key",
                    code="ecs.duplicate_resource",
                    subsystem="ecs",
                    phase="replace_many",
                    details={"resource": checked.name},
                )
            copied[checked] = checked._copy(value, operation="replace_many")
        self._values.update(copied)

    def clone(self) -> ResourceStore:
        """Create an independently copy-owned resource store."""

        duplicate = ResourceStore(self._registry)
        copied: dict[ResourceSpec[object], object] = {}
        for spec in self._registry.specs:
            if spec in self._values:
                copied[spec] = spec._copy(self._values[spec], operation="clone")
        duplicate._values = copied
        return duplicate

    def _insert_object(self, spec: object, value: object) -> None:
        checked = self._validate_spec(spec, operation="insert")
        if checked in self._values:
            raise DuplicateResourceError(
                "resource singleton already has a value",
                code="ecs.duplicate_resource",
                subsystem="ecs",
                phase="insert",
                details={"resource": checked.name},
            )
        copied = checked._copy(value, operation="insert")
        self._values[checked] = copied

    def _validate_spec(self, spec: object, *, operation: str) -> ResourceSpec[object]:
        if not isinstance(spec, ResourceSpec):
            raise UnknownResourceError(
                "resource key is not owned by this registry",
                code="ecs.unknown_resource",
                subsystem="ecs",
                phase=operation,
                details={"resource": None, "actual_type": type(spec).__name__},
            )
        checked = cast(ResourceSpec[object], spec)
        if not self._registry.contains(checked):
            raise UnknownResourceError(
                "resource key is not owned by this registry",
                code="ecs.unknown_resource",
                subsystem="ecs",
                phase=operation,
                details={"resource": checked.name, "actual_type": "ResourceSpec"},
            )
        return checked

    def _require_value(self, spec: ResourceSpec[object], *, operation: str) -> object:
        try:
            return self._values[spec]
        except KeyError as error:
            raise MissingResourceError(
                "resource singleton has no value",
                code="ecs.missing_resource",
                subsystem="ecs",
                phase=operation,
                details={"resource": spec.name},
            ) from error


def _validate_resource_name(name: object, *, phase: str = "define") -> str:
    if type(name) is not str or _RESOURCE_NAME.fullmatch(name) is None:
        raise _invalid_resource_spec(
            "resource identity must be a stable nonempty name",
            details={"actual_type": type(name).__name__},
            phase=phase,
        )
    return name


def _materialize_resource_items(
    values: Iterable[object], *, phase: str, role: str
) -> tuple[object, ...]:
    if isinstance(values, (str, bytes)):
        raise _invalid_resource_spec(
            "resource declaration collection must be an iterable of values",
            details={"role": role, "actual_type": type(values).__name__},
            phase=phase,
        )
    try:
        return tuple(values)
    except Exception as error:
        raise _invalid_resource_spec(
            "resource declaration collection could not be materialized",
            details={
                "role": role,
                "actual_type": type(values).__name__,
                "cause_type": type(error).__name__,
            },
            phase=phase,
        ) from error


def _validate_resource_type(value_type: object) -> tuple[type[object], str]:
    if not isinstance(value_type, type):
        raise _invalid_resource_spec(
            "resource value type must be a class",
            details={"actual_type": type(value_type).__name__},
        )
    qualified_name = f"{value_type.__module__}.{value_type.__qualname__}"
    if "<locals>" in qualified_name or value_type.__name__ == "<lambda>":
        raise _invalid_resource_spec(
            "resource value type must have a stable module-qualified name",
            details={"resource_type": qualified_name},
        )
    return value_type, qualified_name


def _invalid_resource_spec(
    message: str,
    *,
    details: dict[str, str | int | float | bool | None],
    phase: str = "define",
) -> InvalidResourceSpecError:
    return InvalidResourceSpecError(
        message,
        code="ecs.invalid_resource_spec",
        subsystem="ecs",
        phase=phase,
        details=details,
    )


def _resource_copy_error[ResourceT](
    message: str,
    *,
    spec: ResourceSpec[ResourceT],
    operation: str,
    details: dict[str, str | int | float | bool | None],
) -> ResourceCopyError:
    return ResourceCopyError(
        message,
        code="ecs.resource_copy_failed",
        subsystem="ecs",
        phase=operation,
        details={
            "resource": spec.name,
            "resource_type": spec.qualified_type_name,
            **details,
        },
    )
