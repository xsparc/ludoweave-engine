"""Installed, transport-neutral conformance evidence for agent-tool adapters."""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping
from contextlib import suppress
from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Protocol, cast

from ludoweave.agent.contracts import AGENT_SERVICE_PROTOCOL
from ludoweave.agent.errors import AgentRequestError
from ludoweave.agent.tools import AGENT_TOOL_NAMES
from ludoweave.core.errors import LudoWeaveError
from ludoweave.core.version import __version__
from ludoweave.world.canonical import JsonValue, validate_json_value

AGENT_TOOL_CONFORMANCE_PROTOCOL: Final = "ludoweave.agent-tool-conformance/1"
AGENT_TOOL_CONFORMANCE_PROFILE: Final = "agent-tool-baseline/1"

_ADAPTER_ID = re.compile(r"[a-z][a-z0-9]*(?:[._-][a-z0-9]+){1,15}\Z")
_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+-]{0,127}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_ERROR_CODE = re.compile(r"agent_conformance\.[a-z0-9_.-]{1,109}\Z")
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


class AgentToolAdapter(Protocol):
    """Minimal engine-owned boundary exercised by the installed profile."""

    def call(
        self,
        tool: str,
        arguments: Mapping[str, object] | None = None,
    ) -> dict[str, JsonValue]: ...

    def close(self) -> None: ...


class AgentConformanceStatus(StrEnum):
    """Stable result states used by installed agent conformance reports."""

    PASS = "pass"
    FAIL = "fail"
    NOT_RUN = "not_run"


@dataclass(frozen=True, slots=True)
class AgentToolConformanceCheck:
    """One deterministic check result without adapter diagnostic text."""

    check_id: str
    status: AgentConformanceStatus
    code: str | None = None

    def __post_init__(self) -> None:
        if type(self.check_id) is not str or self.check_id not in _CHECK_IDS:
            raise _request_error("check_id")
        if type(self.status) is not AgentConformanceStatus:
            raise _request_error("status")
        if self.status is AgentConformanceStatus.PASS:
            if self.code is not None:
                raise _request_error("code")
        elif type(self.code) is not str or _ERROR_CODE.fullmatch(self.code) is None:
            raise _request_error("code")

    def as_dict(self) -> dict[str, object]:
        """Return one JSON-compatible check record."""

        return {"id": self.check_id, "status": self.status.value, "code": self.code}


