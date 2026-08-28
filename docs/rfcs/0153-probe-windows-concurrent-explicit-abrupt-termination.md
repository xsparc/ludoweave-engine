# RFC-0153: probe Windows concurrent explicit-list abrupt termination

- **Status:** Accepted
- **Milestone:** M170
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that starts two copies of M163's
fixed inherited-handle child concurrently with distinct explicit handle lists.
After both parent handles close, forcibly terminate one child and wait for its
real nonzero exit. Require only that child's root to become renameable while
the survivor remains live and blocks only its own root. Add no runtime or CI
surface.

## Context

M167 proves pairwise isolation for two successful explicit-list children under
graceful release. M156 proves that forced termination of a separate child-owned
blocker releases its handle after a bounded process wait. M169 proves isolation
when one concurrent helper encounters an injected restoration failure. None
establishes what happens when one of two successfully created explicit-list
children exits abruptly after both parent copies have closed.

Python maps `Popen.kill()` to `TerminateProcess()` on Windows and defines
bounded `Popen.wait()` as the observation that sets the return code. Microsoft
documents external `TerminateProcess` as asynchronous and requires a process
wait to establish termination. It also recommends explicit handle lists when
inheritance is required. A controlled combination of M156 and M167 can answer
the remaining pairwise ownership question without changing production code.

## Decision

Accept the [Windows concurrent explicit-list abrupt-termination
probe](../security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md)
as current-host, test-only evidence.

Create independent pytest-owned roots A and B, each containing ordinary
`live/candidate.bin` content and one distinct noninheritable no-delete-share
parent handle. Parameterize which child terminates abruptly so both A/B role
assignments are covered. Preserve M156, M163, M167, M169, the fixed child
fixture, and their accepted records byte-for-byte.

Shared bounded coordination replaces only M163's module-local `os` and
subprocess references. Require both handles inheritable before either real
launch proceeds, capture both returned processes immediately, and require both
helpers to enter restoration while both flags remain true. Release both exact
native resets, join both launch threads, require exact `ready` from both
children, and require both parent flags false.

M154's unchanged native rename must remain false/error 32 for both roots before
and after both parent handles close. While both children remain live, call
`kill()` only on the assigned abrupt child and wait with the existing fixed
bound. Require a nonzero but otherwise unspecified status, EOF after the
already-consumed `ready` document, and empty stderr. Do not send the release
token and do not receive a graceful `closed` phase.

After that wait, require the abruptly terminated root to return true/code zero
while the survivor root stays false/error 32 and its child remains live. Only
the survivor's existing acknowledged close and zero exit may permit its root's
true/code-zero rename. Preserve both distinct payloads beneath ordinary
`displaced` directories.

Every wait is event-, queue-, pipe-, thread-, or process-bounded. `finally`
releases every event gate, joins both threads, retains every created process,
repairs still-owned parent flags, releases still-owned parent handles, and
closes or reaps every captured process. Do not use sleeps, retries, broad
inheritance, shells, arbitrary code, or environment overrides.

## Consequences

The current host now demonstrates one pairwise abrupt-exit isolation case: a
forcibly terminated explicit-list child releases its inherited blocker after
the process wait, while the surviving explicit-list child retains only its own
distinct blocker until graceful close.

This is not crash recovery, cancellation semantics, arbitrary termination-
timing coverage, native close-failure coverage, a concurrency-safe process-
creation contract, general leak-freedom, a runtime launch coordinator,
recovery, general exclusion, or platform admission. Windows is not admitted.

No runtime API, value, protocol, decoder, CLI command, public probe, production
subprocess or `ctypes`, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Terminate the helper thread rather than the child process. Rejected because
  thread termination would not establish inherited child-handle ownership and
  is unsafe to induce in Python.
- Use the M155 child that opens its own blocker. Rejected because M156 already
  covers that ownership shape; M170 specifically tests an inherited blocker.
- Add retries after termination. Rejected because the bounded process wait is
  the accepted ordering boundary and retries could hide a timing failure.
- Add a runtime coordinator or recovery path. Rejected because cancellation,
  participation, durable recovery, and failure semantics remain undesigned.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  is sufficient for this test-only probe; no hosted check is added.

## Validation

Focused validation must prove both handles marked, both real children captured,
both restoration entries reached while both flags remain true, exact readiness,
and both parent flags restored. Both roots must deny rename after parent close.
The abrupt child must be killed and waited for with nonzero status and no
graceful close acknowledgement; only its root may then rename. The survivor
must remain live and denied until its acknowledged zero-exit close. Every owner
must settle. Architecture tests must preserve M169, M167, M163, M156, the
fixture, runtime, examples, scripts, dependencies, workflows, and wheel
contents. Supported-Python, full regression, installed-wheel, reproducibility,
release, documentation, governance, and findings-first gates remain required.

## References

- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)
- [RFC-0139](0139-probe-windows-abrupt-blocker-termination.md)
- [RFC-0150](0150-probe-windows-concurrent-explicit-inheritance.md)
- [RFC-0152](0152-probe-windows-concurrent-explicit-restore-failure.md)
