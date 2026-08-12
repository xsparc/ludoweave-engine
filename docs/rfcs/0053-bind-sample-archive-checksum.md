# RFC-0053: Bind sample-archive parsing and publication to its checksum

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M70

## Context

Complete release smoke validates every staged artifact against `SHA256SUMS`,
and later validates the release manifest's recorded hashes. Sample extraction,
however, subsequently reopened the bundle and admitted only its path and
descriptor type and size before passing the opened handle to `ZipFile`. A
content-silent replacement after the earlier checksum pass could therefore be
parsed and published without reproducing the checksum already admitted for the
staged release.

Python's `zipfile` accepts seekable file objects, and `hashlib` provides the
incremental SHA-256 primitive needed to hash a binary stream. CWE-367 describes
the general time-of-check/time-of-use weakness created when a resource changes
between validation and use. SLSA likewise treats verification of artifact
bytes against expected provenance as a consumer responsibility. M70 narrows
this specific private verifier gap without claiming immutable input.

## Decision

The complete release-smoke composition root passes
`checksums[bundle.name]` to sample extraction. After path admission, the
extractor opens the archive once and revalidates the descriptor as M68 already
requires. It then hashes that same opened handle from byte zero, compares the
digest with the expected `SHA256SUMS` value, and rewinds the handle before ZIP
parsing. This sample-specific hash reads at most M68's 16 MiB limit plus one
rejection byte, so a growing source cannot turn checksum work into an unbounded
read.

After every admitted member has been read and staged completeness has been
validated, the extractor hashes and rewinds the same opened handle again. A
mismatch at either boundary raises the stable content-silent error `sample
bundle checksum does not match staged release`. The second comparison occurs
before publication by final staged-root rename. The archive context still
closes before its underlying stream on every path.

## Boundary

This is a private complete-release-smoke boundary for the project sample
bundle. It creates no snapshot, copy, filesystem lock, operating-system
isolation, raw local-header parser, signature, or immutable-input guarantee.
An actor able to change and restore bytes between the two checks may evade this
specific defense. The rule is not a general archive sandbox and does not
authenticate ZIP metadata independently of the admitted archive bytes.

M70 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Replacing the bundle after the earlier staged-artifact checksum pass but
  before extraction opens it now fails before ZIP parsing or staging.
- Hashing preserves M68's input-resource bound even if the opened source grows
  after descriptor admission.
- A persistent mutation of the admitted descriptor during extraction fails
  before publication and owned partial staging is cleaned.
- The unchanged deterministic sample producer remains admitted by its exact
  digest from `SHA256SUMS`.
- Both comparisons operate on the same opened handle that `ZipFile` parses;
  the path is not reopened between checksum admission and parsing.

## Alternatives considered

- Rely only on the earlier staged-artifact checksum. Rejected because
  extraction subsequently reopened the bundle.
- Parse an immutable in-memory or temporary snapshot. Deferred because it
  adds another copy/resource boundary and is unnecessary for this bounded
  same-descriptor improvement.
- Parse raw local headers and content directly. Rejected as a materially larger
  parser and archive-sandbox surface.
- Apply operating-system file locks. Rejected because portable lock semantics
  do not provide the desired cross-platform immutable-input guarantee.

## References

- [Python 3.12 `zipfile` documentation](https://docs.python.org/3.12/library/zipfile.html)
- [Python 3.12 `hashlib` documentation](https://docs.python.org/3.12/library/hashlib.html)
- [MITRE CWE-367: Time-of-check Time-of-use Race Condition](https://cwe.mitre.org/data/definitions/367.html)
- [SLSA v1.2: Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [RFC-0049: stage sample extraction before publication](0049-atomic-sample-extraction.md)
- [RFC-0051: bound the sample-archive container](0051-bounded-sample-archive-container.md)
