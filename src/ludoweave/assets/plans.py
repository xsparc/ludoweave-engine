"""Pure dependency-first plans for verified selected asset inputs."""

from __future__ import annotations

import heapq
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from math import isfinite
from typing import cast

from ludoweave.assets.locks import ASSET_SOURCE_MAX_BYTES, AssetSourceLock
from ludoweave.assets.pipeline import (
    ASSET_LOADER_PROTOCOL,
    AssetError,
    AssetKind,
    AssetManifest,
    AssetUri,
    SettingValue,
    asset_cache_key,
)

ASSET_BUILD_PLAN_PROTOCOL = "ludoweave.asset-build-plan/1"

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_MAX_PLAN_BYTES = 8 * 1024 * 1024
_MAX_ENTRIES = 4_096
_MAX_ROOTS = 4_096
_MAX_SETTINGS = 128
_MAX_DEPENDENCIES = 256


@dataclass(frozen=True, slots=True)
class AssetBuildPlanLimits:
    """Tightening-only decode limits for one asset build plan."""

    max_bytes: int = _MAX_PLAN_BYTES
    max_entries: int = _MAX_ENTRIES
    max_roots: int = _MAX_ROOTS

    def __post_init__(self) -> None:
        for field, maximum in (
            ("max_bytes", _MAX_PLAN_BYTES),
            ("max_entries", _MAX_ENTRIES),
            ("max_roots", _MAX_ROOTS),
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _plan_error(
                    "asset build plan limits must be exact positive integers",
                    code="asset_build_plan.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _plan_error(
                    "asset build plan limits may tighten but not exceed hard maxima",
                    code="asset_build_plan.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )


DEFAULT_ASSET_BUILD_PLAN_LIMITS = AssetBuildPlanLimits()


@dataclass(frozen=True, slots=True)
class AssetBuildPlanEntry:
    """One prospective build action in dependency-first plan order."""

    uri: AssetUri
    kind: AssetKind
    settings: tuple[tuple[str, SettingValue], ...]
    source_sha256: str
    source_bytes: int
    dependencies: tuple[AssetUri, ...]
    cache_key: str

    def __post_init__(self) -> None:
        if type(self.uri) is not AssetUri or type(self.kind) is not AssetKind:
            raise _entry_error(field="identity")
        if type(self.settings) is not tuple:
            raise _entry_error(field="settings")
        settings = self.settings
        if (
            len(settings) > _MAX_SETTINGS
            or any(
                type(item) is not tuple
                or len(item) != 2
                or not _setting_name(item[0])
                or not _setting_value(item[1])
                for item in settings
            )
            or len({item[0] for item in settings}) != len(settings)
        ):
            raise _entry_error(field="settings")
        if type(self.dependencies) is not tuple:
            raise _entry_error(field="dependencies")
        dependencies = self.dependencies
        if (
            len(dependencies) > _MAX_DEPENDENCIES
            or any(type(item) is not AssetUri for item in dependencies)
            or len(set(dependencies)) != len(dependencies)
            or self.uri in dependencies
        ):
            raise _entry_error(field="dependencies")
        if (
            type(self.source_sha256) is not str
            or _SHA256.fullmatch(self.source_sha256) is None
            or type(self.source_bytes) is not int
            or not 0 <= self.source_bytes <= ASSET_SOURCE_MAX_BYTES
            or type(self.cache_key) is not str
            or _SHA256.fullmatch(self.cache_key) is None
        ):
            raise _entry_error(field="content_identity")
        object.__setattr__(self, "settings", tuple(sorted(settings)))
        object.__setattr__(self, "dependencies", tuple(sorted(dependencies)))

    def as_dict(self) -> dict[str, object]:
        """Return a detached ordinary JSON representation."""

        return {
            "uri": self.uri.value,
            "kind": self.kind.value,
            "settings": dict(self.settings),
            "source_sha256": self.source_sha256,
            "source_bytes": self.source_bytes,
            "dependencies": [item.value for item in self.dependencies],
            "cache_key": self.cache_key,
        }


@dataclass(frozen=True, slots=True)
class AssetBuildPlan:
    """Verified prospective actions in deterministic dependency-first order."""

    asset_source_lock_sha256: str
    asset_manifest_sha256: str
    roots: tuple[AssetUri, ...]
    entries: tuple[AssetBuildPlanEntry, ...]
    loader_protocol: str = ASSET_LOADER_PROTOCOL
    protocol: str = ASSET_BUILD_PLAN_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != ASSET_BUILD_PLAN_PROTOCOL:
            raise _plan_error(
                "asset build plan protocol is unsupported",
                code="asset_build_plan.incompatible_protocol",
                phase="construct",
                details={"field": "$schema"},
            )
        if type(self.loader_protocol) is not str or self.loader_protocol != ASSET_LOADER_PROTOCOL:
            raise _plan_error(
                "asset build plan loader protocol is unsupported",
                code="asset_build_plan.incompatible_loader",
                phase="construct",
                details={"field": "loader_protocol"},
            )
        _require_sha256(
            self.asset_source_lock_sha256,
            field="asset_source_lock_sha256",
            phase="construct",
        )
        _require_sha256(
            self.asset_manifest_sha256,
            field="asset_manifest_sha256",
            phase="construct",
        )
        if (
            type(self.roots) is not tuple
            or len(self.roots) > _MAX_ROOTS
            or any(type(root) is not AssetUri for root in self.roots)
            or len(set(self.roots)) != len(self.roots)
        ):
            raise _plan_error(
                "asset build plan roots must be distinct exact logical URIs",
                code="asset_build_plan.invalid_roots",
                phase="construct",
                details={"field": "roots"},
            )
        if (
            type(self.entries) is not tuple
            or len(self.entries) > _MAX_ENTRIES
            or any(type(entry) is not AssetBuildPlanEntry for entry in self.entries)
        ):
            raise _plan_error(
                "asset build plan entries must be an exact bounded tuple",
                code="asset_build_plan.invalid_entries",
                phase="construct",
                details={"field": "entries"},
            )
        entry_uris = tuple(entry.uri for entry in self.entries)
        if len(set(entry_uris)) != len(entry_uris):
            raise _plan_error(
                "asset build plan repeats a logical URI",
                code="asset_build_plan.duplicate_uri",
                phase="construct",
                details={"field": "uri"},
            )
        positions = {uri: index for index, uri in enumerate(entry_uris)}
        for index, entry in enumerate(self.entries):
            for dependency in entry.dependencies:
                if dependency not in positions:
                    raise _plan_error(
                        "asset build plan dependency is absent",
                        code="asset_build_plan.invalid_dependencies",
                        phase="construct",
                        details={"uri": entry.uri.value, "dependency": dependency.value},
                    )
                if positions[dependency] >= index:
                    raise _plan_error(
                        "asset build plan is not dependency-first",
                        code="asset_build_plan.invalid_order",
                        phase="construct",
                        details={"uri": entry.uri.value, "dependency": dependency.value},
                    )
        dependencies_by_uri = {entry.uri: entry.dependencies for entry in self.entries}
        if entry_uris != _ordered_uris(dependencies_by_uri):
            raise _plan_error(
                "asset build plan does not use canonical ready-set URI order",
                code="asset_build_plan.invalid_order",
                phase="construct",
                details={"field": "entries"},
            )
        roots = tuple(sorted(self.roots))
        missing_roots = tuple(root for root in roots if root not in positions)
        if missing_roots:
            raise _plan_error(
                "asset build plan root is absent",
                code="asset_build_plan.unknown_root",
                phase="construct",
                details={"uri": missing_roots[0].value},
            )
        reachable = _reachable(roots, dependencies_by_uri)
        if reachable != set(entry_uris):
            raise _plan_error(
                "asset build plan entries do not equal the rooted dependency closure",
                code="asset_build_plan.invalid_entries",
                phase="construct",
                details={"field": "entries"},
            )
        keys: dict[AssetUri, str] = {}
        for entry in self.entries:
            expected = asset_cache_key(
                uri=entry.uri,
                kind=entry.kind,
                settings=entry.settings,
                source_hash=entry.source_sha256,
                dependency_keys=tuple(keys[dependency] for dependency in entry.dependencies),
            )
            if entry.cache_key != expected:
                raise _plan_error(
                    "asset build plan cache key does not match declared inputs",
                    code="asset_build_plan.invalid_cache_key",
                    phase="construct",
                    details={"uri": entry.uri.value},
                )
            keys[entry.uri] = entry.cache_key
        object.__setattr__(self, "roots", roots)

    @classmethod
    def from_inputs(
        cls,
        manifest: AssetManifest,
        source_lock: AssetSourceLock,
    ) -> AssetBuildPlan:
        """Plan the exact verified closure without reading, decoding, or building."""

        if type(manifest) is not AssetManifest or type(source_lock) is not AssetSourceLock:
            raise _plan_error(
                "asset build planning requires exact manifest and lock values",
                code="asset_build_plan.invalid_inputs",
                phase="plan",
                details={"field": "inputs"},
            )
        manifest_hash = f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}"
        if source_lock.asset_manifest_sha256 != manifest_hash:
            raise _input_mismatch(field="asset_manifest_sha256")
        try:
            closure = manifest.dependency_closure(source_lock.roots)
        except AssetError as error:
            raise _input_mismatch(field="roots") from error
        locked_by_uri = {entry.uri: entry for entry in source_lock.entries}
        if closure != tuple(sorted(locked_by_uri)):
            raise _input_mismatch(field="entries")
        for uri in closure:
            if manifest.entry(uri).kind is not locked_by_uri[uri].kind:
                raise _input_mismatch(field="kind", uri=uri)
        order = _dependency_order(manifest, closure)
        keys: dict[AssetUri, str] = {}
        entries: list[AssetBuildPlanEntry] = []
        for uri in order:
            declared = manifest.entry(uri)
            locked = locked_by_uri[uri]
            cache_key = asset_cache_key(
                uri=uri,
                kind=declared.kind,
                settings=declared.settings,
                source_hash=locked.source_sha256,
                dependency_keys=tuple(keys[item] for item in declared.dependencies),
            )
            entries.append(
                AssetBuildPlanEntry(
                    uri=uri,
                    kind=declared.kind,
                    settings=declared.settings,
                    source_sha256=locked.source_sha256,
                    source_bytes=locked.source_bytes,
                    dependencies=declared.dependencies,
                    cache_key=cache_key,
                )
            )
            keys[uri] = cache_key
        return cls(
            asset_source_lock_sha256=(
                f"sha256:{sha256(source_lock.canonical_bytes()).hexdigest()}"
            ),
            asset_manifest_sha256=manifest_hash,
            roots=source_lock.roots,
            entries=tuple(entries),
        )

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: AssetBuildPlanLimits = DEFAULT_ASSET_BUILD_PLAN_LIMITS,
    ) -> AssetBuildPlan:
        """Decode one bounded exact asset build plan document."""

        checked_limits = _require_limits(limits)
        raw = _document_bytes(document, max_bytes=checked_limits.max_bytes)
        try:
            decoded: object = json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=_unique_object,
                parse_float=_finite_float,
                parse_constant=_reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
            raise _plan_error(
                "asset build plan JSON could not be decoded",
                code="asset_build_plan.invalid_json",
                phase="decode",
                details={"cause_type": type(error).__name__},
            ) from error
        root = _object(decoded, field="plan")
        _exact_fields(
            root,
            required={
                "$schema",
                "loader_protocol",
                "asset_source_lock_sha256",
                "asset_manifest_sha256",
                "roots",
                "entries",
            },
            field="plan",
        )
        raw_roots = root["roots"]
        raw_entries = root["entries"]
        if type(raw_roots) is not list or type(raw_entries) is not list:
            raise _document_error(field="roots_or_entries")
        roots_list = cast(list[object], raw_roots)
        entries_list = cast(list[object], raw_entries)
        if len(roots_list) > checked_limits.max_roots:
            raise _limit_error(
                field="roots", actual=len(roots_list), limit=checked_limits.max_roots
            )
        if len(entries_list) > checked_limits.max_entries:
            raise _limit_error(
                field="entries", actual=len(entries_list), limit=checked_limits.max_entries
            )
        try:
            roots = tuple(AssetUri(_text(item, field="root")) for item in roots_list)
            entries = tuple(_entry(item) for item in entries_list)
        except AssetError as error:
            if error.code.startswith("asset_build_plan."):
                raise
            raise _document_error(field="entry") from error
        return cls(
            asset_source_lock_sha256=_require_sha256(
                root["asset_source_lock_sha256"],
                field="asset_source_lock_sha256",
                phase="decode",
            ),
            asset_manifest_sha256=_require_sha256(
                root["asset_manifest_sha256"],
                field="asset_manifest_sha256",
                phase="decode",
            ),
            roots=roots,
            entries=entries,
            loader_protocol=_text(root["loader_protocol"], field="loader_protocol"),
            protocol=_text(root["$schema"], field="$schema"),
        )

    def as_dict(self) -> dict[str, object]:
        """Return a detached normalized JSON-compatible representation."""

        return {
            "$schema": self.protocol,
            "loader_protocol": self.loader_protocol,
            "asset_source_lock_sha256": self.asset_source_lock_sha256,
            "asset_manifest_sha256": self.asset_manifest_sha256,
            "roots": [root.value for root in self.roots],
            "entries": [entry.as_dict() for entry in self.entries],
        }

    def canonical_bytes(self) -> bytes:
        """Return deterministic normalized plan bytes."""

        encoded = json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        if len(encoded) > _MAX_PLAN_BYTES:
            raise _limit_error(field="document", actual=len(encoded), limit=_MAX_PLAN_BYTES)
        return encoded


