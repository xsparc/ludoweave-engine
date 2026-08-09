# RFC-0031: Constrain public release HTTP responses and failures

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M48

## Context

M47 establishes one portable standard-library client for the same-workflow
public release consumer on Ubuntu, Windows, and macOS. Its byte, path, identity,
TLS, redirect-count, and installed-smoke bounds are explicit, but its response
policy is broader than the GitHub endpoints it calls. It accepts five redirect
status codes for both release documents and assets even though GitHub documents
a direct `200` response for **Get a release** and either `200` or `302` for
**Get a release asset**.

The first portable implementation also classifies a `TimeoutError` raised while
sending a request or reading response headers as a generic transport failure.
An `OSError` raised while reading a response body crosses the same broad file-I/O
handler as a local write failure. Those paths still fail closed, but their
stable codes do not accurately identify the failing boundary.

Python documents that socket timeouts apply to blocking socket operations and
raise `TimeoutError`, which is also an `OSError`. Exception order and explicit
socket timeout refreshes therefore matter to the observable failure contract.

## Decision

Constrain the existing M47 client without changing its workflow call sites or
authority:

1. the fixed public release-document endpoint accepts only a direct `200`;
2. the fixed release-asset endpoint accepts a direct `200` or follows at most
   three `302` responses to bounded HTTPS port-443 locations;
3. every other `3xx` response fails with `public_release.redirect_failed`;
4. every other non-`200` response fails with
   `public_release.request_failed`;
5. `X-GitHub-Api-Version` is sent only when the current request host is the
   fixed `api.github.com`; redirected hosts receive only the media type,
   identity encoding, connection-close request, and fixed user agent; and
6. no request supplies authorization, cookies, ambient proxy configuration,
   browser URLs, or caller-selected initial hosts.

The initial connection keeps the 10-second blocking timeout inside the existing
30-second monotonic per-request deadline. After request transmission and before
response headers, and again before every bounded body read, the connected
socket timeout is reduced to the smaller of ten seconds and the remaining
deadline.

Every `TimeoutError` from request transmission, timeout refresh, response-header
read, or response-body read maps to `public_release.request_timeout`. Other
socket or HTTP protocol failures map to `public_release.request_failed`. Only
exclusive target creation, local writes, hard-link finalization, or owned-file
removal map to `public_release.output_failed`. Stable output remains one generic
content-silent JSON failure; exception chaining retains internal cause context.

All M47 limits remain unchanged: fixed repository and numeric IDs, verified
default TLS, no non-HTTPS/default-port redirect, 4-MiB document, 16-KiB plan, 32
assets, 256 MiB per asset, 512 MiB total, safe unique names, exclusive
ID-derived partials, exact candidate/document/download validation, and complete
installed release smoke.

## Failure and ownership

The verifier owns only the workflow runner's document, plan, download
directory, partials, and isolated smoke environment. M48 introduces no retry or
cleanup loop. A failed real tag run leaves the already published prerelease for
explicit maintainer review, exactly as M47 does.

The existing release and fresh-consumer jobs remain unchanged. M48 adds no
runner, action, permission, trigger, credential, dependency, package, runtime
API, upload, publication, edit, unpublish, delete, rollback, or other release
mutation. In short, M48 grants no release mutation.

## Claims and non-claims

Fixture-driven tests establish deterministic response-policy and error-taxonomy
behavior. Pull-request CI establishes that the shared verifier and its
architecture contract pass on the supported development platforms. Neither is
a real public release observation.

An authorized signed-tag run would still produce same workflow, repository,
account, and provider evidence. M48 does not establish independent or external
verification, a clean machine outside GitHub-hosted Actions, every CDN or
geographic path, future availability, immutability, artifact security,
vulnerability freedom, PyPI availability, or a supported release channel. No
real M48 tag/release execution is performed or claimed.

## Alternatives rejected

- Continue accepting every common redirect status. Rejected because it exceeds
  the documented response set of the two fixed GitHub endpoints.
- Require an allowlist of redirected CDN hostnames. Rejected because the public
  asset endpoint documents a redirect location but does not publish a stable
  hostname allowlist; HTTPS/default-port and exact post-download digest checks
  remain the durable boundary.
- Treat every `OSError` as a network failure. Rejected because `TimeoutError` is
  an `OSError` and local filesystem failures need a distinct actionable code.
- Add retries or automatic release cleanup. Rejected because either changes
  observation semantics or widens postpublication/destructive authority.
- Add another workflow or runner. Rejected because the conformance gap is in
  the shared client and can be tested inside the unchanged three-allocation
  pull-request topology.

## Sources

- [GitHub: Get a release](https://docs.github.com/en/rest/releases/releases#get-a-release)
- [GitHub: Get a release asset](https://docs.github.com/en/rest/releases/assets#get-a-release-asset)
- [Python 3.14 `http.client`](https://docs.python.org/3/library/http.client.html)
- [Python 3.14 socket timeouts](https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts)
