# RFC-0086: Require contiguous sample-member payloads

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

M102 combines bounded local-header envelopes, matching compressed sizes,
ordered local-header offsets, and the conventional central-directory boundary
to reject payload overlap. It intentionally admits a shorter compressed extent
that leaves unparsed bytes before the next local or central record. The fixed
50-member producer does not create such gaps: each payload ends exactly at its
next record.

PKWARE APPNOTE 6.3.10 section 4.3.7 places file data immediately after the
variable local-file header. Sections 4.3.12 and 4.3.16 place the central
directory after local records and define the conventional end record's
directory offset. Python exposes the central compressed size and local-header
location through public `ZipInfo.compress_size` and `ZipInfo.header_offset`.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, inserting one byte before the
second local header while consistently advancing the affected central offset
and directory position remains readable. Each runtime reports gap widths
`[1, 0]`, local offsets `[0, 59]`, payload ends `[58, 117]`, and returns both
`payload-0` and `payload-1`.

## Decision

After M102 upper-bound validation, private complete release smoke requires each
compressed payload end to equal its next limit:

`header_offset + 30 + local_name_length + local_extra_length + compress_size`

For every nonfinal member, the limit is the next strictly ordered local-header
offset. For the final member, it is the conventional central-directory offset.

- Stable error: `sample bundle member payloads are not contiguous`.

This one compressed-payload equality classifier runs before decoded-name
policy, member metadata, exact inventory, staging, or member reads. M102 retains
precedence for an end beyond its limit. The helper restores the caller's
snapshot position, and the existing `ExitStack` closes the source, snapshot,
and archive before an error returns. An empty parsed inventory satisfies this
aggregate rule and retains the later exact-inventory behavior.

## Boundary

M103 adds an equality check only. It performs no decompression or recompression,
no payload-content read, no CRC recomputation, no compressed-stream
interpretation, no compression-ratio or archive-bomb classification, and no
payload-integrity certification. It does not parse central records, validate
payload bytes, repair archives, or establish a general ZIP policy. It is not a
general archive sandbox and is not a real public release observation.

APPNOTE's data-descriptor and ZIP64 exceptions remain outside the admitted
profile. Established policy rejects general-purpose bit 3 and ZIP64 extra
fields before M103 runs. Established encryption policy rejects bits 0 and 13.

M103 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication.

## Consequences

- Any unparsed byte between a compressed payload and the next local or central
  record fails before decoded names, metadata, inventory, staging, or reads.
- M102 overlap failure retains precedence over M103 contiguity failure.
- Exact producer output and empty-archive inventory behavior remain unchanged.
- The error exposes no archive-controlled name, size, offset, or member
  position.
- Standard-library member reads retain responsibility for decompression and CRC
  validation against the admitted metadata.

## Alternatives considered

- Retain M102's gap admission. Rejected for this fixed deterministic producer
  because no current artifact needs padding and ignored bytes weaken the exact
  local-record profile.
- Inspect the intervening bytes. Rejected because exact equality removes the
  interval without assigning semantics to payload-adjacent content.
- Decompress or recompute CRC during preflight. Rejected because that reads
  payload content before exact inventory and duplicates extraction work.
- Parse raw central records again. Rejected because established directory
  policy and public `ZipInfo` values provide the required limits.
- Repair offsets or remove gaps. Rejected because release smoke is a validator
  and has no archive-mutation authority.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0085: bound sample-member compressed payloads](0085-bound-sample-member-payloads.md)
- [RFC-0084: require consistent local-header uncompressed sizes](0084-require-consistent-local-header-uncompressed-sizes.md)
- [RFC-0075: bound local-header variable envelopes](0075-bound-local-header-envelopes.md)
- [RFC-0072: bound local-header offsets](0072-bound-local-header-offsets.md)
- [RFC-0071: require local-header offset order](0071-require-local-header-offset-order.md)
- [RFC-0068: require exact central-directory placement](0068-require-exact-central-directory-placement.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0052: reject encrypted sample members before extraction](0052-reject-encrypted-sample-members.md)
