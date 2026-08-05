"""Installed agent-tool conformance value, behavior, and failure tests."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from ludoweave.agent import (
    AGENT_TOOL_CONFORMANCE_PROFILE,
    AGENT_TOOL_CONFORMANCE_PROTOCOL,
    AgentCapture,
    AgentCommandService,
    AgentConformanceStatus,
    AgentRequestError,
    AgentToolAdapter,
    AgentToolConformanceCheck,
    AgentToolConformanceReport,
    run_agent_tool_conformance,
)
from ludoweave.samples import create_agent_world_builder
from ludoweave.world import CommandEnvelope, CommandTransaction
from ludoweave.world.canonical import JsonValue

_CHECK_IDS = (
    "factory",
    "service_contract",
    "read_isolation",
    "snapshot_baseline",
    "transaction_validation",
    "transaction_commit",
    "stale_hash_atomicity",
    "entity_query",
    "tick_receipts",
    "snapshot_diff",
    "capture_tests_telemetry",
    "close_lifecycle",
)


class _Capture:
    def __init__(self) -> None:
        self.closed = 0

    def capture(self, width: int, height: int) -> AgentCapture:
        return AgentCapture(width, height, b"\x12\x34\x56\xff" * (width * height))

    def close(self) -> None:
        self.closed += 1


def _service(capture: _Capture | None = None) -> AgentCommandService:
    provider = capture or _Capture()
    return create_agent_world_builder(write=True, capture_provider=provider).service


type _Hook = Callable[
    [str, Mapping[str, object] | None, dict[str, JsonValue]],
    dict[str, JsonValue],
]


class _Proxy:
    def __init__(self, service: AgentCommandService, hook: _Hook | None = None) -> None:
        self.service = service
        self.hook = hook
        self.closed = False

    def call(
        self,
        tool: str,
        arguments: Mapping[str, object] | None = None,
    ) -> dict[str, JsonValue]:
        result = self.service.call(tool, arguments)
        if self.hook is None:
            return result
        return self.hook(tool, arguments, result)

    def close(self) -> None:
        self.closed = True
        self.service.close()


def _factory() -> AgentToolAdapter:
    return _service()


def _check(report: AgentToolConformanceReport, check_id: str) -> AgentToolConformanceCheck:
    return report.checks[_CHECK_IDS.index(check_id)]


def _copy(result: dict[str, JsonValue]) -> dict[str, JsonValue]:
    return deepcopy(result)


def _object(value: JsonValue) -> dict[str, JsonValue]:
    assert isinstance(value, dict)
    return value


def _array(value: JsonValue) -> list[JsonValue]:
    assert isinstance(value, list)
    return value


def _spawn(service: AgentCommandService, transaction_id: str) -> dict[str, object]:
    transaction = CommandTransaction(
        (
            CommandEnvelope(
                command_id=f"{transaction_id}.spawn",
                transaction_id=transaction_id,
                actor=service.actor,
                operation="entity.spawn",
                expected_world_hash=service.session.state_hash,
                arguments={"components": []},
            ),
        ),
        service.session.world_id,
    )
    return {"transaction": transaction.as_dict()}


def test_direct_service_passes_exact_deterministic_profile() -> None:
    first = run_agent_tool_conformance("org.ludoweave.agent-service", _factory)
    second = run_agent_tool_conformance("org.ludoweave.agent-service", _factory)

    assert first == second
    assert first.passed
    assert first.status is AgentConformanceStatus.PASS
    assert tuple(check.check_id for check in first.checks) == _CHECK_IDS
    assert all(check.status is AgentConformanceStatus.PASS for check in first.checks)
    document = first.as_dict()
    assert document["protocol"] == AGENT_TOOL_CONFORMANCE_PROTOCOL
    assert document["profile"] == AGENT_TOOL_CONFORMANCE_PROFILE
    assert document["adapter_id"] == "org.ludoweave.agent-service"
    assert first.to_json().endswith("\n")
    assert "\\" not in first.to_json()


@pytest.mark.parametrize(
    "adapter_id",
    ["", "agent", "Org.LudoWeave.Agent", ".agent", "org..agent", "org/agent", "a." + "b" * 129],
)
def test_invalid_adapter_identity_is_rejected_before_factory_call(adapter_id: str) -> None:
    called = False

    def factory() -> AgentToolAdapter:
        nonlocal called
        called = True
        return _service()

    with pytest.raises(AgentRequestError) as raised:
        run_agent_tool_conformance(adapter_id, factory)

    assert raised.value.code == "agent.conformance_invalid_request"
    assert not called


def test_non_callable_factory_is_rejected() -> None:
    with pytest.raises(AgentRequestError) as raised:
        run_agent_tool_conformance(
            "org.example.invalid",
            cast("object", object()),  # type: ignore[arg-type]
        )
    assert raised.value.code == "agent.conformance_invalid_request"


def test_factory_runs_once_and_invalid_adapter_shape_is_sanitized() -> None:
    calls = 0

    class InvalidShape:
        def __init__(self) -> None:
            self.close_calls = 0

        def close(self) -> None:
            self.close_calls += 1

    invalid = InvalidShape()

    def factory() -> AgentToolAdapter:
        nonlocal calls
        calls += 1
        return cast("AgentToolAdapter", invalid)

    report = run_agent_tool_conformance("org.example.invalid-shape", factory)

    assert calls == 1
    assert invalid.close_calls == 1
    assert _check(report, "factory").code == "agent_conformance.invalid_adapter"
    assert all(check.status is AgentConformanceStatus.NOT_RUN for check in report.checks[1:])


def test_factory_failure_does_not_expose_message_path_or_secret() -> None:
    def factory() -> AgentToolAdapter:
        raise RuntimeError(r"token=private at C:\Users\someone\secret")

    report = run_agent_tool_conformance("org.example.factory-failure", factory)

    assert _check(report, "factory").code == "agent_conformance.unstructured_exception"
    assert "private" not in report.to_json()
    assert "Users" not in report.to_json()


def test_missing_tool_or_capability_fails_the_exact_service_contract_and_closes() -> None:
    proxy = _Proxy(_service())

    def hook(
        tool: str,
        arguments: Mapping[str, object] | None,
        result: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        del arguments
        if tool != "project_describe":
            return result
        changed = _copy(result)
        changed["tools"] = _array(changed["tools"])[:-1]
        capabilities = _object(changed["capabilities"])
        capabilities["capture"] = False
        return changed

    proxy.hook = hook
    report = run_agent_tool_conformance("org.example.contract-mismatch", lambda: proxy)

    assert _check(report, "service_contract").code == ("agent_conformance.invalid_service_contract")
    assert _check(report, "read_isolation").status is AgentConformanceStatus.NOT_RUN
    assert _check(report, "close_lifecycle").status is AgentConformanceStatus.PASS
    assert proxy.closed


def test_non_mapping_and_structured_adapter_failures_are_sanitized() -> None:
    class NonMapping:
        def __init__(self) -> None:
            self.service = _service()

        def call(
            self,
            tool: str,
            arguments: Mapping[str, object] | None = None,
        ) -> dict[str, JsonValue]:
            del tool, arguments
            return cast("dict[str, JsonValue]", object())

        def close(self) -> None:
            self.service.close()

    malformed = run_agent_tool_conformance("org.example.non-mapping", NonMapping)
    assert _check(malformed, "service_contract").code == "agent_conformance.invalid_result"

    class Structured:
        def __init__(self) -> None:
            self.service = _service()

        def call(
            self,
            tool: str,
            arguments: Mapping[str, object] | None = None,
        ) -> dict[str, JsonValue]:
            del tool, arguments
            raise AgentRequestError(
                "provider secret detail",
                code="provider.secret-code",
                subsystem="provider",
            )

        def close(self) -> None:
            self.service.close()

    structured = run_agent_tool_conformance("org.example.structured", Structured)
    assert _check(structured, "service_contract").code == (
        "agent_conformance.structured_adapter_error"
    )
    assert "provider" not in structured.to_json()
    assert "secret-code" not in structured.to_json()


def test_read_mutation_is_detected_after_an_apparently_valid_query() -> None:
    class ReadMutating(_Proxy):
        mutated = False

        def call(
            self,
            tool: str,
            arguments: Mapping[str, object] | None = None,
        ) -> dict[str, JsonValue]:
            result = self.service.call(tool, arguments)
            if tool == "world_query" and not self.mutated:
                self.service.call("transaction_apply", _spawn(self.service, "test.read-mutation"))
                self.mutated = True
            return result

    proxy = ReadMutating(_service())
    report = run_agent_tool_conformance("org.example.read-mutation", lambda: proxy)

    assert _check(report, "read_isolation").code == "agent_conformance.read_mutated_world"
    assert _check(report, "close_lifecycle").status is AgentConformanceStatus.PASS


def test_dry_run_and_commit_receipt_mismatches_are_detected() -> None:
    def dry_hook(
        tool: str,
        arguments: Mapping[str, object] | None,
        result: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        del arguments
        if tool != "transaction_validate":
            return result
        changed = _copy(result)
        _object(changed["receipt"])["status"] = "committed"
        return changed

    dry = run_agent_tool_conformance(
        "org.example.dry-receipt",
        lambda: _Proxy(_service(), dry_hook),
    )
    assert _check(dry, "transaction_validation").code == (
        "agent_conformance.invalid_dry_run_receipt"
    )

    def commit_hook(
        tool: str,
        arguments: Mapping[str, object] | None,
        result: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        del arguments
        if tool != "transaction_apply":
            return result
        changed = _copy(result)
        receipt = _object(changed["receipt"])
        if receipt["transaction_id"] == "conformance.create":
            receipt["post_hash"] = "sha256:" + "0" * 64
        return changed

    committed = run_agent_tool_conformance(
        "org.example.commit-receipt",
        lambda: _Proxy(_service(), commit_hook),
    )
    assert _check(committed, "transaction_commit").code == (
        "agent_conformance.invalid_commit_receipt"
    )


def test_receipt_identity_mismatch_is_detected() -> None:
    def hook(
        tool: str,
        arguments: Mapping[str, object] | None,
        result: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        del arguments
        if tool != "transaction_validate":
            return result
        changed = _copy(result)
        _object(changed["receipt"])["transaction_id"] = "provider.other"
        return changed

    report = run_agent_tool_conformance(
        "org.example.receipt-identity",
        lambda: _Proxy(_service(), hook),
    )
    assert _check(report, "transaction_validation").code == (
        "agent_conformance.invalid_receipt_identity"
    )


def test_stale_hash_rejection_must_leave_world_unchanged() -> None:
    class StaleMutating(_Proxy):
        def call(
            self,
            tool: str,
            arguments: Mapping[str, object] | None = None,
        ) -> dict[str, JsonValue]:
            result = self.service.call(tool, arguments)
            if tool == "transaction_apply":
                receipt = _object(result["receipt"])
                if receipt["transaction_id"] == "conformance.stale":
                    self.service.call(
                        "transaction_apply",
                        _spawn(self.service, "test.stale-mutation"),
                    )
            return result

    report = run_agent_tool_conformance(
        "org.example.stale-mutation",
        lambda: StaleMutating(_service()),
    )

    assert _check(report, "stale_hash_atomicity").code == (
        "agent_conformance.stale_rejection_mutated_world"
    )


@pytest.mark.parametrize(
    ("tool", "check_id", "field", "replacement", "expected_code"),
    [
        (
            "world_tick",
            "tick_receipts",
            "completed",
            1,
            "agent_conformance.invalid_tick_result",
        ),
        (
            "world_diff",
            "snapshot_diff",
            "post_hash",
            "sha256:" + "0" * 64,
            "agent_conformance.invalid_semantic_diff",
        ),
        (
            "render_capture",
            "capture_tests_telemetry",
            "bytes",
            15,
            "agent_conformance.invalid_capture_result",
        ),
    ],
)
def test_late_stage_result_mismatches_fail_with_runner_owned_codes(
    tool: str,
    check_id: str,
    field: str,
    replacement: JsonValue,
    expected_code: str,
) -> None:
    def hook(
        called_tool: str,
        arguments: Mapping[str, object] | None,
        result: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        del arguments
        if called_tool != tool:
            return result
        changed = _copy(result)
        changed[field] = replacement
        return changed

    report = run_agent_tool_conformance(
        f"org.example.{check_id.replace('_', '-')}",
        lambda: _Proxy(_service(), hook),
    )
    assert _check(report, check_id).code == expected_code


def test_close_failure_and_wrong_closed_error_are_not_accepted() -> None:
    class CloseFailure(_Proxy):
        def close(self) -> None:
            self.service.close()
            raise RuntimeError("private close path")

    failed = run_agent_tool_conformance(
        "org.example.close-failure",
        lambda: CloseFailure(_service()),
    )
    assert _check(failed, "close_lifecycle").code == ("agent_conformance.unstructured_exception")
    assert "private" not in failed.to_json()

    class WrongClosedError(_Proxy):
        def call(
            self,
            tool: str,
            arguments: Mapping[str, object] | None = None,
        ) -> dict[str, JsonValue]:
            if self.closed:
                raise AgentRequestError(
                    "provider detail",
                    code="provider.closed",
                    subsystem="provider",
                )
            return super().call(tool, arguments)

    wrong = run_agent_tool_conformance(
        "org.example.wrong-closed",
        lambda: WrongClosedError(_service()),
    )
    assert _check(wrong, "close_lifecycle").code == ("agent_conformance.closed_error_mismatch")


def test_control_flow_failure_is_reraised_after_best_effort_close() -> None:
    class ControlFlow(_Proxy):
        def call(
            self,
            tool: str,
            arguments: Mapping[str, object] | None = None,
        ) -> dict[str, JsonValue]:
            del tool, arguments
            raise KeyboardInterrupt

    proxy = ControlFlow(_service())
    with pytest.raises(KeyboardInterrupt):
        run_agent_tool_conformance("org.example.control-flow", lambda: proxy)
    assert proxy.closed


def test_control_flow_failure_during_close_gets_a_final_cleanup_attempt() -> None:
    class InterruptedClose(_Proxy):
        close_calls = 0

        def close(self) -> None:
            self.close_calls += 1
            if self.close_calls == 1:
                raise KeyboardInterrupt
            super().close()

    proxy = InterruptedClose(_service())
    with pytest.raises(KeyboardInterrupt):
        run_agent_tool_conformance("org.example.interrupted-close", lambda: proxy)
    assert proxy.close_calls == 2
    assert proxy.closed


def test_report_and_check_records_are_frozen_slotted_and_validate_invariants() -> None:
    report = run_agent_tool_conformance("org.ludoweave.agent-service", _factory)
    with pytest.raises(FrozenInstanceError):
        report.adapter_id = "org.example.changed"  # type: ignore[misc]
    assert not hasattr(report, "__dict__")
    assert not hasattr(report.checks[0], "__dict__")

    with pytest.raises(AgentRequestError):
        AgentToolConformanceCheck("unknown", AgentConformanceStatus.PASS)
    with pytest.raises(AgentRequestError):
        AgentToolConformanceCheck(
            "factory",
            AgentConformanceStatus.PASS,
            "agent_conformance.unexpected",
        )
    with pytest.raises(AgentRequestError):
        AgentToolConformanceReport(
            "org.example.invalid",
            AgentConformanceStatus.PASS,
            report.checks[:-1],
        )
