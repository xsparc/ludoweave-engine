"""Small validated asset manifest, cache, PNG loader, and hot-reload slot."""

from __future__ import annotations

import json
import os
import re
import struct
import zlib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from math import isfinite
from pathlib import Path
from types import MappingProxyType
from typing import cast

from ludoweave.core.errors import LudoWeaveError

_ASSET_URI = re.compile(r"asset://[A-Za-z0-9][A-Za-z0-9._/-]{0,511}\Z")
_PATH_PART = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_CACHE_KEY = re.compile(r"sha256:[0-9a-f]{64}\Z")
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_MAX_SOURCE_BYTES = 256 * 1024 * 1024
_MAX_TEXTURE_DIMENSION = 16_384
_MAX_MANIFEST_BYTES = 4 * 1024 * 1024
_MAX_MANIFEST_ASSETS = 4_096
_MAX_MANIFEST_DEPENDENCIES = 256
_MAX_MANIFEST_SETTINGS = 128
ASSET_MANIFEST_PROTOCOL = "ludoweave.assets/1"
_LOADER_VERSION = ASSET_MANIFEST_PROTOCOL
type SettingValue = str | int | float | bool


class AssetError(LudoWeaveError):
    """Raised for asset identity, manifest, decoding, or cache failures."""


@dataclass(frozen=True, slots=True)
class AssetManifestLimits:
    """Tightening-only limits for one existing asset manifest."""

    max_bytes: int = _MAX_MANIFEST_BYTES
    max_assets: int = _MAX_MANIFEST_ASSETS
    max_dependencies: int = _MAX_MANIFEST_DEPENDENCIES
    max_settings: int = _MAX_MANIFEST_SETTINGS

    def __post_init__(self) -> None:
        maxima = (
            ("max_bytes", _MAX_MANIFEST_BYTES),
            ("max_assets", _MAX_MANIFEST_ASSETS),
            ("max_dependencies", _MAX_MANIFEST_DEPENDENCIES),
            ("max_settings", _MAX_MANIFEST_SETTINGS),
        )
        for field, maximum in maxima:
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _asset_error(
                    "asset manifest limits must be exact positive integers within hard maxima",
                    phase="configure_manifest",
                    details={"field": field, "actual_type": type(value).__name__},
                    code="asset.invalid_manifest_limits",
                )
            if value > maximum:
                raise _asset_error(
                    "asset manifest limits may tighten but not exceed hard maxima",
                    phase="configure_manifest",
                    details={"field": field, "actual": value, "maximum": maximum},
                    code="asset.invalid_manifest_limits",
                )


DEFAULT_ASSET_MANIFEST_LIMITS = AssetManifestLimits()


