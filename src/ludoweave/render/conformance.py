"""Installed, provider-neutral conformance evidence for render devices."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from ludoweave.core.errors import LudoWeaveError, RenderError
from ludoweave.core.version import __version__
from ludoweave.platform import (
    CloseEvent,
    FocusEvent,
    GamepadAxisEvent,
    GamepadButtonEvent,
    GamepadConnectionEvent,
    KeyEvent,
    MouseButtonEvent,
    PointerEvent,
    ResizeEvent,
)
from ludoweave.render.contracts import (
    BufferData,
    BufferDescriptor,
    BufferUsage,
    CaptureImage,
    ClearCommand,
    Color,
    CommandList,
    PipelineDescriptor,
    RenderCapabilities,
    Submission,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureUsage,
)
from ludoweave.render.device import RenderDevice
from ludoweave.render.handles import (
    BufferHandle,
    PipelineHandle,
    SurfaceHandle,
    TextureHandle,
)

RENDER_DEVICE_CONFORMANCE_PROTOCOL: Final = "ludoweave.render-device-conformance/1"
RENDER_DEVICE_CONFORMANCE_PROFILE: Final = "render-device-baseline/1"

_ADAPTER_ID = re.compile(r"[a-z][a-z0-9]*(?:[._-][a-z0-9]+){1,15}\Z")
_BACKEND_NAME = re.compile(r"[a-z][a-z0-9._-]{0,63}\Z")
_ERROR_CODE = re.compile(r"conformance\.[a-z0-9_.-]{1,115}\Z")
_CHECK_IDS = (
    "factory",
    "identity_capabilities",
    "resource_handles",
    "clear_submission",
    "completion_capture",
    "resize_events",
    "stale_handle",
    "close_idempotence",
    "closed_rejection",
)
_GAMEPAD_EVENT_TYPES = (GamepadConnectionEvent, GamepadButtonEvent, GamepadAxisEvent)
_PLATFORM_EVENT_TYPES = (
    KeyEvent,
    MouseButtonEvent,
    PointerEvent,
    FocusEvent,
    ResizeEvent,
    CloseEvent,
    *_GAMEPAD_EVENT_TYPES,
)


class ConformanceStatus(StrEnum):
    """Stable result states used by installed conformance reports."""

    PASS = "pass"
    FAIL = "fail"
    NOT_RUN = "not_run"


@dataclass(frozen=True, slots=True)
class RenderDeviceConformanceCheck:
    """One deterministic check result without provider exception text."""

    check_id: str
    status: ConformanceStatus
    code: str | None = None

    def __post_init__(self) -> None:
        if type(self.check_id) is not str or self.check_id not in _CHECK_IDS:
            raise _request_error("check_id")
        if type(self.status) is not ConformanceStatus:
            raise _request_error("status")
        if self.status is ConformanceStatus.PASS:
            if self.code is not None:
                raise _request_error("code")
        elif type(self.code) is not str or _ERROR_CODE.fullmatch(self.code) is None:
            raise _request_error("code")

    def as_dict(self) -> dict[str, object]:
        """Return one JSON-compatible check record."""

        return {
            "id": self.check_id,
            "status": self.status.value,
            "code": self.code,
        }


@dataclass(frozen=True, slots=True)
class RenderDeviceConformanceReport:
    """Versioned evidence from one explicit render-device factory invocation."""

    adapter_id: str
    adapter_name: str | None
    status: ConformanceStatus
    checks: tuple[RenderDeviceConformanceCheck, ...]

    def __post_init__(self) -> None:
        _validate_adapter_id(self.adapter_id)
        if self.adapter_name is not None and (
            type(self.adapter_name) is not str or _BACKEND_NAME.fullmatch(self.adapter_name) is None
        ):
            raise _request_error("adapter_name")
        if type(self.status) is not ConformanceStatus or self.status is ConformanceStatus.NOT_RUN:
            raise _request_error("status")
        try:
            checks = tuple(self.checks)
        except Exception as error:
            raise _request_error("checks") from error
        if (
            len(checks) != len(_CHECK_IDS)
            or any(type(check) is not RenderDeviceConformanceCheck for check in checks)
            or tuple(check.check_id for check in checks) != _CHECK_IDS
        ):
            raise _request_error("checks")
        expected_status = (
            ConformanceStatus.PASS
            if all(check.status is ConformanceStatus.PASS for check in checks)
            else ConformanceStatus.FAIL
        )
        if self.status is not expected_status:
            raise _request_error("status")
        object.__setattr__(self, "checks", checks)

    @property
    def passed(self) -> bool:
        """Whether every baseline check passed."""

        return self.status is ConformanceStatus.PASS

    def as_dict(self) -> dict[str, object]:
        """Return deterministic, path-free, JSON-compatible evidence."""

        return {
            "protocol": RENDER_DEVICE_CONFORMANCE_PROTOCOL,
            "profile": RENDER_DEVICE_CONFORMANCE_PROFILE,
            "ludoweave_version": __version__,
            "adapter_id": self.adapter_id,
            "adapter_name": self.adapter_name,
            "status": self.status.value,
            "checks": [check.as_dict() for check in self.checks],
        }

    def to_json(self) -> str:
        """Encode canonical presentation JSON with a trailing newline."""

        return (
            json.dumps(
                self.as_dict(),
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )


class _CheckFailure(Exception):
    __slots__ = ("code",)

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(slots=True)
class _RunState:
    device: RenderDevice
    adapter_name: str | None = None
    capabilities: RenderCapabilities | None = None
    buffer: BufferHandle | None = None
    texture: TextureHandle | None = None
    pipeline: PipelineHandle | None = None
    surface: SurfaceHandle | None = None
    submission: Submission | None = None


def run_render_device_conformance(
    adapter_id: str,
    factory: Callable[[], RenderDevice],
) -> RenderDeviceConformanceReport:
    """Exercise one trusted, explicitly supplied render-device factory.

    The runner performs no discovery, import, installation, subprocess, network,
    or filesystem operation. It calls adapter code in-process on the calling
    thread, so callers must trust the factory and remain responsible for any
    provider prerequisites or isolation.
    """

    checked_id = _validate_adapter_id(adapter_id)
    if not callable(factory):
        raise _request_error("factory")

    checks: list[RenderDeviceConformanceCheck] = []
    state: _RunState | None = None
    blocked = False
    try:
        device = factory()
        state = _RunState(device)
    except Exception as error:
        checks.append(_failed("factory", error))
        blocked = True
    else:
        checks.append(_passed("factory"))

    stages: tuple[tuple[str, Callable[[_RunState], None]], ...] = (
        ("identity_capabilities", _check_identity_capabilities),
        ("resource_handles", _check_resource_handles),
        ("clear_submission", _check_clear_submission),
        ("completion_capture", _check_completion_capture),
        ("resize_events", _check_resize_events),
        ("stale_handle", _check_stale_handle),
    )
    try:
        for check_id, operation in stages:
            if blocked or state is None:
                checks.append(_not_run(check_id))
                continue
            try:
                operation(state)
            except Exception as error:
                checks.append(_failed(check_id, error))
                blocked = True
            else:
                checks.append(_passed(check_id))
    except BaseException:
        if state is not None:
            with suppress(BaseException):
                state.device.close()
        raise

    close_ok = False
    if state is None:
        checks.append(_not_run("close_idempotence"))
    else:
        try:
            state.device.close()
            state.device.close()
        except Exception as error:
            checks.append(_failed("close_idempotence", error))
        else:
            checks.append(_passed("close_idempotence"))
            close_ok = True

    if state is None or not close_ok:
        checks.append(_not_run("closed_rejection"))
    else:
        try:
            state.device.create_buffer(BufferDescriptor(4, BufferUsage.VERTEX))
        except LudoWeaveError as error:
            if error.code != "render.device_closed":
                checks.append(_failed("closed_rejection", error))
            else:
                checks.append(_passed("closed_rejection"))
        except Exception as error:
            checks.append(_failed("closed_rejection", error))
        else:
            checks.append(
                RenderDeviceConformanceCheck(
                    "closed_rejection",
                    ConformanceStatus.FAIL,
                    "conformance.expected_error",
                )
            )

    frozen_checks = tuple(checks)
    status = (
        ConformanceStatus.PASS
        if all(check.status is ConformanceStatus.PASS for check in frozen_checks)
        else ConformanceStatus.FAIL
    )
    return RenderDeviceConformanceReport(
        checked_id,
        None if state is None else state.adapter_name,
        status,
        frozen_checks,
    )


def _check_identity_capabilities(state: _RunState) -> None:
    name = state.device.name
    capabilities = state.device.capabilities
    if type(name) is not str or _BACKEND_NAME.fullmatch(name) is None:
        raise _CheckFailure("conformance.invalid_adapter_name")
    if type(capabilities) is not RenderCapabilities or capabilities.backend != name:
        raise _CheckFailure("conformance.invalid_capabilities")
    state.adapter_name = name
    state.capabilities = capabilities


def _check_resource_handles(state: _RunState) -> None:
    capabilities = _required(state.capabilities, "capabilities")
    target_format = capabilities.surface_formats[0]
    buffer = state.device.create_buffer(
        BufferDescriptor(4, BufferUsage.VERTEX | BufferUsage.COPY_DESTINATION),
        BufferData(b"LW17"),
    )
    texture = state.device.create_texture(
        TextureDescriptor(
            1,
            1,
            target_format,
            TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
            label="conformance-texture",
        ),
        TextureData(b"\xff\xff\xff\xff", 4),
    )
    pipeline = state.device.create_pipeline(
        PipelineDescriptor(target_format, label="conformance-pipeline")
    )
    surface = state.device.create_surface(
        SurfaceDescriptor(
            2,
            2,
            target_format,
            SurfaceKind.OFFSCREEN,
            "conformance-surface",
        )
    )
    if (
        type(buffer) is not BufferHandle
        or type(texture) is not TextureHandle
        or type(pipeline) is not PipelineHandle
        or type(surface) is not SurfaceHandle
        or len({buffer.scope, texture.scope, pipeline.scope, surface.scope}) != 1
    ):
        raise _CheckFailure("conformance.invalid_handles")
    state.buffer = buffer
    state.texture = texture
    state.pipeline = pipeline
    state.surface = surface


def _check_clear_submission(state: _RunState) -> None:
    surface = _required(state.surface, "surface")
    command_list = CommandList(
        "conformance-clear",
        (ClearCommand(surface, Color(0.25, 0.5, 0.75, 1.0)),),
        surface,
    )
    submission = state.device.submit((command_list,))
    if (
        type(submission) is not Submission
        or submission.command_lists != (command_list,)
        or submission.draw_calls != 0
        or submission.sprite_instances != 0
        or submission.tile_instances != 0
        or submission.debug_primitives != 0
        or submission.fence.scope != surface.scope
    ):
        raise _CheckFailure("conformance.invalid_submission")
    state.submission = submission


def _check_completion_capture(state: _RunState) -> None:
    submission = _required(state.submission, "submission")
    surface = _required(state.surface, "surface")
    capabilities = _required(state.capabilities, "capabilities")
    state.device.poll()
    if state.device.is_fence_complete(submission.fence) is not True:
        raise _CheckFailure("conformance.incomplete_fence")
    if capabilities.offscreen_capture:
        try:
            capture = state.device.capture_surface(surface)
        except LudoWeaveError as error:
            if error.code == "render.capability_missing":
                raise _CheckFailure("conformance.capability_mismatch") from error
            raise
        if (
            type(capture) is not CaptureImage
            or capture.width != 2
            or capture.height != 2
            or len(capture.pixels) != 16
        ):
            raise _CheckFailure("conformance.invalid_capture")
        return
    try:
        state.device.capture_surface(surface)
    except LudoWeaveError as error:
        if error.code != "render.capability_missing":
            raise _CheckFailure("conformance.capability_mismatch") from error
    else:
        raise _CheckFailure("conformance.capability_mismatch")


def _check_resize_events(state: _RunState) -> None:
    surface = _required(state.surface, "surface")
    state.device.resize_surface(surface, 3, 2)
    platform_events = state.device.drain_surface_events(surface)
    gamepad_events = state.device.poll_gamepads()
    if type(platform_events) is not tuple or any(
        type(event) not in _PLATFORM_EVENT_TYPES for event in platform_events
    ):
        raise _CheckFailure("conformance.invalid_platform_events")
    if type(gamepad_events) is not tuple or any(
        type(event) not in _GAMEPAD_EVENT_TYPES for event in gamepad_events
    ):
        raise _CheckFailure("conformance.invalid_gamepad_events")


def _check_stale_handle(state: _RunState) -> None:
    buffer = _required(state.buffer, "buffer")
    state.device.destroy(buffer)
    try:
        state.device.destroy(buffer)
    except LudoWeaveError as error:
        if error.code != "render.stale_handle":
            raise _CheckFailure("conformance.stale_handle_mismatch") from error
    else:
        raise _CheckFailure("conformance.expected_error")


def _required[ValueT](value: ValueT | None, field: str) -> ValueT:
    if value is None:
        raise _CheckFailure(f"conformance.missing_{field}")
    return value


def _passed(check_id: str) -> RenderDeviceConformanceCheck:
    return RenderDeviceConformanceCheck(check_id, ConformanceStatus.PASS)


def _not_run(check_id: str) -> RenderDeviceConformanceCheck:
    return RenderDeviceConformanceCheck(
        check_id,
        ConformanceStatus.NOT_RUN,
        "conformance.prerequisite_failed",
    )


def _failed(check_id: str, error: Exception) -> RenderDeviceConformanceCheck:
    if type(error) is _CheckFailure:
        code = error.code
    elif isinstance(error, LudoWeaveError):
        code = "conformance.structured_adapter_error"
    else:
        code = "conformance.unstructured_exception"
    return RenderDeviceConformanceCheck(check_id, ConformanceStatus.FAIL, code)


def _validate_adapter_id(value: object) -> str:
    if type(value) is not str or len(value) > 128 or _ADAPTER_ID.fullmatch(value) is None:
        raise _request_error("adapter_id")
    return value


def _request_error(field: str) -> RenderError:
    return RenderError(
        "render-device conformance request is invalid",
        code="render.conformance_invalid_request",
        subsystem="render",
        phase="conformance",
        details={"field": field},
    )
