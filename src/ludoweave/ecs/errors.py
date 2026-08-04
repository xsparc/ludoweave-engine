"""Structured failures raised by the deterministic world core."""

from ludoweave.core.errors import LudoWeaveError


class EntityError(LudoWeaveError):
    """Base class for entity identity and allocation failures."""


class InvalidEntityIdError(EntityError):
    """Raised when a public operation receives a malformed entity ID."""


class StaleEntityError(EntityError):
    """Raised when an entity ID does not identify a currently live entity."""


class ComponentError(LudoWeaveError):
    """Base class for component schema and migration failures."""


class ComponentSchemaError(ComponentError):
    """Raised when a component declaration violates the schema contract."""


class DuplicateComponentError(ComponentError):
    """Raised when registry identity indexes would become ambiguous."""


class UnknownComponentError(ComponentError):
    """Raised when a registry lookup cannot resolve a component schema."""


class IncompatibleComponentVersionError(ComponentError):
    """Raised when a component version cannot migrate to the current schema."""


class ComponentMigrationError(ComponentError):
    """Raised when migration execution or output validation fails."""


class WorldError(LudoWeaveError):
    """Base class for canonical world storage failures."""


class ComponentAlreadyPresentError(WorldError):
    """Raised when an entity already owns a requested component type."""


class MissingComponentError(WorldError):
    """Raised when an entity does not own a requested component type."""


class InvalidComponentValueError(WorldError):
    """Raised when a component instance or patch violates its schema."""


class QueryError(LudoWeaveError):
    """Base class for query specification, iteration, and writeback failures."""


class InvalidQueryError(QueryError):
    """Raised when a query specification is malformed or incompatible."""


class QueryLifecycleError(QueryError):
    """Raised when a query cursor is entered, iterated, or closed incorrectly."""


class ActiveQueryError(QueryError):
    """Raised when an operation conflicts with active query ownership."""


class CommandsError(LudoWeaveError):
    """Base class for local deferred structural command failures."""


class CommandBufferStateError(CommandsError):
    """Raised when a command buffer is used with the wrong world or generation."""


class InvalidDeferredEntityError(CommandsError):
    """Raised when a deferred entity token is forged, stale, or foreign."""


class DeferredCommandError(CommandsError):
    """Raised when an atomic local command-buffer flush cannot be applied."""


class ResourceError(LudoWeaveError):
    """Base class for resource identity, ownership, and storage failures."""


class InvalidResourceSpecError(ResourceError):
    """Raised when a typed resource declaration is malformed."""


class DuplicateResourceError(ResourceError):
    """Raised when a resource identity or singleton slot is duplicated."""


class UnknownResourceError(ResourceError):
    """Raised when a resource key is not owned by the selected registry."""


class MissingResourceError(ResourceError):
    """Raised when a registered resource has no value in a store."""


class ResourceCopyError(ResourceError):
    """Raised when explicit resource detachment fails its contract."""


class SystemError(LudoWeaveError):
    """Base class for system declarations and metadata failures."""


class InvalidSystemSpecError(SystemError):
    """Raised when a system declaration is malformed or inconsistent."""


class ScheduleError(LudoWeaveError):
    """Base class for deterministic schedule construction failures."""


class DuplicateSystemError(ScheduleError):
    """Raised when a schedule contains duplicate system identities."""


class UnknownSystemDependencyError(ScheduleError):
    """Raised when a system ordering edge names no registered system."""


class InvalidSystemDependencyError(ScheduleError):
    """Raised for self, duplicate, or cross-phase ordering edges."""


class ScheduleConflictError(ScheduleError):
    """Raised when a same-phase write conflict lacks explicit ordering."""


class ScheduleCycleError(ScheduleError):
    """Raised when explicit ordering contains a deterministic cycle."""


class NondeterministicSystemError(ScheduleError):
    """Raised when deterministic planning includes ineligible work or resources."""


class UnsupportedExecutionClassError(ScheduleError):
    """Raised when M1 planning receives a non-Python execution class."""
