# RFC-0038: Constrain public release HTTP response framing

- **Status:** Accepted
- **Date:** 2026-08-10
- **Owners:** LudoWeave maintainers
- **Milestone:** M55

## Context

M48 constrains response status, redirects, headers, timeouts, and bounded body
reads. M49-M54 establish connected-peer and TLS evidence before transmission.
The verifier did not yet inspect the documented response-version and framing
metadata returned by Python's HTTP client before using status, redirect, or
body data.

Python documents `HTTPResponse.version` as integer `10` for HTTP/1.0 and `11`
for HTTP/1.1. CPython's parser also normalizes other raw `HTTP/1.x` status-line
tokens into value `11`, so this public property is a compatibility bucket and
not exact status-line token evidence. Python documents `getheader()` as joining
repeated header values with `, `. RFC 9112 defines HTTP/1.1 message framing,
requires clients that receive transfer coding to accept only a final `chunked`
coding, and treats a message carrying both `Transfer-Encoding` and
`Content-Length` as potentially ambiguous. The standard-library client decodes
valid chunked bodies before its public `read()` result reaches the verifier.

## Decision

After `getresponse()` and before status, redirect, or body use, every fixed API
and bounded redirected asset response must:

1. expose `version` as an integer, but not a boolean, equal to the documented
   HTTP/1.1-class value `11`;
2. expose `Transfer-Encoding` as absent or a string equal to `chunked` under
   case-insensitive comparison;
3. reject every other or repeated transfer-coding value;
4. reject any response carrying both `Transfer-Encoding` and
   `Content-Length`; and
5. expose `Content-Length`, when present, as a string before the existing
   ASCII-decimal, maximum-size, and exact-size checks apply.

Every redirect repeats this validation before its status or `Location` is
used. A malformed, unsupported, ambiguous, missing, or raising metadata
observation fails content-silently under `public_release.request_failed`; an
available supported accessor exception is chained as its cause. A valid
chunked response continues through the existing deadline-aware, byte-bounded
decoded-body reader.

## Boundary

M55 uses only documented `HTTPResponse.version` and `getheader()` surfaces. It
does not inspect private `chunked`, `length`, or `will_close` implementation
state, parse chunks, implement HTTP, alter connection ownership, or replace the
standard library's decoder. Consequently, value `11` is not proof that the raw
status-line token was exactly `HTTP/1.1`; CPython may normalize another
`HTTP/1.x` token to the same documented value. Duplicate `Content-Length`
values joined by `getheader()` remain rejected by the existing size syntax
check.

M55 changes no workflow, runner allocation, action, permission, trigger,
credential, release mutation, release authority, dependency, lock, version,
runtime package, or public API. It adds no alternate client, HTTP/2 or HTTP/3,
proxy, retry, decompression, cache, network sandbox, or general request-
smuggling defense.

Fixture and pull-request evidence are not a real public release observation,
independent or external verification, proof for every intermediary or origin,
future availability, immutability, artifact security, PyPI availability, or a
supported channel. A real M55 pass remains pending an explicitly authorized
signed-tag release run.

## Consequences

- HTTP/1.0 and every observed response-version value other than integer `11`
  fail closed; exact raw status-line identity remains unclaimed.
- Valid HTTP/1.1 fixed-length, chunked, and connection-delimited responses
  retain the existing bounded-body behavior.
- Transfer-coding lists, repeated codings, and framing ambiguity fail before
  status, redirect, or body data is consumed.
- Existing M54-M47 TLS, peer, response, artifact, and installed-smoke
  boundaries remain authoritative.

## Alternatives considered

- Accept documented value `10`. Rejected because the release client deliberately
  negotiates and transmits HTTP/1.1 and needs one explicit public-property
  contract.
- Inspect private `HTTPResponse` framing attributes. Rejected because they are
  implementation details rather than the documented public API.
- Parse raw response headers or chunk framing independently. Rejected because
  it would duplicate the standard-library HTTP implementation and materially
  widen scope and risk.
- Claim protection against all HTTP request-smuggling paths. Rejected because
  this client-side response check addresses only its observed framing boundary.

## References

- [Python 3.14 `http.client`](https://docs.python.org/3.14/library/http.client.html)
- [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html)
