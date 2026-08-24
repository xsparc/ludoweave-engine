# RFC-0088: Require zero sample-member general-purpose flags

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE APPNOTE 6.3.10 defines a two-byte general-purpose flag field in both
local and central member records. Selected bits describe encryption,
compression options, data descriptors, patched data, and UTF-8 names; other
bits are reserved or currently unused. Supported CPython exposes the central
value through public `ZipInfo.flag_bits` and interprets selected bits.

Earlier milestones reject encryption, enhanced deflating, compressed patched
data, and data descriptors with precise errors. M94 requires exact
local/central flag equality. Those policies intentionally did not create a
broad flag allowlist because valid ZIP producers can use nonzero bits.

The LudoWeave sample bundle is narrower: its fixed 50-member producer uses
ASCII paths, deflate, no descriptors, and emits `ZipInfo.flag_bits == 0` for
every member. On exact CPython 3.12.13, 3.13.13, and 3.14.5, an otherwise valid
deflated fixture whose matching local and central headers carry currently
unused bit 7 retains public value `128` and both payloads remain readable.
M104 now completes the fixed producer's extra-field profile, so the remaining
central flag value can be classified after all established precise checks.

## Decision

After M104 extra-field validation and established decoded-name/member-metadata
policy, private complete release smoke requires `ZipInfo.flag_bits == 0` for
every parsed sample member before exact inventory.

- Stable error: `sample bundle contains unsupported general-purpose flags`.

This zero sample-member general-purpose-flag profile preflight is one central-
flag zero-profile classifier. It runs after decoded-name and member-metadata
policy but before exact inventory, staging, or member reads. Established
encryption, data-descriptor, enhanced-deflate, compressed-patch, unsupported-
codec, nonportable-path, local/central consistency, payload-layout, and M104
errors retain precedence. An empty parsed inventory satisfies the aggregate
zero rule and retains its later exact-inventory failure.

The existing `ExitStack` closes the source, snapshot, and archive before an
error returns. The error contains no archive-controlled flag value, name,
size, offset, or member position.

## Boundary

M105 adds no flag-semantics parser, compression-option interpreter, bit
registry, allowlist for general ZIP input, raw local/central parser, payload-
content read, decompression, recompression, CRC recomputation, repair, or
general ZIP validity claim. It is not a general archive sandbox and is not a
real public release observation.

This is a project-specific fixed-producer profile. It does not assert that all
nonzero flags are malformed or unsafe in general ZIP archives. In particular,
the ZIP format defines legitimate nonzero flags beyond this project's producer.

M105 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication.

## Consequences

- Any remaining member with a nonzero public central flag fails after decoded
  names and member metadata but before exact inventory, staging, or reads.
- Established specific-flag and local/layout errors keep their stable
  precedence.
- M76 remains method-specific, while M105 newly rejects residual nonzero flags
  such as bit 4 on a stored member after member-metadata policy.
- Exact producer output and empty-archive inventory behavior remain unchanged.
- The fixed profile no longer admits unclassified member-processing flags.
- Standard-library member reads retain responsibility for decompression and CRC
  validation against admitted metadata.

## Alternatives considered

- Retain equal nonzero flags. Rejected because the fixed producer emits none
  and no current release artifact needs alternate member processing.
- Parse and allow selected nonzero flags. Rejected because no demonstrated
  producer requirement justifies a new semantics parser or bit registry.
- Move the zero-profile check ahead of established specific checks or M94.
  Rejected because it would erase precise diagnostics and consistency
  precedence.
- Inspect raw flag fields again. Rejected because M94 already proves local
  equality and public `ZipInfo.flag_bits` supplies the admitted central value.
- Describe nonzero flags as generally unsafe. Rejected because the ZIP format
  deliberately defines valid nonzero semantics outside this project profile.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0087: require empty sample-member extra fields](0087-require-empty-sample-member-extra-fields.md)
- [RFC-0077: require consistent local-header flags](0077-require-consistent-local-header-flags.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0059: reject enhanced-deflate sample members](0059-reject-enhanced-deflate-sample-members.md)
- [RFC-0058: reject compressed-patch sample members](0058-reject-compressed-patch-sample-members.md)
- [RFC-0052: reject encrypted sample members](0052-reject-encrypted-sample-members.md)
