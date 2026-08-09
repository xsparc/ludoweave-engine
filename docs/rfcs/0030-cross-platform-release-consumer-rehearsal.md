# RFC-0030: Add a cross-platform public release consumer rehearsal

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M47

## Context

M46 moves final public-byte verification and installed release smoke onto a
fresh Ubuntu runner, but its shared verifier is a Bash program. The first M46
hosted run exposed a real Bash 3.2 portability defect on macOS even though the
tag-only rehearsal itself remains Linux-only. A successful future M46 release
run therefore would not establish that the exact published candidate installs
and passes its bundled scenarios on the other two supported operating systems.

The release candidate is already preserved as one exact named same-workflow
artifact. GitHub documents that artifacts can pass data between jobs in one
workflow and that a job matrix can run the same job definition across operating
systems. Python 3.12 is already provisioned on every supported hosted runner,
and the standard library exposes an HTTPS client with explicit TLS context,
blocking timeout, response status, headers, and bounded response reads.

## Decision

Replace the internal Bash public-release verifier with one typed Python 3.12
program, then expand the existing tag-only `fresh-consumer` job to the exact
matrix `ubuntu-latest`, `windows-latest`, and `macos-latest`.

The publishing job and every fresh matrix execution use that same program.
Publishing mode must reuse M43's existing plan. Each fresh operating-system
runner must reject a preexisting plan and create a new exclusive plan only
after the exact same-workflow candidate matches the public release document.

Each matrix execution:

1. depends on the successful publishing job;
2. has `contents: read`, a 25-minute timeout, no dependency cache, and no
   release, attestation, or identity-token write permission;
3. checks out the exact tag without persisted credentials and installs the
   pinned uv/CPython 3.12 tool pair;
4. downloads the exact named candidate using the already pinned
   `actions/download-artifact` v8.0.1 revision;
5. independently creates and validates its own plan, public document,
   partials, downloaded directory, and isolated installation; and
6. fails the workflow unless the exact published bytes pass complete release
   smoke on that operating system.

The matrix uses `fail-fast: false` so a failure on one operating system does
not cancel evidence collection already assigned to another. M47 adds two
tag-only runner allocations to M46's one fresh allocation. It does not change
the pull-request workflow; substantive pull requests retain exactly the
Linux-first three-allocation M37 topology.

## Portable HTTP boundary

The verifier uses `http.client.HTTPSConnection` directly, so ambient proxy
configuration and user HTTP client configuration cannot select a request host.
Initial requests are fixed to `api.github.com` and the exact repository/release
or asset ID. Remote redirects may change host but must remain HTTPS on the
default port and stop after three responses. User information, fragments,
HTTP, non-default ports, authorization headers, cookies, `GH_TOKEN`, and
`GITHUB_TOKEN` fail closed or are never supplied.

Connections use a verified default TLS context, a maximum 10-second blocking
socket timeout, and one 30-second monotonic request deadline. The release
document remains capped at 4 MiB. The plan is capped at 16 KiB, 32 unique safe
assets, positive 63-bit IDs, 256 MiB per asset, and 512 MiB total. Every target
is created exclusively; assets first use a unique ID-derived partial and move
only after exact length validation. The existing strict release-document
validator rechecks the admitted candidate before retrieval and the complete
downloaded set afterward.

Success emits only protocol, status, asset count, and total bytes. Failure
emits one stable code and generic message without paths, URLs, response bodies,
release notes, credentials, or environment values.

## Failure and ownership

The publishing job must succeed before any matrix execution starts. Each fresh
runner owns only its workspace, downloaded workflow artifact, temporary plan,
public document, partials, public directory, and isolated installation. A
failure leaves the published prerelease for explicit maintainer review.

There is no retry, release edit, unpublish, delete, replacement, rollback,
cleanup, tag creation, asset upload, or publication authority in a fresh job or
the portable verifier. No real tag or release is created while implementing or
validating M47. In particular, there is no release mutation on either success
or failure.

## Claims and non-claims

A successful authorized real tag run would establish that three fresh
GitHub-hosted operating-system runners retrieved the same admitted candidate,
independently fetched the exact public GitHub API bytes without a release
credential, revalidated them, installed the wheel, and passed the bundled
release scenarios on Ubuntu, Windows, and macOS.

This remains inside the same workflow, repository, account, and provider. It
is not independent verification by an external consumer,
organization, account, provider, repository, or build. It does not establish a
clean machine outside GitHub-hosted Actions, every browser/CDN/cache/geographic
path, future availability, immutability, artifact security, vulnerability
freedom, PyPI availability, or a supported release channel. It does not replace
the manual independent consumer check before announcement.

M47 changes only the tag workflow, internal release verifier, focused tests,
and documentation. It changes no runtime package, public API, version,
dependency, lock, release trigger, release artifact set, attestation,
publication command, pull-request CI allocation, or deferred subsystem.

## Alternatives rejected

- Keep Bash and add `shell: bash` to Windows/macOS. Rejected because it would
  keep shell-version behavior inside the boundary M47 is intended to test.
- Duplicate the verifier in PowerShell. Rejected because two security-sensitive
  implementations could drift while validating the same release identity.
- Run only Ubuntu and infer portability from the pure wheel. Rejected because
  wheel portability does not execute platform-specific installation and sample
  behavior.
- Add an external workflow, account, or provider. Rejected because no such
  independently owned verifier is available, and project-owned automation must
  not be represented as external evidence.
- Automatically unpublish after a failed consumer job. Rejected because this
  widens destructive postpublication authority and can hide evidence.

## Sources

- [GitHub: using jobs, prerequisites, and matrices](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs)
- [GitHub: store and share data with workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data)
- [Python 3.14 `http.client` documentation](https://docs.python.org/3/library/http.client.html)
- [Python 3.14 `ssl.create_default_context` documentation](https://docs.python.org/3/library/ssl.html#ssl.create_default_context)
