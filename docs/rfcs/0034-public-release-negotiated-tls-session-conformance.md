# RFC-0034: Constrain negotiated public release TLS sessions

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M51

## Context

M50 constructs and validates an explicit client TLS context for every fixed
public API or bounded asset-redirect hop. That proves the requested trust,
protocol-minimum, certificate, hostname, X.509, and key-log properties before
connection, but it does not inspect the actual negotiated session established
with the peer.

Supported CPython exposes the negotiated protocol through
`SSLSocket.version()`, the active cipher through `SSLSocket.cipher()`, TLS
compression through `SSLSocket.compression()`, and the negotiated application
protocol through `SSLSocket.selected_alpn_protocol()`. A custom context passed
to `HTTPSConnection` also owns its ALPN advertisement. The portable verifier
can therefore fail closed on a small, explicit HTTP/1.1 session contract before
transmitting an HTTP method, path, or header.

## Decision

The M50 context advertises only `http/1.1` through ALPN. After the M49 actual
connected-peer check and before every HTTP request, the verifier must require:

1. an actual negotiated version exactly equal to `TLSv1.2` or `TLSv1.3`;
2. a three-field cipher report containing a non-empty cipher name, a non-empty
   protocol-that-defines-the-cipher field, and an integer secret-bit count of
   at least 128;
3. no negotiated TLS compression; and
4. negotiated ALPN equal to `http/1.1` or `None` when the server did not
   negotiate ALPN.

The cipher report's protocol field is not required to equal the negotiated TLS
version because Python documents it as the protocol version that defines the
cipher. The verifier deliberately has no cipher-name allowlist.

The exact TLSv1.2/TLSv1.3 set is the current supported contract. A future
protocol label, including a future TLS version, requires a reviewed decision
and conformance evidence rather than being accepted implicitly.

## Ordering, failure, and ownership

`HTTPSConnection.connect()` performs the TLS handshake. M49 then validates the
actual port-443 peer, and M51 inspects the resulting socket before
`HTTPSConnection.request()` can send HTTP data. The same ordering repeats for
the fixed API host and every bounded redirect hop.

A missing socket or session accessor, unsupported accessor, malformed value,
unexpected version, weak or malformed cipher report, enabled compression, or
unexpected ALPN fails with the stable, content-silent
`public_release.tls_failed` code. Internal exception chaining retains an
available local cause. The existing connection close path remains
authoritative on every success or failure.

## Authority and non-scope

M51 changes no workflow, runner allocation, action, permission, trigger,
credential, release mutation, publication, retry, rollback, cleanup,
dependency, lock, version, runtime package, or public API. It adds no
cipher-name allowlist, custom CA bundle, certificate/SPKI pin, client
certificate, OCSP/CRL policy, TLS fingerprint, session reuse or ticket policy,
channel binding, certificate-chain export, proxy, or new network path.

Fixture and pull-request conformance are not a real public release observation,
independent or external verification, every CDN/geographic path, future-
availability proof, immutability proof, artifact-security result, PyPI
availability, or a supported release channel. No real M51 signed-tag execution
is performed or claimed.

## Alternatives rejected

- Rely only on the configured TLS minimum. Rejected because it does not verify
  the actual session selected for the request.
- Accept any non-empty protocol reported by the socket. Rejected because an
  unreviewed future or legacy label would silently widen the contract.
- Require one exact cipher suite. Rejected because modern platform TLS stacks
  negotiate several acceptable suites and no maintained cipher-name policy is
  established here.
- Require ALPN `http/1.1` unconditionally. Rejected because a valid HTTPS peer
  may omit ALPN while still serving HTTP/1.1; any explicit result other than
  `http/1.1` remains rejected.
- Add another workflow or runner. Rejected because the shared standard-library
  verifier owns the behavior on all supported platforms.

## Sources

- [Python 3.14 `SSLSocket.version`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.version)
- [Python 3.14 `SSLSocket.cipher`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.cipher)
- [Python 3.14 `SSLSocket.compression`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.compression)
- [Python 3.14 `SSLSocket.selected_alpn_protocol`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.selected_alpn_protocol)
- [Python 3.14 `HTTPSConnection`](https://docs.python.org/3.14/library/http.client.html#http.client.HTTPSConnection)
