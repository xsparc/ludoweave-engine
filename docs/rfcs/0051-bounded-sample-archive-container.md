# RFC-0051: Bound the sample-archive container before parsing

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M68

## Context

M64 bounds the number, declared expanded size, compression methods, and streamed
copy size of sample-ZIP members. M65 through M67 then require portable member
identities, atomic publication, and the exact project inventory. Those checks
all begin after `zipfile.ZipFile` has opened the archive and parsed its central
directory.

The verifier therefore admits an unbounded container to the standard-library
parser before applying its extraction-work limits. Python's `zipfile`
documentation warns that archive processing is subject to memory and disk
resource limits, supports a seekable file-like object as the `ZipFile` input,
and returns the parsed central-directory entries through `infolist()`. OWASP
recommends explicit stored-file size limits in addition to safe calculation of
post-decompression ZIP size.

M64 measured the then-current project bundle at 111,168 bytes. Its member set
and 8 MiB total expanded-size ceiling make a 16 MiB container allowance a
conservative project-specific parser-input boundary rather than an observed
product constraint.

## Decision

The private release smoke first checks path metadata to reject an obvious non-
regular or oversized source without opening it. It then opens the sample bundle
once in binary read mode and revalidates descriptor metadata from that same
opened handle before constructing `zipfile.ZipFile`. The descriptor check is
authoritative if the path identity changes between inspection and opening.

The opened source must be a regular file and its descriptor-reported length
must not exceed **16 MiB** (16,777,216 bytes). A non-regular source or oversized
container fails with a stable content-silent category before `ZipFile`
construction, central-directory parsing, staging-directory creation, archive
member reads, or extraction writes.

After admission, the verifier passes the same opened handle to `ZipFile` and
retains M64 through M67's existing complete metadata, expansion, path,
inventory, streaming, and publication checks. The outer file context closes
the handle after the archive context and on every failure.

M71/RFC-0054 supersedes only that direct-parser detail: descriptor admission
still occurs on the opened source, then a bounded checksum-admitted snapshot
copies its bytes and becomes the `ZipFile` input. The source and snapshot retain
the same verifier-owned close ordering.

The limit and helper remain private implementation details of the release-smoke
script. They are not engine configuration, public Python API, or a general ZIP
format promise.

## Boundary

M68 protects one project-produced sample bundle in the single-process release
smoke. It is not a general archive sandbox, content scanner, malware detector,
raw ZIP parser, authenticated-metadata scheme, or defense against privileged or
concurrent filesystem replacement.

Descriptor admission binds validation and parsing to the same opened file, but
does not make later bytes immutable and does not claim crash, kernel, device, or
host compromise isolation. The staged-release checksum and manifest remain the
authority for expected byte identity. M64's uncompressed-size and codec limits
remain necessary because a small admitted container can still expand greatly.

M68 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Oversized and non-regular container inputs fail before the ZIP parser receives
  them.
- Obvious non-regular inputs fail before an open that could block on a special
  file; descriptor revalidation still catches replacement between checks.
- One descriptor supplies both admission metadata and every archive read,
  avoiding separate check-then-reopen file identities.
- Valid project bundles retain over two orders of magnitude of measured growth
  headroom beneath the parser-input ceiling.
- Compressed and expanded limits now bound distinct layers and remain required
  together.

## Alternatives considered

- Rely only on the staged-release checksum. Rejected because byte identity does
  not bound parser input or availability cost.
- Use `Path.stat()` and then reopen by path. Rejected because validation and
  parsing could refer to different file identities.
- Read the whole archive into a bounded in-memory buffer. Rejected because one
  already-open seekable regular file provides the required standard-library
  seam without an additional full-size allocation.
- Set the container cap equal to the 8 MiB expanded-content cap. Rejected
  because ZIP headers and stored incompressible content need overhead beyond
  the admitted expanded payload.
- Write a raw bounded central-directory parser. Rejected because the narrow
  16 MiB input boundary closes the evidenced resource gap without duplicating
  the ZIP implementation.

## References

- [Python 3.12 `zipfile` documentation](https://docs.python.org/3.12/library/zipfile.html)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0050: require the exact sample-bundle inventory](0050-exact-sample-bundle-inventory.md)
