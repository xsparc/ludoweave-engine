"""Installed render-device conformance value and failure tests."""

from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from ludoweave.core.errors import LudoWeaveError, RenderError
from ludoweave.platform import GamepadConnectionEvent
from ludoweave.render import (
    RENDER_DEVICE_CONFORMANCE_PROFILE,
    RENDER_DEVICE_CONFORMANCE_PROTOCOL,
    ConformanceStatus,
    NullRenderDevice,
    RenderCapabilities,
    RenderDevice,
    RenderDeviceConformanceCheck,
    RenderDeviceConformanceReport,
    TextureFormat,
    run_render_device_conformance,
)

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


def test_null_device_passes_exact_deterministic_profile() -> None:
    first = run_render_device_conformance("org.ludoweave.null", NullRenderDevice)
    second = run_render_device_conformance("org.ludoweave.null", NullRenderDevice)

    assert first == second
    assert first.passed
    assert first.adapter_name == "null-device"
    assert first.status is ConformanceStatus.PASS
    assert tuple(check.check_id for check in first.checks) == _CHECK_IDS
    assert all(check.status is ConformanceStatus.PASS for check in first.checks)
    document = first.as_dict()
    assert document["protocol"] == RENDER_DEVICE_CONFORMANCE_PROTOCOL
    assert document["profile"] == RENDER_DEVICE_CONFORMANCE_PROFILE
    assert document["adapter_id"] == "org.ludoweave.null"
    assert first.to_json().endswith("\n")
    assert "\\" not in first.to_json()


@pytest.mark.parametrize(
    "adapter_id",
    ["", "null", "Org.LudoWeave.Null", ".null", "org..null", "org/null", "a." + "b" * 129],
)
def test_invalid_adapter_identity_is_rejected_before_factory_call(adapter_id: str) -> None:
    called = False

    def factory() -> RenderDevice:
        nonlocal called
        called = True
        return NullRenderDevice()

    with pytest.raises(RenderError) as raised:
        run_render_device_conformance(adapter_id, factory)

    assert raised.value.code == "render.conformance_invalid_request"
    assert not called


def test_non_callable_factory_is_rejected() -> None:
    with pytest.raises(RenderError) as raised:
        run_render_device_conformance(
            "org.ludoweave.invalid",
            cast("object", object()),  # type: ignore[arg-type]
        )
    assert raised.value.code == "render.conformance_invalid_request"


def test_factory_failure_is_sanitized_and_remaining_checks_are_not_run() -> None:
    def factory() -> RenderDevice:
        raise RuntimeError(r"private failure at C:\Users\someone\secret")

    report = run_render_device_conformance("org.example.broken", factory)

    assert not report.passed
    assert report.adapter_name is None
    assert report.checks[0] == RenderDeviceConformanceCheck(
        "factory",
        ConformanceStatus.FAIL,
        "conformance.unstructured_exception",
    )
    assert all(check.status is ConformanceStatus.NOT_RUN for check in report.checks[1:])
    assert "private" not in report.to_json()
    assert "Users" not in report.to_json()


class _BadNameDevice(NullRenderDevice):
    @property
    def name(self) -> str:
        return r"C:\provider\device"


def test_invalid_provider_name_fails_without_echoing_the_value_and_still_closes() -> None:
    device = _BadNameDevice()
    report = run_render_device_conformance("org.example.bad-name", lambda: device)

    assert report.adapter_name is None
    assert report.checks[1] == RenderDeviceConformanceCheck(
        "identity_capabilities",
        ConformanceStatus.FAIL,
        "conformance.invalid_adapter_name",
    )
    assert report.checks[-2].status is ConformanceStatus.PASS
    assert report.checks[-1].status is ConformanceStatus.PASS
    assert "provider" not in report.to_json()


class _CaptureMismatchDevice(NullRenderDevice):
    @property
    def capabilities(self) -> RenderCapabilities:
        return RenderCapabilities(
            backend=self.name,
            max_texture_dimension_2d=16_384,
            offscreen_capture=True,
            timestamp_queries=False,
            surface_formats=(TextureFormat.RGBA8_UNORM,),
        )


def test_capability_claim_must_match_observed_capture_behavior() -> None:
    report = run_render_device_conformance(
        "org.example.capture-mismatch",
        _CaptureMismatchDevice,
    )

    capture_check = report.checks[_CHECK_IDS.index("completion_capture")]
    assert capture_check.status is ConformanceStatus.FAIL
    assert capture_check.code == "conformance.capability_mismatch"
    assert report.checks[_CHECK_IDS.index("resize_events")].status is ConformanceStatus.NOT_RUN
    assert report.checks[-2].status is ConformanceStatus.PASS


