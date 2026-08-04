"""Structured diagnostic contract tests."""

from ludoweave.core.errors import LifecycleError


def test_structured_error_contains_stable_context() -> None:
    error = LifecycleError(
        "transition rejected",
        code="engine.invalid_transition",
        subsystem="application",
        phase="run",
        details={"state": "created", "operation": "run"},
    )

    assert error.details == (("operation", "run"), ("state", "created"))
    assert error.as_dict() == {
        "code": "engine.invalid_transition",
        "subsystem": "application",
        "phase": "run",
        "message": "transition rejected",
        "details": {"operation": "run", "state": "created"},
    }
    assert "engine.invalid_transition" in str(error)