@dataclass(frozen=True, slots=True)
class AgentToolConformanceReport:
    """Versioned evidence from one explicit agent-tool adapter factory."""

    adapter_id: str
    status: AgentConformanceStatus
    checks: tuple[AgentToolConformanceCheck, ...]

    def __post_init__(self) -> None:
        _validate_adapter_id(self.adapter_id)
        if type(self.status) is not AgentConformanceStatus or (
            self.status is AgentConformanceStatus.NOT_RUN
        ):
            raise _request_error("status")
        try:
            checks = tuple(self.checks)
        except Exception as error:
            raise _request_error("checks") from error
        if (
            len(checks) != len(_CHECK_IDS)
            or any(type(check) is not AgentToolConformanceCheck for check in checks)
            or tuple(check.check_id for check in checks) != _CHECK_IDS
        ):
            raise _request_error("checks")
        expected_status = (
            AgentConformanceStatus.PASS
            if all(check.status is AgentConformanceStatus.PASS for check in checks)
            else AgentConformanceStatus.FAIL
        )
        if self.status is not expected_status:
            raise _request_error("status")
        object.__setattr__(self, "checks", checks)

    @property
    def passed(self) -> bool:
        """Whether every baseline check passed."""

        return self.status is AgentConformanceStatus.PASS

    def as_dict(self) -> dict[str, object]:
        """Return deterministic, path-free, JSON-compatible evidence."""

        return {
            "protocol": AGENT_TOOL_CONFORMANCE_PROTOCOL,
            "profile": AGENT_TOOL_CONFORMANCE_PROFILE,
            "ludoweave_version": __version__,
            "adapter_id": self.adapter_id,
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
    adapter: AgentToolAdapter
    world_id: str | None = None
    actor: dict[str, JsonValue] | None = None
    initial_hash: str | None = None
    current_hash: str | None = None
    initial_snapshot: str | None = None
    proposed_hash: str | None = None
    entity_id: str | None = None


def run_agent_tool_conformance(
    adapter_id: str,
    factory: Callable[[], AgentToolAdapter],
) -> AgentToolConformanceReport:
    """Exercise one trusted, explicitly supplied local agent-tool factory.

    The runner performs no discovery, import, installation, subprocess,
    networking, filesystem access, or global registration. Adapter code runs
    in-process on the calling thread, so the caller remains responsible for
    trust, prerequisites, resource bounds, and isolation.
    """

    checked_id = _validate_adapter_id(adapter_id)
    if not callable(factory):
        raise _request_error("factory")

    checks: list[AgentToolConformanceCheck] = []
    state: _RunState | None = None
    blocked = False
    try:
        adapter = cast(object, factory())
        try:
            valid_shape = callable(getattr(adapter, "call", None)) and callable(
                getattr(adapter, "close", None)
            )
        except BaseException:
            _best_effort_close_object(adapter)
            raise
        if not valid_shape:
            _best_effort_close_object(adapter)
            raise _CheckFailure("agent_conformance.invalid_adapter")
        state = _RunState(cast(AgentToolAdapter, adapter))
    except Exception as error:
        checks.append(_failed("factory", error))
        blocked = True
    else:
        checks.append(_passed("factory"))

    stages: tuple[tuple[str, Callable[[_RunState], None]], ...] = (
        ("service_contract", _check_service_contract),
        ("read_isolation", _check_read_isolation),
        ("snapshot_baseline", _check_snapshot_baseline),
        ("transaction_validation", _check_transaction_validation),
        ("transaction_commit", _check_transaction_commit),
        ("stale_hash_atomicity", _check_stale_hash_atomicity),
        ("entity_query", _check_entity_query),
        ("tick_receipts", _check_tick_receipts),
        ("snapshot_diff", _check_snapshot_diff),
        ("capture_tests_telemetry", _check_capture_tests_telemetry),
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
                state.adapter.close()
        raise

    if state is None:
        checks.append(_not_run("close_lifecycle"))
    else:
        try:
            try:
                _check_close_lifecycle(state)
            except Exception as error:
                checks.append(_failed("close_lifecycle", error))
            else:
                checks.append(_passed("close_lifecycle"))
        except BaseException:
            with suppress(BaseException):
                state.adapter.close()
            raise

    frozen_checks = tuple(checks)
    status = (
        AgentConformanceStatus.PASS
        if all(check.status is AgentConformanceStatus.PASS for check in frozen_checks)
        else AgentConformanceStatus.FAIL
    )
    return AgentToolConformanceReport(checked_id, status, frozen_checks)


def _check_service_contract(state: _RunState) -> None:
    project = _call(state, "project_describe")
    capabilities = _object(_field(project, "capabilities"))
    expected_capabilities = {"read": True, "write": True, "capture": True, "tests": True}
    if (
        _text(_field(project, "protocol")) != "ludoweave.agent.project/1"
        or _text(_field(project, "service_protocol")) != AGENT_SERVICE_PROTOCOL
        or _array(_field(project, "tools")) != list(AGENT_TOOL_NAMES)
        or capabilities != expected_capabilities
    ):
        raise _CheckFailure("agent_conformance.invalid_service_contract")
    world_id = _text(_field(project, "world_id"))
    actor = _object(_field(project, "actor"))
    if _STABLE_ID.fullmatch(world_id) is None or set(actor) != {"kind", "id"}:
        raise _CheckFailure("agent_conformance.invalid_service_identity")
    for field in ("kind", "id"):
        if _STABLE_ID.fullmatch(_text(_field(actor, field))) is None:
            raise _CheckFailure("agent_conformance.invalid_service_identity")
    state.world_id = world_id
    state.actor = actor


def _check_read_isolation(state: _RunState) -> None:
    world = _call(state, "world_describe")
    initial_hash = _hash(_field(world, "state_hash"))
    if (
        _text(_field(world, "protocol")) != "ludoweave.agent.world/1"
        or _text(_field(world, "world_id")) != _required(state.world_id, "world_id")
        or _integer(_field(world, "completed_ticks")) != 0
        or _integer(_field(world, "entity_count")) != 0
    ):
        raise _CheckFailure("agent_conformance.invalid_initial_world")
    query = _call(state, "world_query", {"limit": 8})
    if (
        _text(_field(query, "protocol")) != "ludoweave.agent.query/1"
        or _hash(_field(query, "state_hash")) != initial_hash
        or _integer(_field(query, "matched")) != 0
        or _integer(_field(query, "returned")) != 0
        or _array(_field(query, "entities"))
    ):
        raise _CheckFailure("agent_conformance.read_isolation_mismatch")
    after = _call(state, "world_describe")
    if _hash(_field(after, "state_hash")) != initial_hash:
        raise _CheckFailure("agent_conformance.read_mutated_world")
    state.initial_hash = initial_hash
    state.current_hash = initial_hash


def _check_snapshot_baseline(state: _RunState) -> None:
    snapshot = _call(state, "world_snapshot")
    document = _text(_field(snapshot, "snapshot"))
    _hash(_field(snapshot, "document_sha256"))
    if (
        _text(_field(snapshot, "protocol")) != "ludoweave.agent.snapshot/1"
        or _hash(_field(snapshot, "state_hash")) != _required(state.initial_hash, "initial_hash")
        or _integer(_field(snapshot, "completed_ticks")) != 0
        or _text(_field(snapshot, "encoding")) != "base64"
        or not document
    ):
        raise _CheckFailure("agent_conformance.invalid_snapshot")
    state.initial_snapshot = document


def _check_transaction_validation(state: _RunState) -> None:
    transaction = _spawn_transaction(state, "conformance.create", state.initial_hash)
    result = _call(state, "transaction_validate", {"transaction": transaction})
    receipt = _receipt(result)
    _check_receipt_identity(state, receipt, "conformance.create", "spawn", "dry_run")
    initial_hash = _required(state.initial_hash, "initial_hash")
    proposed_hash = _hash(_field(receipt, "proposed_post_hash"))
    changes = _object(_field(receipt, "changes"))
    created = _array(_field(changes, "created_entities"))
    if (
        _text(_field(receipt, "status")) != "dry_run"
        or _hash(_field(receipt, "pre_hash")) != initial_hash
        or _hash(_field(receipt, "post_hash")) != initial_hash
        or proposed_hash == initial_hash
        or created != ["0:0"]
        or _array(_field(receipt, "diagnostics"))
        or _array(_field(receipt, "aliases")) != [{"alias": "subject", "entity": "0:0"}]
    ):
        raise _CheckFailure("agent_conformance.invalid_dry_run_receipt")
    world = _call(state, "world_describe")
    if _hash(_field(world, "state_hash")) != initial_hash:
        raise _CheckFailure("agent_conformance.dry_run_mutated_world")
    state.proposed_hash = proposed_hash
    state.entity_id = "0:0"


def _check_transaction_commit(state: _RunState) -> None:
    transaction = _spawn_transaction(state, "conformance.create", state.initial_hash)
    result = _call(state, "transaction_apply", {"transaction": transaction})
    receipt = _receipt(result)
    _check_receipt_identity(state, receipt, "conformance.create", "spawn", "committed")
    initial_hash = _required(state.initial_hash, "initial_hash")
    post_hash = _hash(_field(receipt, "post_hash"))
    changes = _object(_field(receipt, "changes"))
    if (
        _text(_field(receipt, "status")) != "committed"
        or _hash(_field(receipt, "pre_hash")) != initial_hash
        or post_hash != _required(state.proposed_hash, "proposed_hash")
        or _array(_field(changes, "created_entities")) != [state.entity_id]
        or _integer(_field(receipt, "completed_ticks_before")) != 0
        or _integer(_field(receipt, "completed_ticks_after")) != 0
        or _array(_field(receipt, "diagnostics"))
        or _array(_field(receipt, "aliases")) != [{"alias": "subject", "entity": state.entity_id}]
    ):
        raise _CheckFailure("agent_conformance.invalid_commit_receipt")
    state.current_hash = post_hash


def _check_stale_hash_atomicity(state: _RunState) -> None:
    current_hash = _required(state.current_hash, "current_hash")
    stale = _spawn_transaction(state, "conformance.stale", state.initial_hash)
    result = _call(state, "transaction_apply", {"transaction": stale})
    receipt = _receipt(result)
    _check_receipt_identity(state, receipt, "conformance.stale", "spawn", "rejected")
    if (
        _text(_field(receipt, "status")) != "rejected"
        or _hash(_field(receipt, "pre_hash")) != current_hash
        or _hash(_field(receipt, "post_hash")) != current_hash
        or _field(receipt, "proposed_post_hash") is not None
        or _field(receipt, "changes") is not None
        or not _array(_field(receipt, "diagnostics"))
        or _array(_field(receipt, "aliases"))
    ):
        raise _CheckFailure("agent_conformance.invalid_stale_rejection")
    world = _call(state, "world_describe")
    if (
        _hash(_field(world, "state_hash")) != current_hash
        or _integer(_field(world, "entity_count")) != 1
    ):
        raise _CheckFailure("agent_conformance.stale_rejection_mutated_world")


def _check_entity_query(state: _RunState) -> None:
    current_hash = _required(state.current_hash, "current_hash")
    entity_id = _required(state.entity_id, "entity_id")
    query = _call(state, "world_query", {"limit": 8})
    entities = _array(_field(query, "entities"))
    if (
        _hash(_field(query, "state_hash")) != current_hash
        or _integer(_field(query, "matched")) != 1
        or _integer(_field(query, "returned")) != 1
        or len(entities) != 1
        or _text(_field(_object(entities[0]), "entity")) != entity_id
    ):
        raise _CheckFailure("agent_conformance.invalid_query_result")
    entity = _call(state, "entity_get", {"entity": entity_id})
    if (
        _text(_field(entity, "protocol")) != "ludoweave.agent.entity/1"
        or _text(_field(entity, "entity")) != entity_id
        or _hash(_field(entity, "state_hash")) != current_hash
        or _array(_field(entity, "components"))
    ):
        raise _CheckFailure("agent_conformance.invalid_entity_result")


def _check_tick_receipts(state: _RunState) -> None:
    before_hash = _required(state.current_hash, "current_hash")
    result = _call(
        state,
        "world_tick",
        {"request_id": "conformance.advance", "count": 2, "expected_world_hash": before_hash},
    )
    receipts = _array(_field(result, "receipts"))
    if (
        _text(_field(result, "protocol")) != "ludoweave.agent.tick/1"
        or _text(_field(result, "status")) != "committed"
        or _integer(_field(result, "requested")) != 2
        or _integer(_field(result, "completed")) != 2
        or _integer(_field(result, "completed_ticks")) != 2
        or len(receipts) != 2
    ):
        raise _CheckFailure("agent_conformance.invalid_tick_result")
    expected_pre = before_hash
    for index, value in enumerate(receipts):
        receipt = _object(value)
        _check_receipt_identity(
            state,
            receipt,
            f"conformance.advance.tick-{index}",
            "advance",
            "committed",
            operation="world.tick",
        )
        post_hash = _hash(_field(receipt, "post_hash"))
        if (
            _text(_field(receipt, "protocol")) != "ludoweave.receipt/1"
            or _text(_field(receipt, "status")) != "committed"
            or _hash(_field(receipt, "pre_hash")) != expected_pre
            or _integer(_field(receipt, "completed_ticks_before")) != index
            or _integer(_field(receipt, "completed_ticks_after")) != index + 1
        ):
            raise _CheckFailure("agent_conformance.invalid_tick_receipt")
        expected_pre = post_hash
    result_hash = _hash(_field(result, "state_hash"))
    if result_hash != expected_pre:
        raise _CheckFailure("agent_conformance.tick_hash_mismatch")
    state.current_hash = result_hash


def _check_snapshot_diff(state: _RunState) -> None:
    current_hash = _required(state.current_hash, "current_hash")
    snapshot = _call(state, "world_snapshot")
    if (
        _hash(_field(snapshot, "state_hash")) != current_hash
        or _integer(_field(snapshot, "completed_ticks")) != 2
    ):
        raise _CheckFailure("agent_conformance.invalid_final_snapshot")
    diff = _call(
        state,
        "world_diff",
        {"before_snapshot": _required(state.initial_snapshot, "initial_snapshot")},
    )
    changes = _object(_field(diff, "changes"))
    if (
        _text(_field(diff, "protocol")) != "ludoweave.agent.diff/1"
        or _hash(_field(diff, "pre_hash")) != _required(state.initial_hash, "initial_hash")
        or _hash(_field(diff, "post_hash")) != current_hash
        or _array(_field(changes, "created_entities")) != [state.entity_id]
        or _integer(_field(changes, "completed_ticks_before")) != 0
        or _integer(_field(changes, "completed_ticks_after")) != 2
    ):
        raise _CheckFailure("agent_conformance.invalid_semantic_diff")


def _check_capture_tests_telemetry(state: _RunState) -> None:
    current_hash = _required(state.current_hash, "current_hash")
    capture = _call(
        state,
        "render_capture",
        {"width": 2, "height": 2, "include_pixels": False},
    )
    _hash(_field(capture, "pixel_sha256"))
    if (
        _text(_field(capture, "protocol")) != "ludoweave.agent.capture/1"
        or _integer(_field(capture, "width")) != 2
        or _integer(_field(capture, "height")) != 2
        or _integer(_field(capture, "bytes")) != 16
        or _field(capture, "pixels") is not None
        or _field(capture, "encoding") is not None
        or _hash(_field(capture, "state_hash")) != current_hash
    ):
        raise _CheckFailure("agent_conformance.invalid_capture_result")
    tests = _call(state, "test_run")
    if (
        _text(_field(tests, "protocol")) != "ludoweave.agent.tests/1"
        or type(_field(tests, "passed")) is not bool
        or not _array(_field(tests, "results"))
        or _hash(_field(tests, "state_hash")) != current_hash
    ):
        raise _CheckFailure("agent_conformance.invalid_test_result")
    telemetry = _call(state, "telemetry_get")
    service = _object(_field(telemetry, "service"))
    if (
        _text(_field(telemetry, "protocol")) != "ludoweave.agent.telemetry/1"
        or _hash(_field(telemetry, "state_hash")) != current_hash
        or _integer(_field(telemetry, "completed_ticks")) != 2
        or _integer(_field(service, "calls")) <= 0
    ):
        raise _CheckFailure("agent_conformance.invalid_telemetry_result")
    world = _call(state, "world_describe")
    if _hash(_field(world, "state_hash")) != current_hash:
        raise _CheckFailure("agent_conformance.observation_mutated_world")


def _check_close_lifecycle(state: _RunState) -> None:
    state.adapter.close()
    state.adapter.close()
    try:
        state.adapter.call("world_describe")
    except LudoWeaveError as error:
        if error.code != "agent.closed":
            raise _CheckFailure("agent_conformance.closed_error_mismatch") from error
    else:
        raise _CheckFailure("agent_conformance.expected_closed_error")


def _best_effort_close_object(adapter: object) -> None:
    with suppress(BaseException):
        close = getattr(adapter, "close", None)
        if callable(close):
            close()


def _check_receipt_identity(
    state: _RunState,
    receipt: dict[str, JsonValue],
    transaction_id: str,
    command_suffix: str,
    status: str,
    *,
    operation: str = "entity.spawn",
) -> None:
    outcomes = _array(_field(receipt, "command_outcomes"))
    if (
        _text(_field(receipt, "world_id")) != _required(state.world_id, "world_id")
        or _text(_field(receipt, "transaction_id")) != transaction_id
        or _object(_field(receipt, "actor")) != _required(state.actor, "actor")
        or len(outcomes) != 1
    ):
        raise _CheckFailure("agent_conformance.invalid_receipt_identity")
    outcome = _object(outcomes[0])
    if (
        _text(_field(outcome, "command_id")) != f"{transaction_id}.{command_suffix}"
        or _text(_field(outcome, "operation")) != operation
        or _text(_field(outcome, "status")) != status
    ):
        raise _CheckFailure("agent_conformance.invalid_receipt_identity")


def _spawn_transaction(
    state: _RunState,
    transaction_id: str,
    expected_hash: str | None,
) -> dict[str, object]:
    if expected_hash is None:
        raise _CheckFailure("agent_conformance.missing_expected_hash")
    return {
        "protocol": "ludoweave.transaction/1",
        "world_id": _required(state.world_id, "world_id"),
        "dry_run": False,
        "commands": [
            {
                "protocol": "ludoweave.command/1",
                "command_id": f"{transaction_id}.spawn",
                "transaction_id": transaction_id,
                "actor": _required(state.actor, "actor"),
                "operation": "entity.spawn",
                "operation_version": 1,
                "expected_world_hash": expected_hash,
                "arguments": {"alias": "subject", "components": []},
            }
        ],
    }


def _call(
    state: _RunState,
    tool: str,
    arguments: Mapping[str, object] | None = None,
) -> dict[str, JsonValue]:
    result = cast(object, state.adapter.call(tool, arguments))
    if not isinstance(result, Mapping):
        raise _CheckFailure("agent_conformance.invalid_result")
    checked = validate_json_value(cast(Mapping[object, object], result))
    if not isinstance(checked, dict):
        raise _CheckFailure("agent_conformance.invalid_result")
    return cast(dict[str, JsonValue], checked)


def _receipt(result: dict[str, JsonValue]) -> dict[str, JsonValue]:
    if _text(_field(result, "protocol")) != "ludoweave.agent.transaction/1":
        raise _CheckFailure("agent_conformance.invalid_transaction_result")
    receipt = _object(_field(result, "receipt"))
    if _text(_field(receipt, "protocol")) != "ludoweave.receipt/1":
        raise _CheckFailure("agent_conformance.invalid_receipt_protocol")
    return receipt


def _field(value: dict[str, JsonValue], field: str) -> JsonValue:
    if field not in value:
        raise _CheckFailure("agent_conformance.missing_result_field")
    return value[field]


def _object(value: JsonValue) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise _CheckFailure("agent_conformance.invalid_result_type")
    return value


def _array(value: JsonValue) -> list[JsonValue]:
    if not isinstance(value, list):
        raise _CheckFailure("agent_conformance.invalid_result_type")
    return value


def _text(value: JsonValue) -> str:
    if type(value) is not str:
        raise _CheckFailure("agent_conformance.invalid_result_type")
    return value


def _integer(value: JsonValue) -> int:
    if type(value) is not int:
        raise _CheckFailure("agent_conformance.invalid_result_type")
    return value


def _hash(value: JsonValue) -> str:
    text = _text(value)
    if _SHA256.fullmatch(text) is None:
        raise _CheckFailure("agent_conformance.invalid_hash")
    return text


def _required[ValueT](value: ValueT | None, field: str) -> ValueT:
    if value is None:
        raise _CheckFailure(f"agent_conformance.missing_{field}")
    return value


def _passed(check_id: str) -> AgentToolConformanceCheck:
    return AgentToolConformanceCheck(check_id, AgentConformanceStatus.PASS)


def _not_run(check_id: str) -> AgentToolConformanceCheck:
    return AgentToolConformanceCheck(
        check_id,
        AgentConformanceStatus.NOT_RUN,
        "agent_conformance.prerequisite_failed",
    )


def _failed(check_id: str, error: Exception) -> AgentToolConformanceCheck:
    if type(error) is _CheckFailure:
        code = error.code
    elif isinstance(error, LudoWeaveError):
        code = "agent_conformance.structured_adapter_error"
    else:
        code = "agent_conformance.unstructured_exception"
    return AgentToolConformanceCheck(check_id, AgentConformanceStatus.FAIL, code)


def _validate_adapter_id(value: object) -> str:
    if type(value) is not str or len(value) > 128 or _ADAPTER_ID.fullmatch(value) is None:
        raise _request_error("adapter_id")
    return value


def _request_error(field: str) -> AgentRequestError:
    return AgentRequestError(
        "agent-tool conformance request is invalid",
        code="agent.conformance_invalid_request",
        subsystem="agent",
        phase="conformance",
        details={"field": field},
    )
