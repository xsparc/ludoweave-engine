# RFC-0005: Built-in operation argument compatibility

- **Status:** Accepted
- **Date:** 2026-08-06
- **Decision:** Freeze exact built-in operation/version argument identities and require versioned breaking evolution
- **Related:** [command guide](../commands.md), [compatibility guide](../operation-argument-compatibility.md), [RFC-0003](0003-retain-experimental-command-receipt-contracts.md), [RFC-0004](0004-bounded-receipt-reader-and-v1-baseline.md), [ADR-0008](../adr/0008-versioned-command-envelope-and-canonical-json.md)

## Summary

The seven built-in operation-version-1 argument contracts are exact persistent
identities. Their required and optional fields, unknown-field rejection, and
documented semantic rules cannot change in place. A breaking argument change
uses a new operation version; a new operation identity is additive.

M22 records this policy independently of implementation, freezes a
machine-readable v1 contract, and exercises every valid shape plus missing and
unexpected fields through the installed transaction service. This satisfies
gate 3 of RFC-0003 but does not promote the command, transaction, or receipt
contracts.

## Context

The runtime already selects handlers by operation ID and positive operation
version and rejects unknown fields. Before M22, tests documented current
behavior but did not state how those shapes may evolve. That left consumers
unable to distinguish an accidental in-place change from an intentional new
version.

Compatibility must be stricter than accepting arbitrary extension fields.
Ignoring a future or misspelled mutation argument can produce a valid receipt
for unintended state. Exact objects make an older engine fail closed.

## Decision

For every built-in `(operation, operation_version)` identity:

1. required and optional argument fields are immutable;
2. unknown fields are rejected;
3. semantic rule identifiers recorded in the v1 contract are immutable;
4. a breaking change requires a new positive operation version;
5. a new operation ID is additive and does not reinterpret an old ID; and
6. once an affected surface is preview, deprecation requires at least one
   supported feature release before removal.

The current seven v1 identities remain `component.add`, `component.patch`,
`component.remove`, `entity.destroy`, `entity.spawn`, `resource.patch`, and
`world.tick`. Component/resource payload versions and migrations evolve their
registered values; they do not alter the surrounding operation argument shape.

The repository fixture is normative compatibility evidence. Runtime code does
not load it. The installed example composes trusted public APIs and its strict
validator proves the recorded contract matches current behavior.

RFC-0003's readiness report advances to schema `/3`. Gates 3 and 4 are true;
cross-version fixtures, external consumer feedback, semantic-diff/diagnostic
policy, and a supported feature-release channel remain false. All six remain
required for preview reconsideration.

## Security and determinism

Exact field rejection prevents silent downgrade and typo acceptance. Runtime
schema, canonical JSON, transaction size, and receipt limits continue to bound
untrusted input. The policy adds no evaluator, implementation locator,
discovery, loader, transport, or provider object.

Evidence uses fresh deterministic in-memory authorities and returns only
identities, versions, policy tokens, statuses, diagnostic codes, and the
installed package version. It contains no canonical state, hashes, paths,
environment values, timings, or exception messages.

## Consequences

- Consumers can key compatibility on exact operation ID and version.
- Old engines fail closed on fields they do not understand.
- Breaking evolution spends a new operation version and must retain/document
  prior behavior according to the stability and release policy then in force.
- M22 changes no handler, public export, command/receipt wire field,
  dependency, lock, package version, or CI topology.
- Same-version evidence is not cross-version history or external adoption.

## Alternatives considered

- **Allow unknown fields for forward compatibility.** Rejected because ignored
  mutation intent is unsafe and not evidence of semantic compatibility.
- **Change v1 in place while APIs are experimental.** Rejected because the
  versioned persistent identity would cease to communicate meaning.
- **Add a generic schema language to runtime.** Rejected because the existing
  typed handlers already validate the behavior and M22 needs policy/evidence,
  not a second execution model.
- **Promote command/receipt contracts now.** Rejected because four independent
  RFC-0003 gates remain incomplete.
