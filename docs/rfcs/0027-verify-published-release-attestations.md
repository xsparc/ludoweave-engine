# RFC-0027: Verify published release attestations

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M44

## Context

The tag workflow already creates one multi-subject SLSA v1 provenance
attestation for the staged release set and one SPDX 2.3 SBOM attestation for
the pure wheel. M40-M43 validate the release record, source notes, published
state, exact asset identities, and bytes returned by the authenticated asset
endpoint. The job did not verify that the published bytes were subjects of the
attestations created by the same exact release workflow execution.

GitHub CLI can verify a local artifact against GitHub artifact attestations
while constraining repository, predicate type, signer workflow, signer commit,
source ref, source commit, certificate issuer, runner class, and the number of
candidate bundles inspected. The M43 retrieval plan and materialized download
directory already provide a bounded exact local subject set.

## Decision

After M43 revalidates every downloaded asset against the same published
release document, the existing tag job invokes a standard-library verifier.
It consumes only the canonical
`ludoweave.release-asset-retrieval-plan/1` file, its exact downloaded
directory, the event tag, and the checked-out commit. It requires:

- SLSA v1 provenance for every retrieved release asset;
- an SPDX 2.3 SBOM attestation for exactly one
  `ludoweave-*-py3-none-any.whl` subject;
- repository `xsparc/ludoweave-engine`;
- signer workflow `xsparc/ludoweave-engine/.github/workflows/release.yml`;
- signer and source digest equal to the exact lowercase 40-character
  `GITHUB_SHA`;
- source ref equal to `refs/tags/GITHUB_REF_NAME`;
- GitHub Actions' OIDC issuer and no self-hosted-runner attestations;
- at most 30 candidate attestation bundles per `gh attestation verify` call.

The plan remains capped at 16 KiB, 32 assets, 256 MiB per asset, and 512 MiB
in total. Exact plan/directory equality and non-symlink regular-file sizes are
revalidated before any child process runs. The verifier therefore makes at
most 33 sequential calls: one provenance check per admitted asset and one
wheel SBOM check. Each call has a 30-second timeout and null stdin, stdout, and
stderr. Success emits only protocol, status, and aggregate check counts;
failure emits only a stable code and generic message.

## Failure and ownership

The existing release job owns the GitHub token, `gh` client, attestation
service access, M43 plan, and temporary downloads. The Python verifier owns
validation and bounded subprocess invocation. It cannot create, upload,
publish, edit, delete, unpublish, or roll back a tag, release, asset, or
attestation.

Any missing, malformed, ambiguous, unavailable, mismatched, timed-out, or
nonzero verification fails the job. This gate runs after publication, so the
prerelease may already be public. Failure triggers no retry, cleanup,
unpublication, deletion, or rollback; maintainers inspect and decide recovery.

## Non-claims

This decision does not:

- establish artifact security, safety, freedom from vulnerabilities, or
  fitness for use;
- prove an independent build, a trusted build environment, or reproducibility;
- establish predicate truth beyond the verified predicate type, subject
  digest, and constrained GitHub identity fields;
- guarantee future attestation availability, non-revocation, or later policy
  acceptance;
- prove unauthenticated or global asset availability, every cache/CDN path,
  immutable release state, consumer installation, sample execution, or a
  supported release channel;
- add a job, runner, action, permission, trigger, dependency, credential, tag,
  release, upload, publication, retry, rollback, or cleanup authority;
- change runtime code, package metadata, lock state, public API, or SemVer.

## Alternatives considered

- **Trust successful attestation creation steps.** Rejected because creation
  success alone does not prove that the exact published/downloaded subjects are
  discoverable and verifiable under the intended identity policy.
- **Verify only the wheel.** Rejected because the existing provenance action
  covers every staged release asset and M43 supplies the complete bounded set.
- **Parse downloaded attestation bundles in repository code.** Rejected in
  favor of GitHub CLI's supported verifier and policy flags. Repository code
  suppresses child output and records only bounded outcomes.
- **Move verification before publication.** Rejected because the decision is
  specifically about attestations for the exact assets returned after the
  M42/M43 publication boundary.

## Consequences

- The tag job adds no allocation but performs one GitHub attestation query per
  asset plus one wheel SBOM query after publication.
- Current release staging has ten assets, so a real release would execute
  eleven bounded verifier calls.
- A valid pass can be claimed only after a real signed-tag release run creates
  and verifies the hosted attestations; local and pull-request tests validate
  the policy and failure behavior without claiming a hosted attestation pass.

## Acceptance evidence

- Unit tests cover exact policy arguments, complete subject coverage, canonical
  plan/directory bounds, wheel cardinality, timeouts, unavailable/failed CLI
  behavior, and content-silent structured failures.
- Architecture tests protect workflow order, identity policy, process bounds,
  unchanged action/job/permission topology, dependency isolation, and public
  non-claims.
- The complete local and hosted M44 gates pass before integration.
