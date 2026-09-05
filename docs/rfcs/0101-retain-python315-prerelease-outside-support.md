# RFC-0101: Retain Python 3.15 prerelease outside support

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PEP 790 schedules Python 3.15.0 final for 2026-10-01. At this decision date,
3.15.0 candidate 1 has been released but the final version has not. uv describes
Python 3.15 prereleases as Tier 2 rather than its Tier 1 stable-version set.
LudoWeave declares and tests standard CPython `>=3.12,<3.15`.

The exact uv-managed Windows x86-64 inventory exposed CPython 3.15.0b1 but no
RC1 download. The unavailable RC1 install request failed before project
execution, so no RC1 compatibility result is claimed.

A pure LudoWeave `0.1.0a1` wheel built under the supported environment. An
isolated exact Windows CPython 3.15.0b1 environment installed it without
dependencies only through pip's explicit metadata override. Module version
discovery passed. Doctor correctly rejected the unsupported Python version with
exit code 1 after completing its bounded checks. A separate installed-wheel
probe completed 120 virtual ticks and frames in exactly 2,000,000,000
nanoseconds, closed normally, and rejected a worker-thread initialization with
`engine.wrong_thread`. The installed headless example reproduced the same
deterministic tick, frame, time, renderer, and final-state summary.

## Decision

Retain Python 3.15 outside the supported range until its final release and a
complete admission proposal. Keep `requires-python = ">=3.12,<3.15"`, the
current classifiers, doctor boundary, supported CI matrix, lock, and runtime
unchanged.

Record the exact Windows CPython 3.15.0b1 result as one unsupported prerelease
compatibility observation. It is no support promise. Normal users and release
verification must not apply the explicit metadata override used by the probe.

## Boundary

M118 adds no Python 3.15 classifier, supported-version promise, source/full-
suite/graphics/cross-platform result, free-threaded claim, prerelease runtime
branch, compatibility shim, dependency, lock, metadata, version, runtime
package/API, workflow, runner allocation, action, permission, credential,
release mutation, release authority, tag, release, or publication. It is not a
real public release observation.

The result does not qualify Python 3.15 final, later prereleases, alternate
platforms, optional graphics dependencies, native extensions, or third-party
providers.

## Consequences

- Supported installers continue to reject Python 3.15 through package metadata.
- Doctor remains consistent with metadata and reports the prerelease as
  unsupported even when bounded serial engine operations happen to work.
- The pure-wheel observation supplies early compatibility information without
  spending hosted runner allocation or widening the public contract.
- A future support proposal must use Python 3.15 final and cover supported
  platforms, complete suites, tooling, lock resolution, optional dependencies,
  providers, installed artifacts, documentation, and maintenance policy.

## Alternatives considered

- Promote Python 3.15 now. Rejected because the final release and complete
  admission evidence do not exist.
- Add a hosted prerelease job. Rejected because one early observation does not
  justify recurring runner allocation or support expectations.
- Relax doctor while keeping metadata strict. Rejected because diagnostics and
  installer support boundaries should agree.
- Add compatibility code for the prerelease. Rejected because the serial probe
  found no runtime defect requiring a change.

## References

- [PEP 790: Python 3.15 release schedule](https://peps.python.org/pep-0790/)
- [Python 3.15 documentation](https://docs.python.org/3.15/contents.html)
- [uv Python support policy](https://docs.astral.sh/uv/reference/policies/python/)
- [RFC-0100: retain the standard CPython baseline](0100-retain-standard-cpython-baseline.md)
