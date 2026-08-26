"""Bounded deterministic execution of detached verified asset-plan inputs."""

from __future__ import annotations

import json
import re
import struct
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256

from ludoweave.assets.locks import ASSET_SOURCE_MAX_BYTES, ASSET_SOURCE_TOTAL_MAX_BYTES
from ludoweave.assets.pipeline import (
    ASSET_LOADER_PROTOCOL,
    AssetError,
    AssetKind,
    AssetUri,
    decode_png,
)
from ludoweave.assets.plans import AssetBuildPlan

ASSET_BUILD_RESULT_PROTOCOL = "ludoweave.asset-build-result/1"
ASSET_BUILD_ARTIFACT_MAX_BYTES = 16_384 * 16_384 * 4 + 8
ASSET_BUILD_ARTIFACT_TOTAL_MAX_BYTES = ASSET_BUILD_ARTIFACT_MAX_BYTES

_MAX_RESULT_BYTES = 8 * 1024 * 1024
_MAX_ENTRIES = 4_096
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AssetBuildExecutionLimits:
    """Tightening-only source and decoded-artifact execution limits."""

    max_source_bytes: int = ASSET_SOURCE_MAX_BYTES
    max_total_source_bytes: int = ASSET_SOURCE_TOTAL_MAX_BYTES
    max_artifact_bytes: int = ASSET_BUILD_ARTIFACT_MAX_BYTES
    max_total_artifact_bytes: int = ASSET_BUILD_ARTIFACT_TOTAL_MAX_BYTES

    def __post_init__(self) -> None:
        for field, maximum in (
            ("max_source_bytes", ASSET_SOURCE_MAX_BYTES),
            ("max_total_source_bytes", ASSET_SOURCE_TOTAL_MAX_BYTES),
            ("max_artifact_bytes", ASSET_BUILD_ARTIFACT_MAX_BYTES),
            ("max_total_artifact_bytes", ASSET_BUILD_ARTIFACT_TOTAL_MAX_BYTES),
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _execution_error(
                    "asset build execution limits require exact positive integers",
                    code="asset_build.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _execution_error(
                    "asset build execution limits may tighten but not exceed hard maxima",
                    code="asset_build.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )


DEFAULT_ASSET_BUILD_EXECUTION_LIMITS = AssetBuildExecutionLimits()


@dataclass(frozen=True, slots=True)
class AssetBuildInput:
    """One detached immutable source payload in exact plan order."""

    uri: AssetUri
    source: bytes

    def __post_init__(self) -> None:
        if type(self.uri) is not AssetUri or type(self.source) is not bytes:
            raise _execution_error(
                "asset build input requires an exact URI and immutable bytes",
                code="asset_build.invalid_inputs",
                phase="configure",
                details={"field": "input"},
            )


@dataclass(frozen=True, slots=True)
class AssetBuildResultEntry:
    """Content identity for one decoded artifact without retaining its payload."""

    uri: AssetUri
    kind: AssetKind
    cache_key: str
    source_bytes: int
    artifact_sha256: str
    artifact_bytes: int

    def __post_init__(self) -> None:
        if type(self.uri) is not AssetUri or type(self.kind) is not AssetKind:
            raise _invalid_result(field="identity")
        if (
            type(self.cache_key) is not str
            or _SHA256.fullmatch(self.cache_key) is None
            or type(self.artifact_sha256) is not str
            or _SHA256.fullmatch(self.artifact_sha256) is None
        ):
            raise _invalid_result(field="hash")
        if (
            type(self.source_bytes) is not int
            or not 0 <= self.source_bytes <= ASSET_SOURCE_MAX_BYTES
            or type(self.artifact_bytes) is not int
            or not 0 <= self.artifact_bytes <= ASSET_BUILD_ARTIFACT_MAX_BYTES
        ):
            raise _invalid_result(field="bytes")

    def as_dict(self) -> dict[str, object]:
        """Return one detached normalized result entry."""

        return {
            "uri": self.uri.value,
            "kind": self.kind.value,
            "cache_key": self.cache_key,
            "source_bytes": self.source_bytes,
            "artifact_sha256": self.artifact_sha256,
            "artifact_bytes": self.artifact_bytes,
        }


@dataclass(frozen=True, slots=True)
class AssetBuildResult:
    """Deterministic identities for one complete in-memory plan execution."""

    plan_sha256: str
    source_bytes: int
    artifact_bytes: int
    entries: tuple[AssetBuildResultEntry, ...]
    loader_protocol: str = ASSET_LOADER_PROTOCOL
    protocol: str = ASSET_BUILD_RESULT_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != ASSET_BUILD_RESULT_PROTOCOL:
            raise _invalid_result(field="$schema")
        if type(self.loader_protocol) is not str or self.loader_protocol != ASSET_LOADER_PROTOCOL:
            raise _invalid_result(field="loader_protocol")
        if type(self.plan_sha256) is not str or _SHA256.fullmatch(self.plan_sha256) is None:
            raise _invalid_result(field="plan_sha256")
        if (
            type(self.entries) is not tuple
            or len(self.entries) > _MAX_ENTRIES
            or any(type(entry) is not AssetBuildResultEntry for entry in self.entries)
        ):
            raise _invalid_result(field="entries")
        if len({entry.uri for entry in self.entries}) != len(self.entries):
            raise _invalid_result(field="uri")
        if (
            type(self.source_bytes) is not int
            or self.source_bytes != sum(entry.source_bytes for entry in self.entries)
            or self.source_bytes > ASSET_SOURCE_TOTAL_MAX_BYTES
            or type(self.artifact_bytes) is not int
            or self.artifact_bytes != sum(entry.artifact_bytes for entry in self.entries)
            or self.artifact_bytes > ASSET_BUILD_ARTIFACT_TOTAL_MAX_BYTES
        ):
            raise _invalid_result(field="aggregate_bytes")

    def as_dict(self) -> dict[str, object]:
        """Return a detached normalized JSON-compatible document."""

        return {
            "$schema": self.protocol,
            "loader_protocol": self.loader_protocol,
            "plan_sha256": self.plan_sha256,
            "source_bytes": self.source_bytes,
            "artifact_bytes": self.artifact_bytes,
            "entries": [entry.as_dict() for entry in self.entries],
        }

    def canonical_bytes(self) -> bytes:
        """Return bounded deterministic result bytes."""

        encoded = json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        if len(encoded) > _MAX_RESULT_BYTES:
            raise _execution_error(
                "asset build result exceeds its document bound",
                code="asset_build.limit_exceeded",
                phase="report",
                details={"field": "result_bytes", "limit": _MAX_RESULT_BYTES},
            )
        return encoded


def execute_asset_build_plan(
    plan: AssetBuildPlan,
    inputs: tuple[AssetBuildInput, ...],
    *,
    limits: AssetBuildExecutionLimits = DEFAULT_ASSET_BUILD_EXECUTION_LIMITS,
) -> AssetBuildResult:
    """Execute built-in decoders over exact detached plan inputs without I/O."""

    if type(plan) is not AssetBuildPlan or type(inputs) is not tuple:
        raise _invalid_inputs()
    if type(limits) is not AssetBuildExecutionLimits:
        raise _execution_error(
            "asset build execution requires exact limits",
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
        raise _execution_error(
            "asset build inputs do not match exact plan order",
            code="asset_build.invalid_inputs",
            phase="configure",
            details=details,
        )

    total_source_bytes = 0
    for entry, item in zip(plan.entries, inputs, strict=True):
        source_bytes = len(item.source)
        if source_bytes > limits.max_source_bytes:
            raise _limit_error(field="source_bytes", limit=limits.max_source_bytes, uri=item.uri)
        total_source_bytes += source_bytes
        if total_source_bytes > limits.max_total_source_bytes:
            raise _limit_error(
                field="total_source_bytes",
                limit=limits.max_total_source_bytes,
                uri=item.uri,
            )
        if source_bytes != entry.source_bytes:
            raise _input_mismatch(field="source_bytes", uri=item.uri)
        source_sha256 = f"sha256:{sha256(item.source).hexdigest()}"
        if source_sha256 != entry.source_sha256:
            raise _input_mismatch(field="source_sha256", uri=item.uri)

    total_artifact_bytes = 0
    results: list[AssetBuildResultEntry] = []
    for entry, item in zip(plan.entries, inputs, strict=True):
        try:
            artifact = _decode_payload(entry.kind, item.source)
        except AssetError as error:
            raise _execution_error(
                "asset build decoder rejected a verified source",
                code="asset_build.decode_failed",
                phase="execute",
                details={"uri": entry.uri.value, "cause_code": error.code},
            ) from error
        artifact_bytes = len(artifact)
        if artifact_bytes > limits.max_artifact_bytes:
            raise _limit_error(
                field="artifact_bytes",
                limit=limits.max_artifact_bytes,
                uri=entry.uri,
            )
        total_artifact_bytes += artifact_bytes
        if total_artifact_bytes > limits.max_total_artifact_bytes:
            raise _limit_error(
                field="total_artifact_bytes",
                limit=limits.max_total_artifact_bytes,
                uri=entry.uri,
            )
        results.append(
            AssetBuildResultEntry(
                uri=entry.uri,
                kind=entry.kind,
                cache_key=entry.cache_key,
                source_bytes=len(item.source),
                artifact_sha256=f"sha256:{sha256(artifact).hexdigest()}",
                artifact_bytes=artifact_bytes,
            )
        )

    return AssetBuildResult(
        plan_sha256=f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}",
        source_bytes=total_source_bytes,
        artifact_bytes=total_artifact_bytes,
        entries=tuple(results),
    )


def _decode_payload(kind: AssetKind, source: bytes) -> bytes:
    if kind is AssetKind.PNG:
        texture = decode_png(source)
        return struct.pack(">II", texture.width, texture.height) + texture.rgba8
    if kind is AssetKind.JSON:
        try:
            decoded = json.loads(source)
            return json.dumps(
                decoded,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        except Exception as error:
            raise _decoder_error("JSON asset could not be decoded", error) from error
    if kind is AssetKind.WGSL:
        try:
            return source.decode("utf-8").encode("utf-8")
        except UnicodeError as error:
            raise _decoder_error("WGSL asset must be valid UTF-8", error) from error
    return bytes(source)


def _invalid_inputs() -> AssetError:
    return _execution_error(
        "asset build execution requires an exact plan and input tuple",
        code="asset_build.invalid_inputs",
        phase="configure",
        details={"field": "inputs"},
    )


def _input_mismatch(*, field: str, uri: AssetUri) -> AssetError:
    return _execution_error(
        "detached asset source does not match the verified plan",
        code="asset_build.input_mismatch",
        phase="execute",
        details={"field": field, "uri": uri.value},
    )


def _limit_error(*, field: str, limit: int, uri: AssetUri) -> AssetError:
    return _execution_error(
        "asset build execution exceeds a configured resource limit",
        code="asset_build.limit_exceeded",
        phase="execute",
        details={"field": field, "limit": limit, "uri": uri.value},
    )


def _invalid_result(*, field: str) -> AssetError:
    return _execution_error(
        "asset build result contains invalid immutable metadata",
        code="asset_build.invalid_result",
        phase="result",
        details={"field": field},
    )


def _decoder_error(message: str, cause: Exception) -> AssetError:
    return AssetError(
        message,
        code="asset.invalid_value",
        subsystem="asset",
        phase="load",
        details={"cause_type": type(cause).__name__},
    )


def _execution_error(
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
