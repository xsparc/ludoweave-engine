# RFC-0029: Add a fresh-runner public consumer rehearsal

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M46

## Context

M45 retrieves the published release without a release credential and runs the
complete installed-candidate smoke, but it does so at the end of the publishing
job. That runner still owns the original build and release staging. A copied,
stale, or accidentally retained local file cannot pass M45's exact public
directory validation, but the observation is not a fresh-runner rehearsal.

The release job already uploads the admitted staged candidate as one bounded
workflow artifact. GitHub documents job outputs and the `needs` context for
passing scalar values to a dependent job, and recommends upload/download
artifacts for files shared between jobs in one workflow. The current verified
[`actions/download-artifact` v8.0.1](https://github.com/actions/download-artifact/releases/tag/v8.0.1)
revision supports exact-name current-run retrieval and fails on an artifact
digest mismatch by default.

## Decision

After the existing release job succeeds, one additional hosted Linux runner
per real tag run performs a fresh-runner public consumer rehearsal:

1. The release job exposes only the verified numeric release ID and validated
   package version as job outputs.
2. The dependent job has explicit `contents: read` permission, a 25-minute
   timeout, and no release, attestation, or identity-token write permission.
3. It checks out the exact tagged source without persisted credentials,
   installs the pinned uv and CPython 3.12 tools without a dependency cache,
   and retrieves the exact named candidate uploaded earlier in the same
   workflow through `actions/download-artifact` pinned to commit
   `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c`.
4. Both jobs invoke one repository-owned shell verifier. The publishing job
   explicitly reuses M43's already validated plan; the fresh runner requires
   the plan path to be absent and creates it exclusively from the admitted
   candidate plus public release document.
5. The fresh runner repeats M45's fixed-repository, positive 63-bit ID, HTTPS-
   only, three-redirect, connect/request timeout, 4-MiB document, safe-name,
   no-clobber, 32-asset, 256-MiB individual, and 512-MiB total bounds.
6. It revalidates the complete public directory and runs complete release
   smoke, including checksums, manifest, SPDX metadata, safe extraction,
   isolated wheel installation, and bundled acceptance scenarios.

The public release and asset HTTP requests receive no `GH_TOKEN`,
`GITHUB_TOKEN`, authorization header, cookie, browser URL, or caller-selected
host. Checkout and workflow-artifact actions still use GitHub's scoped workflow
services; the job is not described as credential-free overall.

## Failure and ownership

The publishing job must succeed before the fresh job is scheduled. The new job
owns its workspace, downloaded workflow artifact, public document, plan,
partial files, public asset directory, and isolated install. The shared script
rejects an absent expected directory, wrong repository, invalid release ID,
missing existing plan, preexisting fresh plan, unsafe plan row, unexpected
length, public-document drift, downloaded-set drift, or smoke failure.

This happens after publication. There is no release mutation, retry, edit,
unpublish, delete, replacement, rollback, or cleanup authority. A failed fresh
job makes the workflow fail and leaves any public release for maintainer review.

## Claims and non-claims

A successful real tag run would establish that a second, fresh GitHub-hosted
Linux runner retrieved the same workflow's admitted candidate, independently
retrieved the exact public API bytes without a release credential, revalidated
them, installed the wheel in a new isolated environment, and passed the bundled
scenarios.

This is a same workflow rehearsal. It is not independent verification by an
external consumer, organization, account, provider, repository, or build. It
does not establish a cross-platform public installation matrix, a clean machine
outside GitHub-hosted Actions, every browser/CDN/cache/geographic path, future
availability, immutability, artifact security, vulnerability freedom, PyPI
availability, or a supported release channel. It does not replace the manual
independent consumer check before announcement.

M46 adds one tag-only job, one pinned download action, duplicated pinned
checkout/setup use, two scalar job outputs, one internal shell script, focused
tests, and documentation. It changes no pull-request CI allocation, release
trigger, release permission, build, staged artifact set, attestation, tag,
release, upload, publication command, dependency, lock, version, runtime,
package, or public API. No real fresh-runner pass is claimed until an explicitly
authorized signed-tag release run executes.

## Sources

- [Passing information between jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs)
- [Store and share data with workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data)
- [`actions/download-artifact` v8.0.1](https://github.com/actions/download-artifact/releases/tag/v8.0.1)
