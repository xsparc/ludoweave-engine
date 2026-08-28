# RFC-0157: probe Windows cooperative-lock pathname substitution

- **Status:** Accepted
- **Milestone:** M174
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that renames M173's live
coordination file while a shared participant remains active, creates a new
ordinary file at the original pathname, and proves the two file identities
form independent lock generations. Add no runtime or CI surface.

## Context

M173 proves a cooperative shared/exclusive byte-range barrier only when every
participant opens the same known file object. Its opens include
`FILE_SHARE_DELETE`, so another actor may request rename access while the
handles remain live. A pathname alone is not an object or generation identity.

Microsoft documents `LockFileEx` locks as ranges associated with open file
handles. `CreateFileW` documents that delete sharing permits later delete or
rename access, and `FILE_ID_INFO` provides a volume serial number plus 128-bit
file identifier for comparing open handles on one computer. `MoveFileExW`
moves an existing file or directory to another name. M174 combines only those
narrow contracts under pytest-owned storage.

## Decision

Accept the [Windows cooperative-lock substitution
probe](../security/cache-cleanup-windows-cooperative-lock-substitution-probe.md)
as current-host, test-only negative capability evidence.

Create M173's exact ordinary `live/coordination.lock`, retain one parent
identity handle, and start one unchanged M173 shared participant. A new fixed
isolated child accepts no argument or environment-selected behavior. It calls
`MoveFileExW` from `live/coordination.lock` to
`live/coordination.displaced`, creates a new ordinary
`live/coordination.lock` with null security attributes and all sharing, proves
the handle noninheritable, writes the exact original bytes, closes it, and
emits one bounded canonical result.

The parent must then prove:

1. the retained original handle and the displaced pathname have the same
   `FILE_ID_INFO` identity;
2. the replacement pathname has a different identity;
3. a fresh unchanged M173 shared participant can lock the replacement while
   the original participant remains live;
4. each participant independently refuses an exclusive lock on its own file
   identity with native error 33;
5. closing the replacement participant permits exclusive acquire/release on
   the replacement while the original participant still refuses exclusive
   ownership of the displaced original; and
6. only closing the original participant permits exclusive acquire/release on
   the displaced original.

Require exact bytes, bounded subprocesses and output, deterministic close,
noninheritable handles, explicit unlock, zero leaked parent lock ownership, no
sleeps, no retries, no shells, and no arbitrary path or command input.

## Consequences

The M173 cooperative primitive is substitution-sensitive. Participants that
resolve the same pathname before and after rename/replacement can join distinct
file identities and independent byte-range-lock generations. A replacement
participant can settle while an old-generation participant remains live.

This result does not defeat `LockFileEx` or its same-object semantics. It shows
that a future protocol cannot treat a reusable pathname as sufficient stable
coordination identity. Any later design must bind and revalidate root identity,
coordination identity, and generation through namespace mutation and fail
closed when those bindings change.

Windows is not admitted. Uncooperative actors, complete participant coverage,
generation issuance, retained-root binding, mapped views, abrupt-exit
settlement, delayed operating-system unlock, filesystem variation, recovery,
policy, receipts, and independent hosts remain unresolved.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Remove `FILE_SHARE_DELETE` from participant opens. Rejected as a design
  conclusion: it would change M173's tested primitive and still would not by
  itself establish complete subtree quiescence or recovery.
- Put the coordination file outside the mutable cache root. Deferred because
  root ownership, trusted placement, generation lifecycle, recovery, and
  policy remain unapproved.
- Promote a file-ID registry into runtime code. Rejected because the registry's
  authority, persistence, mutation ordering, and receipts remain undefined.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect this source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove the exact substitution result, identity
relationships, simultaneous old/new participants, independent refusal and
release, unchanged bytes, bounded settlement, and zero leaked ownership.
Architecture tests must preserve M173, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [M147 cleanup threat model](../security/cache-cleanup-threat-model.md)
- [RFC-0156](0156-probe-windows-cooperative-lock.md)