@dataclass(frozen=True, slots=True, order=True)
class AssetUri:
    """Normalized logical identity independent of project filesystem layout."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str or _ASSET_URI.fullmatch(self.value) is None:
            raise _asset_error(
                "asset URI must use canonical asset:// syntax",
                phase="uri",
                details={"actual_type": type(self.value).__name__},
            )
        relative = self.value.removeprefix("asset://")
        parts = relative.split("/")
        if any(part in ("", ".", "..") or _PATH_PART.fullmatch(part) is None for part in parts):
            raise _asset_error(
                "asset URI path contains an invalid segment",
                phase="uri",
                details={"field": "path"},
            )

    @property
    def path(self) -> str:
        return self.value.removeprefix("asset://")

    def __str__(self) -> str:
        return self.value


class AssetKind(StrEnum):
    PNG = "png"
    AUDIO = "audio"
    JSON = "json"
    WGSL = "wgsl"


@dataclass(frozen=True, slots=True)
class AssetEntry:
    uri: AssetUri
    kind: AssetKind
    source: str
    settings: tuple[tuple[str, SettingValue], ...] = ()
    dependencies: tuple[AssetUri, ...] = ()

    def __post_init__(self) -> None:
        if type(self.uri) is not AssetUri or type(self.kind) is not AssetKind:
            raise _asset_error(
                "asset entry requires exact URI and kind values",
                phase="manifest",
                details={"field": "entry"},
            )
        _relative_source(self.source)
        settings = tuple(self.settings)
        if len(settings) > _MAX_MANIFEST_SETTINGS:
            raise _manifest_limit_error(
                field="settings", actual=len(settings), limit=_MAX_MANIFEST_SETTINGS
            )
        if any(
            type(item) is not tuple
            or len(item) != 2
            or type(item[0]) is not str
            or not item[0]
            or not _utf8_text(item[0])
            or not _setting(item[1])
            for item in settings
        ):
            raise _asset_error(
                "asset settings must be stable scalar key/value pairs",
                phase="manifest",
                details={"field": "settings"},
            )
        if len({item[0] for item in settings}) != len(settings):
            raise _asset_error(
                "asset settings repeat a key",
                phase="manifest",
                details={"field": "settings"},
            )
        dependencies = tuple(self.dependencies)
        if len(dependencies) > _MAX_MANIFEST_DEPENDENCIES:
            raise _manifest_limit_error(
                field="dependencies",
                actual=len(dependencies),
                limit=_MAX_MANIFEST_DEPENDENCIES,
            )
        if any(type(item) is not AssetUri for item in dependencies) or self.uri in dependencies:
            raise _asset_error(
                "asset dependencies must be distinct exact URIs without self-reference",
                phase="manifest",
                details={"field": "dependencies"},
            )
        if len(set(dependencies)) != len(dependencies):
            raise _asset_error(
                "asset dependencies repeat a URI",
                phase="manifest",
                details={"field": "dependencies"},
            )
        object.__setattr__(self, "settings", tuple(sorted(settings)))
        object.__setattr__(self, "dependencies", tuple(sorted(dependencies)))


class AssetManifest:
    """Immutable project-confined logical-to-source asset map."""

    __slots__ = ("_entries", "_project_root")

    def __init__(self, project_root: Path, entries: Iterable[AssetEntry]) -> None:
        root = _root(project_root)
        try:
            values = tuple(entries)
        except Exception as error:
            raise _asset_error(
                "asset manifest entries could not be materialized",
                phase="manifest",
                details={"cause_type": type(error).__name__},
            ) from error
        if any(type(item) is not AssetEntry for item in values):
            raise _asset_error(
                "asset manifest entries must be exact AssetEntry values",
                phase="manifest",
                details={"field": "entries"},
            )
        if len(values) > _MAX_MANIFEST_ASSETS:
            raise _manifest_limit_error(
                field="assets", actual=len(values), limit=_MAX_MANIFEST_ASSETS
            )
        by_uri = {item.uri: item for item in values}
        if len(by_uri) != len(values):
            raise _asset_error(
                "asset manifest repeats a logical URI",
                phase="manifest",
                details={"field": "uri"},
            )
        for entry in values:
            self._confined(root, entry.source)
            missing = tuple(dep.value for dep in entry.dependencies if dep not in by_uri)
            if missing:
                raise _asset_error(
                    "asset dependency is not declared in the manifest",
                    phase="manifest",
                    details={"dependency": missing[0]},
                )
        _require_acyclic(by_uri)
        self._project_root = root
        self._entries = MappingProxyType(by_uri)

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        project_root: Path,
        limits: AssetManifestLimits = DEFAULT_ASSET_MANIFEST_LIMITS,
    ) -> AssetManifest:
        """Decode one bounded exact asset manifest from detached JSON."""

        checked_limits = _require_manifest_limits(limits)
        raw = _manifest_bytes(document, checked_limits.max_bytes)
        try:
            text = raw.decode("utf-8")
            decoded: object = json.loads(
                text,
                object_pairs_hook=_unique_object,
                parse_float=_finite_json_float,
                parse_constant=_reject_json_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
            raise _asset_error(
                "asset manifest JSON could not be decoded",
                phase="decode_manifest",
                details={"cause_type": type(error).__name__},
                code="asset.invalid_manifest_json",
            ) from error
        return cls._from_document(decoded, project_root=project_root, limits=checked_limits)

    @classmethod
    def load(
        cls,
        path: Path,
        *,
        project_root: Path | None = None,
        limits: AssetManifestLimits = DEFAULT_ASSET_MANIFEST_LIMITS,
    ) -> AssetManifest:
        """Decode an exact ``ludoweave.assets/1`` JSON manifest."""

        checked_limits = _require_manifest_limits(limits)
        try:
            manifest_path = path.resolve(strict=True)
            root = manifest_path.parent if project_root is None else _root(project_root)
        except OSError as error:
            raise _asset_error(
                "asset manifest is unavailable",
                phase="open_manifest",
                details={"cause_type": type(error).__name__},
                code="asset.invalid_manifest",
            ) from error
        if not manifest_path.is_relative_to(root):
            raise _asset_error(
                "asset manifest must be inside the project root",
                phase="open_manifest",
                details={"field": "path"},
                code="asset.invalid_manifest",
            )
        try:
            with manifest_path.open("rb") as handle:
                raw = handle.read(checked_limits.max_bytes + 1)
        except OSError as error:
            raise _asset_error(
                "asset manifest could not be read",
                phase="open_manifest",
                details={"cause_type": type(error).__name__},
                code="asset.invalid_manifest",
            ) from error
        return cls.from_json(raw, project_root=root, limits=checked_limits)

    @classmethod
    def _from_document(
        cls,
        document: object,
        *,
        project_root: Path,
        limits: AssetManifestLimits,
    ) -> AssetManifest:
        if type(document) is not dict:
            raise _asset_error(
                "asset manifest requires an object document",
                phase="decode_manifest",
                details={"field": "document"},
                code="asset.invalid_manifest",
            )
        checked_document = cast(dict[object, object], document)
        if set(checked_document) != {"protocol", "assets"}:
            raise _asset_error(
                "asset manifest requires exact protocol and assets fields",
                phase="decode_manifest",
                details={"field": "document"},
                code="asset.invalid_manifest",
            )
        if (
            checked_document["protocol"] != ASSET_MANIFEST_PROTOCOL
            or type(checked_document["assets"]) is not list
        ):
            raise _asset_error(
                "asset manifest protocol is unsupported",
                phase="decode_manifest",
                details={"field": "protocol"},
                code="asset.incompatible_manifest_protocol",
            )
        assets = cast(list[object], checked_document["assets"])
        if len(assets) > limits.max_assets:
            raise _manifest_limit_error(field="assets", actual=len(assets), limit=limits.max_assets)
        entries = tuple(_decode_entry(item, limits=limits) for item in assets)
        return cls(project_root, entries)

    @property
    def protocol(self) -> str:
        """Return the exact persistent asset-manifest protocol."""

        return ASSET_MANIFEST_PROTOCOL

    @property
    def project_root(self) -> Path:
        return self._project_root

    @property
    def entries(self) -> tuple[AssetEntry, ...]:
        return tuple(self._entries[uri] for uri in sorted(self._entries))

    def as_dict(self) -> dict[str, object]:
        """Return a detached normalized JSON-compatible representation."""

        assets: list[dict[str, object]] = []
        for entry in self.entries:
            assets.append(
                {
                    "uri": entry.uri.value,
                    "kind": entry.kind.value,
                    "source": entry.source,
                    "settings": dict(entry.settings),
                    "dependencies": [dependency.value for dependency in entry.dependencies],
                }
            )
        return {"protocol": self.protocol, "assets": assets}

    def canonical_bytes(self) -> bytes:
        """Return deterministic normalized manifest bytes."""

        encoded = json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        if len(encoded) > _MAX_MANIFEST_BYTES:
            raise _manifest_limit_error(
                field="document", actual=len(encoded), limit=_MAX_MANIFEST_BYTES
            )
        return encoded

    def entry(self, uri: AssetUri) -> AssetEntry:
        if type(uri) is not AssetUri:
            raise _asset_error(
                "asset lookup requires an exact AssetUri",
                phase="lookup",
                details={"actual_type": type(uri).__name__},
            )
        entry = self._entries.get(uri)
        if entry is None:
            raise _asset_error(
                "asset URI is not declared in the manifest",
                phase="lookup",
                details={"uri": uri.value},
                code="asset.unknown_uri",
            )
        return entry

    def source_path(self, uri: AssetUri) -> Path:
        entry = self.entry(uri)
        return self._confined(self._project_root, entry.source)

    @staticmethod
    def _confined(root: Path, source: str) -> Path:
        candidate = (root / _relative_source(source)).resolve(strict=False)
        if not candidate.is_relative_to(root):
            raise _asset_error(
                "asset source escapes the project root",
                phase="manifest",
                details={"field": "source"},
                code="asset.path_escape",
            )
        return candidate


@dataclass(frozen=True, slots=True)
class AssetArtifact:
    uri: AssetUri
    kind: AssetKind
    source_hash: str
    cache_key: str
    payload: bytes
    dependency_keys: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            type(self.uri) is not AssetUri
            or type(self.kind) is not AssetKind
            or type(self.payload) is not bytes
            or _CACHE_KEY.fullmatch(self.source_hash) is None
            or _CACHE_KEY.fullmatch(self.cache_key) is None
            or any(_CACHE_KEY.fullmatch(item) is None for item in self.dependency_keys)
        ):
            raise _asset_error(
                "asset artifact contains invalid immutable metadata",
                phase="artifact",
                details={"field": "artifact"},
            )


class AssetPipeline:
    """Synchronous content-addressed builder with immutable on-disk artifacts."""

    __slots__ = ("_cache_root", "_manifest")

    def __init__(self, manifest: AssetManifest, cache_root: Path) -> None:
        if type(manifest) is not AssetManifest:
            raise _asset_error(
                "asset pipeline requires an exact AssetManifest",
                phase="compose",
                details={"actual_type": type(manifest).__name__},
            )
        root = cache_root.resolve(strict=False)
        if root == manifest.project_root or manifest.project_root.is_relative_to(root):
            raise _asset_error(
                "asset cache root must not contain the project root",
                phase="compose",
                details={"field": "cache_root"},
            )
        root.mkdir(parents=True, exist_ok=True)
        self._manifest = manifest
        self._cache_root = root

    def build(self, uri: AssetUri) -> AssetArtifact:
        return self._build(uri, stack=())

    def build_all(self) -> tuple[AssetArtifact, ...]:
        return tuple(self.build(entry.uri) for entry in self._manifest.entries)

    def _build(self, uri: AssetUri, *, stack: tuple[AssetUri, ...]) -> AssetArtifact:
        if uri in stack:
            raise _asset_error(
                "asset dependency cycle reached during build",
                phase="build",
                details={"uri": uri.value},
            )
        entry = self._manifest.entry(uri)
        dependencies = tuple(
            self._build(dependency, stack=(*stack, uri)) for dependency in entry.dependencies
        )
        source_path = self._manifest.source_path(uri)
        try:
            source = source_path.read_bytes()
        except Exception as error:
            raise _asset_error(
                "asset source could not be read",
                phase="build",
                details={"uri": uri.value, "cause_type": type(error).__name__},
            ) from error
        if len(source) > _MAX_SOURCE_BYTES:
            raise _asset_error(
                "asset source exceeds the bounded loader size",
                phase="build",
                details={"uri": uri.value, "bytes": len(source)},
            )
        source_hash = f"sha256:{sha256(source).hexdigest()}"
        dependency_keys = tuple(item.cache_key for item in dependencies)
        identity = json.dumps(
            {
                "dependencies": dependency_keys,
                "kind": entry.kind.value,
                "loader": _LOADER_VERSION,
                "settings": entry.settings,
                "source_hash": source_hash,
                "uri": uri.value,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
        cache_key = f"sha256:{sha256(identity).hexdigest()}"
        payload = self._load(entry.kind, source)
        artifact = AssetArtifact(
            uri,
            entry.kind,
            source_hash,
            cache_key,
            payload,
            dependency_keys,
        )
        self._persist(artifact)
        return artifact

    @staticmethod
    def _load(kind: AssetKind, source: bytes) -> bytes:
        if kind is AssetKind.PNG:
            texture = decode_png(source)
            return struct.pack(">II", texture.width, texture.height) + texture.rgba8
        if kind is AssetKind.JSON:
            try:
                decoded = json.loads(source)
                return json.dumps(
                    decoded, sort_keys=True, separators=(",", ":"), ensure_ascii=False
                ).encode("utf-8")
            except Exception as error:
                raise _asset_error(
                    "JSON asset could not be decoded",
                    phase="load",
                    details={"cause_type": type(error).__name__},
                ) from error
        if kind is AssetKind.WGSL:
            try:
                return source.decode("utf-8").encode("utf-8")
            except UnicodeError as error:
                raise _asset_error(
                    "WGSL asset must be valid UTF-8",
                    phase="load",
                    details={"cause_type": type(error).__name__},
                ) from error
        return bytes(source)

    def _persist(self, artifact: AssetArtifact) -> None:
        digest = artifact.cache_key.removeprefix("sha256:")
        directory = self._cache_root / digest[:2]
        directory.mkdir(parents=True, exist_ok=True)
        payload_path = directory / f"{digest}.bin"
        metadata_path = directory / f"{digest}.json"
        if payload_path.exists() and metadata_path.exists():
            return
        metadata = json.dumps(
            {
                "cache_key": artifact.cache_key,
                "dependencies": artifact.dependency_keys,
                "kind": artifact.kind.value,
                "protocol": _LOADER_VERSION,
                "source_hash": artifact.source_hash,
                "uri": artifact.uri.value,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        try:
            _atomic_write(payload_path, artifact.payload)
            _atomic_write(metadata_path, metadata)
        except Exception as error:
            raise _asset_error(
                "asset cache artifact could not be persisted",
                phase="cache",
                details={"cause_type": type(error).__name__},
                code="asset.cache_failed",
            ) from error


@dataclass(frozen=True, slots=True)
class PngTexture:
    width: int
    height: int
    rgba8: bytes

    def __post_init__(self) -> None:
        if (
            type(self.width) is not int
            or type(self.height) is not int
            or self.width <= 0
            or self.height <= 0
            or type(self.rgba8) is not bytes
            or len(self.rgba8) != self.width * self.height * 4
        ):
            raise _asset_error(
                "decoded PNG texture has invalid dimensions or payload",
                phase="png",
                details={"field": "texture"},
            )


def decode_png(source: bytes) -> PngTexture:
    """Decode bounded 8-bit, non-interlaced RGB/RGBA PNG bytes to RGBA8."""

    if type(source) is not bytes or not source.startswith(_PNG_SIGNATURE):
        raise _png_error("PNG source has an invalid signature")
    if len(source) > _MAX_SOURCE_BYTES:
        raise _png_error("PNG source exceeds the bounded loader size")
    offset = len(_PNG_SIGNATURE)
    header: tuple[int, int, int] | None = None
    compressed = bytearray()
    ended = False
    while offset < len(source):
        if len(source) - offset < 12:
            raise _png_error("PNG chunk header is truncated")
        length = struct.unpack_from(">I", source, offset)[0]
        chunk_type = source[offset + 4 : offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        crc_end = data_end + 4
        if crc_end > len(source):
            raise _png_error("PNG chunk payload is truncated")
        data = source[data_start:data_end]
        declared_crc = struct.unpack_from(">I", source, data_end)[0]
        if zlib.crc32(chunk_type + data) & 0xFFFFFFFF != declared_crc:
            raise _png_error("PNG chunk CRC is invalid")
        offset = crc_end
        if chunk_type == b"IHDR":
            if header is not None or length != 13:
                raise _png_error("PNG must contain one exact IHDR chunk")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", data
            )
            if (
                not 0 < width <= _MAX_TEXTURE_DIMENSION
                or not 0 < height <= _MAX_TEXTURE_DIMENSION
                or depth != 8
                or color not in (2, 6)
                or compression != 0
                or filtering != 0
                or interlace != 0
            ):
                raise _png_error("PNG format is outside the supported bounded subset")
            header = (width, height, 3 if color == 2 else 4)
        elif chunk_type == b"IDAT":
            if header is None or ended:
                raise _png_error("PNG IDAT ordering is invalid")
            compressed.extend(data)
            if len(compressed) > _MAX_SOURCE_BYTES:
                raise _png_error("PNG compressed payload is too large")
        elif chunk_type == b"IEND":
            if length != 0 or header is None:
                raise _png_error("PNG IEND chunk is invalid")
            ended = True
            break
    if header is None or not ended or not compressed:
        raise _png_error("PNG is missing required chunks")
    width, height, channels = header
    row_bytes = width * channels
    expected = height * (row_bytes + 1)
    decompressor = zlib.decompressobj()
    try:
        raw = decompressor.decompress(bytes(compressed), expected + 1)
    except zlib.error as error:
        raise _png_error("PNG compressed data is invalid") from error
    if len(raw) != expected or not decompressor.eof or decompressor.unused_data:
        raise _png_error("PNG decompressed data length is invalid")
    previous = bytearray(row_bytes)
    pixels = bytearray()
    cursor = 0
    for _ in range(height):
        filter_type = raw[cursor]
        cursor += 1
        encoded = raw[cursor : cursor + row_bytes]
        cursor += row_bytes
        row = _unfilter(filter_type, encoded, previous, channels)
        if channels == 4:
            pixels.extend(row)
        else:
            for index in range(0, row_bytes, 3):
                pixels.extend((*row[index : index + 3], 255))
        previous = row
    return PngTexture(width, height, bytes(pixels))


@dataclass(frozen=True, slots=True)
class TextureAsset:
    """Immutable decoded texture revision, independent of GPU handles."""

    uri: AssetUri
    source_hash: str
    revision: int
    texture: PngTexture

    def __post_init__(self) -> None:
        if (
            type(self.uri) is not AssetUri
            or _CACHE_KEY.fullmatch(self.source_hash) is None
            or type(self.revision) is not int
            or self.revision < 0
            or type(self.texture) is not PngTexture
        ):
            raise _asset_error(
                "texture revision contains invalid immutable metadata",
                phase="hot_reload",
                details={"field": "texture"},
            )


class TextureSlot:
    """Swap immutable CPU texture revisions and retain old data until a safe point."""

    __slots__ = ("_current", "_retired")

    def __init__(self, initial: TextureAsset) -> None:
        if type(initial) is not TextureAsset:
            raise _asset_error(
                "texture slot requires an exact TextureAsset",
                phase="hot_reload",
                details={"actual_type": type(initial).__name__},
            )
        self._current = initial
        self._retired: list[TextureAsset] = []

    @property
    def current(self) -> TextureAsset:
        return self._current

    @property
    def retired(self) -> tuple[TextureAsset, ...]:
        return tuple(self._retired)

    def replace(self, artifact: AssetArtifact) -> TextureAsset:
        """Build and activate a new revision; the previous revision remains retained."""

        if type(artifact) is not AssetArtifact or artifact.kind is not AssetKind.PNG:
            raise _asset_error(
                "texture replacement requires an exact PNG artifact",
                phase="hot_reload",
                details={"field": "artifact"},
            )
        if artifact.uri != self._current.uri or len(artifact.payload) < 8:
            raise _asset_error(
                "texture replacement must preserve logical identity",
                phase="hot_reload",
                details={"field": "uri"},
            )
        width, height = struct.unpack_from(">II", artifact.payload)
        replacement = TextureAsset(
            artifact.uri,
            artifact.source_hash,
            self._current.revision + 1,
            PngTexture(width, height, artifact.payload[8:]),
        )
        self._retired.append(self._current)
        self._current = replacement
        return replacement

    def release_retired(self) -> tuple[TextureAsset, ...]:
        """Release retained CPU revisions after the renderer's completed fence."""

        released = tuple(self._retired)
        self._retired.clear()
        return released


