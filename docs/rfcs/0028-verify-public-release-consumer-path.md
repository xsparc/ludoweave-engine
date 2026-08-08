# RFC-0028: Verify the public release consumer path

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M45

## Context

M40-M44 verify the private draft, published metadata, authenticated asset
bytes, and hosted SLSA/SPDX attestations. Those checks still use the release
job's GitHub credential for release or attestation access. The final maintainer
checklist separately asks for public downloads and an installed-candidate
smoke, but the tag job did not exercise that consumer-facing path.

GitHub documents that [public release records](https://docs.github.com/en/rest/releases/releases?apiVersion=2026-03-10#get-a-release)
and [public release assets](https://docs.github.com/en/rest/releases/assets?apiVersion=2026-03-10#get-a-release-asset)
may be fetched without authentication. The numeric release and asset IDs
already admitted by M42/M43 let the workflow use fixed GitHub API endpoints
rather than trusting a remote download URL. The existing release smoke already
validates checksums, the manifest, SPDX metadata, safe sample extraction,
isolated wheel installation, and the bundled acceptance scenarios.

## Decision

After M44 verifies attestations, the existing tag job performs one bounded
public consumer-path observation without a GitHub credential:

1. Revalidate the exact positive decimal release ID retained from the private
   draft.
2. Use `curl` with user configuration disabled, HTTPS-only initial and redirect
   protocols, at most three redirects, a 10-second connect timeout, a 30-second
   request timeout, and no authorization or cookie header.
3. Fetch the exact public release ID from the fixed
   `api.github.com/repos/xsparc/ludoweave-engine/releases/ID` endpoint, cap the
   response at 4 MiB plus one byte, and validate it against the staged release,
   exact tag/title, and published-state contract.
4. Reparse the canonical M43 plan and retain its positive 63-bit IDs, safe
   basenames, 32-asset count, 256-MiB individual, and 512-MiB total bounds.
5. Fetch each exact public asset ID through the fixed binary endpoint into a
   new runner-temporary partial file, cap it at the expected byte count plus
   one, reject short or long content, and rename only after exact length.
6. Revalidate the complete downloaded directory against the public document,
   then run the existing complete release smoke against those bytes.

The step receives only the release ID and public title. It does not receive
`GH_TOKEN`, `GITHUB_TOKEN`, an `Authorization` header, a cookie, a browser
download URL, or a caller-supplied host or path. At the current ten-asset
candidate size it makes eleven public requests; the inherited plan caps it at
33 sequential requests. The existing 30-minute job timeout remains the outer
bound.

## Failure and ownership

The tag workflow owns `curl`, public network access, runner-temporary files,
and the existing validation/smoke commands. Repository validators remain
network-free. Every HTTP, redirect, timeout, document, identity, plan, length,
set, checksum, archive, installation, or sample failure fails the job.

This step runs after publication. It never retries, edits, deletes,
unpublishes, replaces, cleans up, or rolls back a release or asset. Temporary
partial content remains job-owned and disappears with the runner.

## Claims and non-claims

A successful real tag run establishes one observation that the exact public
GitHub API release ID and every exact public asset ID were available without a
GitHub credential, matched the already validated release, and passed the
project's isolated installed-candidate smoke on that same hosted Linux runner.

This decision does not establish:

- independent verification, an external consumer, a clean machine, or a
  cross-platform public installation matrix;
- every browser, CDN, cache, geographic, proxy, mirror, or source-archive path;
- future availability, non-revocation, immutability, or protection from later
  release/tag/asset changes;
- artifact security, vulnerability freedom, independent/trusted builds, or
  predicate truth beyond M44's identity checks;
- PyPI availability, a supported release channel, stability promotion, or a
  support commitment.

M45 adds no job, runner, action, permission, trigger, dependency, credential,
runtime import, public API, package version, tag, release, upload, publication,
retry, rollback, cleanup, or repository-setting authority. No real public-path
pass is claimed until an authorized signed-tag release run executes.

## Alternatives considered

- **Continue with a manual public download only.** Rejected because the tag job
  can exercise the same bounded release candidate without another allocation.
- **Reuse authenticated M43 downloads.** Rejected because those bytes do not
  test the public access boundary.
- **Trust `browser_download_url`.** Rejected in favor of fixed-host numeric-ID
  endpoints already bound by the canonical plan.
- **Add a separate workflow or external monitor.** Deferred because it would
  add scheduling, runner, authority, and maintenance scope while still not
  prove global or future availability.
- **Require immutable releases now.** Deferred because repository immutability
  is a separate administrative policy and is not enabled or changed by M45.

## Acceptance evidence

- Architecture tests protect ordering after M44, the exact public endpoints,
  credential absence, HTTPS/redirect/time bounds, plan and byte bounds,
  revalidation, complete smoke, and unchanged topology/dependencies.
- Existing validator and release-smoke suites cover strict documents, exact
  asset identity/content, checksums, manifests, archives, isolated wheel
  installation, and bundled scenarios.
- The complete local and hosted M45 gates pass before integration. A real
  public-path result remains intentionally unclaimed.
