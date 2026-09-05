# Windows cache-cleanup exclusive-root acquisition probe

- **Status:** Accepted current-host acquisition evidence; Windows is not admitted
- **Milestone:** M171
- **Date:** 2026-08-29
- **Baseline:** M170's concurrent explicit-list abrupt-termination probe

## Decision

Retain one Windows-only, test-only controlled observation of both directions
around a directory handle opened with sharing mode zero. The retained owner
must deny one late child open until close. One existing fixed child participant
must deny the parent's exclusive acquisition until its acknowledged close.
Windows is not admitted.

## Why two-way acquisition matters

M153 observes one parent no-delete-share handle blocking a child rename. M155
observes the same exclusion when the child owns that handle. Neither proves
that a no-sharing acquisition refuses an existing participant instead of
silently weakening, or that a successfully acquired no-sharing owner refuses
a later participant.

Microsoft's sharing contract is bidirectional. A new desired access must be
compatible with every existing handle's sharing flags, and a new share mode
must be compatible with the access held by every existing handle. Error 32 is
the expected fail-closed result for either conflict. Close is the only accepted
release boundary in this probe.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_exclusive_root_acquisition_probe.py`:

1. creates an ordinary `live/candidate.bin` below an NTFS pytest root;
2. opens `live` with list/read-attribute/synchronize access, sharing mode zero,
   backup semantics, open-reparse-point behavior, and null security attributes;
3. rejects a reparse identity, adopts the exact handle, and proves it is
   noninheritable;
4. runs one fixed isolated child with `close_fds=True`, `shell=False`, bounded
   output, a fixed script, and the pytest root as working directory;
5. requires the child all-sharing open to return exact false/error 32 while the
   owner remains held, then exact true/error zero after deterministic release;
6. starts M155's unchanged fixed child, consumes exact `ready`, and requires
   the parent zero-sharing acquisition to raise the existing native error with
   code 32 while adopting no handle;
7. proves that child remains live and content remains unchanged;
8. sends the existing one-byte release, consumes exact `closed`, requires zero
   exit, and repeats the parent acquisition successfully;
9. proves the new parent handle noninheritable and closes it once; and
10. settles every handle, process, stream, and temporary owner with fixed
    bounds and preserves the candidate bytes.

`tests/fixtures/windows_exclusive_directory_open_child.py` accepts no argument,
path, command, or environment value. It attempts only the fixed relative name
`live`, emits one bounded canonical document, closes any acquired handle before
success, and never returns native objects or filesystem paths.

## Executed evidence

On the current Windows CPython 3.12 host, both distinct
ownership directions return exact sharing-violation denial while the competing
owner is live. Each identical acquisition succeeds only after that owner
closes. Every returned parent handle is noninheritable, both child processes
settle, all private owners close, and both candidate payloads remain unchanged.

## Missing admission evidence

M171 is not a complete cache quiescence capability. Remaining work includes:

- attribute-only opens, write/delete access permutations, mapped files,
  descendant handles, multiple readers/writers, and unrelated cooperating or
  noncooperating processes;
- oplocks, leases, cancellation, timeout, process death, handle duplication or
  explicit inheritance, and native close failure at this exact acquisition;
- ancestor substitution, mount/reparse variation, hard links, file-ID reuse,
  NTFS variants, ReFS, Dev Drive, removable media, and remote shares;
- retained roots, pins, publication, generation, policy, trusted time,
  candidate identity, and bounded work design;
- quarantine collision, disk-full, permission, crash, retry, restore,
  finalize, durable receipts, and recovery; and
- an accepted private adapter ABI plus independent installed-host evidence.

Sharing mode zero is therefore one observed primitive, not a lock API, lease,
cleanup authority, general exclusion claim, or platform admission.

## Scope and CI restraint

M171 adds no runtime subprocess or `ctypes`, adapter, public probe, cache
access, candidate disclosure, cleanup authority, mutation command, dependency,
native extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Python: handle inheritance](https://docs.python.org/3/library/os.html#inheritance-of-file-descriptors)
- [M153 share-delete exclusion probe](cache-cleanup-windows-share-delete-exclusion-probe.md)
- [M155 child-owned blocker probe](cache-cleanup-windows-child-owned-share-delete-handshake.md)
- [M170 abrupt-termination isolation probe](cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md)
