# Project State

## Current milestone

M0 — repository contract and walking skeleton — and M1 — deterministic world core — are complete locally. M1-01 through M1-06 implement entity allocation, component schemas/migrations, canonical and reference world storage, queries, local deferred commands, typed resources, deterministic schedule planning, immutable input, and fixed-step application execution.

## Repository identity

- Canonical target repository: `ludoweave-engine`.
- Package and CLI: `ludoweave`.
- Development version: `0.1.0.dev0`.
- License and contribution model: Apache-2.0 with DCO sign-off.
- Supported baseline: standard CPython 3.12-3.14 on Windows, macOS, and Linux; no mandatory native compiler.

## Implemented

- Public README, governance, contribution, conduct, security, changelog, NOTICE, issue/PR templates, and agent guidance.
- PEP 621 pure-Python package, uv lockfile, Ruff, strict Pyright, pytest, Hypothesis, MkDocs Material, and typed-package marker.
- Immutable engine configuration and run summary; monotonic and deterministic virtual clocks.
- Explicit single-owner engine lifecycle with initialization, fixed-tick run, shutdown, failure cleanup, idempotent close, and structured exceptions.
- Engine-owned render protocol, backend-neutral descriptor, and lifecycle-validating null renderer.
- `ludoweave --version`, structured `ludoweave doctor`, and deterministic headless example.
- Architecture overview, runtime contract, accepted ADR-0001 through ADR-0007, and AST import rules that test absolute, relative, near-prefix, and reference-model independence constraints.
- Least-privilege GitHub Actions matrices for the supported operating systems/Python versions and installed-wheel smoke tests.
- Immutable two-field entity IDs, deterministic generational allocation, structured stale-handle failures, and installed-wheel ECS smoke coverage.
- Explicit component UUIDs, frozen schemas, immutable UUID-sorted registries, scalar validation metadata, and complete adjacent forward migration chains.
- Storage-neutral `WorldStore`, canonical `World`, private pure-Python dense/sparse component tables, deterministic inspection, change epochs, and independent in-memory cloning.
- Deliberately simple dictionary `ReferenceWorld` with separately implemented allocation, value, epoch, patch, and clone logic, exercised as a Hypothesis state-machine oracle.
- Structured duplicate/missing/malformed-value failures, copy-in/copy-out ownership, generation-safe swap removal, and installed-wheel world lifecycle coverage.
- Storage-neutral typed query builders with include/exclude/changed filters, opt-in stable ordering, detached row values, explicit writable cursor ownership, row-atomic validated writeback, and private structurally invalidated plan caching.
- World-bound reusable `Commands` buffers with copy-on-enqueue values, identity-only deferred entity tokens, clone-staged atomic flush, deterministic direct-operation epochs, retry/clear failure behavior, and local non-receipt `FlushResult` values.
- Production/reference query and flush conformance, extended Hypothesis state-machine coverage, exact reference-import whitelisting, and installed-wheel query/command smoke coverage.
- Explicit identity-owned typed resource keys, immutable registries, copy-owned singleton stores with a trusted read-only-input adapter contract, exact generic return typing, and structured copy failures.
- Immutable module-level Python system declarations, fixed simulation phases, component/resource access metadata, deterministic-eligibility gates, same-phase conflict ambiguity rejection, canonical cycle diagnostics, and input-order-independent serial schedule planning.
- ADR-0006 documentation, generated DAG/property coverage, D0 component rejection in deterministic plans, and installed-wheel resource/scheduler smoke coverage.
- Exact integer-unit fixed-step accumulation, retained catch-up backlog, absolute virtual deadlines, immutable exact-value input snapshots, virtual/recorded input sources, and application-owned input publication.
- Declaration-enforcing invocation contexts, canonical schedule revalidation, serial PRE/SIMULATE/flush/POST execution, structured failure attribution, BaseException-safe cleanup, and an additive installed-wheel fixed-step example.
- Versioned M1 benchmark tooling for seven workloads with raw samples, nearest-rank p50/p95/p99, sanitized CPython/GIL/environment/commit metadata, exact artifact validation, and tamper regressions.

## Next slice

- M2-01 persistent typed command envelopes and schema registry; no M2 implementation has begun in this branch.

## Validation state

- Local validation completed on Windows with uv-managed CPython 3.12.13.
- The complete M1 final local suite reports 303 passing tests, zero Ruff/Pyright findings, a strict documentation build, successful sdist/wheel build, and successful isolated installed-wheel smoke covering both M0 and M1 examples.
- The final 30-sample Windows/CPython 3.12.13 GIL-build benchmark artifact validates all seven versioned workloads. The 3,600-tick headless p95 was 26.8523 ms and observed the local 5×-real-time target. The representative 10,000-entity simulation-tick p95 was 196.8800 ms and did not observe the 4 ms engineering target. These are local observations, not cross-platform claims.
- GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs are configured but have not been executed in this working tree. Their status must not be reported as passing until CI runs.
- MkDocs Material emits its upstream informational warning about the future MkDocs 2.0 project; the strict documentation build exits successfully.

## External follow-ups

- Rename the current GitHub repository to `ludoweave-engine`.
- Verify and reserve the `ludoweave` name before publishing to PyPI.
- Run the committed CI workflow after the changes are pushed through the maintainer's normal review process.

## Deferred roadmap

Persistent typed commands and receipts, snapshots/replay, random streams, WebGPU, MCP, physics, audio, networking, editor tooling, and native acceleration remain unimplemented. The measured 10,000-entity Python tick miss is profiling evidence only and does not satisfy the later native-code admission gate.
