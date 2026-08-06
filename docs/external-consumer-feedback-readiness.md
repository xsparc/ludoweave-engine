# External consumer feedback readiness

M25 defines how RFC-0003 gate 2 can be evidenced without relabeling a
project-owned sample, synthetic test, or hosted CI run as external adoption.
The current feedback manifest is empty, so the gate remains false.

The repository manifest is
`tests/fixtures/external_consumer_feedback.json`. Its exact SHA-256 is pinned by
the installed evidence and strict validator. Future accepted records are
append-only: once a record is reviewed, its full identity enters the executable
mandatory prefix and cannot be silently replaced by changing only the corpus
digest.

## Admission rule

Gate 2 can become true only when all of these are true together:

1. at least one consumer is independently owned rather than a LudoWeave
   project sample or maintainer-controlled fixture;
2. the consumer has a public, real command/transaction/receipt integration at
   a pinned repository revision;
3. the record identifies the exact LudoWeave package version and all three v1
   protocol identities;
4. integration and written-feedback artifacts have exact SHA-256 identities;
5. the feedback outcome is recorded as `compatible` or `issues-found`—negative
   feedback still counts as feedback and must not be hidden;
6. the public repository and evidence locators, ownership relationship,
   revision, artifacts, and outcome are manually verified during review; and
7. the exact whole-manifest digest and every previously accepted record prefix
   are pinned by reviewed executable evidence.

The local tool validates structure, limits, exact identities, duplicates,
protocol coverage, reviewed digest, and append-only prefix. It intentionally
does not contact a repository host or decide whether a consumer is truly
independent. Reviewers own that external fact before updating the reviewed
digest and mandatory prefix.

A synthetic test using `example.invalid` proves only the gate logic. It is not
an external consumer, feedback artifact, adoption result, release, or preview
promotion.

Today the report returns:

- `independent_consumer_feedback: false`;
- `gate_satisfied: false`;
- `external_feedback_proven: false`; and
- `status: not-ready`.

## Installed evidence

Run from the repository:

```console
python examples/external_consumer_feedback_readiness.py
```

The release sample bundle includes an exact copy of the empty reviewed manifest.
The example also accepts an explicitly selected local manifest:

```console
python examples/external_consumer_feedback_readiness.py --corpus tests/fixtures/external_consumer_feedback.json
```

It emits one deterministic
`ludoweave.evaluation.external-consumer-feedback-readiness/1` JSON document.
The report contains counts, versions, protocol/outcome identities, booleans,
reason codes, and the manifest digest. It omits consumer identifiers,
repositories, revisions, evidence locators, artifact hashes, paths, environment
facts, timings, credentials, and provider messages.

## Ownership, failure, and security

The harness is an explicitly invoked repository/release validation tool, not a
runtime loader or telemetry collector. It reads one bounded local JSON document.
Unknown fields, malformed identifiers, mutable/non-HTTPS locators, duplicate
consumers, invalid hashes/revisions, project-owned relationships, incomplete
protocol coverage, unsupported outcomes, record-count overflow, unreviewed
corpus identity, or missing mandatory history fail closed.

Execution is synchronous on the calling thread. The harness retains no file
handle, world, provider, process, socket, credential, global registry, or user
profile. It performs no discovery, dynamic import, installation, subprocess
launch, network access, repository lookup, analytics, or publication.

## Stability boundary

RFC-0008 records admission machinery only. RFC-0003 gate 2 remains false;
actual cross-version history and a supported deprecation-capable feature-release
channel also remain absent. Command, transaction, receipt, and reader exports
remain experimental.

M25 adds no runtime module, public export, protocol field, operation, handler,
telemetry, dependency, lock change, package version, workflow job, tag, release,
or publication.
