# RFC-0152: probe Windows concurrent explicit-list restoration failure

- **Status:** Accepted
- **Milestone:** M169
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that starts two copies of M163's
fixed inherited-handle child concurrently with distinct explicit handle lists.
Hold both parent handles inheritable through both real process creations and
both restoration entries, then inject M165's exact restoration error for one
handle. Require the helper to reap only that handle's child before propagating
the error while the other child remains live and continues to block only its
own root. Add no runtime or CI surface.

## Context

M168 proves pairwise isolation when one concurrent explicit-list launch
succeeds and the other fails before creating a process. M165 separately proves
that M163 reaps an already-created child before an injected restoration error
escapes. Neither observation establishes ownership when two explicit-list
children are created successfully and only one concurrent restoration fails.

Python requires a non-empty Windows `handle_list` to be paired with
`close_fds=True` and temporarily inheritable handles. Current CPython performs
the platform process creation between the caller's inheritability changes.
Microsoft documents `SetHandleInformation` failure separately from successful
`CreateProcessW` ownership and recommends explicit handle lists when
simultaneous creators need different handles. A controlled test can combine
the already accepted M163 and M165 boundaries without changing production
process creation.

## Decision

Accept the [Windows concurrent explicit-list restoration-failure
probe](../security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md)
as current-host, test-only evidence.

Create independent pytest-owned roots A and B, each containing ordinary
`live/candidate.bin` content and one distinct noninheritable no-delete-share
parent handle. Parameterize which root receives the injected restoration
failure so both A/B role assignments are covered. Preserve M163's helper,
M165's failure type and boundary, M168's complete boundary, and the fixed child
fixture byte-for-byte.

Shared bounded coordination replaces only M163's module-local `os` and
subprocess references. Require both handles inheritable before either real
launch proceeds. Capture each returned process immediately, hold both launch
outcomes while both handles remain inheritable, then require both helpers to
enter restoration. Release both restoration calls together. One exact setter
call raises the injected M165 error without performing the native reset; the
other performs its exact native reset.

M163 must close and reap only the failed-restoration child before returning the
same injected error. The surviving child must emit exact `ready`, remain live,
and retain only its distinct blocker. Explicitly repair the still-inheritable
failed parent handle. M154's unchanged native rename must remain false/error 32
for both roots until both parent handles close. The failed-restoration root
must then return true/code zero immediately while the survivor root stays
false/error 32 until its child acknowledges close and exits zero. Preserve both
distinct payloads beneath ordinary `displaced` directories.

Every wait is event-, queue-, pipe-, thread-, or process-bounded. `finally`
releases every event gate, joins both threads, retains every created process,
repairs still-owned parent flags, releases still-owned parent handles, and
closes or reaps every captured process. Do not use sleeps, broad inheritance,
shells, arbitrary code, or environment overrides.

## Consequences

The current host now demonstrates one successful/synthetic-restoration-failure
pairwise isolation interleaving: the helper reaps only the failed side's
already-created child before the error escapes, while the surviving explicit-
list child neither loses its own blocker nor acquires the failed side's
distinct blocker.

This is not a real native restoration failure, not a concurrency-safe process-
creation contract, arbitrary launch/restoration failure coverage,
cancellation, reentrancy, general leak-freedom, a runtime launch coordinator,
recovery, general exclusion, or platform admission. Windows is not admitted.

No runtime API, value, protocol, decoder, CLI command, public probe, production
subprocess or `ctypes`, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Force a real `SetHandleInformation` failure after process creation. Rejected
  because inducing that native state safely and reproducibly without invalid
  ownership or broader process effects is not established.
- Modify M163 with production coordination hooks. Rejected because module-local
  test proxies can control the bounded interleaving while preserving the
  accepted helper contract.
- Add a runtime or global launch lock. Rejected because participation,
  reentrancy, cancellation, compatibility, and failure recovery remain
  undesigned.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  is sufficient for this test-only probe; no hosted check is added.

## Validation

Focused validation must prove both handles marked, both real children created,
both outcomes held, and both restoration entries reached while both flags
remain true. The failed side must propagate the exact injected object only
after its child and streams settle. The other child must remain ready/live.
After explicit failed-parent repair, both roots must deny rename until parent
close; afterward the failed-restoration root must rename while the survivor
root remains denied until child close. Every owner must settle. Architecture
tests must preserve M168, M165, M163, the fixture, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Python: inheritable handles](https://docs.python.org/3/library/os.html#os.set_handle_inheritable)
- [CPython: subprocess implementation](https://github.com/python/cpython/blob/main/Lib/subprocess.py)
- [Microsoft: `SetHandleInformation`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-sethandleinformation)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)
- [RFC-0148](0148-probe-windows-inherited-restore-failure.md)
- [RFC-0151](0151-probe-windows-concurrent-explicit-launch-failure.md)