def _dependency_order(
    manifest: AssetManifest,
    closure: tuple[AssetUri, ...],
) -> tuple[AssetUri, ...]:
    selected = set(closure)
    dependencies_by_uri: dict[AssetUri, tuple[AssetUri, ...]] = {}
    for uri in closure:
        dependencies = manifest.entry(uri).dependencies
        if any(item not in selected for item in dependencies):
            raise _input_mismatch(field="entries", uri=uri)
        dependencies_by_uri[uri] = dependencies
    ordered = _ordered_uris(dependencies_by_uri)
    if len(ordered) != len(closure):
        raise _plan_error(
            "asset build plan graph could not be ordered",
            code="asset_build_plan.invalid_graph",
            phase="plan",
            details={"field": "entries"},
        )
    return ordered


def _ordered_uris(
    dependencies_by_uri: Mapping[AssetUri, tuple[AssetUri, ...]],
) -> tuple[AssetUri, ...]:
    remaining = {uri: len(dependencies) for uri, dependencies in dependencies_by_uri.items()}
    consumers: dict[AssetUri, list[AssetUri]] = {uri: [] for uri in dependencies_by_uri}
    for uri, dependencies in dependencies_by_uri.items():
        for dependency in dependencies:
            consumers[dependency].append(uri)
    ready = [uri for uri, count in remaining.items() if count == 0]
    heapq.heapify(ready)
    ordered: list[AssetUri] = []
    while ready:
        uri = heapq.heappop(ready)
        ordered.append(uri)
        for consumer in sorted(consumers[uri]):
            remaining[consumer] -= 1
            if remaining[consumer] == 0:
                heapq.heappush(ready, consumer)
    return tuple(ordered)


