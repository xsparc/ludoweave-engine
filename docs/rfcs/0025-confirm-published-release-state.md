# RFC-0025: Confirm published release state

- **Status:** Accepted
- **Date:** 2026-08-09

## Context

M40 and M41 keep a GitHub prerelease private until its authenticated tag,
title, mutable draft state, notes body, and complete uploaded asset identities
match local staging. The final `gh release edit --draft=false` command then
publishes that verified draft, but the workflow does not read the resulting
public release record. A failed or unexpected transition could therefore leave
the job without repository-owned evidence of the final state.

The [GitHub CLI manual](https://cli.github.com/manual/gh_release_edit)
documents `--draft=false` as publishing an existing draft. GitHub's
[versioned release API](https://docs.github.com/en/rest/releases/releases?apiVersion=2026-03-10)
exposes `draft`, `prerelease`, `published_at`, `immutable`, `body`, and asset
identities. The draft verifier already consumes the same bounded local staging
and authenticated release schema, so it can confirm the transition without a
new dependency or trust boundary.

## Decision

M42 advances the internal validator protocol from
`ludoweave.release-draft-integrity/2` to `/3` and requires an explicit expected
state on every invocation.

The draft invocation requires:

- `draft=true`, `prerelease=true`, and `immutable=false`;
- an explicit null `published_at`; and
- the existing exact tag, title, notes, and asset checks.

The published invocation requires:

- `draft=false` and `prerelease=true`;
- `immutable` to be a JSON boolean, accepting either truthful value because
  repository immutability policy is a separate control;
- a syntactically and calendrically valid UTC `published_at`; and
- the same exact tag, title, notes, and asset checks.

Success includes only the safe expected state, tag, and sorted asset
identities. It never emits the publication timestamp, immutable setting, or
release-note content.

The existing prepublication step validates the numeric release database ID,
verifies the draft with `--expected-state draft`, and exposes only that numeric
ID as a step output. After `gh release edit --draft=false`, one new read-only
API request fetches that exact release ID and the validator runs with
`--expected-state published`. M42 adds one step inside the existing tag job but
no job, runner, action, permission, trigger, credential, dependency, cache key,
tag, release, upload, or publication authority.

## Trust and guarantee boundary

The postpublication check proves only what GitHub's authenticated API reports
at that observation point. A mismatch fails the workflow and blocks a
successful release-job result and maintainer announcement, but the release is
already public. The workflow deliberately does not unpublish, delete, mutate,
or roll back release evidence automatically.

The check does not make a mutable release immutable or prevent a later actor
from editing it. GitHub documents that immutable-release protections apply
only after publication; enabling that repository setting remains a separate
maintainer decision. The published validator accepts either boolean
`immutable` value and makes no policy claim from it.

M42 does not independently download public assets, verify GitHub storage,
replace attestations, validate rendered Markdown or links, prove factual
release-note completeness, configure a deployment environment or tag rule,
authorize a signer, publish to PyPI, or establish a supported release channel.
No actual tag, draft, release, upload, publication, rollback, or repository-
setting change occurs during M42 validation.

No runtime module, public Python API, persistent world format,
command/receipt protocol, dependency, lock entry, package version, supported
platform, native code, or deferred subsystem changes.

## Alternatives rejected

- **Trust the CLI exit code alone.** Rejected because it does not preserve a
  repository-owned exact final-state assertion over the authenticated record.
- **Resolve the published release by tag.** Rejected because the workflow
  already has the exact database ID; retaining it avoids identity ambiguity.
- **Require `immutable=true`.** Rejected because M42 does not change or assume
  repository immutability policy.
- **Automatically unpublish or delete on mismatch.** Rejected because that is
  destructive, can hide evidence, and expands release authority.
- **Add another runner or job.** Rejected because the existing tag job owns all
  required bounded inputs and credentials.

## Consequences

- A successful tag workflow now has exact prepublication and postpublication
  observations for the same release database identity.
- Invalid or missing publication timestamps and unexpected draft/prerelease
  states fail with the existing stable structured state code.
- Mutable and immutable published prereleases can both be truthfully observed
  without changing policy.
- The existing three-allocation substantive PR gate and one-allocation
  documentation gate remain unchanged.
