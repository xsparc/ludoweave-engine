"""Validated engine configuration values."""

from dataclasses import dataclass

from ludoweave.core.errors import ConfigurationError


@dataclass(frozen=True, slots=True)
class EngineConfig:
    """Configuration for the M0 fixed-tick runner.

    The object is immutable and safe to share. It does not contain backend
    objects, environment-derived paths, or canonical world state.
    """

    fixed_hz: int = 60

    def __post_init__(self) -> None:
        fixed_hz = self.fixed_hz
        if type(fixed_hz) is not int:
            raise ConfigurationError(
                "fixed_hz must be an integer",
                code="config.invalid_fixed_hz",
                subsystem="application",
                phase="configuration",
                details={"fixed_hz": repr(fixed_hz)},
            )
        if self.fixed_hz <= 0:
            raise ConfigurationError(
                "fixed_hz must be greater than zero",
                code="config.invalid_fixed_hz",
                subsystem="application",
                phase="configuration",
                details={"fixed_hz": self.fixed_hz},
            )
