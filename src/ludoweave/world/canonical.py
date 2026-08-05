"""Bounded canonical JSON encoding for persistent world documents.

Canonical JSON v1 is a deliberately small D1 contract. Object keys are sorted,
UTF-8 is used directly, insignificant whitespace is omitted, duplicate keys are
rejected, and non-finite numbers are forbidden. It does not claim that
arbitrary floating-point calculations are bit-identical across platforms.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import cast

from ludoweave.world.errors import CanonicalJsonError

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type FrozenJsonValue = JsonScalar | tuple[FrozenJsonValue, ...] | Mapping[str, FrozenJsonValue]


@dataclass(frozen=True, slots=True)
class JsonLimits:
    """Resource limits applied before a document enters a domain schema."""

    max_bytes: int = 1_048_576
    max_depth: int = 32
    max_nodes: int = 100_000
    max_collection_items: int = 10_000
    max_string_bytes: int = 262_144

    def __post_init__(self) -> None:
        for name in (
            "max_bytes",
            "max_depth",
            "max_nodes",
            "max_collection_items",
            "max_string_bytes",
        ):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise CanonicalJsonError(
                    "canonical JSON limits must be positive integers",
                    code="world.invalid_json_limits",
                    subsystem="world",
                    phase="configure",
                    details={"field": name, "actual_type": type(value).__name__},
                )


DEFAULT_JSON_LIMITS = JsonLimits()
_FLOAT_TAG = "$ludoweave.float"


def canonical_loads(
    document: str | bytes,
    *,
    limits: JsonLimits = DEFAULT_JSON_LIMITS,
) -> JsonValue:
    """Decode one bounded JSON value while rejecting duplicate object keys."""

    if type(document) is bytes:
        raw = document
        if len(raw) > limits.max_bytes:
            raise _json_error(
                "JSON document exceeds the byte limit",
                phase="decode",
                details={"limit": limits.max_bytes, "actual": len(raw)},
            )
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise _json_error(
                "JSON document must be valid UTF-8",
                phase="decode",
                details={"reason": "invalid_utf8"},
            ) from error
    elif type(document) is str:
        text = document
        try:
            encoded_length = len(text.encode("utf-8"))
        except UnicodeEncodeError as error:
            raise _json_error(
                "JSON document must contain valid Unicode scalar text",
                phase="decode",
                details={"reason": "invalid_unicode"},
            ) from error
        if encoded_length > limits.max_bytes:
            raise _json_error(
                "JSON document exceeds the byte limit",
                phase="decode",
                details={"limit": limits.max_bytes, "actual": encoded_length},
            )
    else:
        raise _json_error(
            "JSON document must be text or bytes",
            phase="decode",
            details={"actual_type": type(document).__name__},
        )

    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_without_duplicates,
            parse_constant=_reject_nonfinite_token,
        )
    except CanonicalJsonError:
        raise
    except (json.JSONDecodeError, ValueError, RecursionError) as error:
        raise _json_error(
            "JSON document is malformed",
            phase="decode",
            details={"reason": "malformed_json"},
        ) from error
    checked_wire = validate_json_value(value, limits=limits)
    return validate_json_value(_decode_wire_value(checked_wire), limits=limits)


def canonical_dumps(
    value: object,
    *,
    limits: JsonLimits = DEFAULT_JSON_LIMITS,
) -> bytes:
    """Encode one validated value as canonical UTF-8 JSON bytes."""

    checked = validate_json_value(value, limits=limits)
    wire_value = _encode_wire_value(checked)
    try:
        encoded = json.dumps(
            wire_value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError) as error:
        raise _json_error(
            "value could not be encoded as canonical JSON",
            phase="encode",
            details={"reason": "encoding_failed"},
        ) from error
    if len(encoded) > limits.max_bytes:
        raise _json_error(
            "canonical JSON output exceeds the byte limit",
            phase="encode",
            details={"limit": limits.max_bytes, "actual": len(encoded)},
        )
    return encoded


def validate_json_value(
    value: object,
    *,
    limits: JsonLimits = DEFAULT_JSON_LIMITS,
) -> JsonValue:
    """Return a detached JSON value after recursive type and size validation."""

    nodes = [0]

    def visit(candidate: object, depth: int) -> JsonValue:
        nodes[0] += 1
        if nodes[0] > limits.max_nodes:
            raise _json_error(
                "JSON value exceeds the node limit",
                phase="validate",
                details={"limit": limits.max_nodes},
            )
        if depth > limits.max_depth:
            raise _json_error(
                "JSON value exceeds the nesting limit",
                phase="validate",
                details={"limit": limits.max_depth},
            )
        if candidate is None or type(candidate) is bool:
            return candidate
        if type(candidate) is int:
            integer = candidate
            if integer < -(2**63) or integer > 2**63 - 1:
                raise _json_error(
                    "JSON integers must fit a signed 64-bit value",
                    phase="validate",
                    details={"reason": "integer_out_of_range"},
                )
            return integer
        if type(candidate) is float:
            number = candidate
            if not isfinite(number):
                raise _json_error(
                    "JSON numbers must be finite",
                    phase="validate",
                    details={"reason": "nonfinite_number"},
                )
            return number
        if type(candidate) is str:
            string = candidate
            try:
                size = len(string.encode("utf-8"))
            except UnicodeEncodeError as error:
                raise _json_error(
                    "JSON strings must contain valid Unicode scalar text",
                    phase="validate",
                    details={"reason": "invalid_unicode"},
                ) from error
            if size > limits.max_string_bytes:
                raise _json_error(
                    "JSON string exceeds the byte limit",
                    phase="validate",
                    details={"limit": limits.max_string_bytes, "actual": size},
                )
            return string
        if isinstance(candidate, Mapping):
            mapping = cast(Mapping[object, object], candidate)
            if len(mapping) > limits.max_collection_items:
                raise _json_error(
                    "JSON object exceeds the item limit",
                    phase="validate",
                    details={"limit": limits.max_collection_items, "actual": len(mapping)},
                )
            result: dict[str, JsonValue] = {}
            for key, item in mapping.items():
                if type(key) is not str:
                    raise _json_error(
                        "JSON object keys must be strings",
                        phase="validate",
                        details={"actual_type": type(key).__name__},
                    )
                checked_key = key
                if checked_key in result:
                    raise _json_error(
                        "JSON object keys must be unique",
                        phase="validate",
                        details={"key": checked_key},
                    )
                visit(checked_key, depth + 1)
                result[checked_key] = visit(item, depth + 1)
            return result
        if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes, bytearray)):
            sequence = cast(Sequence[object], candidate)
            if len(sequence) > limits.max_collection_items:
                raise _json_error(
                    "JSON array exceeds the item limit",
                    phase="validate",
                    details={"limit": limits.max_collection_items, "actual": len(sequence)},
                )
            return [visit(item, depth + 1) for item in sequence]
        raise _json_error(
            "value is outside the canonical JSON domain",
            phase="validate",
            details={"actual_type": type(candidate).__name__},
        )

    try:
        return visit(value, 0)
    except CanonicalJsonError:
        raise
    except Exception as error:
        raise _json_error(
            "value could not be inspected as canonical JSON",
            phase="validate",
            details={"reason": "container_inspection_failed"},
        ) from error


def freeze_json_object(value: object) -> Mapping[str, FrozenJsonValue]:
    """Validate, detach, and recursively freeze a JSON object."""

    checked = validate_json_value(value)
    if not isinstance(checked, dict):
        raise _json_error(
            "command arguments must be a JSON object",
            phase="validate",
            details={"actual_type": type(checked).__name__},
        )
    frozen = _freeze(checked)
    return cast(Mapping[str, FrozenJsonValue], frozen)


def thaw_json(value: FrozenJsonValue) -> JsonValue:
    """Return a detached ordinary JSON value from a frozen value."""

    if isinstance(value, Mapping):
        return {key: thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw_json(item) for item in value]
    return value


def _freeze(value: JsonValue) -> FrozenJsonValue:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _encode_wire_value(value: JsonValue) -> JsonValue:
    if type(value) is float:
        return {_FLOAT_TAG: value.hex()}
    if isinstance(value, dict):
        if _FLOAT_TAG in value:
            raise _json_error(
                "JSON objects may not use the reserved float tag",
                phase="encode",
                details={"key": _FLOAT_TAG},
            )
        return {key: _encode_wire_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_encode_wire_value(item) for item in value]
    return value


def _decode_wire_value(value: JsonValue) -> JsonValue:
    if isinstance(value, dict):
        if _FLOAT_TAG in value:
            if set(value) != {_FLOAT_TAG} or type(value[_FLOAT_TAG]) is not str:
                raise _json_error(
                    "canonical float tag must be the only field and contain text",
                    phase="decode",
                    details={"key": _FLOAT_TAG},
                )
            encoded = cast(str, value[_FLOAT_TAG])
            try:
                decoded = float.fromhex(encoded)
            except ValueError as error:
                raise _json_error(
                    "canonical float tag contains an invalid hexadecimal value",
                    phase="decode",
                    details={"key": _FLOAT_TAG},
                ) from error
            if not isfinite(decoded):
                raise _json_error(
                    "canonical float tag must contain a finite value",
                    phase="decode",
                    details={"key": _FLOAT_TAG},
                )
            return decoded
        return {key: _decode_wire_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_decode_wire_value(item) for item in value]
    return value


def _object_without_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _json_error(
                "JSON document contains a duplicate object key",
                phase="decode",
                details={"key": key},
            )
        result[key] = value
    return result


def _reject_nonfinite_token(token: str) -> object:
    raise _json_error(
        "JSON document contains a non-finite number",
        phase="decode",
        details={"token": token},
    )


def _json_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> CanonicalJsonError:
    return CanonicalJsonError(
        message,
        code="world.invalid_canonical_json",
        subsystem="world",
        phase=phase,
        details=details,
    )
