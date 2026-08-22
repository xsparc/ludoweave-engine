# RFC-0079: Require consistent local-header extra fields

- **Status:** Accepted
- **Date:** 2026-08-23
- **Decision owners:** LudoWeave maintainers

## Context

M95 proves that each bounded two-byte local compression method equals the
corresponding parser-exposed central value. It intentionally does not compare
the variable extra-field bytes present in both local and central member
records.

PKWARE APPNOTE 6.3.10 sections 4.3.7 and 4.3.12 define separate variable extra
fields in those records. Python exposes the central bytes as public
`ZipInfo.extra` and the local-header location as `ZipInfo.header_offset`. During
a member read, CPython advances over the local extra length without comparing
the local bytes with `ZipInfo.extra`.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the final byte of
the second local extra from `feca02006f6b` to `feca02006f21` leaves both central
extras at `feca02006f6b`, preserves offsets `[0, 60]`, and permits both payloads
to be read. This decision relies only on that observed admission gap, public
attributes, and documented record structure.

## Decision

After M95 compression-method consistency, private complete release smoke reads
the already bounded local name and extra lengths at
`ZipInfo.header_offset + 26`, then reads exactly the declared local extra bytes
after the fixed 30-byte prefix and local name. The local bytes must equal the
corresponding central `ZipInfo.extra`. A mismatch raises stable, content-silent
error `sample bundle local header extra fields are inconsistent`.

This one bounded local-extra equality classifier runs before decoded-name
policy, member metadata, exact inventory, staging, or member reads. Every
established policy through M95 retains precedence. M92 already proves the
complete local name-plus-extra envelope precedes the conventional central
directory, the helper restores the snapshot position, and the existing
`ExitStack` closes the source, snapshot, and archive before an error returns.
An empty parsed inventory satisfies this aggregate rule and retains the later
exact-inventory behavior.

## Boundary

M96 adds no extra-field semantics parser and no broad extra-field ban. Existing
central Unicode Path and ZIP64 ID policies retain their earlier precedence; no
new field ID, nested length, ordering, duplication, or canonicalization rule is
introduced. Exact byte equality is a fixed-producer profile, not a claim that
all ZIP producers must emit identical local and central extra fields.

M96 performs no version/time/CRC/size comparison, field-wide local/central
comparison, complete local-record or payload bound, next-header bound, gap,
adjacency, contiguity, physical non-overlap rule, or inter-member layout
validator, and no archive repair. It adds no workflow, runner allocation,
action, permission, credential, dependency, lock, version, runtime package/API,
sample producer, release mutation, release authority, tag, release, or
publication. Pull-request evidence is not a real public release observation,
and this fixed-producer policy is not a general archive sandbox.

## Consequences

- Any local/central extra-byte or extra-length mismatch fails before decoded
  names, metadata, exact inventory, staging, or reads.
- Every established policy through M95 retains precedence.
- Equal unrelated extra fields remain admitted; their semantics are not
  interpreted by M96.
- The fixed 50-member producer remains unchanged with empty matching extras.
- The error exposes no archive-controlled name, bytes, length, field ID, or
  offset.
- Standard-library member reads retain responsibility for payload extents,
  overlap checks, decompression, and CRC validation.

## Alternatives considered

- Reject every non-empty local or central extra field. Rejected as a broad ban
  that would supersede the established exact central-ID policies.
- Parse and compare extra-field IDs semantically. Rejected because local and
  central records may assign different meanings or payloads to the same field;
  the fixed producer needs only exact-profile equality.
- Defer local-only extra changes to member reads. Rejected because supported
  Python versions ignore the demonstrated same-length content mismatch.
- Compare all remaining fixed fields. Rejected because version, time, CRC, and
  size consistency require separate policies, including data-descriptor and
  ZIP64 considerations.
- Bound payloads, next headers, gaps, adjacency, or overlap. Rejected because
  those require broader record parsing and inter-member layout policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0078: require consistent local-header compression methods](0078-require-consistent-local-header-compression-methods.md)
- [RFC-0062: reject Unicode Path extra fields](0062-reject-unicode-path-extra-fields.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0075: bound local-header envelopes](0075-bound-local-header-envelopes.md)
