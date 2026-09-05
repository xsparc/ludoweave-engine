# RFC-0140: probe Windows blocker control-pipe EOF closure

- **Status:** Accepted
- **Milestone:** M157
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS probe that closes the parent writer for
M155's fixed blocker control pipe after readiness. Require the unchanged native
rename probe to report false/32 while the blocker is alive, wait with a fixed
bound for the helper's existing invalid-control exit, require no graceful-close
acknowledgement, and then require the identical rename to report true/0 with
content preserved. Preserve the no-admission decision and add no runtime or CI
surface.

## Context

M155 proves explicit acquisition and valid-token release. M156 bypasses the
helper's user-mode cleanup by terminating its process. Neither observes the
existing helper's `finally` close when the control pipe reaches EOF instead of
delivering the fixed release byte.

Microsoft documents that an anonymous-pipe read returns when every write handle
closes. Its handle-inheritance guidance specifically requires the child not to
inherit a writer, because such inheritance prevents EOF. Python documents that
`stdin=PIPE` creates a pipe to the child, `close_fds=True` prevents unrelated
Windows handle inheritance while allowing explicit standard-stream
redirection, and `wait(timeout=...)` bounds the process wait.

## Decision

Accept the [Windows blocker control-pipe EOF
probe](../security/cache-cleanup-windows-control-pipe-eof-probe.md) as
current-host, test-only feasibility evidence.

Reuse M155's blocker child, readiness parser, timeout, and failure cleanup
unchanged. Bind the pytest-owned root to handle-reported NTFS and close the
parent probe before launch. Start the exact current interpreter with `-I -B`,
the fixed helper, explicit pipes, `shell=False`, and `close_fds=True`. After
bounded exact-schema `ready`, require M154's unchanged rename child to return
false/32 while the blocker remains alive and namespace/content remain
unchanged.

Write no byte to the control pipe. Close only the parent `Popen.stdin` stream,
confirm it is closed, wait with the existing fixed timeout, and require the
helper's existing exit code 4. Require EOF with no `closed` acknowledgement and
no stderr. Only after the wait may the identical rename helper retry; require
true/0 and unchanged content beneath ordinary `displaced`.

Do not modify or add a helper, inject a wrong byte, retry, sleep, add runtime
subprocess or `ctypes`, add a platform adapter or public capability, claim
recovery, add a dependency, or add workflow/CI allocation.

## Consequences

The current host now observes one case where the child-owned exclusion remains
effective before control-channel EOF and the helper's existing `finally` close
releases the handle before its bounded nonzero exit. The identical rename then
succeeds without process termination or a valid release acknowledgement.

Exit code 4 is fixed only for this repository-owned fixture protocol. This
observation is not arbitrary pipe failure, broken-pipe write behavior,
readiness or termination timeout, cancellation, native close failure, crash or
restart recovery, concurrent mutation safety, general exclusion, or platform
admission.

Windows is not admitted.

## Alternatives considered

- Send an invalid byte. Rejected because EOF is the remaining bounded
  control-channel condition and writing data would exercise a different case.
- Use `communicate()`. Rejected because this probe needs an explicit close-only
  transition and an independently bounded process wait.
- Modify the helper to acknowledge invalid control. Rejected because M157 must
  exercise M155's existing closure behavior unchanged.
- Retry until rename succeeds. Rejected because the child process wait is the
  only accepted ordering boundary.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove exact M155 fixture reuse, fixed isolated launch,
bounded readiness, false/32 with a live blocker, unchanged denial state, no
control write, explicit writer close, bounded wait, exact fixture exit 4, no
close acknowledgement, identical true/0 retry, and content preservation.
Architecture tests must preserve M156, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full regression,
installed-wheel, reproducibility, release, documentation, governance, and
findings-first gates remain required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0139](0139-probe-windows-abrupt-blocker-termination.md)
