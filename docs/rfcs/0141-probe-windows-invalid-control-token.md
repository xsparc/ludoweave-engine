# RFC-0141: probe a Windows blocker invalid control token

- **Status:** Accepted
- **Milestone:** M158
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS probe that sends one fixed invalid byte to
M155's unchanged blocker after readiness. Require the unchanged native rename
probe to report false/32 while the blocker is alive, flush and close the parent
writer, wait with a fixed bound for the helper's existing invalid-control exit,
require no graceful-close acknowledgement, and then require the identical
rename to report true/0 with content preserved. Preserve the no-admission
decision and add no runtime or CI surface.

## Context

M155 proves explicit acquisition and valid-token release. M157 proves that
closing the unwritten parent control stream triggers the same helper's
`finally` close through EOF. Neither distinguishes EOF from receipt of one
non-release byte on the byte-stream control channel.

Microsoft documents that anonymous pipes carry bytes and that `WriteFile`
completes only after writing the specified byte count or returning an error.
Its handle-inheritance guidance states that an anonymous pipe is a byte stream
whose message boundaries require an application protocol. Python documents
that binary buffered streams accept bytes, `flush()` transfers buffered writes,
and `close()` flushes and closes the stream. These sources support one fixed
invalid byte followed by an explicit bounded wait; they do not establish a
general malformed-input protocol or recovery policy.

## Decision

Accept the [Windows blocker invalid-control-token
probe](../security/cache-cleanup-windows-invalid-control-token-probe.md) as
current-host, test-only feasibility evidence.

Reuse M155's blocker child, readiness parser, timeout, and failure cleanup
unchanged. Bind the pytest-owned root to handle-reported NTFS and close the
parent probe before launch. Start the exact current interpreter with `-I -B`,
the fixed helper, explicit pipes, `shell=False`, and `close_fds=True`. After
bounded exact-schema `ready`, require M154's unchanged rename child to return
false/32 while the blocker remains alive and namespace/content remain
unchanged.

Write exactly one repository-fixed `?` byte to `Popen.stdin`, require the
buffered write to accept that byte, flush it, close the parent stream, and
confirm the stream is closed. Wait with the existing fixed timeout and require
the helper's existing exit code 4. Require EOF with no `closed`
acknowledgement and no stderr. Only after the wait may the identical rename
helper retry; require true/0 and unchanged content beneath ordinary
`displaced`.

Do not modify or add a helper, accept arbitrary input, send partial or multiple
writes, retry a pipe write, use `communicate()`, sleep, add runtime subprocess
or `ctypes`, add a platform adapter or public capability, claim recovery, add a
dependency, or add workflow/CI allocation.

## Consequences

The current host now observes one case where the child-owned exclusion remains
effective before a fixed invalid control token and the helper's existing
`finally` close releases the handle before its bounded nonzero exit. The
identical rename then succeeds without process termination, EOF-only input, or
a valid release acknowledgement.

Exit code 4 and the `?` byte are fixed only for this repository-owned fixture
protocol. This observation is not arbitrary malformed input, partial or
multiple write behavior, broken-pipe behavior, readiness or termination
timeout, cancellation, native close failure, crash or restart recovery,
concurrent mutation safety, general exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Generate malformed bytes. Rejected because one fixed non-release byte is the
  smallest deterministic distinction from M157's EOF observation.
- Send more than one byte. Rejected because the unchanged fixture reads exactly
  one byte and extra buffered input would add unobserved behavior.
- Use `communicate()`. Rejected because this probe needs separately observable
  write, flush, close, and bounded-wait transitions.
- Modify the helper to acknowledge invalid control. Rejected because M158 must
  exercise M155's existing closure behavior unchanged.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove exact M155 fixture reuse, fixed isolated launch,
bounded readiness, false/32 with a live blocker, unchanged denial state, one
fixed invalid byte, explicit flush and writer close, bounded wait, exact fixture
exit 4, no close acknowledgement, identical true/0 retry, and content
preservation. Architecture tests must preserve M157, runtime, examples,
scripts, dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0140](0140-probe-windows-control-pipe-eof.md)
