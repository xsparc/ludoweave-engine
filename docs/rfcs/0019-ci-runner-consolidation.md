# RFC-0019: CI runner consolidation

- **Status:** Accepted
- **Date:** 2026-08-08

## Context

M34 limited hosted CI to substantive pull requests and excluded redundant
post-merge and `.project/**`-only runs. The remaining workflow still allocated
eight runners for eight validation slices. Corrected M35 run `31231410432`
repeated checkout and uv setup in every allocation even though slices on the
same operating system can execute sequentially in one owned environment.

The eight validation slices remain necessary:

1. Ubuntu CPython 3.12 quality, baseline tests, docs, build, installed wheel,
   release smoke, and base profiling;
2. Ubuntu CPython 3.13 compatibility tests;
3. Ubuntu CPython 3.14 compatibility tests;
4. Windows CPython 3.14 compatibility tests;
5. macOS CPython 3.14 compatibility tests;
6. Ubuntu CPython 3.12 real-graphics tests, profile, and vertical slices;
7. Windows CPython 3.12 real-graphics tests, profile, and vertical slices; and
8. macOS CPython 3.12 real-graphics tests, profile, and vertical slices.

Deleting a slice would weaken supported CPython, desktop, distribution, or
provider evidence. Retaining one runner per slice repeats orchestration work
and spends five avoidable runner allocations.

## Decision

M36 groups the same eight validation slices into three OS-owned runner
allocations:

- one Ubuntu allocation performs the 3.12 quality/distribution and graphics
  slices, then installs managed 3.13 and 3.14 interpreters and runs both
  compatibility slices sequentially;
- one Windows allocation performs the 3.12 graphics slice, then installs
  managed 3.14 and runs the compatibility slice; and
- one macOS allocation performs the same two desktop slices.

The workflow continues to use exact uv and action revisions, a frozen lock,
least-privilege `contents: read`, disabled credential persistence, bounded
timeouts, dependency caching, fail-fast isolation between Windows and macOS,
and cancellation of superseded pull-request runs. It remains pull-request only
and ignores `.project/**`-only changes.

Each OS runner owns its environment transitions explicitly. Distribution
artifacts are still built and smoke-tested once on baseline Ubuntu rather than
rebuilding the same universal wheel. Graphics dependencies and Linux Vulkan
software rendering are installed only in runners that execute graphics.

## Consequences

- A substantive pull request allocates three runners instead of eight: five
  fewer allocations, a 62.5% structural reduction.
- Checkout and setup execute three times instead of eight while all eight
  validation slices remain present.
- Slices within one OS runner fail sequentially. This trades some parallel
  feedback and per-slice rerun granularity for lower setup and allocation cost.
- Windows and macOS remain independently isolated by the two-entry desktop
  matrix with `fail-fast: false`.
- No billed-minute reduction is claimed until a corrected hosted run provides
  comparable evidence; allocation reduction is established by workflow
  structure.
- No runtime, public API, protocol, format, dependency, lockfile, package
  version, release workflow, tag, publication, or support-policy change is
  introduced.

## Alternatives considered

Removing compatibility or graphics slices was rejected because it would
weaken the documented platform contract. Keeping eight allocations was
rejected because it repeats setup without adding coverage. One cross-platform
runner is impossible because operating systems are distinct execution
environments. Replacing hosted desktop evidence with local maintainer results
was rejected because local results are not reproducible project gates.
