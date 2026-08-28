# RFC-0143: probe an immediate Windows blocker wait timeout

- **Status:** Accepted
- **Milestone:** M160
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS probe that performs a zero-duration
`Popen.wait` after M155's unchanged blocker is ready and M154's native rename
has returned false/32. Require exact `TimeoutExpired`, a still-live child, and
the identical false/32 result after the timeout. Then use M155's unchanged
graceful release/acknowledgement path and require the identical rename to
return true/0 with content preserved. Preserve the no-admission decision and
add no runtime or CI surface.

## Context

M155 proves one graceful blocker release, M156 proves one forced termination,
and M159 observes one native late write after termination. None observes what
the parent sees when it waits with an already-ready blocker still live and the
wait interval expires.

Python documents that `Popen.wait(timeout)` raises `TimeoutExpired` if the
process remains live and that catching the exception and retrying the wait is
safe. Microsoft documents that a zero-millisecond `WaitForSingleObject` call
returns immediately with `WAIT_TIMEOUT` for a nonsignaled process object. M160
uses those semantics only to observe one already-synchronized fixture. It does
not establish a general timeout, cancellation, retry, or recovery policy.

## Decision

Accept the [Windows live-blocker wait-timeout
probe](../security/cache-cleanup-windows-live-wait-timeout-probe.md) as
current-host, test-only feasibility evidence.

Reuse M155's blocker child, readiness parser, graceful release helper, timeout,
and failure cleanup unchanged. Bind the pytest-owned root to handle-reported
NTFS and close the parent probe before launch. Start the exact current
interpreter with `-I -B`, the fixed helper, explicit pipes, `shell=False`, and
`close_fds=True`. After bounded exact-schema `ready`, require M154's unchanged
rename child to return false/32 while the blocker remains alive and namespace/
content remain unchanged.

Call `Popen.wait` exactly once with `timeout=0.0` and require
`subprocess.TimeoutExpired` with the exact child arguments and timeout value.
Require the process return code to remain unset, the child to remain alive,
and the identical native rename to return false/32 again with namespace and
content unchanged. Then invoke M155's existing fixed release and bounded
`closed` acknowledgement once. Require exact child exit zero and one final
identical native rename returning true/0 with content preserved beneath
ordinary `displaced`.

Do not change or add a helper, use a nonzero scheduler-sensitive timeout,
attempt the wait before readiness, kill or terminate after the timeout, use
`communicate()`, sleep, retry the immediate wait, add runtime subprocess or
`ctypes`, add a platform adapter or public capability, claim recovery, add a
dependency, or add workflow/CI allocation.

## Consequences

The current host now observes one case where a zero-duration wait on the live
blocker raises `TimeoutExpired` without terminating it or releasing its native
denial. The unchanged graceful close still orders the one successful rename.

This is not a timeout recovery contract, nonzero timeout guarantee, readiness
or close-timeout result, cancellation behavior, kill policy, native close-
failure result, crash or restart recovery, concurrent mutation safety, general
exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Use a small nonzero timeout. Rejected because scheduler latency would become
  part of the fixture rather than the already-proven live state.
- Wait before `ready`. Rejected because process creation and readiness would be
  confounded with the process wait.
- Use `communicate(timeout=...)`. Rejected because it has different input,
  output, and post-timeout handling semantics.
- Kill after timeout. Rejected because that would repeat M156 rather than prove
  the live state is unchanged.
- Add runtime retry or recovery. Rejected because M160 is admission evidence,
  not cleanup authority or policy.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove exact M155 fixture/helper reuse, fixed isolated
launch, bounded readiness, false/32 with a live blocker, one zero-duration
wait, exact `TimeoutExpired` fields, an unset return code, a still-live child,
the identical second false/32 denial, one graceful release/acknowledgement,
one final true/0 rename, and content preservation. Architecture tests must
preserve M159, runtime, examples, scripts, dependencies, workflows, and wheel
contents. Supported-Python, full regression, installed-wheel, reproducibility,
release, documentation, governance, and findings-first gates remain required.

## References

- [Python: `Popen.wait`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.wait)
- [Microsoft: `WaitForSingleObject`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0142](0142-probe-windows-broken-control-pipe.md)
