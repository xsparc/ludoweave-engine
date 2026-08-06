# Built-in operation argument compatibility

M22 records an explicit evolution policy for the seven built-in version-1
operation argument contracts. It does not add an operation or change runtime
validation. The normative decision is
[RFC-0005](rfcs/0005-built-in-operation-argument-compatibility.md).

## Exact v1 contracts

| Operation | Required arguments | Optional arguments |
| --- | --- | --- |
| `component.add` | `component`, `entity` | none |
| `component.patch` | `changes`, `entity`, `type_id`, `version` | none |
| `component.remove` | `entity`, `type_id` | none |
| `entity.destroy` | `entity` | none |
| `entity.spawn` | `components` | `alias` |
| `resource.patch` | `type_id`, `value`, `version` | none |
| `world.tick` | `count` | none |

Every object is exact: unknown fields are rejected. Entity references are
either `{alias}` or `{generation, index}`. Component payloads require
`type_id`, `values`, and `version`; the values object must exactly match the
registered component schema after any registered forward migration. Every
current field remains required in the persistent values object even when the
Python dataclass field has an authoring default; registered defaults do not
silently fill persistent payload omissions.
`component.patch` changes at least one exact registered field at the current
schema version. `resource.patch` targets a registered authoritative state
resource at its current schema version. `world.tick` accepts the exact integer
`1` at a transaction-safe point.

The machine-readable baseline is
`tests/fixtures/operation_arguments_v1/contracts.json`. Its operation order,
required/optional fields, semantic-rule identifiers, byte size, and SHA-256
digest are checked in tests. It is repository compatibility evidence, not a
runtime manifest or discovery source.

## Evolution policy

- An existing `(operation, operation_version)` identity never changes its
  required fields, optional fields, unknown-field behavior, or stated semantic
  rules in place.
- A breaking argument change uses a new operation version. A reader never
  silently interprets that version as v1.
- A new operation identity is additive and does not alter existing identities.
- Unknown fields remain rejected so a misspelled or future argument cannot be
  silently ignored by an older engine.
- Deprecation of a supported operation version requires at least one supported
  feature release carrying the notice after the affected surface reaches
  preview. The current alpha has no such release channel, so no removal is
  authorized by this policy.

Component and resource schema evolution remains governed by their persistent
UUIDs, explicit positive versions, and adjacent migrations. Those migrations
do not reinterpret the surrounding operation argument object.

## Installed evidence

From a source checkout or version-matched sample bundle, run:

```console
python operation_argument_compatibility.py
```

The composition applies one valid transaction for every built-in operation,
then proves missing-required, unexpected-field, and defaulted-component-field
omission rejection on fresh worlds.
It emits one deterministic
`ludoweave.evaluation.operation-argument-compatibility/1` JSON document. The
strict validator accepts only the exact seven contracts, policy, statuses, and
engine-owned diagnostic code.

The report contains no world values or hashes, exception messages, paths,
environment facts, credentials, or timings. It is exercised from source, an
isolated dependency-free wheel, and the release sample bundle.

## Compatibility boundary

This satisfies only the operation-argument-policy gate in RFC-0003. The
evidence uses one package version and project-owned implementations. It does
not prove cross-version readability, external adoption, receipt semantic-diff
or diagnostic-code evolution, or a supported deprecation release channel.
Command, transaction, and receipt exports therefore remain experimental.

The composition creates fresh in-memory worlds synchronously and performs no
filesystem read, discovery, dynamic import, installation, subprocess,
networking, provider selection, or global registration. M22 adds no runtime
API, wire format, dependency, lock change, package version, or CI job.
