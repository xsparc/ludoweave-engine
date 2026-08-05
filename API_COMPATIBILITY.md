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

Plugin manifest protocol `ludoweave.plugin-manifest/1` is persistent under
RFC-0002. A breaking wire change requires another protocol identifier and RFC;
the v1 fields and fingerprint semantics are not reinterpreted in place.

Component UUIDs are persistent identities and released versions never move
backward. Compatible schema evolution keeps explicit adjacent migrations. A
breaking persistent-format, stability-policy, security-boundary, backend, or
governance change requires an RFC under `GOVERNANCE.md`.
