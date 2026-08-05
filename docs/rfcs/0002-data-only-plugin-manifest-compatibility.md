# RFC-0002: Data-only plugin manifests and compatibility checks

- **Status:** Accepted
- **Date:** 2026-08-06
- **Decision:** Adopt preview manifest protocol v1 without discovery or code loading
- **Related:** [adapter guide](../adapter-guide.md), [API status](../api-status.md), [ADR-0002](../adr/0002-dependency-direction-and-backend-isolation.md)

## Summary

M12 introduces `ludoweave.plugin-manifest/1`, a strict canonical data format,
and a deterministic evaluator that answers whether an explicitly supplied set
of manifests is compatible with an explicit engine, CPython, platform, and
policy context. The Python values are preview API. The wire protocol is
versioned independently and will not be silently reinterpreted.

This is not a plugin loader. A manifest cannot name a module, callable, entry
point, path, URL, command, environment variable, credential, or provider
object. The engine does not discover, import, install, resolve, execute, hot
reload, or sandbox plugin code. Trusted application composition roots still
inject implementations explicitly through existing engine-owned protocols.

## Context

The community-alpha adapter guide already asks separately distributed adapters
to declare a bounded LudoWeave version, Python/platform support, stability,
native requirements, and their extension boundary. Until M12 those claims are
prose only. That makes compatibility checks inconsistent and makes dependency
failures appear after application composition.

Entry-point discovery would widen the trust boundary from explicit injection
to ambient installed packages. A general dependency resolver would duplicate
the Python packaging ecosystem and encourage runtime installation. Executable
hooks or project-authored module names would violate the no-eval and data-only
project contracts. M12 therefore standardizes only information and evaluation.

## Manifest v1

Every document is bounded canonical JSON with these exact fields:

- `protocol`: exactly `ludoweave.plugin-manifest/1`;
- `plugin_id`: a lowercase dotted stable identity;
- `plugin_version`: `MAJOR.MINOR.PATCH` with an optional `aN`, `bN`, or `rcN`
  suffix;
- `engine`: inclusive `minimum` and exclusive `maximum_exclusive` release
  bounds using the same syntax;
- `python`: inclusive/exclusive CPython `MAJOR.MINOR` bounds;
- `platforms`: a non-empty unique subset of `linux`, `macos`, and `windows`;
- `capabilities`: a non-empty unique subset of the engine-owned v1 extension
  IDs;
- `determinism`: the plugin's highest claimed `d0`, `d1`, or `d2` tier;
- `native`: an exact boolean policy fact; and
- `requires`: bounded unique plugin identities with half-open version ranges.

The v1 engine-owned capabilities are render backend/device, audio backend,
agent capture/telemetry/test, resource adapter, and simulation tick executor.
The manifest declares a boundary; it does not prove protocol conformance or
authorize a provider. Physics is absent because ADR-0024 deferred that adapter.
New capability vocabulary or fields require a new compatible protocol reader
or a versioned successor rather than accepting arbitrary text.

### Persistent v1 invariants

The following syntax, bounds, ordering, and digest rules are part of protocol
v1 and cannot be changed in place:

- a manifest is at most 65,536 UTF-8 bytes, eight levels, 4,096 nodes, 256
  items in any JSON collection, and 512 UTF-8 bytes in any string;
- `plugin_id` is at most 128 characters and contains at least two dot-separated
  labels; each label matches `[a-z0-9][a-z0-9-]{0,62}` exactly;
- release text is at most 64 characters. Numeric release and prerelease serial
  components are at most 2,147,483,647, leading zeroes are rejected except for
  zero itself, and ordering is numeric `major`, `minor`, `patch`, then
  `a < b < rc < final`, with numeric serial ordering inside a prerelease phase;
- CPython range endpoints are `MAJOR.MINOR`, at most 32 characters, with each
  component at most 2,147,483,647 and the same leading-zero rule;
- platforms contain 1-3 values, capabilities contain 1-16 values, and
  dependencies contain 0-64 values. Every collection is duplicate-free and is
  serialized in its defined lexical identity/value order;
