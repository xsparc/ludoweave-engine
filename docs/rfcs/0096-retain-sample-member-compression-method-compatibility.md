# RFC-0096: Retain sample-member compression-method compatibility

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE defines compression as optional, method `0` as stored without
compression, and method `8` as deflated. It notes that deflate is the default
used by most ZIP-compatible applications. Python exposes the parsed method as
public `ZipInfo.compress_type`, documents `ZIP_STORED` as an uncompressed
member and `ZIP_DEFLATED` as the usual ZIP compression method, and defaults new
archives to stored.

M64 already admits exactly stored and deflated sample members before declared-
size bounds and extraction. M95 separately requires each bounded local-header
method to equal the parser-exposed central method. Exact CPython 3.12.13,
3.13.13, and 3.14.5 each preserve/read methods `0` and `8` with version `20`
and flags `0`. Complete 50-member stored, deflated, and mixed-method bundles
pass the existing release-smoke boundary.

The fixed 50-member LudoWeave producer explicitly emits only deflate method
`8`. Producer reproducibility and verifier admission are separate contracts.

## Decision

Retain sample-member compression-method compatibility. Complete release smoke
continues to admit exactly methods `0` and `8` through M64 and adds no exact
deflate-only profile after M112.

M95's local/central method-consistency check remains unchanged. A supported
method cannot bypass the established flag, path, file-type, size, inventory,
staging, read, cleanup, or content-silent diagnostic boundaries. Methods
outside the existing two-method sample profile remain rejected.

The fixed producer continues to emit method `8` for reproducible artifacts.
The verifier does not rewrite stored payloads or infer producer identity from a
member's compression method.

This is one compression-method compatibility decision. It adds no error
category or precedence change.

## Boundary

M113 adds no exact deflate-only profile, no new decompressor, no additional
compression method, no compression-level policy, no compression-ratio policy,
no recompression, no payload-content read, no raw compression-stream parser,
no repair, and no general ZIP validity claim. It is not a general archive
sandbox and is not a real public release observation.

M113 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, verifier, sample producer,
release mutation, release authority, tag, release, or publication.

## Consequences

- Standard-library stored and deflated sample bundles remain admitted when
  every established check passes.
- M95 continues to reject local/central method disagreement before reads or
  staging.
- BZIP2, LZMA, Zstandard, Deflate64, and unknown methods remain outside the
  private sample-bundle profile.
- The fixed producer remains byte-reproducible with deflate method `8`.
- No payload is decompressed until all existing preflight and inventory checks
  have passed.

## Alternatives considered

- Require exact deflate method `8`. Rejected because M64 deliberately admits
  both base ZIP methods, Python's standard writer defaults to stored, and no
  current extraction-security property depends on deflate-only admission.
- Expand admission to every compression method supported by each Python
  runtime. Rejected because the private sample profile needs only stored and
  deflated, and runtime support differs across versions and optional modules.
- Recompress stored members as deflate. Rejected because release smoke verifies
  and extracts checksum-admitted bytes; it does not repair or rewrite them.
- Inspect payload bytes to confirm method semantics independently. Rejected
  because M95 already binds local and central metadata and the standard-library
  decoder remains the owned extraction boundary after admission.

## References

- [PKWARE APPNOTE](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0047: bounded sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0078: require consistent local-header compression methods](0078-require-consistent-local-header-compression-methods.md)
- [RFC-0095: retain sample-member creating-system compatibility](0095-retain-sample-member-creating-system-compatibility.md)
