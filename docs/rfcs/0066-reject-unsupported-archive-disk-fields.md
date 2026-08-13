# RFC-0066: Reject unsupported archive disk fields before extraction

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample bundle is one small regular ZIP file. Its producer
emits a conventional 22-byte end-of-central-directory record at the end of the
file with both the current-disk number and central-directory-start disk number
set to zero.

PKWARE APPNOTE sections 4.3.16, 4.4.19, and 4.4.20 define those two little-
endian fields. Nonzero values describe archive disks outside the fixed sample
profile; `0xFFFF` defers the corresponding value to a ZIP64 end record. Current
CPython parses the conventional fields but does not consult them in
`ZipFile._RealGetContents()`. Supported CPython 3.12.13, 3.13.13, and 3.14.5
each open and read the same deflated payload when either field is patched to
one, both are one, or both are `0xFFFF`; the member still exposes volume zero.

## Decision

Private complete release smoke reads exactly the final conventional 22-byte
end-of-central-directory record from its owned checksum-admitted snapshot. It
requires the signature, zero declared comment length, current-disk number
zero, and central-directory-start disk number zero. Either nonzero disk field
raises stable content-silent error
`sample bundle uses unsupported archive disk fields`.

Complete release smoke first finishes every established M69/M75/M76 flag pass,
M78 descriptor policy, M79 Unicode Path policy, M80 ZIP64 member-extra policy,
both M81 comment passes, and M82 member-volume policy. The M83 check then runs
before M77 decoded-name policy, member metadata, exact inventory validation,
staging, or member reads. Its temporary seek restores the snapshot position.
The existing `ExitStack` closes the source, snapshot, and archive before an
error returns.

A missing final conventional record, wrong signature, or nonzero final comment
length uses the existing content-silent ZIP-data error. This structural check
is necessary to keep the bounded final-record read unambiguous; it is not a
new public error category.

## Boundary

M83 reads only the fixed final conventional end record after M81 has admitted
an empty parser-exposed archive comment. It adds no ZIP64 end-record parser, no
end-record search, no central-directory or local-header parser, no neighboring-
volume discovery, and no multi-volume assembler. In particular, it rejects a
conventional `0xFFFF` field as outside the fixed profile; it does not resolve
the sentinel or infer whether a referenced ZIP64 value represents one or more
volumes.

M83 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- Either conventional EOCD disk field outside base disk zero fails before
  decoded-name policy, metadata, inventory, staging, or reads.
- Every established archive-wide flag, extra-field, comment, and member-volume
  category retains precedence.
- The fixed producer remains unchanged and compatible.
- The error exposes no archive-controlled numeric value, member name, or path.
- The owned snapshot position is restored and all owned resources close before
  control returns.
- ZIP64 end records and actual split/spanned archive assembly remain deferred.

## Alternatives considered

- Continue ignoring the fields because CPython reads the patched fixture.
  Rejected because the values widen the admitted format beyond the fixed
  producer without a supported consumer use case.
- Label every nonzero or sentinel value as a split-volume archive. Rejected
  because `0xFFFF` can defer to a single-disk ZIP64 value; the selected error
  describes only the unsupported metadata actually observed.
- Parse the ZIP64 end record to resolve `0xFFFF`. Rejected because that adds a
  second record grammar without a need in the fixed sample profile.
- Find or assemble neighboring volumes. Rejected because that adds filesystem
  discovery, ownership, and unsupported multi-volume semantics.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0065: reject split-volume sample members](0065-reject-split-volume-sample-members.md)
- [RFC-0064: reject ZIP comments](0064-reject-zip-comments.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
