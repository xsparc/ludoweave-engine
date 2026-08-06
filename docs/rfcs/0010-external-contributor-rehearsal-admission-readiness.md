# RFC-0010: External-contributor rehearsal admission readiness

- **Status:** Accepted
- **Date:** 2026-08-07
- **Decision:** Define strict first-contribution rehearsal admission and retain the current result as false
- **Related:** [readiness guide](../external-contributor-rehearsal-readiness.md), [first contribution](../first-contribution.md), [triage](../triage.md), [RFC-0008](0008-external-consumer-feedback-admission-readiness.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence for the
design-plan objective that project documentation enables a first external
contribution without private maintainer knowledge. Retain the result as false
because the reviewed manifest contains no contribution rehearsals.

M27 defines how a later real contribution can be admitted. It does not solicit
or contact a contributor, invent an issue or pull request, publish telemetry,
change project workflows, or claim usability, adoption, or external review.

## Context

A walkthrough, good-first issue form, pull-request template, and passing CI
show that a public path is documented and mechanically viable. They do not
show that an independent person could follow that path without undocumented
maintainer help. Project-owned synthetic tests cannot supply that missing human
evidence.

The relevant event is a narrowly scoped contribution from an independent human
that starts with a public issue, completes the documented setup and validation
path, records feedback, and merges with valid DCO sign-off. Because identity,
independence, and assistance are social facts, an offline evaluator must not
infer them from GitHub metadata or network queries.

## Decision

The contributor-rehearsal manifest:

1. requires at least one manually reviewed, independently contributed, merged
   good-first project pull request linked to a public project issue;
2. permits only bounded bug-fix, documentation, test, or tooling scope;
3. records exact distinct base, head, and merge Git object IDs plus distinct
   SHA-256 identities for the reviewed patch and contributor feedback, with
   head/merge and artifact identities unique across records and roles;
4. requires valid DCO sign-off, the documented clean-setup, focused-check, and
   complete-gate sequence, and explicit review that no private maintainer
   knowledge was used;
5. rejects records that change a public API, persistent format, dependency, or
   workflow;
6. preserves every accepted record through an executable mandatory full-record
   prefix equal to the complete reviewed manifest identity sequence;
7. requires the exact whole-manifest digest to be pinned by reviewed code and
   strict installed evidence; and
8. never counts project-owned fixtures, automated agents, documentation text,
   CI passes, opened-but-unmerged pull requests, maintainer-authored changes,
   or synthetic GitHub-shaped URLs as external-contributor evidence.

Before pinning a nonempty manifest, human reviewers verify the contributor's
independence, public issue and pull request, exact revisions, patch/feedback
hashes, task scope, DCO state, validation evidence, merge result, assistance
record, and absence of protected changes. The evaluator validates the frozen
record but cannot replace that review.

The current normative report is `not-ready`, with zero records and reason code
`external-contributor-rehearsal-absent`. Synthetic future-state regressions use
nonexistent canonical-shaped project references solely to prove gate behavior.

## Security, privacy, and determinism

The evaluator reads one explicitly selected bounded local manifest. It rejects
unknown fields, malformed or repeated identities, noncanonical project URLs,
invalid Git/SHA identities, incomplete validation, unreviewed independence,
non-human contributors, private-knowledge use, protected changes, symlinks,
oversized documents, and excess records.

The reviewed manifest is public evidence and may contain a public GitHub login,
public project references, Git object IDs, and artifact hashes. It must never
contain an email address, private communication, credential, private prompt,
local path, telemetry record, or unpublished personal information. Generated
reports omit contributor identities, URLs, revisions, hashes, paths, platform
facts, and timings.

The harness performs no discovery, remote lookup, dynamic import, installation,
subprocess, networking, telemetry, contributor contact, issue mutation, or
provider execution. It is synchronous and owns no external resource.

## Consequences

- The contributor-usability objective now has an exact, artifact-exercised
  admission path, but remains false.
- Existing public contribution documents remain useful without being presented
  as completed usability evidence.
- A real independently reviewed merged contribution and feedback record are
  required before the result can become true.
- M27 changes no runtime source, public export, wire/persistent format,
  dependency, lock, package version, workflow topology, tag, or publication.

## Alternatives considered

- **Count the public walkthrough or CI matrix.** Rejected because project-owned
  documentation and automation do not establish independent human usability.
- **Count an automated-agent pull request.** Rejected because the design metric
  specifically concerns an external human contributor using public guidance.
- **Query GitHub during CI.** Rejected because remote state is mutable and
  cannot establish independence or undisclosed assistance.
- **Store private interviews or email.** Rejected because only minimal public
  evidence and reviewed artifact hashes belong in the repository.
- **Allow API, dependency, workflow, or format changes.** Rejected because a
  first-contribution rehearsal should remain bounded and independently
  reviewable without a separate architectural decision.
- **Mark the objective complete from synthetic tests.** Rejected because those
  fixtures prove validation mechanics, not an external contribution.
