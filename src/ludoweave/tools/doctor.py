"""Structured, non-mutating local environment diagnostics."""

import platform
import sys

from ludoweave import Engine, EngineConfig, LifecycleState, __version__
from ludoweave.app import RunSummary
from ludoweave.core.clock import MonotonicClock, VirtualClock
from ludoweave.render import NullRenderBackend, RenderDescriptor


def _check_record(
    name: str, *, status: str, details: dict[str, object] | None = None
) -> dict[str, object]:
    return {"name": name, "status": status, "details": details or {}}


def run_doctor() -> tuple[dict[str, object], int]:
    """Run bounded M0 checks and return a JSON-compatible report and exit code."""

    checks: list[dict[str, object]] = []

    version_info = sys.version_info
    python_supported = sys.implementation.name == "cpython" and (3, 12) <= version_info[:2] < (
        3,
        15,
    )
    checks.append(
        _check_record(
            "python",
            status="ok" if python_supported else "error",
            details={
                "implementation": sys.implementation.name,
                "version": platform.python_version(),
            },
        )
    )

    try:
        clock = MonotonicClock()
        first_ns = clock.now_ns()
        second_ns = clock.now_ns()
        monotonic = second_ns >= first_ns
        checks.append(_check_record("monotonic_clock", status="ok" if monotonic else "error"))
    except Exception as error:
        checks.append(
            _check_record(
                "monotonic_clock",
                status="error",
                details={"error_type": type(error).__name__},
            )
        )

    backend = NullRenderBackend()
    engine = Engine(
        EngineConfig(),
        backend,
        clock=VirtualClock(),
        descriptor=RenderDescriptor(label="doctor"),
    )
    summary: RunSummary | None = None
    try:
        with engine:
            summary = engine.run(ticks=1)
        assert summary is not None
        null_ok = (
            summary.ticks == 1
            and backend.frame_count == 1
            and engine.state is LifecycleState.CLOSED
        )
        checks.append(
            _check_record(
                "null_renderer",
                status="ok" if null_ok else "error",
                details={"frames": backend.frame_count},
            )
        )
    except Exception as error:
        checks.append(
            _check_record(
                "null_renderer",
                status="error",
                details={"error_type": type(error).__name__},
            )
        )

    ok = all(check["status"] == "ok" for check in checks)
    report: dict[str, object] = {
        "schema": "ludoweave.doctor/1",
        "status": "ok" if ok else "error",
        "ludoweave_version": __version__,
        "platform": platform.system(),
        "checks": checks,
    }
    return report, 0 if ok else 1
