# RFC-0068: Require exact conventional central-directory placement

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample producer writes one conventional ZIP archive from
byte zero. Its final 22-byte end-of-central-directory record declares a
central-directory size and offset whose sum is exactly the absolute offset of
that final record.

PKWARE APPNOTE sections 4.4.23 and 4.4.24 define the conventional central-
directory size and starting offset. Current CPython deliberately computes a
`concat` adjustment from the final-record location minus those two values so
ZIP data can follow prepended bytes. Supported CPython 3.12.13, 3.13.13, and
3.14.5 each expose and read the same payload when one or eleven bytes are
prepended; the parsed member header offset moves by exactly the prefix length.

That broad compatibility is not needed by the fixed release producer and
widens the admitted container profile before extraction.

## Decision

Private complete release smoke reads the final conventional record through the
shared position-restoring structural helper. It requires
`central_directory_size + central_directory_offset` to equal the absolute
offset of that final record. Any nonzero adjustment raises stable content-
silent error `sample bundle central directory placement is inconsistent`.

Complete release smoke first finishes every established M69-M82 policy, M83
archive disk policy, and M84 archive entry-count policy. M85 then validates
placement before M77 decoded-name policy, member metadata, exact inventory,
staging, or member reads. The existing `ExitStack` closes the source, snapshot,
and archive before an error returns.

The shared helper validates exactly the final 22-byte record's signature and
zero comment length and restores the previous snapshot position. Structural
mismatch retains the existing content-silent ZIP-data error.

## Boundary

M85 checks one arithmetic relationship among the snapshot length and two
conventional final-record fields. It adds no central-directory record parser,
no local-header parser, no end-record search, no ZIP64 end-record parser or
sentinel resolution, no binary-format classifier, no self-extracting archive
support, no prepended executable support, and no multi-volume assembler.

M85 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- Any nonzero concatenation adjustment or contradictory conventional placement
  geometry fails before decoded names, metadata, inventory, staging, or reads.
- Every established flag, extra-field, comment, member-volume, archive-disk,
  and entry-count error retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled size, offset, member name, or path.
- Generic concatenated and self-extracting ZIP compatibility remains available
  through Python itself but outside this private release-bundle profile.
- Exact individual central-directory record grammar remains deferred.

## Alternatives considered

- Continue accepting CPython's concatenated-archive adjustment. Rejected
  because the fixed producer starts at byte zero and needs no prepended data.
- Reject a short list of executable signatures. Rejected because content
  classification is incomplete and the exact zero-adjustment invariant is
  simpler.
- Parse every central-directory record and recompute its byte span. Rejected
  because this milestone needs only the fixed producer's placement invariant.
- Add self-extracting ZIP support. Rejected because it introduces executable
  container semantics unrelated to the release sample bundle.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0067: require consistent archive entry counts](0067-require-consistent-archive-entry-counts.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
