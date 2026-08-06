# RFC-0007: Cross-version receipt-corpus admission readiness

- **Status:** Accepted
- **Date:** 2026-08-06
- **Decision:** Add a strict corpus admission harness and retain gate 1 as false
- **Related:** [readiness guide](../cross-version-corpus-readiness.md), [RFC-0003](0003-retain-experimental-command-receipt-contracts.md), [RFC-0004](0004-bounded-receipt-reader-and-v1-baseline.md), [RFC-0005](0005-built-in-operation-argument-compatibility.md), [RFC-0006](0006-receipt-semantic-diff-and-diagnostic-compatibility.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence that
audits the immutable M21 receipt baseline and states the exact admission rule
for future cross-version evidence. Retain RFC-0003 gate 1 as false because the
reader and source fixtures are all `0.1.0a1` and no supported-release records
exist.

M24 makes future evidence harder to fabricate; it does not create package
history, release support, external adoption, or a stability promotion.

## Context

RFC-0004 preserved exact committed, dry-run, and rejected receipt-v1 documents
for a later version to read. RFC-0005 and RFC-0006 fix the operation and receipt
evolution rules. The remaining cross-version gate still lacked one strict
composition that could distinguish current project-owned baseline checks from
actual execution by a different supported package version.

A naive green test could relabel the current fixtures as cross-version or use a
synthetic version string. A repository rule must instead preserve source bytes,
observe a distinct installed reader version, and require separately reviewed
release evidence.

## Decision

The admission manifest:

1. references each source manifest by safe directory name, source version,
   exact byte length, and SHA-256;
2. is append-only with respect to historical source and release records,
   enforced by executable frozen mandatory prefixes in addition to the reviewed
   whole-manifest digest;
3. requires at least two distinct versions across source fixtures and the
   installed reader;
4. requires the reader to differ from at least one source version;
5. requires supported-release records for every observed version; and
6. requires the exact admission-manifest digest to be pinned by reviewed code
   and strict installed-evidence validation; and
7. never treats a synthetic test, local version override, source example, or
   hosted same-version pass as release history.

The installed example verifies the manifest graph, exact receipt identities,
status coverage, bounded public decoding, and canonical round trips. It emits a
sanitized report and explicit reason codes. The current normative report is
`not-ready` with both cross-version execution and supported-release evidence
false.

Supported-release records carry exact version, `vVERSION` tag, Git object
identity, and artifact SHA-256. The local harness validates their structure and
coverage. Reviewers remain responsible for verifying the external tag,
artifact, support status, and provenance before accepting such a record.

## Security and determinism

The tool reads one explicitly selected local manifest and only bounded,
safe-basename children. Manifest bytes, child counts, per-receipt bytes, exact
fields, duplicate identities, manifest/fixture hashes, canonical receipt bytes,
and exact release-record coverage fail closed.
Successful reports omit paths, state/world hashes, values, environment facts,
timings, credentials, and provider messages.

The harness performs no discovery, dynamic import, code installation,
subprocess launch, network access, tag lookup, release publication, provider
selection, or global registration. It is synchronous and retains no external
resource.

## Consequences

- A later supported package version has one exact, artifact-exercised route to
  present gate-1 evidence.
- The current corpus remains explicitly single-version and gate 1 remains
  false.
- Existing M21 receipt bytes and their manifest remain unchanged.
- Command/receipt stability remains experimental because gates 1, 2, and 6
  are still false.
- M24 changes no runtime source, public export, wire format, dependency, lock,
  package version, CI topology, tag, release, or publication.

## Alternatives considered

- **Mark M21 fixtures cross-version now.** Rejected because source and reader
  versions are identical.
- **Use a synthetic version override as evidence.** Rejected because a unit
  test proves gate logic, not released-package history.
- **Trust filenames without byte identities.** Rejected because historical
  inputs could be silently rewritten.
- **Query GitHub or PyPI during validation.** Rejected because admission must be
  deterministic and offline; external release facts are reviewed before their
  immutable identities enter the corpus.
- **Promote the contracts after adding the harness.** Rejected because actual
  cross-version execution, external consumer feedback, and a supported
  deprecation-capable release channel remain absent.
