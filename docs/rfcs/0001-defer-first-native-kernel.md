# RFC-0001: Defer the first native acceleration kernel

- **Status:** Accepted
- **Date:** 2026-08-05
- **Decision:** No Rust/PyO3 kernel is admitted in M7
- **Related:** [ADR-0022](../adr/0022-defer-native-acceleration-after-profiling.md), [benchmark discipline](../benchmarks.md)

## Summary

M7 profiles the recorded M1 and M3 target misses, applies ordinary Python and
standard-library improvements, and declines to add Rust, PyO3, NumPy storage,
or a native build. The remaining costs do not yet provide a safe, maintainable
kernel boundary that can satisfy the native-code admission gate.

This is a measured deferral, not a conclusion that native acceleration will
never be useful.

## Evidence

The final local artifacts were recorded on Windows 11, AMD64, uv-managed
CPython 3.12.13 release/GIL, with the worktree and commit identity embedded in
each versioned JSON document. `cProfile` time is diagnostic and must not be
compared directly with `perf_counter_ns` benchmark time.

The official 30-sample measurements changed as follows after the M7 pure-Python
work:

| Workload | Earlier p95 | M7 p95 | Local change | Starting target |
| --- | ---: | ---: | ---: | ---: |
| 10,000-entity simulation tick | 196.8800 ms | 144.0474 ms | -26.83% | < 4 ms |
| 10,000-sprite extraction and packing | 41.9722 ms | 30.6902 ms | -26.88% | < 3 ms |
| 10,000-sprite wgpu CPU submission | 6.5363 ms | 5.1918 ms | -20.57% | < 3 ms |

None of the three target observations passed. The deltas are same-machine local
observations, not cross-platform performance claims.

The five-repeat profile records show:

- Simulation is distributed across query opening, detached component copying,
  iteration, signature comparison, and row writeback. `_open_query` accounts
  for about 55% cumulative profiled time and `_prepare_component_copy` about
  47%; these overlap rather than identify independent kernels.
- Extraction is dominated by constructing validated immutable presentation
  records. `_interpolate_validated_sprite` accounts for about 42% cumulative
  profiled time. Packing is about 8% of this complete extraction workload.
- Sprite packing is about 86% of the separate wgpu submission profile. It is
  the strongest narrow candidate, but its current input is a sequence of Python
  `SpriteInstance` and nested `Color` objects. A native loop must retain the GIL
  while reading those objects, or require a preceding scalar-buffer conversion
  that performs most of the same traversal.

The artifacts use schema `ludoweave.profile.m7/1`, exact 10,000-item workload
parameters, normalized module/function identities, no filesystem paths or
environment values, and a separate validator with tamper regressions.

## Ordinary optimization performed first

M7 follows the required optimization order before considering a new language:

1. Query setup resolves schemas and writable columns once per query rather
   than once per row.
2. Read-only query columns no longer compute unused mutation signatures.
3. Copy validation and writable signature capture share one scalar traversal.
4. Extraction reuses already validated source fields while checking the three
   interpolated values that can become non-finite.
5. Sprite instances are packed as fixed 64-byte standard-library records,
   avoiding one large intermediate float list and variadic pack operation.

The independent reference world received equivalent query changes, property
tests retain production/reference parity, and exact float32 packing has a
reference-layout regression test.

## Admission-gate assessment

| Required evidence | Assessment |
| --- | --- |
| Representative hotspot and scale | Satisfied locally for the exact 10,000-item M1/M3 workloads. Cross-platform timing is not yet controlled. |
| Pure-Python reference | Satisfied by the existing world/query, extraction, and sprite-packing implementations. |
| Stable buffer and ownership boundary | Not satisfied. ECS and extraction operate on detached Python records. Packing returns owned bytes but consumes Python object graphs. |
| Threading and GIL behavior | Not satisfied for a useful accelerator. Reading the current Python records requires the GIL; a release-safe scalar buffer does not yet exist. |
| Windows/macOS/Linux build and distribution plan | Not supplied. The current pure wheel deliberately requires no compiler. |
| Portable fallback | Available, but a fallback alone does not justify a second implementation. |
| Conformance and fuzz plan | Existing properties provide a base, but no native candidate has a precise buffer-level fuzz contract yet. |
| Maintenance owner | Not assigned; the project must not invent an owner. |
| Quantified improvement target | A future packing experiment must bring the 10,000-sprite submission p95 below 3 ms and improve it by at least 25% on controlled evidence. No admitted ECS kernel can plausibly bridge the current 36x simulation gap without a prior algorithm/data-layout redesign. |

Because several mandatory rows are unsatisfied, introducing a native build in
M7 would violate the project contract even though one profiled function is
prominent.

## Decision and revisit trigger

Rust/PyO3 is deferred. The repository remains pure Python, the baseline wheel
has no dependencies, and no public or canonical-state API exposes a native or
NumPy object.

A new RFC may propose one kernel only when all of these are present:

1. controlled benchmark results on at least two maintained operating systems
   and two supported CPython minors still miss an assigned target;
2. one engine-owned contiguous scalar input/output boundary accounts for at
   least 40% of the residual end-to-end workload;
3. the boundary can cross Python/native once per batch and release the GIL
   without borrowing mutable Python objects;
4. the proposal names a maintainer, portable fallback, exact build matrix,
   conformance/fuzz corpus, wheel-size impact, and rollback plan; and
5. an experiment demonstrates at least 25% end-to-end improvement and meets
   its assigned p95 target without changing deterministic results.

Until then, profiling should guide data-access, allocation, and batching work
inside normal CPython.

## Alternatives considered

- **Add a PyO3 sprite packer now.** Rejected because Python object traversal
  prevents a useful GIL-free kernel and the standard-library change already
  removed meaningful cost without a compiler.
- **Move ECS copy/writeback into Rust.** Rejected because the hotspot spans
  Python component validation and ownership semantics; it is not a stable
  scalar-buffer kernel and cannot close the target gap alone.
- **Add NumPy-backed canonical storage.** Rejected because it would change
  ownership/layout boundaries, add a mandatory native dependency, and expose a
  storage decision before a design slice has justified it.
- **Treat wgpu provider calls as an engine kernel.** Rejected because provider
  submission is already native/FFI territory and must remain isolated behind
  the engine-owned render adapter.
