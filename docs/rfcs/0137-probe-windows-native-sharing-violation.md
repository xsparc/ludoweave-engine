# RFC-0137: probe the Windows native sharing-violation result

- **Status:** Accepted
- **Milestone:** M154
- **Date:** 2026-08-28

## Summary

Add one test-only NTFS fixture that executes a fixed `MoveFileExW` rename in an
isolated child process and captures its native last-error code directly. Require
`ERROR_SHARING_VIOLATION` while the parent withholds delete sharing and require
success after deterministic close. Preserve the no-admission decision and add
no runtime or CI surface.

## Context

M153 pairs a failed `cmd.exe` rename with successful execution of the identical
command after the blocking handle closes. That fixture deliberately observes
only the command exit and namespace result, so it cannot identify the native
failure returned by the rename operation.

Microsoft documents that `MoveFileExW` renames files or directories, returns
zero on failure, and requires immediate `GetLastError` capture for extended
information. Microsoft identifies system error 32 as
`ERROR_SHARING_VIOLATION`, while warning that exact error returns can vary by
operating system or driver. The new result must therefore remain explicitly
host-bound.

## Decision

Accept the [Windows native sharing-violation
probe](../security/cache-cleanup-windows-native-sharing-violation-probe.md) as
current-host, test-only feasibility evidence.

The parent must retain M153's ordinary NTFS `live` directory handle opened with
read and write sharing but without delete sharing. It must launch its exact
current interpreter with `-I -B` and one fixed repository-owned helper script.
The helper accepts no argument or input, uses only the relative names `live`
and `displaced`, calls `MoveFileExW` with zero flags, and immediately captures
the last-error value only after failure.

The child may emit only one bounded exact-schema JSON document containing the
success flag and non-negative native code. The first result must be false/32
and leave namespace and content unchanged. After the parent closes the blocker,
the identical child invocation must return true/0 and place the unchanged
candidate under `displaced`.

Do not use `-c`, stdin, caller arguments, environment-selected behavior,
localized text parsing, polling, sleeps, concurrent timing, handle inheritance,
runtime subprocess or `ctypes`, a platform adapter, public capability value,
cleanup authority, dependency, workflow, or Windows admission.

## Consequences

The current host now directly observes one `MoveFileExW` sharing violation and
its release transition across a process boundary. The exact structured result
is path-free, bounded, and independent of localized command diagnostics.

This is one current-host native error observation. It does not establish that
every Windows version, filesystem, driver, rename API, or namespace condition
returns code 32. It is not general cross-process exclusion, quiescence, a
controlled race, a selected interleaving, an oplock protocol, or platform
admission. Competing actors, duplicated handles, filesystem variation,
recovery, policy, receipts, and independent hosts remain open.

Windows is not admitted.

## Alternatives considered

- Parse `cmd.exe` stderr. Rejected because messages are locale-dependent and do
  not provide direct native-call evidence.
- Execute native code with `python -c`. Rejected because an inline evaluation
  surface is unnecessary; the fixed exercised helper is easier to review and
  isolate.
- Generalize error 32 as a portable contract. Rejected because Microsoft warns
  that function error codes may vary across systems and drivers.
- Add a dedicated hosted job. Rejected because the existing Windows suite can
  execute this source test after the unpublished stack is safely integrated.
- Implement a runtime adapter. Rejected because M147's wider admission and
  recovery requirements remain incomplete.

## Validation

Focused validation must prove NTFS binding, omission of delete sharing, fixed
isolated script execution, no inherited native handle, strict bounded output,
direct false/32 observation, unchanged denial state, explicit handle release,
direct true/0 observation, and deterministic close. Architecture tests must
preserve M153, runtime, examples, scripts, dependencies, workflows, and wheel
contents. Supported-Python, full regression, installed-wheel,
reproducibility, release, documentation, governance, and findings-first gates
remain required.

## References

- [`MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [`GetLastError`](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror)
- [`CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [System error codes](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [Python command-line isolation](https://docs.python.org/3/using/cmdline.html#cmdoption-I)
- [Python `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [RFC-0136](0136-probe-windows-share-delete-exclusion.md)