def _unfilter(filter_type: int, encoded: bytes, previous: bytearray, bpp: int) -> bytearray:
    if filter_type > 4:
        raise _png_error("PNG row uses an unsupported filter")
    row = bytearray(len(encoded))
    for index, value in enumerate(encoded):
        left = row[index - bpp] if index >= bpp else 0
        above = previous[index]
        upper_left = previous[index - bpp] if index >= bpp else 0
        if filter_type == 0:
            predictor = 0
        elif filter_type == 1:
            predictor = left
        elif filter_type == 2:
            predictor = above
        elif filter_type == 3:
            predictor = (left + above) // 2
        else:
            predictor = _paeth(left, above, upper_left)
        row[index] = (value + predictor) & 0xFF
    return row


def _paeth(left: int, above: int, upper_left: int) -> int:
    prediction = left + above - upper_left
    left_distance = abs(prediction - left)
    above_distance = abs(prediction - above)
    diagonal_distance = abs(prediction - upper_left)
    if left_distance <= above_distance and left_distance <= diagonal_distance:
        return left
    if above_distance <= diagonal_distance:
        return above
    return upper_left


def _decode_entry(value: object, *, limits: AssetManifestLimits) -> AssetEntry:
    if type(value) is not dict:
        raise _asset_error(
            "asset manifest entry must be an object",
            phase="manifest",
            details={"field": "asset"},
        )
    entry = cast(dict[str, object], value)
    if set(entry) != {"uri", "kind", "source", "settings", "dependencies"}:
        raise _asset_error(
            "asset entry requires exact fields",
            phase="manifest",
            details={"field": "asset"},
        )
    settings_value = entry["settings"]
    dependencies_value = entry["dependencies"]
    if type(settings_value) is not dict or type(dependencies_value) is not list:
        raise _asset_error(
            "asset settings and dependencies use invalid shapes",
            phase="manifest",
            details={"field": "asset"},
        )
    settings = cast(dict[object, object], settings_value)
    dependencies = cast(list[object], dependencies_value)
    if len(settings) > limits.max_settings:
        raise _manifest_limit_error(
            field="settings", actual=len(settings), limit=limits.max_settings
        )
    if len(dependencies) > limits.max_dependencies:
        raise _manifest_limit_error(
            field="dependencies",
            actual=len(dependencies),
            limit=limits.max_dependencies,
        )
    try:
        kind = AssetKind(entry["kind"])
    except (TypeError, ValueError) as error:
        raise _asset_error(
            "asset kind is unsupported",
            phase="manifest",
            details={"field": "kind"},
        ) from error
    return AssetEntry(
        AssetUri(cast(str, entry["uri"])),
        kind,
        cast(str, entry["source"]),
        tuple(cast(dict[str, SettingValue], settings).items()),
        tuple(AssetUri(cast(str, item)) for item in dependencies),
    )


