# RFC-0023: Verify draft release assets before publication

- **Status:** Accepted
- **Date:** 2026-08-09

## Context

The tag-only release workflow validates the signed annotated release ref under
RFC-0022, builds and smoke-tests a deterministic candidate, generates local
checksums, and attests the staged files. Its final `gh release create` command
supplies every staged asset in one invocation.

The [GitHub CLI manual](https://cli.github.com/manual/gh_release_create)
documents that an asset-bearing create command internally creates a draft,
uploads the files through separate API calls, and then publishes the release.
That safe ordering is not visible to this repository's workflow, so the job
cannot compare the stored draft asset set with local staging before the final
publication transition.

GitHub's
[release API](https://docs.github.com/en/rest/releases/releases)
reports an uploaded asset's name, state, byte size, and `sha256:` digest. GitHub
also recommends the explicit draft, attach, publish sequence for
[immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).
Release immutability is a separate repository setting and is not required or
changed by this decision.

## Decision

M40 makes the existing final sequence explicit inside the same tag job:

1. create the exact verified-tag release as a prerelease draft without assets;
2. upload every staged file without `--clobber`;
3. fetch the draft release document using GitHub REST API version
   `2026-03-10`;
4. run `scripts/verify_release_draft.py` against local staging and that
   runner-temporary document; and
5. publish the verified draft as the non-latest prerelease.

The standard-library validator requires:

- a bounded slash-free `vVERSION` tag and bounded release title;
- an exact matching `tag_name` and title;
- `draft=true`, `prerelease=true`, and `immutable=false` while verification is
  in progress;
- one non-empty set of at most 32 local regular, non-symlink files with bounded
  safe basenames;
- at most 256 MiB per file and 512 MiB total local content;
- one duplicate-free remote asset per local file;
- `state=uploaded`; and
- exact name, byte-size, and SHA-256 equality for every remote/local asset.

The GitHub document is capped at 4 MiB, decoded as strict UTF-8 JSON, and
rejects duplicate keys. Success emits deterministic
`ludoweave.release-draft-integrity/1` JSON containing only the tag and sorted
safe asset identities. Invalid directories, entries, identities, state,
documents, asset sets, sizes, or digests fail nonzero with a stable code and no
traceback.

No network client, token handling, shell, dynamic import, or arbitrary
evaluation exists in the validator. The workflow owns both read-only API access
and the already-authorized publication commands. A verification or upload
failure deliberately leaves the release as an unpublished draft for maintainer
inspection; the workflow does not destructively delete evidence or clobber a
prior asset.

M40 adds no workflow job, runner matrix entry, action, permission, trigger,
credential, dependency, cache key, tag, release, or publication authority. It
does not change the pull-request CI workflow and consumes no additional runner
allocation.

## Trust and guarantee boundary

The remote digest is GitHub's authenticated API report for the uploaded draft
asset. Comparing it with independently computed local bytes detects missing,
extra, incomplete, truncated, renamed, or digest-different remote assets before
publication. Existing build-provenance and SPDX attestations remain the
cryptographic provenance mechanisms; local checksums and the draft comparison
do not replace them.

The gate does not prove GitHub storage correctness independently of GitHub, add
an external transparency log, download the remote bytes, make the published
release immutable, authorize the tag signer, or protect against an actor who can
replace the workflow. Release immutability, tag/environment rules, signer/key
policy, workflow governance, PyPI trusted publishing, and a supported release
channel remain separate operational or architectural decisions.

No actual tag, draft, release, asset upload, or publication is created during
M40 validation. Unit and architecture tests use local files and synthetic API
documents. No runtime module, public Python API, persistent world format,
command/receipt protocol, dependency, lock entry, package version, supported
Python/platform contract, native code, or deferred subsystem changes.

## Alternatives rejected

- **Keep the single asset-bearing `gh release create` command.** Rejected
  because its internal draft is published without a repository-owned remote
  asset identity check.
- **Trust `SHA256SUMS` alone.** Rejected because it describes local staging and
  cannot prove which assets GitHub reports as uploaded.
- **Download every draft asset before publication.** Rejected because the API
  exposes exact SHA-256 digests and sizes, avoiding duplicate transfer and
  runner time while preserving the required comparison.
- **Use `gh release upload --clobber`.** Rejected because a retry could delete a
  prior asset before the replacement upload succeeds.
- **Delete the draft automatically on any failure.** Rejected because deletion
  is destructive, hides failure evidence, and makes recovery policy implicit.
- **Enable immutable releases as part of M40.** Rejected because that repository
  setting changes tag/release operations and requires explicit maintainer
  authorization; this slice only prepares and validates the draft boundary.
- **Create a real test release.** Rejected because publication remains an
  explicit maintainer operation outside the implementation milestone.

## Consequences

- Publication cannot occur until GitHub reports the exact complete staged asset
  set and SHA-256 identities.
- Failed uploads or verification remain private drafts that require deliberate
  maintainer inspection and cleanup before retry.
- The workflow makes one bounded read-only release API request and two explicit
  CLI publication-state transitions inside the existing release job.
- Enabling immutable releases later fits the same draft/upload/verify/publish
  ordering without changing this validator contract.
