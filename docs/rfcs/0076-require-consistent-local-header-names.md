# RFC-0076: Require consistent local-header names

- **Status:** Accepted
- **Date:** 2026-08-23
- **Decision owners:** LudoWeave maintainers

## Context

M92 proves that each parser-exposed local-header variable envelope ends before
the conventional central directory. It does not prove that the bounded local
file-name identifies the same sample member as the corresponding central
directory record.

PKWARE APPNOTE 6.3.10 sections 4.3.2 and 4.3.7 require a local header and a
corresponding central header for each member and place the variable file-name
immediately after the 30-byte local prefix. Appendix D defines CP437 as the
historical encoding and UTF-8 when general-purpose bit 11 is set. Python
documents the same default/flag precedence and exposes each central name,
`flag_bits`, and `header_offset` through `ZipInfo`.

Supported CPython 3.12.13, 3.13.13, and 3.14.5 expose an unchanged two-member
central inventory and local-header offsets `[0, 46]` when one same-length local
name is changed from `second.txt` to `second.txu`. The first payload remains
readable; opening the mismatched second member raises public `BadZipFile`. This
decision does not depend on that exception's message.

## Decision

After M92 policy, private complete release smoke reads each declared local
file-name from the owned checksum-admitted snapshot. It reconstructs the
parser-exposed central `ZipInfo.orig_filename` as UTF-8 bytes when central
`flag_bits` contains bit 11 and as CP437 bytes otherwise. The raw byte strings
must be equal. A mismatch or a central name that cannot be reconstructed under
its declared central encoding raises stable, content-silent error
`sample bundle local header names are inconsistent`.

This one raw local-name consistency classifier runs before decoded-name policy,
member metadata, exact inventory, staging, or member reads. Every established
policy through M92 retains precedence. M79 already rejects Unicode Path extra
fields, so `orig_filename` remains the central directory's decoded original
name. The M92 envelope bound makes the local read finite, the helper restores
the snapshot position, and the existing `ExitStack` closes the source,
snapshot, and archive before an error returns. An empty parsed inventory
satisfies this aggregate rule and retains the later exact-inventory behavior.

## Boundary

M93 performs no local-flag comparison and no extra-field comparison or parsing,
field-wide local/central consistency check, complete local-record or payload
bound, next-header bound, gap, adjacency, contiguity, physical non-overlap rule,
or inter-member layout validator, and no archive repair. Reconstructing the
expected central name is not a general local-header or central-directory
parser.

M93 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- A bounded local name that differs from its corresponding central name fails
  before decoded names, metadata, exact inventory, staging, or reads.
- Every established policy through M92 retains precedence.
- CP437 and UTF-8 central names are reconstructed deterministically.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled name, bytes, encoding, or offset.
- Standard-library member reads retain responsibility for later local-header
  fields, payload extents, overlap checks, decompression, and CRC validation.

## Alternatives considered

- Defer local/central name mismatch to member reads. Rejected because that
  permits a known fixed-producer identity violation past metadata preflight.
- Decode with the local flag and compare strings exactly as CPython currently
  does. Rejected because M93 does not need to admit or compare local flag
  semantics; the fixed producer requires raw equality with its central name.
- Parse the raw central directory name. Rejected because the public `ZipInfo`
  surface plus the already admitted encoding policy is sufficient here.
- Compare local and central extra fields or every fixed field. Rejected because
  those are materially broader consistency policies.
- Bound payloads, next headers, gaps, adjacency, or overlap. Rejected because
  those require broader record parsing and inter-member layout policy.
- Depend on CPython's current `BadZipFile` text. Rejected because public error
  wording is not part of this policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0075: bound local-header variable envelopes](0075-bound-local-header-envelopes.md)
- [RFC-0062: reject Unicode Path extra fields](0062-reject-unicode-path-extra-fields.md)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
