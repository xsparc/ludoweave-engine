"""Read-only cache-assisted realization of verified asset build plans."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256

from ludoweave.assets.cache import AssetCacheStore
from ludoweave.assets.execution import (
    DEFAULT_ASSET_BUILD_EXECUTION_LIMITS,
    AssetBuildArtifact,
    AssetBuildExecutionLimits,
    AssetBuildInput,
    AssetBuildMaterialization,
    AssetBuildResult,
    AssetBuildResultEntry,
    _decode_payload,  # pyright: ignore[reportPrivateUsage]
)
from ludoweave.assets.pipeline import AssetError, AssetUri
from ludoweave.assets.plans import AssetBuildPlan, AssetBuildPlanEntry

ASSET_BUILD_REALIZATION_PROTOCOL = "ludoweave.asset-build-realization/1"

_REPORT_MAX_BYTES = 8 * 1024 * 1024
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AssetBuildRealizationEntry:
    """One plan-ordered verified cache hit or locally decoded result."""

    result: AssetBuildResultEntry
    status: str

    def __post_init__(self) -> None:
        if (
            type(self.result) is not AssetBuildResultEntry
            or type(self.status) is not str
            or self.status not in {"hit", "decoded"}
        ):
            raise _realization_error(
                "asset build realization entry is invalid",
                code="asset_build.invalid_realization",
                phase="report",
                details={"field": "entry"},
            )

    @property
    def uri(self) -> AssetUri:
        return self.result.uri

    def as_dict(self) -> dict[str, object]:
        return {**self.result.as_dict(), "status": self.status}


@dataclass(frozen=True, slots=True)
class AssetBuildRealization:
    """Complete immutable materialization with path-free reuse evidence."""

    materialization: AssetBuildMaterialization
    entries: tuple[AssetBuildRealizationEntry, ...]
    protocol: str = ASSET_BUILD_REALIZATION_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_BUILD_REALIZATION_PROTOCOL
            or type(self.materialization) is not AssetBuildMaterialization
            or type(self.entries) is not tuple
            or any(type(entry) is not AssetBuildRealizationEntry for entry in self.entries)
            or tuple(entry.result for entry in self.entries) != self.materialization.result.entries
            or len({entry.uri for entry in self.entries}) != len(self.entries)
            or _SHA256.fullmatch(self.materialization.result.plan_sha256) is None
        ):
            raise _realization_error(
                "asset build realization is invalid",
                code="asset_build.invalid_realization",
                phase="report",
                details={"field": "realization"},
            )

    @property
    def hits(self) -> int:
        return sum(entry.status == "hit" for entry in self.entries)

    @property
    def decoded(self) -> int:
        return sum(entry.status == "decoded" for entry in self.entries)

    def as_dict(self) -> dict[str, object]:
        result = self.materialization.result
        return {
            "$schema": self.protocol,
            "loader_protocol": result.loader_protocol,
            "plan_sha256": result.plan_sha256,
            "source_bytes": result.source_bytes,
            "artifact_bytes": result.artifact_bytes,
            "hits": self.hits,
            "decoded": self.decoded,
            "entries": [entry.as_dict() for entry in self.entries],
        }

    def canonical_bytes(self) -> bytes:
        encoded = json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        if len(encoded) > _REPORT_MAX_BYTES:
            raise _realization_error(
                "asset build realization report exceeds its byte bound",
                code="asset_build.invalid_realization",
                phase="report",
                details={"field": "report_bytes"},
            )
        return encoded


def realize_asset_build_plan(
    plan: AssetBuildPlan,
    inputs: tuple[AssetBuildInput, ...],
    cache: AssetCacheStore,
    *,
    limits: AssetBuildExecutionLimits = DEFAULT_ASSET_BUILD_EXECUTION_LIMITS,
) -> AssetBuildRealization:
    """Verify cache candidates, decode misses, and retain plan-ordered payloads."""

    if type(cache) is not AssetCacheStore:
        raise _realization_error(
            "asset build realization requires an exact local cache store",
            code="asset_build.invalid_cache",
            phase="configure",
            details={"field": "cache"},
        )
    total_source_bytes = _preflight_inputs(plan, inputs, limits=limits)

    cached: list[AssetBuildArtifact | None] = []
    cached_artifact_bytes = 0
    for entry in plan.entries:
        artifact = cache.load_action(entry)
        if artifact is not None:
            cached_artifact_bytes = _checked_artifact_total(
                cached_artifact_bytes,
                artifact,
                limits=limits,
            )
        cached.append(artifact)

    artifacts: list[AssetBuildArtifact] = []
    entries: list[AssetBuildRealizationEntry] = []
    total_artifact_bytes = 0
    for plan_entry, item, cached_artifact in zip(plan.entries, inputs, cached, strict=True):
        if cached_artifact is None:
            artifact = _decode_artifact(plan_entry, item)
            status = "decoded"
        else:
            artifact = cached_artifact
            status = "hit"
        total_artifact_bytes = _checked_artifact_total(
            total_artifact_bytes,
            artifact,
            limits=limits,
        )
        artifacts.append(artifact)
        entries.append(AssetBuildRealizationEntry(artifact.entry, status))

    materialization = AssetBuildMaterialization(
        AssetBuildResult(
            plan_sha256=f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}",
            source_bytes=total_source_bytes,
            artifact_bytes=total_artifact_bytes,
            entries=tuple(artifact.entry for artifact in artifacts),
        ),
        tuple(artifacts),
    )
    return AssetBuildRealization(materialization, tuple(entries))


def _preflight_inputs(
    plan: AssetBuildPlan,
    inputs: tuple[AssetBuildInput, ...],
    *,
    limits: AssetBuildExecutionLimits,
) -> int:
    if type(plan) is not AssetBuildPlan or type(inputs) is not tuple:
        raise _invalid_inputs()
    if type(limits) is not AssetBuildExecutionLimits:
        raise _realization_error(
            "asset build realization requires exact limits",
            code="asset_build.invalid_limits",
            phase="configure",
            details={"actual_type": type(limits).__name__},
        )
    if any(type(item) is not AssetBuildInput for item in inputs):
        raise _invalid_inputs()
    expected_uris = tuple(entry.uri for entry in plan.entries)
    actual_uris = tuple(item.uri for item in inputs)
    if actual_uris != expected_uris:
        uri = next(
            (
                expected
                for expected, actual in zip(expected_uris, actual_uris, strict=False)
                if expected != actual
            ),
            None,
        )
        details: dict[str, str | int | float | bool | None] = {"field": "inputs"}
        if uri is not None:
            details["uri"] = uri.value
        raise _realization_error(
            "asset build inputs do not match exact plan order",
            code="asset_build.invalid_inputs",
            phase="configure",
            details=details,
        )

    total_source_bytes = 0
    for entry, item in zip(plan.entries, inputs, strict=True):
        source_bytes = len(item.source)
        if source_bytes > limits.max_source_bytes:
            raise _limit_error(
                field="source_bytes",
                limit=limits.max_source_bytes,
                uri=item.uri,
            )
        total_source_bytes += source_bytes
        if total_source_bytes > limits.max_total_source_bytes:
            raise _limit_error(
                field="total_source_bytes",
                limit=limits.max_total_source_bytes,
                uri=item.uri,
            )
        if source_bytes != entry.source_bytes:
            raise _input_mismatch(field="source_bytes", uri=item.uri)
        if f"sha256:{sha256(item.source).hexdigest()}" != entry.source_sha256:
            raise _input_mismatch(field="source_sha256", uri=item.uri)
    return total_source_bytes


def _decode_artifact(
    plan_entry: AssetBuildPlanEntry,
    item: AssetBuildInput,
) -> AssetBuildArtifact:
    try:
        payload = _decode_payload(plan_entry.kind, item.source)
    except AssetError as error:
        raise _realization_error(
            "asset build decoder rejected a verified source",
            code="asset_build.decode_failed",
            phase="execute",
            details={"uri": plan_entry.uri.value, "cause_code": error.code},
        ) from error
    result = AssetBuildResultEntry(
        uri=plan_entry.uri,
        kind=plan_entry.kind,
        cache_key=plan_entry.cache_key,
        source_bytes=len(item.source),
        artifact_sha256=f"sha256:{sha256(payload).hexdigest()}",
        artifact_bytes=len(payload),
    )
    return AssetBuildArtifact(result, payload)


def _checked_artifact_total(
    total_artifact_bytes: int,
    artifact: AssetBuildArtifact,
    *,
    limits: AssetBuildExecutionLimits,
) -> int:
    artifact_bytes = artifact.entry.artifact_bytes
    if artifact_bytes > limits.max_artifact_bytes:
        raise _limit_error(
            field="artifact_bytes",
            limit=limits.max_artifact_bytes,
            uri=artifact.entry.uri,
        )
    updated = total_artifact_bytes + artifact_bytes
    if updated > limits.max_total_artifact_bytes:
        raise _limit_error(
            field="total_artifact_bytes",
            limit=limits.max_total_artifact_bytes,
            uri=artifact.entry.uri,
        )
    return updated


def _invalid_inputs() -> AssetError:
    return _realization_error(
        "asset build realization requires an exact plan and input tuple",
        code="asset_build.invalid_inputs",
        phase="configure",
        details={"field": "inputs"},
    )


def _input_mismatch(*, field: str, uri: AssetUri) -> AssetError:
    return _realization_error(
        "detached asset source does not match the verified plan",
        code="asset_build.input_mismatch",
        phase="execute",
        details={"field": field, "uri": uri.value},
    )


def _limit_error(*, field: str, limit: int, uri: AssetUri) -> AssetError:
    return _realization_error(
        "asset build realization exceeds a configured resource limit",
        code="asset_build.limit_exceeded",
        phase="execute",
        details={"field": field, "limit": limit, "uri": uri.value},
    )


def _realization_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> AssetError:
    return AssetError(
        message,
        code=code,
        subsystem="assets",
        phase=phase,
        details=details,
    )
