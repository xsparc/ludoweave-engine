# External-contributor rehearsal readiness

M27 turns the community-alpha first-contribution objective into a strict,
offline admission contract. The current result is deliberately `not-ready`:
the public walkthrough exists, but no independent external contributor has
completed a reviewed contribution rehearsal.

Run the installed evidence path against the repository fixture:

```console
python examples/external_contributor_rehearsal_readiness.py --rehearsals tests/fixtures/external_contributor_rehearsal.json
```

The command reads one explicitly selected local JSON document and emits one
versioned, path-free JSON report. The same path runs from the pure wheel and
the deterministic release sample bundle. It performs no discovery, dynamic
import, subprocess execution, network access, telemetry, issue mutation, or
contributor contact.

## What would satisfy the gate

A future reviewed manifest must preserve every earlier accepted record and
contain at least one actual merged contribution that:

- was made by an independently reviewed human contributor;
- links a canonical public project issue and pull request;
- records distinct exact base, head, and squash/merge Git object IDs;
- binds the reviewed contribution patch and feedback with SHA-256 identities;
- is limited to a good-first bug fix, documentation, test, or tooling task;
- completed clean setup, the focused check, and the complete public gate;
- has valid DCO sign-off and a merged outcome;
- required no private maintainer knowledge; and
- changed no public API, persistent format, dependency, or workflow.

The complete reviewed manifest identity sequence must equal the executable
mandatory prefix, and the exact whole-document digest must be pinned in the
evaluator and strict installed evidence. Revision and artifact identities are
unique across roles and records. Pinning only a digest is insufficient.

## Review authority and privacy

Humans establish that the contributor is independent, that the contribution
was completed without private maintainer knowledge, that its public issue/PR
and revisions are genuine, and that the patch and feedback hashes identify the
reviewed artifacts. The evaluator validates frozen reviewed facts; it cannot
infer independence, contribution quality, provenance, or contributor intent.

The public manifest deliberately contains only the contributor's public GitHub
login, public project references, Git object IDs, artifact digests, and bounded
review facts. Never add email addresses, credentials, private messages,
private prompts, local paths, telemetry, or unpublished personal information.
The emitted report omits the login, URLs, revision IDs, and artifact hashes.

## Current evidence and non-claims

The normative manifest has zero rehearsal records, so the report contains
`external-contributor-rehearsal-absent` and cannot prove that the documentation
works without private maintainer knowledge. Synthetic populated fixtures in
the tests prove fail-closed gate mechanics only. They are not contributors,
issues, pull requests, feedback, adoption, usability research, or project
history.

M27 adds no runtime package, public export, persistent format, dependency,
version, workflow job, provider, transport, publication, or support promise.
See [RFC-0010](rfcs/0010-external-contributor-rehearsal-admission-readiness.md)
and the [first-contribution walkthrough](first-contribution.md).
