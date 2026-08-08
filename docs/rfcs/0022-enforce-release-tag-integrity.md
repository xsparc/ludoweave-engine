# RFC-0022: Enforce release tag integrity

- **Status:** Accepted
- **Date:** 2026-08-09

## Context

The tag-only release workflow already checks that `GITHUB_REF_NAME` equals the
package version and passes `--verify-tag` to `gh release create`. The
[GitHub CLI manual](https://cli.github.com/manual/gh_release_create) defines
that option narrowly: it aborts if the tag does not already exist in the
remote repository. It does not claim that the tag is annotated, signed,
verified, aimed at the checked-out commit, or reachable from the protected
development line.

[Git documentation](https://git-scm.com/docs/git-tag) distinguishes annotated
tag objects intended for releases from lightweight object labels. Git can
verify signatures locally when the necessary trust material exists, but the
ephemeral release runner does not own a project signing-key allowlist or key
distribution mechanism. The
[GitHub Git tags API](https://docs.github.com/en/rest/git/tags) supports
annotated tag objects and returns GitHub's signature-verification result,
including whether the signature is verified and why.

The existing checkout fetches one object by default. The
[checkout action documentation](https://github.com/actions/checkout/blob/main/README.md)
requires `fetch-depth: 0` to obtain all branch history and tags. Full history is
needed to prove that the release commit is reachable from `origin/main`.

## Decision

M39 adds `scripts/verify_release_ref.py`, a standard-library, explicitly invoked
release validator. The release workflow saves the exact GitHub tag-ref and
annotated-tag API responses into runner-temporary files, then supplies those
documents with the event tag and commit to the validator. The workflow
materializes the validator from fetched `origin/main`, rather than executing
the not-yet-admitted tag checkout's copy.

The validator requires all of the following:

1. the event tag is a bounded slash-free `vVERSION` identity;
2. the GitHub ref is the exact `refs/tags/vVERSION` ref and targets an
   annotated tag object;
3. the returned tag object has the same object SHA and exact tag name;
4. the tag targets the exact event/checkout commit;
5. GitHub reports `verified=true`, `reason=valid`, and non-empty signature,
   payload, and verification-time fields;
6. local Git resolves the exact annotated tag object and commit to the same
   identities;
7. `HEAD` equals the event commit; and
8. that commit is an ancestor of fetched `origin/main`.

Success emits one deterministic `ludoweave.release-ref-integrity/1` JSON
document containing only the safe tag, tag-object SHA, commit SHA, and main-ref
identity. It never emits the signature or signed payload. Invalid paths,
oversized or duplicate-key JSON, malformed identities, lightweight or
mismatched tags, unverified signatures, detached checkouts, missing Git state,
and non-main commits fail nonzero with a stable code and no traceback.

The workflow performs this check immediately after version validation and
before dependency synchronization, system-package installation, tests, build,
staging, attestation, or publication. It changes the existing checkout to full
history and makes two read-only GitHub API requests within the already
authorized tag job. M39 adds no workflow job, runner matrix entry, action,
permission, trigger, credential, dependency, cache key, tag, or publication
authority. It consumes no additional runner allocation.

## Trust and guarantee boundary

GitHub's tag-object response is the hosted signature-verification authority.
Local Git separately checks object identity, checkout identity, and ancestry;
it does not cryptographically re-verify the tag because the runner has no
project signing-key trust store. M39 therefore does not create or manage a key
allowlist, pin a signer, distribute trust roots, prove signer authorization, or
replace maintainer review.

The gate prevents the existing workflow from publishing a lightweight,
unsigned/unverified, retargeted, detached, or non-main tag. It does not create
a tag or release, enable immutable releases, publish to PyPI, configure trusted
publishing, alter attestations, prove artifact reproducibility beyond M38, or
establish a supported release channel. GitHub's artifact/SBOM attestations
remain the release-build provenance mechanism after this ref gate passes.

This is a guard inside the accepted workflow, not protection from an actor who
is authorized to replace that workflow at the tagged commit or change
repository tag/environment rules. Tag protection, deployment-environment
approval, and workflow-file governance remain operational controls outside
M39. Loading the verifier from `origin/main` removes trust in the tag's script
copy but cannot make a mutable workflow self-authenticating.

No runtime module, public Python API, persistent format, command/receipt
protocol, dependency, lock entry, package version, supported Python/platform
contract, native code, or deferred subsystem changes.

## Alternatives rejected

- **Keep only `gh release create --verify-tag`.** Rejected because that option
  checks remote existence, not annotated type, signature, target, or ancestry.
- **Run only `git verify-tag` in the hosted runner.** Rejected because local
  cryptographic verification requires an accepted trust-root/key-distribution
  policy that this project does not have.
- **Accept a lightweight tag that points at a signed commit.** Rejected because
  the release identity itself would remain mutable metadata without a signed
  annotated tag object.
- **Require a particular signing key now.** Rejected because no key allowlist,
  rotation, revocation, recovery, or maintenance-owner policy has been accepted.
- **Add a separate pre-release workflow or runner.** Rejected because the same
  fail-fast check fits before expensive work in the existing tag job.
- **Create or exercise a real release during M39.** Rejected because tag and
  publication actions remain explicit maintainer operations outside this
  implementation milestone.

## Consequences

- A malformed or untrusted tag fails before the expensive release gate spends
  time building artifacts or gains any publication effect.
- The release checkout fetches full repository history and tags instead of one
  object, a bounded cost accepted for the tag-only job.
- Consumers can distinguish tag identity/signature admission from later build
  provenance and same-source reproducibility evidence.
- A future signer-authorization or immutable-release policy requires a separate
  accepted decision and operational ownership.