class _UnstructuredResourceFailure(NullRenderDevice):
    def create_pipeline(self, descriptor: object) -> object:  # type: ignore[override]
        del descriptor
        raise RuntimeError("token=secret-provider-value")


def test_unstructured_provider_failure_is_reduced_to_a_stable_code() -> None:
    report = run_render_device_conformance(
        "org.example.unstructured",
        cast("type[RenderDevice]", _UnstructuredResourceFailure),
    )

    resource_check = report.checks[_CHECK_IDS.index("resource_handles")]
    assert resource_check.code == "conformance.unstructured_exception"
    assert "secret-provider-value" not in report.to_json()


class _StructuredResourceFailure(NullRenderDevice):
    def create_pipeline(self, descriptor: object) -> object:  # type: ignore[override]
        del descriptor
        raise RenderError(
            "provider detail is not report data",
            code="render.provider-secret-value",
            subsystem="render",
            phase="create",
        )


def test_provider_supplied_structured_code_is_not_copied() -> None:
    report = run_render_device_conformance(
        "org.example.structured",
        cast("type[RenderDevice]", _StructuredResourceFailure),
    )

    resource_check = report.checks[_CHECK_IDS.index("resource_handles")]
    assert resource_check.code == "conformance.structured_adapter_error"
    assert "provider-secret-value" not in report.to_json()


class _MalformedStructuredFailure(NullRenderDevice):
    def create_pipeline(self, descriptor: object) -> object:  # type: ignore[override]
        del descriptor
        error = LudoWeaveError(
            "do not disclose",
            code="provider.failure",
            subsystem="provider",
        )
        error.code = cast("str", object())
        raise error


def test_malformed_provider_error_code_is_sanitized() -> None:
    report = run_render_device_conformance(
        "org.example.malformed-error",
        cast("type[RenderDevice]", _MalformedStructuredFailure),
    )

    resource_check = report.checks[_CHECK_IDS.index("resource_handles")]
    assert resource_check.code == "conformance.structured_adapter_error"


class _GamepadSurfaceEventDevice(NullRenderDevice):
    def drain_surface_events(self, handle: object) -> tuple[GamepadConnectionEvent, ...]:
        super().drain_surface_events(handle)  # type: ignore[arg-type]
        return (GamepadConnectionEvent(0, True),)


def test_any_engine_owned_platform_event_is_accepted() -> None:
    report = run_render_device_conformance(
        "org.example.gamepad-surface-event",
        cast("type[RenderDevice]", _GamepadSurfaceEventDevice),
    )
    assert report.passed


class _CloseFailureDevice(NullRenderDevice):
    def close(self) -> None:
        raise RuntimeError("provider close path")


def test_close_failure_is_reported_and_closed_rejection_is_not_claimed() -> None:
    report = run_render_device_conformance("org.example.close-failure", _CloseFailureDevice)

    assert report.checks[-2].code == "conformance.unstructured_exception"
    assert report.checks[-1] == RenderDeviceConformanceCheck(
        "closed_rejection",
        ConformanceStatus.NOT_RUN,
        "conformance.prerequisite_failed",
    )
    assert not report.passed


class _ControlFlowFailureDevice(NullRenderDevice):
    closed = False

    @property
    def capabilities(self) -> RenderCapabilities:
        raise KeyboardInterrupt

    def close(self) -> None:
        self.closed = True
        super().close()


def test_control_flow_failure_is_reraised_after_best_effort_close() -> None:
    device = _ControlFlowFailureDevice()
    with pytest.raises(KeyboardInterrupt):
        run_render_device_conformance("org.example.control-flow", lambda: device)
    assert device.closed


def test_report_and_check_records_are_frozen_slotted_and_validate_invariants() -> None:
    report = run_render_device_conformance("org.ludoweave.null", NullRenderDevice)
    with pytest.raises(FrozenInstanceError):
        report.adapter_id = "org.example.changed"  # type: ignore[misc]
    assert not hasattr(report, "__dict__")
    assert not hasattr(report.checks[0], "__dict__")

    with pytest.raises(RenderError):
        RenderDeviceConformanceCheck("unknown", ConformanceStatus.PASS)
    with pytest.raises(RenderError):
        RenderDeviceConformanceCheck("factory", ConformanceStatus.PASS, "unexpected")
    with pytest.raises(RenderError):
        RenderDeviceConformanceReport(
            "org.example.invalid",
            "invalid",
            ConformanceStatus.PASS,
            report.checks[:-1],
        )
