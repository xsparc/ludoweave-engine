# RFC-0089: Require zero sample-member extraction-version reserved bytes

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE APPNOTE 6.3.10 defines the two-byte version-needed-to-extract field in
both local and central member records. Supported CPython exposes the two bytes
separately through public `ZipInfo.extract_version` and `ZipInfo.reserved`;
Python documents the reserved value as required to be zero, and CPython's
`ZipInfo` writer default is zero.

M97 requires exact local/central equality for the complete two-byte pair but
intentionally adds no supported-version or reserved-byte policy. Exact CPython
3.12.13, 3.13.13, and 3.14.5 each admit an otherwise valid deflated fixture
whose second member has matching local and central pairs `(20, 1)`, expose the
nonzero public central value, and read both payloads. The fixed 50-member
LudoWeave producer emits `ZipInfo.reserved == 0` for every member.

## Decision

After established local-header, payload-layout, extra-field, decoded-name,
member-metadata, and M105 flag-profile checks, private complete release smoke
requires `ZipInfo.reserved == 0` for every parsed sample member before exact
inventory.

- Stable error: `sample bundle has a nonzero extraction-version reserved byte`.

This zero sample-member extraction-version reserved-byte profile preflight is
one central-reserved zero-profile classifier. It runs before exact inventory,
staging, or member reads. Established local extraction-version mismatch,
payload-layout, M104 extra-field, unsupported-codec, nonportable-path, and M105
flag-profile errors retain precedence. An empty parsed inventory satisfies the
aggregate zero rule and retains its later exact-inventory failure.

The existing `ExitStack` closes the source, snapshot, and archive before an
error returns. The error contains no archive-controlled byte value, name, size,
offset, or member position.

## Boundary

M106 adds no extraction-version semantics parser, supported-version allowlist,
minimum extractor-capability rule, raw local/central parser, payload-content
read, decompression, recompression, CRC recomputation, repair, or general ZIP
validity claim. It is not a general archive sandbox and is not a real public
release observation.

This is a project-specific fixed-producer profile. It does not assert that a
nonzero byte is an exploitable condition or define behavior for general ZIP
archives.

M106 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication.

## Consequences

- Any remaining member with a nonzero public central reserved byte fails before
  exact inventory, staging, or reads.
- Established specific, local-consistency, layout, metadata, and M105 errors
  keep their stable precedence.
- Exact producer output and empty-archive inventory behavior remain unchanged.
- The fixed profile no longer admits a nonzero extraction-version reserved byte.
- Standard-library member reads retain responsibility for decompression and CRC
  validation against admitted metadata.

## Alternatives considered

- Retain equal nonzero reserved bytes. Rejected because Python documents zero
  and the fixed producer emits no other value.
- Interpret extraction-version semantics. Rejected because no demonstrated
  producer requirement justifies a supported-version or capability parser.
- Move the zero-profile check ahead of M97 or precise metadata diagnostics.
  Rejected because that would erase established mismatch and metadata
  precedence.
- Re-read the raw reserved byte. Rejected because M97 already proves local
  equality and public `ZipInfo.reserved` supplies the admitted central value.
- Describe this check as general archive security. Rejected because it is only
  a fixed-producer release-smoke profile.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0080: require consistent local-header extraction versions](0080-require-consistent-local-header-extraction-versions.md)
- [RFC-0086: require contiguous sample-member payloads](0086-require-contiguous-sample-payloads.md)
- [RFC-0087: require empty sample-member extra fields](0087-require-empty-sample-member-extra-fields.md)
- [RFC-0088: require zero sample-member general-purpose flags](0088-require-zero-sample-member-general-purpose-flags.md)
