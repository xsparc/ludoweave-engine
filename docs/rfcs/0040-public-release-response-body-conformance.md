# RFC-0040: Constrain public release response bodies

- **Status:** Accepted
- **Date:** 2026-08-10
- **Owners:** LudoWeave maintainers
- **Milestone:** M57

## Context

M48-M56 validate request failures, connected peers, TLS, HTTP framing, status,
and redirect references before consuming a public release response body. The
streaming loop still trusted the annotated return from
`HTTPResponse.read(amount)`. A malformed or unsupported response object could
return text, a mutable buffer, no value, or more than the requested amount;
those shapes could escape as raw exceptions or be accepted as response data.

The release-document path also has no pre-known byte count. Although M55
validates `Content-Length` syntax and bounds before streaming, that path did not
compare a declared length with the number of octets actually read. A truncated
or overlong declared body could therefore reach the later document validator
without first failing the HTTP size boundary.

Python documents `HTTPResponse` as a binary buffered reader and
`read(amount)` as returning the response body up to the requested number of
bytes. RFC 9112 defines an HTTP message body as octets and requires a response
with `Content-Length` to contain exactly that declared number of octets; a
shorter message is incomplete.

## Decision

Every successful response body read must return an immutable `bytes` block no
larger than the positive requested amount. The check occurs immediately after
each read and before EOF interpretation, length accounting, or local output.
Text, mutable buffers, memory views, booleans, absent values, and oversized
blocks fail closed.

If M55 exposes a `Content-Length`, M57 retains its validated integer and,
after EOF, requires the total streamed octets to equal that declaration. This
applies to both the public release document and every successful response
after an asset redirect. Existing pre-known asset sizes remain independently
required whether or not a response declares a length.

A malformed block or supported read-shape/access failure uses stable,
content-silent `public_release.request_failed`. A declared-versus-streamed
length mismatch uses `public_release.size_mismatch`. Supported local read
exceptions remain chained. Existing timeout, transport, output, byte-limit,
and exact-artifact failures retain their established codes and ordering.

## Boundary

M57 uses only documented `HTTPResponse.read(amount)` results and the already
validated M55 `Content-Length`. It does not inspect private response or socket
state, parse raw HTTP or chunks, decode content, add an alternate client,
require a new response header, or claim general completeness for an unframed
close-delimited response. It does not change redirect-body handling: only an
accepted final `200` body is streamed.

M57 adds no cleanup or rollback, retry, cache, proxy, DNS preflight, network
sandbox, workflow, runner allocation, action, permission, trigger, credential,
release mutation, release authority, dependency, lock, version, runtime
package, public API, or supported-channel decision.

Fixture and pull-request evidence are not a real public release observation,
independent or external verification, proof for every intermediary or origin,
future availability, immutability, artifact security, PyPI availability, or a
supported channel. A real M57 pass remains pending an explicitly authorized
signed-tag release run.

## Consequences

- Malformed body values fail before they can be treated as EOF, counted, or
  written.
- A response cannot satisfy the reader with more bytes than one read request.
- Any declared `Content-Length` is checked against actual streamed octets for
  the release document as well as assets.
- Valid short reads, zero-length EOF, chunked decoding through `http.client`,
  close-delimited responses without a declared length, and existing exact
  asset-size checks remain supported.

## Alternatives considered

- Trust `HTTPResponse` annotations. Rejected because this verifier treats
  malformed or unsupported runtime observations as untrusted boundary data and
  promises structured failures.
- Convert arbitrary bytes-like values with `bytes()`. Rejected because it
  silently accepts an undocumented response shape and can copy attacker-sized
  data before the requested-amount check.
- Require `Content-Length` on every response. Rejected because HTTP/1.1 also
  supports chunked and close-delimited responses; M57 constrains declarations
  that exist without inventing a new provider requirement.
- Implement a raw HTTP or chunk parser. Rejected because the standard-library
  client remains the owned parser boundary and existing parser failures are
  already mapped content-silently.

## References

- [Python 3.14 `http.client`](https://docs.python.org/3.14/library/http.client.html)
- [Python 3.14 binary I/O](https://docs.python.org/3.14/library/io.html#binary-i-o)
- [RFC 9112: HTTP/1.1 message body length](https://www.rfc-editor.org/rfc/rfc9112.html#section-6.3)
- [RFC 9112: incomplete messages](https://www.rfc-editor.org/rfc/rfc9112.html#section-8)
