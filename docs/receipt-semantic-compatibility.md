# Receipt semantic-diff and diagnostic compatibility

M23 fixes an explicit evolution policy for the semantic changes and diagnostics
inside `ludoweave.receipt/1`. The policy is independent of the current Python
implementation and does not promote the receipt protocol or its exports from
`experimental`.

The normative machine-readable contract is
`tests/fixtures/receipt_semantics_v1/contracts.json`. Runtime code does not load
that repository fixture.

## Protocol rule

Within `ludoweave.receipt/1`, exact fields, status relationships, ordering, and
documented meanings cannot change in place. Unknown receipt and nested
semantic-diff fields fail closed. A removal, rename, type change, ordering
change, presence change, or semantic reinterpretation requires a new receipt
protocol identity such as `ludoweave.receipt/2` and a separate decision.

The exact root semantic-diff fields are:

1. `created_entities`, `destroyed_entities`, and `changed_entities`;
2. `components_added`, `components_removed`, and `components_changed`;
3. `resources_changed`;
4. `allocator` and `epochs`; and
5. `completed_ticks_before` and `completed_ticks_after`.

Committed and dry-run receipts contain a semantic diff. Rejected receipts have
`changes: null` and never expose partial staged changes. An equivalent dry run
and commit produce equal semantic diffs even though their root hash/status
relationships differ.

## Semantic meaning and ordering

The diff describes the net comparison of engine-produced authoritative before
and after images. It does not expose component or resource values.

- Entity identities sort by numeric index and generation.
- Component records sort by entity and then component type UUID; changed field
  names sort lexicographically.
- Resource records and table epochs sort by type UUID.
- Allocator slot records sort by slot index.
- Created and destroyed identities do not also appear in `changed_entities`.
- Same-value or reverted writes may advance epochs while reporting no changed
  value fields. Epochs are observable mutation metadata, not value snapshots.

Record field sets are exact. Component changes contain `entity`, `type_id`,
`fields`, `before_epoch`, and `after_epoch`. Resource changes contain
`type_id`, presence booleans, and `value_changed`. Allocator and epoch objects
retain their current exact nested field sets.

## Diagnostic evolution

`ReceiptDiagnostic.code` is the machine-readable identity. The current built-in
transaction service can emit these top-level rejection codes:

- `world.hash.unsupported_algorithm`
- `world.transaction.apply_failed`
- `world.transaction.limit_exceeded`
- `world.transaction.stale_hash`
- `world.transaction.validation_failed`
- `world.transaction.world_mismatch`

An existing code cannot be removed, reused, or assigned a different meaning
within receipt protocol v1. A new well-formed code is additive: readers must
preserve the rejected receipt status and use an unknown-code fallback rather
than treating rejection as success.

The `phase`, `message`, and `details` fields remain structurally required, but
they are diagnostic metadata rather than compatibility identities. `phase` is
advisory, `message` is human-readable prose that must not be parsed for machine
decisions, and `details` is a sanitized scalar extension map whose keys may be
added or omitted. Consumers must not execute or grant authority to any of
those values.

## Installed evidence

Run:

```console
python examples/receipt_semantic_compatibility.py
```

The example emits one deterministic
`ludoweave.evaluation.receipt-semantic-compatibility/1` JSON document. It uses
fresh in-memory worlds and installed public APIs to prove:

- every semantic-diff change family and exact nested field set;
- equal dry-run/commit diffs and rejected-receipt null changes;
- all six current top-level rejection codes;
- fail-closed missing, unknown, and incompatible protocol fields; and
- successful bounded decoding of changed diagnostic metadata and a future
  well-formed diagnostic code.

The evidence contains identities, field names, policy tokens, statuses, codes,
and package version only. It contains no world hash, state value, path,
environment value, timing, credential, or provider message.

## Stability boundary

RFC-0006 satisfies only RFC-0003 gate 5. The cross-version corpus is still gate
1 and remains false: all committed fixtures and evidence come from
`0.1.0a1`. External consumer feedback and a supported deprecation-capable
feature-release channel also remain absent. The command, transaction, and
receipt surfaces therefore remain experimental.

M23 adds no runtime module, public export, operation, handler, receipt field,
migration, dependency, lock change, package version, workflow job, tag,
release, or publication.
