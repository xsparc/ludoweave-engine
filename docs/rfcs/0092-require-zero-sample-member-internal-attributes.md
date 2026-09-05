# RFC-0092: Require zero sample-member internal attributes

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE APPNOTE 6.3.10 defines the two-byte central internal-file-attribute field.
Bit zero is an advisory apparent text marker, bit one denotes a mainframe
variable-record control field, and other bits are reserved or unused. Python
exposes the complete public central value as `ZipInfo.internal_attr`; CPython
initializes it to zero.

Exact CPython 3.12.13, 3.13.13, and 3.14.5 each admit a deflated fixture with
public central `internal_attr == 1`, expose that value, and read its payload.
The fixed 50-member LudoWeave producer emits `internal_attr == 0` for every
member.

The producer archives text-bearing `.md` and `.py` files while retaining the
standard zero default. The field is therefore treated only as fixed-producer
metadata. M109 does not infer, inspect, or certify payload content.

## Decision

After established local-header, payload-layout, extra-field, member-metadata,
M105 flag-profile, M106 reserved-byte, M107 extraction-version, and M108
creation-version checks, private complete release smoke requires
`ZipInfo.internal_attr == 0` for every parsed sample member before exact
inventory.

- Stable error: `sample bundle has unsupported internal attributes`.

This preflight is one central-internal-attribute exact-profile classifier. It
runs before exact inventory, staging, or member reads. Established local-header,
payload-layout, extra-field, unsupported-codec, nonportable-path, and M105-M108
errors retain precedence. An empty parsed inventory satisfies the aggregate
exact rule and retains its later exact-inventory failure.

The existing `ExitStack` closes the source, snapshot, and archive before an
error returns. The error contains no archive-controlled attribute, name, size,
offset, or member position.

## Boundary

M109 adds no text/binary content interpretation, record-control semantics
parser, supported-bit mask, external-attribute or host-system policy, raw
central record parser, payload-content read, decompression, recompression, CRC
recomputation, repair, or general ZIP validity claim. It is not a general
archive sandbox and is not a real public release observation.

This is a project-specific fixed-producer profile. It does not assert that
nonzero internal attributes are malformed, unsafe, or unreadable in general ZIP
archives.

M109 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication.

## Consequences

- Any remaining member whose public central internal attributes differ from
  zero fails before exact inventory, staging, or reads.
- Established local-header, layout, metadata, and M105-M108 errors keep their
  stable precedence.
- Exact producer output and empty-archive inventory behavior remain unchanged.
- Payload classification and host/attribute interpretation remain unchanged.

## Alternatives considered

- Retain all internal-attribute values. Rejected because the fixed producer
  emits only zero and no current artifact requires another value.
- Accept the apparent-text bit. Rejected because the producer does not set it
  for text-bearing members and no payload-classification requirement exists.
- Interpret or validate record-control semantics. Rejected because that would
  require payload inspection and a materially broader parser.
- Re-read the raw central field. Rejected because public
  `ZipInfo.internal_attr` supplies the admitted central value.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0091: require exact sample-member creation version](0091-require-exact-sample-member-creation-version.md)
