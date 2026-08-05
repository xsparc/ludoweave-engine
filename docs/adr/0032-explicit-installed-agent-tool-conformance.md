# ADR-0032: Explicit installed agent-tool conformance

- **Status:** Accepted
- **Date:** 2026-08-06

## Context

The alpha exposes 12 typed agent tools through one transport-independent
service and exercises them internally through Python, CLI, MCP, and the Agent
World Builder. An external local adapter author cannot, however, run a small
versioned installed behavioral contract without copying private tests. The
design plan names third-party adapter conformance and successful agent-tool
operation as eventual adoption measures, while current evidence is limited to
project-owned compositions.

Discovery, data-selected imports, installation, subprocesses, networking, or
global adapter registries would widen the executable-code and remote-control
boundaries. A broad certification or adoption claim would also be unsupported:
one in-process run cannot establish provider trust, provenance, support-matrix
coverage, performance, or human recovery rates.

## Decision

Add experimental protocol `ludoweave.agent-tool-conformance/1` with profile
`agent-tool-baseline/1`. It exercises the exact existing tool set against a
fresh clean authority: service discovery/capabilities, detached observation,
snapshot baseline, dry-run and committed transaction receipts, stale-hash
atomicity, entity query, per-tick receipts, semantic diff, capture/test/
telemetry shapes, idempotent close, and structured use-after-close rejection.

The installed runner accepts only a bounded adapter ID and a caller-supplied
factory. The caller explicitly imports and trusts the adapter. The runner does
not discover, dynamically import, install, launch, connect to, scan for, or
register provider code. It invokes one adapter synchronously on the calling
thread, owns and closes it, and returns only frozen engine-owned evidence.

Reports have fixed check order, stable status text, runner-owned
`agent_conformance.*` codes, and the installed LudoWeave version. They exclude
provider codes/messages, paths, environment and platform data, timing,
credentials, world snapshots, captures, entity values, and native objects. A
failed prerequisite marks dependent checks `not_run`; best-effort close still
runs. Every check must pass for overall success.

The direct project service must pass from source, an isolated installed wheel,
and the release sample bundle. M18 adds no transport, listener, provider,
plugin field, registry, dependency, lock change, persistent format, canonical
state, root-package export, or CI job.

## Consequences

- Local adapter authors can produce comparable installed behavioral evidence
  without copying repository-private fixtures.
- The conformance runner exercises the same command/receipt contract as direct
  Python while remaining transport-independent.
- The runner executes trusted code in-process. It is not a sandbox, timeout,
  signature or provenance check, security certification, or defense against a
  malicious factory.
- A passing report does not prove transport security, cross-platform support,
  determinism outside the fixed fixture, performance, free-threaded safety,
  maintenance readiness, or real-agent success without manual recovery.
- Project-owned passes are reference evidence, not third-party adoption. No
  external adapter is counted until maintainers review independently authored
  evidence.
- Profile meaning/order changes require a new profile version; incompatible
  report changes require a new protocol version and superseding decision.
