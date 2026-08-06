# Supported release channel readiness

M26 defines how RFC-0003 gate 6 can be evidenced without treating a tag-only
prerelease workflow, local release candidate, synthetic fixture, or hosted CI
run as an established deprecation-capable feature-release channel. The current
reviewed manifest has no release records, so the gate remains false.

The repository manifest is
`tests/fixtures/supported_release_channel.json`. Its exact SHA-256 is pinned by
installed evidence and the strict validator. Future accepted records are
append-only: once a release is reviewed, its full identity enters the
executable mandatory prefix and cannot be replaced by changing only the
manifest digest.

## Admission rule

Gate 6 can become true only when all of these are true together:

1. at least two final `MAJOR.MINOR.PATCH` releases exist on distinct
   major/minor feature lines;
2. every release remains supported, non-yanked, non-draft, and non-prerelease;
3. each release has an exact `vVERSION` tag, Git commit, canonical project tag
   URL, artifact SHA-256, and release-notes SHA-256;
4. every record uses the reviewed `github-release` publication channel;
5. versions are canonical, unique, and strictly increasing;
6. the compatibility policy continues to require a deprecation in at least one
   supported feature release before an incompatible preview removal; and
7. reviewers verify the actual published release, tag, commit, assets, notes,
   support, yank, draft, and prerelease status before pinning the whole-manifest
   digest and mandatory release prefix.

Two patch releases on the same feature line do not establish recurring feature-
release capability. Alpha/beta/RC versions do not count as final feature
releases. A negative or superseded release record is not deleted: it remains in
history and the gate stays false until the complete supported channel exists.

The local tool validates structure, limits, exact identities, ordering,
duplicates, reviewed digest, and append-only history. It intentionally does not
query GitHub, inspect a remote tag, download an artifact, or decide support
status. Reviewers own those external facts before updating the reviewed digest
and mandatory prefix.

A synthetic test using canonical-shaped project-tag URLs for nonexistent
releases proves only gate mechanics. It is not a release, channel, support
commitment, tag, publication, or preview promotion.

Today the report returns:

- `supported_feature_release_channel: false`;
- `gate_satisfied: false`;
- `supported_deprecation_release_channel_proven: false`; and
- `status: not-ready`.

## Installed evidence

Run from the repository:

```console
python examples/supported_release_channel_readiness.py
```

The release sample bundle includes an exact copy of the empty reviewed
manifest. The example also accepts an explicitly selected local manifest:

```console
python examples/supported_release_channel_readiness.py --channel tests/fixtures/supported_release_channel.json
```

It emits one deterministic
`ludoweave.evaluation.supported-release-channel-readiness/1` JSON document. The
report contains counts, versions, publication-channel identities, booleans,
reason codes, and the manifest digest. It omits release URLs, commits, artifact
and notes hashes, paths, environment facts, timings, credentials, and provider
messages.

## Ownership, failure, and security

The harness is explicitly invoked repository/release validation tooling, not a
publisher, updater, package resolver, or support service. It reads one bounded
local JSON document. Unknown fields, malformed or prerelease versions,
duplicate/out-of-order releases, mutable/non-HTTPS or IP-literal URLs, invalid
hashes/revisions, missing channels, unsupported/yanked records, record-count
overflow, unreviewed identity, or missing mandatory history fail closed.

Execution is synchronous on the calling thread. The harness retains no file
handle, world, provider, process, socket, credential, global registry, or user
profile. It performs no discovery, dynamic import, installation, subprocess,
network access, repository lookup, telemetry, tag creation, upload, or
publication.

## Stability boundary

RFC-0009 records admission machinery only. RFC-0003 gate 6 remains false;
actual cross-version supported-release execution and external consumer feedback
also remain absent. Command, transaction, receipt, and reader exports remain
experimental.

M26 adds no runtime module, public export, protocol field, operation, handler,
dependency, lock change, package version, workflow job, tag, GitHub release,
PyPI configuration, support promise, or publication.
