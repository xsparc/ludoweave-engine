# RFC-0148: probe Windows inherited-handle restoration failure

- **Status:** Accepted
- **Milestone:** M165
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that injects a fixed failure when
M163's unchanged successful-child launch helper first attempts to restore its
temporarily inheritable blocker handle. Require the helper to close and reap
the already-created child before the identical injected exception escapes,
then require the parent to repair noninheritability explicitly while retaining
sole ownership and native rename denial until close. Add no runtime or CI
surface.

## Context

M163 successfully transfers one explicitly allowlisted blocker handle to a
child. Its helper defensively calls the unchanged child-close routine when
restoring noninheritability raises after process creation. M164 separately
observes a real missing-executable launch failure, but no process exists on
that path and native restoration succeeds.

Python exposes explicit Windows handle-inheritability mutation. Microsoft
documents that `SetHandleInformation` can fail and exposes extended error
information. Those facts make restoration a distinct ownership boundary, but
forcing a real kernel failure safely and deterministically on a valid owned
handle is not available through the existing test contract. M165 therefore
injects one failure before the native restore call and makes no claim about a
real native restoration failure.

## Decision

Accept the [Windows inherited-handle restoration-failure
probe](../security/cache-cleanup-windows-inherited-restore-failure-probe.md) as
current-host, test-only ownership evidence.

The test binds its pytest-owned root to handle-reported NTFS, creates ordinary
relative `live`, and opens one noninheritable no-delete-share handle. It uses
M163's unchanged child fixture and launch helper. The test captures the exact
original inheritability setter and child-close function, then installs two
bounded test doubles:

1. a setter that delegates the initial `True` transition to the real setter
   but raises one fixed `OSError` subclass before the first `False` transition
   for the exact blocker handle; and
2. a close observer that records only the created child and delegates
   immediately to M155's unchanged close-and-reap function.

The real child creation must succeed before the injected restore failure. The
helper must return no process, re-raise the identical injected exception, call
the close observer exactly once, leave the child terminal, and close all three
owned pipe streams. Because the native restore was deliberately bypassed, the
parent handle must still be inheritable; the test must not describe that state
as repaired.

In a `finally` boundary, the caller uses the captured original setter to clear
inheritability and closes any unexpectedly returned process. After explicit
repair, require noninheritability, parent owned count one, and M154's unchanged
native rename false/error 32 with namespace and content preserved. Close the
parent handle exactly once, require owned count zero, and require the identical
second rename true/code zero with content preserved beneath ordinary
`displaced`.

Do not modify M163 or M164, inject failure before successful child creation,
replace the native child close, leave the handle inheritable after the test,
run concurrent launches, claim real native restoration-failure behavior, add
runtime subprocess or `ctypes`, add a dependency, or add workflow/CI
allocation.

## Consequences

The current host now observes that the existing successful-launch helper
reclaims its created child before an injected restoration exception escapes,
while the caller retains explicit responsibility to repair the still-
inheritable parent handle.

This is an injected restoration failure, not a real native restoration
failure, arbitrary failure coverage, concurrent-launch leak-freedom, a
concurrency-safe inheritance contract, native-close failure, recovery,
general exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Invalidate or close the handle before restoration. Rejected because it
  destroys the owned-handle invariant and tests a different invalid-handle
  boundary.
- Patch `Popen` to fail. Rejected because M164 already covers a real launch
  failure with no created child.
- Swallow the restoration error after reaping. Rejected because the parent
  remains inheritable and must retain explicit repair duty.
- Add runtime recovery. Rejected because M165 is admission evidence, not
  production cleanup authority.
- Add another hosted job. Rejected because the existing Windows suite can run
  the probe after the unpublished stack is safely integrated.

## Validation

Focused validation must prove one real child creation, one fixed injected
restore attempt, exact exception identity, no returned process, one delegated
close/reap, terminal process state, closed streams, observable retained
inheritability before caller repair, explicit repair, retained parent
ownership, false/32 before parent close, true/0 only after parent close, and
content preservation. Architecture tests must preserve M164, runtime,
examples, scripts, dependencies, workflows, and wheel contents. Supported-
Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Python: inheritance of file descriptors and handles](https://docs.python.org/3/library/os.html#inheritance-of-file-descriptors)
- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: `SetHandleInformation`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-sethandleinformation)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0147](0147-probe-windows-inherited-launch-failure.md)
