# RFC-0026: Verify published release asset retrieval

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M43

## Context

M40 verifies the authenticated draft release document's asset names, upload
state, byte sizes, and GitHub-reported SHA-256 digests against local staging.
M41 adds exact source release notes, and M42 carries the same numeric release
database ID across publication before rechecking final state and metadata. That
chain still trusts GitHub's asset metadata without reading the stored asset
bytes back through the release-asset endpoint.

GitHub's versioned REST API exposes each release asset by a numeric asset ID.
With `Accept: application/octet-stream`, the endpoint returns the binary
content directly or redirects the client to it. The existing tag job already
has the contents permission and authenticated GitHub CLI client required for
that read.

## Decision

Advance the internal release validator to
`ludoweave.release-draft-integrity/4` and require every remote asset to have a
unique positive integer ID bounded to 63 bits. After a complete published-state,
notes, and asset verification, an explicit `--asset-plan` may create one new
file containing:

- protocol `ludoweave.release-asset-retrieval-plan/1`;
- one canonical name-sorted line per asset;
- only the validated decimal asset ID, expected byte size, and safe asset
  basename.

The plan is available only for expected published state, is written only after
all verification succeeds, requires an existing parent directory, and opens
the target exclusively. It never clobbers an existing path. Normal structured
success output remains limited to state, tag, and safe name/size/digest
identities; it does not expose asset IDs, URLs, local paths, notes, publication
time, or immutable state.

The existing M42 published-state step writes the plan from the exact release
document fetched by the validated release database ID. A following step in the
same tag job:

1. validates the plan protocol, identity, expected byte size, and each bounded
   shell token again;
2. retrieves each numeric asset ID through `gh api` with
   `Accept: application/octet-stream` and REST version `2026-03-10`;
3. streams at most the expected byte size plus one byte into a new
   runner-temporary partial file, rejects short or long responses, enforces the
   512-MiB expected-total cap, and never clobbers a partial or final path;
4. reruns the same standard-library validator on the retrieved directory and
   the same published release document.

The second verification hashes every retrieved byte. Because local staging was
already matched to the same exact document, a passing result establishes that
the authenticated asset endpoint returned the same complete bounded byte set
at that observation point.

## Failure and ownership

The workflow owns all authenticated network reads and runner-temporary files.
The validator owns no token, network client, shell, process, release mutation,
or cleanup authority; its only new write is the explicit exclusive plan path.
A missing, malformed, duplicate, out-of-range, unavailable, short, oversized,
partial, extra, or byte-different asset fails the release job with no retry,
clobber, delete, unpublish, rollback, or other release mutation. Oversized
responses are cut off after the expected size plus one byte, before final
validation.

As in M42, failure occurs after publication. The prerelease may therefore
already be public and requires deliberate maintainer inspection.

## Non-claims

This decision does not:

- prove unauthenticated consumer access or availability;
- verify every CDN edge, cache, geography, future request, or later mutation;
- enable, require, or claim immutable releases;
- replace GitHub artifact/SBOM attestations or consumer-side verification;
- install the downloaded wheel, execute the downloaded sample bundle, or
  announce/support a release;
- add a job, runner, action, permission, trigger, dependency, credential, tag,
  release, upload, publication, rollback, or cleanup authority;
- change runtime code, package metadata, lock state, public API, or SemVer.

## Alternatives considered

- **Use `gh release download` by tag.** Rejected for this gate because M42
  deliberately preserves an exact release and asset database identity; a
  second tag-name lookup would weaken that chain.
- **Add a network client to the Python validator.** Rejected to preserve the
  verifier's deterministic local-input boundary and keep credentials/network
  authority visible in the workflow.
- **Require immutable-release verification.** Deferred because repository
  immutability policy is an independent operational decision and mutable
  prereleases remain valid under M42.
- **Use unauthenticated browser download URLs.** Deferred to a separate public
  availability decision; those URLs are not needed to establish exact-ID
  authenticated retrieval.

## Consequences

- The tag job performs one bounded asset read per staged member after
  publication; the current candidate has ten members.
- Retrieval enforces the existing 32-asset, 256-MiB individual, and 512-MiB
  expected-total limits before or during transfer; the complete validator then
  rechecks the materialized directory.
- A storage/retrieval mismatch becomes visible before the job reports success,
  while remediation remains a maintainer decision.
- Pull-request CI topology and quota usage remain unchanged.

## Acceptance evidence

- Exact plan generation, no-clobber, state, ID, confidentiality, and byte-drift
  behavior tests pass.
- Architecture tests protect same-document/exact-ID retrieval, quoted bounded
  shell consumption, non-mutation, workflow topology, permissions, and runtime
  isolation.
- The complete local and hosted M43 gates pass before integration.