def _reachable(
    roots: tuple[AssetUri, ...],
    dependencies: Mapping[AssetUri, tuple[AssetUri, ...]],
) -> set[AssetUri]:
    reached: set[AssetUri] = set()
    pending = list(roots)
    while pending:
        uri = pending.pop()
        if uri in reached:
            continue
        reached.add(uri)
        pending.extend(dependencies.get(uri, ()))
    return reached


def _entry(value: object) -> AssetBuildPlanEntry:
    document = _object(value, field="entry")
    _exact_fields(
        document,
        required={
            "uri",
            "kind",
            "settings",
            "source_sha256",
            "source_bytes",
            "dependencies",
            "cache_key",
        },
        field="entry",
    )
    raw_settings = _object(document["settings"], field="settings")
    if len(raw_settings) > _MAX_SETTINGS:
        raise _limit_error(field="settings", actual=len(raw_settings), limit=_MAX_SETTINGS)
    settings = tuple(
        (_text(key, field="setting_name"), _setting_from_json(item))
        for key, item in raw_settings.items()
    )
    raw_dependencies = document["dependencies"]
    if type(raw_dependencies) is not list:
        raise _document_error(field="dependencies")
    dependency_values = cast(list[object], raw_dependencies)
    if len(dependency_values) > _MAX_DEPENDENCIES:
        raise _limit_error(
            field="dependencies",
            actual=len(dependency_values),
            limit=_MAX_DEPENDENCIES,
        )
    try:
        uri = AssetUri(_text(document["uri"], field="uri"))
        kind = AssetKind(_text(document["kind"], field="kind"))
        dependencies = tuple(
            AssetUri(_text(item, field="dependency")) for item in dependency_values
        )
    except (AssetError, ValueError) as error:
        raise _document_error(field="entry") from error
    return AssetBuildPlanEntry(
        uri=uri,
        kind=kind,
        settings=settings,
        source_sha256=_require_sha256(
            document["source_sha256"], field="source_sha256", phase="decode"
        ),
        source_bytes=_integer(document["source_bytes"], field="source_bytes"),
        dependencies=dependencies,
        cache_key=_require_sha256(document["cache_key"], field="cache_key", phase="decode"),
    )


