# RFC-0093: Retain sample-member timestamp compatibility

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE APPNOTE 6.3.10 defines member date and time as MS-DOS calendar fields
relative to 1980 with two-second resolution. The field is not an absolute UTC
instant. Python exposes the decoded public central value as the six-part
`ZipInfo.date_time` tuple. New `ZipInfo` records use
`(1980, 1, 1, 0, 0, 0)`, while convenience writer calls use the current local
calendar time.

Exact CPython 3.12.13, 3.13.13, and 3.14.5 each admit a deflated fixture dated
`(2026, 8, 25, 12, 34, 56)`, expose that value, and read its payload. The fixed
50-member LudoWeave producer emits `(1980, 1, 1, 0, 0, 0)` for every member.

An initial M110 implementation required the producer tuple after M109. Its 21
focused assertions passed, but the complete architecture suite failed 22
established assertions. Valid bounded-extraction, portable-path, atomic-
staging, exact-inventory, owned-snapshot, decompression, and content-silent
diagnostic fixtures use the supported convenience writer and therefore carry
another consistent timestamp. Rewriting those contracts would narrow existing
compatibility without a security or interoperability requirement.

## Decision

Retain sample-member timestamp compatibility. M98 continues to require every
local timestamp field to match the parser-exposed central `ZipInfo.date_time`.
M104 continues to require empty member extra fields. No exact central timestamp
classifier is added after M109.

The fixed producer continues to use `(1980, 1, 1, 0, 0, 0)` for reproducible
artifacts. Producer reproducibility and verifier admission remain separate
contracts.

This is one central-timestamp compatibility decision. It adds no timestamp
error category or precedence change. Existing inventory, staging, read,
cleanup, and content-silent diagnostics remain unchanged.

## Boundary

M110 performs no timezone or UTC conversion, wall-clock lookup in the verifier,
daylight-saving interpretation, extra-field timestamp parsing, timestamp
normalization, raw local or central record parsing, payload-content read,
decompression, recompression, CRC recomputation, repair, or general ZIP
validity claim. It is not a general archive sandbox and is not a real public
release observation.

The decision does not assert that all encodable timestamps are semantically
trustworthy or suitable for user-facing time display. Timestamps remain archive
metadata; they are not canonical runtime state or release authority.

M110 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, verifier, sample producer,
release mutation, release authority, tag, release, or publication.

## Consequences

- Alternate MS-DOS timestamp tuples remain admitted when all established
  structural, metadata, profile, inventory, and content checks pass.
- M98 still rejects local/central timestamp mismatches before later processing.
- The fixed producer remains byte-reproducible with its existing timestamp.
- The 22 established architecture regressions caused by the exact profile are
  removed without weakening any prior check.

## Alternatives considered

- Require the fixed producer tuple. Rejected after 22 established architecture
  regressions demonstrated an unjustified compatibility break.
- Rewrite historical fixtures with the producer tuple. Rejected because those
  fixtures intentionally exercise supported standard-library writer behavior.
- Convert timestamps to UTC. Rejected because the field carries no timezone and
  the verifier has no need for inferred time semantics.
- Interpret extended timestamp extra fields. Rejected because M104 already
  requires empty member extras and the producer emits none.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [M98 local-header timestamp consistency preflight](../architecture.md#m98-local-header-timestamp-consistency-preflight)
- [RFC-0092: require zero sample-member internal attributes](0092-require-zero-sample-member-internal-attributes.md)
