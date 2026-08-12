# RFC-0057: Normalize sample ZIP decompression failures content-silently

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M74

## Context

M72 and M73 normalize documented ZIP parser failures and strict UTF-8 name-
decoding failures around the private checksum-admitted sample extractor. The
same extractor admits only stored and deflated members, then streams each
member through Python's standard ZIP reader in bounded blocks.

Official Python documentation defines `zlib.error` as the exception for
compression and decompression failures. Exact installed CPython 3.12.13,
3.13.13, and 3.14.5 implementations pass deflated member bytes directly to a
raw-deflate decompressor. A checksum-admitted archive can have valid container
metadata and exact expected inventory but invalid compressed payload bytes;
before M74, reading such a member escaped as a raw `zlib.error` after staging
had begun.

## Decision

The private `_extract_bundle` outer catch adds exactly `zlib.error` to the
existing `BadZipFile`, `LargeZipFile`, and `UnicodeDecodeError` tuple. It
reuses the stable error `sample bundle ZIP data is invalid` raised with
suppressed context.

The original decompression exception remains available as programmatic
`__context__`. Normal formatted exception output omits its library-specific
decompression diagnostic. Because translation remains outside the checksum-
admitted extractor, source, snapshot, archive, member, target, and temporary-
stage cleanup completes before the stable error returns.

Verifier policy errors remain specific. The catch deliberately excludes
`EOFError`, `OSError`, broad compression/error families, and `Exception`.
Filesystem, subprocess, memory, truncated-stream categories not established by
this decision, and unexpected implementation failures retain their existing
types and context. The unchanged sample producer remains admitted.

## Boundary

M74 is private complete-release-smoke behavior. It creates no public error
protocol, replacement decompressor, metadata or payload repair, telemetry,
logging system, recovery artifact, raw ZIP parser, content scanner, malware
detector, signature, or provenance authority. Suppressed context controls
normal rendered output; it does not erase the exception from trusted in-
process inspection.

M74 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. It is not a general
archive sandbox. Pull-request evidence is not a real public release
observation.

## Consequences

- Invalid raw-deflate payload failures share the stable outer ZIP-data error.
- Decompressor diagnostics stay out of normal rendered output.
- The original `zlib.error` remains available programmatically.
- Owned source, snapshot, archive, member, target, and staging cleanup
  completes first.
- EOF, verifier-policy, filesystem, and other failures keep their existing
  categories.

## Alternatives considered

- Preserve raw decompression failures. Rejected because a private verifier's
  rendered failure should not expose library- and content-determined parser
  diagnostics.
- Catch `EOFError`, `OSError`, or `Exception`. Rejected because those broad or
  distinct categories are not established as the exact decompressor failure
  addressed here.
- Pre-decompress every member during preflight. Rejected because it duplicates
  the existing bounded extraction pass without removing the need to handle
  decompressor failure.
- Replace or repair compressed payloads. Rejected because the verifier should
  fail closed on a checksum-admitted invalid sample.
- Implement a custom ZIP or deflate parser. Rejected as unnecessary scope and
  a larger security surface.

## References

- [Python 3.12 `zlib.error` documentation](https://docs.python.org/3.12/library/zlib.html#zlib.error)
- [Python 3.12 `zipfile` implementation](https://github.com/python/cpython/blob/3.12/Lib/zipfile/__init__.py)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
- [RFC-0055: normalize sample ZIP failures content-silently](0055-content-silent-sample-zip-failures.md)
- [RFC-0056: normalize sample ZIP text failures content-silently](0056-content-silent-sample-zip-text-failures.md)
