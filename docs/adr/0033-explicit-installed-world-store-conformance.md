# ADR-0033: Explicit installed WorldStore conformance

- **Status:** Accepted
- **Date:** 2026-08-06

## Context

`WorldStore` is the public storage-neutral boundary for canonical ECS state.
The production dense/sparse `World` and independent dictionary
`ReferenceWorld` already share extensive private behavior and property tests,
but an external implementation author cannot run a small installed contract
without copying those tests. The design plan names storage-protocol conformance
and independently authored adapters passing conformance as eventual alpha and
adoption measures.

Discovery, data-selected imports, installation, persistence, provider handles,
or a global registry would widen the execution and canonical-state boundaries.
The current protocol also has no external-resource lifecycle. A broad
certification claim would be unsupported because one in-process fixture cannot
establish trust, provenance, complete platform support, performance, recovery,
or determinism beyond the exercised values.

## Decision

Add experimental protocol `ludoweave.world-store-conformance/1` with profile
`world-store-baseline/1`. Its fixed ordered checks cover factory/registry
identity, empty state, direct mutation and epochs, detached copy ownership,
entity generations, read and writable queries, atomic local command buffers,
independent cloning, and structured failure atomicity.

The installed runner accepts only a bounded adapter ID and an explicitly
supplied trusted `factory(ComponentRegistry)`. It creates one immutable fixture
registry, invokes the factory once on the calling thread, and requires the
returned store to expose that exact borrowed registry identity. It does not
discover, dynamically import, install, launch, connect to, scan for, or register
provider code.

Reports have fixed check order, stable status text, runner-owned
`world_store_conformance.*` codes, and the installed LudoWeave version. They
exclude provider messages and codes, paths, environment/platform data, timing,
component/entity values, storage layout, credentials, and native objects. A
failed prerequisite marks dependent checks `not_run`; every check must pass for
overall success.

The current `WorldStore` is an in-memory, single-owner protocol without
`close()`. The runner calls no cleanup method and does not cover stores that own
files, databases, processes, threads, native handles, or other external
resources. Adding such ownership requires a separate engine protocol and
decision rather than duck-typing lifecycle into this profile.

Both project-owned worlds must pass from source, an isolated dependency-free
wheel, and the deterministic release sample bundle. M19 adds no storage
backend, persistence format, provider, plugin field, dependency, lock change,
package version, root export, canonical authority, or CI job.

## Consequences

- Adapter authors can produce comparable installed behavioral evidence without
  copying private fixtures or exposing implementation storage.
- The baseline protects generational identity, epochs, query ownership,
  command atomicity, cloning, and structured errors across implementations.
- The runner executes trusted code in-process. It is not a sandbox, timeout,
  signature/provenance check, security certification, performance benchmark,
  or defense against a malicious factory.
- Passing does not prove cross-platform support, determinism outside the fixed
  fixture, free-threaded safety, external-resource recovery, persistence,
  maintenance readiness, or compatibility with a future profile.
- Project-owned passes are reference evidence, not third-party adoption. The
  independent-adapter count remains zero until maintainers review evidence from
  a separately authored implementation.
- Profile meaning/order changes require a new profile version; incompatible
  report changes require a new protocol version and superseding decision.