- one check accepts at most 64 manifests and 6,000 issues. Its canonical report
  is at most 4,194,304 bytes, eight levels, 100,000 nodes, 10,000 items in any
  collection, and 512 UTF-8 bytes in any string; and
- canonical integers are signed 64-bit, canonical floats are finite, and all
  text must be valid Unicode encoded as UTF-8.

An individual manifest fingerprint is `sha256:` followed by lowercase SHA-256
hexadecimal over its canonical manifest bytes. For a manifest-set fingerprint,
the canonical bytes of every supplied manifest are sorted lexicographically.
For each item in that order, the digest receives its byte length as an unsigned
eight-byte big-endian integer followed by the bytes themselves. This framing
preserves duplicates without concatenation ambiguity. Issues are ordered by
`plugin_id`, machine code, then canonical issue bytes. A dependency-cycle
fingerprint hashes the canonical JSON array of the component's sorted plugin
identities; each member receives that digest and the component size rather than
an unbounded joined identifier string.

## Compatibility semantics

Evaluation is a pure bounded operation over explicit frozen values. It checks:

1. current engine release is within each half-open engine range;
2. the process is CPython and its major/minor is within each Python range;
3. the selected desktop platform is declared;
4. every capability is enabled by the explicit context;
5. native code is allowed by explicit policy;
6. the declared determinism tier meets the requested minimum;
7. plugin identities are unique;
8. required plugins exist exactly once and satisfy their version ranges; and
9. the dependency graph is acyclic.

All issues have stable machine codes and bounded context. Manifest ordering,
dependency ordering, and collection insertion history do not affect the report
or manifest-set fingerprint. Invalid wire data is a structured error. Valid but
incompatible data is a complete report, not an exception.

The local command `ludoweave plugin check` reads only explicitly named bounded
files. It returns 0 for compatible, 1 for valid but incompatible, and 2 for an
invalid request/document. Output contains normalized compatibility facts and
plugin identities, never source paths or ambient environment values.

## Compatibility promise

The `ludoweave.plugins` Python exports are the project's first `preview`
surface. Incompatible removal requires a documented deprecation in at least one
feature release. Manifest protocol v1 is persistent: future readers may reject
it explicitly or add a versioned migration, but must not reinterpret its fields
or ordering/fingerprint rules in place. A breaking wire change uses another
protocol identifier and an RFC.

Preview status does not make third-party code trusted, deterministic, secure,
or supported. Provider admission still follows the adapter-specific RFC/ADR,
conformance, packaging, ownership, maintenance, and hosted-platform gates.

## Security and ownership

- Manifests are inert data and have strict byte, node, depth, collection, text,
  dependency, and total-plugin limits.
- The plugins package does not use importlib, package metadata discovery,
  subprocesses, networking, dynamic evaluation, or a mutable global registry.
- The CLI owns bounded filesystem reads; paths never enter compatibility data.
- A positive report authorizes only compatibility at the declared metadata
  boundary. Application code must still choose and own an implementation.
- Native permission is explicit and defaults off in the local CLI. It does not
  override RFC-0001 or provider-specific admission decisions.

## Consequences

- Projects and CI can reject obvious environment and dependency mismatches
  before an adapter is composed.
- Third-party packages have one small portable manifest format independent of
  Python object identity and installed-package discovery.
- The engine gains no automatic extensibility or new runtime dependency.
- Manifest authors must update explicit version ranges and dependency records
  as contracts change.
- Compatibility remains a necessary but insufficient gate; conformance and
  trust are deliberately separate.

## Alternatives considered

- **Python packaging entry points.** Rejected because discovery imports ambient
  trust and makes installed environment state part of application composition.
- **Module/callable names in project JSON.** Rejected because project data must
  remain inert and cannot become arbitrary Python execution.
- **Runtime pip installation or dependency solving.** Rejected because package
  management is outside the engine and would require network/security policy.
- **Only a package-version specifier.** Rejected because it cannot express
  platform, native, determinism, capability, or plugin dependency constraints.
- **Arbitrary capability strings.** Rejected for v1 because unknown extension
  boundaries would appear supported without an engine contract or review.
- **Mark the API stable immediately.** Rejected because community-alpha needs
  implementation feedback; preview status supplies a deprecation promise
  without claiming 1.0 maturity.
