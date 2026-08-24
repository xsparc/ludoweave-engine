# RFC-0091: Require exact sample-member creation version

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE APPNOTE 6.3.10 defines the lower byte of `version made by` as the ZIP
specification version supported by the software that encoded a member. Python
exposes the public central fields as `ZipInfo.create_version` and
`ZipInfo.create_system`. CPython uses creation version `20` as its default and
raises that minimum only for features that require a newer format version.

Exact CPython 3.12.13, 3.13.13, and 3.14.5 each admit an otherwise valid
deflated fixture whose public central creation version is `21`, expose that
value independently from extraction version `20`, and read its payload. The
fixed 50-member LudoWeave producer emits `(create_version, create_system) ==
(20, 3)` for every member.

An initially considered exact `create_system == 3` profile failed 54 established
architecture assertions because Windows-created compatibility fixtures use host
`0`. That broader compatibility change is rejected from M108. Host-specific
external-attribute semantics require a separate design and corpus.

## Decision

After established local-header, payload-layout, extra-field, member-metadata,
M105 flag-profile, M106 reserved-byte, and M107 extraction-version checks,
private complete release smoke requires `ZipInfo.create_version == 20` for every
parsed sample member before exact inventory.

- Stable error: `sample bundle has an unsupported creation version`.

This exact sample-member creation-version profile preflight is one
central-creation-version exact-profile classifier. It runs before exact
inventory, staging, or member reads. Established local-header, payload-layout,
extra-field, unsupported-codec, nonportable-path, M105, M106, and M107 errors
retain precedence. An empty parsed inventory satisfies the aggregate exact rule
and retains its later exact-inventory failure.

The existing `ExitStack` closes the source, snapshot, and archive before an
error returns. The error contains no archive-controlled version, host, name,
size, offset, or member position.

## Boundary

M108 adds no general creation-version semantics parser, supported-version
range, producer-capability evaluator, attribute-host policy, external-attribute
semantics parser, raw central record parser, payload-content read,
decompression, recompression, CRC recomputation, repair, or general ZIP
validity claim. It is not a general archive sandbox and is not a real public
release observation.

This is a project-specific fixed-producer profile. It does not assert that
other creation versions or host systems are malformed, unsafe, or unreadable in
general ZIP archives.

M108 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication.

## Consequences

- Any remaining member whose public central creation version differs from `20`
  fails before exact inventory, staging, or reads.
- Established local-header, layout, metadata, M105, M106, and M107 errors keep
  their stable precedence.
- Exact producer output and empty-archive inventory behavior remain unchanged.
- Attribute-host interpretation and compatibility remain unchanged.

## Alternatives considered

- Retain all creation-version values. Rejected because the fixed producer emits
  only `20` and no current artifact requires another value.
- Accept a range. Rejected because no demonstrated producer requirement
  justifies a general encoder-capability evaluator.
- Couple `create_system == 3` to this check. Rejected after the first full
  architecture checkpoint produced 54 compatibility regressions in established
  Windows-created fixtures.
- Add a general host-specific attribute parser. Deferred because it requires a
  separate compatibility corpus and semantics decision.
- Re-read the raw creation byte. Rejected because public
  `ZipInfo.create_version` supplies the admitted central value.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0090: require exact sample-member extraction version](0090-require-exact-sample-member-extraction-version.md)
