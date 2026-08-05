# pyright: reportPrivateUsage=false
"""Transport-independent typed command/query service for agent-operable worlds."""

from __future__ import annotations

import re
import threading
from base64 import b64decode, b64encode
from binascii import Error as Base64Error
from collections import deque
from collections.abc import Mapping
from hashlib import sha256
from typing import cast
from uuid import UUID

from ludoweave.agent.contracts import (
    AGENT_SERVICE_PROTOCOL,
    AgentCapabilities,
    AgentCapture,
    AgentCaptureProvider,
    AgentLimits,
    AgentProject,
    AgentTelemetryProvider,
    AgentTestProvider,
    AgentTestResult,
    validated_telemetry,
)
from ludoweave.agent.errors import (
    AgentCapabilityError,
    AgentConcurrencyError,
    AgentLimitError,
    AgentProviderError,
    AgentRequestError,
)
from ludoweave.agent.tools import AGENT_TOOL_NAMES, tool_for_name
from ludoweave.core.clock import Clock, MonotonicClock
from ludoweave.core.errors import LudoWeaveError
from ludoweave.core.version import __version__
from ludoweave.world import (
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    ReceiptStatus,
    ReplayRecorder,
    SnapshotCodec,
    TransactionLimits,
    TransactionReceipt,
    TransactionService,
    WorldSession,
    canonical_dumps,
    semantic_diff,
)
from ludoweave.world.canonical import JsonValue, validate_json_value

_ENTITY_ID = re.compile(r"(0|[1-9][0-9]*):(0|[1-9][0-9]*)\Z")
_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+-]{0,127}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_REDACTED = "[redacted]"
_SENSITIVE_KEY_PARTS = (
    "api_key",
    "apikey",
    "authorization",
    "cookie",
    "credential",
    "environment",
    "password",
    "private_key",
    "secret",
    "token",
)