def _require_manifest_limits(value: object) -> AssetManifestLimits:
    if type(value) is not AssetManifestLimits:
        raise _asset_error(
            "asset manifest limits require an exact AssetManifestLimits value",
            phase="configure_manifest",
            details={"actual_type": type(value).__name__},
            code="asset.invalid_manifest_limits",
        )
    return value


def _manifest_bytes(document: str | bytes, limit: int) -> bytes:
    if type(document) is bytes:
        raw = document
    elif type(document) is str:
        try:
            raw = document.encode("utf-8")
        except UnicodeEncodeError as error:
            raise _asset_error(
                "asset manifest text is not UTF-8 encodable",
                phase="decode_manifest",
                details={"cause_type": type(error).__name__},
                code="asset.invalid_manifest_json",
            ) from error
    else:
        raise _asset_error(
            "asset manifest input must be bytes or text",
            phase="decode_manifest",
            details={"actual_type": type(document).__name__},
            code="asset.invalid_manifest_json",
        )
    if len(raw) > limit:
        raise _manifest_limit_error(field="document", actual=len(raw), limit=limit)
    return raw


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_object_key")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> object:
    del value
    raise ValueError("nonfinite_json_number")


def _finite_json_float(value: str) -> float:
    parsed = float(value)
    if not isfinite(parsed):
        raise ValueError("nonfinite_json_number")
    return parsed


