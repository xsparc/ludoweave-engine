"""Validate a bounded M13 rollback-readiness evidence document."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from os import fstat
from pathlib import Path
from stat import S_ISREG
from typing import cast

from ludoweave import __version__
from ludoweave.world import JsonLimits, canonical_loads

_SCHEMA = "ludoweave.evaluation.rollback-readiness/1"
_MAX_DOCUMENT_BYTES = 64 * 1024
_MAX_TICKS = 600
_HASH_PREFIX = "sha256:"
_JSON_LIMITS = JsonLimits(
    max_bytes=_MAX_DOCUMENT_BYTES,
    max_depth=8,
    max_nodes=128,
    max_collection_items=32,
    max_string_bytes=256,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    arguments = parser.parse_args(argv)
    artifact = arguments.artifact
    path_status = artifact.stat()
    if not S_ISREG(path_status.st_mode):
        raise ValueError("readiness artifact must be a regular file")
    if not 1 <= path_status.st_size <= _MAX_DOCUMENT_BYTES:
        raise ValueError("readiness artifact size is outside the accepted bound")
    with artifact.open("rb") as stream:
        file_status = fstat(stream.fileno())
        if not S_ISREG(file_status.st_mode):
            raise ValueError("readiness artifact must be a regular file")
        if not 1 <= file_status.st_size <= _MAX_DOCUMENT_BYTES:
            raise ValueError("readiness artifact size is outside the accepted bound")
        document_bytes = stream.read(_MAX_DOCUMENT_BYTES + 1)
    if not document_bytes or len(document_bytes) > _MAX_DOCUMENT_BYTES:
        raise ValueError("readiness artifact size is outside the accepted bound")
    decoded: object = canonical_loads(document_bytes, limits=_JSON_LIMITS)
    validate(decoded)
    print("rollback readiness evidence valid")
    return 0


def validate(value: object) -> None:
    """Reject incomplete, admitted, unsanitized, or inconsistent evidence."""

    document = _object(value, field="document")
    _exact_fields(
        document,
        {
            "decision",
            "gates",
            "hashes",
            "ludoweave_version",
            "metrics",
            "proof",
            "schema",
            "status",
            "transport_implemented",
            "work",
        },
        field="document",
    )
    if type(document["schema"]) is not str or document["schema"] != _SCHEMA:
        raise ValueError("readiness schema is incompatible")
    if (
        type(document["status"]) is not str
        or document["status"] != "deferred"
        or type(document["decision"]) is not str
        or document["decision"] != "defer-network-rollback"
    ):
        raise ValueError("readiness decision must remain deferred")
    if document["transport_implemented"] is not False:
        raise ValueError("readiness evidence cannot claim a transport")
    version = document["ludoweave_version"]
    if type(version) is not str or version != __version__:
        raise ValueError("readiness version does not match this validator")

    proof = _object(document["proof"], field="proof")
    _exact_fields(
        proof,
        {
            "correction_changed_state",
            "correction_checkpoints_verified",
            "correction_repeatable",
            "input_rehydration_required",
            "lineage_verified",
            "parent_checkpoints_verified",
            "parent_repeatable",
        },
        field="proof",
    )
    if any(proof[field] is not True for field in proof):
        raise ValueError("every local readiness proof must be true")

    gates = _object(document["gates"], field="gates")
    expected_gates = {
        "bounded_runtime_budget": False,
        "canonical_tick_inputs": False,
        "cross_platform_loss_simulation": False,
        "local_branch_lineage": True,
        "local_repeatable_resimulation": True,
        "transport_security": False,
        "versioned_network_snapshot_protocol": False,
    }
    if set(gates) != set(expected_gates) or any(
        gates[field] is not expected for field, expected in expected_gates.items()
    ):
        raise ValueError("readiness admission gates are incomplete or inconsistent")

    hashes = _object(document["hashes"], field="hashes")
    _exact_fields(hashes, {"corrected_final", "parent_final", "parent_timeline"}, field="hashes")
    corrected_hash = _hash(hashes["corrected_final"], field="corrected_final")
    parent_hash = _hash(hashes["parent_final"], field="parent_final")
    _hash(hashes["parent_timeline"], field="parent_timeline")
    if corrected_hash == parent_hash:
        raise ValueError("corrected and parent final hashes must differ")

    work = _object(document["work"], field="work")
    _exact_fields(
        work,
        {
            "branch_batches",
            "branch_checkpoints",
            "branch_tick",
            "parent_batches",
            "parent_checkpoints",
            "ticks",
        },
        field="work",
    )
    ticks = _integer(work["ticks"], field="ticks", minimum=2, maximum=_MAX_TICKS)
    branch_tick = _integer(work["branch_tick"], field="branch_tick", minimum=1, maximum=ticks - 1)
    parent_batches = _integer(
        work["parent_batches"], field="parent_batches", minimum=1, maximum=ticks
    )
    branch_batches = _integer(
        work["branch_batches"], field="branch_batches", minimum=1, maximum=ticks
    )
    parent_checkpoints = _integer(
        work["parent_checkpoints"],
        field="parent_checkpoints",
        minimum=2,
        maximum=ticks + 1,
    )
    branch_checkpoints = _integer(
        work["branch_checkpoints"],
        field="branch_checkpoints",
        minimum=2,
        maximum=ticks + 1,
    )
    if (
        parent_batches != ticks
        or branch_batches != ticks - branch_tick
        or parent_checkpoints != parent_batches + 1
        or branch_checkpoints != branch_batches + 1
    ):
        raise ValueError("readiness work counts do not match the branch boundary")

    metrics = _object(document["metrics"], field="metrics")
    _exact_fields(
        metrics,
        {"branch_timeline_bytes", "parent_snapshot_bytes", "parent_timeline_bytes"},
        field="metrics",
    )
    for field in metrics:
        _integer(metrics[field], field=field, minimum=1, maximum=64 * 1024 * 1024)


def _object(value: object, *, field: str) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object with string keys")
    mapping = cast(Mapping[object, object], value)
    if any(type(key) is not str for key in mapping):
        raise ValueError(f"{field} must be an object with string keys")
    return {cast(str, key): item for key, item in mapping.items()}


def _exact_fields(value: Mapping[str, object], expected: set[str], *, field: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{field} fields are incomplete or unknown")


def _hash(value: object, *, field: str) -> str:
    if (
        type(value) is not str
        or not value.startswith(_HASH_PREFIX)
        or len(value) != len(_HASH_PREFIX) + 64
        or any(character not in "0123456789abcdef" for character in value[len(_HASH_PREFIX) :])
    ):
        raise ValueError(f"{field} must be a lowercase SHA-256 identifier")
    return value


def _integer(value: object, *, field: str, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{field} is outside the accepted integer bound")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
