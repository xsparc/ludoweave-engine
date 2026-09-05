# RFC-0087: Require empty sample-member extra fields

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE APPNOTE 6.3.10 defines variable member extra fields as an extensibility
mechanism in both local and central records. Supported CPython exposes the
central bytes through public `ZipInfo.extra`, interprets selected known field
IDs, and otherwise retains uninterpreted field bytes. This is valid ZIP
extensibility, but
the fixed 50-member LudoWeave producer has no use for it and emits empty member
extra fields.

M79 rejects Unicode Path field ID `0x7075`, M80 rejects ZIP64 field ID `0x0001`,
and M96 requires exact local/central extra-field equality. Those precise
policies intentionally retained equal fields not interpreted by CPython. On
exact CPython 3.12.13, 3.13.13, and 3.14.5, two deflated members with equal
local and central third-party field `feca02006f6b` retain that field and both
payloads remain readable.

M103 now completes the fixed producer's compressed-payload contiguity boundary,
so an explicit empty-extra profile can be enforced after all established field-
specific, consistency, bounds, and layout errors without conflating valid ZIP
extensibility with the narrower release contract.

## Decision

After M103 contiguity validation, private complete release smoke requires
`ZipInfo.extra == b""` for every parsed sample member.

- Stable error: `sample bundle contains an unsupported extra field`.

This empty sample-member extra-field profile preflight is one central-extra
emptiness classifier. It runs before decoded-name policy, member metadata,
exact inventory, staging, or member reads. M79 Unicode Path, M80 ZIP64, M96
local/central consistency, M102 payload bounds, and M103 contiguity errors
retain precedence. An empty parsed inventory satisfies the aggregate emptiness
rule and retains its later exact-inventory failure.

The existing `ExitStack` closes the source, snapshot, and archive before an
error returns. The error contains no archive-controlled field bytes, name,
size, offset, ID, or member position.

## Boundary

M104 adds no extra-field semantics parser, field-ID registry, allowlist, raw
central-record parser, archive extra-data record policy, payload-content read,
decompression, recompression, CRC recomputation, repair, or general ZIP
validity claim. It is not a general archive sandbox and is not a real public
release observation.

This is a project-specific fixed-producer profile. It does not assert that
non-empty extra fields are malformed or unsafe in general ZIP archives.

M104 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication.

## Consequences

- Any remaining equal non-empty member extra field fails before decoded names,
  metadata, inventory, staging, or reads.
- Established specific extra-field and local/layout errors keep their stable
  precedence.
- Exact producer output and empty-archive inventory behavior remain unchanged.
- The fixed profile no longer admits unparsed per-member extension metadata.
- Standard-library member reads retain responsibility for decompression and CRC
  validation against admitted metadata.

## Alternatives considered

- Retain equal non-empty extra fields. Rejected because the fixed producer emits
  none and no current release artifact needs extension metadata.
- Parse and allow selected non-empty fields. Rejected because no demonstrated
  producer requirement justifies a new semantics parser or registry.
- Move the emptiness check ahead of M79/M80 or M96. Rejected because it would
  erase established precise diagnostics and consistency precedence.
- Inspect raw central records again. Rejected because public `ZipInfo.extra`
  already supplies the admitted central bytes after local equality is proven.
- Describe non-empty fields as generally unsafe. Rejected because APPNOTE
  deliberately defines extra-field extensibility beyond this project profile.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0086: require contiguous sample-member payloads](0086-require-contiguous-sample-payloads.md)
- [RFC-0079: require consistent local-header extra fields](0079-require-consistent-local-header-extra-fields.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0062: reject Unicode Path extra fields](0062-reject-unicode-path-extra-fields.md)
