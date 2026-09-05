# RFC-0144: probe an acknowledged Windows blocker release timeout

- **Status:** Accepted
- **Milestone:** M161
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS fixture with separate release-intent and
close tokens. After it acknowledges release intent while deliberately
retaining its no-delete-share directory handle, require one zero-duration
`Popen.wait` to raise exact `TimeoutExpired` and M154's unchanged native rename
to remain false/32. A separate close token must order handle close, exact
`closed`, child exit zero, and the identical rename's true/0 result with
content preserved. Add no runtime or CI surface.

## Context

M155 proves one immediate graceful release, and M160 proves one wait timeout
while its blocker is live before any release request. Neither separates an
acknowledged release request from actual native handle close, so neither can
show whether the denial remains in force across that explicit boundary.

Python documents that `Popen.wait(timeout)` raises `TimeoutExpired` when the
process does not terminate and that retrying the wait is safe. Microsoft
documents that anonymous-pipe reads return when data arrives, that byte-stream
messages require an application protocol, and that share flags remain in
effect until the associated handle closes. Those facts support a fixed
two-token test protocol without a timing sleep. They do not establish runtime
recovery or general cross-process exclusion.

## Decision

Accept the [Windows acknowledged-release timeout
probe](../security/cache-cleanup-windows-acknowledged-release-timeout-probe.md)
as current-host, test-only feasibility evidence.

Add one fixed standalone child fixture. It opens ordinary relative `live`
without delete sharing, emits exact `ready`, accepts M155's existing `!`
release-intent byte, emits exact `release-held` while retaining the native
handle, and blocks on a distinct repository-fixed `.` close byte. Only after
that byte may it close the handle, emit exact `closed`, and exit zero. Invalid
input and native close failure retain separate nonzero fixture exits.

The parent binds the pytest-owned root to handle-reported NTFS and closes its
probe before launch. It starts the current interpreter with `-I -B`, the fixed
helper, explicit pipes, `shell=False`, and `close_fds=True`. After exact
`ready`, require M154's unchanged rename to return false/32. Send and flush
only the release-intent byte, require bounded exact `release-held`, then call
`Popen.wait(timeout=0.0)` exactly once. Require exact `TimeoutExpired`, the
fixed child arguments and timeout, an unset return code, and a live child.
Require the identical rename to remain false/32 with namespace and content
unchanged.

Send and flush the close byte, close the parent writer, require bounded exact
`closed`, bounded child exit zero, stdout/stderr EOF, and one final identical
rename returning true/0 with content preserved beneath ordinary `displaced`.

Do not modify an existing fixture, use a timing sleep or nonzero process wait,
kill or terminate on the accepted path, use `communicate()`, add runtime
subprocess or `ctypes`, add an adapter or public capability, claim recovery,
add a dependency, or add workflow/CI allocation.

## Consequences

The current host now observes one explicitly acknowledged release intent that
does not release the native blocker until the separate close token. The
process wait and rename denial remain aligned during that held phase, and the
fixed close transition orders the one successful rename.

This is not a graceful-close timeout contract, timeout recovery, nonzero
timeout guarantee, cancellation behavior, kill policy, native close-failure
result, crash or restart recovery, concurrent mutation safety, general
exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Add a sleep before close. Rejected because elapsed scheduler time would be
  the synchronization mechanism.
- Modify M155's fixture. Rejected because its accepted single-token protocol
  is protected history.
- Treat release intent as handle release. Rejected because the probe exists to
  distinguish those two states.
- Use `communicate(timeout=...)`. Rejected because it couples input, stream
  closure, output collection, and process wait.
- Add runtime timeout recovery. Rejected because M161 is admission evidence,
  not cleanup authority or policy.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove fixed helper bytes/schema/phases, native handle
retention between `release-held` and the close token, fixed isolated launch,
bounded phase parsing, false/32 before release intent, one zero-duration wait,
exact `TimeoutExpired` fields, an unset return code, the identical second
false/32 denial, a separate close byte, exact `closed`/zero/EOF, one final
true/0 rename, and content preservation. Architecture tests must preserve
M160, runtime, examples, scripts, dependencies, workflows, and wheel contents.
Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Python: `Popen.wait`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.wait)
- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Microsoft: `CreateFile` sharing](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0143](0143-probe-windows-live-wait-timeout.md)
