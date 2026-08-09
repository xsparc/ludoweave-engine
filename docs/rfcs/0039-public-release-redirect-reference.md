# RFC-0039: Constrain public release status and redirect references

- **Status:** Accepted
- **Date:** 2026-08-10
- **Owners:** LudoWeave maintainers
- **Milestone:** M56

## Context

M48 accepts direct `200` responses for public release documents and permits at
most three `302` responses while retrieving an asset. M49-M55 validate the
connected peer, TLS session, and HTTP framing before status or redirect use.
The verifier still relied on the runtime shape of `HTTPResponse.status` and on
`getheader("Location")` plus `urljoin()` recovery without independently
validating the redirect reference.

Python documents `HTTPResponse.status` as the server's status code and
`getheaders()` as a list of response-header pairs. Python also warns that its
URL parsers do not validate inputs and that `urljoin()` can change authority
when given an absolute second argument. RFC 9110 defines a status code as an
integer from 100 through 599, defines `Location` as a single URI-reference,
describes recovery from invalid or multiple Location fields as difficult and
non-interoperable, and recommends support for URI references of at least 8,000
octets.

## Decision

After M55 framing validation and before status comparison, redirect resolution,
or body use, every response must expose `status` as an integer, but not a
boolean, from 100 through 599.

For an accepted `302` response, the documented `getheaders()` collection must
be a list of two-string tuples and contain exactly one case-insensitive
`Location` field. Its value must be a single URI-reference from 1 through 8,000
ASCII octets using RFC 3986 URI-reference characters and complete `%HH`
escapes. Raw whitespace, controls, backslashes, non-ASCII characters,
incomplete percent escapes, missing values, duplicate field lines, malformed
header collections, and oversized references fail before another request.

The validated reference is resolved against the current URL. The result must
again pass the existing bounded HTTPS URL policy before it becomes the next
hop. Relative and absolute references remain permitted; absolute references
can change host, so every resulting hop still receives an independent context,
globally reachable connected-peer check, service-identity check, TLS-session
check, framing check, and bounded exact-byte validation.

Malformed, unavailable, unsupported, or raising status observations use the
stable, content-silent `public_release.request_failed` code. Invalid Location
metadata or resolution uses `public_release.redirect_failed`. A supported
local inspection or resolution exception remains chained as its cause. Every
redirect repeats the complete validation.

## Boundary

M56 uses documented `HTTPResponse.status` and `getheaders()` surfaces. It does
not inspect private parser state, parse raw HTTP headers, implement general URI
normalization, add a host allowlist, or claim that `urljoin()` is itself a
validator. It does not reject an absolute redirect merely because its host
differs; M49-M54 per-hop peer, identity, context, freshness, and session checks
remain the authority boundary.

M56 changes no workflow, runner allocation, action, permission, trigger,
credential, release mutation, release authority, dependency, lock, version,
runtime package, or public API. It adds no proxy, DNS preflight, network
sandbox, retry, cache, cleanup, alternate HTTP client, raw parser, or general
SSRF or request-smuggling claim.

Fixture and pull-request evidence are not a real public release observation,
independent or external verification, proof for every intermediary or origin,
future availability, immutability, artifact security, PyPI availability, or a
supported channel. A real M56 pass remains pending an explicitly authorized
signed-tag release run.

## Consequences

- Float, boolean, string, absent, container, and out-of-range status values
  fail before redirect or body use.
- A redirect has one unambiguous Location field and one bounded reference using
  the accepted character and percent-escape subset before URL resolution.
- Valid relative references, cross-host absolute references, percent escapes,
  and exactly 8,000-octet references remain supported.
- Existing direct-`200`, bounded-`302`, per-hop TLS/peer, exact-byte, timeout,
  output, and installed-smoke behavior remains authoritative.

## Alternatives considered

- Continue using joined `getheader("Location")`. Rejected because RFC 9110
  defines one field value and notes that recovering multiple field lines after
  combination is difficult and non-interoperable.
- Treat `urljoin()` as validation. Rejected because Python explicitly says URL
  parsing functions do not validate and warns that an absolute reference can
  replace the base authority.
- Add a redirect-host allowlist. Rejected because the public asset delivery
  authority can vary; the existing actual-peer and TLS identity checks are the
  portable per-hop boundary.
- Reject every cross-host redirect. Rejected because GitHub's documented asset
  retrieval flow uses redirects to delivery origins.

## References

- [Python 3.14 `http.client`](https://docs.python.org/3.14/library/http.client.html)
- [Python 3.14 `urllib.parse` security guidance](https://docs.python.org/3.14/library/urllib.parse.html#url-parsing-security)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 3986: URI Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986.html)