class AgentCommandService:
    """Single-owner command/query service shared by direct, CLI, and MCP paths.

    The service owns an injected capture provider after construction and closes
    it exactly once. World reads are detached snapshots. Mutations are accepted
    only with explicit write capability and pass through the existing atomic
    transaction service and replay recorder at one non-reentrant safe point.
    """

    __slots__ = (
        "_actor",
        "_capabilities",
        "_capture_provider",
        "_clock",
        "_closed",
        "_counters",
        "_limits",
        "_mutation_gate",
        "_owner_thread",
        "_project",
        "_rate_samples",
        "_recorder",
        "_session",
        "_snapshot_codec",
        "_telemetry_provider",
        "_test_provider",
        "_validator",
    )

    def __init__(
        self,
        session: WorldSession,
        snapshot_codec: SnapshotCodec,
        project: AgentProject,
        actor: CommandActor,
        *,
        capabilities: AgentCapabilities | None = None,
        limits: AgentLimits | None = None,
        clock: Clock | None = None,
        capture_provider: AgentCaptureProvider | None = None,
        test_provider: AgentTestProvider | None = None,
        telemetry_provider: AgentTelemetryProvider | None = None,
        timeline_id: str = "agent-session",
    ) -> None:
        checked_capabilities = capabilities or AgentCapabilities()
        checked_limits = limits or AgentLimits()
        if checked_capabilities.capture != (capture_provider is not None):
            raise _request_error(
                "capture capability must exactly match the injected provider",
                code="agent.capability_provider_mismatch",
                phase="configure",
                details={"capability": "capture"},
            )
        if checked_capabilities.tests != (test_provider is not None):
            raise _request_error(
                "test capability must exactly match the injected provider",
                code="agent.capability_provider_mismatch",
                phase="configure",
                details={"capability": "tests"},
            )
        if type(timeline_id) is not str or _STABLE_ID.fullmatch(timeline_id) is None:
            raise _request_error(
                "agent timeline ID must use bounded stable text",
                code="agent.invalid_timeline",
                phase="configure",
                details={"field": "timeline_id"},
            )
        transaction_limits = TransactionLimits(
            max_bytes=checked_limits.max_transaction_bytes,
            max_commands=checked_limits.max_transaction_commands,
            max_ticks=checked_limits.max_ticks_per_request,
            max_aliases=checked_limits.max_transaction_commands,
            max_diff_records=max(checked_limits.max_query_entities * 16, 1_024),
            max_receipt_bytes=min(
                checked_limits.max_result_bytes,
                checked_limits.max_transaction_bytes,
            ),
        )
        self._session = session
        self._snapshot_codec = snapshot_codec
        self._project = project
        self._actor = actor
        self._capabilities = checked_capabilities
        self._limits = checked_limits
        self._clock = clock or MonotonicClock()
        self._capture_provider = capture_provider
        self._test_provider = test_provider
        self._telemetry_provider = telemetry_provider
        self._validator = TransactionService(session, limits=transaction_limits)
        self._recorder = ReplayRecorder(
            session,
            snapshot_codec,
            timeline_id=timeline_id,
            project_schema=project.project_schema,
            dependency_lock_hash=project.dependency_lock_hash,
            platform_profile=project.platform_profile,
            transaction_limits=transaction_limits,
        )
        self._mutation_gate = threading.Lock()
        self._owner_thread = threading.get_ident()
        self._rate_samples: deque[int] = deque()
        self._closed = False
        self._counters = {
            "calls": 0,
            "errors": 0,
            "transaction_dry_runs": 0,
            "transactions_committed": 0,
            "transactions_rejected": 0,
            "ticks_committed": 0,
            "captures": 0,
            "test_runs": 0,
        }

    @property
    def session(self) -> WorldSession:
        self._assert_owner("inspect")
        self._guard_open("inspect")
        return self._session

    @property
    def capabilities(self) -> AgentCapabilities:
        return self._capabilities

    @property
    def limits(self) -> AgentLimits:
        return self._limits

    @property
    def actor(self) -> CommandActor:
        return self._actor

    def __enter__(self) -> AgentCommandService:
        self._assert_owner("enter")
        self._guard_open("enter")
        return self

    def __exit__(self, *_exception: object) -> bool:
        self.close()
        return False

    def close(self) -> None:
        """Close the owned capture provider once; session state remains inspectable elsewhere."""

        self._assert_owner("close")
        if self._closed:
            return
        self._closed = True
        provider = self._capture_provider
        if provider is None:
            return
        try:
            provider.close()
        except Exception as error:
            raise _provider_error(
                "agent capture provider failed during close",
                phase="close",
                provider="capture",
                cause=error,
            ) from error

    def call(
        self,
        tool: str,
        arguments: Mapping[str, object] | None = None,
    ) -> dict[str, JsonValue]:
        """Invoke one typed tool and return a bounded transport-neutral object."""

        self._assert_owner("call")
        self._guard_open("call")
        if type(tool) is not str or tool_for_name(tool) is None:
            raise _request_error(
                "agent tool is not registered",
                code="agent.unknown_tool",
                phase="dispatch",
                details={"tool": tool if type(tool) is str else type(tool).__name__},
            )
        checked_arguments = _arguments(arguments)
        request_document: dict[str, JsonValue] = {
            "tool": tool,
            "arguments": checked_arguments,
        }
        request_size = len(canonical_dumps(request_document))
        if request_size > self._limits.max_request_bytes:
            raise _limit_error("request_bytes", request_size, self._limits.max_request_bytes)
        self._enforce_rate_limit()
        self._counters["calls"] += 1
        try:
            result = self._dispatch(tool, checked_arguments)
            redacted = cast(dict[str, JsonValue], _redact(result))
            result_size = len(canonical_dumps(redacted))
            if result_size > self._limits.max_result_bytes:
                raise _limit_error("result_bytes", result_size, self._limits.max_result_bytes)
        except LudoWeaveError:
            self._counters["errors"] += 1
            raise
        return redacted

    def replay_bytes(self) -> bytes:
        """Return the current immutable replay timeline for local artifact adapters."""

        self._assert_owner("replay")
        self._guard_open("replay")
        return self._recorder.timeline().canonical_bytes()

    def _dispatch(self, tool: str, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        if tool == "project_describe":
            return self._project_describe(arguments)
        if tool == "world_describe":
            return self._world_describe(arguments)
        if tool == "world_query":
            return self._world_query(arguments)
        if tool == "entity_get":
            return self._entity_get(arguments)
        if tool == "transaction_validate":
            return self._transaction_validate(arguments)
        if tool == "transaction_apply":
            return self._transaction_apply(arguments)
        if tool == "world_tick":
            return self._world_tick(arguments)
        if tool == "world_snapshot":
            return self._world_snapshot(arguments)
        if tool == "world_diff":
            return self._world_diff(arguments)
        if tool == "render_capture":
            return self._render_capture(arguments)
        if tool == "telemetry_get":
            return self._telemetry_get(arguments)
        if tool == "test_run":
            return self._test_run(arguments)
        raise AssertionError(f"registered agent tool {tool!r} has no handler")

    def _project_describe(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(arguments, required=set(), optional=set(), tool="project_describe")
        component_schemas: list[JsonValue] = []
        for schema in self._session.component_registry.schemas:
            component_schemas.append(
                {
                    "type_id": str(schema.type_id),
                    "qualified_name": schema.qualified_name,
                    "version": schema.version,
                    "authoritative": schema.authoritative,
                    "determinism": schema.determinism.value,
                    "fields": [
                        {
                            "name": field.name,
                            "type": field.value_type.value,
                            "optional": field.allow_none,
                        }
                        for field in schema.fields
                    ],
                }
            )
        resource_schemas: list[JsonValue] = [
            {
                "type_id": str(schema.type_id),
                "resource": schema.spec.name,
                "version": schema.version,
                "role": schema.role.value,
                "codec": schema.codec_id,
            }
            for schema in self._session.authority_resources.schemas
        ]
        return {
            "protocol": "ludoweave.agent.project/1",
            "service_protocol": AGENT_SERVICE_PROTOCOL,
            "engine_version": __version__,
            "project": self._project.as_dict(),
            "world_id": self._session.world_id,
            "actor": cast(dict[str, JsonValue], self._actor.as_dict()),
            "capabilities": self._capabilities.as_dict(),
            "limits": self._limits.as_dict(),
            "tools": list(AGENT_TOOL_NAMES),
            "component_schemas": component_schemas,
            "resource_schemas": resource_schemas,
        }

    def _world_describe(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(arguments, required=set(), optional=set(), tool="world_describe")
        document = self._session.authority_document()
        allocator = _object(document["allocator"])
        alive = _array(allocator["alive"])
        component_tables = _array(document["components"])
        resources = _array(document["resources"])
        by_component: list[JsonValue] = []
        component_count = 0
        for value in component_tables:
            table = _object(value)
            rows = _array(table["rows"])
            component_count += len(rows)
            by_component.append({"type_id": _text(table["type_id"]), "count": len(rows)})
        return {
            "protocol": "ludoweave.agent.world/1",
            "world_id": self._session.world_id,
            "completed_ticks": self._session.completed_ticks,
            "state_hash": self._session.state_hash,
            "entity_count": sum(value is True for value in alive),
            "component_count": component_count,
            "components": by_component,
            "state_resource_count": sum(_object(value)["present"] is True for value in resources),
        }

    def _world_query(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(
            arguments,
            required=set(),
            optional={"exclude", "include", "limit"},
            tool="world_query",
        )
        included = _component_ids(arguments.get("include", []), self._session, field="include")
        excluded = _component_ids(arguments.get("exclude", []), self._session, field="exclude")
        if included & excluded:
            raise _request_error(
                "world query include and exclude component sets must be disjoint",
                code="agent.invalid_query",
                phase="query",
                details={"field": "include_exclude"},
            )
        limit = _positive_int(
            arguments.get("limit", self._limits.max_query_entities),
            field="limit",
            tool="world_query",
        )
        if limit > self._limits.max_query_entities:
            raise _limit_error("query_entities", limit, self._limits.max_query_entities)
        entities = _authority_entities(self._session.authority_document())
        matches: list[JsonValue] = []
        matched = 0
        for entity, components in entities:
            available = {_text(_object(component)["type_id"]) for component in components}
            if not included <= available or excluded & available:
                continue
            matched += 1
            if len(matches) < limit:
                matches.append({"entity": entity, "components": components})
        return {
            "protocol": "ludoweave.agent.query/1",
            "world_id": self._session.world_id,
            "state_hash": self._session.state_hash,
            "matched": matched,
            "returned": len(matches),
            "truncated": matched > len(matches),
            "entities": matches,
        }

    def _entity_get(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(arguments, required={"entity"}, optional=set(), tool="entity_get")
        entity = _entity_id(arguments["entity"])
        for current, components in _authority_entities(self._session.authority_document()):
            if current == entity:
                return {
                    "protocol": "ludoweave.agent.entity/1",
                    "world_id": self._session.world_id,
                    "state_hash": self._session.state_hash,
                    "entity": current,
                    "components": components,
                }
        raise _request_error(
            "entity is not live in the current authoritative world",
            code="agent.entity_not_found",
            phase="query",
            details={"entity": entity},
        )

    def _transaction_validate(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        transaction = self._transaction(arguments, tool="transaction_validate")
        receipt = self._validator.validate(transaction)
        self._counters["transaction_dry_runs"] += 1
        if receipt.status is ReceiptStatus.REJECTED:
            self._counters["transactions_rejected"] += 1
        return _receipt_result(receipt)

    def _transaction_apply(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        self._require_write("transaction_apply")
        transaction = self._transaction(arguments, tool="transaction_apply")
        if transaction.dry_run:
            raise _request_error(
                "transaction_apply requires dry_run to be false",
                code="agent.invalid_transaction",
                phase="validate",
                details={"field": "dry_run"},
            )
        self._enter_mutation("transaction_apply")
        try:
            receipt = self._recorder.record(transaction)
        finally:
            self._leave_mutation()
        self._record_receipt(receipt)
        return _receipt_result(receipt)

    def _world_tick(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        self._require_write("world_tick")
        _exact_fields(
            arguments,
            required={"count", "request_id"},
            optional={"expected_world_hash"},
            tool="world_tick",
        )
        request_id = _stable_id(arguments["request_id"], field="request_id", tool="world_tick")
        count = _positive_int(arguments["count"], field="count", tool="world_tick")
        if count > self._limits.max_ticks_per_request:
            raise _limit_error("ticks", count, self._limits.max_ticks_per_request)
        expected_value = arguments.get("expected_world_hash")
        if expected_value is not None and (
            type(expected_value) is not str or _SHA256.fullmatch(expected_value) is None
        ):
            raise _request_error(
                "world_tick expected hash must be a SHA-256 identifier or null",
                code="agent.invalid_request",
                phase="validate",
                details={"field": "expected_world_hash"},
            )
        receipts: list[JsonValue] = []
        with _MutationLease(self, "world_tick"):
            for index in range(count):
                transaction_id = f"{request_id}.tick-{self._session.completed_ticks}"
                expected = expected_value if index == 0 and expected_value is not None else None
                transaction = CommandTransaction(
                    (
                        CommandEnvelope(
                            command_id=f"{transaction_id}.advance",
                            transaction_id=transaction_id,
                            actor=self._actor,
                            operation="world.tick",
                            arguments={"count": 1},
                            expected_world_hash=expected,
                        ),
                    ),
                    self._session.world_id,
                )
                receipt = self._recorder.record(transaction)
                receipts.append(receipt.as_dict())
                self._record_receipt(receipt)
                if receipt.status is not ReceiptStatus.COMMITTED:
                    break
                self._counters["ticks_committed"] += 1
        completed = sum(
            _object(receipt)["status"] == ReceiptStatus.COMMITTED.value for receipt in receipts
        )
        status = "committed" if completed == count else "rejected"
        return {
            "protocol": "ludoweave.agent.tick/1",
            "status": status,
            "requested": count,
            "completed": completed,
            "completed_ticks": self._session.completed_ticks,
            "state_hash": self._session.state_hash,
            "receipts": receipts,
        }

    def _world_snapshot(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(arguments, required=set(), optional=set(), tool="world_snapshot")
        document = self._snapshot_codec.encode(self._session)
        if len(document) > self._limits.max_snapshot_bytes:
            raise _limit_error("snapshot_bytes", len(document), self._limits.max_snapshot_bytes)
        return {
            "protocol": "ludoweave.agent.snapshot/1",
            "world_id": self._session.world_id,
            "completed_ticks": self._session.completed_ticks,
            "state_hash": self._session.state_hash,
            "document_sha256": f"sha256:{sha256(document).hexdigest()}",
            "bytes": len(document),
            "encoding": "base64",
            "snapshot": b64encode(document).decode("ascii"),
        }

    def _world_diff(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(
            arguments,
            required={"before_snapshot"},
            optional={"after_snapshot"},
            tool="world_diff",
        )
        before = self._decode_snapshot(arguments["before_snapshot"], field="before_snapshot")
        after_value = arguments.get("after_snapshot")
        after = (
            self._session
            if after_value is None
            else self._decode_snapshot(after_value, field="after_snapshot")
        )
        if before.world_id != after.world_id:
            raise _request_error(
                "world diff snapshots must name the same world",
                code="agent.snapshot_mismatch",
                phase="diff",
                details={"field": "world_id"},
            )
        changes = semantic_diff(before.authority_document(), after.authority_document())
        return {
            "protocol": "ludoweave.agent.diff/1",
            "world_id": before.world_id,
            "pre_hash": before.state_hash,
            "post_hash": after.state_hash,
            "changes": changes.as_dict(),
        }

    def _render_capture(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(
            arguments,
            required={"height", "width"},
            optional={"include_pixels"},
            tool="render_capture",
        )
        if not self._capabilities.capture or self._capture_provider is None:
            raise _capability_error("capture", "render_capture")
        width = _positive_int(arguments["width"], field="width", tool="render_capture")
        height = _positive_int(arguments["height"], field="height", tool="render_capture")
        pixels = width * height
        if pixels > self._limits.max_capture_pixels:
            raise _limit_error("capture_pixels", pixels, self._limits.max_capture_pixels)
        include_pixels = arguments.get("include_pixels", True)
        if type(include_pixels) is not bool:
            raise _request_error(
                "render_capture include_pixels must be an exact boolean",
                code="agent.invalid_request",
                phase="validate",
                details={"field": "include_pixels"},
            )
        try:
            capture = self._capture_provider.capture(width, height)
        except Exception as error:
            raise _provider_error(
                "agent capture provider failed",
                phase="capture",
                provider="capture",
                cause=error,
            ) from error
        if type(capture) is not AgentCapture or (capture.width, capture.height) != (width, height):
            raise _provider_error(
                "agent capture provider returned an incompatible frame",
                phase="capture",
                provider="capture",
                cause=None,
            )
        self._counters["captures"] += 1
        result: dict[str, JsonValue] = {
            "protocol": "ludoweave.agent.capture/1",
            "width": width,
            "height": height,
            "format": "rgba8-unorm",
            "bytes": len(capture.pixels),
            "pixel_sha256": f"sha256:{sha256(capture.pixels).hexdigest()}",
            "state_hash": self._session.state_hash,
            "completed_ticks": self._session.completed_ticks,
            "encoding": "base64" if include_pixels else None,
            "pixels": b64encode(capture.pixels).decode("ascii") if include_pixels else None,
        }
        return result

    def _telemetry_get(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(arguments, required=set(), optional=set(), tool="telemetry_get")
        application: dict[str, JsonValue] = {}
        if self._telemetry_provider is not None:
            try:
                application = validated_telemetry(self._telemetry_provider.telemetry())
            except Exception as error:
                raise _provider_error(
                    "agent telemetry provider failed",
                    phase="telemetry",
                    provider="telemetry",
                    cause=error,
                ) from error
        return {
            "protocol": "ludoweave.agent.telemetry/1",
            "world_id": self._session.world_id,
            "completed_ticks": self._session.completed_ticks,
            "state_hash": self._session.state_hash,
            "service": {name: value for name, value in sorted(self._counters.items())},
            "replay_batches": len(self._recorder.timeline().batches),
            "application": application,
        }

    def _test_run(self, arguments: dict[str, JsonValue]) -> dict[str, JsonValue]:
        _exact_fields(arguments, required=set(), optional={"tests"}, tool="test_run")
        if not self._capabilities.tests or self._test_provider is None:
            raise _capability_error("tests", "test_run")
        try:
            available = self._test_provider.test_names()
        except Exception as error:
            raise _provider_error(
                "agent test provider could not enumerate tests",
                phase="test",
                provider="tests",
                cause=error,
            ) from error
        if len(available) > self._limits.max_test_names or any(
            type(name) is not str or _STABLE_ID.fullmatch(name) is None for name in available
        ):
            raise _provider_error(
                "agent test provider exposed an invalid allowlist",
                phase="test",
                provider="tests",
                cause=None,
            )
        selected = _test_names(arguments.get("tests", list(available)))
        if len(selected) > self._limits.max_test_names:
            raise _limit_error("test_names", len(selected), self._limits.max_test_names)
        unknown = tuple(sorted(set(selected) - set(available)))
        if unknown:
            raise _request_error(
                "test_run requested a name outside the registered allowlist",
                code="agent.unknown_test",
                phase="test",
                details={"tests": ",".join(unknown)},
            )
        try:
            results = self._test_provider.run_tests(selected)
        except Exception as error:
            raise _provider_error(
                "agent test provider failed",
                phase="test",
                provider="tests",
                cause=error,
            ) from error
        if (
            any(type(result) is not AgentTestResult for result in results)
            or tuple(result.name for result in results) != selected
        ):
            raise _provider_error(
                "agent test provider returned results outside the requested allowlist",
                phase="test",
                provider="tests",
                cause=None,
            )
        self._counters["test_runs"] += 1
        return {
            "protocol": "ludoweave.agent.tests/1",
            "passed": all(result.passed for result in results),
            "results": [result.as_dict() for result in results],
            "state_hash": self._session.state_hash,
            "completed_ticks": self._session.completed_ticks,
        }

    def _transaction(
        self,
        arguments: dict[str, JsonValue],
        *,
        tool: str,
    ) -> CommandTransaction:
        _exact_fields(arguments, required={"transaction"}, optional=set(), tool=tool)
        transaction = CommandTransaction.from_mapping(arguments["transaction"])
        size = len(transaction.canonical_bytes())
        if size > self._limits.max_transaction_bytes:
            raise _limit_error("transaction_bytes", size, self._limits.max_transaction_bytes)
        if len(transaction.commands) > self._limits.max_transaction_commands:
            raise _limit_error(
                "transaction_commands",
                len(transaction.commands),
                self._limits.max_transaction_commands,
            )
        if transaction.world_id != self._session.world_id:
            raise _request_error(
                "agent transaction targets a different world",
                code="agent.world_mismatch",
                phase="validate",
                details={"field": "world_id"},
            )
        if transaction.actor != self._actor:
            raise _request_error(
                "agent transaction actor does not match the authenticated local session",
                code="agent.actor_mismatch",
                phase="validate",
                details={"field": "actor"},
            )
        return transaction

    def _decode_snapshot(self, value: JsonValue, *, field: str) -> WorldSession:
        if type(value) is not str:
            raise _request_error(
                "world snapshot arguments must be base64 text",
                code="agent.invalid_request",
                phase="decode",
                details={"field": field},
            )
        try:
            encoded = value.encode("ascii")
            document = b64decode(encoded, validate=True)
        except (UnicodeEncodeError, Base64Error) as error:
            raise _request_error(
                "world snapshot argument is not valid base64",
                code="agent.invalid_request",
                phase="decode",
                details={"field": field},
            ) from error
        if len(document) > self._limits.max_snapshot_bytes:
            raise _limit_error("snapshot_bytes", len(document), self._limits.max_snapshot_bytes)
        return self._snapshot_codec.decode(document)

    def _record_receipt(self, receipt: TransactionReceipt) -> None:
        if receipt.status is ReceiptStatus.COMMITTED:
            self._counters["transactions_committed"] += 1
        elif receipt.status is ReceiptStatus.REJECTED:
            self._counters["transactions_rejected"] += 1

    def _require_write(self, tool: str) -> None:
        if not self._capabilities.write:
            raise _capability_error("write", tool)

    def _enter_mutation(self, tool: str) -> None:
        self._assert_owner(tool)
        if not self._mutation_gate.acquire(blocking=False):
            raise AgentConcurrencyError(
                "another mutating request already owns the engine safe point",
                code="agent.mutation_busy",
                subsystem="agent",
                phase="safe_point",
                details={"tool": tool, "policy": "reject"},
            )

    def _leave_mutation(self) -> None:
        self._mutation_gate.release()

    def _assert_owner(self, operation: str) -> None:
        if threading.get_ident() != self._owner_thread:
            raise AgentConcurrencyError(
                "agent service calls are owned by the constructing thread",
                code="agent.wrong_thread",
                subsystem="agent",
                phase="ownership",
                details={
                    "operation": operation,
                    "owner": "constructing_thread",
                    "caller": "different_thread",
                },
            )

    def _guard_open(self, operation: str) -> None:
        if self._closed:
            raise AgentConcurrencyError(
                "agent service is closed",
                code="agent.closed",
                subsystem="agent",
                phase="lifecycle",
                details={"operation": operation},
            )

    def _enforce_rate_limit(self) -> None:
        now = self._clock.now_ns()
        threshold = now - self._limits.rate_window_ns
        while self._rate_samples and self._rate_samples[0] <= threshold:
            self._rate_samples.popleft()
        if len(self._rate_samples) >= self._limits.max_requests_per_window:
            raise _limit_error(
                "requests_per_window",
                len(self._rate_samples) + 1,
                self._limits.max_requests_per_window,
            )
        self._rate_samples.append(now)


class _MutationLease:
    __slots__ = ("_service", "_tool")

    def __init__(self, service: AgentCommandService, tool: str) -> None:
        self._service = service
        self._tool = tool

    def __enter__(self) -> None:
        self._service._enter_mutation(self._tool)

    def __exit__(self, *_exception: object) -> bool:
        self._service._leave_mutation()
        return False


def _receipt_result(receipt: TransactionReceipt) -> dict[str, JsonValue]:
    return {
        "protocol": "ludoweave.agent.transaction/1",
        "receipt": receipt.as_dict(),
    }


def _arguments(arguments: Mapping[str, object] | None) -> dict[str, JsonValue]:
    source: Mapping[str, object] = {} if arguments is None else arguments
    checked = validate_json_value(dict(source))
    if not isinstance(checked, dict):
        raise AssertionError("validated argument mapping did not remain an object")
    return checked


def _exact_fields(
    arguments: Mapping[str, JsonValue],
    *,
    required: set[str],
    optional: set[str],
    tool: str,
) -> None:
    actual = set(arguments)
    missing = sorted(required - actual)
    unexpected = sorted(actual - required - optional)
    if missing or unexpected:
        raise _request_error(
            "agent tool arguments do not match the exact schema",
            code="agent.invalid_request",
            phase="validate",
            details={
                "tool": tool,
                "missing": ",".join(missing),
                "unexpected": ",".join(unexpected),
            },
        )


def _positive_int(value: object, *, field: str, tool: str) -> int:
    if type(value) is not int or value <= 0:
        raise _request_error(
            "agent tool field must be a positive integer",
            code="agent.invalid_request",
            phase="validate",
            details={"tool": tool, "field": field, "actual_type": type(value).__name__},
        )
    return value


def _stable_id(value: object, *, field: str, tool: str) -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _request_error(
            "agent tool field must use bounded stable text",
            code="agent.invalid_request",
            phase="validate",
            details={"tool": tool, "field": field},
        )
    return value


def _entity_id(value: object) -> str:
    if type(value) is not str or _ENTITY_ID.fullmatch(value) is None:
        raise _request_error(
            "entity_get requires an index:generation entity ID",
            code="agent.invalid_request",
            phase="validate",
            details={"field": "entity"},
        )
    return value


def _component_ids(value: object, session: WorldSession, *, field: str) -> set[str]:
    if not isinstance(value, list):
        raise _request_error(
            "world query component filters must be arrays",
            code="agent.invalid_query",
            phase="query",
            details={"field": field},
        )
    result: set[str] = set()
    for item in cast(list[object], value):
        if type(item) is not str:
            raise _request_error(
                "world query component filters must contain UUID text",
                code="agent.invalid_query",
                phase="query",
                details={"field": field},
            )
        try:
            type_id = UUID(item)
            session.component_registry.schema_for_id(type_id)
        except (ValueError, LudoWeaveError) as error:
            raise _request_error(
                "world query component filter is not registered",
                code="agent.invalid_query",
                phase="query",
                details={"field": field, "type_id": item},
            ) from error
        if item in result:
            raise _request_error(
                "world query component filters must not contain duplicates",
                code="agent.invalid_query",
                phase="query",
                details={"field": field, "type_id": item},
            )
        result.add(item)
    return result


def _authority_entities(
    document: dict[str, JsonValue],
) -> tuple[tuple[str, list[JsonValue]], ...]:
    by_entity: dict[str, list[JsonValue]] = {}
    allocator = _object(document["allocator"])
    generations = _array(allocator["generations"])
    alive = _array(allocator["alive"])
    for index, (generation, is_alive) in enumerate(zip(generations, alive, strict=True)):
        if is_alive is True:
            if type(generation) is not int:
                raise AssertionError("engine authority generation is not an integer")
            by_entity[f"{index}:{generation}"] = []
    for table_value in _array(document["components"]):
        table = _object(table_value)
        type_id = _text(table["type_id"])
        version = _integer(table["version"])
        for row_value in _array(table["rows"]):
            row = _object(row_value)
            entity_parts = _array(row["entity"])
            if len(entity_parts) != 2:
                raise AssertionError("engine authority entity tuple is malformed")
            entity = f"{_integer(entity_parts[0])}:{_integer(entity_parts[1])}"
            by_entity[entity].append(
                {
                    "type_id": type_id,
                    "version": version,
                    "changed_epoch": _integer(row["changed_epoch"]),
                    "values": _object(row["values"]),
                }
            )
    return tuple(
        (
            entity,
            sorted(
                components,
                key=lambda component: _text(_object(component)["type_id"]),
            ),
        )
        for entity, components in sorted(by_entity.items(), key=lambda item: _entity_sort(item[0]))
    )


def _entity_sort(value: str) -> tuple[int, int]:
    index, generation = value.split(":", 1)
    return int(index), int(generation)


def _test_names(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise _request_error(
            "test_run tests must be an array",
            code="agent.invalid_request",
            phase="test",
            details={"field": "tests"},
        )
    names = tuple(cast(list[object], value))
    if any(type(name) is not str or _STABLE_ID.fullmatch(name) is None for name in names):
        raise _request_error(
            "test_run tests must contain stable names",
            code="agent.invalid_request",
            phase="test",
            details={"field": "tests"},
        )
    checked = cast(tuple[str, ...], names)
    if len(set(checked)) != len(checked):
        raise _request_error(
            "test_run tests must not contain duplicates",
            code="agent.invalid_request",
            phase="test",
            details={"field": "tests"},
        )
    return checked


def _object(value: JsonValue) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise AssertionError("engine-produced JSON value is not an object")
    return value


def _array(value: JsonValue) -> list[JsonValue]:
    if not isinstance(value, list):
        raise AssertionError("engine-produced JSON value is not an array")
    return value


def _text(value: JsonValue) -> str:
    if type(value) is not str:
        raise AssertionError("engine-produced JSON value is not text")
    return value


def _integer(value: JsonValue) -> int:
    if type(value) is not int:
        raise AssertionError("engine-produced JSON value is not an integer")
    return value


def _redact(value: JsonValue, *, key: str | None = None) -> JsonValue:
    if key is not None and any(part in key.casefold() for part in _SENSITIVE_KEY_PARTS):
        return _REDACTED
    if isinstance(value, dict):
        return {name: _redact(item, key=name) for name, item in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


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


def _capability_error(capability: str, tool: str) -> AgentCapabilityError:
    return AgentCapabilityError(
        "agent capability is disabled for this local session",
        code="agent.capability_denied",
        subsystem="agent",
        phase="authorize",
        details={"capability": capability, "tool": tool},
    )


def _limit_error(field: str, actual: int, limit: int) -> AgentLimitError:
    return AgentLimitError(
        "agent request exceeds a configured service limit",
        code="agent.limit_exceeded",
        subsystem="agent",
        phase="limit",
        details={"field": field, "actual": actual, "limit": limit},
    )


def _provider_error(
    message: str,
    *,
    phase: str,
    provider: str,
    cause: Exception | None,
) -> AgentProviderError:
    cause_code = (
        cause.code
        if isinstance(cause, LudoWeaveError)
        else None
        if cause is None
        else type(cause).__name__
    )
    return AgentProviderError(
        message,
        code="agent.provider_failed",
        subsystem="agent",
        phase=phase,
        details={"provider": provider, "cause_code": cause_code},
    )
