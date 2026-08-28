# RFC-0156: probe Windows cooperative coordination locking

- **Status:** Accepted
- **Milestone:** M173
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe for a fixed coordination file and
one fixed byte range. Require multiple shared participants to coexist and
collectively refuse a fail-immediate exclusive cleanup participant until the
last shared owner closes. Require the exclusive owner to refuse a late shared
participant until exact release. Add no runtime or CI surface.

## Context

M171 proves incompatible sharing modes on the same directory object. M172
proves that the directory object does not recursively exclude separately
opened descendants. The M147 threat model still requires every cache reader,
writer, lease, pin, and publisher to participate in a cross-process
quiescence boundary before cleanup could be considered.

Microsoft documents `LockFileEx` as a shared or exclusive byte-range lock over
one opened file handle. Overlapping shared locks may coexist. An overlapping
exclusive lock cannot coexist with a lock held through a different handle,
and `LOCKFILE_FAIL_IMMEDIATELY` makes refusal synchronous rather than a wait.
The same documentation also states that mapped views bypass byte-range locks
and that process termination may not release a lock immediately. Those limits
must remain explicit.

## Decision

Accept the [Windows cooperative-lock
probe](../security/cache-cleanup-windows-cooperative-lock-probe.md) as
current-host, test-only positive evidence for one cooperative primitive.

Create one ordinary `live/coordination.lock` beneath an NTFS pytest root. Two
fixed isolated child processes each open only that relative file for generic
read access with read/write/delete sharing and null security attributes. Each
child proves its handle noninheritable, requests a shared fail-immediate lock
over byte zero with length one, emits exact bounded `ready`, waits for one
fixed release byte, explicitly unlocks, closes, emits exact bounded `closed`,
and exits zero. A refused shared request emits one exact bounded `refused`
document carrying native error 33 and exits zero.

The parent opens the same ordinary file with the same access and sharing,
rejects reparse identity, and requests an exclusive fail-immediate lock over
the identical range. Exercise both directions:

1. hold two shared child participants, require parent-exclusive error 33 while
   both remain live, close one participant, require the same refusal while the
   other remains live, then close the last participant and acquire/release the
   exclusive owner; and
2. hold the exclusive parent owner, require a late shared child to report
   refusal/error 33, release the exact exclusive owner, then require a fresh
   shared child to become ready and close normally.

Require unchanged coordination bytes, exact range and flags, noninheritable
handles, deterministic independent close, bounded process/stream settlement,
and zero leaked parent ownership. Use no sleeps, retries, shells, broad handle
inheritance, path arguments, environment-selected behavior, arbitrary
commands, or unbounded output.

## Consequences

The current NTFS host provides one promising cooperative building block:
multiple shared participants can represent active users of a single known
coordination object, while an exclusive participant can observe quiescence
only after the last shared owner releases. The inverse exclusion also holds.

This is not cleanup authority. An uncooperative process can ignore the
coordination file. The probe does not bind the file identity to a cache root or
generation, protect it from substitution, prove complete retained roots,
cover mapped views, survive abrupt exit or native unlock failure, define wait
or cancellation policy, or provide recovery and receipts. Windows is not
admitted.

No runtime API, value, protocol, decoder, CLI command, public probe,
production subprocess or `ctypes`, dependency, workflow, permission, or
hosted check is added.

## Alternatives considered

- Extend the M171 directory owner to descendants. Rejected by M172's observed
  object-specific non-exclusion.
- Use only `CreateFile` sharing modes on a coordination file. Deferred because
  `LockFileEx` directly models overlapping shared and exclusive participants
  over an exact range and makes the mapped-view caveat explicit.
- Adopt Python `msvcrt.locking` directly. Rejected for this milestone because
  its documented surface does not establish the complete shared/exclusive,
  ownership, identity, and recovery contract required for admission.
- Promote the primitive into a private runtime adapter now. Rejected because
  participant completeness, generation binding, retained roots, substitution,
  recovery, policy, and receipts remain jointly unresolved.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect this source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove the fixed coordination path and one-byte range,
all-sharing opens, null security attributes, shared/shared coexistence,
shared/exclusive refusal through the last participant, exclusive/shared
refusal, exact native error, explicit unlock, deterministic close, unchanged
content, bounded output/waits, and zero leaked handles or streams.
Architecture tests must preserve M172, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `UnlockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-unlockfileex)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Python: `msvcrt`](https://docs.python.org/3.14/library/msvcrt.html)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [M147 cleanup threat model](../security/cache-cleanup-threat-model.md)
- [RFC-0155](0155-probe-windows-descendant-non-exclusion.md)
