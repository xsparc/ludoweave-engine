"""Frozen receipt/1 single-version baseline for future cross-version checks."""

from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.world import RECEIPT_PROTOCOL, ReceiptStatus, TransactionReceipt, canonical_loads

_ROOT = Path(__file__).parents[2]
_FIXTURES = _ROOT / "tests" / "fixtures" / "receipt_v1"
_EXPECTED = (
    (
        "committed.json",
        "committed",
        1987,
        "d51548b17218a1e2c439a2376fbb017ff0a2fa5ed6c9061637e63865085a07fc",
    ),
    (
        "dry_run.json",
        "dry_run",
        2046,
        "04adf1d88a3e2607e900a27809ed41ccba64e85d0f4e1ee4d6361b3397204057",
    ),
    (
        "rejected.json",
        "rejected",
        789,
        "afbc64d93e92a4b52041a10687e78b51f5eacfb3d4bf50870512ce77960d5ebf",
    ),
)


def test_receipt_v1_manifest_is_an_exact_single_version_baseline() -> None:
    manifest = cast(dict[str, object], canonical_loads((_FIXTURES / "manifest.json").read_bytes()))

    assert set(manifest) == {
        "schema",
        "source_package",
        "source_version",
        "receipt_protocol",
        "evidence_level",
        "fixtures",
    }
    assert manifest["schema"] == "ludoweave.compatibility.receipt-corpus/1"
    assert manifest["source_package"] == "ludoweave"
    assert manifest["source_version"] == "0.1.0a1"
    assert manifest["receipt_protocol"] == RECEIPT_PROTOCOL
    assert manifest["evidence_level"] == "single-version-baseline"
    entries = cast(list[dict[str, object]], manifest["fixtures"])
    assert (
        tuple(
            (entry["file"], entry["status"], entry["bytes"], entry["sha256"]) for entry in entries
        )
        == _EXPECTED
    )


def test_every_frozen_receipt_is_exact_and_readable() -> None:
    for filename, status, size, digest in _EXPECTED:
        raw = (_FIXTURES / filename).read_bytes()
        decoded = TransactionReceipt.from_json(raw)

        assert len(raw) == size
        assert sha256(raw).hexdigest() == digest
        assert decoded.protocol == RECEIPT_PROTOCOL
        assert decoded.status is ReceiptStatus(status)
        assert decoded.canonical_bytes() == raw.rstrip(b"\r\n")
        assert TransactionReceipt.from_mapping(decoded.as_dict()) == decoded


def test_frozen_corpus_does_not_claim_cross_version_evidence() -> None:
    manifest = cast(dict[str, object], canonical_loads((_FIXTURES / "manifest.json").read_bytes()))

    assert manifest["evidence_level"] == "single-version-baseline"
    assert "target_version" not in manifest
    assert "compatible_versions" not in manifest
