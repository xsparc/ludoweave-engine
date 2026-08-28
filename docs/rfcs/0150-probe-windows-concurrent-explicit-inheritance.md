# RFC-0150: probe Windows concurrent explicit-list isolation

- **Status:** Accepted
- **Milestone:** M167
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that overlaps two real process
creations while two distinct no-delete-share handles are temporarily
inheritable. Give each fixed child only its own explicit handle list, then
release the children in both orders and require each child to block only its
own root. Add no runtime or CI surface.

## Context

M163 establishes serial inheritance through one explicit Windows handle list.
M166 then demonstrates Python's documented hazard: a concurrent process
creation that broadly inherits handles can acquire M163's temporarily
inheritable blocker.

Python documents that a non-empty Windows `handle_list` requires
`close_fds=True` and temporary inheritability. Microsoft recommends
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST` when simultaneous process creators need
different inherited handles. Neither source substitutes for an observation
that two overlapping explicit-list launches isolate the exact directory
handles used by this evaluation.

## Decision

Accept the [Windows concurrent explicit-list isolation
probe](../security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md)
as current-host, test-only evidence.

The test creates two independent pytest-owned roots. Each contains ordinary
relative `live/candidate.bin` content and receives its own noninheritable
no-delete-share parent handle. It preserves M163's helper and fixed child
fixture byte-for-byte.

A module-local `os` proxy coordinates only M163's exact inheritability calls.
Both real parent handles must become inheritable before either worker proceeds.
A separate module-local subprocess proxy verifies a one-handle explicit list,
`close_fds=True`, `shell=False`, the corresponding trusted pytest root, and
owned standard pipes before delegating to the captured real `Popen` class.
Neither delegated call returns to M163 until both real process creations have
completed while both parent handles remain inheritable.

The test then requires both helpers to reach restoration while both flags are
still true, releases both exact restore calls, joins both launch threads, and
requires both parent flags false. Both fixed children must emit exact `ready`
and remain live. M154's unchanged native rename must return false/error 32 for
both roots before and after both parent handles close.

Parameterize the child release order as A then B and B then A. In each case,
the first child's acknowledged close and zero exit must permit true/code-zero
rename only for its root while the other root remains false/error 32. The
second child's close must then permit the second rename. Preserve both distinct
candidate payloads beneath ordinary `displaced` directories.

All waits are event-, queue-, pipe-, or process-bounded. `finally` releases
every event gate, joins both threads, captures every process returned by the
real creator, restores any still-owned parent flag, closes every still-owned
parent handle, and closes/reaps every captured child. Do not use sleeps, broad
inheritance, `os.system`, a shell, arbitrary code, or environment overrides.

## Consequences

The current host now supplies one pairwise isolation observation for two
simultaneous explicit handle-list launches: each child retains only the blocker
named in its own list even though both parent handles are inheritable at both
process-creation points.

This is not a concurrency-safe process-creation contract, proof about every
creator or handle type, cancellation/failure/reentrancy coverage, general
leak-freedom, a production launch coordinator, recovery, general exclusion,
or platform admission. Windows is not admitted.

No runtime API, value, protocol, decoder, CLI command, public probe, production
subprocess or `ctypes`, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Add a process-global runtime lock. Rejected because participation by every
  process creator remains undesigned and unproven.
- Infer isolation from Microsoft and Python documentation. Rejected because
  M166 established that process-creation details materially affect this exact
  blocker and a bounded direct observation is available.
- Modify M163's helper to embed coordination. Rejected because the accepted
  serial contract remains useful unchanged and module-local test proxies can
  control the interleaving.
- Add another child fixture or hosted matrix entry. Rejected because the fixed
  M163 child and existing Windows suite exercise the required behavior.

## Validation

Focused validation must prove both handles are marked before either launch
continues, both real `Popen` calls complete before either returns, both helpers
reach restoration while both flags remain true, and both flags return false.
Both children must become ready, both parent handles must close, and both
release orders must prove the first child affects only its own root. Every
thread, process, stream, and parent handle must settle. Architecture tests must
preserve M166, the reused helper and fixture, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: process and handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)
- [RFC-0149](0149-probe-windows-concurrent-inheritance-leak.md)
