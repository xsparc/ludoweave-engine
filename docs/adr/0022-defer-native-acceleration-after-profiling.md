# ADR-0022: Defer native acceleration after profiling

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

The M1 10,000-entity simulation tick and M3 10,000-sprite extraction and wgpu
submission workloads missed their starting local targets. Project policy
requires profiling and an RFC before Rust/PyO3 or another native language may
enter the baseline.

[RFC-0001](../rfcs/0001-defer-first-native-kernel.md) records the exact
benchmark/profile evidence and assesses every native-code admission field.

## Decision

Do not add a native kernel in M7. Retain the pure-Python reference paths, pure
wheel, no-compiler baseline, engine-owned public types, and existing backend
isolation.

Ordinary Python and standard-library query, extraction, and packing
optimizations are accepted because property/reference/layout tests exercise
their unchanged semantics. A future native proposal requires a new RFC meeting
all quantified revisit conditions in RFC-0001; a prominent profiler row alone
is insufficient authorization.

## Consequences

- Users retain one portable no-dependency baseline wheel.
- Local target misses remain explicit and continue to motivate profiling.
- No native object, storage layout, GIL promise, or build tool enters public or
  canonical-state APIs.
- The sprite-packing path remains a possible future candidate only after an
  engine-owned contiguous scalar boundary and cross-platform controlled
  evidence exist.
- ECS performance work must first address algorithms and detached-record data
  access; translating the current Python object traversal is not an accepted
  architecture.

## Alternatives considered

Adding PyO3 immediately, changing canonical storage to NumPy, and wrapping
current Python component records in Rust were rejected for the gate failures
and boundary risks documented in RFC-0001.
