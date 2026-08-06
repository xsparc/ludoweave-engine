# Bounded receipt reader

M21 adds a public, resource-bounded reader for the existing
`ludoweave.receipt/1` document. It does not change that wire format or promote
any command/receipt API from `experimental`.

## Public surface

```python
from ludoweave.world import ReceiptLimits, TransactionReceipt

receipt = TransactionReceipt.from_json(receipt_bytes)
same_receipt = TransactionReceipt.from_mapping(receipt.as_dict())
assert same_receipt.canonical_bytes() == receipt.canonical_bytes()
```

`from_json` accepts `str` or UTF-8 `bytes`. `from_mapping` accepts a decoded
JSON-domain object, recursively validates and detaches it, and retains no
reference to caller-owned containers. Both return immutable receipt, outcome,
diagnostic, and semantic-diff value objects.

`ReceiptLimits` is frozen and slotted. Its defaults are:

| Limit | Default |
| --- | ---: |
| encoded bytes | 1,048,576 |
| nesting depth | 32 |
| JSON nodes | 100,000 |
| items in one collection | 10,000 |
| bytes in one string | 262,144 |
| command outcomes | 1,024 |
| diagnostics | 64 |
| scalar details per diagnostic | 64 |
| aliases | 1,024 |
| semantic-diff records | 100,000 |

Every limit must be a positive integer. Callers may supply a smaller
`ReceiptLimits` value to either reader. Limits constrain parsing and memory
work; they do not authorize a transaction or verify that a receipt came from a
trusted authority.

## Validation

The reader requires the exact v1 fields at every object layer. It rejects
missing and unknown fields, duplicate JSON keys, invalid UTF-8, non-finite
numbers, invalid canonical float tags, unsupported JSON types, non-canonical
entity/UUID/hash identities, duplicate outcome/alias/change identities, and
configured limit violations.

It also validates relationships that make a receipt meaningful:

- every command outcome has the receipt status and a unique command ID;
- completed ticks and semantic epochs never move backward;
- `committed` receipts have changes, no proposed hash, and no diagnostics;
- `dry_run` receipts preserve the live hash/tick, include a proposed hash and
  changes, and contain no diagnostics;
- `rejected` receipts preserve the live hash/tick, have no proposed hash,
  aliases, or changes, and include at least one diagnostic;
- root and semantic-diff tick boundaries agree; and
- component, resource, allocator, and epoch changes have role-correct shapes.

The reader reconstructs only detached evidence. It does not apply a receipt,
mutate a world, verify a signature, authenticate an actor, resolve a provider,
or trust diagnostic messages as commands.

## Failures

Expected failures are structured `LudoWeaveError` subclasses:

- `ReceiptDecodeError` with `world.receipt.malformed` for schema or invariant
  failures;
- `ReceiptDecodeError` with `world.receipt.oversized` for JSON byte/tree/string
  or semantic limits;
- `ReceiptDecodeError` with `world.receipt.invalid_limits` for invalid reader
  configuration; and
- `IncompatibleReceiptError` with `world.receipt.incompatible` for any protocol
  other than `ludoweave.receipt/1`.

Errors expose bounded field/role/count context and chain nested canonical or
command-schema failures without copying receipt values into the message.

## Compatibility baseline

`tests/fixtures/receipt_v1` freezes committed, dry-run, and rejected documents
produced by `0.1.0a1`, with exact byte counts and SHA-256 digests in
`ludoweave.compatibility.receipt-corpus/1`. Current tests prove the M21 reader
can decode and reproduce those bytes.

This is a **single-version baseline**, not cross-version evidence. RFC-0003's
cross-version gate remains false until a later supported package version reads
these unchanged fixtures under a documented compatibility policy. The fixture
manifest deliberately contains no `target_version` or `compatible_versions`
claim.

Run the installed evidence example from source or the release sample bundle:

```console
python receipt_reader.py
```

It emits sanitized `ludoweave.example.receipt-reader/1` JSON covering all three
statuses, mapping/wire round trips, exact failure codes, default bounds, and the
single-version non-claim. It prints no state hash, world value, path,
environment fact, timing, credential, or provider diagnostic.

## Threading and ownership

Reader calls are synchronous, side-effect free, and create a new detached
object graph. They use no global mutable registry, file, subprocess, thread,
listener, network connection, backend, or ambient configuration. Immutable
decoded receipts can be shared by callers under normal Python object rules;
the reader itself makes no free-threaded execution guarantee beyond the
project's standard CPython baseline.
