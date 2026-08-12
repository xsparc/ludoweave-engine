# RFC-0056: Normalize sample ZIP text failures content-silently

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M73

## Context

M72 normalizes documented `BadZipFile` and `LargeZipFile` failures around the
private checksum-admitted sample extractor. Exact CPython 3.12 through 3.14
source also decodes UTF-8-marked archive-controlled member names strictly while
reading the central directory and again while reading a local header.

Malformed names raise `UnicodeDecodeError`, not `BadZipFile`. Its documented
attributes retain the invalid byte object, failing offsets, encoding, and
reason, and its normal message renders some of that detail. Before M73, a
malformed central-directory name escaped during `ZipFile` construction and a
malformed local-header name escaped during `archive.open` after staging began.

## Decision

The private `_extract_bundle` outer catch adds exactly `UnicodeDecodeError` to
the existing `BadZipFile` and `LargeZipFile` tuple. It reuses the stable error
`sample bundle ZIP data is invalid` raised with suppressed context.

The original decoding exception remains available as programmatic
`__context__`. Normal formatted exception output omits it, keeping the invalid
byte sequence, offsets, codec, and reason content-silent. Because translation
remains outside the checksum-admitted extractor, constructor-time and staged
member-open failures complete owned source, snapshot, archive, and temporary-
stage cleanup first.

Verifier policy errors remain specific. The catch deliberately excludes the
broader `UnicodeError`, its encoding/translation siblings, `ValueError`, and
`Exception`. Filesystem, subprocess, memory, and unexpected implementation
failures retain their existing types and context. The unchanged sample producer
remains admitted.

## Boundary

M73 is private complete-release-smoke behavior. It creates no public error
protocol, Unicode policy, replacement decoder, metadata rewriting, telemetry,
logging system, recovery artifact, raw ZIP parser, content scanner, malware
detector, signature, or provenance authority. Suppressed context controls
normal rendered output; it does not erase the exception from trusted in-process
inspection.

M73 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. It is not a general
archive sandbox. Pull-request evidence is not a real public release
observation.

## Consequences

- Central-directory and local-header UTF-8 decoding failures share the stable
  outer ZIP-data error.
- Archive-controlled invalid bytes and decode diagnostics stay out of normal
  rendered output.
- The original `UnicodeDecodeError` remains available programmatically.
- Owned source, snapshot, archive, and staging cleanup completes first.
- Other Unicode/value, verifier-policy, and non-parser failures keep their
  existing categories.

## Alternatives considered

- Preserve raw decoding failures. Rejected because their documented state and
  normal messages expose archive-controlled bytes and offsets.
- Catch `UnicodeError` or `ValueError`. Rejected because those families include
  unrelated failures not established as standard ZIP metadata decoding.
- Replace or repair malformed names. Rejected because the project requires a
  portable restricted sample inventory and should fail closed.
- Implement a custom ZIP parser. Rejected as unnecessary scope and a larger
  security surface.

## References

- [Python 3.12 `UnicodeDecodeError` documentation](https://docs.python.org/3.12/library/exceptions.html#UnicodeDecodeError)
- [CPython 3.12 `zipfile` implementation](https://github.com/python/cpython/blob/3.12/Lib/zipfile/__init__.py)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
- [RFC-0055: normalize sample ZIP failures content-silently](0055-content-silent-sample-zip-failures.md)
