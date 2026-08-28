# RFC-0146: probe an inherited Windows blocker handle

- **Status:** Accepted
- **Milestone:** M163
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS fixture that passes a no-delete-share
directory handle to a fixed child through `STARTUPINFO.lpAttributeList`'s
explicit handle list. Restore the parent handle to noninheritable immediately
after process creation. Closing the parent's handle must leave M154's
unchanged native rename false/error 32 until the child closes its inherited
handle, after which the identical rename must return true/code zero with
content preserved. Add no runtime or CI surface.

## Context

M162 proves same-process duplicate retention but explicitly excludes
inheritance across process creation. Python documents that Windows
`handle_list` can explicitly pass selected handles when `close_fds=True`, and
that listed handles must be made temporarily inheritable. Microsoft documents
that an inherited handle refers to the same object and retains its access and
handle value in the child.

Python also warns that temporarily changing inheritability can leak handles
when process creation is concurrent. This milestone observes one serial,
explicitly allowlisted launch only. It does not establish a general or
concurrency-safe inheritance policy.

## Decision

Accept the [Windows inherited-handle
probe](../security/cache-cleanup-windows-inherited-handle-probe.md) as
current-host, test-only feasibility evidence.

The parent binds the pytest-owned root to handle-reported NTFS, opens ordinary
relative `live` without delete sharing, and creates a fixed child with the
current interpreter, `-I -B`, explicit pipes, `shell=False`, `close_fds=True`,
and a `STARTUPINFO` explicit handle list containing only that handle. It makes
the handle inheritable only around `Popen` and restores it to noninheritable in
`finally` before waiting for child readiness.

The child accepts exactly one canonical positive decimal handle value. It
emits exact `ready`, waits for fixed byte `!`, closes the inherited handle
exactly once, emits exact `closed`, and exits zero. Invalid arguments, invalid
control, and native close failure have separate nonzero exits. Failure cleanup
closes only a handle the fixture still owns.

After exact `ready`, require M154's unchanged native rename to return false/32.
Close the parent handle exactly once and require the identical second rename
to remain false/32 while the child is live, with namespace and content
unchanged. Send only `!`, close the parent writer, require exact `closed`,
bounded exit zero, stdout/stderr EOF, and one final identical rename returning
true/0 with content preserved beneath ordinary `displaced`.

Do not modify an accepted fixture, pass a path or environment value to the
child, inherit all handles, use arbitrary evaluation, use a timing sleep, kill
or terminate on the accepted path, use `communicate()`, add runtime subprocess
or `ctypes`, claim concurrent inheritance safety, add a dependency, or add
workflow/CI allocation.

## Consequences

The current host now observes that one explicitly inherited child handle keeps
the no-delete-share rename denial alive after the parent closes its handle.
Only the child's acknowledged close releases the observed denial.

This is not a concurrency-safe inheritance contract, cross-process
`DuplicateHandle` evidence, broad inheritance evidence, native close-failure
behavior, leak-freedom under concurrent launches, crash/restart recovery,
general exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Set `close_fds=False`. Rejected because it would permit broad inheritance
  rather than one explicit handle list.
- Leave the handle inheritable. Rejected because the parent must restore its
  local ownership metadata immediately after process creation.
- Modify M155 or M162's child. Rejected because their accepted protocols are
  protected history.
- Launch concurrent children. Rejected because Python documents a leakage
  hazard around temporary inheritability; concurrency needs a separate design.
- Add runtime ownership transfer. Rejected because M163 is admission evidence,
  not cleanup authority or production policy.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove canonical handle parsing, the exact child
schema/phases, explicit single-handle allowlisting, `close_fds=True`, immediate
inheritability restoration, false/32 before parent close, false/32 after
parent close while the child remains live, exact `closed`/zero/EOF after the
child close, one final true/0 rename, and content preservation. Architecture
tests must preserve M162, runtime, examples, scripts, dependencies, workflows,
and wheel contents. Supported-Python, full regression, installed-wheel,
reproducibility, release, documentation, governance, and findings-first gates
remain required.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: handle inheritance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handle-inheritance)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [Microsoft: `UpdateProcThreadAttribute`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0145](0145-probe-windows-duplicated-blocker-handle.md)
