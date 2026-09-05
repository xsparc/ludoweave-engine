"""Explicit cache population after complete verified asset realization."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from ludoweave.assets.cache import (
    AssetCachePublishEntry,
    AssetCachePublishSummary,
    AssetCacheStore,
)
from ludoweave.assets.execution import (
    DEFAULT_ASSET_BUILD_EXECUTION_LIMITS,
    AssetBuildExecutionLimits,
    AssetBuildInput,
)
from ludoweave.assets.pipeline import AssetError, AssetUri
from ludoweave.assets.plans import AssetBuildPlan
from ludoweave.assets.realization import (
    AssetBuildRealization,
    AssetBuildRealizationEntry,
    realize_asset_build_plan,
)

ASSET_CACHE_POPULATION_PROTOCOL = "ludoweave.asset-cache-population/1"

_REPORT_MAX_BYTES = 8 * 1024 * 1024
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AssetCachePopulationEntry:
    """Plan-ordered realization and publication evidence for one artifact."""

    realization: AssetBuildRealizationEntry
    publication: AssetCachePublishEntry

    def __post_init__(self) -> None:
        if (
            type(self.realization) is not AssetBuildRealizationEntry
            or type(self.publication) is not AssetCachePublishEntry
            or self.realization.uri != self.publication.uri
            or self.realization.result.cache_key != self.publication.cache_key
            or self.realization.result.artifact_sha256 != self.publication.artifact_sha256
            or self.realization.result.artifact_bytes != self.publication.artifact_bytes
        ):
            raise _population_error(
                "asset cache population entry is invalid",
                code="asset_cache.invalid_population",
                phase="report",
                details={"field": "entry"},
            )

    @property
    def uri(self) -> AssetUri:
        return self.realization.uri

    def as_dict(self) -> dict[str, object]:
        return {
            **self.realization.result.as_dict(),
            "realization_status": self.realization.status,
            "publication_status": self.publication.status,
        }


@dataclass(frozen=True, slots=True)
class AssetCachePopulation:
    """Complete immutable evidence for explicit post-realization publication."""

    realization: AssetBuildRealization
    publication: AssetCachePublishSummary
    entries: tuple[AssetCachePopulationEntry, ...]
    protocol: str = ASSET_CACHE_POPULATION_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_POPULATION_PROTOCOL
            or type(self.realization) is not AssetBuildRealization
            or type(self.publication) is not AssetCachePublishSummary
            or type(self.entries) is not tuple
            or any(type(entry) is not AssetCachePopulationEntry for entry in self.entries)
            or self.publication.plan_sha256 != self.realization.materialization.result.plan_sha256
            or tuple(entry.realization for entry in self.entries) != self.realization.entries
            or tuple(entry.publication for entry in self.entries) != self.publication.entries
            or len({entry.uri for entry in self.entries}) != len(self.entries)
            or _SHA256.fullmatch(self.publication.plan_sha256) is None
        ):
            raise _population_error(
                "asset cache population report is invalid",
                code="asset_cache.invalid_population",
                phase="report",
                details={"field": "population"},
            )

    @property
    def hits(self) -> int:
        return self.realization.hits

    @property
    def decoded(self) -> int:
        return self.realization.decoded

    @property
    def published(self) -> int:
        return self.publication.published

    @property
    def reused(self) -> int:
        return self.publication.reused

    def as_dict(self) -> dict[str, object]:
        result = self.realization.materialization.result
        return {
            "$schema": self.protocol,
            "loader_protocol": result.loader_protocol,
            "plan_sha256": result.plan_sha256,
            "source_bytes": result.source_bytes,
            "artifact_bytes": result.artifact_bytes,
            "hits": self.hits,
            "decoded": self.decoded,
            "published": self.published,
            "reused": self.reused,
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
            raise _population_error(
                "asset cache population report exceeds its byte bound",
                code="asset_cache.invalid_population",
                phase="report",
                details={"field": "report_bytes"},
            )
        return encoded


def populate_asset_build_cache(
    plan: AssetBuildPlan,
    inputs: tuple[AssetBuildInput, ...],
    cache_root: Path,
    *,
    project_root: Path | None = None,
    limits: AssetBuildExecutionLimits = DEFAULT_ASSET_BUILD_EXECUTION_LIMITS,
) -> AssetCachePopulation:
    """Realize a complete plan before acquiring authority to publish it."""

    read_store = AssetCacheStore(
        cache_root,
        project_root=project_root,
        writable=False,
    )
    realization = realize_asset_build_plan(plan, inputs, read_store, limits=limits)
    write_store = AssetCacheStore(
        read_store.root,
        project_root=project_root,
        writable=True,
    )
    publication = write_store.publish(realization.materialization)
    entries = tuple(
        AssetCachePopulationEntry(realized, published)
        for realized, published in zip(
            realization.entries,
            publication.entries,
            strict=True,
        )
    )
    return AssetCachePopulation(realization, publication, entries)


def _population_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> AssetError:
    return AssetError(
        message,
        code=code,
        subsystem="asset_cache",
        phase=phase,
        details=details,
    )
