"""Canonical JSON profile and hostile-input coverage."""

import math
from collections.abc import Iterator, Mapping

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.world import CanonicalJsonError, JsonLimits, canonical_dumps, canonical_loads


def test_mapping_order_and_lexical_number_forms_canonicalize_identically() -> None:
    left = canonical_loads('{"z":1.0,"a":{"b":2,"a":-0.0}}')
    right = canonical_loads('{"a":{"a":-0e0,"b":2},"z":1e0}')

    assert canonical_dumps(left) == canonical_dumps(right)
    assert canonical_dumps(left) == (
        b'{"a":{"a":{"$ludoweave.float":"-0x0.0p+0"},"b":2},'
        b'"z":{"$ludoweave.float":"0x1.0000000000000p+0"}}'
    )


def test_tagged_float_round_trip_preserves_kind_and_signed_zero() -> None:
    encoded = canonical_dumps({"boolean": False, "integer": 0, "negative_zero": -0.0})
    decoded = canonical_loads(encoded)

    assert isinstance(decoded, dict)
    assert type(decoded["boolean"]) is bool
    assert type(decoded["integer"]) is int
    assert type(decoded["negative_zero"]) is float
    assert math.copysign(1.0, decoded["negative_zero"]) == -1.0


@given(
    st.dictionaries(
        st.text(min_size=1).filter(lambda key: key != "$ludoweave.float"),
        st.integers(min_value=-100, max_value=100),
        max_size=20,
    )
)
def test_canonical_encode_decode_is_idempotent(value: dict[str, int]) -> None:
    first = canonical_dumps(value)
    assert canonical_dumps(canonical_loads(first)) == first


@pytest.mark.parametrize(
    "document",
    [
        '{"a":1,"a":2}',
        '{"value":NaN}',
        '{"value":Infinity}',
        "{} trailing",
        "\ufeff{}",
        '{"$ludoweave.float":"nan"}',
        '{"$ludoweave.float":"0x0p+0","extra":1}',
    ],
)
def test_malformed_or_noncanonical_domains_are_rejected(document: str) -> None:
    with pytest.raises(CanonicalJsonError):
        canonical_loads(document)


def test_invalid_utf8_and_lone_surrogate_are_structured_failures() -> None:
    with pytest.raises(CanonicalJsonError) as bytes_error:
        canonical_loads(b'"\xff"')
    assert bytes_error.value.code == "world.invalid_canonical_json"

    with pytest.raises(CanonicalJsonError):
        canonical_loads('"\ud800"')


def test_limits_apply_at_boundary() -> None:
    limits = JsonLimits(
        max_bytes=8,
        max_depth=2,
        max_nodes=4,
        max_collection_items=2,
        max_string_bytes=4,
    )
    assert canonical_loads('{"a":1}', limits=limits) == {"a": 1}

    with pytest.raises(CanonicalJsonError):
        canonical_loads('{"abc":1}', limits=limits)
    with pytest.raises(CanonicalJsonError):
        canonical_dumps({"a": {"b": {"c": 1}}}, limits=limits)
    with pytest.raises(CanonicalJsonError):
        canonical_dumps({"value": 2**63})


def test_python_boundary_rejects_unsupported_values_and_reserved_keys() -> None:
    with pytest.raises(CanonicalJsonError):
        canonical_dumps({"items": {1, 2}})
    with pytest.raises(CanonicalJsonError):
        canonical_dumps({"$ludoweave.float": "user data"})


def test_python_boundary_wraps_hostile_container_inspection() -> None:
    class HostileMapping(Mapping[str, object]):
        def __getitem__(self, key: str) -> object:
            raise KeyError(key)

        def __iter__(self) -> Iterator[str]:
            raise RuntimeError("boom")

        def __len__(self) -> int:
            return 1

    with pytest.raises(CanonicalJsonError) as raised:
        canonical_dumps(HostileMapping())
    assert raised.value.code == "world.invalid_canonical_json"
    assert isinstance(raised.value.__cause__, RuntimeError)
