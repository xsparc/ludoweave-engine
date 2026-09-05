# RFC-0090: Require exact sample-member extraction version

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE APPNOTE 6.3.10 defines the low byte of the version-needed-to-extract
field as the minimum ZIP feature version and assigns 2.0 to Deflate. Supported
CPython exposes this byte through public `ZipInfo.extract_version`, uses `20` as
its default writer value, and recognizes features through version 6.3.

M97 requires exact local/central equality for the complete two-byte pair but
intentionally adds no supported-version policy. M106 then requires the reserved
high byte to be zero. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each admit an
otherwise valid deflated fixture whose second member has matching local and
central pairs `(21, 0)`, expose the changed public central value, and read both
payloads. The fixed 50-member LudoWeave producer emits pair `(20, 0)` for every
member.

## Decision

After established local-header, payload-layout, extra-field, decoded-name,
member-metadata, M105 flag-profile, and M106 reserved-byte checks, private
complete release smoke requires `ZipInfo.extract_version == 20` for every
parsed sample member before exact inventory.

- Stable error: `sample bundle has an unsupported extraction version`.

This exact sample-member extraction-version profile preflight is
one central-extraction-version exact-profile classifier. It runs before exact
inventory, staging, or member reads. Established local extraction-version mismatch,
payload-layout, M104 extra-field, unsupported-codec, nonportable-path, M105
flag-profile, and M106 reserved-byte errors retain precedence. An empty parsed
inventory satisfies the aggregate exact rule and retains its later exact-
inventory failure.

The existing `ExitStack` closes the source, snapshot, and archive before an
error returns. The error contains no archive-controlled version, name, size,
offset, or member position.

## Boundary

M107 adds no general extraction-version semantics parser, supported-version
range, minimum extractor-capability evaluator, feature inference, raw local/
central parser, payload-content read, decompression, recompression, CRC
recomputation, repair, or general ZIP validity claim. It is not a general
archive sandbox and is not a real public release observation.

This is a project-specific fixed-producer profile. It does not assert that
other extraction versions are malformed, unsafe, or unreadable in general ZIP
archives.

M107 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication.

## Consequences

- Any remaining member whose public central extraction version differs from
  `20` fails before exact inventory, staging, or reads.
- Established specific, local-consistency, layout, metadata, M105, and M106
  errors keep their stable precedence.
- Exact producer output and empty-archive inventory behavior remain unchanged.
- The fixed profile no longer admits overdeclared or underdeclared versions.
- Standard-library member reads retain responsibility for decompression and CRC
  validation against admitted metadata.

## Alternatives considered

- Retain equal non-20 values. Rejected because the fixed Deflate producer emits
  none and no current artifact needs another feature version.
- Accept a range. Rejected because no demonstrated producer requirement
  justifies a general capability or feature-version evaluator.
- Move the exact-profile check ahead of M97, M106, or precise metadata
  diagnostics. Rejected because that would erase established mismatch,
  reserved-byte, and metadata precedence.
- Re-read the raw low byte. Rejected because M97 already proves local equality
  and public `ZipInfo.extract_version` supplies the admitted central value.
- Describe version `20` as universally required. Rejected because ZIP defines
  legitimate other feature versions outside this fixed producer profile.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0080: require consistent local-header extraction versions](0080-require-consistent-local-header-extraction-versions.md)
- [RFC-0086: require contiguous sample-member payloads](0086-require-contiguous-sample-payloads.md)
- [RFC-0087: require empty sample-member extra fields](0087-require-empty-sample-member-extra-fields.md)
- [RFC-0088: require zero sample-member general-purpose flags](0088-require-zero-sample-member-general-purpose-flags.md)
- [RFC-0089: require zero sample-member extraction-version reserved bytes](0089-require-zero-sample-member-extraction-version-reserved-bytes.md)
