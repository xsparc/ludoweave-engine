# ADR-0008: Versioned command envelopes and exact canonical JSON

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M2 needs one persistent mutation language for Python services, CLI adapters,
replay, future MCP tools, tests, and possible editor tooling. M1's local
`Commands` and `DeferredEntity` values intentionally contain process identity
and cannot be serialized or attributed. Command bytes must not depend on map
insertion order, wall-clock IDs, Python callables, or backend objects.

Plain JSON also leaves duplicate keys, non-finite numbers, signed zero, number
kind, nesting, and resource limits underspecified. The design example uses a
BLAKE3-shaped hash but does not justify adding a native hashing dependency.

## Decision

Persistent commands use immutable `ludoweave.command/1` envelopes containing
caller-supplied command and transaction IDs, actor attribution, operation ID
and version, optional expected world hash, and bounded JSON arguments. An
immutable `ludoweave.transaction/1` document names a target world and is the
complete transaction boundary. It rejects empty batches, duplicate command
IDs, and mixed transaction, actor, or optimistic-hash identity. Begin/commit/
rollback are not half-open streaming operations in M2.

An explicit immutable `OperationRegistry`, not a global registry or dynamic
import mechanism, indexes `(operation ID, version)` and exposes a SHA-256
fingerprint. Initial identities cover entity, component, authoritative
resource, and tick operations that later M2 slices validate and apply. Scene
operations remain unsupported until a real scene contract exists.

Canonical JSON v1 emits UTF-8 with lexical object-key ordering and no
insignificant whitespace. It rejects duplicate keys, BOM/trailing input,
invalid Unicode scalar text, non-finite values, unsupported objects, and
configured size/depth limits. Integers are signed 64-bit. Finite floats are
canonically encoded as a reserved `$ludoweave.float` object containing
`float.hex()` text, retaining `bool`/`int`/`float` distinctions and signed
zero. Text code points are preserved without implicit Unicode normalization.

State and document hashes use versioned standard-library SHA-256 identifiers.
The engine may support another algorithm later through a compatibility
decision, but M2 does not add BLAKE3 or a compiler/native dependency for it.

## Consequences

- Logically equal accepted maps and number spellings produce identical bytes.
- Command documents cannot request Python evaluation, imports, transports, or
  backend operations.
- Clients must supply stable IDs and respect reserved float-tag objects.
- Canonical bytes are a D1 engine profile and do not overclaim arbitrary
  cross-platform floating-point computation.
- The full typed operation schemas, atomic staging, receipts, state hash,
  snapshot, and replay contracts are separate M2 acceptance slices.

## Alternatives considered

RFC 8785/JCS was not adopted unqualified because the engine must preserve its
explicit number-kind and signed-zero semantics. Ordinary JSON floats were
rejected as too implicit for authoritative values. BLAKE3 was deferred because
the standard library provides SHA-256 without adding a native dependency.