def _document_bytes(document: str | bytes, *, max_bytes: int) -> bytes:
    try:
        if type(document) is bytes:
            raw = document
        elif type(document) is str:
            raw = document.encode("utf-8")
        else:
            raise TypeError
    except (TypeError, UnicodeEncodeError) as error:
        raise _plan_error(
            "asset build plan document must be UTF-8 text or bytes",
            code="asset_build_plan.invalid_json",
            phase="decode",
            details={"actual_type": type(document).__name__},
        ) from error
    if len(raw) > max_bytes:
        raise _limit_error(field="document", actual=len(raw), limit=max_bytes)
    return raw


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate object key")
        value[key] = item
    return value


def _finite_float(value: str) -> float:
    parsed = float(value)
    if not isfinite(parsed):
        raise ValueError("non-finite number")
    return parsed


def _reject_constant(value: str) -> object:
    raise ValueError(f"unsupported JSON constant: {value}")


def _require_limits(value: object) -> AssetBuildPlanLimits:
    if type(value) is not AssetBuildPlanLimits:
        raise _plan_error(
            "asset build plan limits must be an exact limits value",
            code="asset_build_plan.invalid_limits",
            phase="configure",
            details={"actual_type": type(value).__name__},
        )
    return value


def _object(value: object, *, field: str) -> dict[str, object]:
    if type(value) is not dict:
        raise _document_error(field=field)
    return cast(dict[str, object], value)


