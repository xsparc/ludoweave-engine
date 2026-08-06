# API compatibility and stability

LudoWeave `0.1.0a1` is a community alpha. No Python symbol or persistent wire
format is implicitly stable.

## Supported public surface

The supported Python surface is the exact set of names listed by `__all__` in
an exported package/module. Each such module exposes `__stability__`, a mapping
whose keys exactly equal `__all__` and whose values are one of:

- `experimental`: public for testing; may change or be removed in a minor alpha
  without a deprecation period;
- `preview`: intended to stabilize; incompatible removal requires a documented
  deprecation in at least one feature release;
- `stable`: governed by semantic-versioning compatibility and the published
  deprecation policy.

`internal` code has no compatibility promise and is not listed in `__all__`.
Importing a non-exported name from an implementation module does not make that
name public. The sole concrete-adapter entry point is explicitly exported from
`ludoweave.render.backends.wgpu`; provider-native objects are still forbidden
from its engine-facing API.

Exports introduced through M11 are `experimental`. The M12
`ludoweave.plugins` exports are the first `preview` surface under RFC-0002: an
incompatible removal requires a documented deprecation in at least one feature
release. CI imports every exporting module, requires exact export/metadata
agreement, validates the allowed vocabulary, and checks that every named export
exists. Adding or removing a public export must update its module metadata,
documentation, tests, and changelog.

## Package versions

Package releases use PEP 440 versions. Before `1.0`, experimental and preview
surfaces can change between alpha/minor versions as stated above. Stable symbols,
if introduced before `1.0`, still receive the stable policy; a breaking change
requires the next permitted major version and an accepted RFC.

Deprecations identify the replacement and earliest removal version in the API
docs and changelog. Stable removals require at least one non-yanked feature
release carrying the deprecation unless an actively exploited vulnerability
requires an emergency exception documented in a security advisory.

## Persistent protocols and assets

Command, receipt, authority, snapshot, replay, agent, and MCP protocol revisions
are versioned independently from the Python package. Their documented readers
determine compatibility. Package-version changes do not silently reinterpret
canonical bytes. The alpha snapshot/replay policy remains deliberately strict
where the protocol documents require an exact engine version.

RFC-0003 retains the command, transaction, and receipt Python/wire surfaces as
experimental after M20's installed readiness audit. Preview promotion requires
the complete cross-version corpus, external feedback, operation-argument,
receipt-reader/diff/diagnostic, and supported-release-channel gate; same-version
conformance alone does not create a deprecation promise.

RFC-0004 adds a bounded experimental `TransactionReceipt` reader and freezes
exact `0.1.0a1` receipt/1 fixtures. This satisfies the reader-and-bounds gate
only. The fixtures are a single-version baseline, so cross-version
compatibility and preview status remain unproven. RFC-0006 later defines
diagnostic/diff evolution without turning those fixtures into cross-version
history.
Future fixture checks preserve the historical bytes rather than rewriting them
to match new behavior.

RFC-0005 freezes every built-in `(operation, operation_version)` v1 argument
identity: required/optional fields and semantic rules do not change in place,
unknown fields are rejected, breaking changes use a new operation version, and
new operation identities are additive. This satisfies the operation-policy
gate only.

RFC-0006 freezes receipt-v1 semantic-diff field sets, presence, ordering, and
meanings. Existing diagnostic-code meanings are fixed; new well-formed codes
are additive, while phase/message/detail metadata remains non-authoritative.
This satisfies the receipt-policy gate only. Cross-version history, external
feedback, and a supported release channel remain incomplete.

RFC-0007 adds an offline admission harness that preserves exact historical
receipt identities, requires a different installed reader version, and requires
supported-release records for every observed version. The current corpus has
only `0.1.0a1` and no release records, so the cross-version gate remains false.

Plugin manifest protocol `ludoweave.plugin-manifest/1` is persistent under
RFC-0002. A breaking wire change requires another protocol identifier and RFC;
the v1 fields and fingerprint semantics are not reinterpreted in place.

Component UUIDs are persistent identities and released versions never move
backward. Compatible schema evolution keeps explicit adjacent migrations. A
breaking persistent-format, stability-policy, security-boundary, backend, or
governance change requires an RFC under `GOVERNANCE.md`.
