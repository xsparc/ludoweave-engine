# RFC-0160: probe Windows protected guardian handoff

- **Status:** Accepted
- **Milestone:** M177
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that holds M175's coordination
identity with a noninheritable guardian handle which omits delete sharing but
owns no byte-range lock. Require that guardian to bridge a participant-free
interval, admit a later protected participant on the same identity, and hand
namespace protection to that participant before closing. Add no runtime or CI
surface.

## Context

M175 proves that protected participants prevent pathname substitution only
through a continuous live-participant interval. M176 proves abrupt participant
settlement on the current host, but the coordination pathname becomes
replaceable after the final owner settles.

Microsoft documents that a `CreateFileW` handle's sharing options remain in
effect until that handle closes. Omitting `FILE_SHARE_DELETE` prevents later
opens requesting delete access, and delete access includes rename. A separate
non-range-locking handle can therefore be tested as an identity bridge while
the cooperative range has no participant.

The guardian must remain distinct from cooperative quiescence. `LockFileEx`
range ownership must be available while only the guardian exists and refused
only while a protected participant holds the shared range.

## Decision

Accept the [Windows protected guardian-handoff
probe](../security/cache-cleanup-windows-protected-guardian-handoff-probe.md)
as current-host, test-only evidence for one exact continuous ownership chain.

Create M173's fixed ordinary `live/coordination.lock` and capture its exact
`FILE_ID_INFO`. Open one private parent guardian for generic read with
read/write sharing, deliberately omit delete sharing, use null security
attributes, reject reparse identity, and prove the handle noninheritable.

With only the guardian present, require M174 substitution to fail with sharing
error 32 while M173 exclusive range acquire/release succeeds. Start M175's
unchanged protected participant, require exact `ready`, substitution error 32,
and exclusive-range error 33, then close it exactly.

While no participant owns the range and the guardian remains live, require the
same substitution refusal and successful exclusive acquire/release. Start a
second unchanged protected participant and prove a fresh handle still observes
the original identity. Close the guardian while that participant remains live;
require substitution error 32 and exclusive-range error 33 to persist.

After the participant closes exactly, require exclusive acquire/release and
then M174 substitution success. Prove the displaced file retains the original
identity, the replacement differs, both payloads remain exact, and every
handle, process, pipe, and range owner settles. Use no retry or sleep.

## Consequences

On the observed host, one continuous chain of compatible no-delete-share
handles protects the same coordination identity across a participant-free
range-lock interval and through guardian-to-participant handoff. The guardian
does not own the byte range and therefore does not itself establish
quiescence.

This is not generation authority, trusted placement, participant admission,
or crash recovery. The guardian is process-local and already live before the
observation begins. A guardian crash, hostile preexisting handle, startup race,
untrusted root, omitted participant, or later unprotected interval can still
break continuity. No cleanup or mutation authority is established.

Windows remains unadmitted. Mapped views, multiple guardians, arbitrary
process death, filesystem/driver variation, durable generation issuance,
revalidation at use, fail-closed policy, typed receipts, and independent-host
proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Promote a permanent runtime guardian. Rejected because ownership, trusted
  placement, startup, crash recovery, admission, and generation policy remain
  undesigned.
- Treat the guardian as an exclusive range owner. Rejected because that would
  prevent participant admission and conflate identity continuity with
  quiescence.
- Add another fixture. Rejected because M175's fixed participant already
  exercises the required child boundary.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect the source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove guardian-only substitution refusal and exclusive
range availability, first-participant range refusal, an exact participant-free
guardian interval, later-participant identity continuity, guardian release
with participant protection retained, final range settlement, substitution and
identity outcomes, byte preservation, and complete owner cleanup. Architecture
tests must preserve M176, runtime, examples, scripts, dependencies, workflows,
and the wheel package boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [M147 cleanup threat model](../security/cache-cleanup-threat-model.md)
- [RFC-0159](0159-probe-windows-cooperative-lock-abrupt-settlement.md)
