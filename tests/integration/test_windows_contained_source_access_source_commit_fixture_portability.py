"""Prove the historical probe family explicitly consumes its offline fixture."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as probe,
)

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows probe composition")


def test_probe_uses_temporary_store_not_checkout_history() -> None:
    store = probe._ROOT  # pyright: ignore[reportPrivateUsage]
    assert store != Path(__file__).parents[2]
    assert store.name == "objects.git"
    assert (store / "objects").is_dir()
    assert not (store / "objects/info/alternates").exists()
    snapshot = probe._load_committed_source()  # pyright: ignore[reportPrivateUsage]
    assert snapshot.commit == "734d4eb943c3da7a1a8357ef3e180cac4353cb6b"
    assert (
        snapshot.sha256.hex() == "fa01dae3119f817c62d0b27b0f575642c9837ad5259d79507bd2a1c09c41d2dd"
    )
