# RFC-0008: External consumer feedback admission readiness

- **Status:** Accepted
- **Date:** 2026-08-07
- **Decision:** Define strict external-feedback admission and retain gate 2 as false
- **Related:** [readiness guide](../external-consumer-feedback-readiness.md), [RFC-0003](0003-retain-experimental-command-receipt-contracts.md), [RFC-0007](0007-cross-version-corpus-admission-readiness.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence that
distinguishes reviewable external command/receipt integration feedback from
project-owned tests and samples. Retain RFC-0003 gate 2 as false because the
current reviewed manifest has no feedback records.

M25 defines how a later external fact can be admitted. It does not create a
consumer, contact a repository host, collect telemetry, claim adoption, or
promote stability.

## Context

RFC-0003 requires feedback from at least one real external command/receipt
integration before preview promotion. The project has many installed examples,
conformance profiles, and hosted platform passes, but all are project-owned.
Counting them as consumer feedback would make the gate meaningless.

External evidence also carries privacy and provenance risks. A useful record
must be public, consented by publication, revision-pinned, reviewable, and
sanitized in generated reports. The local validator cannot prove ownership or
fetch remote facts; review must remain the authority for those claims.

## Decision

The feedback manifest:

1. requires at least one distinct independently owned consumer;
2. accepts only a public command/transaction/receipt integration at an exact Git
   revision and exact LudoWeave version;
3. requires all three current protocol identities;
4. records exact integration and written-feedback SHA-256 identities plus
   immutable HTTPS repository/evidence locators;
5. records `compatible` and `issues-found` outcomes without treating negative
   feedback as a failed or suppressible record;
6. is append-only through executable mandatory full-record prefixes;
7. requires the exact whole-manifest digest to be pinned by reviewed code and
   strict installed evidence; and
8. never treats a project-owned sample, synthetic fixture, bot review, hosted CI
   pass, benchmark, download count, or anonymous telemetry as external feedback.

Before pinning a non-empty manifest, reviewers verify consumer independence,
public consent, repository ownership, immutable revision/locators, artifact
hashes, protocol use, package version, and the feedback outcome. The offline
tool validates the frozen record but does not replace that review.

The current normative report is `not-ready` with zero consumers and reason code
`external-consumer-feedback-absent`. The synthetic future-state regression
proves only gate mechanics and uses the reserved `example.invalid` domain.

## Security, privacy, and determinism

The tool reads one explicitly selected bounded local manifest. Exact fields,
safe bounded identifiers, HTTPS locators without query/fragment components,
Git/SHA identities, record count, unique consumers, protocol coverage,
outcomes, reviewed digest, and mandatory history fail closed.

Generated reports omit consumer identifiers, repositories, revisions, locators,
artifact hashes, paths, environment/platform facts, timings, credentials, and
provider messages. The public manifest itself is deliberate reviewed evidence;
private feedback must not be copied into it.

The harness performs no discovery, dynamic import, installation, subprocess,
network access, telemetry, repository lookup, global registration, or
publication. It is synchronous and retains no external resource.

## Consequences

- Gate 2 now has an exact, artifact-exercised admission route, but remains false.
- Project-owned evidence continues not to count as external adoption.
- Negative external feedback can be retained honestly and trigger later work.
- Command/receipt stability remains experimental because gates 1, 2, and 6 are
  false.
- M25 changes no runtime source, public export, wire format, dependency, lock,
  package version, CI topology, tag, release, or publication.

## Alternatives considered

- **Count the sample applications or conformance profiles.** Rejected because
  they are maintained in this repository.
- **Count GitHub stars, downloads, or package index traffic.** Rejected because
  they do not prove command/receipt integration or actionable feedback.
- **Collect anonymous telemetry.** Rejected because it adds privacy, consent,
  networking, security, and operability scope without proving reviewed use.
- **Fetch external repositories during CI.** Rejected because admission must be
  deterministic, offline, and resistant to mutable remote state.
- **Add a synthetic record to make the gate green.** Rejected because a unit
  test is not an external consumer fact.
- **Promote after defining the harness.** Rejected because the corpus is empty,
  cross-version release history is absent, and no supported release channel
  exists.
