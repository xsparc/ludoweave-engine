# RFC-0024: Verify draft release notes before publication

- **Status:** Accepted
- **Date:** 2026-08-09

## Context

M40 verifies the authenticated draft's exact tag, title, mutable prerelease
state, and complete uploaded asset identities before publication. The workflow
also passes staged `RELEASE_NOTES.md` to `gh release create --notes-file`, but
the validator does not compare that file with the draft release's public notes
body. A missing, truncated, substituted, or newline-different body could
therefore pass the M40 asset gate even though the separately uploaded
`RELEASE_NOTES.md` asset remains correct.

The [GitHub CLI manual](https://cli.github.com/manual/gh_release_create)
documents that `--notes-file` reads release notes from a file. GitHub's
[versioned release API](https://docs.github.com/en/rest/releases/releases?apiVersion=2026-03-10)
exposes those notes as the release `body`. The existing authenticated draft
document already contains that field, so comparing it requires no additional
API call or workflow permission.

## Decision

M41 advances the internal validator protocol from
`ludoweave.release-draft-integrity/1` to `/2`. Before accepting assets, the
validator reads the fixed staged member `RELEASE_NOTES.md` and requires the
authenticated draft's `body` to equal that exact UTF-8 text.

Local notes must be:

- the regular, non-symlink `RELEASE_NOTES.md` member already covered by staged
  asset identity verification;
- non-empty strict UTF-8 without a NUL character; and
- no more than 256 KiB.

Missing, null, non-text, truncated, substituted, newline-different,
whitespace-different, or Unicode-different remote bodies fail with the stable
code `release_draft.notes_mismatch`. Missing, empty, invalid-UTF-8, NUL-bearing,
oversized, non-file, or symlinked local notes fail closed before publication.
Neither success nor failure output includes release-note content.

The existing workflow ordering remains unchanged: create the private draft
using `--notes-file release/RELEASE_NOTES.md`, upload assets without clobbering,
fetch the authenticated draft, run the validator, and publish only after it
passes. M41 changes no workflow file, job, runner matrix entry, action,
permission, trigger, credential, dependency, cache key, tag, release, or
publication authority. It requires no additional runner allocation.

## Trust and guarantee boundary

The comparison proves that GitHub's authenticated API reports the same source
notes text that local staging supplied. Together with M40, it binds the private
draft's tag, title, state, notes body, and asset identities before publication.
The notes file remains covered separately by the asset name, size, and SHA-256
comparison.

The gate does not independently verify GitHub storage or rendered Markdown,
evaluate links, prove the notes factually complete, sanitize maintainer-authored
content, make a published release immutable, download the remote body, or
protect against an actor who can replace the workflow. Human review remains
responsible for content accuracy and release approval. Immutable-release
policy, tag/environment rules, workflow governance, PyPI trusted publishing,
and a supported release channel remain separate decisions.

No actual tag, draft, release, upload, or publication is created during M41
validation. No runtime module, public Python API, world format, command/receipt
protocol, dependency, lock entry, package version, supported platform, native
code, or deferred subsystem changes.

## Alternatives rejected

- **Trust the uploaded `RELEASE_NOTES.md` asset alone.** Rejected because the
  uploaded asset and the release page body are distinct GitHub fields.
- **Accept whitespace or newline normalization.** Rejected because silent
  normalization could hide truncation or substitution; the workflow uses a
  deterministic LF-normalized source file.
- **Hash only the remote body.** Rejected because direct exact comparison is
  simpler, bounded, and does not emit either content or a new content-derived
  identifier.
- **Fetch rendered HTML.** Rejected because rendering is not the publication
  source contract and would add network calls and presentation instability.
- **Add another workflow step or runner.** Rejected because the existing M40
  validator already receives both bounded inputs at the correct boundary.

## Consequences

- Publication cannot occur if the draft body differs from staged release notes
  by even one character.
- The validator protocol truthfully advances to `/2` because its acceptance
  contract is stronger.
- Release-note text remains absent from structured validator output and logs.
- The existing three-allocation substantive PR gate and one-allocation
  documentation gate remain unchanged.
