# RFC-0054: Parse a checksum-admitted sample snapshot

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M71

## Context

M70 hashes the opened sample source before ZIP parsing and again before
publication. That detects replacement before use and persistent mutation during
use, but `ZipFile` still reads the externally mutable source descriptor between
those comparisons. A capable local actor could change and restore source bytes
between checks, so the parser was not directly confined to the exact bytes
whose digest matched `SHA256SUMS`.

Python documents `SpooledTemporaryFile` as a file-like temporary object that
remains in memory until its configured size is exceeded or rollover is
requested. `ZipFile` accepts seekable file objects. The existing M68 16 MiB
container cap therefore permits one bounded, private parser snapshot without a
dependency or native facility. CWE-367 motivates minimizing separation between
resource validation and use, while SLSA treats artifact digest verification as
a consumer responsibility.

## Decision

After M68 path and descriptor admission, sample extraction creates one owned
binary spooled temporary file. It copies the source once in blocks while
computing SHA-256 and reads at most 16 MiB plus one rejection byte. An over-limit
source or digest mismatch clears the temporary target and raises the existing
stable content-silent error `sample bundle checksum does not match staged
release` before ZIP parsing or staging.

On success, both source and snapshot are rewound and `ZipFile` receives the
checksum-admitted snapshot. The parser and every member read therefore consume
the exact bytes whose digest matched the staged release. The snapshot, archive,
and source are verifier-owned and close in reverse acquisition order on success
or failure.

Direct private helper calls that omit an expected digest retain their existing
test utility behavior: they still parse a bounded owned snapshot but make no
staged-release checksum claim. Complete release smoke always supplies the
already validated `SHA256SUMS` entry.

## Boundary

M71 creates no persistent copy, public cache, recovery artifact, filesystem
lock, source-immutability guarantee, raw ZIP parser, signature, provenance
authority, or general archive sandbox. It does not prevent the source path or
descriptor from changing; instead it prevents those later changes from
altering the private parser input after checksum admission. Process compromise,
memory corruption, temporary-storage implementation defects, and SHA-256
collision resistance remain outside this boundary.

M71 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- `ZipFile` no longer consumes the mutable source descriptor in the admitted
  complete-release-smoke path.
- Parser input is the exact bounded byte sequence that matched the expected
  sample digest.
- Source change-and-restore after the copy cannot alter the parser snapshot.
- M70's second source hash is unnecessary because publication derives entirely
  from the already admitted owned snapshot.
- Accepted archives stay within the existing 16 MiB spooling and work bound.

## Alternatives considered

- Retain two source-descriptor hashes. Rejected because change-and-restore
  between comparisons remains possible.
- Copy to a named persistent file. Rejected because the bounded spooled
  temporary file has simpler ownership and no persistent-copy lifecycle.
- Read the whole archive into immutable `bytes`. Rejected because the file-like
  snapshot composes directly with `ZipFile` and exposes explicit close
  ownership while remaining bounded.
- Apply operating-system locks. Rejected because portable locking does not
  supply the desired exact parser-byte identity.

## References

- [Python 3.12 `tempfile` documentation](https://docs.python.org/3.12/library/tempfile.html#tempfile.SpooledTemporaryFile)
- [Python 3.12 `zipfile` documentation](https://docs.python.org/3.12/library/zipfile.html)
- [MITRE CWE-367: Time-of-check Time-of-use Race Condition](https://cwe.mitre.org/data/definitions/367.html)
- [SLSA v1.2: Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [RFC-0051: bound the sample-archive container](0051-bounded-sample-archive-container.md)
- [RFC-0053: bind sample parsing and publication to its checksum](0053-bind-sample-archive-checksum.md)
