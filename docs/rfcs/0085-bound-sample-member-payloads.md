# RFC-0085: Bound sample-member compressed payloads

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

M92 bounds each complete variable local-header envelope, M88 orders local-
header offsets, M89 bounds them by the conventional central directory, and
M100/M101 prove equality for the duplicated size fields. The admitted profile
still does not combine those established facts to prove that a compressed
payload ends before the next local header or central directory.

PKWARE APPNOTE 6.3.10 section 4.3.7 places file data immediately after the
local-file header and its variable name and extra fields. Sections 4.3.12 and
4.3.16 place the central-directory records after local records and define the
conventional end record's directory offset. Python exposes each central
compressed size and local-header location as public `ZipInfo.compress_size`
and `ZipInfo.header_offset`.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, increasing the first member's
matching local and central compressed size from `11` to `12` places its
calculated payload end at byte `54`, one byte beyond the next local header at
`53`. `ZipFile` still opens, the second payload remains readable, and only the
first member read later raises `BadZipFile`.

## Decision

After M101 size-field consistency, private complete release smoke calculates
each compressed payload end as:

`header_offset + 30 + local_name_length + local_extra_length + compress_size`

Each nonfinal end must be no greater than the next strictly ordered local-
header offset. The final end must be no greater than the conventional central-
directory offset.

- Stable error: `sample bundle member payloads are out of bounds`.

This one compressed-payload upper-bound classifier runs before decoded-name
policy, member metadata, exact inventory, staging, or member reads. Every
established policy through M101 retains precedence. Existing checks have
already bounded and compared the local-header envelope and size fields. The
helper restores the caller's snapshot position, and the existing `ExitStack`
closes the source, snapshot, and archive before an error returns. An empty
parsed inventory satisfies this aggregate rule and retains the later exact-
inventory behavior.

## Boundary

M102 adds an upper bound only. It performs no decompression or recompression,
no payload-content read, no exact-contiguity requirement, no gap or adjacency
ban, no requirement that a payload end equal its limit, no compression-ratio
or archive-bomb policy, and no payload-integrity certification. It does not
parse descriptors, central records, or payload bytes and is not a complete
inter-member layout validator.

APPNOTE's data-descriptor and ZIP64 exceptions remain outside this admitted
profile: established policy rejects general-purpose bit 3 and ZIP64 extra
fields before M102 runs. Established central-directory-encryption policy also
rejects bit 13.

M102 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any compressed payload extending beyond its next local-header or directory
  limit fails before decoded names, metadata, inventory, staging, or reads.
- Every established policy through M101 retains precedence.
- Exact producer payload boundaries and shorter non-overlapping payload extents
  remain admitted by this classifier.
- The fixed 50-member producer remains unchanged; each payload currently ends
  exactly at the next header or directory boundary.
- The error exposes no archive-controlled name, size, offset, or member
  position.
- Standard-library member reads retain responsibility for decompression and
  CRC validation against the admitted central metadata.

## Alternatives considered

- Require exact contiguity. Rejected because forbidding benign gaps is a
  separate producer-profile decision and is unnecessary to prevent overlap.
- Decompress members during preflight. Rejected because that would read payload
  content before exact inventory and duplicate extraction work.
- Rely only on the later standard-library overlap error. Rejected because the
  demonstrated archive is admitted through parsing and exposes later policy
  stages before the first member read.
- Parse raw central records again. Rejected because established conventional
  directory policy and public `ZipInfo` values provide the required limits.
- Repair sizes or payload placement. Rejected because release smoke is a
  validator and has no archive-mutation authority.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0084: require consistent local-header uncompressed sizes](0084-require-consistent-local-header-uncompressed-sizes.md)
- [RFC-0083: require consistent local-header compressed sizes](0083-require-consistent-local-header-compressed-sizes.md)
- [RFC-0075: bound local-header variable envelopes](0075-bound-local-header-envelopes.md)
- [RFC-0072: bound local-header offsets](0072-bound-local-header-offsets.md)
- [RFC-0071: require local-header offset order](0071-require-local-header-offset-order.md)
- [RFC-0068: require exact central-directory placement](0068-require-exact-central-directory-placement.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0052: reject encrypted sample members before extraction](0052-reject-encrypted-sample-members.md)
