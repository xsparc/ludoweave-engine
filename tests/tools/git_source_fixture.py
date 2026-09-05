"""Materialize the bounded M220 path proof without relying on checkout history.

This is a deliberately partial test object database, not a clone or provenance
store. It contains the original commit, three path trees, and source
blob only. No other historical files, remotes, hooks, or alternates are used.
"""

from __future__ import annotations

import base64
import hashlib
import json
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, cast

_MANIFEST = Path(__file__).parents[1] / "fixtures/m220_git_objects.json"
_MANIFEST_SHA256 = "07fff6fbece00d150a1dad71425d9b7ea0ebc26778ea5eaeca093f8792448fcd"
_MAX_MANIFEST_BYTES = 16_384
_EXPECTED_OBJECTS = (
    ("734d4eb943c3da7a1a8357ef3e180cac4353cb6b", "commit"),
    ("5575eeeb8123a0eaed9028a6281227b64fdfb73d", "tree"),
    ("1b2b29f1788fb4cfa1d53b252ac62eef7c9f3a50", "tree"),
    ("f3d0421dd1cf2b90d14927f08a390c774cda8baf", "tree"),
    ("10b71fc7d2d555160bf4a2869190a0b3e66d3330", "blob"),
)


class _EncodedObject(TypedDict):
    oid: str
    kind: str
    data: str


class _Manifest(TypedDict):
    schema_version: int
    source_commit: str
    objects: list[_EncodedObject]


@dataclass(frozen=True, slots=True)
class GitFixtureObject:
    """One detached, pinned loose-object payload, including its Git header."""

    oid: str
    content: bytes


def read_m220_objects(manifest: Path = _MANIFEST) -> tuple[GitFixtureObject, ...]:
    """Verify exact fixture bytes and Git identities before any materialization."""

    with manifest.open("rb") as stream:
        raw = stream.read(_MAX_MANIFEST_BYTES + 1)
    if len(raw) > _MAX_MANIFEST_BYTES or hashlib.sha256(raw).hexdigest() != _MANIFEST_SHA256:
        raise ValueError("M220 fixture manifest identity mismatch")
    # Shape and encoding are pinned above, not accepted from arbitrary JSON.
    document = cast(_Manifest, json.loads(raw))
    if document["schema_version"] != 1 or document["source_commit"] != _EXPECTED_OBJECTS[0][0]:
        raise ValueError("M220 fixture descriptor mismatch")
    if tuple((item["oid"], item["kind"]) for item in document["objects"]) != _EXPECTED_OBJECTS:
        raise ValueError("M220 fixture object inventory mismatch")
    objects: list[GitFixtureObject] = []
    for item in document["objects"]:
        payload = base64.b64decode(item["data"], validate=True)
        content = f"{item['kind']} {len(payload)}\0".encode("ascii") + payload
        if hashlib.sha1(content, usedforsecurity=False).hexdigest() != item["oid"]:
            raise ValueError("M220 fixture Git object identity mismatch")
        objects.append(GitFixtureObject(item["oid"], content))
    return tuple(objects)


def materialize_m220_objects(destination: Path, *, manifest: Path = _MANIFEST) -> Path:
    """Create a new caller-owned bare test database; never modify a checkout.

    The caller supplies a fresh path beneath its owned temporary directory and
    owns cleanup. Existing destinations refuse. Missing unrelated historical
    objects are intentional: this database supports only the fixed path proof.
    """

    objects = read_m220_objects(manifest)
    destination.mkdir()  # exist_ok=False also refuses a pre-existing symlink.
    (destination / "objects").mkdir()
    (destination / "refs").mkdir()
    (destination / "HEAD").write_bytes(b"ref: refs/heads/fixture\n")
    (destination / "config").write_bytes(b"[core]\nrepositoryformatversion = 0\nbare = true\n")
    for item in objects:
        directory = destination / "objects" / item.oid[:2]
        directory.mkdir(exist_ok=True)
        (directory / item.oid[2:]).write_bytes(zlib.compress(item.content))
    return destination