def _manifest_limit_error(*, field: str, actual: int, limit: int) -> AssetError:
    return _asset_error(
        "asset manifest exceeds a configured resource limit",
        phase="decode_manifest",
        details={"field": field, "actual": actual, "limit": limit},
        code="asset.manifest_limit_exceeded",
    )


def _require_acyclic(entries: Mapping[AssetUri, AssetEntry]) -> None:
    visited: set[AssetUri] = set()
    active: set[AssetUri] = set()

    def visit(uri: AssetUri) -> None:
        if uri in active:
            raise _asset_error(
                "asset dependencies contain a cycle",
                phase="manifest",
                details={"uri": uri.value},
            )
        if uri in visited:
            return
        active.add(uri)
        for dependency in entries[uri].dependencies:
            visit(dependency)
        active.remove(uri)
        visited.add(uri)

    for uri in sorted(entries):
        visit(uri)


def _root(value: Path) -> Path:
    return value.resolve(strict=True)


def _relative_source(value: object) -> Path:
    if (
        type(value) is not str
        or not value
        or not _utf8_text(value)
        or "\0" in value
        or "\\" in value
    ):
        raise _asset_error(
            "asset source must be a normalized project-relative path",
            phase="manifest",
            details={"field": "source"},
        )
    candidate = Path(value)
    if candidate.is_absolute() or any(part in ("", ".", "..") for part in candidate.parts):
        raise _asset_error(
            "asset source must not be absolute or traverse directories",
            phase="manifest",
            details={"field": "source"},
        )
    return candidate


def _setting(value: object) -> bool:
    return (
        (type(value) is str and _utf8_text(value))
        or type(value) in (int, bool)
        or (type(value) is float and isfinite(value))
    )


def _utf8_text(value: str) -> bool:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    temporary.write_bytes(payload)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _png_error(message: str) -> AssetError:
    return _asset_error(message, phase="png", details={"field": "source"}, code="asset.png_invalid")


def _asset_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
    code: str = "asset.invalid_value",
) -> AssetError:
    return AssetError(
        message,
        code=code,
        subsystem="asset",
        phase=phase,
        details=details,
    )
