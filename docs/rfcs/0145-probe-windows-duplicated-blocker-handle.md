# RFC-0145: probe a duplicated Windows blocker handle

- **Status:** Accepted
- **Milestone:** M162
- **Date:** 2026-08-28

## Summary

Add one Windows-only, test-only NTFS fixture that opens a no-delete-share
directory handle and creates a noninheritable same-process duplicate with
`DuplicateHandle` and `DUPLICATE_SAME_ACCESS`. Closing only the original must
leave M154's unchanged native rename false/error 32. Closing the final
duplicate must permit the identical rename with true/code zero and content
preserved. Add no runtime or CI surface.

## Context

M153-M161 exercise one native blocker handle at a time. Their explicit close,
pipe, termination, and wait boundaries do not prove whether a duplicate of the
same handle keeps the native object and its share-mode denial alive after the
original handle closes.

Microsoft documents that `DuplicateHandle` creates a distinct handle referring
to the same object, that `DUPLICATE_SAME_ACCESS` preserves access, and that
duplicating a handle increases the object's reference count. Microsoft also
documents that `CloseHandle` decrements the handle count, that applications
should close each opened handle once, and that `CreateFileW` sharing options
remain effective until the associated handle closes. Those facts support one
same-process duplicate-lifetime observation. They do not establish inherited
or cross-process handle behavior.

## Decision

Accept the [Windows duplicated-handle
probe](../security/cache-cleanup-windows-duplicated-handle-probe.md) as
current-host, test-only feasibility evidence.

Add one fixed standalone child fixture. It opens ordinary relative `live`
without delete sharing, obtains the `GetCurrentProcess` pseudo handle, and
duplicates the directory handle in the same process with
`DUPLICATE_SAME_ACCESS` and inheritance disabled. Only after both handles exist
may it emit exact `ready`.

The fixed `1` token closes the original handle exactly once and emits exact
`original-closed` while retaining the duplicate. The fixed `2` token closes
the duplicate exactly once, emits exact `closed`, and exits zero. Invalid
tokens and native duplicate/close failures retain separate nonzero fixture
exits. Failure cleanup closes only handles that remain owned.

The parent binds the pytest-owned root to handle-reported NTFS and closes its
probe before launch. It starts the current interpreter with `-I -B`, the fixed
helper, explicit pipes, `shell=False`, and `close_fds=True`. After exact
`ready`, require M154's unchanged rename to return false/32. Send and flush
only `1`, require bounded exact `original-closed`, a live child, and the
identical second false/32 result with namespace and content unchanged.

Send and flush only `2`, close the parent writer, require bounded exact
`closed`, bounded child exit zero, stdout/stderr EOF, and one final identical
rename returning true/0 with content preserved beneath ordinary `displaced`.

Do not modify an accepted fixture, use a timing sleep, kill or terminate on the
accepted path, use `communicate()`, add runtime subprocess or `ctypes`, add an
adapter or public capability, claim inherited/cross-process handle behavior,
add a dependency, or add workflow/CI allocation.

## Consequences

The current host now observes that closing one of two same-process handles to
the same no-delete-share directory object leaves the native rename denial in
force. Only closing the final duplicate releases the observed denial.

This is not inherited-handle evidence, cross-process duplication evidence,
general reference-count verification, native close-failure behavior, oplock
or lease behavior, crash/restart recovery, concurrent mutation safety,
general exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Open the path twice. Rejected because two independent `CreateFileW` calls do
  not isolate `DuplicateHandle` lifetime semantics.
- Modify M155 or M161's child. Rejected because their accepted protocols are
  protected history.
- Make the duplicate inheritable. Rejected because inherited-handle behavior
  is a distinct process-creation boundary.
- Duplicate into another process. Rejected because cross-process transfer and
  ownership require a separate protocol and failure model.
- Add runtime duplicate tracking. Rejected because M162 is admission evidence,
  not cleanup authority or policy.
- Add a hosted job. Rejected because the existing Windows suite can execute
  this test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove fixed helper bytes/schema/phases, a
noninheritable same-access duplicate before `ready`, exact one-time accepted
closure of the original and duplicate, fixed isolated launch, bounded phase
parsing, false/32 before close, false/32 after only the original closes, exact
`closed`/zero/EOF after the duplicate closes, one final true/0 rename, and
content preservation. Architecture tests must preserve M161, runtime,
examples, scripts, dependencies, workflows, and wheel contents.
Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `DuplicateHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [Microsoft: `GetCurrentProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentprocess)
- [Microsoft: handle inheritance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handle-inheritance)
- [Microsoft: `CreateFileW` sharing](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0144](0144-probe-windows-acknowledged-release-timeout.md)
