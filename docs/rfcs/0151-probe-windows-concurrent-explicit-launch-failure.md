# RFC-0151: probe Windows concurrent explicit-list launch failure

- **Status:** Accepted
- **Milestone:** M168
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that starts M163's fixed inherited-
handle child concurrently with M164's real missing-executable launch. Keep two
distinct blocker handles inheritable across both real launch outcomes and both
restoration entries. After both parent handles close, require the failed-launch
root to rename while the successful child still blocks only its own root. Add
no runtime or CI surface.

## Context

M167 proves pairwise isolation for two successful explicit-handle-list process
creations. It does not establish ownership when one concurrent `CreateProcess`
call fails before returning a process owner.

Python documents that child-start failures are re-raised in the parent and
that a non-empty Windows `handle_list` requires temporary inheritability.
Current CPython delegates to Win32 process creation and closes its parent-side
pipe copies in `finally`. Microsoft specifies a zero return on `CreateProcessW`
failure and recommends explicit handle lists when simultaneous creators need
different handles. A direct successful/failed interleaving can test whether
the successful child remains confined to its own blocker.

## Decision

Accept the [Windows concurrent explicit-list launch-failure
probe](../security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md)
as current-host, test-only evidence.

Create independent pytest-owned roots A and B, each containing ordinary
`live/candidate.bin` content and one distinct noninheritable no-delete-share
parent handle. Parameterize which root receives the successful M163 launch and
which receives M164's missing-executable launch so both label assignments are
covered. Preserve both accepted helpers and M163's fixed child fixture byte-
for-byte.

Shared bounded coordination replaces only the helpers' module-local `os` and
subprocess references. Require both handles inheritable before either launch
continues. Require both wrappers at their launch boundary, then release the
captured real `Popen` calls. The successful wrapper must capture its process
owner immediately; the failure wrapper must capture an exact
`FileNotFoundError`. Neither wrapper may return or re-raise until both outcomes
exist while both handles remain inheritable.

Require both helpers to reach restoration while both flags remain true, then
release both exact resets and join both threads. M164 must return the same
captured error with `errno.ENOENT` and Windows error 2; M163's child must emit
exact `ready` and remain live. Both parent flags must be false.

M154's unchanged native rename must initially return false/error 32 for both
roots. After both parent handles close, require the failed-launch root to return
true/code zero immediately while the successful root remains false/error 32
and its child remains live. Only that child's acknowledged close and zero exit
may permit the successful root's true/code-zero rename. Preserve both distinct
payloads beneath ordinary `displaced` directories.

Every wait is event-, queue-, pipe-, thread-, or process-bounded. `finally`
releases every event gate, joins both threads, retains any successfully created
process before coordination waits, repairs still-owned parent flags, releases
still-owned parent handles, and closes/reaps every captured process. Do not use
sleeps, broad inheritance, shells, arbitrary code, or environment overrides.

## Consequences

The current host now demonstrates one successful/failed pairwise isolation
interleaving: failure creates no lasting child owner for its blocker, and the
successful explicit-list child does not acquire the failed launch's distinct
handle even though both were inheritable at both outcomes.

This is not a concurrency-safe process-creation contract, arbitrary launch-
failure coverage, cancellation/restoration-failure/reentrancy coverage,
general leak-freedom, a runtime launch coordinator, recovery, general
exclusion, or platform admission. Windows is not admitted.

No runtime API, value, protocol, decoder, CLI command, public probe, production
subprocess or `ctypes`, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Inject a synthetic exception before process creation. Rejected because M164
  already provides a bounded real Win32 missing-executable result.
- Modify M163 or M164 with concurrency hooks. Rejected because module-local
  test proxies can control the interleaving while preserving both contracts.
- Add a runtime/global launch lock. Rejected because participation, reentrancy,
  cancellation, and compatibility remain undesigned.
- Add another fixture or hosted matrix entry. Rejected because existing fixed
  helpers and the existing Windows suite cover the bounded question.

## Validation

Focused validation must prove both handles marked, both launch boundaries
ready, both real outcomes observed before return, both restoration entries
reached while both flags remain true, and both flags restored. The failure must
be exact and process-free; the successful child must be ready/live. Before
parent close both roots must deny rename. After parent close only the failed-
launch root may rename, and the successful root must remain denied until its
child closes. Every owner and stream must settle. Architecture tests must
preserve M167, both reused helpers, the fixture, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full regression,
installed-wheel, reproducibility, release, documentation, governance, and
findings-first gates remain required.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [CPython: subprocess implementation](https://github.com/python/cpython/blob/main/Lib/subprocess.py)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)
- [RFC-0150](0150-probe-windows-concurrent-explicit-inheritance.md)
