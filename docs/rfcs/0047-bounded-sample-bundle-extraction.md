# RFC-0047: Bound sample-bundle extraction

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M64

## Context

The release smoke extracts the staged sample ZIP before exercising examples
from an installed wheel. Existing checks rejected unsafe paths and symbolic-link
entries, but extraction trusted an unbounded central-directory member count and
declared expansion size. It also used `ZipFile.read()`, which materialized a
complete expanded member in memory, and could write earlier entries before a
later entry failed validation.

Python's `zipfile` documentation explicitly warns that decompression bombs can
exhaust disk or memory. `ZipInfo.file_size` exposes each member's declared
uncompressed size, and `ZipFile.open()` exposes a binary stream suitable for
bounded copying.

The actual M63 staged sample bundle is well inside conservative limits: 50
members, 379,577 declared uncompressed bytes in total, and a 33,018-byte
largest member.

## Decision

Before extraction creates a directory or file, the release smoke preflights the
complete central directory and requires all of the following:

1. At most **256 members**.
2. At most **1 MiB** declared uncompressed size for one member.
3. At most **8 MiB** declared uncompressed size across all members.
4. Every member continues to satisfy the existing path-confinement and
   symbolic-link rejection rules.
5. Every member uses ZIP stored or deflated compression. BZIP2, LZMA, and
   unknown methods are rejected before extraction.

After the complete preflight succeeds, regular files stream from
`ZipFile.open()` to an exclusively selected temporary workspace in **64 KiB**
blocks. The copied byte count must exactly equal the member's declared
uncompressed size. A count or size violation fails before extraction starts.

The limit constants remain private to the release-smoke script. They are not
engine configuration, a public Python contract, or an archive-format promise.

## Boundary

M64 protects the trusted staged sample bundle consumed by the existing release
smoke. It does not create a general archive-extraction library or claim that ZIP
metadata is authenticated. The existing release checksum and manifest checks
remain responsible for staged-byte identity.

`zipfile` parses the central directory before this code can inspect its member
count, so the 256-member rule bounds admitted extraction work rather than the
library's initial archive-parsing allocation. A raw bounded ZIP parser is not
introduced.

CPython passes the requested output limit to its deflate decompressor, while
its BZIP2/LZMA paths decompress an input chunk without that output limit before
truncating to the declared remaining size. Admitting only stored and deflated
members is therefore part of the streaming memory boundary; a forged small
`file_size` cannot select those unbounded library paths.

Extraction still has no transactional cleanup or rollback guarantee after a
successful preflight. A later I/O, decompression, or declared-size mismatch can
leave partial output only inside the runner-owned temporary smoke directory.
Duplicate-name, case-folding, Unicode-normalization, encrypted-member, and
cross-platform filename-portability policies are otherwise unchanged and
outside this milestone.

M64 adds no workflow, runner allocation, action, permission, trigger,
credential, dependency, lock, version, runtime package/API, release mutation,
release authority, tag, release, or publication. Pull-request evidence is not
a real public release observation.

## Consequences

- An oversized central directory or declared expansion fails before the first
  extracted path is created.
- A valid member no longer requires memory proportional to its full expanded
  size.
- Exact copied-size validation fails closed if streamed bytes disagree with the
  preflight metadata.
- BZIP2, LZMA, and unknown compression methods fail before filesystem writes;
  stored and deflated members remain admitted.
- Current project sample bundles retain ample space below every admitted limit.

## Alternatives considered

- Keep whole-member reads and rely only on the staged ZIP checksum. Rejected
  because trusted identity does not bound resource consumption.
- Limit only compressed archive bytes. Rejected because compression ratio can
  make a small archive expand far beyond its stored size.
- Validate and extract in one pass. Rejected because a later invalid member
  would be discovered only after earlier filesystem writes.
- Add a third-party archive or sandbox dependency. Rejected because the
  standard library provides the bounded metadata and streaming seams required
  for this narrow smoke utility.
- Admit every standard-library ZIP codec. Rejected because CPython's BZIP2 and
  LZMA member readers do not pass a maximum-output length to their decompressor.
- Delete partial output after an extraction-time failure. Deferred because the
  output already lives in a disposable runner-owned temporary directory and
  cleanup semantics are a separate decision.

## References

- [Python 3.14 `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [RFC-0047 predecessor: subordinate-output confinement](0046-public-release-output-confinement.md)