def _exact_fields(value: Mapping[str, object], *, required: set[str], field: str) -> None:
    if set(value) != required:
        raise _document_error(field=field)


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _document_error(field=field)
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise _document_error(field=field) from error
    if not encoded:
        raise _document_error(field=field)
    return value


def _integer(value: object, *, field: str) -> int:
    if type(value) is not int:
        raise _document_error(field=field)
    return value


def _setting_name(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        value.encode("utf-8")
        return True
    except UnicodeEncodeError:
        return False


def _setting_value(value: object) -> bool:
    return (type(value) in (str, int, bool) and (type(value) is not str or _utf8_text(value))) or (
        type(value) is float and isfinite(value)
    )


def _setting_from_json(value: object) -> SettingValue:
    if not _setting_value(value):
        raise _document_error(field="setting_value")
    return cast(SettingValue, value)


def _utf8_text(value: str) -> bool:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _require_sha256(value: object, *, field: str, phase: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise _plan_error(
            "asset build plan hash must use lowercase SHA-256 identity text",
            code="asset_build_plan.invalid_hash",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _entry_error(*, field: str) -> AssetError:
    return _plan_error(
        "asset build plan entry contains invalid immutable data",
        code="asset_build_plan.invalid_entry",
        phase="construct",
        details={"field": field},
    )


def _input_mismatch(*, field: str, uri: AssetUri | None = None) -> AssetError:
    details: dict[str, str | int | float | bool | None] = {"field": field}
    if uri is not None:
        details["uri"] = uri.value
    return _plan_error(
        "asset manifest and verified source lock do not agree",
        code="asset_build_plan.input_mismatch",
        phase="plan",
        details=details,
    )


def _limit_error(*, field: str, actual: int, limit: int) -> AssetError:
    return _plan_error(
        "asset build plan exceeds its configured limit",
        code="asset_build_plan.limit_exceeded",
        phase="decode",
        details={"field": field, "actual": actual, "limit": limit},
    )


def _document_error(*, field: str) -> AssetError:
    return _plan_error(
        "asset build plan document contains an invalid field",
        code="asset_build_plan.invalid_document",
        phase="decode",
        details={"field": field},
    )


def _plan_error(
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
