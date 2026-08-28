# RFC-0158: probe Windows live coordination-substitution exclusion

- **Status:** Accepted
- **Milestone:** M175
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that combines M173's cooperative
shared byte-range lock with an open that omits `FILE_SHARE_DELETE`. Require two
live participants to preserve both cooperative exclusive-lock refusal and M174
rename/replacement refusal through the final participant close. Then prove the
coordination identity can still be replaced in the zero-participant window.
Add no runtime or CI surface.

## Context

M174 proves that M173's all-sharing participants permit the coordination
pathname to be renamed and rebound while a participant remains live, splitting
the protocol across independent file identities. Microsoft documents that an
open handle's sharing options persist until close and that omitting
`FILE_SHARE_DELETE` prevents later opens requesting delete access. Delete
access includes rename.

M153 and M154 established that same principle for an ordinary directory. M175
tests the narrower interaction needed here: multiple shared `LockFileEx`
participants on one coordination file, an incompatible exclusive range owner,
and a direct native substitution attempt against that exact file.

## Decision

Accept the [Windows live substitution-exclusion
probe](../security/cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md)
as current-host, test-only positive evidence for one live-participant window
and negative evidence for quiescent continuity.

Create M173's exact ordinary `live/coordination.lock`. Start two fixed isolated
children. Each child opens only that relative file for generic read with
`FILE_SHARE_READ | FILE_SHARE_WRITE`, deliberately omitting delete sharing,
and null security attributes. Each proves its handle noninheritable, requests
the unchanged shared fail-immediate lock over byte zero/length one, emits exact
bounded `ready`, waits for one release byte, explicitly unlocks and closes,
emits exact bounded `closed`, and exits zero.

While both children remain live, run M174's unchanged fixed substitution child
and require `rename_failed` with native error 32. Also require M173's unchanged
parent-exclusive range request to fail with native error 33. Close one child
exactly and require both refusals again while the second child remains live.

After the final child closes, require parent-exclusive acquire/release on the
unchanged original identity. Then run the exact M174 substitution child and
require success. Use retained `FILE_ID_INFO` evidence to prove the displaced
file retains the original identity while the replacement differs. Preserve
both files' exact bytes and settle every handle, process, pipe, and lock owner.

Use no sleeps, retries, shells, broad inheritance, path arguments,
environment-selected behavior, arbitrary commands, or unbounded output.

## Consequences

Omitting delete sharing can prevent M174's substitution while at least one
protected participant owns the coordination file. It does not weaken M173's
shared/shared coexistence or exclusive-range refusal in the observed case.

This is not stable generation authority. Once the last protected participant
closes, the pathname can be renamed and replaced before a later participant
opens it. A future protocol still needs a trusted retained root, a durable or
otherwise authoritative generation binding, identity revalidation, complete
participant admission, recovery, and fail-closed mutation ordering.

Windows is not admitted. Uncooperative actors, preexisting hostile handles,
mapped views, abrupt-exit settlement, delayed operating-system release,
filesystem variation, policy, receipts, and independent hosts remain
unresolved.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Treat no-delete-sharing as the final coordination design. Rejected because
  the zero-participant substitution window and authority/recovery lifecycle
  remain unresolved.
- Hold one process-global handle permanently. Deferred because ownership,
  startup, shutdown, crash recovery, independent process coordination, and
  generation policy are undefined.
- Move the coordination file outside the cache root. Deferred because trusted
  placement and root/generation binding remain unapproved.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect this source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove two protected participants coexist, native
rename error 32 and exclusive-lock error 33 persist through the final live
participant, exclusive ownership succeeds after the final close, substitution
then succeeds, identities split exactly, bytes remain unchanged, and every
owner settles. Architecture tests must preserve M174, runtime, examples,
scripts, dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [M147 cleanup threat model](../security/cache-cleanup-threat-model.md)
- [RFC-0157](0157-probe-windows-cooperative-lock-substitution.md)
