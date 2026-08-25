# RFC-0099: Separate sample-bundle semantic portability from byte identity

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

RFC-0098 scopes sample-bundle byte reproducibility to repeated production
inside one fixed resolved release environment. It records that default Windows
CPython 3.14 uses zlib-ng and can emit different compressed bytes from the zlib
implementation used by exact Windows CPython 3.12 and 3.13.

Different compressed representations do not necessarily imply different
archive semantics. PKWARE assigns ZIP compression method `8` to Deflate.
Python exposes that method as `ZIP_DEFLATED`, describes it as the usual ZIP
compression method, and reads it through the available zlib-compatible module.
Python reports no known compatibility issue from the default Windows zlib-ng
change, and zlib-ng provides a zlib-compatible API.

Exact Windows CPython 3.12.13, 3.13.13, and 3.14.5 each produced the fixed 50-
member LudoWeave sample bundle. Every one of those runtimes then consumed all
three archives through the complete sample extraction boundary. All nine
producer-consumer combinations passed and extracted all 50 source files. The
canonical extracted-tree SHA-256 was
`eb4089dc35539baa9af95c757da9172506d61b6d45ab19d5ad5d8740b77a9ed0`
in every combination. The
3.12/3.13 archive remained 111,168 bytes at SHA-256
`52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
the 3.14 zlib-ng archive remained 111,413 bytes at SHA-256
`d592e99c8c3a65ae63f0cf89ed7eff6094365ca98ba58d08c2099fac4316834b`.

## Decision

Separate sample-bundle semantic portability from byte identity. Supported
runtime producers may emit different valid Deflate bytes under RFC-0098 while
their fixed-producer archives remain acceptable to supported runtime consumers
and extract the same source-defined sample tree.

Record the exact Windows 3x3 matrix as cross-runtime producer-consumer
compatibility evidence. Keep the standard method `8` boundary, fixed producer,
complete release checks, integrity digests, and extraction ownership unchanged.

This is one sample-bundle semantic-portability decision. It does not replace
artifact digest verification: each particular staged release still carries and
must satisfy its own exact manifest/checksum identity.

## Boundary

M116 adds no alternate compression method, new decoder, compressor pin,
recompression, payload transformation, runtime branch, digest allowlist,
cross-runtime byte-identity claim, or cross-platform proof. It does not admit an
arbitrary ZIP producer and is not a general ZIP interoperability claim.

M116 adds no workflow, runner allocation, matrix entry, action, permission,
credential, dependency, lock, version, runtime package/API, verifier, sample
producer, release mutation, release authority, tag, release, or publication.
It is not a real public release observation.

## Consequences

- The exact Windows supported-runtime matrix distinguishes semantic extraction
  success from compressed-byte equality.
- A particular release bundle remains bound to its own manifest and checksum;
  portability does not bypass artifact identity.
- M64, M95, and M113 continue to own compression-method admission and
  consistency. M114 and M115 continue to own level non-observability and byte-
  reproducibility scope.
- Cross-platform producer-consumer evidence remains future work rather than an
  inferred result.

## Alternatives considered

- Require one archive digest across supported runtimes. Rejected by RFC-0098
  and the observed zlib/zlib-ng producer variance.
- Add a digest allowlist for known runtime outputs. Rejected because release
  integrity already binds each staged artifact and an implementation allowlist
  would turn observations into permanent producer identities.
- Add another compression method. Rejected because semantic portability is
  proven within the established Deflate boundary and no alternate method is
  needed.
- Add a hosted cross-runtime artifact matrix. Rejected because the exact local
  evidence and existing supported-runtime tests establish this decision without
  another runner or job.

## References

- [PKWARE APPNOTE](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `zipfile` documentation](https://docs.python.org/3.14/library/zipfile.html)
- [What's new in Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html#zlib)
- [zlib-ng](https://github.com/zlib-ng/zlib-ng)
- [RFC-0096: retain sample-member compression-method compatibility](0096-retain-sample-member-compression-method-compatibility.md)
- [RFC-0098: scope sample-bundle byte reproducibility](0098-scope-sample-bundle-byte-reproducibility.md)
