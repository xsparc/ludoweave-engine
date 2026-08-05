"""Immutable contracts owned by the transport-independent agent service."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

from ludoweave.agent.errors import AgentRequestError
from ludoweave.world.canonical import JsonValue, validate_json_value

AGENT_SERVICE_PROTOCOL = "ludoweave.agent.service/1"
AGENT_ERROR_PROTOCOL = "ludoweave.agent.error/1"

_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+-]{0,127}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AgentCapabilities:
    """Explicit service capabilities; write access is disabled by default."""

    write: bool = False
    capture: bool = False
    tests: bool = False

    def __post_init__(self) -> None:
        for name in ("capture", "tests", "write"):
            if type(getattr(self, name)) is not bool:
                raise _request_error(
                    "agent capability flags must be exact booleans",
                    code="agent.invalid_capabilities",
                    phase="configure",
                    details={"field": name},
                )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "read": True,
            "write": self.write,
            "capture": self.capture,
            "tests": self.tests,
        }


@dataclass(frozen=True, slots=True)
class AgentLimits:
    """Whole-request, result, mutation, capture, and rate bounds."""

    max_request_bytes: int = 1_048_576
    max_result_bytes: int = 8_388_608
    max_query_entities: int = 1_000
    max_transaction_bytes: int = 1_048_576
    max_transaction_commands: int = 256
    max_ticks_per_request: int = 600
    max_snapshot_bytes: int = 67_108_864
    max_capture_pixels: int = 2_073_600
    max_test_names: int = 32
    max_requests_per_window: int = 120
    rate_window_ns: int = 60_000_000_000

    def __post_init__(self) -> None:
        for name in (
            "max_capture_pixels",
            "max_query_entities",
            "max_request_bytes",
            "max_requests_per_window",
            "max_result_bytes",
            "max_snapshot_bytes",
            "max_test_names",
            "max_ticks_per_request",
            "max_transaction_bytes",
            "max_transaction_commands",
            "rate_window_ns",
        ):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise _request_error(
                    "agent limits must be positive integers",
                    code="agent.invalid_limits",
                    phase="configure",
                    details={"field": name, "actual_type": type(value).__name__},
                )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "max_capture_pixels": self.max_capture_pixels,
            "max_query_entities": self.max_query_entities,
            "max_request_bytes": self.max_request_bytes,
            "max_requests_per_window": self.max_requests_per_window,
            "max_result_bytes": self.max_result_bytes,
            "max_snapshot_bytes": self.max_snapshot_bytes,
            "max_test_names": self.max_test_names,
            "max_ticks_per_request": self.max_ticks_per_request,
            "max_transaction_bytes": self.max_transaction_bytes,
            "max_transaction_commands": self.max_transaction_commands,
            "rate_window_ns": self.rate_window_ns,
        }


@dataclass(frozen=True, slots=True)
class AgentProject:
    """Stable project identity exposed without filesystem or environment data."""

    project_id: str
    name: str
    project_schema: str
    dependency_lock_hash: str
    platform_profile: str
    description: str = ""

    def __post_init__(self) -> None:
        for name in ("name", "platform_profile", "project_id"):
            value = getattr(self, name)
            if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
                raise _request_error(
                    "agent project identity must use bounded stable text",
                    code="agent.invalid_project",
                    phase="configure",
                    details={"field": name},
                )
        for name in ("dependency_lock_hash", "project_schema"):
            value = getattr(self, name)
            if type(value) is not str or _SHA256.fullmatch(value) is None:
                raise _request_error(
                    "agent project hashes must use SHA-256 identifiers",
                    code="agent.invalid_project",
                    phase="configure",
                    details={"field": name},
                )
        if type(self.description) is not str or len(self.description.encode("utf-8")) > 4_096:
            raise _request_error(
                "agent project description must be bounded text",
                code="agent.invalid_project",
                phase="configure",
                details={"field": "description"},
            )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "project_schema": self.project_schema,
            "dependency_lock_hash": self.dependency_lock_hash,
            "platform_profile": self.platform_profile,
        }


@dataclass(frozen=True, slots=True)
class AgentCapture:
    """Provider-neutral immutable RGBA8 capture."""

    width: int
    height: int
    pixels: bytes

    def __post_init__(self) -> None:
        if (
            type(self.width) is not int
            or self.width <= 0
            or type(self.height) is not int
            or self.height <= 0
        ):
            raise _request_error(
                "agent capture dimensions must be positive integers",
                code="agent.invalid_capture",
                phase="capture",
                details={"field": "extent"},
            )
        if type(self.pixels) is not bytes or len(self.pixels) != self.width * self.height * 4:
            raise _request_error(
                "agent capture must contain tightly packed immutable RGBA8 pixels",
                code="agent.invalid_capture",
                phase="capture",
                details={"field": "pixels"},
            )


class AgentCaptureProvider(Protocol):
    """Application-owned presentation provider injected into the service."""

    def capture(self, width: int, height: int) -> AgentCapture: ...

    def close(self) -> None: ...


@dataclass(frozen=True, slots=True)
class AgentTestResult:
    """One bounded test result from an explicit composition-owned allowlist."""

    name: str
    passed: bool
    diagnostics: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.name) is not str or _STABLE_ID.fullmatch(self.name) is None:
            raise _request_error(
                "agent test names must use bounded stable text",
                code="agent.invalid_test_result",
                phase="test",
                details={"field": "name"},
            )
        if type(self.passed) is not bool:
            raise _request_error(
                "agent test status must be an exact boolean",
                code="agent.invalid_test_result",
                phase="test",
                details={"field": "passed"},
            )
        diagnostics = tuple(self.diagnostics)
        if len(diagnostics) > 16 or any(
            type(item) is not str or len(item.encode("utf-8")) > 1_024 for item in diagnostics
        ):
            raise _request_error(
                "agent test diagnostics exceed their bounded text contract",
                code="agent.invalid_test_result",
                phase="test",
                details={"field": "diagnostics"},
            )
        object.__setattr__(self, "diagnostics", diagnostics)

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "name": self.name,
            "passed": self.passed,
            "diagnostics": list(self.diagnostics),
        }


class AgentTestProvider(Protocol):
    """Trusted local test allowlist; it never launches a shell or imports by name."""

    def test_names(self) -> tuple[str, ...]: ...

    def run_tests(self, names: Sequence[str]) -> tuple[AgentTestResult, ...]: ...


class AgentTelemetryProvider(Protocol):
    """Optional application telemetry projected into bounded JSON values."""

    def telemetry(self) -> Mapping[str, object]: ...


def validated_telemetry(value: Mapping[str, object]) -> dict[str, JsonValue]:
    """Return a detached JSON-domain telemetry object."""

    checked = validate_json_value(dict(value))
    if not isinstance(checked, dict):
        raise AssertionError("validated telemetry mapping did not remain an object")
    return checked


def _request_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> AgentRequestError:
    return AgentRequestError(
        message,
        code=code,
        subsystem="agent",
        phase=phase,
        details=details,
    )
