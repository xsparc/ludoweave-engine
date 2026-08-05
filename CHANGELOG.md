# Changelog

All notable changes to LudoWeave Engine will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project intends to use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) once release compatibility levels are defined.

## Unreleased

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

## 0.1.0.dev0 - 2026-08-04

- Initial pre-alpha development version reserved for the M0 walking skeleton.
