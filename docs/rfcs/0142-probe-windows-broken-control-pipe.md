# RFC-0142: probe a broken Windows blocker control pipe

- **Status:** Accepted
- **Milestone:** M159
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS probe that attempts one fixed late release
write after M155's unchanged blocker child has been killed and boundedly
reaped. Require the unchanged native rename probe to report false/32 while the
blocker is alive, require a direct test-only `WriteFile` call to report
false/error 232 with zero bytes after the reader is gone, close the parent
writer, and then require the identical rename to report true/0 with content
preserved. Preserve the no-admission decision and add no runtime or CI surface.

## Context

M156 proves that abrupt blocker-owner termination releases the native denial.
M158 proves one fixed invalid byte while the child is still reading. Neither
observes the parent-side control write after process termination has closed the
pipe's read end.

Microsoft's `WriteFile` page describes `ERROR_BROKEN_PIPE` after an anonymous-
pipe reader closes. Its system-error table separately defines `ERROR_NO_DATA`
232 as "the pipe is being closed." Python defines `BrokenPipeError` for writing
after the other end closes. Initial live probes instead showed
`OSError(errno.EINVAL)` through CPython's buffered stream and exact native
false/error 232 with zero bytes on this host. M159 adopts only that direct
native observation; it does not establish Python exception mapping, a
universal Windows error code, recovery, retry, or cancellation behavior.

## Decision

Accept the [Windows blocker broken-control-pipe
probe](../security/cache-cleanup-windows-broken-control-pipe-probe.md) as
current-host, test-only feasibility evidence.

Reuse M155's blocker child, release token, readiness parser, timeout, and
failure cleanup unchanged. Bind the pytest-owned root to handle-reported NTFS
and close the parent probe before launch. Start the exact current interpreter
with `-I -B`, the fixed helper, explicit pipes, `shell=False`, and
`close_fds=True`. After bounded exact-schema `ready`, require M154's unchanged
rename child to return false/32 while the blocker remains alive and namespace/
content remain unchanged.

Kill the blocker exactly once and require its bounded process wait to complete
with a nonzero result. Only after output EOF confirms child pipe closure, map
the parent stream's existing descriptor to its Windows handle and call
`WriteFile` exactly once with the existing one-byte release token. Require
false, exact `ERROR_NO_DATA` 232, and zero written bytes. Close the parent
writer normally and confirm it is closed. Then invoke the identical native
rename once, require true/0, and preserve content beneath ordinary `displaced`.

Do not change or add a helper, inject arbitrary pipe faults, write before the
bounded child wait and output EOF, accept a generic error or alternate code,
retry a write, use `communicate()`, sleep, add runtime subprocess or `ctypes`,
add a platform adapter or public capability, claim recovery, add a dependency,
or add workflow/CI allocation.

## Consequences

The current host now observes one case where the child-owned exclusion remains
effective before abrupt process termination, the process wait orders native
handle release, and a late fixed release write reports false/error 232 with
zero bytes before the identical rename succeeds. Parent stream closure remains
explicit and ordinary after the direct native observation.

The native false/error 232 result and operation order are fixed only for this
repository-owned fixture on the current host. This observation is not Python
exception-mapping behavior, arbitrary pipe failure, retry or recovery policy,
readiness or termination timeout, cancellation, native close failure, crash or
restart recovery, concurrent mutation safety, general exclusion, or platform
admission.

Windows is not admitted.

## Alternatives considered

- Write before the child wait. Rejected because the process boundary would be
  racy and could deliver a valid release rather than observe a closed reader.
- Require `BrokenPipeError`. Rejected after the live high-level probe produced
  `OSError(errno.EINVAL)` instead.
- Require native error 109. Rejected after the direct `WriteFile` observation
  returned exact `ERROR_NO_DATA` 232 with zero bytes; M159 records that current-
  host result without generalizing it.
- Use `communicate()`. Rejected because Python deliberately handles broken-pipe
  input internally and would hide the explicit late-write observation.
- Retry the release. Rejected because M159 observes failure and owns no
  recovery policy.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove exact M155 fixture reuse, fixed isolated launch,
bounded readiness, false/32 with a live blocker, unchanged denial state, one
kill, bounded nonzero wait, one post-wait native release write, exact
false/error 232 with zero bytes, explicit writer close, empty output, identical
true/0 retry, and content preservation. Architecture tests must preserve M158,
runtime, examples, scripts, dependencies, workflows, and wheel contents.
Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Microsoft: system error codes 0-499](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [Python: `BrokenPipeError`](https://docs.python.org/3/library/exceptions.html#BrokenPipeError)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0141](0141-probe-windows-invalid-control-token.md)
