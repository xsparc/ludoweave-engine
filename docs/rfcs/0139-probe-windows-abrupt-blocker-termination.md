# RFC-0139: probe abrupt termination of a Windows blocker owner

- **Status:** Accepted
- **Milestone:** M156
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS probe that abruptly terminates M155's
fixed child-owned no-delete-share blocker. Require the unchanged native rename
probe to report false/32 while the blocker is alive, wait with a fixed bound
after forced termination, require no graceful-close acknowledgement, and then
require the identical rename to report true/0 with content preserved. Preserve
the no-admission decision and add no runtime or CI surface.

## Context

M155 proves explicit acquisition and graceful release by a distinct blocker
process. Its fixed release byte allows the child to close the native handle in
`finally`, emit `closed`, and exit zero. That does not observe what happens when
the owner is terminated without executing that user-mode cleanup path.

Microsoft documents that open kernel-object handles are closed automatically
when a process terminates. It also documents that `TerminateProcess` is
asynchronous when invoked by another process and that a caller must wait on the
process object to establish termination. Python maps `Popen.kill()` to
`TerminateProcess` on Windows and provides a bounded `wait(timeout=...)`.

## Decision

Accept the [Windows abrupt blocker-owner termination
probe](../security/cache-cleanup-windows-abrupt-blocker-termination-probe.md)
as current-host, test-only feasibility evidence.

Reuse M155's blocker child, readiness parser, timeout, and failure cleanup
unchanged. Bind the pytest-owned root to handle-reported NTFS and close the
parent probe before launch. Start the exact current interpreter with `-I -B`,
the fixed helper, explicit pipes, `shell=False`, and `close_fds=True`. After
bounded exact-schema `ready`, require the unchanged M154 rename child to return
false/32 while the blocker remains alive and namespace/content remain
unchanged.

Do not send M155's release token. Force termination, wait with the existing
fixed timeout, require a nonzero but otherwise unspecified exit code, and
require EOF with no `closed` acknowledgement or stderr. Only after the wait may
the identical rename helper retry; require true/0 and unchanged content beneath
ordinary `displaced`.

Do not add a new helper, retry, sleep, runtime subprocess or `ctypes`, platform
adapter, public capability, cleanup authority, dependency, workflow, or CI
allocation.

## Consequences

The current host now observes one case where a child-owned exclusion remains
effective before forced termination and the identical rename succeeds after
the operating system reports that child terminated. The fixture distinguishes
the abrupt path from M155's acknowledged graceful close.

The nonzero process status is intentionally not fixed to one numeric value.
The observation is not crash recovery, restart recovery, durable cleanup,
close-failure recovery, cancellation semantics, concurrent mutation safety,
duplicated-handle behavior, general exclusion, or platform admission. It does
not establish when underlying cancellation or filesystem work completes on
every Windows/filesystem/driver combination.

Windows is not admitted.

## Alternatives considered

- Modify the blocker to simulate failure. Rejected because forced process
  termination must bypass the helper's graceful release path.
- Assert one Windows termination status. Rejected because the milestone needs
  only a non-successful abrupt exit and does not define Python or Windows exit
  code compatibility.
- Retry until rename succeeds. Rejected because the explicit process wait is
  the accepted ordering boundary and a retry loop would conceal timing.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.
- Implement recovery. Rejected because recovery policy, durable receipts,
  restart state, and production adapter ownership remain unresolved.

## Validation

Focused validation must prove exact M155 fixture reuse, fixed isolated launch,
bounded readiness, false/32 with a live blocker, unchanged denial state, no
release token, forced termination, bounded wait, nonzero exit, no close
acknowledgement, identical true/0 retry, and content preservation. Architecture
tests must preserve M155, runtime, examples, scripts, dependencies, workflows,
and wheel contents. Supported-Python, full regression, installed-wheel,
reproducibility, release, documentation, governance, and findings-first gates
remain required.

## References

- [Microsoft: terminating a process](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0138](0138-probe-windows-child-owned-share-delete-handshake.md)
