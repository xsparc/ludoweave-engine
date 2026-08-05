# Changelog

All notable changes to LudoWeave Engine will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project intends to use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) once release compatibility levels are defined.

## Unreleased

### Added

- M7 versioned, sanitized `cProfile` evidence and strict tamper-resistant
  validation for the representative 10,000-entity and 10,000-sprite workloads.
- RFC-0001 and ADR-0022 recording the evidence-based decision to defer the
  first Rust/PyO3 kernel.

### Changed

- Reduced detached query overhead by resolving column metadata once, skipping
  unused read-only signatures, and sharing copy/signature traversals.
- Reduced presentation extraction and float32 sprite-packing allocations while
  preserving exact validation, error, ownership, and provider-neutral layout
  behavior.

## 0.1.0a1 - 2026-08-05

### Added

- M0 repository contract and deterministic headless walking skeleton.
- M1 generational entity IDs and deterministic slot allocator with structured stale-handle failures.
- Explicit component UUIDs, immutable schema registries, validation metadata, and adjacent forward migrations.
- Canonical dense/sparse world storage, copy-safe component ownership, change epochs, cloning, and an independent dictionary reference model.
- Storage-neutral typed queries, changed-epoch filters, explicit writable row cursors, and private plan caching.
- World-bound local structural command buffers with exact deferred-token ownership and atomic clone-staged flush.
- Explicit typed resources with copy-owned singleton storage and deterministic conflict-aware serial schedule planning.
- Additive fixed-step application runtime with immutable input, declaration-enforcing system contexts, retained catch-up backlog, and one PRE/SIM command flush before POST.
- Sanitized M1 benchmark and validation tooling with raw samples, p50/p95/p99 distributions, environment metadata, and explicit local target observations.
- M2 bounded canonical JSON, immutable versioned command/transaction envelopes, and explicit operation registry.
- Atomic clone-staged world sessions with optimistic hashes, dry-run, authoritative resource codecs, staged ticks, canonical receipts, and exact semantic diffs.
- Canonical authority snapshots with bounded atomic restore, registered forward migrations, SHA-256 verification, and deterministic named PCG32 random streams.
- Self-contained canonical replay timelines with exact tick/hash batches, verified checkpoints, composition headers, and immutable parent-referenced branches.
- Project-confined data-only CLI workflows for equivalent command receipts, snapshot extraction, replay verification, and semantic snapshot diffing.
- Exhaustive session resource roles, detached authority views, project-bound snapshots, one-tick replay branch boundaries, and handle-bounded CLI artifact reads.
- M3 backend-neutral render descriptors, scoped generational handles, immutable presentation extraction, and deterministic render-graph validation.
- Optional exactly pinned wgpu/rendercanvas/GLFW rendering with instanced atlas sprites, tiles, orthographic cameras, debug primitives, offscreen RGBA capture, resize/minimize behavior, and typed device loss.
- Reproducible 1k/10k renderer benchmarks, tolerant GPU fixtures, and graphics-extra CI coverage.
- M4 provider-neutral keyboard, mouse, pointer, resize, focus, and close records with deterministic digital transitions and 2D action mapping.
- Validated `asset://` manifests, project path confinement, content-addressed dependency invalidation, bounded PNG decoding, and safe retained texture replacement.
- Pure-Python AABB/circle overlap, a property-tested deterministic spatial grid, documented kinematic resolution, and a lifecycle-validating Null audio backend.
- ECS-authoritative Clockwork Arena gameplay with deterministic waves, enemies, projectiles, health, score, restart, exact 3,600-tick fixture/replay evidence, optional wgpu rendering, and stress benchmark tooling.
- M5 transport-independent typed agent service with immutable tool schemas, explicit read/write/capture/test capabilities, quotas, redaction, mutation serialization, and provider ownership.
- Equivalent direct Python, project-confined CLI, and local stdio MCP `2025-11-25` tool calls over the existing transaction, receipt, snapshot, diff, replay, capture, telemetry, and acceptance-test contracts.
- Agent World Builder acceptance composition exercising describe, validate, apply, fixed ticks, offscreen capture, query, adjustment, semantic diff, replay evidence, telemetry, and registered in-process checks.
- M6 deterministic release staging with a pure wheel, source distribution, sample bundle, SPDX 2.3 SBOM, checksums, notices, manifest, and isolated cross-platform artifact smoke.
- Explicit `internal`, `experimental`, `preview`, and `stable` compatibility policy with exact `__all__`/`__stability__` metadata validation for every public Python export.
- Community-alpha user, adapter, release, contribution, triage, roadmap, and retrospective documentation.
- Tag-only, immutable-action release automation for build-provenance and SBOM attestations plus staged GitHub prerelease creation; no PyPI publishing step.
- Declarative triage labels, focused issue forms, and an issue-ready good-first contribution queue.

## 0.1.0.dev0 - 2026-08-04

- Initial pre-alpha development version reserved for the M0 walking skeleton.
