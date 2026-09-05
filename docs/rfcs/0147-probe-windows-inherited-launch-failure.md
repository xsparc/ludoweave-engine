# RFC-0147: probe Windows inherited-handle launch failure

- **Status:** Accepted
- **Milestone:** M164
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS probe that temporarily marks a
no-delete-share directory handle inheritable, puts only that handle in a
`STARTUPINFO` explicit handle list, and attempts to start one fixed missing
executable. Require a real process-creation failure, immediate restoration to
noninheritable, continued parent ownership and native rename denial, then
true/code-zero rename only after the parent closes its handle. Add no runtime
or CI surface.

## Context

M163 observes successful explicit handle inheritance and hardens its test
harness against an inheritability-restoration exception after a successful
spawn. It does not observe the more common boundary where `Popen` itself fails
after the parent has temporarily changed handle inheritability.

Python documents that a non-empty Windows `handle_list` requires
`close_fds=True`, listed handles must be temporarily inheritable, and invalid
process-creation inputs raise `OSError` subclasses. Microsoft documents that
`CreateProcessW` returns zero on failure and exposes extended error
information. Those facts support one real missing-executable failure and
rollback observation. They do not prove arbitrary failure or concurrency
safety.

## Decision

Accept the [Windows inherited-launch failure
probe](../security/cache-cleanup-windows-inherited-launch-failure-probe.md) as
current-host, test-only feasibility evidence.

The test binds its pytest-owned root to handle-reported NTFS, creates ordinary
relative `live`, and opens one no-delete-share handle. It confirms the fixed
missing executable does not exist and the handle is initially noninheritable.
It then builds a `STARTUPINFO` explicit handle list containing only that
handle, marks it inheritable, and calls `Popen` with the fixed absolute missing
executable as both the sole argument and explicit executable, `shell=False`,
`close_fds=True`, the trusted temporary root as working directory, and all
three standard streams set to `DEVNULL`.

The call must raise exact `FileNotFoundError` with current-host errno
`ENOENT`/Windows error 2. A `finally` boundary restores the handle to
noninheritable before the error is returned to the test. Unexpected process
creation is closed and reaped before failure. An exception while restoring
after an unexpected spawn likewise closes and reaps that process.

After the failed launch, require the handle noninheritable, parent owned count
one, the missing path still absent, and M154's unchanged native rename
false/error 32 with namespace and content unchanged. Close the parent handle
exactly once, require owned count zero, and require the identical second rename
true/code zero with content preserved beneath ordinary `displaced`.

Do not modify an accepted fixture, create an executable, use `shell=True`,
search `PATH`, pass an environment, inherit all handles, use arbitrary
evaluation, inject a restoration failure, run concurrent launches, add runtime
subprocess or `ctypes`, claim general rollback safety, add a dependency, or add
workflow/CI allocation.

## Consequences

The current host now observes that one real missing-executable process-
creation failure restores the parent handle to noninheritable while preserving
its ownership and no-delete-share denial until explicit close.

This is not restoration-failure injection, arbitrary `CreateProcessW` failure
coverage, leak-freedom under concurrent launches, a concurrency-safe
inheritance contract, invalid-handle evidence, child-crash behavior, recovery,
general exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Monkeypatch `Popen` to raise. Rejected because it would not exercise a real
  process-creation failure on the current host.
- Pass a noninheritable handle. Rejected because Python documents that as a
  different invalid-parameter boundary.
- Inject failure into `os.set_handle_inheritable(..., False)`. Rejected because
  restore-failure ownership needs a separate controlled design.
- Run several simultaneous launches. Rejected because M163 explicitly leaves
  Python's documented concurrent-inheritance hazard unresolved.
- Add runtime retry or recovery. Rejected because M164 is admission evidence,
  not production cleanup authority.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this probe after the unpublished stack is safely integrated.

## Validation

Focused validation must prove a fixed absent executable, one explicitly listed
handle, initial and restored noninheritability, exact failure mapping, no
returned process, retained parent ownership, false/32 before parent close,
true/0 only after parent close, and content preservation. Architecture tests
must preserve M163, runtime, examples, scripts, dependencies, workflows, and
wheel contents. Supported-Python, full regression, installed-wheel,
reproducibility, release, documentation, governance, and findings-first gates
remain required.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [Microsoft: handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0146](0146-probe-windows-inherited-blocker-handle.md)
