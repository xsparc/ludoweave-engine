# RFC-0055: Normalize sample ZIP failures content-silently

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M72

RFC-0056 extends the same stable boundary to the exact ZIP metadata text-decoding
failure without changing this RFC's documented `BadZipFile`/`LargeZipFile`
decision.

## Context

M71 gives `ZipFile` an owned checksum-admitted snapshot, but the standard ZIP
parser still reports malformed data through its own exceptions. CPython 3.12
through 3.14 use `BadZipFile` diagnostics that can contain archive-controlled
filenames for CRC failures, mismatched central/local names, and overlapping
entries. `LargeZipFile` is the documented companion exception for ZIP64 limit
failures. Complete release smoke previously allowed those parser messages to
be rendered directly.

The verifier already has stable content-silent policy failures and owns the
source, snapshot, archive, and staging contexts. A narrow outer boundary can
therefore normalize documented parser failures after owned cleanup without
changing parser behavior or hiding verifier policy errors.

## Decision

The private `_extract_bundle` entry point delegates to the checksum-admitted
extractor and catches exactly `zipfile.BadZipFile` and
`zipfile.LargeZipFile`. Either becomes the stable error
`sample bundle ZIP data is invalid` raised with suppressed context.

Python retains the original exception as programmatic `__context__`, so a
trusted diagnostic caller can inspect its type and details. Normal formatted
exception output omits that context, keeping archive-controlled member names
and parser diagnostics content-silent. Because normalization occurs outside
the inner extractor, its `ExitStack` and temporary staging contexts complete
owned cleanup first on constructor, metadata, member-open, or member-read
failure.

Verifier-created policy `RuntimeError` values remain specific. Filesystem,
subprocess, memory, and unexpected implementation failures also retain their
existing types and context. The unchanged sample producer remains admitted.

## Boundary

M72 is private complete-release-smoke behavior. It creates no public error
protocol, general exception translation, telemetry, logging system, recovery
artifact, raw ZIP parser, content scanner, malware detector, signature, or
provenance authority. Suppressed context controls normal rendered output; it
does not erase the exception object from trusted in-process inspection.

M72 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. It is not a general
archive sandbox. Pull-request evidence is not a real public release
observation.

## Consequences

- Documented malformed-ZIP and ZIP64 parser failures share one stable outer
  category.
- Archive-controlled parser details do not appear in normal rendered output.
- The original parser exception remains available programmatically.
- Owned source, snapshot, archive, and staging cleanup completes first.
- Verifier policy and non-parser failures keep their existing categories.

## Alternatives considered

- Preserve raw `zipfile` diagnostics. Rejected because some diagnostics embed
  archive-controlled member names.
- Catch every exception from extraction. Rejected because it would collapse
  actionable verifier, filesystem, and implementation failures.
- Discard the original parser exception completely. Rejected because
  suppressed context provides output confinement while retaining trusted
  diagnostic evidence.
- Implement a custom ZIP parser. Rejected as unnecessary scope and a larger
  security surface.

## References

- [Python 3.12 `zipfile` documentation](https://docs.python.org/3.12/library/zipfile.html)
- [CPython 3.12 `zipfile` implementation](https://github.com/python/cpython/blob/3.12/Lib/zipfile/__init__.py)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
