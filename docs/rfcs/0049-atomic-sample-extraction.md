# RFC-0049: Stage sample extraction before publication

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M66

## Context

M64 bounds and streams admitted sample-ZIP content, and M65 gives every member
one portable collision-free path before extraction. Once those preflights pass,
the release smoke currently writes each member directly beneath the final
sample root. A later streamed-size mismatch, decompression or I/O failure, or
incomplete required-file set can therefore leave a partial tree at the path
that denotes a complete extracted bundle.

The production caller already creates an empty runner-owned output directory
inside its disposable release-smoke temporary directory. This permits staging
and publication on the same filesystem without expanding public API or release
authority.

## Decision

The release smoke requires the supplied output parent to be an existing real
directory. The versioned final sample root must not already exist as a file,
directory, live symbolic link, or dangling symbolic link. These preconditions
fail with stable content-silent categories before archive content is opened or
any owned extraction path is created.

After the complete M64/M65 archive preflight, extraction creates an owned
temporary staging directory directly beneath that output parent. Every admitted
member is streamed beneath the expected root inside that directory. Required-
file completeness is validated against the staged root, not the final sample
root. Only a complete staged root is published to the absent final path with a
single same-filesystem rename.

The temporary-directory context owns pre-publication cleanup. A streamed-size,
decompression, write, completeness, or rename failure removes the partial
staging tree while leaving the final sample root absent. Existing output entries
are neither replaced nor removed. The original extraction, validation, or
publication exception remains observable.

## Boundary

M66 is private release-smoke handling for a project-produced sample bundle in a
single-thread, runner-owned temporary workspace. It is not a general archive
sandbox, filesystem transaction, or recovery journal. The single rename is a
visibility boundary, not crash-durable storage. M66 does not call `fsync`,
recover after process or host termination, roll back after successful
publication, isolate races with concurrent filesystem actors, or clean paths it
did not create.

The parent-directory check does not prove mount identity or protect against a
privileged actor replacing ancestors. Archive metadata remains protected by the
existing staged-release checksum and manifest boundary. Pull-request evidence
is not a real public release observation.

M66 adds no workflow, runner allocation, action, permission, trigger,
credential, dependency, lock, version, runtime package/API, sample producer,
release mutation, release authority, tag, release, or publication.

## Consequences

- A failed copy or incomplete bundle cannot leave a partial final sample root.
- A publication failure cleans the owned temporary staging directory and
  preserves its cause.
- An existing final entry, including a dangling link, fails before archive
  content is opened and remains unchanged.
- Successful extraction exposes exactly one complete versioned root beneath the
  caller-owned output directory.
- The random private staging name does not enter output, diagnostics, receipts,
  or release artifacts and therefore does not change deterministic results.

## Alternatives considered

- Delete the final root after a direct-extraction failure. Rejected because the
  final identity becomes partially visible and cleanup must distinguish owned
  paths from pre-existing collisions.
- Extract directly and write a completion marker last. Rejected because callers
  could still observe or execute a partial tree and every consumer would need
  marker enforcement.
- Copy a completed tree into the final path. Rejected because a copy recreates a
  partial-publication window and uses more I/O than a same-filesystem rename.
- Replace an existing final root. Rejected because verifier-owned cleanup must
  never overwrite or remove a path it did not create.
- Add journaling, locking, or crash recovery. Deferred because the production
  caller owns a disposable single-process temporary workspace and no evidence
  justifies that broader system.

## References

- [RFC-0048: constrain sample-bundle member paths portably](0048-portable-sample-member-paths.md)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [Python `tempfile` documentation](https://docs.python.org/3/library/tempfile.html)
- [Python `os.replace` documentation](https://docs.python.org/3/library/os.html#os.replace)
