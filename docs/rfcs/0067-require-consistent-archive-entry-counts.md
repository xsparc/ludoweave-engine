# RFC-0067: Require consistent archive entry counts before extraction

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample bundle contains 50 regular files in one conventional
ZIP archive. Its final 22-byte end-of-central-directory record declares 50
entries on the current disk and 50 total entries, matching the 50 central-
directory entries exposed by the standard reader.

PKWARE APPNOTE sections 4.3.16, 4.4.21, and 4.4.22 define the two conventional
entry-count fields. `0xFFFF` defers the corresponding count to a ZIP64 end
record. Current CPython parses the fields but does not consult them in
`ZipFile._RealGetContents()`. Supported CPython 3.12.13, 3.13.13, and 3.14.5
each expose one readable member when the conventional pair is patched to zero,
made asymmetric, inflated to two, or set to `0xFFFF`.

## Decision

Private complete release smoke reads exactly the final conventional 22-byte
end-of-central-directory record from its owned checksum-admitted snapshot. It
requires both the current-disk entry count and total entry count to equal the
number of members already exposed by the standard reader. A mismatch raises
stable content-silent error
`sample bundle archive entry counts are inconsistent`.

Complete release smoke first finishes every established M69-M82 policy
and M83 archive disk-field policy. M84 then validates the counts before M77
decoded-name policy, member metadata, exact inventory validation, staging, or
member reads. Its temporary seek restores the snapshot position. The existing
`ExitStack` closes the source, snapshot, and archive before an error returns.

The earlier M83 structural check establishes the final conventional record's
signature and zero comment length. The M84 helper independently retains the
same content-silent ZIP-data normalization for an unusable final record.

## Boundary

M84 checks only equality among two conventional fields and the standard
reader's already parsed member count. It adds no ZIP64 end-record parser, no
sentinel resolution, no end-record search, no central-directory or local-
header parser, no neighboring-volume discovery, and no multi-volume assembler.
A conventional `0xFFFF` count is outside the fixed profile even if a separate
ZIP64 record could supply a matching value.

M84 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- Both conventional counts must exactly match all parsed members before name,
  metadata, inventory, staging, or read policy.
- Every established flag, extra-field, comment, member-volume, and archive-
  disk error retains precedence.
- Empty or otherwise inventory-incomplete archives with internally consistent
  counts retain the later exact-inventory error.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled count, member name, or path.
- ZIP64 end records and actual split/spanned archive assembly remain deferred.

## Alternatives considered

- Continue ignoring the counts because CPython scans the declared central-
  directory size. Rejected because contradictory metadata widens the admitted
  release profile without helping the fixed producer.
- Compare only the two conventional fields to each other. Rejected because a
  matching but false pair such as two/two remains inconsistent with the parsed
  archive.
- Parse the ZIP64 end record to resolve `0xFFFF`. Rejected because the fixed
  archive has 50 members and needs no second record grammar.
- Find or assemble neighboring volumes. Rejected because that adds filesystem
  discovery, ownership, and unsupported multi-volume semantics.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0066: reject unsupported archive disk fields](0066-reject-unsupported-archive-disk-fields.md)
- [RFC-0065: reject split-volume sample members](0065-reject-split-volume-sample-members.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
