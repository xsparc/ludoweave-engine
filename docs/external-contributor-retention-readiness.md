# External contributor-retention readiness

No retained external contributor is currently admitted. M29 provides a
strict offline path for measuring the design plan's preference for contributor
retention over raw star counts without turning maintainers, non-human
automation, synthetic fixtures, CI activity, or repository popularity into
people.

## What can count

A future record can count only after human review establishes all of these
facts together:

- one independently reviewed external human made two distinct contributions
  to the public LudoWeave repository;
- the first and return contributions each link distinct public issues and
  merged pull requests and record exact base, head, and merge Git identities;
- the return contribution merged after the first contribution;
- both contributions have valid DCO sign-off, complete the clean-setup,
  focused-check, and complete-gate validation sequence, and have reviewed
  provenance and validation evidence;
- exact patch and review SHA-256 identities are distinct within and across
  records; and
- reviewers explicitly establish contributor identity, continued external
  independence, same-person continuity, chronology, and the retention result.

Public GitHub logins are canonicalized case-insensitively before identity and
history checks, so spelling case cannot count the same contributor twice.

The first and return contribution may cover a bug fix, documentation, feature,
maintenance, tests, or tooling. The evaluator validates only frozen reviewed
facts. It cannot infer a person's identity or independence, inspect GitHub,
verify ancestry, decide whether two accounts identify the same person, or
replace human review.

## Current evidence

The reviewed manifest is exactly 274 bytes and contains zero retention records.
Its SHA-256 is
`61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee`.
The deterministic report is therefore `not-ready`, with zero retained
contributors, zero return contributions, and reason code
`retained-external-contributor-absent`.

Run the source-tree evidence explicitly:

```console
uv run --frozen python examples/external_contributor_retention_readiness.py
```

The same evaluator and exact empty manifest run from an isolated wheel and the
deterministic release sample bundle. Generated reports omit contributor
identities, issue and pull-request locations, revisions, artifact hashes,
timestamps, local paths, platform facts, and timings. Candidate or incomplete
history exposes no record-derived counts or scopes.

Synthetic populated fixtures prove only fail-closed admission mechanics. They
are not contributors, issues, pull requests, feedback, retention, adoption, or
project history. Stars, forks, downloads, traffic, and CI authorship never
enter the report.

## History and updates

Before a nonempty manifest is accepted, reviewers must pin its complete
ordered retention identity sequence as the mandatory history and pin the exact
whole-manifest SHA-256 in the evaluator and installed validator. A reviewed
manifest cannot silently add, drop, replace, reorder, or reuse an accepted
contributor, issue, pull request, head/merge revision, or artifact identity.

The public manifest may contain only a public GitHub login, public project
references, immutable Git identities, artifact hashes, canonical public merge
timestamps, and bounded review facts. Never add email addresses, credentials,
private messages, private prompts, local paths, telemetry, or unpublished
personal information.

## Boundaries

The evaluator performs one bounded synchronous read of an explicitly selected
local JSON document. It uses no networking, telemetry, discovery, dynamic
imports, subprocesses, provider execution, GitHub API, or retained external
resources. Duplicate fields, excessive nesting, and non-ASCII timestamp
lookalikes fail closed. M29 does not contact contributors, mutate issues or
pull requests, publish a package, promote stability, change runtime source or public APIs,
change persistent formats or dependencies, or alter the workflow and CI
topology.

See
[RFC-0012](rfcs/0012-external-contributor-retention-admission-readiness.md)
for the accepted decision.
