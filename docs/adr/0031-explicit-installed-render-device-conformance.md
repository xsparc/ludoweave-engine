# ADR-0031: Explicit installed render-device conformance

- **Status:** Accepted
- **Date:** 2026-08-06

## Context

The alpha has repository-internal Null and wgpu tests and a prose adapter
checklist. The design plan's longer-term adoption metrics include the number of
third-party adapters and plugins passing conformance, but an external adapter
author cannot run a small versioned installed contract without copying private
test code. Plugin manifests deliberately describe inert compatibility metadata
and cannot establish runtime behavior.

A conformance tool that discovers or imports packages by data would violate
RFC-0002, expand the executable-plugin trust boundary, and make installed
ambient state affect composition. A broad certification claim would also be
unsupported: provider provenance, security, performance, and cross-platform
behavior require evidence beyond one local run.

## Decision

Add experimental protocol `ludoweave.render-device-conformance/1` with profile
`render-device-baseline/1`. The profile exercises the existing engine-owned
`RenderDevice` boundary: validated identity and capabilities, provider-neutral
resource handles, offscreen clear submission, fence completion, capability-
consistent capture, copied events, resize, stale-handle rejection, idempotent
close, and use-after-close rejection.

The installed runner accepts only a bounded adapter ID and a caller-supplied
factory. The caller explicitly imports and trusts the adapter. The runner does
not discover, dynamically import, install, launch, connect to, or register
provider code. It imports no concrete backend and returns only frozen
engine-owned evidence records.

Reports use fixed check order, stable status text, runner-owned
`conformance.*` error codes, and the installed LudoWeave version. They exclude
provider error codes and exception messages, paths,
environment values, platform metadata, timing, capture bytes, and native
objects. A failed prerequisite marks later dependent checks `not_run` while
best-effort close remains observable. Every check must pass for overall
success.

The Null device must pass from the baseline wheel and release sample bundle.
The official wgpu adapter must pass in the existing three-platform graphics
job. M17 adds no CI job, dependency, plugin field, loader, registry, persistent
world format, canonical state, or public package-root export.

## Consequences

- External adapter authors can produce comparable installed evidence without
  copying repository-private fixtures.
- Null and wgpu exercise the same baseline semantics; provider-specific tests
  remain necessary.
- The runner executes trusted code in-process. It is not a sandbox, timeout,
  signature, provenance check, security certification, or protection against a
  malicious factory.
- One passing local report does not prove support across the CPython/desktop
  matrix, deterministic raster output, performance, device recovery, or
  maintenance readiness.
- No independently authored adapter is counted as adopted until maintainers
  review external evidence. Project-owned Null/wgpu passes are reference
  evidence, not third-party adoption.
- Profile meaning/order changes require a new profile version; incompatible
  envelope changes require a new protocol version and superseding decision.
